# Codex model provider

## 設定

- cmoc は、Codex CLI 呼び出しごとに使用する model と model provider を `CmocConfigCodex` だけから決定する
- `CodexModelSpec.model_provider` は `str | None` とする
    - `None` は Codex CLI の既定 model provider を意味し、provider override と provider-local 設定を argv に渡さない
    - null でない値は Codex CLI の model provider ID として扱う
- `CmocConfigCodex.model_providers` は、model provider ID を、その provider に属する Codex config 値の mapping へ対応付ける
- null でない model provider ID は `CmocConfigCodex.model_providers` に存在しなければならない。存在しない場合は Codex CLI を起動する前にエラーとする
- Codex CLI の組み込み model provider を明示的に選択する場合を含め、provider-local 設定が不要なら空の mapping を provider 定義として使用してよい
- cmoc は model provider ID の allowlist または provider 固有 schema を持たず、Codex CLI が受理する model provider ID と provider-local key を許容する
- provider-local key は `model_providers.<provider ID>` の直下に属する key だけを表し、完全な Codex config path や provider 外の設定を含めてはならない
- provider-local 設定値は、null を除く JSON value の型であり、かつ TOML value へ一意に符号化できなければならない
- git 追跡対象の `CmocConfig` に secret 値を直接保存してはならない
- model provider の argv への反映方法は `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` を正本とする

## cmoc の責務境界

- cmoc は model provider の取得、配置、起動、停止、修復、疎通確認、model pull、cache 管理、または GPU 推論確認を行わない
- model provider の稼働、応答品質、provider-local 設定の意味、および認証要件は cmoc の保証対象外とし、Codex CLI と選択した model provider に委ねる
- cmoc は model provider を自動起動しない
