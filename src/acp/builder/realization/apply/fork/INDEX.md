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
- realization apply fork の launch_exec に関する互換入口。正本 builder を再公開し、apply fork の launch_exec パラメータ生成へ到達するための対象。

## Read this when
- apply fork の launch_exec パラメータ生成を利用・確認するとき
- 互換入口から正本 builder への委譲関係を確認するとき

## Do not read this when
- 正本 builder の実装内容や挙動を確認したいときは、対応する oracle file を直接読む
- apply fork 以外の realization apply や、launch_exec パラメータ生成と無関係な処理を扱うとき

## hash
- 63d3b490194bc1558f63f4dddda55776611d4ee7a3cdcde632c9e57d9df7ca80
