"""
# path model

## パス表記の基本ルール

- cmoc 上では、ファイル・ディレクトリパスを絶対パス・相対パスどちらで書いても良い
- 相対パスを書く時は、そのルートディレクトリパスを `{{place-holder}}/relative/path/to/file` のように、プレースホルダ＋相対パスの形式で表記する
- `src/foo.py` のようなプレースホルダを持たない相対パスでの表記は禁止

## ルートパスプレースホルダ一覧

- クラス `RootPathPlaceHolder` で定義

## パスの表記例

- ユーザーは `{{repo-root}}` をカレントとして `{{cmoc-root}}/bin/cmoc` を呼び出す
- `cmoc oracle edit` は main worktree から呼び出され、`{{repo-root}}` を agent call の cwd とする 2 回の `codex exec` を直列に起動する
- `cmoc realization apply fork`, `cmoc realization refactor fork` は `{{repo-root}}` を cmoc process の cwd として呼び出され、run の作業隔離のために `{{run-root}}` を git linked worktree として作成する
- realization の各 fork が起動する編集用 `codex exec` は `{{run-root}}` を agent call の cwd とする
- agent call の call-scoped path context は `AgentCallPathContext` を正本とする

NOTE
    root placeholder の名前と解決はこの module が所有し、prompt builder はこの model を使う。
"""

# std
import os
import subprocess
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Generator


class RootPathPlaceHolder(StrEnum):
    """
    ルートパスプレースホルダ一覧
    """

    # cmoc 自体のリポジトリのルートディレクトリ
    # cmoc 自体のソースコード・ドキュメントを指す時に使う
    CMOC = "{{cmoc-root}}"

    # AgentCallPathContext.repo_root に対応する placeholder
    REPO = "{{repo-root}}"

    # cmoc が run の隔離作業用に作る linked worktree のルートを指す
    # 直下に `.git` ファイルを持つ
    RUN = "{{run-root}}"

    # AgentCallPathContext.work_root に対応する placeholder
    WORK = "{{work-root}}"


@dataclass(frozen=True)
class AgentCallPathContext:
    """1 回の agent call で共有する root path の正本モデル。

    constructor は決定済みの AgentCallParameter.agent_call_cwd だけを受け取る。
    work_root と repo_root は agent_call_cwd と Git repository metadata から導出し、
    呼び出し側から指定させない。
    構築後の値は変更できず、同じ agent call の prompt 全体で共有する。

    NOTE
        builder は cwd の確定後に context を構築し、並列 call 間では共有しない。
    """

    # prompt 構築前に builder が決定する agent call の cwd
    # cmoc process の cwd から暗黙に補完してはならない
    agent_call_cwd: Path

    # `{{work-root}}` として使う、agent_call_cwd を含む最寄りの Git worktree root
    # agent_call_cwd が main worktree 上なら repo_root と同値になる
    # agent_call_cwd が `{{cmoc-run-worktree}}` 上なら `{{run-root}}` と同値になり、repo_root とは異なる
    work_root: Path = field(init=False)

    # `{{repo-root}}` として使う、work_root が属する Git repository の main worktree root
    repo_root: Path = field(init=False)

    def __post_init__(self) -> None:
        """agent_call_cwd を正規化し、同じ起点から派生 root を初期化する。"""
        # agent call で実際に使用できる絶対ディレクトリへ正規化する
        resolved_agent_call_cwd = self.agent_call_cwd.resolve()
        if not resolved_agent_call_cwd.is_dir():
            raise ValueError(
                "AgentCallParameter.agent_call_cwd is not directory "
                f"(agent_call_cwd={resolved_agent_call_cwd})"
            )

        # 同じ Git metadata 応答から worktree root と main worktree root を決める
        work_root, repo_root = _resolve_git_worktree_roots(resolved_agent_call_cwd)
        object.__setattr__(self, "agent_call_cwd", resolved_agent_call_cwd)
        object.__setattr__(self, "work_root", work_root)
        object.__setattr__(self, "repo_root", repo_root)

    def root_placeholder_definitions(self) -> dict[str, str | Path]:
        """call-scoped root placeholder の全定義を返す。

        NOTE
            call-scoped root の名前と値は、この関数を唯一の取得元とする。
        """
        return {
            "repo-root": self.repo_root,
            "work-root": self.work_root,
        }


def resolve_real_path(
    source: RootPathPlaceHolder | str | Path,
    path_context: AgentCallPathContext | None = None,
) -> Path:
    """
    ルートパスプレースホルダそのもの、あるいはルートパスプレースホルダを含むパスを、実際の絶対パスに解決する。

    path_context が指定された場合、agent call に依存する root は同じ context から解決する。
    """
    if isinstance(source, RootPathPlaceHolder):
        # agent call に依存する root は、指定済み context を process cwd より優先する。
        match source:
            case RootPathPlaceHolder.CMOC:
                return resolve_cmoc_root()
            case RootPathPlaceHolder.REPO:
                if path_context is not None:
                    return path_context.repo_root
                return resolve_repo_root()
            case RootPathPlaceHolder.RUN:
                if path_context is not None:
                    return resolve_run_root(path_context.agent_call_cwd)
                return resolve_run_root()
            case RootPathPlaceHolder.WORK:
                if path_context is not None:
                    return path_context.work_root
                return resolve_work_root()
            case _:
                raise ValueError(f"{source} is invalid RootPathPlaceHolder.")
    elif isinstance(source, str):
        return resolve_real_path(Path(source), path_context)
    elif isinstance(source, Path):
        # 絶対 path は placeholder 解決の対象外だが、symlink を含むため正規化する。
        if source.is_absolute():
            return source.resolve()
        if not source.parts:
            raise ValueError(f"source is empty like path (source={source})")
        # root placeholder は相対 path の先頭 token にだけ許可する。
        head_part = source.parts[0]
        for root_path_ph in RootPathPlaceHolder:
            if head_part == root_path_ph.value:
                result = resolve_real_path(root_path_ph, path_context) / Path(
                    *source.parts[1:]
                )
                return result.resolve()
        else:
            raise ValueError(
                f"source is relative path without root path place holder (source={source})"
            )
    else:
        raise TypeError(f"{source} is unexpected type")


def resolve_cmoc_root(
    start_path: Path | None = None,
) -> Path:
    """
    `{{cmoc-root}}` を返す。
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
        raise ValueError("`{{cmoc-root}}` was not found")


def _resolve_git_worktree_roots(
    start_path: Path | None = None,
) -> tuple[Path, Path]:
    """Git repository metadata から worktree root と main worktree root を返す。

    最寄りの worktree を Git discovery で特定する。linked worktree の場合は、
    `git worktree list --porcelain -z` の先頭 record を main worktree とする。
    """
    resolved_start_path = (Path.cwd() if start_path is None else start_path).resolve()
    # repository 選択用の環境変数で cwd 起点の探索を上書きさせない
    git_environment = os.environ.copy()
    for variable_name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR"):
        git_environment.pop(variable_name, None)

    for candidate in _enumerate_candidates(start_path, Path.cwd()):
        git_result = subprocess.run(
            [
                "git",
                "rev-parse",
                "--show-toplevel",
                "--absolute-git-dir",
                "--path-format=absolute",
                "--git-common-dir",
            ],
            cwd=candidate,
            text=True,
            capture_output=True,
            env=git_environment,
        )
        if git_result.returncode != 0:
            continue

        path_lines = git_result.stdout.splitlines()
        if len(path_lines) != 3:
            continue
        worktree_root, git_dir, common_dir = (
            Path(path_line).resolve() for path_line in path_lines
        )
        if not worktree_root.is_dir() or not resolved_start_path.is_relative_to(
            worktree_root
        ):
            continue
        if git_dir == common_dir:
            return worktree_root, worktree_root

        worktree_list_result = subprocess.run(
            [
                "git",
                f"--git-dir={common_dir}",
                "worktree",
                "list",
                "--porcelain",
                "-z",
            ],
            text=True,
            capture_output=True,
            env=git_environment,
        )
        main_record = worktree_list_result.stdout.split("\0", maxsplit=1)[0]
        if worktree_list_result.returncode != 0 or not main_record.startswith(
            "worktree "
        ):
            continue
        main_worktree_root = Path(main_record.removeprefix("worktree ")).resolve()
        return worktree_root, main_worktree_root

    raise ValueError("`{{work-root}}` was not found")


def resolve_repo_root(
    start_path: Path | None = None,
) -> Path:
    """
    `{{repo-root}}` を返す。
    agent call path context の構築と root placeholder の解決に使用する。
    start_path が指定されていれば、その探索開始 path を起点とする。
    start_path が省略されていれば、cmoc process の cwd を探索開始 path とする。
    Git repository metadata から、所属 repository の main worktree を特定する。
    """
    try:
        _, repo_root = _resolve_git_worktree_roots(start_path)
    except ValueError:
        raise ValueError("`{{repo-root}}` was not found") from None
    return repo_root


def resolve_run_root(
    start_path: Path | None = None,
) -> Path:
    """
    `{{run-root}}` を返す。
    これは内部実装であり、`resolve_real_path` からのみ呼び出される想定。
    start_path が指定されていれば、その探索開始 path を起点とする。
    start_path が省略されていれば、cmoc process の cwd を探索開始 path とする。
    「`.git` ファイルを直下に持つディレクトリ」を探索する。
    """
    # 指定された探索開始 path または cmoc process の cwd から探索する
    for candidate in _enumerate_candidates(start_path, Path.cwd()):
        if (candidate / ".git").is_file():
            return candidate
    else:
        raise ValueError("`{{run-root}}` was not found")


def resolve_work_root(
    start_path: Path | None = None,
) -> Path:
    """
    `{{work-root}}` を返す。
    agent call path context の構築と root placeholder の解決に使用する。
    start_path が指定されていれば、その探索開始 path を起点とする。
    start_path が省略されていれば、cmoc process の cwd を探索開始 path とする。
    Git repository metadata から、探索開始 path を含む最寄りの worktree を特定する。
    """
    return _resolve_git_worktree_roots(start_path)[0]


def resolve_ph_path(
    real_path: Path,
    rpph: RootPathPlaceHolder,
    path_context: AgentCallPathContext | None = None,
) -> Path:
    """
    実パス (`real_path`) を root path place holder 表記に変換する。
    変換先は `rpph` で指定し、マッチしなかった場合は例外を投げる。
    """
    real_path = real_path.resolve()
    root_real_path = resolve_real_path(rpph, path_context)
    try:
        relative_path = real_path.relative_to(root_real_path)
    except ValueError:
        raise ValueError(
            f"real_path is not matched with rpph (real_path={real_path}, rpph={rpph})"
        )
    return Path(rpph.value) / relative_path


def _enumerate_candidates(
    start_path: Path | None,
    default_path: Path,
) -> Generator[Path, None, None]:
    """
    `resolve_***_root` 系関数向けにルートパスプレースホルダと対応する実パスの候補を列挙する。
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
