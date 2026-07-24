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
