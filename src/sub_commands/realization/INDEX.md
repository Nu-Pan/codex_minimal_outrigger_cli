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
- realization の apply 処理に関する workload と、`cmoc realization apply fork` の実行制御を扱う。apply workload の調査入口であり、fork では editing run の開始から agent 実行、差分検査、commit・rollback、run 状態更新、report 保存、joinable 公開までを統括する。

## Read this when
- realization の apply workload の内容を調査・変更するとき
- `cmoc realization apply fork` の開始から joinable または error までの制御フローを確認するとき
- apply agent の実行条件、oracle 差分、想定外差分、commit、rollback、run report、例外処理を調査・変更するとき

## Do not read this when
- apply workload 以外の処理を扱うとき
- 共通の editing run ライフサイクル、process tracking、report 生成の一般仕様や実装だけを調査するとき
- `cmoc realization apply` の通常実行や別の apply サブコマンドだけを調査するとき
- apply agent の prompt 構築内容だけを確認するとき

## hash
- 66f6170c37b0f2633264194384049584f7809db7f2ef2c8455dba3f5466cd08e

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
