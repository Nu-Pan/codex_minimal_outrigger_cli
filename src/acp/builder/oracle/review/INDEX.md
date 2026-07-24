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
- oracle review finding enumeration の canonical builder を呼び出す互換 adapter。関連所見セクション内の動的内容を code fence から保護し、既存の呼び出し元へ parameter builder を再公開する。全呼び出し元が canonical oracle path を直接利用した後は削除対象となる。

## Read this when
- oracle review finding enumeration の agent call parameter 生成や、関連所見の prompt fence 保護を変更・調査するとき
- canonical builder への移行状況や、この adapter の削除可否を確認するとき

## Do not read this when
- oracle review 以外の builder や、canonical implementation 自体の仕様・挙動を直接調査するとき
- prompt fence 保護と無関係な agent call parameter の処理を調べるとき

## hash
- 85f4eb71e0ff1cedaa438f279d41716ff6c791f6a9cdf066c8b4deb30e47d460

# `judge_finding.py`

## Summary
- Oracle review finding の判定用 parameter builder を再公開する互換アダプター。canonical 実装へ委譲した後、動的に埋め込まれる3つの所見関連セクション内のコードフェンスを保護して prompt を返す。

## Read this when
- `acp.builder.oracle.review.judge_finding` からの既存 import や互換経路を調査・変更するとき
- oracle review finding judgment の prompt 生成やコードフェンス保護の挙動を確認するとき

## Do not read this when
- canonical な oracle review judge_finding の仕様・実装を確認したいときは、oracle 側の canonical 実装を直接読む
- oracle review finding と無関係な builder や prompt 処理を変更するとき

## hash
- 894edf7d0ae7a78f22c44fc496e1ea826ead283eec9dfd7d966d41dd7c209468

# `merge_finding.py`

## Summary
- oracle review finding merge の canonical builder を再利用し、動的な所見リストを含む prompt のコードブロック fence を保護する realization adapter。レビュー所見の merge 用 AgentCallParameter を構築する実装への入口。

## Read this when
- oracle review finding merge 用の AgentCallParameter 構築処理を変更・調査するとき
- 所見リストの prompt 埋め込みやコードブロック fence 保護の挙動を確認するとき

## Do not read this when
- canonical な parameter 構築仕様そのものを確認したいときは oracle 側の merge_finding 実装を直接読む
- レビュー所見の merge 以外の prompt builder や一般的な fence 処理を調査するとき

## hash
- 8c8a1b1f38263f5ae1fd2ed78521b269040ea9288c683adb3fa6068aa627df82

# `validate_finding_advocate.py`

## Summary
- oracle の canonical parameter を生成した後、prompt 内の oracle root typo を補正し、動的入力を含む3つのセクションを text コードフェンスで保護する builder。oracle src の意図に基づく最小限の補正と入力保持を担う。

## Read this when
- oracle review の validate finding advocate 用 AgentCallParameter の生成・補正処理を変更または調査するとき
- 対象所見や既知理由の prompt 埋め込み、コードフェンス保護、oracle root typo 補正の挙動を確認するとき

## Do not read this when
- canonical parameter の正本定義そのものを確認したいときは、参照先の oracle src を直接読む
- validate finding advocate と無関係な prompt builder やレビュー処理を調査するとき

## hash
- 3c505361f5ca3e8afc942827e46a265a413e244063e4a5180ad08345a0ee138e

# `validate_finding_challenger.py`

## Summary
- oracle review の finding challenger 検証用 canonical builder を再公開する互換アダプター。既存 caller 向けの parameter 生成を委譲し、動的な所見・既知理由をコードフェンスで保護した prompt を返す。canonical 実装へ移行するまでの入口。

## Read this when
- oracle review の finding challenger 検証 parameter builder の既存 caller 互換性や prompt のコードフェンス保護を確認・変更するとき。

## Do not read this when
- canonical な parameter 仕様や prompt 本体を確認したいときは、oracle 側の canonical builder を直接読む。
- oracle review 以外の builder や、一般的な prompt fence 処理を調査するとき。

## hash
- a8f05b5b4b0c6c6f8020479bd56ed87627c466ae631a28d2a855c7001f0bcb0d
