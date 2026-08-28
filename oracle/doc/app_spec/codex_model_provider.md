# Codex model provider

## goal

- 各 agent call で使用する model provider、Model、および Reasoning Effort を、`CmocConfigCodex` の一つの対応 entry だけから直接決定する
- Codex CLI が受理する名前を意味を変えずに渡し、cmoc 固有の論理分類や変換を介在させない

## agent call ごとの直接設定

- 設定単位は、`AgentCallParameter.agent_call_kind` が表す安定した agent call 種別とする
- 各 agent call 種別の設定は、model provider ID、Model 名、および Reasoning Effort 名を必須の直接文字列として持つ
- model provider ID は null を許容しない
- 対応する agent call 種別の設定が存在しない場合は、値を推測せず Codex CLI の起動前にエラーとする
- `CmocConfigCodex` の既定値は、全ての既存 agent call 種別に一つずつ対応する設定を持つ
- cmoc は、三つの直接文字列を別名へ解決し、近い値へ丸め、または fallback してはならない
- cmoc は、Model、Reasoning Effort、および model provider の組み合わせに対する互換性検査や allowlist を持たない
- Codex CLI が設定を拒否した場合は、既存の Codex CLI 呼び出し失敗規則に従う
- Structured Output の補正、retry、および quota 待機後の resume を個別の設定単位にしてはならない
- 設定データ構造、field 名、型、および既定値の正確な詳細は、`{{cmoc-root}}/oracle/src/oracle/other/cmoc_config.py` の `CodexCallConfig`、`CodexModelProviderConfig`、および `CmocConfigCodex` へ委譲する
- `agent_call_kind` から設定を取得して Codex CLI の argv へ反映する規則は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「Model provider、Model、Reasoning Effort」を正本とする

## provider 定義

- provider 定義 mapping は、model provider ID を単一 provider の provider-local 設定へ対応付ける
- 各 provider-local 設定は、provider-local key を null 以外の JSON/TOML 共通値へ対応付ける
- 設定された model provider ID が provider 定義 mapping に存在しない場合は、Codex CLI を起動する前にエラーとする
- `model_provider="openai"` は Codex CLI の組み込み既定 provider を選択する直接の provider ID とする
- `openai` を cmoc 固有の論理名または sentinel として扱わず、別の provider ID へ変換してはならない
- 既定の provider 定義には、provider-local 設定が空の `openai` を含める
- Codex CLI の組み込み model provider を明示的に選択する場合を含め、provider-local 設定が不要な provider は空の provider-local 設定を持ってよい
- cmoc は model provider ID の allowlist または provider 固有 schema を持たず、Codex CLI が受理する model provider ID と provider-local key を許容する
- provider-local key は選択した provider の定義直下に属する key だけを表し、完全な Codex config path や provider 外の設定を含めてはならない
- provider-local の値は null を許容せず、JSON value と TOML value の双方へ一意に符号化できなければならない
- git 追跡対象の `CmocConfig` に secret 値を直接保存してはならない

## cmoc の責務境界

- cmoc は、設定された直接文字列と provider-local 設定を Codex CLI へ渡すところまでを責務とする
- cmoc は model provider の取得、配置、起動、停止、修復、疎通確認、model pull、cache 管理、または GPU 推論確認を行わない
- model provider の稼働、応答品質、provider-local 設定の意味、および認証要件は cmoc の保証対象外とし、Codex CLI と選択した model provider に委ねる

## non-goal

- model provider 設定を理由に、prompt、sandbox、file access policy、network access、または通知設定を変更することは目的としない
