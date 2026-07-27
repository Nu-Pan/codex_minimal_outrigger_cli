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
- `cmoc realization apply fork` サブコマンドの実行制御を担うモジュール。realization apply 用 editing run の開始、oracle 差分の構築、Codex agent 実行、想定外変更の検査、INDEX 更新を含む commit、joinable 公開、fork report 保存を統括する。
- agent 実行時の失敗では子プロセス停止、作業差分の rollback、run の error state 更新、失敗 report 保存までを行う。run 回収や差分始点 commit の解決など、fork 固有のライフサイクル処理も含む。
- realization apply fork の挙動、run 状態遷移、Codex 実行、差分検査、commit・rollback、report 生成を変更または調査するときの入口となる。共通ライフサイクルや process tracking の詳細実装を変更する場合は、直接それらの共通モジュールを読む。

## Read this when
- `cmoc realization apply fork` の開始から joinable または error までの制御フローを確認するとき
- realization apply agent の実行条件、oracle 差分、想定外差分、commit、rollback、run report の扱いを変更または調査するとき
- fork 開始後の例外処理や run 回収の挙動を確認するとき

## Do not read this when
- 共通の editing run ライフサイクル、process tracking、report 生成の一般仕様や実装だけを調査するときは、対応する共通モジュールや oracle 文書を直接読む
- `cmoc realization apply` の通常実行や別の apply サブコマンドの責務だけを調査するとき
- realization apply agent の prompt 構築内容だけを確認するときは、launch parameter builder を直接読む

## hash
- 71fae81cb4ca2009f3849fa1200204d68fe49bb3034b8ef54ac30b1f38bd964a
