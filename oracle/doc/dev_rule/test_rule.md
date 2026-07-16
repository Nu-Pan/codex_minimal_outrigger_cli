
# cmoc テスト実装規約

## 基本

- pytest を使用する
- realization test は `{{cmoc-root}}/test` に実装する

## goal

- cmoc の決定論的な制御ロジックが仕様どおりに動作する事を検証する
    - e.g. git 状態の検査、作業ディレクトリの決定、対象ファイルの列挙、設定生成、ログ保存、状態更新、エラー処理、…
- Real Codex CLI 呼び出しを伴う経路では、cmoc managed ollama を provider として使用し、cmoc が責任を持つ結合動作を検証対象に含める
    - e.g. profile 生成、prompt 渡し、出力保存、schema 指定、…

## non-goal

- LLM の回答品質や、Codex CLI に依頼した仕事の意味的な成功は cmoc の自動テストの目的としない
- Codex CLI 自体、外部 provider、有料クラウド backend の正しさや安定性を保証することは目的としない

## テスト用開発対象リポジトリパス

- `python-dev-skill` が pytest の隔離に使用する `tmp_path` を `{{test-root}}` とし、被テスト cmoc が動作する環境全体をそのツリー内に構築する
- cmoc managed ollama のサービス、サービス設定、および永続化したダウンロード資源はこの隔離の対象外とし、本番実行とテストで共有する
- cmoc managed ollama の管理・ライフサイクル・配置先は `{{cmoc-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md` を正本とする
- 前項の例外を除いてテストが `{{test-root}}` ツリー内で収まりさえすれば、それ以外は agent の裁量で決めて良い

## クラウドバックエンド

- テスト目的での Real Codex CLI 呼び出しで、ChatGPT サブスクリプション枠や従量課金のクラウド API などの「お金がかかるモデル」を使用するのは禁止

## ollama バックエンド

- Real Codex CLI 呼び出しを伴うテストを実行する際は、原則として cmoc managed ollama を Codex CLI の model provider として使用する
- テスト用の SLM としては `qwen3:4b-instruct-2507-q4_K_M` を使うこと
- テスト目的の場合は `AgentCallParameter.model_class` に対応する Codex CLI provider/model を cmoc managed ollama とテスト用 SLM に切り替えてよい

### Codex agent sandbox からの実行

- cmoc managed ollama を使用する test command は、`{{cmoc-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md` の sandbox 外実行規則に従う
- sandbox 外実行が承認されない、または必要な実環境へ access できない場合は、該当テストを成功または失敗とみなさず、未検証の理由を報告する

## Fake Codex CLI

- Real Codex CLI 呼び出しがテストの目的上不要な場合、Fake Codex CLI を使用してよい
- Fake Codex CLI は、cmoc 側の呼び出し構築、ログ保存、状態更新などを決定論的に検証するために使用する
- Codex CLI 呼び出し経路そのものの結合動作を検証する場合は、Fake Codex CLI ではなく cmoc managed ollama を provider とする Real Codex CLI 呼び出しを優先する
