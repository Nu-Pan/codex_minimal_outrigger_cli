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
- `cmoc oracle edit` の realization adapter package。正本の oracle edit TUI builder を呼び出す入口を提供し、起動前に完全 prompt の保存先となる editor input log directory を準備する。配下の launch TUI adapter の責務確認に進むためのディレクトリ単位の入口。

## Read this when
- `cmoc oracle edit` の builder adapter の責務や実装入口を確認するとき
- oracle edit の TUI 起動前に必要な realization 側の directory 準備と正本 builder の接続を確認するとき

## Do not read this when
- oracle edit の具体的な prompt 内容や正本 builder の動作を確認するとき
- CLI 全体の動作や editor input log directory の管理だけを確認するとき

## hash
- 0c553033270441536df4aa0abdfb079f34b19c2586e7ac561d6a42953b1444b3

# `investigation`

## Summary
- oracle investigation 用 builder adapter のパッケージ入口。該当 builder adapter の構成を把握し、下位実装へ進む前の責務確認に使う。
- oracle investigation の launch TUI 呼び出し向け agent-call parameter を生成する realization adapter。正本 builder 呼び出し前の editor input log directory 作成と、builder 生成結果の受け渡しを扱う。

## Read this when
- oracle investigation 用 builder adapter の入口や構成を確認するとき
- oracle investigation の launch TUI 呼び出し用 parameter 生成処理を確認・変更するとき
- 正本 builder 呼び出し前に必要な runtime directory 準備の責務を確認するとき

## Do not read this when
- builder adapter の具体的な prompt 構築仕様を確認したいときは、正本 builder を直接読む
- editor input log のパス解決や runtime path の詳細だけを確認したいときは、対応する path/runtime 定義を直接読む
- oracle investigation 以外の builder や ACP 実装を調べるとき

## hash
- ccc6abeb232b6f0b9fcba8f2c56075a4e91e60b964242e9d66f0e8a4184d43c0

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
