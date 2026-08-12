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
- realization の apply 処理を構成する実装を扱うディレクトリ。apply workload の実装と、apply fork における agent 実行、差分検査、run状態更新、rollback、fork report保存の入口となる。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の実行フロー、run状態遷移、fork reportの保存条件を調べるとき。
- apply agentが作成した差分の許可範囲、commit検査、想定外変更、失敗時のrollbackやerror stateを確認・変更するとき。

## Do not read this when
- apply workload以外のrealization処理を扱うとき。
- apply agent自体のプロンプト生成や差分適用仕様を調べるとき。
- editing run全般の共通ライフサイクル、INDEX生成機能そのものの仕様や実装を調べるとき。

## hash
- 2eb7b3e16a04df8e5901fe5b1081254e24ec9cf33810dcec224ead9f8de8563e

# `refactor`

## Summary
- realization のリファクタリング作業を扱うパッケージ。refactor fork の実行 lifecycle と関連処理への入口となる。
- fork の実行順序、対象選択、agent による変更検証、state 更新、INDEX 同期、完了・中断・エラー時の処理を確認する際は fork 実装へ進む。

## Read this when
- realization refactor fork の CLI 実行 lifecycle や処理順序を調査するとき
- 対象 realization file の選択、findings と unresolved の整合、refactor state 更新、完了条件を確認するとき
- agent の変更検証、INDEX refresh、rollback・joinable・error 処理を確認するとき
- fork report や completion log の生成内容・完了理由を確認するとき

## Do not read this when
- file review agent の入力形式や調査・修正プロンプトだけを確認する場合
- 正常完了時の変更概要生成の入力・Structured Output を確認する場合
- refactor state の一般的な保存・同期仕様だけを確認する場合
- run isolation や interruption の正本仕様を確認する場合

## hash
- 6d967dc9ec35685fad62a7e8185c1e5e92cae8c9f2a49bcbdcf72eff281457a9
