# `__init__.py`

## Summary
- realization の apply 処理に関する workload を扱うモジュール。apply workload の実装を確認する入口となる。

## Read this when
- realization の apply workload の内容を調査・変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。

## hash
- d6d2ca470e50cfd6872e3d6ceaaf3a134b7f0dc8205826c843ca70d79352d5f7

# `fork.py`

## Summary
- `cmoc realization apply fork` の CLI 実行を担当し、oracle 差分を基準に realization apply agent を起動する。
- agent の変更範囲を検証し、INDEX 更新を含む差分の commit、run の joinable/error 更新、fork report の保存までを管理する。
- realization apply fork の実行制御、失敗時の rollback・error 記録・実行済み run の復旧処理を確認する入口。

## Read this when
- `cmoc realization apply fork` の実行フローや run lifecycle を変更・調査するとき。
- oracle 差分の構築、Codex agent の起動、agent 差分の許可範囲検証を確認するとき。
- 正常終了時の commit・joinable 化・fork report、または失敗時の rollback と error report を確認するとき。

## Do not read this when
- realization apply agent の起動パラメータ生成だけを調査する場合は、専用の launch parameter 実装を直接読む。
- run 状態管理、差分計算、INDEX 更新、report 生成の共通仕様だけを調査する場合は、それぞれの共通 runtime module を直接読む。
- 別の realization apply サブコマンドの処理を調査する場合。

## hash
- 157f220280d3e4aa9b1b1daeb90518a0948fa64b855af716fce162ce389972f9
