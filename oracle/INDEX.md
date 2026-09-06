# `doc`

## Summary
- `oracle/doc` 配下の正本仕様・開発ルールを横断して案内する上位入口。アプリケーション共通仕様、branch model、検討資料、開発ルール群から、目的に応じた下位文書へ進むためのルーティングを提供する。

## Read this when
- cmoc の正本ドキュメント全体から、アプリケーション共通仕様・branch/run model・開発ルール・設計判断資料のどこを読むべきか判断するとき
- 複数の仕様領域にまたがる調査や変更で、下位文書への入口を選ぶとき

## Do not read this when
- 対象の具体的な仕様ファイル、開発規則、実装、prompt、schema、provider 設定、feedback 観測、または個別サブコマンドの詳細が既に特定できているとき
- oracle/realization の個別内容や実装コードの内部構造だけを確認するとき

## hash
- a7a38a900f5b87c23c72949ca67038d20596cc172d54751b0211666dc8933c64

# `src`

## Summary
- Codex CLI を用いる cmoc の実装層で、agent call のパラメータ構築、prompt と policy の生成、パス・構造化文書・設定の共通処理を担う。
- quota probe、indexing、feedback、oracle、realization、session、TUI などの用途別 call builder と、editor input handoff や feedback reporter の入力契約を提供する。
- oracle と realization の扱い、ファイルアクセス制約、routing、Structured Output 連携を組み合わせて、用途ごとの agent call を構成する入口となる。

## Read this when
- cmoc の agent call 構築における共通パラメータ、prompt、policy、パス解決、構造化文書処理の責務分担を確認するとき。
- quota probe、indexing、feedback、oracle、realization、session、TUI の用途別 agent call builder や、editor input handoff・feedback reporter の入力契約を探すとき。
- oracle・realization の正本責務、ファイルアクセスモード、INDEX.md routing、Structured Output を agent call に組み込む方法を調べるとき。

## Do not read this when
- 特定用途の prompt、出力契約、起動パラメータの詳細だけを確認したいときは、該当する用途別 builder と schema を直接読む。
- agent call の実行処理や Codex CLI の実際の挙動を調べるときは、実行層や対応する外部仕様を直接確認する。
- oracle・realization・feedback の意味仕様、保存・受付処理、または個別の入力契約だけを調べるときは、それぞれの正本仕様や専用入力定義を直接読む。

## hash
- 39340166c0e1059ce1115273520875a712f43899db4538a882ffbf0de62d8b98
