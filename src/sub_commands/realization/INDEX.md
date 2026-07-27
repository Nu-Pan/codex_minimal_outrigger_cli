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
- realization のリファクタリング処理を扱うパッケージ。リファクタリング関連機能の入口として、パッケージ構成を確認する際に参照する。
- realization refactor fork の実行ライフサイクルを担当する CLI ワークロード。state 初期化、対象ファイルの調査・修正、差分検証、commit、未解決所見、完了判定、report 生成までのフローを扱う。

## Read this when
- realization のリファクタリング処理の構成や入口を確認するとき。
- refactor fork の実行フロー、対象選択、state 遷移、commit、未解決所見、cleanup、完了判定、report 出力を調査・変更するとき。

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき。
- 対象選択や state 同期の共通処理を調査するとき。
- 単一ファイルの agent review・修正処理や変更概要生成を調査するとき。
- 一般的な editing run の lifecycle や report 共通処理を調査するとき。

## hash
- a7be7907997f647d4e00d93e2ca395191df16dbbc1a05bf77eb4736f9e0a2e96
