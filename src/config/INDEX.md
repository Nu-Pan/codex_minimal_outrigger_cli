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
- oracle 側にある cmoc 設定定義を realization 側の既存参照名で再公開する互換用モジュール。設定定義そのものは複製せず、公開面や realization 側から旧来の参照が残っている間だけ橋渡しする。

## Read this when
- realization 側で cmoc の設定定義を参照する import 経路を調べるとき。
- 設定定義の正本を複製せずに既存参照を維持している理由を確認するとき。
- この互換用の再公開を削除できる条件を確認するとき。

## Do not read this when
- 設定項目の内容や型など、設定定義そのものを確認したいとき。
- oracle 側の正本仕様断片として設定を変更・確認したいとき。
- 新しい設定項目や公開面を追加する設計判断をしたいとき。

## hash
- 96661a3576725931d1a746eafcb745029a6db9b11df02841355452ad56759809
