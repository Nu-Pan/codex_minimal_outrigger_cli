# `__init__.py`

## Summary
- oracle command builder の realization package。oracle command builder 関連のパッケージ入口として機能する。

## Read this when
- oracle command builder の realization package の責務や構成を確認するとき。

## Do not read this when
- oracle command builder 以外の処理を確認するとき。

## hash
- 04f29448a0f9d675976d8cda22279a162a5e8e89a169554a4926766bf0f88d6b

# `edit`

## Summary
- `cmoc oracle edit` builder 用の realization adapter package。oracle edit 向け builder 実装へ進むためのパッケージ入口。

## Read this when
- `cmoc oracle edit` の builder adapter の責務や実装入口を確認するとき。

## Do not read this when
- oracle edit の具体的な編集処理や CLI 全体の挙動を確認するときは、実装ファイルまたは上位の CLI 関連ファイルを直接読む。

## hash
- b1383fbbd6c0d1e8620975620e380ef789da565e4710f09f8f46c23740359e26

# `investigation`

## Summary
- oracle investigation 用 builder adapter パッケージの入口。配下の builder adapter 構成と責務を確認し、下位実装へ進むための参照先。
- oracle investigation の起動 TUI パラメータ builder を互換 import 経路として再公開するファイル。正本実装を確認せずに、既存経路で公開対象を参照したい場合の入口。

## Read this when
- oracle investigation 用 builder adapter の構成や入口を確認するとき
- 該当パッケージ内の下位実装へ進む前に責務を確認するとき
- oracle investigation の起動 TUI パラメータ builder を既存の互換 import 経路から参照するとき
- 互換経路が再公開する対象や範囲を確認するとき

## Do not read this when
- builder adapter の具体的な実装詳細を確認したいとき
- oracle investigation 以外の builder や ACP 実装を調べるとき
- builder の処理内容や investigation 起動パラメータの仕様を確認・変更するとき
- 正本実装を確認する必要があるときは、oracle investigation 側の正本 builder を直接読む

## hash
- 50f8760e1258bc55a46aeda2cd8f311f5334e0e84ce888ac6f9c5df7cb81dc55

# `review`

## Summary
- `cmoc oracle review` builder の realization adapter 群を収容するパッケージ。canonical 実装への互換 import 経路を提供し、finding の列挙・判定・merge・advocate／challenger 検証に関する関連実装へ進むための入口。

## Read this when
- `cmoc oracle review` builder における realization adapter の責務や、旧 import 経路から canonical 実装へ委譲される構成を確認するとき
- oracle review の finding 処理について、互換 import の維持・利用箇所や canonical 実装への移行関係を調べるとき

## Do not read this when
- oracle review の正本仕様や、builder 以外の CLI 実装を確認するとき
- finding 列挙・判定・merge・検証の具体的な処理内容や入出力仕様を確認するとき。互換経路ではなく canonical 実装を直接読む

## hash
- f9b763b21f8eb79c9de8bc550c70a9cf8de681e79ccc483de70d283621060a03
