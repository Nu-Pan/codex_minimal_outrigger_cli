
# `cmoc tui` サブコマンド

## 概要

- ユーザーから与えられたプロンプトと cmoc の自動生成プロンプトを注入した状態で AI Agent CLI/TUI を起動する
- cmoc に実装されている規則・規範の上で任意のプロンプトを実行するための仕組み

## 引数

- なし

## 事前条件

- なし

## 実行手順

1. doctor preprocess を呼び出す
2. オリジナルプロンプトをユーザーからエディタ入力
3. 必要なパラメータを agent call で決定
4. AI Agent CLI/TUI を起動

## 「オリジナルプロンプトをユーザーからエディタ入力」の詳細

- cmoc がエディタを起動して、そこにユーザーがオリジナルプロンプトを入力する
- 起動するエディタは (高優先度) `code` --> `nano` --> `vim` --> `vi` (低優先度) の順でフォールバックする
- `code` で起動する場合は必ず `--wait` を付けること
- エディタの編集対象は `<repo-root>/.cmoc/local/log/tui/<time-stamp>_orig.md` とする
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

## 「AI Agent CLI/TUI を起動」の詳細

### 全バックエンド共通

- TUI 起動パラメータは `build_tui_launch_tui_parameter` を正本とする

### Codex CLI の場合

- 起動コマンドは `codex` とする (`codex exec` ではない)
- `<cmoc-root>/oracle/doc/app_spec/codex_exec_rule.md` から、以下の要素を持ち込む
    - 環境変数 `$CODEX_HOME`
    - preflight validation
    - codex profile
