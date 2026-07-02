# `__init__.py`

## Summary
- oracle.acp_builder.review と互換のパッケージ入口を示す。実体的な実装や挙動ではなく、互換用パッケージとしての位置づけだけを持つ。

## Read this when
- oracle.acp_builder.review 互換の import 経路やパッケージ存在を確認したいとき。
- review 配下の互換パッケージ入口がどの責務を持つかを確認したいとき。

## Do not read this when
- review 機能の具体的な処理内容や制御ロジックを調べたいとき。
- 互換 package ではなく実装本体やテスト対象の詳細を確認したいとき。

## hash
- adf6124f1c3a49a136159186b6a58b39f4321e0113527b60e85d8b1e3205484e

# `oracle`

## Summary
- review oracle builder 配下に生成された互換 package 群で、旧 import 経路を canonical 実装へつなぐ薄い再 export と、一部 prompt placeholder 補正用 builder を収める。
- review finding の列挙・判定・validation・merge finding review 用 agent call parameter 生成について、旧経路維持や一時的な `<oracle_root>` 表記補正の所在を調べる入口になる。

## Read this when
- review oracle builder の旧 import 経路がまだ必要か、canonical 実装への移行や互換 shim の削除条件を確認したいとき。
- oracle merge finding review や oracle finding advocate review の agent call parameter 生成で、oracle 側 builder の出力を使いながら prompt 内 placeholder 表記だけを補正する経路を確認したいとき。
- build 配下に生成された review oracle 互換 package が、実体的な処理ではなく import 互換性や限定的な補正だけを担うことを確認したいとき。

## Do not read this when
- review finding の列挙・判定・validation の仕様や実装ロジックそのものを確認したいときは、canonical 実装を直接読む。
- merge finding や finding advocate の正本 prompt、正本仕様断片、共通 agent call parameter 構造を確認したいときは、元の oracle 側定義や共通 builder を読む。
- oracle merge finding review や finding advocate review 以外の review 種別、または placeholder 補正と関係しない builder 実装を調べたいとき。

## hash
- bdc8d9e8318ffd0285288c89c13fc164d02b10bf0bf5beefe163e551bab3e9d5
