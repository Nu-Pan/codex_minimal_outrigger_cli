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
- realization のリファクタリング処理をまとめるパッケージ。リファクタリング実行フローの入口と、対象ファイル単位の調査・修正から完了判定・レポート生成までの流れを扱う。

## Read this when
- realization のリファクタリング処理の構成や入口を確認するとき。
- realization refactor fork の実行フロー、state 更新、未解決所見、cleanup、完了判定、レポート生成を調査・変更するとき。

## Do not read this when
- realization refactor の対象選択や state 永続化の共通処理を調べるとき。
- file review agent の prompt parameter や change summary の生成仕様を調べるとき。
- editing run の共通ライフサイクルや report writer の一般仕様を調べるとき。

## hash
- 8fb20074e34f1e44609a1711b7683473e3cc4a53545800efc2d26c7790430fb3
