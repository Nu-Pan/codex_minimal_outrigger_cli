# `oracle`

## Summary
- cmoc の oracle 実装を機能別に整理するディレクトリ。ACP agent call 設定、共通設定・パス・構造化文書処理、prompt builder 部品を扱う各下位領域への入口を提供する。

## Read this when
- ACP agent call の共通設定、prompt、Structured Output schema を調査・変更するとき。
- cmoc 固有設定、パス解決、規範構造、StructDoc の生成や Markdown レンダリングを調査するとき。
- oracle／realization 規則、ファイルアクセス制約、INDEX.md ルーティング規則などの prompt builder 部品を調査・変更するとき。

## Do not read this when
- CLI コマンドの通常処理、TUI の画面表示、Python 実行環境やテスト実行方法を直接確認したいとき。
- 個別の oracle 文書、realization 実装・テスト、または特定の下位機能の詳細だけを調査するときは、対応する下位ディレクトリやファイルを直接読む。

## hash
- ec341d179695c8d07de9ceaedb7e70766979fffb6a8b5344834dc167aeae2c5b
