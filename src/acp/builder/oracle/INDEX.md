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
- `cmoc oracle edit` builder の realization adapter パッケージ。oracle edit 用 builder の実装入口と、TUI 起動時の AgentCallParameter 生成を扱う。

## Read this when
- `cmoc oracle edit` の builder adapter の責務や実装入口を確認するとき。
- oracle edit TUI の起動パラメータ生成や editor input 保存先の準備処理を確認・変更するとき。

## Do not read this when
- oracle edit の具体的な編集処理や CLI 全体の動作を確認するとき。
- 正本 builder の prompt 構築仕様や editor input ディレクトリのパス定義を確認するとき。

## hash
- 0848653168fbe8bcbe22d1c7b5ca6180c2887b94a61b532b657ca5ff92b6cbcc

# `review`

## Summary
- `cmoc oracle review` builder の realization adapter 群を収めるパッケージ。finding の enumeration、judgment、merge、advocate、challenger 向け parameter builder を canonical 実装へ委譲し、必要な互換 import や限定的な prompt typo 補正を提供する入口。

## Read this when
- `cmoc oracle review` builder の realization adapter の責務、canonical builder への委譲、互換 import、prompt の限定補正を変更・調査するとき。
- oracle review の finding enumeration、judgment、merge、advocate、challenger validation の realization 側の呼び出し経路や旧 caller の移行状況を確認するとき。

## Do not read this when
- oracle review の正本仕様や canonical builder 本体の実装を確認するとき。
- oracle review と無関係な builder、CLI、validation 処理を扱うとき。

## hash
- 513c63cf0edf6bebe3cabb1bbc749aa82aab34fa545ae50eabc161f943e6bbd6
