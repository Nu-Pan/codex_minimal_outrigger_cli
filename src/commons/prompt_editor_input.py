"""AI Agent 用 prompt をエディタから受け取る共通境界。"""

import re
import shutil
import subprocess
from pathlib import Path

from commons.runtime_errors import CmocError
from commons.runtime_git import ensure_cmoc_ignored
from commons.runtime_paths import editor_input_dir, timestamp, work_root

# {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
PROMPT_EDITOR_INPUT_TEMPLATE = """<!--
AI Agent CLI/TUI に与えるプロンプトをここに書く。
フォーマットは Markdown で、見出し (`#`, `##`, `###`, ...) やコードブロック (```...```) などの使用は自由。

基本的な考え方は以下の通り

- 短く、簡潔で、明瞭な指示を書く
    - 「良い」とは一体何か？　具体的な品質基準にブレークダウンする
    - reasoning effort などの設定値を上げれば人間の真意を汲み取ってもらえるなどというナイーブな考えを持ってはいけない
    - AI Agent が知りえない概念・言葉を使う時は必ず説明・定義を入れる
- 作業手順は可能な限りモデルに任せる
    - 解き方の指示は最小限度に留める
    - 「必ず〇〇する」「絶対〇〇しない」は本当に必要なものだけにする
- 古い文脈への依存
    - 過去の会話を参照させたい場合、可能なら ID を書く
    - 思い出せない場合は、機械検索可能なキーワードを含めてあげる
- 以上の基本的な考え方は、実害があった場合は破って良い
    - agent が実際にハマった場合、リトライ時にはそれが再現しないようにプロンプトで誘導する（禁止指示を書く）
-->

# ゴール

<!--
- 何を作る／直す／判断するのかを成果ベースで書く。
- 例：「cmoc build の失敗原因を特定し、最小修正でビルドを通す。」

- 最終的に何を返してほしいのかを明示する。
- 例：「修正概要、変更ファイル、実行した検証、残課題を返す。」

- 長さ、順序、必須フィールド、Markdown/JSON などを指定する。
- 例：「`原因 / 修正 / 検証 / 注意点` の4見出しで返す。」

- 何が良くて、何が良くないのか？　良い解と見なす品質基準・観点を書く。
- 例：「差分が小さく、既存アーキテクチャに沿い、回帰リスクが低い。」
- 例：「差分を見直し、不要な変更、境界条件漏れ、危険な副作用がないか確認する。」

- 作業を終えてよい観測可能な状態を指定する。
- 実行すべきテスト、リンター、型チェック、ビルドを具体的に指定したほうが良い
- 例：「対象テストが通り、元のバグが再現しなくなったら完了。」
- 例：「変更後に `cargo test parser` と `cargo clippy` を実行する。」

- 失敗が想定されるなら、最悪ケースの停止条件を書く
- 例：「同じ原因で2回失敗したら追加修正せず、ログと仮説を報告する。」
-->

TODO

# 制約境界

<!--
- 参照すべきファイル、ディレクトリ、ログ、仕様を明示する。
- 例：「`src/parser/`、`tests/parser/`、以下のエラーログを対象にする。」

- 絶対にしてはいけないこと、絶対に起きてはいけないことを書く
- 守るべき設計、規約、安全要件、互換性、禁止操作、…
- 例：「公開 API のシグネチャは変更しない。」
- 例：「マイグレーション、依存追加、秘密情報の出力は行わない。」
- 例：「本番用の設定ファイルは書き換えてはいけない。」

- モデルが自由に判断してよい部分と、そうではない部分の境界を述べる
- 例：「命名は既存規約に合わせて裁量でよいが、仕様変更は提案に留める。」

- どの情報源を信頼し、どの主張に引用が必要かを指定する。
- 例：「仕様に関する断定は `docs/spec.md` の該当箇所を引用する。」
-->

TODO
"""


def collect_prompt_editor_input(
    root: Path,
    additional_template: str = "",
) -> tuple[Path, str]:
    """初期 prompt を保存・編集し、コメント除去済み入力と path を返す。"""
    # 同じ timestamp を完全 prompt のファイル名にも引き継げるよう path を返す。
    path = editor_input_dir(root) / f"{timestamp()}_orig.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    parts = [
        part.strip()
        for part in (additional_template, PROMPT_EDITOR_INPUT_TEMPLATE)
        if part.strip()
    ]
    path.write_text("\n\n".join(parts) + "\n", encoding="utf-8")

    # エディタが戻った時点を入力完了とし、終了失敗は利用者向けエラーにする。
    argv = [*_select_editor(), str(path)]
    result = subprocess.run(argv)
    if result.returncode != 0:
        raise CmocError(
            "エディタが正常終了しませんでした。",
            ["エディタの状態を確認してから cmoc コマンドを再実行してください。"],
            f"command: {' '.join(argv)}\nreturncode: {result.returncode}",
        )
    return path, _read_prompt_editor_input(path)


def ensure_prompt_editor_roots_ignored(root: Path) -> None:
    """editor/TUI が使う repository と現在 worktree の `.cmoc` ignore を保証する。"""
    current_root = work_root()
    ensure_cmoc_ignored(current_root)
    if current_root.resolve() != root.resolve():
        ensure_cmoc_ignored(root)


def _select_editor() -> list[str]:
    """仕様の優先順で PATH 上の editor command を選ぶ。"""
    for command in ("code", "nano", "vim", "vi"):
        executable = shutil.which(command)
        if executable is None:
            continue
        return [executable, "--wait"] if command == "code" else [executable]
    raise CmocError(
        "利用可能なエディタが見つかりません。",
        ["code, nano, vim, vi のいずれかを PATH から起動できるようにしてください。"],
        "searched: code, nano, vim, vi",
    )


def _read_prompt_editor_input(path: Path) -> str:
    """HTML comment と前後の空白を除去して利用者入力を読む。"""
    return re.sub(
        r"<!--.*?-->",
        "",
        path.read_text(encoding="utf-8"),
        flags=re.DOTALL,
    ).strip()
