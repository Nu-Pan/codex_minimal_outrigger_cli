# `doc`

## Summary
- `oracle/doc` 配下の正本文書群を、cmoc の共通仕様・設計検討・開発ルール・アプリケーション仕様へ案内する最上位の入口です。`app_spec`、`branch_model.md`、`considered_alternative`、`dev_rule` から、対象の仕様・用語・不採用案・開発手順に応じた下位文書を選びます。

## Read this when
- cmoc の正本仕様・設計資料・開発ルールを横断して探すとき
- アプリケーション共通仕様、branch／commit／worktree のモデル、不採用となった設計案、Python・CLI・環境・テストの開発規約の参照先を判断するとき
- 対象文書が複数の仕様領域にまたがり、まず適切な下位ディレクトリまたは文書を選ぶ必要があるとき

## Do not read this when
- 対象の個別仕様書や開発ルール文書が明らかな場合は、その文書を直接読むとき
- 特定機能の実装、prompt、Structured Output schema、テスト実行手順など、既に対象が明確な下位内容だけを確認したいとき
- `oracle/doc` 配下の文書と無関係な realization、実装ファイル、既存の INDEX.md の内容を確認するとき

## hash
- ed14661f8a936ff7b45ee16838fea19ff16b0e64c4072e348dfc9a5bed13a512

# `src`

## Summary
- `oracle/src` は、cmoc の agent call と prompt 構築を支える実装の上位入口です。agent call の用途別起動定義、prompt の共通構築、ファイルアクセス・oracle・realization・feedback・routing などの規定、パス・設定・構造化文書の共通モデルを横断して確認できます。配下には、起動定義を扱う `acp_builder`、prompt と policy を扱う `prompt_builder`、共通モデルを扱う `other`、feedback 入力契約を扱う領域があります。

## Read this when
- agent call の用途別起動定義、prompt 構築、共通 policy、feedback、パスや設定モデルの責務を横断して調査・変更するとき
- 対象となる下位領域がまだ特定できず、oracle 側の agent call または prompt 関連実装への入口を選ぶとき
- oracle review、oracle edit、realization apply/refactor、feedback、indexing、session join、TUI など複数の処理系にまたがる構築規則を確認するとき

## Do not read this when
- 特定の agent call の起動パラメータ、個別の prompt policy、構造化文書モデル、パスモデル、設定モデルを直接調査するときは、対応する下位対象へ進むとき
- CLI サブコマンドの実行処理、TUI の表示処理、正本仕様や realization file の内容だけを確認するとき
- Structured Output の個別スキーマだけを確認するときは、対応するスキーマを直接読むとき

## hash
- 965a5ef4ec8ef6c695138a88bc6855fd5e34e6eae0af391699bb56914ec871a1
