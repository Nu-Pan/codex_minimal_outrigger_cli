# `launch_tui.py`

## Summary
- `cmoc oracle investigation` 用に、ユーザーの調査指示を埋め込んだ完全 prompt と Codex CLI TUI 起動パラメータを構築する関数。
- oracle 限定の読み取り専用アクセス、固定モデル・推論設定、リポジトリルートの作業ディレクトリ、indexing preflight の実行を含む起動条件を確認する入口。

## Read this when
- oracle investigation の TUI 起動条件を変更・確認するとき。
- oracle file 調査用 prompt の分類、routing、アクセスモード、ユーザー指示の埋め込み方を確認するとき。
- 調査用起動で使用するモデル、推論 effort、作業ディレクトリ、indexing preflight の設定を確認するとき。

## Do not read this when
- 共通の完全 prompt 構築規則を確認したいときは `build_complete_prompt` の定義を直接読む。
- 起動パラメータの型や列挙値の意味を確認したいときは `oracle.acp_builder.basic` の定義を直接読む。
- パスコンテキストの解決規則を確認したいときは `oracle.other.path_model` の定義を直接読む。

## hash
- d595e83e4bc8d56918cc6d66536a39dea8d5da44e38904dde36eef48e8310ea0
