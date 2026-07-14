import re
import shutil
import subprocess
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path

from acp.builder.tui.resolve_parameter import (
    TUI_FILE_ACCESS_MODES,
    build_tui_resolve_parameter_parameter,
)
from acp.builder.tui.launch_tui import build_tui_launch_tui_parameter
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import (
    CmocError,
    CodexExecResult,
    ensure_cmoc_ignored,
    load_config,
    logs_dir,
    repo_root,
    run_cli_subcommand,
    start_subcommand_step,
    run_codex_exec,
    run_codex_tui,
    timestamp,
    work_root,
)
from config.cmoc_config import CmocConfig
from commons.indexing import enable_indexing_preflight

# <work-root>/oracle/doc/app_spec/sub_command/tui.md
ORIGINAL_PROMPT_TEMPLATE = """<!--
AI Agent CLI/TUI に与えるプロンプトをここに書く。
フォーマットは Markdown で、見出し (`#`, `##`, `###`, ...) やコードブロック (```...```) などの使用は自由。

基本的な考え方は以下の通り

- 曖昧な指示は避ける
- 短く簡潔に保つ
- 必要以上の指示はしない

アンチパターンは以下の通り

- 手順の過剰固定
    - 解き方を細かく縛りすぎない。
    - 例：「必ず A→B→C の順で調査し、他の方法は使わない。」
- 曖昧な丸投げ
    - 品質基準なしに「いい感じ」を求めない。
    - 例：「このコードをいい感じに直して。」
- 不要な絶対ルール
    - 真の不変条件ではない `always` / `never` を増やさない。
    - 例：「常に全ファイルを読んでから回答する。」
- 設定値への品質丸投げ
    - 曖昧な指示を reasoning effort などの設定値で補おうとしない。
    - 例：「プロンプトは雑でよいので高 reasoning で正しくして。」
- 未理解の概念の採用
    - 意味が曖昧なキーワードを指示に入れない。
    - 例：「phase を良い感じに使って進めて。」
- 古い文脈への依存
    - 長くなったスレッドの空気で判断させない。
    - 例：「前の流れを踏まえて、いつもの感じで直して。」
-->

# 目的

<!--
- 何を作る／直す／判断するのかを成果ベースで書く。
- 例：「cmoc build の失敗原因を特定し、最小修正でビルドを通す。」
-->

TODO

# 作業対象

<!--
- 参照すべきファイル、ディレクトリ、ログ、仕様を明示する。
- 例：「`src/parser/`、`tests/parser/`、以下のエラーログを対象にする。」
-->

TODO

# 制約条件

<!--
    - 絶対にしてはいけないこと、絶対に起きてはいけないことを書く
    - 守るべき設計、規約、安全要件、互換性、禁止操作、…
    - 例：「公開 API のシグネチャは変更しない。」
    - 例：「マイグレーション、依存追加、秘密情報の出力は行わない。」
    - 例：「本番用の設定ファイルは書き換えてはいけない。」
-->

TODO

# 期待する成果物

<!--
- 最終的に何を返してほしいのかを明示する。
- 例：「修正概要、変更ファイル、実行した検証、残課題を返す。」
-->

TODO

# 出力形式

<!--
- 長さ、順序、必須フィールド、Markdown/JSON などを指定する。
- 例：「`原因 / 修正 / 検証 / 注意点` の4見出しで返す。」
-->

TODO

# 完了条件

<!--
- 作業を終えてよい観測可能な状態を指定する。
- 実行すべきテスト、リンター、型チェック、ビルドを具体的に指定したほうが良い
- 失敗が想定されるなら、最悪ケースの停止条件を書く
- 例：「対象テストが通り、元のバグが再現しなくなったら完了。」
- 例：「変更後に `cargo test parser` と `cargo clippy` を実行する。」
- 例：「同じ原因で2回失敗したら追加修正せず、ログと仮説を報告する。」
-->

TODO

# 成功基準

<!--
- 何が良くて、何が良くないのか？　良い解と見なす品質基準・観点を書く。
- 例：「差分が小さく、既存アーキテクチャに沿い、回帰リスクが低い。」
- 例：「差分を見直し、不要な変更、境界条件漏れ、危険な副作用がないか確認する。」
-->

TODO

# 裁量範囲

<!--
- 裁量範囲
    - モデルが自由に判断してよい部分と、根拠が必要な部分を分ける。
    - 例：「命名は既存規約に合わせて裁量でよいが、仕様変更は提案に留める。」
- 根拠の範囲
    - どの情報源を信頼し、どの主張に引用が必要かを指定する。
    - 例：「仕様に関する断定は `docs/spec.md` の該当箇所を引用する。」
-->

TODO

"""

CodexExec = Callable[..., CodexExecResult]
CodexTui = Callable[..., None]


def cmoc_tui_impl() -> None:
    """CLI runtime を通して tui を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_tui_from_current_context,
        pre_log_check=ensure_tui_cmoc_ignored,
        command_name="tui",
        command_argv=["cmoc", "tui"],
        total_steps=4,
    )


def _cmoc_tui_body(
    run_codex_exec: CodexExec,
    run_codex_tui: CodexTui,
    *,
    root: Path,
    work_root: Path,
    config: CmocConfig,
) -> None:
    """依頼文の編集、実行パラメータ解決、Codex TUI 起動を一連で行う。"""
    start_subcommand_step(2, "オリジナルプロンプトを入力", "edit original prompt")
    original_path = initialize_original_prompt(root)
    run_editor(original_path)
    original_prompt = read_original_prompt(original_path)
    start_subcommand_step(3, "実行パラメータを決定", "resolve parameters")
    resolved = run_codex_exec(
        replace(
            build_tui_resolve_parameter_parameter(original_prompt),
            cwd=work_root,
        ),
        root=root,
        cwd=work_root,
        config=config,
        purpose="tui resolve parameter",
    ).output_json
    launch_timestamp = original_path.name.removesuffix("_orig.md")
    parameter = build_tui_codex_parameter(
        original_prompt,
        resolved or {},
        launch_timestamp=launch_timestamp,
    )
    parameter = replace(parameter, cwd=work_root)
    complete_prompt_path = logs_dir(root).parent / "tui" / f"{launch_timestamp}_cmpl.md"
    start_subcommand_step(4, "AI Agent TUI を起動", "launch agent TUI")
    run_codex_tui(
        parameter,
        root=root,
        cwd=work_root,
        config=config,
        purpose="tui codex",
        extra_read_paths=[complete_prompt_path],
    )


def ensure_tui_cmoc_ignored(root: Path) -> None:
    """TUI がログを書く root の `.cmoc` ignore をログ作成前に保証する。"""
    # <work-root>/oracle/doc/app_spec/sub_command/tui.md
    # <work-root>/oracle/doc/app_spec/misc_spec.md
    current_root = work_root()
    ensure_cmoc_ignored(current_root)
    if current_root.resolve() != root.resolve():
        ensure_cmoc_ignored(root)


def _cmoc_tui_from_current_context() -> None:
    """現在の repository 状態から `cmoc tui` の本体処理を起動する。"""
    root = repo_root()
    current_root = work_root()
    _cmoc_tui_body(
        run_codex_exec,
        run_codex_tui,
        root=root,
        work_root=current_root,
        config=load_config(root),
    )


def initialize_original_prompt(root: Path) -> Path:
    """利用者が編集する元 prompt ファイルを TUI log 領域へ作成する。"""
    path = logs_dir(root).parent / "tui" / f"{timestamp()}_orig.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ORIGINAL_PROMPT_TEMPLATE)
    return path


def select_editor() -> list[str]:
    """cmoc tui で利用できる editor command を PATH から選ぶ。"""
    for command in ["code", "nano", "vim", "vi"]:
        executable = shutil.which(command)
        if executable is None:
            continue
        if command == "code":
            return [executable, "--wait"]
        return [executable]
    raise CmocError(
        "利用可能なエディタが見つかりません。",
        ["code, nano, vim, vi のいずれかを PATH から起動できるようにしてください。"],
        "searched: code, nano, vim, vi",
    )


def run_editor(path: Path) -> None:
    """利用者の prompt 編集が正常終了したことを確認する。"""
    argv = [*select_editor(), str(path)]
    result = subprocess.run(argv)
    if result.returncode != 0:
        raise CmocError(
            "エディタが正常終了しませんでした。",
            ["エディタの状態を確認してから `cmoc tui` を再実行してください。"],
            f"command: {' '.join(argv)}\nreturncode: {result.returncode}",
        )


def read_original_prompt(path: Path) -> str:
    """テンプレート用 HTML comment を除去した利用者 prompt を読む。"""
    return re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.DOTALL).strip()


def build_tui_codex_parameter(
    original_prompt: str,
    resolved_parameter: dict,
    *,
    launch_timestamp: str | None = None,
) -> AgentCallParameter:
    """解決済み JSON から TUI 起動用 AgentCallParameter を構築する。"""
    file_access_mode = FileAccessMode(
        nested_value(resolved_parameter, "file_access_mode", FileAccessMode.READONLY.value)
    )
    if file_access_mode not in TUI_FILE_ACCESS_MODES:
        raise CmocError(
            "TUI では使用できないファイルアクセスモードです。",
            ["プロンプトを保存して `cmoc tui` を再実行してください。"],
            f"file_access_mode: {file_access_mode.value}",
        )
    # <work-root>/oracle/doc/app_spec/prompt_standard.md
    # <work-root>/oracle/doc/app_spec/sub_command/tui.md
    return build_tui_launch_tui_parameter(
        launch_timestamp or timestamp(),
        role=nested_value(
            resolved_parameter,
            "role",
            "- あなたは AI Agent CLI/TUI として、ユーザーから与えられた依頼を実行します",
        ),
        summary=nested_value(
            resolved_parameter,
            "summary",
            "- 後述する詳細指示に従って作業してください",
        ),
        goal=nested_value(
            resolved_parameter,
            "goal",
            "- 詳細指示の要求を満たしていること",
        ),
        file_access_mode=file_access_mode,
        original_prompt=original_prompt,
        oracle_and_realization_basic=nested_bool(
            resolved_parameter, "oracle_and_realization_basic"
        ),
        oracle_standard=nested_bool(resolved_parameter, "oracle_standard"),
        realization_standard=nested_bool(resolved_parameter, "realization_standard"),
        review_oracle_standard=nested_bool(
            resolved_parameter, "review_oracle_standard"
        ),
        apply_review_standard=nested_bool(resolved_parameter, "apply_review_standard"),
        index_entry_standard=nested_bool(resolved_parameter, "index_entry_standard"),
    )


def nested_value(data: dict, name: str, default: str) -> str:
    """TUI parameter JSON で `{value: ...}` 形式の項目から文字列値を取り出す。"""
    value = data.get(name)
    if (
        isinstance(value, dict)
        and isinstance(value.get("value"), str)
        and value["value"]
    ):
        return value["value"]
    return default


def nested_bool(data: dict, name: str) -> bool:
    """TUI parameter JSON で `{value: ...}` 形式の項目を真偽値として読む。"""
    value = data.get(name)
    return bool(value.get("value")) if isinstance(value, dict) else False
