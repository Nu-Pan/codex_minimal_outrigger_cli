"""配布アセットをユーザー単位で検証・排他取得し、独立したコピーを渡す。"""

import base64
import copy
import hashlib
import json
import os
import shutil
import tempfile
import time
import urllib.request
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from .runtime_document_search import SearchError, _file_lock, _safe_directory
from .runtime_logging import current_subcommand_logger


def asset_cache_directory() -> Path:
    """配置場所と repository に依存しない、数値 UID ごとの保存先を返す。"""
    # oracle/doc/app_spec/download_asset_cache.md の保存先。
    return Path("/tmp/cmoc_asset_cache") / str(os.getuid())


@dataclass(frozen=True)
class DownloadAsset:
    """取得元とローカル検証に必要な固定識別情報を一緒に保持する。"""

    name: str
    url: str
    integrity: str
    identity: dict[str, object]
    size_bytes: int | None = None

    @property
    def key(self) -> str:
        """要求資材の内容・版・適合条件を識別する。"""
        # component の配置先や動作検証条件は取得資材の identity に混ぜない。
        return hashlib.sha256(
            json.dumps(asdict(self), sort_keys=True).encode("utf-8")
        ).hexdigest()

    def check(self, path: Path) -> str:
        """保存物の存在と完全性を確認し、不適合の理由を返す。"""
        # 正本のサイズ・hash をすべて照合する。npm は lock の SRI を使う。
        try:
            if path.is_symlink():
                return "integrity_failed"
            if not path.is_file():
                return "missing"
            if self.size_bytes is not None and path.stat().st_size != self.size_bytes:
                return "integrity_failed"
            digests = []
            for item in self.integrity.split():
                algorithm, encoded = item.split("-", 1)
                digests.append(
                    (hashlib.new(algorithm), base64.b64decode(encoded, validate=True))
                )
            if not digests:
                raise ValueError("asset integrity is unspecified")
            with path.open("rb") as source:
                while block := source.read(1024 * 1024):
                    for digest, _expected in digests:
                        digest.update(block)
            if any(digest.digest() != expected for digest, expected in digests):
                return "integrity_failed"
        except OSError:
            return "read_failed"
        return "valid"


def record_asset_event(kind: str, root: Path, **payload: object) -> None:
    """doctor の最外側ログへ、コンポーネントと配置場所を対応付けて即時記録する。"""
    # logger が実行 ID とサブコマンドを補う。本文や認証情報は記録しない。
    logger = current_subcommand_logger()
    if logger is not None:
        logger.event(kind, cmoc_root=str(root), component="document_search", **payload)


class _AssetUse:
    def __init__(self, root: Path, asset: DownloadAsset, destination: Path) -> None:
        # 終端のない強制終了も requested/downloading のまま識別できるようにする。
        self.root = root
        self.fields: dict[str, object] = {
            "use_id": uuid.uuid4().hex,
            "asset_key": asset.key,
            "asset": asdict(asset),
            "destination": str(destination),
            "download_count": 0,
            "communications": [],
            "cache_status": "not_checked",
            "publication": "not_attempted",
        }
        self.communications: list[dict[str, object]] = []
        self.event(status="requested")

    def event(self, **fields: object) -> None:
        # snapshot は後続更新で過去の in-memory 記録が変わらないようにする。
        self.fields.update(fields)
        self.fields["communications"] = self.communications
        record_asset_event("asset.state", self.root, **copy.deepcopy(self.fields))


class _CommunicationRecorder(urllib.request.BaseHandler):
    handler_order = 499

    def __init__(self, use: _AssetUse) -> None:
        # redirect ごとの request/response も同じ資材取得へ関連付ける。
        self.use = use

    def http_request(self, request: urllib.request.Request) -> urllib.request.Request:
        # 署名付き redirect の query と fragment は診断へ残さない。
        parsed = urlsplit(request.full_url)
        self.use.communications.append(
            {
                "kind": "asset_body",
                "url": urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", "")),
                "status": "started",
            }
        )
        self.use.event(status="downloading")
        return request

    def http_response(
        self, request: urllib.request.Request, response: object
    ) -> object:
        self.use.communications[-1].update(
            status="succeeded" if getattr(response, "status") < 400 else "failed",
            http_status=getattr(response, "status"),
        )
        self.use.event(status="downloading")
        return response

    https_request = http_request
    https_response = http_response


def _download(asset: DownloadAsset, path: Path, use: _AssetUse) -> None:
    # 一回の取得試行内の redirect 通信を、取得回数とは別に数える。
    use.event(status="downloading", download_count=1)
    try:
        opener = urllib.request.build_opener(_CommunicationRecorder(use))
        with opener.open(asset.url, timeout=60) as source, path.open("wb") as output:
            size = 0
            while block := source.read(1024 * 1024):
                output.write(block)
                size += len(block)
                if asset.size_bytes is not None and size > asset.size_bytes:
                    raise ValueError(f"asset exceeds fixed size: {asset.name}")
            output.flush()
            os.fsync(output.fileno())
    except BaseException as exc:
        if use.communications and use.communications[-1]["status"] == "started":
            use.communications[-1].update(status="failed", reason=str(exc))
        use.event(status="failed", failure=str(exc))
        raise


def _cache_status(entry: Path, asset: DownloadAsset) -> str:
    # receipt の識別情報とサイズも照合し、存在だけでは hit にしない。
    try:
        if entry.is_symlink():
            return "identity_mismatch"
        receipt = entry / "receipt.json"
        if receipt.is_symlink():
            return "identity_mismatch"
        if not receipt.is_file():
            return "missing"
        saved = json.loads(receipt.read_text(encoding="utf-8"))
        if not isinstance(saved, dict) or saved.get("asset") != asdict(asset):
            return "identity_mismatch"
        status = asset.check(entry / "content")
        if status != "valid":
            return status
        if saved.get("size_bytes") != (entry / "content").stat().st_size:
            return "integrity_failed"
        return "valid"
    except OSError:
        return "read_failed"
    except ValueError:
        return "identity_mismatch"


def _remove_entry(path: Path) -> None:
    # symlink は参照先を辿らず、その path だけを取り除く。
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


class DownloadAssetCache:
    """資材ごとに取得・確認・公開・コピーを排他し、公開済みの資材を保持する。"""

    def __init__(self, cmoc_root: Path) -> None:
        """使用する cmoc 配置を診断に残し、共有キャッシュとは区別する。"""
        self.cmoc_root = cmoc_root

    def obtain(
        self,
        asset: DownloadAsset,
        destination: Path,
        *,
        local_sources: tuple[Path, ...] = (),
    ) -> str:
        """有効なローカル資材を優先し、不足した資材だけを取得してコピーする。"""
        # 正常 component からのローカルコピーは cache 消失後も動作する。
        use = _AssetUse(self.cmoc_root, asset, destination)
        try:
            for source in local_sources:
                status = asset.check(source)
                use.event(local_path=str(source), local_status=status)
                if status == "valid":
                    shutil.copyfile(source, destination)
                    if asset.check(destination) != "valid":
                        raise ValueError(f"local asset changed: {asset.name}")
                    use.event(
                        status="completed",
                        source="local",
                        path=str(source),
                        cache_status="not_checked_local_available",
                    )
                    return "reused"
            return self._obtain_cached(asset, destination, use)
        except BaseException as exc:
            use.event(status="failed", failure=str(exc))
            raise

    def _obtain_cached(
        self, asset: DownloadAsset, destination: Path, use: _AssetUse
    ) -> str:
        # 一つの OS ユーザーだけが所有する root に固定し、版間の回収は行わない。
        root = asset_cache_directory()
        try:
            _safe_directory(root)
            if root.stat().st_uid != os.getuid():
                raise ValueError("asset cache belongs to another OS user")
        except (OSError, ValueError, SearchError):
            use.event(cache_status="write_failed")
            raise
        entry = root / asset.key
        waited = False

        def record_wait(seconds: float) -> None:
            nonlocal waited
            waited = True
            use.event(wait_seconds=seconds)

        use.event(cache_path=str(entry), cache_status="pending", status="waiting")
        with _file_lock(
            root / f"{asset.key}.lock", time.monotonic() + 7200, on_wait=record_wait
        ):
            # 公開切替前の異常終了で退避した既存資材を、先に戻して照合する。
            backup = root / f".previous-{asset.key}"
            if not entry.exists() and backup.exists():
                os.replace(backup, entry)
            status = _cache_status(entry, asset)
            use.event(cache_status=status)
            if status != "valid":
                self._publish(root, entry, asset, use)
                action = "downloaded"
            else:
                action = "reused"
            # cache の参照を component に残さず、削除・消失から独立させる。
            shutil.copyfile(entry / "content", destination)
            if asset.check(destination) != "valid":
                raise ValueError(f"cached asset changed: {asset.name}")
            use.event(
                status="completed",
                source="download" if action == "downloaded" else "cache",
                path=str(entry / "content"),
                waited=waited,
            )
            return action

    def _publish(
        self, root: Path, entry: Path, asset: DownloadAsset, use: _AssetUse
    ) -> None:
        # 同じ資材の lock 内で、前回の未公開 staging だけを回収する。
        prefix = f".incomplete-{asset.key}-"
        for abandoned in root.glob(f"{prefix}*"):
            if abandoned.is_dir() and not abandoned.is_symlink():
                shutil.rmtree(abandoned)
        staging = Path(tempfile.mkdtemp(prefix=prefix, dir=root))
        backup = root / f".previous-{asset.key}"
        published = False
        try:
            _download(asset, staging / "content", use)
            use.event(status="checking_integrity")
            if asset.check(staging / "content") != "valid":
                raise ValueError(f"asset integrity check failed: {asset.name}")
            receipt = {
                "asset": asdict(asset),
                "size_bytes": (staging / "content").stat().st_size,
            }
            with (staging / "receipt.json").open("w", encoding="utf-8") as output:
                json.dump(receipt, output, sort_keys=True)
                output.flush()
                os.fsync(output.fileno())
            use.event(status="publishing", publication="started")
            if entry.exists() or entry.is_symlink():
                _remove_entry(backup)
                os.replace(entry, backup)
            os.replace(staging, entry)
            published = True
            use.event(status="published", publication="succeeded")
        except BaseException as exc:
            if not published and backup.exists():
                os.replace(backup, entry)
            use.event(
                status="failed",
                publication="failed"
                if use.fields["publication"] == "started"
                else use.fields["publication"],
                failure=str(exc),
            )
            raise
        finally:
            if staging.exists():
                shutil.rmtree(staging)
            if published:
                _remove_entry(backup)
