# `__init__.py`

## Summary
- oracle src 側の設定実装を正本に保ったまま、既存の `config.*` import を成立させるための互換入口。
- realization 側と利用者向け公開面に残る旧来の `config.*` 参照を受けるためだけに存在し、正本仕様や設定ロジック本体は担わない。

## Read this when
- `config.*` import がどこで受け止められているか、またはその互換入口を残す理由を確認したいとき。
- 旧来の `config.*` 参照を削除・置換する作業で、この互換入口を削除できる条件を確認したいとき。
- oracle src 側の設定実装を正本にしたまま realization 側で互換 import を維持している境界を確認したいとき。

## Do not read this when
- 設定値の定義、読み込み、検証などの本体挙動を確認したいとき。
- oracle src 側の正本となる設定実装そのものを確認したいとき。
- 新しい設定項目や公開面を追加する作業で、互換 import の残存理由が論点ではないとき。

## hash
- 991b20cfe981e7da47b9fb4f45010bb926ac60ed1f2f88ce102a246827f26742

# `cmoc_config.py`

## Summary
- oracle 側で定義された設定型を realization 側の既存公開参照として再公開する互換用モジュール。設定定義を複製せず、正本側を参照し続けるための入口であり、公開参照が残る間だけ維持される。

## Read this when
- realization 側から設定型を import する既存公開参照の維持、削除可否、参照先の責務境界を確認したいとき。
- 設定定義を realization 側へ複製せず oracle 側の定義へ委譲している理由を確認したいとき。

## Do not read this when
- 設定項目そのものの定義、型の内容、正本仕様としての設定構造を確認したいとき。
- 設定値の読み込み、検証、適用処理など、再公開以外の実装挙動を調べたいとき。

## hash
- 2b9ccce6bffa9324937357d4bd74fe2d498068845f516b5acd864622aa803700
