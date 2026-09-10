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
- realization の apply workload を扱うモジュール群への入口。
- apply fork の実行入口として、editing run の作成、oracle 差分範囲の固定、追従 agent の実行、変更検査と commit、joinable/error 状態の記録を担う。

## Read this when
- realization apply workload の構成や実装を調査・変更するとき
- realization apply fork の実行手順、差分の始点、agent 実行後の変更検査・commit、joinable/error run の状態遷移を確認するとき

## Do not read this when
- apply workload 以外の realization 処理を扱うとき
- realization apply の agent 起動パラメータを確認したいとき
- editing run の共通 lifecycle や run の join・abandon 実装を確認したいとき
- INDEX.md 生成の一般仕様や利用者向け CLI 仕様だけを確認したいとき

## hash
- c3a77808dce997fb29e44a0e9c6129da744dc557e9ee958b581a261b12cedb17

# `refactor`

## Summary
- realization のリファクタリング処理をまとめるパッケージ。fork の実行ライフサイクルを入口として、対象調査・修正、状態更新、commit、未解決事項管理、完了判定、report 保存までを扱う。

## Read this when
- realization refactor fork の処理順序や対象反復、状態・commit・INDEX の検証、完了条件、cleanup、report を確認または変更するとき。

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき。
- 対象選択や refactor state 同期の詳細だけを確認するときは、専用の state 管理・target selection 実装を読むとき。
- file review agent や change summary の prompt・schema 契約だけを確認するとき。

## hash
- 189d1ee01f0ac00be80a00c9f83bab58c4fec771daf07b5797245060aa012226
