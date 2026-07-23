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
- realization の apply 処理に関する workload を扱うディレクトリ。apply workload の実装を確認する入口であり、配下に apply の共通処理と fork サブコマンド処理がある。
- fork は `cmoc realization apply fork` の実行フローを担い、oracle 差分を基準とした agent 起動、変更検証、INDEX 更新、commit、状態遷移、report 保存、および失敗時の rollback・error state 更新を扱う。

## Read this when
- realization の apply workload の内容を調査・変更するとき
- `cmoc realization apply fork` の処理フロー、状態管理、差分検証、commit、fork report、成功・失敗時の挙動を確認するとき

## Do not read this when
- apply workload 以外の処理を扱うとき
- apply agent の起動パラメータ生成だけを確認する場合
- run の共通ライフサイクルや report 生成の汎用処理だけを確認する場合

## hash
- 8500437c78ea8062326ea97df740d0c9310eb18d04da07fe68509b847dcaa1d9

# `refactor`

## Summary
- realization のリファクタリング処理を扱うパッケージ。refactor fork の実行フロー、状態管理、差分検証、commit、report 保存など、関連する処理への入口となる。

## Read this when
- realization refactor の実行フローや処理構成を確認するとき。
- refactor fork の対象選択、agent 調査・修正、未解決所見、完了判定、中断時の report 処理を調査・変更するとき。

## Do not read this when
- realization refactor 以外の処理を確認するとき。
- agent parameter の構築、refactor state のデータ操作、一般的な run lifecycle・差分分類・report 共通処理だけを確認するとき。

## hash
- 04d961e363b178b36df13b5d89e8dfb812ff839e4d1d9df1be607031ea7ccb7b
