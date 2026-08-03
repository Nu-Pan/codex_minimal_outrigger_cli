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
- `cmoc oracle edit` builder の realization adapter パッケージ。oracle edit 用 builder 実装への入口と、TUI 起動パラメータ生成を扱う。
- 空のディレクトリで、現時点では案内対象となる実装・テスト・補助ファイルを含まない。
- oracle edit 用 TUI 起動パラメータを生成し、リポジトリ実パスの解決、editor input directory の準備、oracle 側 builder の呼び出しを担う。

## Read this when
- `cmoc oracle edit` の builder adapter の責務や実装入口を確認するとき。
- このディレクトリにファイルが追加されたか確認するとき。
- oracle edit の TUI 起動パラメータ生成、editor input directory の準備、または realization 側から oracle 側 builder を呼び出す経路を確認・変更するとき。

## Do not read this when
- oracle edit の具体的な編集処理や CLI 全体の動作を確認したいとき。対象の実装ファイルや上位の CLI 関連ファイルを直接読む。
- oracle 側の TUI builder の prompt 内容や本体ロジックを直接確認するとき。
- oracle edit や TUI 起動パラメータと無関係な builder、パス解決、実行時処理を調べるとき。

## hash
- 8f3a1408430c389329fe8f6468d5594d329af74b48c018f93d6368153e193bf1

# `investigation`

## Summary
- `cmoc oracle investigation` 用 builder adapter パッケージの入口。oracle investigation 向け builder 機能への参照先。
- oracle investigation 用の完全な AgentCallParameter を正本 builder に委譲する realization adapter。実行前のリポジトリ解決と editor input 用ディレクトリ準備を担い、investigation launch TUI のパラメータ生成処理への入口となる。

## Read this when
- oracle investigation 用 builder adapter の構成や入口を確認するとき
- 該当パッケージ内の下位実装へ進む前に責務を確認するとき
- oracle investigation の launch TUI 用 builder や AgentCallParameter 生成の呼び出し経路を確認するとき
- editor input ディレクトリの準備を含む investigation 起動処理を変更・調査するとき

## Do not read this when
- builder adapter の具体的な実装詳細を確認したいときは、パッケージ内の実装ファイルを直接読む
- 正本 builder の prompt 内容や investigation 起動仕様そのものを確認したいとき
- investigation 以外の builder、TUI 実装、または共通パス解決処理だけを調査するとき

## hash
- ebdb0eded51c4843b36edad877803b1b0e31f6fcff21c28327631abb2cecfc39

# `review`

## Summary
- `cmoc oracle review` builder の realization adapter 群をまとめたパッケージ。finding 列挙・判定・統合・妥当性検証の各 parameter builder を canonical oracle 実装へ委譲し、動的なレビュー内容の prompt fence 保護や互換 import の入口を提供する。

## Read this when
- `cmoc oracle review` builder の realization adapter の責務、利用可能な finding 関連 builder、canonical 実装への委譲関係を確認するとき。
- finding や既知理由などの動的 prompt section の保護処理、symlink 経由の oracle path 補正、旧 caller との互換性を調査するとき。

## Do not read this when
- oracle review の正本仕様、canonical builder の仕様や prompt 本文を確認するときは、参照先の oracle 実装を直接読む。
- builder 以外の CLI 実装や、oracle review と無関係な prompt・path 処理を調査するとき。

## hash
- 28cbe085f0a525ab4d7e9ffc344160bb67fbbffd47c4d351e4c106472ee425f9
