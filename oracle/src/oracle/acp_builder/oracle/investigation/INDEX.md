# `launch_tui.py`

## Summary
- `cmoc oracle investigation` のユーザー指示と呼び出し側が確定した閲覧範囲から、完全 prompt と TUI 起動パラメータを構築する。
- 調査タスクの文面、oracle file を根拠とする範囲、アクセス方針、エディタ入力の受け渡しを、この呼び出し固有の設定としてまとめる。

## Read this when
- oracle investigation の指示文や完了条件、ユーザー指示の prompt への組み込み方を変更するとき。
- この調査呼び出しのファイルアクセス方針、作業ディレクトリ、文書検索範囲やエディタ入力 handoff の設定を変更するとき。

## Do not read this when
- 完全 prompt の共通構成や共通ポリシー文面を変更するときは、prompt 構築側や該当ポリシーの定義へ進む。
- 共通のアクセスモード、検索範囲、agent call parameter の定義を変更するときは、共通型の定義へ進む。
- 調査対象や文書検索範囲を決める処理が対象なら、その選択を行う呼び出し元を確認する。

## hash
- 7f613562c14718384a60865446a52bbb7484c5b92e71fc692771c815c8c6f691
