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
- `cmoc oracle investigation` 用 builder adapter パッケージの入口であり、oracle investigation 向け builder 機能へ進む際の参照先です。
- oracle investigation の正本 builder 関数を互換 import 経路として公開し、既存の `acp.builder.oracle.investigation.launch_tui` 利用箇所から正本実装へ接続します。oracle.* への移行完了後は削除対象です。

## Read this when
- oracle investigation 用 builder adapter の構成や入口を確認するとき。
- 該当パッケージ内の下位実装へ進む前に責務を確認するとき。
- 既存の `acp.builder.oracle.investigation.launch_tui` import 経路の互換性や、oracle investigation の `launch_tui` builder への移行状況を確認するとき。

## Do not read this when
- builder adapter の具体的な実装詳細を確認したいときは、下位実装を直接読む。
- 正本の builder 実装や oracle investigation の仕様・挙動を確認したいときは、oracle 側の `launch_tui` 実装を直接読む。
- oracle investigation 以外の builder や ACP 実装を調べるとき。
- `acp.builder.oracle.investigation.launch_tui` の互換性を調べる必要がない一般的な oracle investigation の調査をするとき。

## hash
- ee2b233b3a0171319a5425e67d6d5c88e7ef3c3f306281f8eba3a8a0996a918c

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
