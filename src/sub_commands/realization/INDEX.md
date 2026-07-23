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
- realization のリファクタリング処理をまとめるパッケージ。refactor fork のライフサイクル全体を管理し、対象選択から agent 実行、差分検証、state 更新、commit、完了判定、report 生成までの上位 orchestration を提供する。

## Read this when
- realization refactor fork の処理フロー、完了条件、unresolved finding、state・run・git 差分・report の連携を調査または変更するとき。
- agent 実行後の差分検証、commit、KeyboardInterrupt や失敗時の cleanup・rollback・error report の挙動を確認するとき。

## Do not read this when
- refactor agent の Structured Output parameter や file review 固有の処理を変更・調査するとき。
- refactor state のデータ構造・target 同期、または editing run の共通処理だけを確認するときは、対応する専用 module を直接読む。

## hash
- e45fb1f654a781d16df26f7ce280ce48efc16bbd9676fb17e82735f561c925ea
