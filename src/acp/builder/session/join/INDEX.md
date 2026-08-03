# `__init__.py`

## Summary
- oracle.acp_builder.session.join 互換の package 初期化ファイル。既存の acp.builder.session.join.* import を維持するためだけに残る互換入口であり、実装本体は持たない。

## Read this when
- acp.builder.session.join 配下の import 互換性や公開面維持のために、この package が存在する理由を確認したいとき。
- oracle.acp_builder.session.join から realization 側への互換 package 配置を調べているとき。

## Do not read this when
- session join の具体的な処理内容や振る舞いを確認したいとき。
- 互換 import の利用箇所を探したいとき。
- realization 側と利用者向け公開面から参照がなくなったかを判断するために、実際の参照元を調査したいとき。

## hash
- 072255c777a758fe7fa412dab9c417d50fc420b5871fae782e550e97a8c1b483

# `conflict_resolution.py`

## Summary
- 互換 import 経路として、canonical な session join conflict resolution 実装を再公開する薄いアダプター。競合ファイル一覧を canonical parameter に渡し、生成済み prompt の conflict 対象ファイル節だけ fence 保護して返す。
- session join の競合解決 parameter を利用する既存 caller から canonical 実装へ移行するまでの暫定的な入口。

## Read this when
- `acp.builder.session.join.conflict_resolution` からの互換 import を調査・変更するとき
- 競合 path の prompt 埋め込みや code block fence 保護の挙動を確認するとき
- session join conflict resolution の canonical parameter と互換ラッパーの差分を確認するとき

## Do not read this when
- canonical な conflict resolution の仕様や本体実装を確認したいときは、oracle 側の canonical 実装を直接読む
- session join の競合解決以外の builder や prompt fence 処理を調査するとき
- 互換 import caller がなく、canonical path への移行完了後の構成だけを確認するとき

## hash
- df1c9fc7faf28466fa86b69c0bc45f518f61457d14fc616e0b9d9adb5664c105
