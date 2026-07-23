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
- realization apply の workload 実装を扱うディレクトリ。apply workload 全体の調査・変更時に、配下の各実装へ進む入口となる。

## Read this when
- realization apply workload の実行フロー、agent 起動、差分検証、commit・rollback、run state、fork report の挙動を調査・変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- agent 起動パラメータ、run の共通 lifecycle・差分計算・状態管理、fork report の形式だけを変更・調査するとき。

## hash
- b01abe2a06082d4c8096e120594ec68328dcac5efc628f9af6800bddd4c4486b

# `refactor`

## Summary
- realization のリファクタリング処理をまとめるパッケージ。`fork.py` を中心に、refactor fork の実行ライフサイクル、対象処理、状態同期、commit、完了判定、report、cleanup を扱う。

## Read this when
- realization のリファクタリング処理の構成や入口を確認するとき。
- refactor fork の実行フロー、対象選択、commit、unresolved 管理、完了条件、report、割り込み・エラー時の cleanup を調査・変更するとき。
- refactor agent の Structured Output と、差分・state・index の整合性を確認するとき。

## Do not read this when
- 通常の realization refactor 仕様や agent prompt の内容を確認したいとき。対応する oracle 文書を直接読む。
- refactor state のデータ構造や対象同期処理を変更・調査するとき。`commons.runtime_refactor` の実装を直接読む。
- run の一般的な lifecycle、差分分類、report 共通処理を変更・調査するとき。`sub_commands.run` 配下の責務モジュールを直接読む。

## hash
- 9dbac15295d20373e096a258bead5681fdb361870dd941aa205692f7b01697e2
