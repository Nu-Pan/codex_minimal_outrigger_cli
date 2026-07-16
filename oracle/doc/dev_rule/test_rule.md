
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

- Codex agent が、cmoc managed ollama の実際の preflight を通るテスト、または cmoc managed ollama を provider とする Real Codex CLI テストを起動する場合は、そのテストを含む test command の最初の実行前に、command 単位で sandbox 外実行の承認を得ること
- 前項は対象テストだけを選択した実行にも、対象テストを含む full test suite の実行にも適用する。通常 sandbox 内で lock access などの失敗を一度発生させてから、sandbox 外で再実行する手順を標準としてはならない
- 承認要求は実行する test command に必要な範囲へ限定し、`~/.cmoc/ollama/lock` への書き込み、user systemd、`127.0.0.1:11434` の local service、および GPU の利用が必要であることを理由として示す
- sandbox 外実行が承認されない、または sandbox・host policy により必要な実環境へ access できない場合、その結果をテスト成功にも実装の失敗にも数えず、cmoc managed ollama を使用する実環境テストが未検証であることと、その理由を報告する。sandbox 制約を理由とする skip も、検証成功とはみなさない
- sandbox 外実行が承認され、必要な実環境へ access できる状態で発生した preflight またはテストの失敗は、通常のテスト失敗として原因を調査する
- テストの終了時にサービスを停止または disable したり、lock file や永続化したダウンロード資源を削除したりしてはならない。管理・ライフサイクル・lock の意味は `{{cmoc-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md` を正本とする

## Fake Codex CLI

- Real Codex CLI 呼び出しがテストの目的上不要な場合、Fake Codex CLI を使用してよい
- Fake Codex CLI は、cmoc 側の呼び出し構築、ログ保存、状態更新などを決定論的に検証するために使用する
- Codex CLI 呼び出し経路そのものの結合動作を検証する場合は、Fake Codex CLI ではなく cmoc managed ollama を provider とする Real Codex CLI 呼び出しを優先する
