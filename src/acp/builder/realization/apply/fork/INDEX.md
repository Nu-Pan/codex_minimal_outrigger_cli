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
- realization apply fork 用の正本 builder を再公開する adapter。正本 builder が生成した agent call parameter の prompt に含まれる raw oracle diff のコードフェンスを保護する。

## Read this when
- realization apply fork の launch_exec builder の呼び出し元や prompt 加工を確認するとき
- raw oracle diff のコードフェンス保護の挙動を変更・検証するとき

## Do not read this when
- 正本 builder 自体の仕様や prompt 内容を変更するときは、対応する oracle source を直接読む
- apply fork 以外の builder や一般的な prompt fence 処理を調べるとき

## hash
- ad8b6414faf5db7a582c40bdb0497e77e238bd5567989f66edc9483a8608a9fe
