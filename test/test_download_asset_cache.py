"""配布アセットの共有・部分修復・通信実績と、npm のオフライン構築を検査する。

正本: oracle/doc/app_spec/download_asset_cache.md の「診断と受入条件」。
"""

import base64
import fcntl
import gzip
import hashlib
import io
import json
import multiprocessing
import shutil
import subprocess
import tarfile
import urllib.error
import urllib.request
from dataclasses import replace
from importlib import resources
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import unquote, urlsplit

import pytest
from _cli_support import runner, terminal_primary_report
from _download_asset_support import (
    download_response,
    http_distribution_opener,
    process_obtain,
)

import commons.runtime_cli as cli_module
import commons.runtime_doctor as doctor_module
import commons.runtime_document_search as search_module
import commons.runtime_document_search_assets as assets
import commons.runtime_document_search_setup as setup
import commons.runtime_download_asset_cache as cache_module
import commons.runtime_logging as logging_module
from commons.runtime_document_search import SearchError
from commons.runtime_download_asset_cache import DownloadAsset, DownloadAssetCache
from commons.runtime_logging import (
    SubcommandLogger,
    reset_current_subcommand_logger,
    set_current_subcommand_logger,
)
from commons.runtime_primary_report_render import render_primary_report
from commons.runtime_primary_report_specs import primary_report_spec
from commons.runtime_results import TerminalResult
from main import app


@pytest.fixture
def distribution(monkeypatch):
    """HTTP transport の応答を置換し、urllib の redirect と通信記録を通す。"""
    bodies = {"/model": b"model bytes", "/dependency": b"dependency bytes"}
    requests = []

    def transport(_handler, request):
        path = urlsplit(request.full_url).path
        requests.append(path)
        if path == "/redirect":
            return download_response(request.full_url, b"", 302, "/model")
        return download_response(
            request.full_url, bodies.get(path, b""), 200 if path in bodies else 503
        )

    monkeypatch.setattr(urllib.request, "build_opener", http_distribution_opener())
    monkeypatch.setattr(urllib.request.HTTPHandler, "http_open", transport)
    return "http://distribution.invalid", bodies, requests


def _asset(distribution, path="/model"):
    url, bodies, _requests = distribution
    body = bodies[path]
    return DownloadAsset(
        name=path,
        url=url + path,
        integrity="sha256-" + base64.b64encode(hashlib.sha256(body).digest()).decode(),
        identity={"version": "1", "os": "linux", "cpu": "x64"},
        size_bytes=len(body),
    )


@pytest.fixture
def asset_logger(tmp_path, nonpersistent_execution_ids):
    """資材と実行 ID の対応を保ち、採番 DB の初期化・同期書き込みを省く。"""
    # 採番の永続性は test_runtime_ids.py、実 logger との結合は
    # test_runtime_cli.py の test_subcommand_logger_keeps_one_file_per_execution に残す。
    logger = SubcommandLogger(tmp_path, "doctor")
    token = set_current_subcommand_logger(logger)
    try:
        yield logger
    finally:
        reset_current_subcommand_logger(token)


@pytest.fixture
def asset_events(asset_logger, monkeypatch):
    """実ファイルと logger の状態を検査し、重複するディスク追記・同期を省く。"""
    # 保存・report との結合は redirect と doctor の専用ケースに残す。
    monkeypatch.setattr(logging_module, "append_log_record", lambda *_args: None)
    # 実 fsync による取得・公開は並行取得・redirect・doctor のケースに残す。
    # ここでも write・flush・rename と保存内容・完全性の照合は実行する。
    monkeypatch.setattr(cache_module.os, "fsync", lambda _fd: None)
    return asset_logger


def _states(logger):
    latest = {}
    for event in logger.event_records():
        if event["event"] == "asset.state":
            latest[event["use_id"]] = event
    return list(latest.values())


def _forbid_download(*_args, **_kwargs):
    raise AssertionError("a reusable asset must not attempt external communication")


@pytest.mark.parametrize("damage", ["content", "identity", "size", "version"])
def test_only_invalid_asset_is_downloaded(tmp_path, distribution, damage, asset_events):
    """不適合な一資材だけ再取得し、他の資材と別版を保持する。"""
    first, second = _asset(distribution), _asset(distribution, "/dependency")
    cache = DownloadAssetCache(tmp_path / "cmoc-a")
    cache.obtain(first, tmp_path / "model-a")
    cache.obtain(second, tmp_path / "dependency-a")
    entry = cache_module.asset_cache_directory() / first.key
    requested = first
    if damage == "content":
        (entry / "content").write_bytes(b"bad")
    elif damage in ("identity", "size"):
        receipt = json.loads((entry / "receipt.json").read_text())
        if damage == "identity":
            receipt["asset"]["identity"]["version"] = "different"
        else:
            receipt["size_bytes"] += 1
        (entry / "receipt.json").write_text(json.dumps(receipt))
    else:
        requested = replace(first, identity={**first.identity, "version": "2"})
    cache = DownloadAssetCache(tmp_path / "other-repository/other-cmoc")
    cache.obtain(requested, tmp_path / "model-b")
    cache.obtain(second, tmp_path / "dependency-b")
    assert distribution[2] == ["/model", "/dependency", "/model"]
    assert (tmp_path / "model-b").read_bytes() == distribution[1]["/model"]
    assert _states(asset_events)[-1]["download_count"] == 0
    if damage == "version":
        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(urllib.request.OpenerDirector, "open", _forbid_download)
            cache.obtain(first, tmp_path / "original-version")


def test_local_asset_and_cache_loss_are_independent(
    tmp_path, distribution, monkeypatch, asset_events
):
    """導入前の資材を優先し、cache の消失でコピー済み資材を破損させない。"""
    asset = _asset(distribution)
    existing = tmp_path / "existing"
    existing.write_bytes(distribution[1]["/model"])
    cache = DownloadAssetCache(tmp_path)
    with monkeypatch.context() as patch:
        patch.setattr(urllib.request.OpenerDirector, "open", _forbid_download)
        cache.obtain(asset, tmp_path / "prepared", local_sources=(existing,))
    assert not cache_module.asset_cache_directory().exists()
    assert _states(asset_events)[-1]["cache_status"] == "not_checked_local_available"
    cache.obtain(asset, tmp_path / "copied")
    shutil.rmtree(cache_module.asset_cache_directory())
    assert (tmp_path / "copied").read_bytes() == existing.read_bytes()
    cache.obtain(asset, tmp_path / "new", local_sources=(tmp_path / "copied",))
    assert distribution[2] == ["/model"]


def test_publication_failure_preserves_existing_unreadable_cache(
    tmp_path, distribution, monkeypatch, asset_events
):
    """読み取り失敗で再取得しても、公開失敗によって既存保存物を消さない。"""
    asset = _asset(distribution)
    cache = DownloadAssetCache(tmp_path)
    cache.obtain(asset, tmp_path / "first")
    entry = cache_module.asset_cache_directory() / asset.key
    old_receipt = (entry / "receipt.json").read_bytes()
    original_read = Path.read_text
    original_replace = cache_module.os.replace
    with monkeypatch.context() as patch:

        def unreadable(path, *args, **kwargs):
            if path == entry / "receipt.json":
                raise PermissionError("cache read denied")
            return original_read(path, *args, **kwargs)

        def fail_publication(source, destination):
            if Path(source).name.startswith(".incomplete-"):
                raise PermissionError("cache write denied")
            return original_replace(source, destination)

        patch.setattr(Path, "read_text", unreadable)
        patch.setattr(cache_module.os, "replace", fail_publication)
        with pytest.raises(PermissionError, match="cache write denied"):
            cache.obtain(asset, tmp_path / "second")
    assert (entry / "receipt.json").read_bytes() == old_receipt
    assert (entry / "content").read_bytes() == distribution[1]["/model"]
    assert _states(asset_events)[-1]["cache_status"] == "read_failed"
    with monkeypatch.context() as patch:
        patch.setattr(urllib.request.OpenerDirector, "open", _forbid_download)
        cache.obtain(asset, tmp_path / "recovered")


@pytest.mark.parametrize("failure", ["http", "integrity", "publication", "cancel"])
def test_partial_failure_preserves_published_assets(
    tmp_path, distribution, monkeypatch, asset_events, failure
):
    """失敗・取消前の公開済み資材を再取得せず、未完成の保存物を拒否する。"""
    first, second = _asset(distribution), _asset(distribution, "/dependency")
    cache = DownloadAssetCache(tmp_path)
    cache.obtain(first, tmp_path / "first")
    with monkeypatch.context() as patch:
        if failure == "http":
            distribution[1].pop("/dependency")
        elif failure == "integrity":
            distribution[1]["/dependency"] = b"wrong bytes"
        elif failure == "publication":
            original = cache_module.os.replace

            def fail_publish(source, destination):
                if Path(destination).name == second.key:
                    raise OSError("publication denied")
                return original(source, destination)

            patch.setattr(cache_module.os, "replace", fail_publish)
        else:
            patch.setattr(
                cache_module,
                "_download",
                lambda *_args: (_ for _ in ()).throw(KeyboardInterrupt()),
            )
        with pytest.raises(
            (urllib.error.HTTPError, ValueError, OSError, KeyboardInterrupt)
        ):
            cache.obtain(second, tmp_path / "second")
    distribution[1]["/dependency"] = b"dependency bytes"
    failed = _states(asset_events)[-1]
    assert failed["status"] == "failed"
    assert failed["publication"] != "succeeded"
    assert not (cache_module.asset_cache_directory() / second.key).exists()
    cache.obtain(first, tmp_path / "first-again")
    cache.obtain(second, tmp_path / "second-again")
    assert distribution[2].count("/model") == 1
    assert (tmp_path / "second-again").read_bytes() == b"dependency bytes"
    assert not list(cache_module.asset_cache_directory().glob(".incomplete-*"))


def test_parallel_installations_download_once(tmp_path, distribution, monkeypatch):
    """独立 process と異なる cmoc 配置でも、待機後に完成品を再利用する。"""
    # lock は親子の obtain 内で別々に開き、interpreter の再起動だけを省く。
    context = multiprocessing.get_context("fork")
    downloading = context.Event()
    waiting = context.Event()
    asset = _asset(distribution)
    receive, send = context.Pipe(duplex=False)
    destination = tmp_path / "child-result"
    process = context.Process(
        target=process_obtain,
        args=(
            cache_module.asset_cache_directory(),
            tmp_path / "cmoc-child",
            asset,
            destination,
            downloading,
            waiting,
            send,
        ),
    )
    flock = fcntl.flock

    def observe_lock(fd, operation):
        try:
            return flock(fd, operation)
        except BlockingIOError:
            waiting.set()
            raise

    def wait_for_publication(_seconds):
        assert receive.poll(20), "child publication did not finish"

    try:
        process.start()
        send.close()
        assert downloading.wait(10), "child download did not start"
        # 親を二つ目の取得 process とし、実 lock の競合を観測する。
        monkeypatch.setattr(fcntl, "flock", observe_lock)
        # poll 間隔を待たず、lock 解放後の子の通知で再試行する。
        # 待機時間の計測と取消は test_document_search.py の専用 test に残す。
        monkeypatch.setattr(
            search_module,
            "time",
            SimpleNamespace(
                monotonic=cache_module.time.monotonic, sleep=wait_for_publication
            ),
        )
        parent_destination = tmp_path / "parent-result"
        action = DownloadAssetCache(tmp_path / "cmoc-parent").obtain(
            asset, parent_destination
        )
        assert waiting.is_set()
        assert action == "reused"
        assert distribution[2] == []
        assert receive.poll(20)
        assert receive.recv() == ("downloaded", 1)
        process.join(20)
        assert process.exitcode == 0
        assert (
            parent_destination.read_bytes()
            == destination.read_bytes()
            == distribution[1]["/model"]
        )
    finally:
        if process.is_alive():
            process.kill()
            process.join()
        receive.close()
        send.close()
        process.close()


def test_redirect_failure_and_report_preserve_observed_counts(
    tmp_path, distribution, monkeypatch, asset_logger
):
    """取得試行と redirect 通信を分け、遮断された通信も失敗として保存する。"""
    asset = replace(_asset(distribution), url=distribution[0] + "/redirect")
    cache = DownloadAssetCache(tmp_path)
    cache.obtain(asset, tmp_path / "download")
    event = _states(asset_logger)[-1]
    assert event["download_count"] == 1
    assert len(event["communications"]) == 2
    assert [attempt["http_status"] for attempt in event["communications"]] == [302, 200]
    blocked = replace(asset, identity={"version": "blocked"})
    monkeypatch.setattr(
        urllib.request.HTTPHandler,
        "http_open",
        lambda *_args: (_ for _ in ()).throw(OSError("network blocked")),
    )
    with pytest.raises(OSError, match="network blocked"):
        cache.obtain(blocked, tmp_path / "blocked")
    event = _states(asset_logger)[-1]
    assert event["download_count"] == 1
    assert event["communications"][0]["status"] == "failed"
    saved = [json.loads(line) for line in asset_logger.path.read_text().splitlines()]
    # 後続の通信更新で過去の snapshot が変わらず、保存内容と一致することを確認する。
    assert saved == list(asset_logger.event_records())
    assert saved[-1]["execution_id"] == asset_logger.execution_id
    assert saved[-1]["cmoc_root"] == str(tmp_path)
    assert saved[-1]["component"] == "document_search"
    report = render_primary_report(
        primary_report_spec("doctor"), [], "error", TerminalResult(), asset_logger
    )
    assert "資材取得の試行数: 2" in report
    assert "未完了資材:" in report
    assert "network blocked" in report
    assert str(asset_logger.path) in report


def test_doctor_reports_asset_success_separately_from_validation_failure(
    committed_repository, distribution, monkeypatch, nonpersistent_execution_ids
):
    """取得・公開成功を保持し、検証失敗を報告して索引同期前に停止する。"""
    # 前処理に必要な HEAD だけ用意し、使わない初期内容と git add は準備しない。
    # 既存ファイルの Git 修復・commit は test_doctor_cli.py に残す。
    root = committed_repository
    monkeypatch.chdir(root)
    # 資材準備から失敗 report までを通し、TCP 受付は test_feedback.py に残す。
    monkeypatch.setattr(
        cli_module, "start_feedback_invocation", lambda *_args: (None, None)
    )
    asset = _asset(distribution)

    def prepare_and_fail(cmoc_root, _config):
        DownloadAssetCache(cmoc_root).obtain(asset, root / "copied-model")
        raise SearchError("MODEL_FAILURE", "real-model validation failed")

    monkeypatch.setattr(
        doctor_module, "prepare_document_search_materials", prepare_and_fail
    )
    result = runner.invoke(app, ["doctor"], catch_exceptions=False)
    assert result.exit_code != 0
    report = terminal_primary_report(result).read_text()
    assert 'terminal_classification: "error"' in report
    assert "照合と実モデル検証: `失敗`" in report
    assert "資材取得の試行数: 1" in report
    assert "有効キャッシュの公開数: 1" in report
    assert "real-model validation failed" in report
    assert "cmoc doctor を再実行" in report
    assert (
        cache_module.asset_cache_directory() / asset.key / "content"
    ).read_bytes() == distribution[1]["/model"]
    [log_path] = (root / ".cmoc/gu/log/sub_command").glob("*.jsonl")
    events = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert not any(
        event["event"].startswith("document_search_sync_") for event in events
    )


def _tarball(name, dependencies=None, version="1.0.0"):
    package = {
        "name": name,
        "version": version,
        "dependencies": dependencies or {},
        "scripts": {
            "preinstall": "node -e 'throw Error(\"scripts must be disabled\")'"
        },
    }
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode="w") as archive:
        for path, body in (
            ("package.json", json.dumps(package).encode()),
            ("index.js", b"export default 1;"),
        ):
            info = tarfile.TarInfo("package/" + path)
            info.size = len(body)
            archive.addfile(info, io.BytesIO(body))
    return gzip.compress(output.getvalue(), mtime=0)


def test_node_preparation_uses_adopted_distribution_without_system_node(
    tmp_path, distribution, monkeypatch
):
    """固定配布物の初回取得、別配置での再利用、cache 消失後のローカル再利用を通す。"""
    package = json.loads(
        resources.files("commons.document_search_worker")
        .joinpath("package.json")
        .read_text()
    )
    adopted = package["cmoc"]["node_distribution"]
    filename = adopted["filename"]
    directory = filename.removesuffix(".tar.xz")
    output = io.BytesIO()
    # 内容照合・展開の検査用なので、fixture の圧縮には最小 preset を使う。
    with tarfile.open(fileobj=output, mode="w:xz", preset=0) as archive:
        for name in ("bin/node", "lib/node_modules/npm/bin/npm-cli.js"):
            body = name.encode()
            info = tarfile.TarInfo(f"{directory}/{name}")
            info.size, info.mode = len(body), 0o755
            archive.addfile(info, io.BytesIO(body))
    body = output.getvalue()
    distribution[1]["/node.tar.xz"] = body
    adopted.update(
        url=distribution[0] + "/node.tar.xz",
        size_bytes=len(body),
        sha256=hashlib.sha256(body).hexdigest(),
    )
    monkeypatch.setenv("PATH", "")

    def prepare(name, previous):
        root = tmp_path / name
        root.mkdir()
        (root / "package.json").write_text(json.dumps(package))
        assets.prepare_node_runtime(root, previous, root)
        assert (root / "node/bin/node").read_bytes() == b"bin/node"
        assert (root / "node/lib/node_modules/npm/bin/npm-cli.js").is_file()
        return root

    first = prepare("first", tmp_path / "missing")
    monkeypatch.setattr(urllib.request.OpenerDirector, "open", _forbid_download)
    prepare("second", tmp_path / "missing")
    shutil.rmtree(cache_module.asset_cache_directory())
    prepare("local", first)
    assert distribution[2] == ["/node.tar.xz"]
    assert not cache_module.asset_cache_directory().exists()


def _npm_fixture(base, distribution):
    base.mkdir(parents=True)
    url, bodies, _requests = distribution
    bodies["/a.tgz"] = _tarball("asset-a", {"asset-b": "1.0.0"})
    bodies["/b.tgz"] = _tarball("asset-b")
    package = {
        "name": "fixture",
        "version": "1.0.0",
        "dependencies": {"asset-a": "1.0.0"},
    }
    packages = {"": package}
    for name, path in (("asset-a", "/a.tgz"), ("asset-b", "/b.tgz")):
        packages["node_modules/" + name] = {
            "version": "1.0.0",
            "resolved": url + path,
            "integrity": "sha512-"
            + base64.b64encode(hashlib.sha512(bodies[path]).digest()).decode(),
            **({"dependencies": {"asset-b": "1.0.0"}} if name == "asset-a" else {}),
        }
    (base / "package.json").write_text(json.dumps(package))
    lock = {
        "name": "fixture",
        "version": "1.0.0",
        "lockfileVersion": 3,
        "packages": packages,
    }
    (base / "package-lock.json").write_text(json.dumps(lock))
    return (base / "package-lock.json").read_bytes()


def test_npm_build_reuses_all_dependencies_without_network(
    tmp_path, distribution, monkeypatch, asset_events
):
    """取得資材を照合し、別配置の cold build を実 npm で通信なしに完了する。"""
    system_node, system_npm = shutil.which("node"), shutil.which("npm")
    if not system_node or not system_npm:
        pytest.skip("Node and npm are required for offline asset preparation")
    # Node の socket 境界で通信を禁止し、試行もファイルから検出する。
    attempted = tmp_path / "network-attempts"
    guard = tmp_path / "guard.cjs"
    guard.write_text(
        "const fs=require('fs');require('net').Socket.prototype.connect=function(){"
        f"fs.appendFileSync({json.dumps(str(attempted))},'attempt\\n');"
        "throw Error('network forbidden');};"
    )
    monkeypatch.setenv("NODE_OPTIONS", f"--require={guard}")
    monkeypatch.setenv("npm_config_registry", distribution[0])

    # 制約のない tarball の取得では Node を起動せず、実 platform は後段で検査する。
    root = tmp_path / "cmoc-download"
    base = root / "build"
    original = _npm_fixture(base, distribution)
    with monkeypatch.context() as acquisition:
        acquisition.setattr(
            assets,
            "_npm_platform",
            lambda _base: {"os": "linux", "cpu": "x64", "libc": "glibc"},
        )
        with assets.node_runtime_assets(root, base):
            lock = json.loads((base / "package-lock.json").read_text())
            for name, path in (("asset-a", "/a.tgz"), ("asset-b", "/b.tgz")):
                resolved = urlsplit(
                    lock["packages"]["node_modules/" + name]["resolved"]
                )
                assert resolved.scheme == "file"
                assert (
                    Path(unquote(resolved.path)).read_bytes() == distribution[1][path]
                )
    assert (base / "package-lock.json").read_bytes() == original
    assert not (base / ".assets").exists()
    assert all(event["source"] == "download" for event in _states(asset_events))

    # 同じ依存物の npm 構築は、全資材を再利用する別配置の cold build で一度通す。
    root = tmp_path / "cmoc-cached"
    base = root / "build"
    original = _npm_fixture(base, distribution)
    # 実 Node/npm は、この cold build でだけ用意する。
    node = base / "node/bin/node"
    node.parent.mkdir(parents=True)
    node.symlink_to(system_node)
    npm = base / "node/lib/node_modules/npm"
    npm.parent.mkdir(parents=True)
    npm.symlink_to(Path(system_npm).resolve().parent.parent)
    monkeypatch.setattr(urllib.request.OpenerDirector, "open", _forbid_download)
    with (root / "lock").open("w") as descriptor:
        try:
            setup._install_node_runtime(root, base, descriptor.fileno())
        except subprocess.CalledProcessError as exc:
            pytest.fail(f"offline npm failed:\n{exc.stderr}\n{exc.stdout}")
    assert (base / "node_modules/asset-a/index.js").is_file()
    assert (base / "node_modules/asset-b/index.js").is_file()
    assert (base / "package-lock.json").read_bytes() == original
    assert not (base / ".assets").exists()
    assert not attempted.exists()
    assert distribution[2] == ["/a.tgz", "/b.tgz"]
    assert sum(event["download_count"] for event in _states(asset_events)) == 2
    assert all(event["source"] == "cache" for event in _states(asset_events)[-2:])


def test_npm_uses_preexisting_cache_and_platform_pins(
    tmp_path, distribution, monkeypatch, asset_events
):
    """同一資材を共有し、同名の別版と異なる OS/CPU の optional 資材を区別する。"""
    # platform の実取得と npm への受け渡しは、通信禁止の実 npm test で通す。
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(
        assets,
        "_npm_platform",
        lambda _base: {"os": "linux", "cpu": "x64", "libc": "glibc"},
    )
    root = tmp_path / "cmoc"
    base = root / "build"
    _npm_fixture(base, distribution)
    lock = json.loads((base / "package-lock.json").read_text())
    nested_name = "node_modules/asset-a/node_modules/asset-b"
    versioned_name = "node_modules/asset-b/node_modules/asset-b"
    # 同一 tarball の共有と同名別版の区別を、一つの lock で検査する。
    lock["packages"][nested_name] = dict(lock["packages"]["node_modules/asset-b"])
    body = _tarball("asset-b", version="2.0.0")
    distribution[1]["/b-2.tgz"] = body
    lock["packages"][versioned_name] = {
        "version": "2.0.0",
        "resolved": distribution[0] + "/b-2.tgz",
        "integrity": "sha512-"
        + base64.b64encode(hashlib.sha512(body).digest()).decode(),
    }
    seeded = set()
    for package in lock["packages"].values():
        if "integrity" in package and package["integrity"] not in seeded:
            local = assets._npm_local_source(
                base.parent / "npm-cache", package["integrity"]
            )
            local.parent.mkdir(parents=True)
            local.write_bytes(
                distribution[1][package["resolved"].removeprefix(distribution[0])]
            )
            seeded.add(package["integrity"])
    lock["packages"]["node_modules/alien"] = {
        "version": "1.0.0",
        "integrity": "sha512-unused",
        "resolved": distribution[0] + "/alien",
        "os": ["alien-os"],
        "cpu": ["alien-cpu"],
        "optional": True,
    }
    (base / "package-lock.json").write_text(json.dumps(lock))
    original = (base / "package-lock.json").read_bytes()
    monkeypatch.setattr(urllib.request.OpenerDirector, "open", _forbid_download)
    with assets.node_runtime_assets(root, base):
        local_lock = json.loads((base / "package-lock.json").read_text())
        assert local_lock["packages"]["node_modules/asset-a"]["resolved"].startswith(
            "file:"
        )
        assert local_lock["packages"]["node_modules/alien"]["resolved"].endswith(
            "/alien"
        )
        direct = local_lock["packages"]["node_modules/asset-b"]["resolved"]
        nested = local_lock["packages"][nested_name]["resolved"]
        versioned = local_lock["packages"][versioned_name]["resolved"]
        assert direct == nested
        assert direct != versioned
        assert Path(unquote(urlsplit(versioned).path)).read_bytes() == body
    # 一度検証・コピーした tarball の準備を、lock の参照数だけ繰り返さない。
    states = _states(asset_events)
    assert len(states) == len(seeded)
    assert all(event["source"] == "local" for event in states)
    assert (base / "package-lock.json").read_bytes() == original
    assert not (base / ".assets").exists()

    # 前回の成功を次の準備へ持ち越さず、破損時も lock と一時資材を回収する。
    local = assets._npm_local_source(
        base.parent / "npm-cache",
        lock["packages"]["node_modules/asset-b"]["integrity"],
    )
    local.write_bytes(b"corrupted")
    with pytest.raises(AssertionError, match="must not attempt external communication"):
        with assets.node_runtime_assets(root, base):
            pytest.fail("a corrupted tarball was accepted")
    assert (base / "package-lock.json").read_bytes() == original
    assert not (base / ".assets").exists()
    assert distribution[2] == []
