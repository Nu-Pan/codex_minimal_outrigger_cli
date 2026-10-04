"""固定したモデルと npm 配布物を、検索用コンポーネントの構築へ渡す。"""

import base64
import json
import platform
import shutil
import subprocess
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import asdict
from pathlib import Path
from urllib.parse import quote

from .runtime_document_search_types import ModelArtifact
from .runtime_download_asset_cache import DownloadAsset, DownloadAssetCache


def prepare_model(
    root: Path, base: Path, staging: Path, artifact: ModelArtifact
) -> str:
    """既存モデル、共有キャッシュ、固定 revision の順に完全性を確認する。"""
    # 正本のモデル識別情報をそのまま取得・検証条件へ使う。
    asset = DownloadAsset(
        name=artifact.filename,
        url=f"https://huggingface.co/{artifact.repository}/resolve/{artifact.revision}/{quote(artifact.filename)}",
        integrity="sha256-"
        + base64.b64encode(bytes.fromhex(artifact.sha256)).decode("ascii"),
        size_bytes=artifact.size_bytes,
        identity=asdict(artifact),
    )
    return DownloadAssetCache(root).obtain(
        asset, staging / artifact.filename, local_sources=(base / artifact.filename,)
    )


def _allows(restriction: object, value: str) -> bool:
    # npm の os/cpu/libc で指定された許可と否定を同じ条件で判定する。
    values = [restriction] if isinstance(restriction, str) else restriction
    if values is None:
        return True
    if not isinstance(values, list) or not all(
        isinstance(item, str) for item in values
    ):
        raise ValueError("invalid npm platform restriction")
    return f"!{value}" not in values and (
        not any(not item.startswith("!") for item in values)
        or value in values
        or "any" in values
    )


def _npm_platform() -> dict[str, str]:
    # npm と同じ Node の process.platform/process.arch を参照する。
    result = subprocess.run(
        ["node", "-p", "JSON.stringify({os:process.platform,cpu:process.arch})"],
        check=True,
        capture_output=True,
        text=True,
        timeout=5,
    )
    values = json.loads(result.stdout)
    libc = platform.libc_ver()[0]
    return {
        "os": str(values["os"]),
        "cpu": str(values["cpu"]),
        "libc": "glibc" if libc == "glibc" else "musl",
    }


def _npm_local_source(cache: Path, integrity: str) -> Path:
    # cacache の content-v2 は SRI の digest を分割する。未知の形式は hit しない。
    # https://github.com/npm/cacache/blob/main/lib/content/path.js
    algorithm, encoded = integrity.split("-", 1)
    digest = base64.b64decode(encoded, validate=True).hex()
    return (
        cache
        / "_cacache/content-v2"
        / algorithm
        / digest[:2]
        / digest[2:4]
        / digest[4:]
    )


@contextmanager
def node_runtime_assets(root: Path, base: Path) -> Iterator[None]:
    """各依存物を検証してローカル tarball に固定し、npm の外部通信を不要にする。"""
    # 構築時だけ resolved をローカル資材へ置換し、配布元の lock は保持する。
    lock_path = base / "package-lock.json"
    original = lock_path.read_bytes()
    lock = json.loads(original)
    packages = lock["packages"]
    if lock.get("lockfileVersion") != 3 or not isinstance(packages, dict):
        raise ValueError("npm lock is incomplete")
    target = _npm_platform()
    asset_dir = base / ".assets"
    asset_dir.mkdir()
    cache = DownloadAssetCache(root)
    try:
        for name, package in packages.items():
            if not name or package.get("link") or package.get("inBundle"):
                continue
            if not all(
                _allows(package.get(field), value) for field, value in target.items()
            ):
                if not package.get("optional"):
                    raise ValueError(f"npm dependency is incompatible: {name}")
                continue
            if not all(
                isinstance(package.get(field), str) and package[field]
                for field in ("version", "resolved", "integrity")
            ):
                raise ValueError(f"npm dependency is not pinned: {name}")
            asset = DownloadAsset(
                name=name.split("node_modules/")[-1],
                url=package["resolved"],
                integrity=package["integrity"],
                identity={
                    "kind": "npm",
                    **{
                        field: package.get(field)
                        for field in (
                            "version",
                            "os",
                            "cpu",
                            "libc",
                            "dependencies",
                            "optionalDependencies",
                        )
                    },
                },
            )
            destination = asset_dir / f"{asset.key}.tgz"
            # キャッシュ導入前の配置内 npm cache も SRI で確認して再利用する。
            local = _npm_local_source(base.parent / "npm-cache", asset.integrity)
            cache.obtain(asset, destination, local_sources=(local,))
            package["resolved"] = destination.as_uri()
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        yield
    finally:
        lock_path.write_bytes(original)
        shutil.rmtree(asset_dir)
        shutil.rmtree(base / ".npm-cache", ignore_errors=True)
