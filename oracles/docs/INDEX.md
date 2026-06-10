# `app_specs`

## Summary

- この `docs/app_specs` ディレクトリの目次で、`cmoc` の呼び出し手順から共通仕様、各サブコマンド入口までをまとめます。
- `usage.md`、`cli_auto_completion.md`、`codex_call.md`、`console_and_file_log.md`、`error_handling.md`、`misc_specs.md`、`run_isolation.md`、`session_state.md` を案内します。
- `indexing.md`、`oracles/`、`sub_commands/` を含み、`INDEX.md` の生成・更新方針と個別サブコマンド仕様への入口にもなります。

## Read this when

- `cmoc` の使い方、初期化、セッション・apply の往復をまとめて把握したいとき。
- `codex exec` 呼び出し、ログ出力、エラー処理、作業分離、セッション状態などの共通仕様を確認したいとき。
- `INDEX.md` の更新ルールや、`oracles` 配下の読み方、個別サブコマンド仕様への分岐点を素早くたどりたいとき。

## Do not read this when

- 個別サブコマンドの引数や状態遷移だけを確認したいときは、`sub_commands/` 配下の該当文書を直接読むべきです。
- `dev_rules/` 側のコーディング規則、設計方針、テスト規約だけを確認したいときは、この目次ではなくそちらを読むべきです。
- `README.md` や `AGENTS.md` などのリポジトリ運用ルールだけを確認したいときは、このディレクトリを読む必要はありません。

## hash

- 4be00bcd63f7ff157d91ddd63e43dfa4a83297ad985c790f4763d340116d89ea

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
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを確認したいとき。

## hash

- c72ad07c95591dd5ecb3c243c6660fb623636f135e25b446bf9e141d00546f94

# `considered_alternatives`

## Summary

- `cmoc` で採用しなかった設計案と、その不採用理由をまとめたディレクトリの入口です。
- 修正点リスト後の作業計画立案、AI-generated kaizen の自動注入、作業計画レビューの不採用理由を扱います。
- `oracles` と実装の役割分担を考えるときに、代替案の判断材料をたどるための目次です。

## Read this when

- `cmoc apply` 系で、修正点リスト完成後に作業計画を立てる案を採用しなかった理由を確認したいとき。
- AI-generated kaizen を次回の実行コンテキストへ自動的に持ち越さない方針と、その理由を整理したいとき。
- `tgbt plan` や `/plan` のような作業計画レビューを採用しなかった背景や、人間が `oracles` を編集して AI が追従する方針を把握したいとき。

## Do not read this when

- `cmoc apply` 系の実装手順やコマンド仕様そのものを確認したいときは、該当する正本仕様を直接読むべきです。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを確認したいときは、このディレクトリを読む必要はありません。
- この配下のうち特定の代替案だけを見たいときは、`apply_behavior.md`、`memory_alternative.md`、`working_plan_review.md` を直接参照すべきです。

## hash

- 5326c864cc9e8c75a90c03568805dc2c2049a51f0d7e375da4b44b4c92c0fe00

# `dev_rules`

## Summary

- `cmoc` の開発ルールをまとめたディレクトリの入口です。
- Python のコーディング規則、CLI と共通処理の設計方針、開発環境の前提、テスト実装規約を案内します。
- 実装やテストを書く前に、共通の作法と前提条件を素早く確認するための目次です。

## Read this when

- cmoc 全体のコーディング規則、設計方針、開発環境、テスト規約をまとめて確認したいとき。
- `src` と `tests` に実装を書く前に、共通の開発ルールを整理したいとき。
- Python の書き方、CLI の構成、仮想環境の扱い、テストの目的と範囲を俯瞰したいとき。

## Do not read this when

- cmoc の個別サブコマンドの仕様や引数だけを確認したいとき。
- `oracles` 全体のルーティング方針や他ディレクトリの入口文書だけを確認したいとき。
- `INDEX.md` の生成・更新ルールそのものだけを確認したいときは、ここではなく `indexing.md` を参照すべきとき。

## hash

- 3e4d31733982a9b80629b97d1b9396964a868e7cbfeda46f65c00eb9564a46fd

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
