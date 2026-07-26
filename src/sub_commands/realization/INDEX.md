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
- realization の apply 処理に関する workload を扱うディレクトリ。apply workload の実装を確認する入口であり、apply fork の実行制御を含む。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` のライフサイクル、agent 実行、oracle 差分、差分 commit、state 遷移、fork report、失敗時 cleanup を調査・変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- realization apply agent の prompt 構築だけを変更・調査する場合。
- run の一般的な join・abandon 処理や共通 state 操作だけを確認する場合。

## hash
- 5294150fc290468bf937c4e1117bc512d3abd21dad07817a77e69eb2513166b6

# `refactor`

## Summary
- realization のリファクタリング処理をまとめるパッケージ。リファクタリングの実行フローを担うランタイムへの入口を提供し、関連する処理単位や実行状態の管理に関わる。

## Read this when
- realization refactor の実行フロー、処理単位、完了条件を確認するとき
- refactor state や unresolved finding の同期・判定を調査するとき
- agent call 後の差分検証、commit、中断・エラー処理、report 保存を調査するとき

## Do not read this when
- realization refactor の agent call パラメータ生成だけを調査するとき
- 変更概要の Structured Output 生成だけを調査するとき
- 共通の editing run lifecycle、refactor state、process tracking、report 生成を調査するとき

## hash
- 5fe8b27e62900ef446317d39e3e72bb129765a7a40e3a49ce0db15d3acff417e
