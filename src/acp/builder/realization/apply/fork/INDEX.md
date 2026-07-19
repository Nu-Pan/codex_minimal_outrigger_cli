# `__init__.py`

## Summary
- `cmoc realization apply fork` 用の builder adapter を示す初期化モジュール。fork 適用処理の builder 接続点を確認する際の入口となる。

## Read this when
- `cmoc realization apply fork` の builder adapter の責務や配置を確認するとき。

## Do not read this when
- fork 適用処理そのものの実装詳細を調査するとき。
- `cmoc realization apply fork` 以外の builder adapter を調査するとき。

## hash
- 8ac1b4ff7590d29ce880b9d540f7fcace726de341416b79123260b174c415a65

# `launch_exec.py`

## Summary
- realization apply fork 用の launch_exec builder を oracle 側の正本実装から再公開する薄い adapter。呼び出し側がこのモジュール経由で builder を利用するための入口を提供する。

## Read this when
- realization apply fork の launch_exec builder の import 入口や公開 API を確認するとき。

## Do not read this when
- builder の具体的な構築ロジックや仕様を確認するときは、再公開元の oracle 実装を直接読む。

## hash
- 9061ec63223d4ab9de66f345dac0bd26b409eae976b89ac27f8c73e1086ed548
