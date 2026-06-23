# `app_spec`

## Summary

- この `app_spec` ディレクトリのルーティング文書で、cmoc の利用手順と共通仕様への入口をまとめます。
- `usage.md`、`sub_command/`、`indexing.md`、`run_isolation.md`、`session_state.md`、`console_and_file_log.md`、`error_handling.md`、`codex_exec_rule.md`、`cli_auto_completion.md`、`prompt_standard.md`、`misc_spec.md` へ分岐します。
- `sub_command/` は `apply` 系、`session` 系、`init`、`indexing`、`review oracle` の個別仕様へ進むための入口です。

## Read this when

- cmoc の利用手順、共通仕様、実行制約、ログ、エラー処理、状態管理をどの順で読むか整理したいとき。
- `cmoc` の通常利用フローや `apply` / `session` 系の入口をまとめて把握したいとき。
- `app_spec` 配下のどの文書に何が書かれているか確認し、`sub_command/` 配下の個別サブコマンド仕様へ進む前に役割分担を整理したいとき。

## Do not read this when

- `usage.md` や `sub_command/` 配下の個別文書へ直接進む先がすでに決まっていて、この階層の案内が不要なとき。
- `cli_auto_completion.md`、`codex_exec_rule.md`、`console_and_file_log.md`、`error_handling.md` など、個別の共通仕様だけを確認したいとき。
- この階層全体ではなく、別の `oracle` 配下ディレクトリや上位のルーティング文書を探しているとき。

## hash

- 5c023b06c0469fd2e3de97be526cfb2c1426731caf37201bf85867b6f7e359b2

# `branch_model.md`

## Summary

- `cmoc` における通常ブランチ、session ブランチ、run ブランチ、commit、worktree の関係をまとめたブランチモデルの入口です。
- `repository-default-branch` を特別扱いしない方針と、`session fork` 時点の `local-branch` を `session home branch` とする考え方を示します。
- 各種 `cmoc-managed-branch` の命名規則と、`fork` / `join` に対応するコミットの意味をたどるための目次です。

## Read this when

- cmoc のブランチモデル全体を把握したいとき。
- `<local-branch>`、`<cmoc-session-branch>`、`<cmoc-run-branch>`、`<cmoc-session-home-branch>` の関係や役割を確認したいとき。
- `session fork` と `session join`、および run の fork / join における commit と worktree の対応関係を整理したいとき。
- ブランチ名・コミット名・worktree 名の命名規則を素早く参照したいとき。

## Do not read this when

- cmoc のブランチ命名や session/run の分離方針ではなく、個別サブコマンドの引数や手順だけを確認したいとき。
- `session fork` / `session join` / `apply` などの実装手順そのものを追いたいとき。
- `INDEX.md` の生成ルールや oracle 全体のルーティング方針だけを確認したいとき。

## hash

- 3548445dc5441fa2e2e774ba8b45d8bdaaf363b110f5e8a3f4704bdac6cdf3af

# `considered_alternative`

## Summary

- `cmoc apply` 系サブコマンドで採用しなかった設計判断をまとめる文書群への入口です。
- 修正点リスト後に追加の作業計画を立てない理由、AI-generated kaizen を自動注入しない理由、作業計画レビューを採用しない理由を案内します。
- 明示的な仕様・入力・ログ・成果物を優先し、暗黙記憶や準仕様レイヤーを増やさない方針を整理する節目です。

## Read this when

- 修正点リスト完成後に作業計画を立てる案を採るべきか検討したいとき。
- AI が生成した改善案を次回以降へ自動反映すべきか判断したいとき。
- 作業計画レビューを採用しなかった理由や、人間が `oracle` を編集して AI が追従する方針の背景を知りたいとき。

## Do not read this when

- `cmoc apply` 系の実装手順やコマンド仕様そのものを確認したいとき。
- AI-generated kaizen の扱いではなく、セッション・レビュー・他サブコマンドの仕様を確認したいとき。
- `INDEX.md` の生成ルールや `oracle` 全体のルーティング方針だけを確認したいとき。

## hash

- 1ad6daf0acaae977b28c2cbee5e1760cf36356b75d12c6cf142e4f3d962482f2

# `dev_rule`

## Summary

- この `dev_rule` ディレクトリのルーティング文書で、`coding_rule.md`、`design_rule.md`、`development_environment.md`、`test_rule.md` への入口です。
- cmoc の Python 実装規約、CLI 設計方針、開発環境、テスト規約を横断的にたどるための目次です。
- 実装やテストの前に、どの開発ルールを読むべきか迷ったときの起点です。

## Read this when

- cmoc の実装や修正の前に、開発ルール全体の入口をまとめて把握したいとき。
- Python の書き方、CLI の配置方針、仮想環境や実行環境、テスト方針のどれを参照すべきか迷ったとき。
- `<cmoc-root>/src` や `<cmoc-root>/test` で作業する前に、守るべき基本ルールを確認したいとき。
- 新しいコード、テスト、または oracle の標準文書を追加・修正する前に、関連する開発規約の所在を整理したいとき。

## Do not read this when

- このディレクトリの個別文書をすでに特定していて、`coding_rule.md`、`design_rule.md`、`development_environment.md`、`test_rule.md` のいずれかへ直接進むとき。
- コーディング規約だけ、設計規約だけ、開発環境だけ、テスト規約だけのように、単一テーマの正本仕様を確認したいとき。
- この階層ではなく、別の `oracle` 配下の自然言語仕様や Structured Output schema を探しているとき。

## hash

- c1fea811a659d60c1026cb0cff145c59f0af412ed0e06fbdc61402924b088a7f
