# Codex model provider

## goal

- 通常の agent call の設定は、`CmocConfigCodex` の対応する一つの entry だけから直接決定する。対象は model provider、Model、および Reasoning Effort とする。回復確認 probe に限る例外は、本書の「回復確認 probe の設定例外」で定める
- Codex CLI が受理する名前を意味を変えずに渡し、cmoc 固有の論理分類や変換を介在させない

## agent call ごとの直接設定

本節の設定取得に対する例外は、本書の「回復確認 probe の設定例外」に限定する。

- 設定単位は、`AgentCallParameter.agent_call_kind` が表す安定した agent call 種別とする。cmoc はこの値を key として、`CmocConfigCodex` の対応する entry から設定を取得する
- 各 agent call 種別の設定は、model provider ID、Model 名、および Reasoning Effort 名を必須の直接文字列として持つ
- 対応する agent call 種別の設定が存在しない場合は、値を推測せず Codex CLI の起動前にエラーとする
- `CmocConfigCodex` の既定値は、すべての既存 agent call 種別に一つずつ対応する設定を持つ
- cmoc は、三つの直接文字列について、別名への解決、近い値への丸め、または fallback を行ってはならない
- cmoc は、Model、Reasoning Effort、および model provider の組み合わせに対する互換性検査や allowlist を持たない
- Codex CLI が設定を拒否した場合は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「`codex exec` が失敗した場合」に従う
- Structured Output の補正、retry、および回復待ち後の再開を個別の設定単位にしてはならない
- 設定データ構造、field 名、型、および既定値の正確な詳細は、`{{cmoc-root}}/oracle/src/oracle/other/cmoc_config.py` の `CodexCallConfig`、`CodexModelProviderConfig`、および `CmocConfigCodex` へ委譲する
- 取得した設定を Codex CLI の argv へ反映し、同じ agent call で維持する規則は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「Model provider、Model、Reasoning Effort」を正本とする

### 回復確認 probe の設定例外

一時障害の回復確認では、異なる条件での成功を、停止した呼び出しの復旧と誤認しないことを目的とする。対象の probe は独立した agent call のまま、probe 自身の設定 entry から取得する規則の例外として、停止した呼び出しで確定済みの model provider、Model、Reasoning Effort、および provider-local 設定を使用し、同じ認証適用先を確認する。

この例外は、一時障害による待機と、quota 待機から一時障害の確認へ切り替えた場合に適用する。一時障害の確認を始めた後に理由が quota へ変わっても、停止した呼び出しを再開するまで同じ確認条件を維持する。異なる条件での probe 成功を、その呼び出しの一時障害の復旧確認として使ってはならない。

一時障害の確認を含まない既存 quota 待機では、quota availability probe 自身の `agent_call_kind` に対応する設定を使用する。この経路全体への設定継承の拡張は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「未確定事項」に従う。待機理由の変更と確認結果の共有は、同文書の「回復待ちと再開」に従い、異なる確認条件の結果を混同しない。

この例外は、通常の作業呼び出しの設定取得・固定、probe の読み取り専用という境界、または provider に対する責務を変更しない。認証の解釈・更新は Codex CLI に委ね、cmoc が認証情報を解釈して複製・更新することは要求しない。

## provider 定義

- provider 定義 mapping は、model provider ID を単一 provider の provider-local 設定へ対応付ける
- 各 provider-local 設定は、provider-local key を null 以外の値へ対応付ける。値は JSON と TOML の双方へ一意に符号化できなければならない
- 設定された model provider ID が provider 定義 mapping に存在しない場合は、Codex CLI を起動する前にエラーとする
- `model_provider="openai"` は Codex CLI の組み込み既定 provider を選択する直接の provider ID とする
- `openai` を cmoc 固有の論理名または sentinel として扱わず、別の provider ID へ変換してはならない
- 既定の provider 定義には、provider-local 設定が空の `openai` を含める
- Codex CLI の組み込み model provider を明示的に選択する場合を含め、provider-local 設定が不要な provider は空の provider-local 設定を持ってよい
- cmoc は model provider ID の allowlist または provider 固有 schema を持たず、Codex CLI が受理する model provider ID と provider-local key を許容する
- provider-local key は選択した provider の定義直下に属する key だけを表し、完全な Codex config path や provider 外の設定を含めてはならない
- git 追跡対象の `CmocConfig` に secret 値を直接保存してはならない

## cmoc の責務境界

- cmoc は、設定された直接文字列と provider-local 設定を Codex CLI へ渡すところまでを責務とする
- cmoc は model provider の取得、配置、起動、停止、診断、修復、直接の疎通確認、model pull、cache 管理、または GPU 推論確認を行わない。Codex CLI を介した回復確認は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「回復確認 probe」の範囲に限定する
- model provider の稼働、応答品質、provider-local 設定の意味、および認証要件は cmoc の保証対象外とし、Codex CLI と選択した model provider に委ねる

## non-goal

- model provider 設定を理由に、prompt、sandbox、file access policy、network access、または通知設定を変更することは目的としない
