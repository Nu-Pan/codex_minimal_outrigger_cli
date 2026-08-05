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
- `cmoc oracle investigation` 用 builder adapter パッケージの入口。oracle investigation 向け builder 機能へ進む際の参照先。
- oracle investigation の正本 builder を呼び出す realization adapter。エディタ入力用ディレクトリを準備し、時刻情報とユーザー指示を正本 builder に渡して AgentCallParameter を生成する。

## Read this when
- oracle investigation 用 builder adapter の構成や入口を確認するとき
- 該当パッケージ内の下位実装へ進む前に責務を確認するとき
- oracle investigation の launch TUI 用パラメータ生成、完全な prompt の保存先準備、正本 builder への委譲経路を確認するとき

## Do not read this when
- oracle 側の launch TUI builder の仕様や prompt 構築詳細を確認したいとき
- launch TUI 以外の builder や、エディタ入力ディレクトリの一般的な実装だけを調べるとき
- oracle investigation 以外の builder や ACP 実装を調べるとき

## hash
- 80cc28d0067aa6d4edfe448b81bdeec6cbd2b358695b1bf3958ae53924fc5e03

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
