# cmoc テスト実装規約

## 責務境界

- この文書は、realization test が満たすべき意味上の要件を定める
- 構築済み環境で test と品質検査を選択、実行、完了判定、および報告する手順は、`{{cmoc-root}}/oracle/doc/dev_rule/test_execution.md` を正本とする
- 開発環境の新規構築、依存関係の追加、および pip 操作は、`{{cmoc-root}}/oracle/doc/dev_rule/development_environment.md` を正本とする

## 基本

- pytest を使用する
- realization test は `{{cmoc-root}}/test` に実装する
- pytest の `tmp_path` を `{{test-root}}` とし、被テスト cmoc の HOME、repository、worktree、設定、および実行成果物をそのツリー内に構築する

## goal

- cmoc の決定論的な制御ロジックが仕様どおりに動作する事を検証する
    - e.g. git 状態の検査、作業ディレクトリの決定、対象ファイルの列挙、設定生成、ログ保存、状態更新、エラー処理、…
- Codex CLI 呼び出しを伴う経路では、cmoc が責任を持つ結合動作を検証する
    - e.g. prompt 渡し、argv による設定、出力保存、schema 指定、response 後の処理、…
    - 実行経路の要件は、本書の「実経路統合テスト」で定める

## non-goal

- LLM の回答品質や、Codex CLI に依頼した仕事の意味的な成功は cmoc の自動テストの目的としない
- Codex CLI 自体または model provider の正しさや安定性を保証することは目的としない

## 実経路統合テスト

### 用語と選択

- 正本用語は「実経路統合テスト」とする
- 個々の test case は「実経路統合テストケース」と表記する
- `e2e` を実経路統合テストの同義語、正本用語、または pytest marker として導入してはならない
- 実経路統合テストを分離選択する pytest marker が必要な場合は、`real_path_integration` だけを使用する

### 検証要件

- 実経路統合テストとは、利用者向け CLI entrypoint を独立 process で実行し、本番と同じ code path、実在の外部 executable、および必要な実推論を使って、response 後の処理と外部から観測可能な結果まで検証する realization test である
- 実行時点で公開されている全末端サブコマンドを対象とする
- 各実経路統合テストケースは、終了 code とコマンド固有の外部から観測可能な結果を検証する
- 公開末端サブコマンドと実経路統合テストケースの対応は、機械的に比較可能にする
- 公開末端サブコマンドの追加または rename に対して、対応する実経路統合テストケースがなければ test を失敗させる
- Codex CLI 呼び出しには、実在の Codex CLI executable と実推論を使用する
- Fake、mock、stub、記録済み response、または起動確認だけでは実経路統合テストを代替できない
- 本番との差は、`{{test-root}}` による隔離、決定論的な入力、対話操作の自動化、および本書が定めるテスト用 `CmocConfig` の直接設定に必要な範囲だけ許容する
- `--help`、shell completion、不正入力、事前条件違反、handler の直接呼び出し、または process を分離しない確認は、実経路統合テストとはみなさない
- 新規の公開末端サブコマンドには、同じ変更で対応する実経路統合テストケースを追加する

### Model provider、Model、Reasoning Effort、および quota

- 実経路統合テストから発生する各 agent call は、テスト用 `CmocConfig` の対応する `agent_call_kind` entry から model provider、Model、および Reasoning Effort の直接文字列を取得する
- テスト用 `CmocConfig` には、実経路統合テストから発生する各 agent call 種別の設定を用意する
- テスト用 `CmocConfig` の直接設定は、必要な実推論を維持しながら実経路統合テストの quota 消費を抑えるために、通常の既定設定と異なる値を使用してよい
- 実経路統合テスト専用の cmoc 固有なモデル分類または推論強度分類を導入してはならない
- 自動テストによる quota 消費を一律には禁止せず、テスト用 `CmocConfig` で選択される model provider の quota 消費を許容する
- 実経路統合テストの仕様または pytest command へ、具体的な model provider または Model 名を固定してはならない
- model provider に対する cmoc の責務境界は、`{{cmoc-root}}/oracle/doc/app_spec/codex_model_provider.md` を正本とし、実経路統合テストのために広げてはならない
- quota 枯渇時の待機と再開を含む通常の Codex CLI 呼び出し規則は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` を正本とする

## Fake Codex CLI

- Fake Codex CLI は、実経路統合テスト以外で Real Codex CLI が不要な場合に限り、決定論的な制御ロジックの検証に使用してよい
