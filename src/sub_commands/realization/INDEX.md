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
- realization の apply workload を扱うディレクトリ。apply workload の入口と、`cmoc realization apply fork` の実行フローを確認するために読む。

## Read this when
- realization の apply workload を調査・変更するとき。
- `cmoc realization apply fork` の処理フロー、agent 実行、差分検査、commit、run 状態遷移、fork report を確認するとき。

## Do not read this when
- apply fork の launch parameter 構築だけを調査・変更するとき。
- run lifecycle の共通処理や report 形式だけを確認するとき。
- realization apply fork 以外のサブコマンドの実行フローを調査するとき。

## hash
- 3d86a47945ffd9b4cd81539a13dabff57ad1d09ca9730bbc46edef03f283b31c

# `refactor`

## Summary
- realization のリファクタリング処理をまとめるパッケージ。リファクタリング全体の入口と、fork 実行のライフサイクル管理を扱う。

## Read this when
- realization のリファクタリング機能の構成や実行フローを確認するとき
- fork の対象選択、調査・修正、state 遷移、差分検証、rollback、report 保存を調査・変更するとき

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき
- file 単位の agent prompt や findings schema を変更するとき
- 共通の state 保存・同期、lifecycle、commit、rollback 処理を変更するとき

## hash
- 9964c974903cdcaeab28d49225241f168eff2424297b4fd72fb0f1325e0d6aab
