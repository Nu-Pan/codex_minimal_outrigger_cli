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
- realization の apply 処理に関する workload を扱うディレクトリ。apply workload の実装を確認する入口であり、apply fork の実行制御を含む。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` のライフサイクル、agent 実行、oracle 差分、差分 commit、state 遷移、fork report、失敗時 cleanup を調査・変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- realization apply agent の prompt 構築だけを変更・調査する場合。
- run の一般的な join・abandon 処理や共通 state 操作だけを確認する場合。

## hash
- 5294150fc290468bf937c4e1117bc512d3abd21dad07817a77e69eb2513166b6

# `refactor`

## Summary
- realization のリファクタリング処理を扱うパッケージ。リファクタリング関連実装への入口となる。
- realization refactor fork の CLI lifecycle を管理し、editing run の初期化、対象ファイルの調査・修正、所見・状態更新、commit、完了判定、cleanup、状態遷移、fork report 保存までを扱う。

## Read this when
- realization のリファクタリング処理の構成や入口を確認するとき。
- realization refactor fork の lifecycle、対象選択、commit、unresolved finding、完了条件を調査・変更するとき。
- 中断・エラー時の cleanup、状態遷移、fork report、refactor state と worktree 差分の連携を確認するとき。

## Do not read this when
- 単一ファイルの調査・修正 agent call の入出力仕様だけを確認したいとき。
- 変更概要の Structured Output や report の共通保存処理だけを確認したいとき。
- realization refactor 以外の editing run、run join、abandon の仕様だけを調査するとき。

## hash
- 4cdc0f4390ff0ce07095f3d3440209c2ed75138affe3c25354babeda246f6d95
