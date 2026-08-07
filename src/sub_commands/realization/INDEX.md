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
- realization の apply 処理に関する実装をまとめるディレクトリ。apply workload の入口と、`realization apply fork` の実行オーケストレーションを確認するために読む。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の実行順序、run state 遷移、apply agent 起動、差分検査、commit 単位の処理、fork report 保存や失敗時 cleanup を調査・変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- apply agent 自体のプロンプトや差分適用規則だけを調べるとき。
- 共通の run lifecycle、process tracking、git 差分操作の一般仕様だけを調べるとき。
- apply fork と無関係な CLI サブコマンドの挙動を調べるとき。

## hash
- eb7545f0b637ac9a56a90a93e267347684b622220449242820e5034e90a9b328

# `refactor`

## Summary
- realization のリファクタリング処理を担うパッケージ。CLI 実行ライフサイクル、対象ファイルの調査・修正、状態同期、差分・commit 検証、完了・中断・エラー処理、fork report 生成への入口となる。
- 個別の agent parameter、共通 runtime、refactor state のデータ構造、INDEX 更新処理だけを確認する場合は、配下の実装や対応する共通処理へ直接進む。

## Read this when
- realization refactor fork サブコマンドの実行順序、状態遷移、処理単位、commit 境界を調査するとき
- refactor target の選択、unresolved finding の管理、rename 後の state 同期、完了判定を変更・検証するとき
- 中断・例外時の child process 停止、rollback、run state 更新、error/interruption report の挙動を調査するとき
- fork report の変更概要、state 集計、completion log の生成内容を確認するとき

## Do not read this when
- file review agent の prompt や Structured Output parameter の仕様だけを確認したいとき
- refactor state のデータ構造や target 同期処理だけを確認したいとき
- run の共通 lifecycle、git 差分分類、process tracking の一般仕様だけを確認したいとき
- INDEX 更新処理そのものの仕様だけを確認したいとき
- realization のリファクタリング以外の処理を確認するとき

## hash
- abe322cb84e0b08816d5f1b252d160fdd8f033ccc4ee42735065f185f7380818
