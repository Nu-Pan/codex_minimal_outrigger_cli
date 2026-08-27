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
- realization の apply 処理に関する workload を扱うディレクトリで、apply workload の実装を確認する入口。配下には apply の共通入口と、`cmoc realization apply fork` の実行を統括する実装がある。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の処理順序、成功・失敗時の run state、差分の許可範囲、commit/rollback、fork report、cleanup を確認または変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- realization apply の仕様や共通 editing run の契約を確認する場合は、対応する oracle/specification または共通 runtime 実装を直接読む。
- fork 以外の realization apply サブコマンドの固有処理だけを確認する場合は、各サブコマンドの実装を直接読む。

## hash
- 6cf3290d311d6d35194046bbeed7ea4ee6eaa5b1b8233f1c0893a54b7da0f0d9

# `refactor`

## Summary
- realization のリファクタリング処理を扱うパッケージで、関連処理への入口となる。
- `fork.py` は realization file の refactor fork を実行し、対象選択、refactor state と INDEX の初期化、agent 委譲、変更検証、commit、rollback、完了判定、report 保存までの lifecycle を担う。

## Read this when
- realization のリファクタリング処理の構成や入口を確認するとき。
- `cmoc realization refactor fork` の開始から joinable 公開までの lifecycle を調査・変更するとき。
- refactor の target 選択、処理単位、state 管理、unresolved finding、rename reconciliation、完了判定を確認するとき。
- agent の変更 path 検証、INDEX refresh、commit、rollback、Codex descendant cleanup、interruption/error handling を確認するとき。

## Do not read this when
- realization リファクタリング以外の処理を確認するとき。
- 個別 realization file の調査・修正 agent prompt の内容だけを確認したいとき。
- refactor の変更概要生成の Structured Output や prompt だけを確認したいとき。
- 一般的な run join、run abandon、editing run の共通仕様だけを確認したいとき。
- INDEX 更新の一般仕様だけを確認したいとき。

## hash
- 7850b8f9579f46b29dd86efdedd8da5a1b6592e89ab8fb8c097c19054b6e83e7
