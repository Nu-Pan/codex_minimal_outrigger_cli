"""
# path model

対応 oracle file: `<work-root>/oracle/src/basic/path_model.py`。

## パス表記の基本ルール

- cmoc 上では、ファイル・ディレクトリパスを絶対パス・相対パスどちらで書いても良い
- 相対パスを書く時は、そのルートディレクトリパスを `<root-token>/relative/path/to/file` のように、ルートトークン＋相対パスの形式で表記する
- `src/foo.py` のようなルートトークンを持たない相対パスでの表記は禁止

## ルートトークン一覧

- クラス `RootToken` で定義

## パスの表記例

- ユーザーは `<repo-root>` をカレントとして `<cmoc-root>/bin/cmoc` を呼び出す
- `cmoc apply fork` は `<repo-root>` を pwd として呼び出されて、 run の作業隔離のために `<run-root>` を git linked worktree として作成する
- run の作業隔離のための linked worktree は `<repo-root>` 内に作成されるから、「`<repo-root>` のフルパス」は「`<run-root>` のフルパス」の部分文字列となる
- `<run-root>` 内で cmoc を起動した場合 `<run-root>` と同値
"""

from pathlib import Path
from enum import StrEnum
from typing import Generator
import subprocess


class RootToken(StrEnum):
    """
    root token 一覧
    """

    # cmoc 自体のリポジトリのルートディレクトリ
    # cmoc 自体のソースコード・ドキュメントを指す時に使う
    CMOC = "<cmoc-root>"

    # cmoc を用いた開発を行う対象となる git リポジトリの main worktree のルートディレクトリ
    # より平易に git リポジトリ本体のルートディレクトリとも言える
    # 直下に `.git` ディレクトリを持つ
    REPO = "<repo-root>"

    # cmoc が run の隔離作業用に作る linked worktree のルートを指す
    # 直下に `.git` ファイルを持つ
    RUN = "<run-root>"

    # ユーザーが cmoc を呼び出した cwd から最近傍の `.git` ディレクトリ・ファイルで解決される worktree root
    # 直下に `.git` ディレクトリ・ファイルを持つ
    WORK = "<work-root>"


def resolve_real_path(source: RootToken | str | Path) -> Path:
    """
    root token そのもの、あるいは root token を含むパスを、現実の絶対パスに解決する。
    """
    if isinstance(source, RootToken):
        # 引数が RootToken の場合は素直に解決して返す
        match source:
            case RootToken.CMOC:
                return resolve_cmoc_root()
            case RootToken.REPO:
                return resolve_repo_root()
            case RootToken.RUN:
                return resolve_run_root()
            case RootToken.WORK:
                return resolve_work_root()
            case _:
                raise ValueError(f"{source} is invalid RootToken.")
    elif isinstance(source, str):
        # 引数が str の場合は Path に処理を回す
        return resolve_real_path(Path(source))
    elif isinstance(source, Path):
        # Path の場合は先頭のトークンを置換
        # 絶対パスならそのまま返す（symlink とかの可能性があるので resolve はする）
        if source.is_absolute():
            return source.resolve()
        # 空パスは禁止
        if not source.parts:
            raise ValueError(f"source is empty like path (source={source})")
        # パス先頭パーツのみ置換
        head_part = source.parts[0]
        for root_token in RootToken:
            if head_part == root_token.value:
                result = resolve_real_path(root_token) / Path(*source.parts[1:])
                return result.resolve()
        else:
            raise ValueError(
                f"source is relative path without root token (source={source})"
            )
    else:
        raise TypeError(f"{source} is unexpected type")


def resolve_cmoc_root(
    start_path: Path | None = None,
) -> Path:
    """
    `<cmoc-root>` を返す。
    これは内部実装であり、`resolve_real_path` からのみ呼び出される想定。
    自身の絶対パスを起点として

    - `.git` ディレクトリを直下に持つディレクトリ
    - `bin/cmoc` ファイルを直下に持つディレクトリ

    を探索する。
    """
    # 直下に `.git` ディレクトリを持つディレクトリを探す
    for candidate in _enumerate_candidates(start_path, Path(__file__)):
        if (candidate / ".git").is_dir():
            return candidate
        elif (candidate / "bin" / "cmoc").is_file():
            return candidate
    else:
        raise ValueError("`<cmoc-root>` was not found")


def resolve_repo_root(
    start_path: Path | None = None,
) -> Path:
    """
    `<repo-root>` を返す。
    これは内部実装であり、`resolve_real_path` からのみ呼び出される想定。
    cwd を起点として「`.git` ディレクトリを直下に持つディレクトリ」を探索する。
    """
    # カレントからの .git ディレクトリ探索を試みる
    for candidate in _enumerate_candidates(start_path, Path.cwd()):
        if (candidate / ".git").is_dir():
            return candidate
    # カレントディレクトリを解決
    if start_path is None:
        start_dir = Path.cwd()
    elif start_path.is_dir():
        start_dir = start_path.resolve()
    else:
        start_dir = start_path.resolve().parent
    # git コマンドからの特定を試みる
    # NOTE
    #   `<run-root>` が `<repo-root>` の外にある場合向けの処理
    git_result = subprocess.run(
        ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
        cwd=start_dir,
        text=True,
        capture_output=True,
    )
    if git_result.returncode == 0:
        common_dir = git_result.stdout.strip()
        if common_dir:
            return Path(common_dir).parent
    # 全部ダメだったら例外
    raise ValueError("`<repo-root>` was not found")


def resolve_run_root(
    start_path: Path | None = None,
) -> Path:
    """
    `<run-root>` を返す。
    これは内部実装であり、`resolve_real_path` からのみ呼び出される想定。
    cwd を起点として「`.git` ファイルを直下に持つディレクトリ」を探索する。
    """
    # .git ファイルを探索
    for candidate in _enumerate_candidates(start_path, Path.cwd()):
        if (candidate / ".git").is_file():
            return candidate
    else:
        raise ValueError("`<run-root>` was not found")


def resolve_work_root(
    start_path: Path | None = None,
) -> Path:
    """
    `<work-root>` を返す。
    これは内部実装であり、`resolve_real_path` からのみ呼び出される想定。
    cwd を起点として「`.git` ファイル・ディレクトリを直下に持つディレクトリ」を探索する。
    """
    # .git ファイル・ディレクトリを探索
    for candidate in _enumerate_candidates(start_path, Path.cwd()):
        dot_git_path = candidate / ".git"
        if dot_git_path.is_dir() or dot_git_path.is_file():
            return candidate
    else:
        raise ValueError("`<work-root>` was not found")


def resolve_token_path(real_path: Path, root_token: RootToken) -> Path:
    """
    実パス (`real_path`) を root token 表記に変換する。
    変換先は `root_token` で指定し、マッチしなかった場合は例外を投げる。
    """
    real_path = real_path.resolve()
    root_real_path = resolve_real_path(root_token)
    try:
        relative_path = real_path.relative_to(root_real_path)
    except ValueError:
        raise ValueError(
            f"real_path is not matched with root_token (real_path={real_path}, root_token={root_token})"
        )
    return Path(root_token.value) / relative_path


def _enumerate_candidates(
    start_path: Path | None,
    default_path: Path,
) -> Generator[Path, None, None]:
    """
    `resolve_***_root` 系関数向けに root token と対応する実パスの候補を列挙する。
    """
    # 始点パスを正規化
    if start_path is None:
        start_path = default_path.resolve()
    else:
        start_path = start_path.resolve()
    # start_path 自体がディレクトリなら、まずはそれを返す
    if start_path.is_dir():
        yield start_path
    # 親ディレクトリを子側から順番に返す
    for p in start_path.parents:
        yield p
