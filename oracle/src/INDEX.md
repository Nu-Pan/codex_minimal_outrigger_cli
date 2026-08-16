# `oracle`

## Summary
- AI コーディングエージェント呼び出しの prompt、アクセス権限、モデル・推論設定、作業ディレクトリ、Structured Output を構築する定義群。共通パラメータ契約を確認し、用途別の agent call 設定や下位領域へ進むための入口となる。

## Read this when
- agent call builder の共通パラメータ契約、論理モデル、推論強度、ファイルアクセスモードを確認するとき
- 用途別 agent call の prompt、起動設定、Structured Output、indexing preflight の扱いを調査するとき
- 複数の agent call 定義にまたがる構成を確認し、feedback、indexing、oracle、realization、session、tui の各下位領域への入口を探すとき

## Do not read this when
- 実際の agent call の実行処理やサブコマンド全体の制御フローを確認するとき
- 個別の oracle file、realization file、feedback state、session の Git 操作そのものを確認するとき
- 共通 prompt の生成規則や Codex CLI sandbox の正本仕様を確認するとき

## hash
- 3299bf6bef8d14ad5215cffe34f05e72e03105f38830c075f120b86644e72b9a
