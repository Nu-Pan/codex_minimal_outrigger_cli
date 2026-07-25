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
- realization の apply 処理に関する workload を扱うディレクトリ。apply workload の実装を確認する入口となる。
- `cmoc realization apply fork` の CLI 実行処理を担当し、apply fork の run lifecycle、agent 実行、差分検証、commit、状態遷移、report 保存、失敗時 rollback を扱う。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の CLI 挙動、run lifecycle、agent 実行、差分検証、commit、joinable/error state、fork report、失敗時 rollback を調査・変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- realization apply agent のプロンプトや起動パラメータ生成だけを扱うとき。
- run 状態管理、差分取得、commit、INDEX 更新、report 生成の共通仕様・実装だけを確認するとき。
- `cmoc realization apply fork` 以外のサブコマンドの CLI 本体を扱うとき。

## hash
- 8fcac3ceac4121ef9caeffdcd6f3f3b6d866432259fc7803d12301b2838d7520

# `refactor`

## Summary
- realization のリファクタリング処理をまとめるパッケージ。リファクタリング実行全体の入口として、関連する fork 実行処理へ進むためのルーティング先。

## Read this when
- realization refactor の実行ライフサイクル、対象ファイル単位の処理、agent 調査・修正、差分検証、commit、unresolved finding 管理を確認するとき。
- リファクタリングの中断・エラー時の cleanup、rollback、run state、report、完了ログの挙動を確認するとき。

## Do not read this when
- realization refactor の agent 入力 parameter の内容だけを変更・調査するとき。
- refactor state のデータモデルや対象選択ロジックだけを確認するとき。
- run の共通ライフサイクル、Git 差分、INDEX 更新の汎用処理だけを確認するとき。

## hash
- 0ec98020331ecfc2c8fb23b930977fd83640e8aa0b3f6403bf15904812d300b2
