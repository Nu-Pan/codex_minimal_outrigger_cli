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
- realization の apply 処理を実装するモジュール群。apply workload の入口と、fork サブコマンドの実行フローを確認するためのディレクトリ。

## Read this when
- realization の apply workload を調査・変更するとき
- `cmoc realization apply fork` の実装、差分追従、commit、run 状態更新、fork report 保存を確認するとき

## Do not read this when
- apply workload 以外の処理を扱うとき
- apply agent の prompt 生成だけを確認したいとき
- run 共通状態管理や fork report 共通フォーマットだけを確認したいとき

## hash
- 4bb03f02951c0b98f5a26985f5c72ed03924b30be9a9877d469444f12f2b7f3b

# `refactor`

## Summary
- realization のリファクタリング処理を提供するパッケージ。パッケージ初期化と、refactor run の開始から完了・中断・エラー処理までを担う CLI 実行フローへの入口。
- 対象 realization file の選択・調査・修正、findings と unresolved 状態の管理、差分検証、state 更新、処理単位の commit、report 保存を扱う。

## Read this when
- realization refactor の CLI 挙動や run lifecycle を確認・変更するとき
- 対象 file の選択、findings の検証、refactor state、完了条件、fork report を調査するとき
- 中断・エラー時の子プロセス停止、rollback、run 回収、unresolved findings の整合性を調査するとき

## Do not read this when
- 個別 realization file のリファクタリング内容を調査・変更するとき
- refactor state のデータ構造や target 選択ロジックだけを調査するとき
- 一般的な editing run の join、abandon、report 処理だけを調査するとき

## hash
- 224a154b32b89a8f08c690787c066591dba475d1ba6f9e1a6418b55df2e8d881
