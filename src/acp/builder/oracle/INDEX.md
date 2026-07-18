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
- `cmoc oracle review` builder の realization adapter 群。canonical な oracle review builder への委譲、既存 import caller との互換性維持、限定的な prompt typo 補正を扱う。各ファイルは finding enumeration・judgment・merge・advocate・challenger validation の個別入口となる。

## Read this when
- `cmoc oracle review` builder の realization adapter 全体の責務や、既存 caller から canonical 実装への移行状況を確認するとき
- oracle review の各 finding 処理における互換 import、委譲経路、限定的な prompt 補正を調査するとき

## Do not read this when
- canonical な oracle review の正本仕様や builder 本体の実装を確認するとき
- builder 以外の CLI 実装、永続化、実行処理を調査するとき
- 特定の adapter の詳細だけを確認する場合は、対象の個別ファイルを直接読む

## hash
- ec47f1e8454013376ba50df7a47eeed780fae79bdb70aed929b1704cb3690be3
