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
- `cmoc oracle review` builder の realization adapter package。oracle review の各 parameter builder への互換入口と、限定的な prompt 補正を提供する。

## Read this when
- `cmoc oracle review` builder の realization adapter の責務、canonical builder への委譲、既存 caller との互換性を確認するとき
- oracle review の prompt 補正や旧 import 経路の移行状況を調査するとき

## Do not read this when
- oracle review の正本仕様や canonical builder 本体を確認するとき
- builder 以外の CLI 実装や oracle review と無関係な処理を調査するとき

## hash
- b8ed1c1626b03f415e22503a796214f8f91df23cc6fbec613d4659ad45a1093c
