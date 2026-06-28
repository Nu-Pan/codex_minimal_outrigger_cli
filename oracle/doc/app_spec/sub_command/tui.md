
# `cmoc tui` サブコマンド

## 概要

- ユーザーから与えられたプロンプトと cmoc の自動生成プロンプトを注入した状態で AI Agent CLI/TUI を起動する
- cmoc に実装されている規則・規範の上で任意のプロンプトを実行するための仕組み

## 引数

- なし

## 事前条件

- なし

## 実行手順

1. `<work-root>/.cmoc` が git の追跡対象外であることを保証する
2. オリジナルプロンプトをユーザーからエディタ入力
3. 必要なパラメータを agent call で決定
4. プロンプト全文を agent call で決定
5. AI Agent CLI/TUI を起動

## 「オリジナルプロンプトをユーザーからエディタ入力」の詳細

- cmoc がエディタを起動して、そこにユーザーがオリジナルプロンプトを入力する
- 起動するエディタは (高優先度) `code` --> `nano` --> `vim` --> `vi` (低優先度) の順でフォールバックする
- `code` で起動する場合は必ず `--wait` を付けること
- エディタの編集対象は `<repo-root>/.cmoc/log/tui/<time-stamp>_orig.md` とする
- `<time-stamp>_orig.md` は初期値として以下の文面を持つこととする
    ```markdown
    <!--
        AI Agent CLI/TUI に与えるプロンプトを書いて下さい。
        フォーマットは Markdown です。
        見出し (`#`, `##`, `###`, ...) やコードブロック (```...```) などの使用は自由です。
    -->

    TODO ここから書き始める
    ```
- エディタから cmoc に処理が戻ってきたらユーザー入力完了とみなす
- `<time-stamp>_orig.md` からのオリジナルプロンプト読み出しは以下の挙動とする
    - コメント `<!-- ... -->` は削除
    - 前後の空白文字は除去 (`strip`)

## 「必要なパラメータを agent call で決定」の詳細

- `cmoc tui` で必要になるパラメータの大半は agent call で決定する
- agent call の詳細仕様は `build_tui_resolve_parameter_parameter` を正本とする
- 以下のパラメータは agent call に委ねず固定とする
    - `ModelClass.MAINSTREAM`
    - `ReasoningEffort.MEDIUM`

## 「プロンプト全文を agent call で決定」の詳細

- AI Agent CLI/TUI に渡すプロンプト全文は `build_complete_prompt` で生成する
- オリジナルプロンプトは `aux_prompt` に注入する
    - オリジナルプロンプト (`str`) を Markdown としてパースし、見出しが存在する場合は `list[StructDoc]` に、見出しが存在しない場合は `str` に変換する
    - `aux_prompt=StructDoc("詳細指示", <変換後のオリジナルプロンプト>)` とする

## 「AI Agent CLI/TUI を起動」の詳細

### Codex CLI の場合

- ここまでの処理で選択したパラメータを使用して Codex CLI を起動する
- 起動コマンドは `codex` とする (`codex exec` ではない)
- `<cmoc-root>/oracle/doc/app_spec/codex_exec_rule.md` から、以下の要素を持ち込む
    - 環境変数 `$CODEX_HOME`
    - preflight validation
    - codex profile
    - ファイルアクセス制限
    - Model, Reasoning Effort
- プロンプトの渡し方
    - 完全なプロンプトを `<work-root>/.cmoc/log/tui/<time-stamp>_cmpl.md` に保存する
    - `codex` 引数経由で以下の初期プロンプトを与える
        ```text
        `<work-root>/.cmoc/log/tui/<time-stamp>_cmpl.md` の指示に従って下さい。
        ```
    - 実際に `codex` に渡す文字列では `<work-root>`, `<time-stamp>` を実際の値で置き換えること
    