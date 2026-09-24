# `__init__.py`

## Summary
- `realization apply fork` 向け builder adapter の責務を示す docstring。パッケージの役割を確認する入口であり、個別の処理は説明しない。

## Read this when
- `realization apply fork` 用 adapter パッケージの役割や責務の境界を確認するとき。

## Do not read this when
- 起動パラメーター builder の処理や互換再公開を調べるときは、その個別 builder の定義へ進む。
- apply 全体に共通する builder adapter の役割だけを調べるときは、apply パッケージの説明から確認する。

## hash
- 8ac1b4ff7590d29ce880b9d540f7fcace726de341416b79123260b174c415a65

# `launch_exec.py`

## Summary
- 既存の builder import 経路を保つため、正本の builder 関数を再公開する互換 adapter。builder の処理自体はここでは定義しない。

## Read this when
- この adapter 経由の import 互換性を確認するときや、参照がなくなり削除できるか判断するとき。

## Do not read this when
- prompt や起動パラメータの構築内容を調べるときは、正本 builder を直接読む。
- apply fork コマンドの処理順や起動フローを調べるときは、呼び出し側を読む。

## hash
- 383f0d2aed0b8d5c4573772e81b09790be3d587e72a832d0610df1d55c42340c
