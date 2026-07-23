# `__init__.py`

## Summary
- `cmoc oracle review` builder の realization adapter package。oracle review ビルド処理に関する実装への入口。

## Read this when
- `cmoc oracle review` builder の realization adapter package の責務や関連実装を確認するとき。

## Do not read this when
- oracle review の正本仕様や、builder 以外の CLI 実装を確認するとき。

## hash
- 84497f0a0d2660a41158b931a250159397e20e8d81643dd88eac4315ffeb3813

# `enumerate_finding.py`

## Summary
- oracle review の finding enumeration 用 canonical builder を再公開する互換アダプター。既存の旧 import 呼び出し元を維持し、処理本体は oracle 側の実装へ委譲する。全呼び出し元の移行後は削除可能。

## Read this when
- oracle review の finding enumeration builder の旧 import 経路を維持・移行・削除するとき
- canonical oracle 実装への委譲や旧呼び出し元の互換性を確認するとき

## Do not read this when
- canonical な builder の仕様や実装詳細を確認したいとき
- oracle review の別機能を調査するときは、対応する oracle 実装を直接読む

## hash
- 8b9b36fc04d35cc98f97d8ccb70ef670f831d8bf5a404485e69ebbae393097ba

# `judge_finding.py`

## Summary
- oracle review の finding judgment 用 canonical 実装を呼び出す realization adapter。既存 caller との互換 import を提供し、全 caller 移行後に削除される一時的な入口。

## Read this when
- `acp.builder.oracle.review.judge_finding` からの既存 import 互換性や caller 移行状況を確認するとき。

## Do not read this when
- canonical な finding judgment の仕様・実装を確認するときは、oracle 側の `judge_finding.py` を直接読む。
- 新規 caller を canonical 実装へ追加するとき。

## hash
- 8c89b49504ced72c72b0b1888c50793774ec56790e357a902d09b07cfbd7b1ae

# `merge_finding.py`

## Summary
- Oracle の merge-finding parameter builder を呼び出し、生成された prompt に既知の oracle-root placeholder typo の限定的な補正を適用する realization 実装。入力 finding は変更せず、prompt の placeholder 定義部分だけを対象にする。

## Read this when
- merge-finding 用 agent call parameter の生成や prompt 補正の挙動を変更・確認するとき
- oracle builder の出力に含まれる既知 placeholder typo への互換補正を調査するとき

## Do not read this when
- merge-finding の正本仕様や builder 本体の定義を確認したいときは、参照されている oracle source を直接読む
- merge-finding 以外の agent call parameter や一般的な prompt 規約を扱うとき

## hash
- 3b6a5b70b2dd6e2f4f9814aeb3213984433a0d490676f65dc6b5755325c43911

# `validate_finding_advocate.py`

## Summary
- oracle review の finding advocate 用 AgentCallParameter を生成する canonical builder を呼び出し、prompt 内の既知の oracle root placeholder typo だけを補正する。finding と既知の advocate/challenger 理由はそのまま保持する。

## Read this when
- oracle review の finding advocate 用パラメータ生成や、canonical prompt の typo 補正を確認・変更するとき。

## Do not read this when
- challenger 用 builder の実装や、canonical advocate prompt 自体の仕様を確認したいとき。

## hash
- 0403ae214e76b31656c2f69e32e94e0ce6946e35e1c28eb0d38e408ee50bd749

# `validate_finding_challenger.py`

## Summary
- oracle review の challenger validation 実装を参照する realization adapter。旧 realization import caller との互換入口を提供し、canonical な oracle 実装へ委譲する。

## Read this when
- oracle review の challenger validation の import 経路や互換 adapter を変更・確認するとき。
- 旧 `acp.builder.oracle.review.validate_finding_challenger` caller の削除可否を調べるとき。

## Do not read this when
- canonical な challenger validation の仕様や実装内容を確認したいときは、oracle 側の実装を直接読む。
- oracle review と無関係な builder や validation の処理を調べるとき。

## hash
- b9445fef10e9cfc9f8e89bd567c9963dc4a7ab6e028f18be7ff1ba428ad39c53
