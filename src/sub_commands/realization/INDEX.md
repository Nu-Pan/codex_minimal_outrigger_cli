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
- realization の apply 処理を扱うディレクトリ。apply workload の入口と、`cmoc realization apply fork` による差分追従・run 管理・失敗時処理を確認するための領域。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の実行フロー、差分検査、commit・rollback、fork report、run 状態遷移を確認するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- 通常の apply agent の prompt 構築だけを変更するとき。
- run の共通ライフサイクルや状態管理自体を変更するとき。

## hash
- ffe513eaffcdea50c7bf61af57444c3d303033e63b2129f07eea9872f95dce41

# `refactor`

## Summary
- realization のリファクタリング処理を扱うパッケージで、関連する fork 実行ライフサイクルやリファクタリング処理への入口を提供する。

## Read this when
- realization のリファクタリング実行フロー、対象選択、agent call 後の差分検証、state 更新、commit、完了判定を確認するとき
- 中断・エラー時の cleanup、unresolved finding、fork report の保存と run state 遷移を確認するとき

## Do not read this when
- 単一ファイルの調査・修正 agent parameter 生成だけを確認するとき
- 変更概要の Structured Output 仕様だけを確認するとき
- 一般的な editing run のライフサイクルや共通 Git 差分処理だけを確認するとき

## hash
- 3a2e0746d40b9164ab454388960e45ebb640143c712ebc343f4c47e7f5635478
