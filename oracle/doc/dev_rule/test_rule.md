
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

- pytest の `tmp_path` を `<test-root>` とする
- realization test 上の実行中、被テスト cmoc が動作する環境は `<test-root>` ツリー内に構築する
- テストが `<test-root>` ツリー内で収まりさえすれば、それ以外は agent の裁量で決めて良い

## クラウドバックエンド

- 被テスト目的で実行される Codex CLI で、ChatGPT サブスクリプション枠や・従量課金のクラウド API などの「お金がかかるモデル」を使用するのは禁止

## ollama バックエンド

- Codex CLI 呼び出しを伴うテストを実行する際は、原則としてローカル実行の SLM を バックエンドとして使用する
- テスト目的の場合は oracle src 上の構築関数が返した `AgentCallParameter` のモデル指定をオーバーライドして SLM に切り変えて良い

## Fake Codex CLI

- Codex CLI のサブスクリプション枠のモデルを使わないと成立しないテストについては Fake Codex CLI を使用する
