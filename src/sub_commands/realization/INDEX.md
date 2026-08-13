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
- realization の apply 処理に関する実装を扱うディレクトリ。apply workload の実装と、`realization apply fork` の CLI 実行フローを調査・変更する際の入口となる。
- apply fork では editing run の開始、差分追従 agent の実行、想定外変更や agent commit などの検査、INDEX 生成を含む変更の commit、joinable/error 状態と report の保存を扱う。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の実行フロー、editing run の状態遷移、差分の commit・rollback・report 保存を確認するとき。
- apply agent の変更と cmoc が生成する INDEX 差分の境界、agent commit や遅延 child の扱いを確認するとき。

## Do not read this when
- apply workload 以外の realization 処理を扱うとき。
- apply agent の起動パラメータだけを変更するときは、agent launch parameter の実装を直接読む。
- editing run の共通ライフサイクル、git 操作、state 管理、index refresh の一般仕様だけを確認するときは、対応する共通実装または正本仕様を直接読む。
- apply fork の利用者向け仕様や run isolation・indexing の正本仕様を確認するときは、参照されている app specification を読む。

## hash
- 1cac93e44cd9b42024897895b67141aebefc28ad7144e9c990518c4195d92219

# `refactor`

## Summary
- realization のリファクタリング処理をまとめるパッケージで、関連するリファクタリング処理への入口を提供する。
- fork.py は realization refactor fork CLI の実行 lifecycle と一時状態共有型 workload を管理し、対象 realization file の選択、Codex による調査・修正、変更検証、所見管理、INDEX 同期、fork report 保存までを扱う。

## Read this when
- realization のリファクタリング処理の構成や実行入口を確認するとき
- refactor fork CLI の実行順序、run state、対象 file の処理単位、完了条件、fork report を調査・変更するとき
- 中断・例外時の停止、rollback、cleanup、error state の挙動を確認するとき
- refactor state、INDEX 同期、changed_paths 検証、所見の unresolved 管理を確認するとき

## Do not read this when
- realization refactor の一般仕様や CLI 契約だけを確認する場合
- file 単位の agent prompt や finding schema の生成内容だけを確認する場合
- run lifecycle、git 差分分類、process tracking など共通機構の詳細だけを確認する場合
- INDEX 生成規則や INDEX 更新処理だけを確認する場合

## hash
- a76634eebce7f45b64553259b6e504b87c28afbfe0acce184a4ef35ede1fcaba
