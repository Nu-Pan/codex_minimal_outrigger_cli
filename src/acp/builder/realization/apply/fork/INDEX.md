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
- 日本語の技術文書向け INDEX.md エントリー生成のため、対象ファイルの互換入口としての責務と、正本実装へ進む入口条件を整理します。

## Read this when
- 既存の acp.builder.realization.apply.fork.launch_exec 参照を維持する互換入口の役割を確認するとき
- この入口が再公開する launch_exec パラメータ builder の正本実装を確認するとき

## Do not read this when
- 互換参照の有無を確認するだけで、正本 builder の実装内容を調べる必要がないとき
- realization 側の実装や利用者向け公開面から旧参照を削除する条件を検討するとき

## hash
- 383f0d2aed0b8d5c4573772e81b09790be3d587e72a832d0610df1d55c42340c
