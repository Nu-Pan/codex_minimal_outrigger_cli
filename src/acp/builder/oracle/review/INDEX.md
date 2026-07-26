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
- oracle review finding enumeration の canonical builder を再公開する互換 adapter。動的な関連所見を prompt fence で保護し、symlink 使用時は oracle path の lexical entry を prompt に保持する。

## Read this when
- `build_oracle_review_enumerate_finding_parameter` の呼び出し元、互換維持、または削除条件を調査するとき
- oracle path の symlink 処理や関連所見の prompt 埋め込みを変更・検証するとき

## Do not read this when
- canonical な finding enumeration builder の仕様や実装を確認するときは、oracle 側の canonical path を直接読む
- oracle review finding enumeration と無関係な builder や prompt 処理を調査するとき

## hash
- 7ea11d71d1bce267516b7c1f950207696e42e0da9c58619216534d5e3da457ed

# `judge_finding.py`

## Summary
- Oracle review の finding judgment 用 parameter builder を再公開する互換 adapter。canonical 実装を呼び出した後、動的な所見・賛成理由・反対理由の各 prompt section を保護する。

## Read this when
- `acp.builder.oracle.review.judge_finding` の caller や互換 import 経路を変更・確認するとき。
- review finding judgment の prompt fence 保護処理を調査するとき。

## Do not read this when
- canonical な parameter 生成仕様や本体実装を確認したいときは、oracle 側の `oracle/acp_builder/oracle/review/judge_finding.py` を直接読む。
- review finding judgment と無関係な builder や prompt 処理を調査するとき。

## hash
- 908f319b7b5984945ebed453677adbbfa0e30322ce9fab81ac17f2c3eb8f5893

# `merge_finding.py`

## Summary
- oracle review finding merge の canonical builder を呼び出す realization adapter。動的な所見リストを含む prompt の code fence を保護し、AgentCallParameter を再公開する。

## Read this when
- oracle review finding merge の agent call parameter 生成や、所見リストの prompt 埋め込み・code fence 保護を変更するとき。

## Do not read this when
- canonical な prompt 定義や parameter 生成ロジック自体を変更するときは、まず oracle 側の canonical 実装を読む。
- review finding merge 以外の agent call builder や prompt fence 処理を変更するとき。

## hash
- 5ec78a1a67d3a9a6ac0d791531475b252b54bcd50893b5464bd2ea003fc3f783

# `validate_finding_advocate.py`

## Summary
- Oracle review の妥当性検証エージェント向けパラメータを構築する補正層。canonical parameter の prompt に含まれる oracle root の typo を限定的に修正し、対象所見と既知理由の動的入力を fence で保護する。

## Read this when
- oracle review の finding advocate 用エージェント呼び出しパラメータの生成・補正ロジックを変更または検証するとき。
- 動的な所見・妥当性理由を prompt に埋め込む際の保護範囲や、canonical prompt の typo 補正を確認するとき。

## Do not read this when
- canonical な oracle review prompt の仕様や内容を確認したいときは、参照先の oracle builder を直接読む。
- prompt fence の共通実装を変更・調査するときは、共通の prompt fence 実装を直接読む。

## hash
- e79ab39cbc11ccc4d09dddd79ee274ebcfd57fdd0b586f5e8f052bda0f43dcfd

# `validate_finding_challenger.py`

## Summary
- oracle review の finding challenger 検証用 canonical builder を再公開する互換 adapter。canonical parameter に動的な所見・既知理由を埋め込み、review section の fence を保護する。旧 import caller がなくなるまでの移行入口。

## Read this when
- oracle review の finding challenger 検証用 agent call parameter の生成や、旧 `acp.builder.oracle.review.validate_finding_challenger` import 互換性を変更・調査するとき。
- 動的な所見・妥当性理由の prompt section 保護処理を確認するとき。

## Do not read this when
- canonical な prompt 定義や builder 本体の仕様を確認したいときは、記載された oracle 側の canonical file を直接読む。
- oracle review と無関係な agent call parameter や prompt fence の変更を扱うとき。

## hash
- 327dbd9953060b5a205b5bfbe4f6f32fc0b7ff6d7d85aaa8d4fa0fc81f6c5dda
