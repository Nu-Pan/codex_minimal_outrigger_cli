# `__init__.py`

## Summary
- realization workload サブコマンドのパッケージ入口。

## Read this when
- realization workload サブコマンドの実装や構成を確認するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。

## hash
- 45f2cdf62d9edd181a1f1cc14734db2757e556059630746b1486c1bd5d1101b4

# `apply`

## Summary
- realization の apply workload を扱うディレクトリ。apply workload の入口と、`cmoc realization apply fork` の実行フローを確認するために読む。

## Read this when
- realization の apply workload を調査・変更するとき。
- `cmoc realization apply fork` の処理フロー、agent 実行、差分検査、commit、run 状態遷移、fork report を確認するとき。

## Do not read this when
- apply fork の launch parameter 構築だけを調査・変更するとき。
- run lifecycle の共通処理や report 形式だけを確認するとき。
- realization apply fork 以外のサブコマンドの実行フローを調査するとき。

## hash
- 3d86a47945ffd9b4cd81539a13dabff57ad1d09ca9730bbc46edef03f283b31c

# `refactor`

## Summary
- realization のリファクタリング処理を扱うパッケージで、関連処理への入口を提供する。
- fork.py は、refactor run の初期化から対象ファイルの調査・修正、検証、commit、所見追跡、完了判定、状態更新、レポート出力までの full-cycle CLI lifecycle を実装する。

## Read this when
- realization のリファクタリング処理の構成や入口を確認するとき。
- refactor fork の CLI 実行フロー、状態遷移、対象ファイル処理、unresolved 所見、rollback、完了条件、fork report を調査・変更するとき。

## Do not read this when
- refactor state のデータ構造や target 選択ロジックだけを扱うときは、commons.runtime_refactor を直接読む。
- file 単位の review agent parameter や change summary parameter の生成だけを扱うときは、対応する builder module を直接読む。
- 一般的な run lifecycle、commit、差分分類、共通 report 処理だけを扱うときは、sub_commands.run の共通 module を直接読む。

## hash
- 8d526c9abc790303ffa1c8f10b81f63600ae4793ecc61e06d6af6062c987bc06
