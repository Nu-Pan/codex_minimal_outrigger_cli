
# cmoc テスト実装規約

## 基本

- pytest を使用する
- realization test は `<cmoc-root>/test` に実装する

## goal

- cmoc の決定論的な制御ロジックが仕様どおりに動作する事を検証する
- e.g. git 状態の検査、作業ディレクトリの決定、対象ファイルの列挙、…

## non-goal

- Codex CLI や LLM の挙動そのものは cmoc の自動テストの目的としない
- e.g. Codex CLI に依頼した仕事の結果が期待通りの品質であることの確認

## テスト用開発対象リポジトリパス

TODO 埋める

- cmoc の realization test で cmoc が操作する開発対象 Git repository のルートディレクトリを `<test-root>` とする
- 原則として pytest の `tmp_path` 直下の `target` directory に作成する

- `<test-target-root>` = `<tmp_path>/target`
- main worktree を使うテストでは `<repo-root>` と `<work-root>` は `<test-target-root>` に一致する
- linked worktree を使うテストでは `<repo-root>` は `<test-target-root>` のまま、`<work-root>` は linked worktree root になる
- cmoc 管理 linked worktree は `<test-target-root>/.cmoc/local/worktree/<purpose>` 配下に作る
- repo 外 linked worktree の検証が目的である場合に限り、`<tmp_path>/external-worktree/<purpose>` 配下に作ってよい
- fake Codex executable、record file、schema file、CODEX_HOME など、開発対象 repository ではない補助ファイルは `<tmp_path>` 配下の用途別 directory に置いてよい

テストコードでは、開発対象 repository root を `target_root`、実行対象 worktree root を `work_root` または `linked_work_root` と呼ぶ。

## クラウドバックエンド

- ChatGPT サブスクリプション枠や、従量課金のクラウド API などの「お金がかかる方法」のテストでの使用は禁止

## ollama バックエンド

- Codex CLI 呼び出しを伴うテストを実行する際は、原則として、ローカルで起動した ollama でサーブされる SLM をバックエンドとして使用する
- TODO 埋める

## Fake Codex CLI

- Codex CLI のサブスクリプション枠のモデルを使わないと成立しないテストについては Fake Codex CLI を使用する
