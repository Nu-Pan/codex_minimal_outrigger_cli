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
- Oracle review finding enumeration の互換アダプター。canonical builder に処理を委譲しつつ、動的な関連所見のコードフェンス保護と symlink 使用時の oracle path 表現補正を行う。呼び出し元が canonical path を直接利用するまでの移行用入口。

## Read this when
- oracle review finding enumeration の parameter builder の呼び出し元や移行状況を確認するとき
- 関連所見を含む prompt の fence 保護や symlink oracle path の扱いを変更するとき

## Do not read this when
- canonical な enumeration builder の仕様・実装を確認したいとき
- oracle review 以外の builder や prompt fence 処理を調べるとき

## hash
- e9e8d01912d26c8fe23a51190eb6dd7c74cf45c85893c1f7df3b7e1663fe5b9c

# `judge_finding.py`

## Summary
- oracle review の finding judgment 用 canonical builder を再公開する互換 adapter。動的な所見・賛成理由・反対理由を prompt fence で保護し、既存 caller が canonical oracle path へ移行するまでの入口を提供する。

## Read this when
- oracle review の finding judgment parameter builder の caller や互換 import を調査・変更するとき。
- 動的レビュー内容を prompt 内の所定セクションとして安全に埋め込む処理を確認するとき。

## Do not read this when
- canonical な builder の仕様や prompt 本文を確認したいときは、参照先の oracle 実装を直接読む。
- oracle review や finding judgment と無関係な builder、prompt、CLI 処理を調査するとき。

## hash
- 72e2700ef3f0572acede306cd6aa250cc47eb95a7b8536ec631dda68ae9321a1

# `merge_finding.py`

## Summary
- oracle review finding merge 用の realization adapter。canonical builder を再利用し、動的な所見リストを含む prompt 内のコードフェンスを保護して、レビュー所見統合用の AgentCallParameter を生成する。

## Read this when
- oracle review finding merge の parameter 生成処理を変更・確認するとき
- 動的な所見リストの prompt 埋め込みやコードフェンス保護の挙動を確認するとき

## Do not read this when
- canonical builder の仕様や prompt 本文を確認したいときは、参照先の oracle 実装を直接読む
- レビュー所見統合以外の builder や prompt fence 処理を調査するとき

## hash
- 6d22b428055bda107099448ee4e32f4f9d8fb99eee14fdd81085fbfd16b9d294

# `validate_finding_advocate.py`

## Summary
- 妥当性検証用の agent call parameter を構築するモジュール。canonical parameter を生成した後、oracle root placeholder の typo を限定的に補正し、対象所見と既知の賛成・反対理由を prompt fence で保護する。

## Read this when
- oracle review における finding の妥当性検証 prompt の生成・修正・テストを確認するとき
- 動的な finding や既知理由を保持した prompt parameter の組み立てを変更するとき

## Do not read this when
- canonical な妥当性検証 parameter の正本定義そのものを確認するとき
- prompt fence の共通実装を確認するときは、まず共通の prompt fence module を読む

## hash
- 8968304748accf6e357b983ac04140a9829210866d5827f9b28560b53128b9f0

# `validate_finding_challenger.py`

## Summary
- oracle review の finding challenger 検証用パラメータ生成を再公開する互換 adapter。canonical oracle 実装の builder を呼び出し、finding・既知理由の prompt section を fence 保護して返す。

## Read this when
- oracle review の finding challenger 検証処理や、その agent call parameter の生成・prompt 保護を変更するとき。
- canonical 実装への移行状況や、旧 adapter caller の互換維持を確認するとき。

## Do not read this when
- canonical な oracle review builder 自体の仕様・実装を変更する作業。
- prompt fence の共通処理だけを調査・変更する作業。

## hash
- b937c8eec287e4aeac088b29ae3f6cf090fa8829e45a257dfe46b37cdc3deb33
