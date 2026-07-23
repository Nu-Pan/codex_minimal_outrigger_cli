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
- realization の apply 処理に関する workload を扱うディレクトリ。apply workload 実装の確認入口であり、fork サブコマンドの実行制御や run lifecycle の実装へ進む起点となる。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の実行フロー、oracle 差分を基準にした agent 起動、変更範囲検証、commit、run 状態更新、fork report 保存、失敗時 rollback を調査・変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- realization apply agent の起動パラメータ生成だけを調査する場合。
- run 状態管理、差分計算、INDEX 更新、report 生成の共通仕様だけを調査する場合。
- 別の realization apply サブコマンドの処理を調査する場合。

## hash
- 9aba22ebe989d266f79868e8c7e5bec34e5ee842f417b462c92d9fa774723844

# `refactor`

## Summary
- realization のリファクタリング処理をまとめるパッケージ。リファクタリング関連 CLI の実行入口と、個別処理へ進むための構成を提供する。

## Read this when
- realization のリファクタリング処理の実行フローやパッケージ構成を確認するとき。

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき。
- 個別 realization file のレビュー・修正、変更概要生成、共通 lifecycle・state・差分分類・report 処理だけを調べるとき。

## hash
- 3c3d46bee05cbed94f87b79904e586471efa1cf9f691988c01489d643d3f98b4
