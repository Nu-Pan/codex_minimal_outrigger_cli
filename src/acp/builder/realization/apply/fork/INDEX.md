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
- realization apply fork の launch_exec 用 builder を再公開する adapter。oracle 側の builder を利用し、raw git diff に含まれる backtick が外側の Markdown fence を閉じないよう prompt の diff セクションだけを補正する。

## Read this when
- realization apply fork の launch_exec parameter builder の公開 API、prompt 生成、または raw git diff の Markdown fence 保護を確認・変更するとき。

## Do not read this when
- oracle 側の正本 builder の仕様や prompt 構成自体を確認したいときは、対応する oracle source を直接読む。fork 以外の apply 処理や一般的な builder の責務を調べる場合。

## hash
- f0a7de5b661960c37f2e8c724b5c8f6839c617a762a1e0d0feddce78ff10c2e7
