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
- Oracle review の finding 列挙用 parameter builder を再公開する互換アダプター。canonical oracle 実装を利用しつつ、symlink 経由の oracle path 表記を補正し、関連所見内のコードフェンスを保護する。

## Read this when
- Oracle review の finding 列挙処理や、その AgentCallParameter の生成・再公開経路を変更するとき。
- canonical builder と realization adapter の path 変換、symlink 対応、関連所見の prompt fence 保護を確認するとき。

## Do not read this when
- canonical な oracle 側の finding 列挙仕様・実装自体を変更または確認するときは、参照先の oracle 実装を直接読む。
- Oracle review の finding 列挙や parameter 生成に関係しない処理を変更するとき。

## hash
- b1e070698eb70c3565c628cbe6649bd4ffaab074bd0c32bf98ec7b7ff477c2e8

# `judge_finding.py`

## Summary
- Oracle review finding の canonical builder を呼び出す realization adapter。動的な所見・賛成理由・反対理由を含む prompt のコードフェンスを保護し、既存 caller 向けに parameter builder を再公開する。canonical 実装への移行完了後は削除対象。

## Read this when
- oracle review finding の parameter 生成や prompt fence 保護、既存 caller との互換維持を変更・調査するとき。

## Do not read this when
- canonical な oracle review judge finding の仕様や実装自体を確認したいときは、直接 canonical oracle path を読む。prompt fence 共通処理だけを調べるときは prompt_fence の実装を読む。

## hash
- c597d7bb4d8910b78bf5dd5e1bd7de26f18f2b9df8528870b95bb486fa788737

# `merge_finding.py`

## Summary
- oracle review finding merge の realization adapter。canonical builder を再利用し、動的な所見リストを含む prompt のコードフェンスを保護する。

## Read this when
- oracle review finding merge の realization 側 adapter の挙動や prompt fence 保護を確認・変更するとき。

## Do not read this when
- canonical builder の仕様や prompt 本文を確認するときは、oracle 側の実装を直接読む。

## hash
- f9019a97d3570e7fcee15ac9fae3d941bbbafcff3ff7f3b325e12a59901f596c

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
