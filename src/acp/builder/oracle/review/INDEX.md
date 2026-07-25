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
- Oracle review finding の判定用 parameter builder を再公開する互換アダプター。canonical builder の結果に対し、所見・賛成理由・反対理由へ動的に挿入されるコードフェンスを保護する。既存 caller の移行期間に限って使用され、canonical 実装への移行完了後は削除対象。

## Read this when
- oracle review finding の判定用 parameter builder の既存 caller や互換経路を調査・変更するとき
- 所見や賛成・反対理由を prompt に埋め込む際のコードフェンス保護を確認するとき

## Do not read this when
- canonical な oracle review judge_finding 実装を直接利用する caller の処理だけを確認するとき
- oracle review finding の判定や prompt 構築と無関係な処理を調査するとき

## hash
- 784c17b9ecc63fc63170fcc07a3635a72e6d6f350b363dc32d920cce51065c12

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
- Oracle review の finding advocate 用 agent call parameter を構築する実装。canonical parameter を生成した後、oracle-root の typo を補正し、finding と既知理由をコードフェンスで保護した prompt に置換する。内部 helper は typo 補正を一箇所に限定し、動的入力を byte-for-byte で保持する。

## Read this when
- oracle review の finding advocate 用 prompt 生成・補正・コードフェンス保護の挙動を変更または確認するとき。

## Do not read this when
- 他の oracle review 以外の agent call parameter を扱うとき。canonical prompt の正本仕様や typo の根拠を確認する場合は、参照されている oracle src・oracle doc を直接読む。

## hash
- 251be73f2e71e07f527febb373e8176c16e6a4126240aef74937fefd255209d6

# `validate_finding_challenger.py`

## Summary
- oracle review の finding challenger 検証用 parameter builder を再公開する互換アダプター。canonical oracle 実装から parameter を取得し、動的に埋め込む finding・既知理由のコードフェンスを保護する。caller が canonical oracle path を直接使うまでの移行入口。

## Read this when
- oracle review の finding challenger 検証用 parameter builder の caller や import 互換性を調べるとき
- finding、既知の妥当であるとする理由、既知の妥当ではないとする理由の prompt 埋め込み時の fence 保護を変更・確認するとき

## Do not read this when
- canonical な parameter 生成仕様や prompt 本文を確認したいときは、直接 oracle 側の実装を読む
- oracle review の finding challenger 以外の builder や prompt fence 処理を調べるとき

## hash
- 75579da2d2d72c9fa2b30669c1547b4d81cf253260db82bdcce81f7a61ad47fe
