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
- `cmoc realization apply fork` の実行本体を担い、realization apply agent の起動、差分検査、INDEX 生成、処理単位の commit、joinable/error 状態への更新、fork report 保存までを一連の run として管理する。
- agent による commit や想定外ファイル変更、遅延 Codex child、失敗時の rollback を検出・処理し、run の安全な後続操作（join または abandon）に必要な状態と報告を整える。
- apply 固有の差分始点 commit と accepted feedback observation を report に記録する。補助的な差分検査・cleanup・例外変換の実装への入口でもある。

## Read this when
- `cmoc realization apply fork` の実行フロー、run state、joinable/error 遷移、または fork report の挙動を確認・変更するとき。
- realization apply agent の変更許可範囲、agent commit 検出、INDEX 生成差分の扱い、遅延 Codex child の停止、rollback の境界を調査するとき。
- apply 差分の始点 commit や accepted feedback observation が report にどう反映されるかを確認するとき。

## Do not read this when
- realization apply agent 自体のプロンプト生成や launch parameter の構築だけを変更・調査するときは、対応する launch parameter 実装を直接読む。
- run の共通ライフサイクル、state 管理、差分分類、rollback、index refresh の一般仕様だけを確認するときは、対応する `commons.runtime_run*` 実装または正本仕様を直接読む。
- `cmoc run join` や `cmoc run abandon` の取り込み・破棄処理だけを確認するときは、それぞれの sub-command 実装を直接読む。

## hash
- eba08793f7cd8ac5ca53d33bf957bad90587f193325571c05adbfbd8ba1822e9
