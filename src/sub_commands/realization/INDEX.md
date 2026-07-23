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
- realization の apply 処理に関する workload を扱うモジュール群。apply workload の実装を確認する入口となる。
- `cmoc realization apply fork` の CLI 実行フローを担当し、apply 差分の特定、oracle diff 構築、realization 追従 agent 実行、差分検査・commit、run 状態更新、fork report 保存を扱う。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の実行フロー、失敗時の rollback・error state 遷移、想定外差分の検証を変更または調査するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- fork 用の launch parameter 生成だけを変更するとき。専用の builder 実装を直接読む。
- run の共通ライフサイクルや report 形式だけを確認するとき。対応する共通実装を直接読む。

## hash
- 41b4b84042134c51b640afd471f995b1289d860ad1bc9ea2e3c30fa8c7e65b29

# `refactor`

## Summary
- realization のリファクタリング処理を扱うパッケージ。fork のライフサイクル実行と関連処理への入口を提供する。
- fork は、run 初期化から target 選択、調査・修正・commit、unresolved 管理、完了検証、summary/report 生成、中断・例外時の cleanup までを一つのフローとして実装する。

## Read this when
- realization refactor fork の CLI 実行フロー、target 処理、unresolved finding、完了判定を確認・変更するとき。
- 中断・例外時の cleanup、run state、fork report、change summary、worktree や agent 出力の整合性を調査するとき。
- realization のリファクタリング作業全体の構成や入口を確認するとき。

## Do not read this when
- target 選択や state 同期だけを変更・調査する場合。
- file 単位の調査・修正 agent の prompt 構築だけを変更する場合。
- 一般的な run lifecycle、report 出力、process tracking の共通実装だけを確認する場合。

## hash
- a4e80e064346eb0492ad620f30f739fca349cd4a88d53da14baec64b3d4607e5
