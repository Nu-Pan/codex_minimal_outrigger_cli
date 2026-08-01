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
- `cmoc realization apply fork` サブコマンドの実行制御を担う実装。realization apply agent を起動し、oracle 差分の構築、変更検査、INDEX 更新、commit、joinable/error 状態への遷移、fork report 保存までを一連の workload として管理する。
- apply run の開始・失敗時回収・変更 rollback・Codex 子プロセス停止・想定外差分の検出など、編集 run のライフサイクル制御が必要な処理の入口。

## Read this when
- `cmoc realization apply fork` の実行フロー、成功時の joinable 化、または fork report の内容を変更・調査するとき。
- realization apply agent に渡す oracle 差分、許可済み変更、commit 前後の差分検査を確認するとき。
- apply run の error state、rollback、cleanup warning、Codex 子プロセス停止の挙動を変更・調査するとき。

## Do not read this when
- realization apply agent が受け取る launch parameter の構築詳細だけを確認したいときは、`acp.builder.realization.apply.fork.launch_exec` を直接読む。
- 編集 run 全体の仕様や共通ライフサイクル API の定義だけを確認したいときは、対応する `commons.runtime_run_lifecycle` および oracle の editing run 文書を直接読む。
- fork report の共通フォーマットだけを確認したいときは、`commons.runtime_run_report` を直接読む。

## hash
- 65aeabb04eb3c594658c48665f0db6226ebd8734481c537631812b348a078734
