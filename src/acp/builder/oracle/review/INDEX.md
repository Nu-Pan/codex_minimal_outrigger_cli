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
- canonical な oracle review finding 列挙用 parameter builder を再公開する互換アダプター。関連所見を含む prompt の code fence を保護し、既存の呼び出し元を canonical 実装へ移行するまでの入口となる。

## Read this when
- oracle review finding の列挙 parameter builder の既存呼び出し元や互換性を確認するとき
- 関連所見を prompt に埋め込む際の code fence 保護処理を確認するとき

## Do not read this when
- canonical な builder の仕様や本体実装を確認したいときは、oracle 側の実装を直接読む
- review finding の列挙以外の ACP builder や prompt fence 処理を調査するとき

## hash
- 8c135f902786c590b13d59c5748de7cb2a49b0a15c5375565c976e3b67931df5

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
- oracle review finding の canonical parameter builder を再公開する realization adapter。動的な所見リストを prompt に埋め込む際、コードブロックの fence を保護する。

## Read this when
- oracle review finding の agent call parameter を生成・再公開する実装を確認するとき。
- 所見リストの prompt 埋め込みやコードブロック fence 保護の挙動を確認するとき。

## Do not read this when
- canonical builder 自体の仕様や prompt 内容を確認したいときは、対応する oracle の実装・定義を直接読む。
- review finding と無関係な agent call builder や prompt fence 処理を調査するとき。

## hash
- e7eee39c1cc6da7a9c11626c164a5f34322d6814f43fce8aec86e8adc409b439

# `validate_finding_advocate.py`

## Summary
- レビュー所見が妥当である理由を列挙する canonical prompt builder の realization adapter。canonical parameter を再利用し、対象所見と既知理由を含む動的 prompt section を fence で保護する。レビュー処理から擁護理由列挙用 parameter を構築する入口である。

## Read this when
- 擁護理由列挙用 builder の realization 側の委譲や動的 prompt section 保護を確認するとき
- レビュー所見・既知理由の prompt 注入防止処理を追跡するとき

## Do not read this when
- canonical な prompt 内容、モデル設定、ファイルアクセス設定を確認するときは oracle 側の実装を読む
- 妥当ではない理由の列挙や所見判定の処理を確認するときは、それぞれの専用 builder を直接読む

## hash
- 565d65144153e071e455c57663ac03bba887173be798cfaaecca3d49fa03a52b

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
