# Codex model provider

## goal

- realization file の編集を主目的とする対象 call の model provider、Model、および Reasoning Effort を一つの設定元にまとめ、複数モデルによる編集の不整合と余計な修正コストを減らす
- Codex CLI が受理する名前を意味を変えずに渡し、cmoc 固有の論理分類や変換を介在させない

## agent call ごとの直接設定

通常の agent call は、builder が指定した `AgentCallParameter.agent_call_kind` をそのまま設定取得キーとし、`CmocConfigCodex.agent_calls` の対応する一つの entry から設定を直接取得する。この規則から外れる設定取得は、本書の「回復確認 probe の設定例外」に限定する。取得した設定を二つの agent call で共用する TUI の経路は、本節の「TUI 起動での設定の確定」に従う。

- realization apply の本命 call、realization refactor の所見調査・修正 call、feedback の issue remediation call、および run join の競合解消 call は、各 builder で realization 編集用の同じ `agent_call_kind` を直接指定し、設定を共有する。run join は、workload の自動 join と明示的な `cmoc run join` の両方を含む
- session join、汎用 TUI、oracle 調査、oracle 編集、feedback normalization、primary report の重要事項確認、および quota availability probe は、それぞれ独立した個別設定を持つ
- `agent_calls` に受理するキーは、委譲先が定める `agent_call_kind` の集合に限る。共有対象の builder 関数名をキーとする個別 entry や、共有設定への call ごとの個別上書きは受理しない
- 共有設定と各個別設定は、model provider ID、Model 名、および Reasoning Effort 名を必須の直接文字列として持つ
- 共有設定、必要な個別設定、または provider 定義が欠落しているか、定められた構造・型・値の制約・参照整合性を満たさない場合は、値を推測せず Codex CLI の起動前にエラーとする。対応する entry が欠落しても、`agent_call_kind` と異なるキーを使う設定取得へ fallback してはならない
- primary report の重要事項確認には、確認対象に含まれる本命 call の設定を流用しない。call の責務と builder は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「重要事項確認用 call」に従う
- cmoc は、三つの直接文字列について、別名への解決、近い値への丸め、または fallback を行ってはならない
- cmoc は、Model、Reasoning Effort、および model provider の組み合わせに対する互換性検査や allowlist を持たない
- Codex CLI が設定を拒否した場合は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「`codex exec` が失敗した場合」に従う。TUI への適用範囲は同文書の「TUI の新規起動と対話 resume」に従い、非対話の回復待ちを持ち込まない
- Structured Output の補正、retry、および回復待ち後の再開を個別の設定単位にしてはならない
- 設定データ構造、field 名、型、および既定値の正確な詳細は、`{{cmoc-root}}/oracle/src/oracle/other/cmoc_config.py` の `CodexCallConfig`、`CodexModelProviderConfig`、および `CmocConfigCodex` へ委譲する。受理する設定キーと各 entry の既定値は `CmocConfigCodex.agent_calls` を正本とする
- 取得した設定を Codex CLI の argv へ反映し、同じ agent call で維持する規則は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「Model provider、Model、Reasoning Effort」を正本とする

### TUI 起動での設定の確定

汎用 TUI と oracle 調査 TUI の新規起動では、初回 exec の開始時に、元の workload の `agent_call_kind` に対応する model provider・Model・Reasoning Effort・provider-local 設定を取得して確定する。初回 exec と自動移行先 TUI は別の agent call だが、その確定値を共用し、移行時には再取得しない。一回の起動操作の途中で設定が変わることを避けるためである。

後日の公開 `cmoc resume` は、再開時点の同じ workload の設定を取得する。`resume` 専用の agent call 種別や設定 entry は設けない。

共用するのは設定値であり、process の接続や実行 context ではない。各 process への設定適用と MCP・通知の準備は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「対話 resume の process」に従う。

### 回復確認 probe の設定例外

一時障害の回復確認では、異なる条件での成功を、停止した呼び出しの復旧と誤認しないことを目的とする。対象の probe は独立した agent call のまま、probe 自身の設定 entry から取得する規則の例外として、停止した呼び出しで確定済みの model provider、Model、Reasoning Effort、および provider-local 設定を使用し、同じ認証適用先を確認する。

この例外は、一時障害による待機と、quota 待機から一時障害の確認へ切り替えた場合に適用する。一時障害の確認を始めた後に理由が quota へ変わっても、停止した呼び出しを再開するまで同じ確認条件を維持する。異なる条件での probe 成功を、その呼び出しの一時障害の復旧確認として使ってはならない。

一時障害の確認を含まない既存 quota 待機では、quota availability probe 自身の `agent_call_kind` に対応する設定を使用する。この経路全体への設定継承の拡張は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「未確定事項」に従う。待機理由の変更と確認結果の共有は、同文書の「回復待ちと再開」に従い、異なる確認条件の結果を混同しない。

この例外は、通常の作業呼び出しの設定取得・固定、probe の読み取り専用という境界、または provider に対する責務を変更しない。認証の解釈・更新は Codex CLI に委ね、cmoc が認証情報を解釈して複製・更新することは要求しない。

## provider 定義

- provider 定義 mapping は、model provider ID を単一 provider の provider-local 設定へ対応付ける
- 各 provider-local 設定は、provider-local key を null 以外の値へ対応付ける。値は JSON と TOML の双方へ一意に符号化できなければならない
- `model_provider="openai"` は Codex CLI の組み込み既定 provider を選択する直接の provider ID とする
- `openai` を cmoc 固有の論理名または sentinel として扱わず、別の provider ID へ変換してはならない
- Codex CLI の組み込み model provider を明示的に選択する場合を含め、provider-local 設定が不要な provider は空の provider-local 設定を持ってよい
- cmoc は model provider ID の allowlist または provider 固有 schema を持たず、Codex CLI が受理する model provider ID と provider-local key を許容する
- provider-local key は選択した provider の定義直下に属する key だけを表し、完全な Codex config path や provider 外の設定を含めてはならない
- git 追跡対象の `CmocConfig` に secret 値を直接保存してはならない

## cmoc の責務境界

- cmoc は、設定された直接文字列と provider-local 設定を Codex CLI へ渡すところまでを責務とする
- cmoc は model provider の取得、配置、起動、停止、診断、修復、直接の疎通確認、model pull、cache 管理、または GPU 推論確認を行わない。Codex CLI を介した回復確認は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「回復確認 probe」の範囲に限定する
- model provider の稼働、応答品質、provider-local 設定の意味、および認証要件は cmoc の保証対象外とし、Codex CLI と選択した model provider に委ねる

## non-goal

- model provider の設定や設定の共有を理由に、各 workload の意味・権限・prompt・call 数、sandbox、file access policy、network access、または通知設定を変更することは目的としない
- session join と汎用 TUI は oracle も扱うため、これらの経路で行う realization 編集までモデル設定を完全に統一することは目的としない
- 汎用 profile 機構は設けない
- 旧設定との互換対応、移行、旧形式の読み込み、または旧 key 専用の検出・診断・案内は行わず、現行の設定構造だけを生成・検証する
