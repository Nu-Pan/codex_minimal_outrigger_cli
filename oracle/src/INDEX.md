# `oracle`

## Summary
- AIエージェント呼び出しの共通パラメータモデルと、用途別のプロンプト・モデル・推論強度・ファイルアクセス・作業ディレクトリ・事前 indexing 設定を構築する領域。
- oracle、realization、session join、TUI、indexing、feedback、quota probe など、目的別の agent call 定義へ進むための上位入口。
- 完全な構造化 prompt の組み立て、設定・パス・構造化文書の共通モデル、feedback 入力契約もこの領域から確認できる。

## Read this when
- AIエージェント呼び出しの共通契約や用途別の起動設定を確認・変更するとき。
- oracle、realization、session join、TUI、indexing、feedback、quota probe の agent call 構築処理を調査するとき。
- prompt の統合規則、パスコンテキスト、設定モデル、構造化文書モデル、feedback reporter の入力契約を確認するとき。

## Do not read this when
- 通常のサブコマンド実行フローや、構築済み agent call の実行処理を確認するとき。
- 個別の oracle・realization ファイルや実装内容そのものを調査するときは、対象ファイルまたは対応する下位定義を直接読む。
- Structured Output の項目・型・形式だけを確認するときは、対応する schema を直接読む。
- バックエンド固有のモデル解決や一般的なファイルアクセス実装だけを確認するときは、それぞれの直接の定義へ進む。

## hash
- 330d5c494cba12f1885fd7a08caa4b63b6d3826fa41095cef4929970f1a0ec1e
