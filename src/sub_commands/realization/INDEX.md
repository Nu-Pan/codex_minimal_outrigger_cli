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
- realization の apply 処理に関する workload と、apply fork の実行・差分検査・処理単位確定を扱う実装群への入口。

## Read this when
- realization apply workload の実装を調査・変更するとき
- realization apply fork の run 作成、agent 実行、差分検査、commit、joinable 公開、成功・失敗 report の挙動を確認するとき

## Do not read this when
- apply workload 以外の処理を扱うとき
- apply fork の agent 起動パラメータだけを確認するとき
- editing run 共通ライフサイクルや realization apply agent の具体的な差分内容を直接確認するとき

## hash
- bea89968dea14226e760d3c9247a1219bab9432e20fd4963c5637d0245c3a499

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
