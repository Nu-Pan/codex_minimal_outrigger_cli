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
- realization apply fork 用の launch_exec builder adapter。oracle 側の正本 builder を呼び出し、生成された agent call parameter の prompt 内にある raw oracle git diff のコードフェンスを保護して再公開する。

## Read this when
- realization apply fork の launch_exec builder の挙動、引数、prompt の diff フェンス保護、または oracle builder との adapter 境界を確認・変更するとき。

## Do not read this when
- apply fork 以外の builder を調査するとき。
- prompt fence 保護の共通処理自体を調査するときは、共通 prompt fence module を直接読む。
- 正本 builder の仕様や prompt 構成を確認するときは、対応する oracle file を直接読む。

## hash
- 473f716b1cb96a375e360999e60a8e757465dfd74b025119f58c276e84e379a6
