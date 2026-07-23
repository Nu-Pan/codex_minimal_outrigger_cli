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
- realization の apply 処理に関する workload を扱うディレクトリ。apply workload 実装への入口であり、配下の apply fork 実行本体も確認できる。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の実行フロー、agent 起動、変更検査、commit、run state、fork report の挙動を確認・変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- realization apply fork の agent 起動パラメータ生成だけを変更するとき。
- run の共通ライフサイクルや report 生成の仕様だけを確認するとき。

## hash
- a72ad755ca8f8bc0679176e8189c25d6ee3a6708ea3a74176f488274d859907a

# `refactor`

## Summary
- realization のリファクタリング処理を扱うパッケージ。一般的なリファクタリング処理の入口と、fork による一連のリファクタリング lifecycle の実装を含む。
- fork の full-cycle CLI workload では、対象選択、調査・修正、state 同期、差分検証・commit、unresolved 所見の管理、完了判定、change summary と fork report の生成までを扱う。

## Read this when
- realization のリファクタリング処理の構成や CLI 動作を確認・変更するとき。
- realization refactor fork の対象選択、処理順序、state、unresolved 所見、commit、rollback、error、report 生成を確認するとき。
- refactor agent の findings または change summary の Structured Output 検証を調査するとき。

## Do not read this when
- realization refactor の一般仕様だけを確認したいときは、対応する oracle の仕様を先に読む。
- file 単位の agent パラメータ生成、個別 review・fix、共通 lifecycle・runtime・report の実装を確認するときは、対応する下位モジュールを直接読む。
- fork 以外の realization refactor サブコマンドを調査するとき。

## hash
- ec788adfe2114b410ca7ba71b37fd55a9c7cde3e2a0d1d27e33399a80035a07b
