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
- oracle review finding enumeration の canonical builder を呼び出す互換 adapter。絶対 symlink の lexical path を prompt に保持し、既存呼び出し元が残る間の入口となる。全呼び出し元が canonical oracle path を直接利用した後は削除可能。

## Read this when
- oracle review finding enumeration の parameter builder の呼び出し元や移行状況を調査するとき
- symlink された oracle path が prompt にどう表示されるかを変更・確認するとき

## Do not read this when
- canonical な prompt 生成仕様や builder 本体を確認したいときは、oracle 側の canonical 実装を直接読む
- oracle review enumeration と無関係な adapter や CLI 機能を調査するとき

## hash
- db90ae9f2d7a42c57d3ee6bebd2f3863c01d8c422e9be775279f74a294e586ad

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
- Oracle の merge-finding parameter builder を呼び出し、生成 prompt に含まれる既知の oracle-root placeholder typo だけを補正する realization implementation。補正 helper は oracle src の typo が解消されたら削除対象。

## Read this when
- merge-finding 用 agent call parameter の生成や prompt placeholder の typo 補正を変更・調査するとき
- oracle review builder の realization 側の互換処理と対応テストを確認するとき

## Do not read this when
- merge-finding builder の正本仕様や prompt 本文を変更するときは、まず対応する oracle src を直接読む
- 他の review builder や prompt 補正処理を調査するとき
- agent call parameter と無関係な CLI・永続化・実行処理を扱うとき

## hash
- 5a1fe8107957aa9004ce504b5b97afafa5c68a2f4e0659764e97026db43ba2de

# `validate_finding_advocate.py`

## Summary
- oracle review の finding advocate 用 AgentCallParameter を構築する。canonical builder の結果を基に、prompt 内に残る oracle root placeholder の既知 typo を一箇所だけ補正し、finding と既知理由は変更せず保持する。

## Read this when
- oracle review の finding advocate 用 parameter 生成や prompt 補正の実装を変更・検証するとき。
- canonical builder と、既知 typo の限定的な補正境界を確認するとき。

## Do not read this when
- 他の agent call parameter の生成規則だけを確認したいとき。
- prompt の正本仕様や canonical builder 本体を直接調査することが目的のときは、それぞれ対応する oracle file を読む。

## hash
- 104d25ced8a0f0a7333c53215facedb8016d1c2847de23f4c863e8efc5fabedf

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
