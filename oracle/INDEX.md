# `doc`

## Summary
- cmoc の正本ドキュメントを、アプリケーション仕様、開発規約、設計上の不採用案、branch・commit・worktree モデルに分けて案内する最上位ディレクトリ。対象領域が複数にまたがる場合のルーティング入口として機能する。
- `app_spec` は CLI、サブコマンド、Codex 呼び出し、出力・ログ、session/run、oracle・realization、feedback、通知などのアプリケーション挙動仕様を扱う。
- `dev_rule` は Python コーディング、CLI 実装配置、開発環境、テスト要件、テスト・品質検査の実行手順を扱う。
- `considered_alternative` は採用しなかった設計・運用案と、その採否理由を扱う。
- `branch_model.md` は session/run の分岐、commit、linked worktree、統合のモデルと責務境界を扱う。

## Read this when
- cmoc の正本文書全体から、機能仕様・開発規約・branch model・不採用案のどの領域を読むべきか判断するとき
- CLI の挙動、実装規約、テスト、session/run の状態や隔離、branch・commit・worktree の関係など、複数の文書領域にまたがる確認を始めるとき
- 現行仕様ではなく、過去に検討された代替方式の採否理由を調べるとき

## Do not read this when
- 対象となる下位ディレクトリまたは個別文書が明確な場合は、このディレクトリ全体ではなく該当する文書を直接読むとき
- 実装コード、テストコード、保存済み成果物、または oracle/doc の正本範囲外にある外部契約を確認するとき
- 現在の実行結果や具体的な操作結果だけを確認する場合は、対応する実装・テスト・レポートへ直接進むとき

## hash
- 2e9f690696a034adf4daae663e3e52b99af67406b700252dfbfda3da0ea120e9

# `src`

## Summary
- `oracle/src` は、oracle 配下の agent call 用ソース実装をまとめる階層です。agent call パラメータ、prompt 構築、設定・パスモデル、構造化文書、feedback・indexing などの実装を確認するときの入口で、具体的な責務は下位の `oracle` 配下へ進んで確認します。

## Read this when
- oracle のソース実装全体の構成や入口を把握したいとき
- agent call、prompt、設定・パス、feedback、indexing に関わる実装の参照先を選ぶとき

## Do not read this when
- oracle の正本仕様や agent call の実行結果そのものを確認したいとき
- 通常の CLI 呼び出し処理や実行制御を確認したいとき
- 特定の builder、policy、schema、設定モデルの詳細を確認したいときは、`oracle` 配下の該当対象を直接読む

## hash
- 6f0e71bda1237253b2c01e5c2bda46ab8144f1044b81ee2f416427aaff2f9312
