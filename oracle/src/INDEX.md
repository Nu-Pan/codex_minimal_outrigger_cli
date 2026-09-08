# `oracle`

## Summary
- cmoc の agent call 構築、prompt 構成、設定・パスモデル、構造化文書処理を担う実装群への入口。
- oracle・realization・feedback・indexing・session・TUI など、用途別の agent call とその入力契約を確認できる。
- agent call のファイルアクセスモード、作業ディレクトリ、モデル設定、Structured Output schema、prompt 部品の定義を横断して扱う。

## Read this when
- cmoc の agent call 共通パラメータ、ファイルアクセスモード、cwd、モデル・並列数などの設定を確認するとき。
- 用途別の agent call builder、prompt builder、Structured Output schema、feedback 入力契約を探すとき。
- agent call で使う root placeholder の導出・解決や、構造化文書の Markdown レンダリングを確認するとき。

## Do not read this when
- 特定の agent call の prompt、出力契約、または個別処理の実装詳細だけを確認したいときは、該当する下位ファイルを直接読む。
- oracle・realization・feedback・session の具体的な業務処理や保存手順だけを調べたいとき。
- Codex CLI 自体の実行挙動や、永続化された設定ファイルの人手による編集方法だけを確認したいとき。

## hash
- 7ee4206d3bfe14bd906ce4988193084f252b317c2b73ca1ee148a681f675cd83
