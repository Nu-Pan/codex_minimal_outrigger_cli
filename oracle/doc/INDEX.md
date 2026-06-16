# `app_specs`

## Summary

- この `docs/app_specs` ディレクトリの目次で、`cmoc` の利用手順と共通仕様の入口をまとめます。
- `usage.md`、`cli_auto_completion.md`、`codex_call.md`、`console_and_file_log.md`、`error_handling.md`、`indexing.md`、`misc_specs.md`、`run_isolation.md`、`session_state.md` を案内します。
- `oracle/`、`realization/`、`sub_commands/` を含み、個別仕様への入口と `INDEX.md` の更新方針をたどるためのハブです。

## Read this when

- `cmoc` の利用手順、共通仕様、エラー処理、ログ、パス、状態管理をまとめて把握したいとき。
- `usage.md`、`cli_auto_completion.md`、`codex_call.md`、`console_and_file_log.md`、`error_handling.md`、`indexing.md`、`misc_specs.md`、`run_isolation.md`、`session_state.md` のどれを読むべきか迷ったとき。
- `sub_commands/`、`oracle/`、`realization/` の各入口へ分岐する前に、この階層の全体像を確認したいとき。
- `INDEX.md` の更新や、`docs/app_specs` 配下のルーティングをたどりたいとき。

## Do not read this when

- 個別サブコマンドの仕様をすでに把握していて、`sub_commands/` 配下の該当文書へ直接進むとき。
- `oracle/` や `realization/` の個別仕様を直接確認したいだけで、この目次を経由する必要がないとき。
- `docs/` 配下の開発規約や代替案だけを確認したいとき。

## hash

- f92db23a3e0bad7a8542418641d9a32eee07e96e19e6b48bf0c075802169ece4

# `branch_model.md`

## Summary

- `cmoc` における通常ブランチ、session ブランチ、run ブランチ、commit、worktree の関係をまとめたブランチモデルの入口です。
- `repository-default-branch` を特別扱いしない方針と、`session fork` 時点の `local-branch` を `session home branch` とする考え方を示します。
- 各種 `cmoc-managed-branch` の命名規則と、`fork` / `join` に対応するコミットの意味をたどるための目次です。

## Read this when

- `cmoc` のブランチモデル全体を把握したいとき。
- `<local-branch>`、`<cmoc-session-branch>`、`<cmoc-run-branch>`、`<cmoc-session-home-branch>` の関係や役割を確認したいとき。
- `session fork` と `session join`、および run の fork / join における commit と worktree の対応関係を整理したいとき。
- ブランチ名・コミット名・worktree 名の命名規則を素早く参照したいとき。

## Do not read this when

- `cmoc` のブランチ命名や session/run の分離方針ではなく、個別サブコマンドの引数や手順だけを確認したいとき。
- `session fork` / `session join` / `apply` などの実装手順そのものを追いたいときは、この概念整理ではなく該当する正本仕様を直接読むべきです。
- `INDEX.md` の生成ルールや `oracle` 全体のルーティング方針だけを確認したいとき。

## hash

- c72ad07c95591dd5ecb3c243c6660fb623636f135e25b446bf9e141d00546f94

# `considered_alternatives`

## Summary

- `cmoc` で採用しなかった設計案と、その不採用理由をまとめたディレクトリの入口です。
- 修正点リスト後の作業計画立案、AI-generated kaizen の自動注入、作業計画レビューの不採用理由を扱います。
- `oracle` と実装の役割分担を考えるときに、代替案の判断材料をたどるための目次です。

## Read this when

- `cmoc apply` 系で、修正点リスト完成後に作業計画を立てる案を採用しなかった理由を確認したいとき。
- AI-generated kaizen を次回の実行コンテキストへ自動的に持ち越さない方針と、その理由を整理したいとき。
- `tgbt plan` や `/plan` のような作業計画レビューを採用しなかった背景や、人間が `oracle` を編集して AI が追従する方針を把握したいとき。

## Do not read this when

- `cmoc apply` 系の実装手順やコマンド仕様そのものを確認したいときは、該当する正本仕様を直接読むべきです。
- `INDEX.md` の生成ルールや `oracle` 全体のルーティング方針だけを確認したいときは、このディレクトリを読む必要はありません。
- この配下のうち特定の代替案だけを見たいときは、`apply_behavior.md`、`memory_alternative.md`、`working_plan_review.md` を直接参照すべきです。

## hash

- 5326c864cc9e8c75a90c03568805dc2c2049a51f0d7e375da4b44b4c92c0fe00

# `dev_rules`

## Summary

- `<cmoc-root>/oracle/docs/dev_rules/` 配下の開発ルール文書への入口です。
- `coding_rules.md`、`design_rules.md`、`development_environment.md`、`_format.md`、`test_rules.md` を案内します。
- cmoc の Python 実装規約、設計方針、開発環境、oracle 標準文書の書式、テスト規約を横断的にたどるための目次です。

## Read this when

- cmoc の実装や修正の前に、開発ルール全体の入口をまとめて把握したいとき。
- Python の書き方、CLI の配置方針、仮想環境や実行環境、標準文書の書式、テスト方針のどれを参照すべきか迷ったとき。
- `<cmoc-root>/src` や `<cmoc-root>/tests` で作業する前に、守るべき基本ルールを確認したいとき。
- 新しいコード、テスト、または oracle の標準文書を追加・修正する前に、関連する開発規約の所在を整理したいとき。

## Do not read this when

- `<cmoc-root>/oracle/docs/dev_rules/` 配下の個別文書をすでに特定していて、`coding_rules.md`、`design_rules.md`、`development_environment.md`、`_format.md`、`test_rules.md` のいずれかへ直接進むとき。
- コーディング規約だけ、設計規約だけ、開発環境だけ、テスト規約だけのように、単一テーマの正本仕様を確認したいとき。
- `docs/` の利用方法や `considered_alternatives/` の設計記録だけを探していて、開発ルールの入口は不要なとき。

## hash

- 0f9fb88e7a4e51c144f6bb706e0cdea6aed8fe7c5e5b039e8953f3f29a354f06

# `path_model.md`

## Summary

- `cmoc` におけるパス表記の基本ルールと、各 root token の意味をまとめた文書です。
- 絶対パス・相対パスの扱い、`<cmoc-root>` / `<repo-root>` / `<run-root>` / `<work-root>` の定義、具体例を説明します。
- パスの解決方法や表記の統一が必要な場面で参照するための入口です。

## Read this when

- `cmoc` で使う絶対パス・相対パスの書き方を確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` の定義と使い分けを整理したいとき。
- `run-root` と `repo-root`、`work-root` の関係や、どの root token を使うべきか迷ったとき。

## Do not read this when

- パス表記の規則を確認したいのではなく、個別コマンドや機能の仕様だけを確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` の意味がすでに確定していて、表記ルールを再確認する必要がないとき。
- `docs` 配下の入口や他のルーティング文書だけをたどりたいとき。

## hash

- 46aa1a2bfb1cc78be1fee42eede0977a5c288b0589890d7b73f18e0fc4d24703
