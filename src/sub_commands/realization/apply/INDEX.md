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
- `cmoc realization apply fork` の実行本体を担い、realization apply agent の差分追従処理を run として管理する。oracle diff の構築、agent 実行、想定外差分の検査、INDEX 更新を含む commit、joinable/error state への更新、fork report 保存までを扱う。
- realization apply fork の CLI 制御を確認する際の実装入口であり、run lifecycle、process tracking、差分検査、レポート生成の下位処理へつながる。

## Read this when
- `cmoc realization apply fork` の実行フロー、成功時の commit・joinable 化、失敗時の rollback・error report を調査または変更するとき
- realization apply agent の差分範囲検査、Codex child process の停止、run state の復旧処理を確認するとき

## Do not read this when
- realization apply agent が生成する prompt や launch parameter の詳細だけを確認したいときは、対応する builder を直接読む
- run の共通状態管理・差分操作・process tracking の実装だけを確認したいときは、`commons.runtime_run*` 系の実装を直接読む
- 別の realization apply サブコマンドや fork report の一般仕様だけを確認したいときは、該当するサブコマンド実装または oracle 文書を直接読む

## hash
- 7a3b08bd650a7b812e47677d18546fe27b2b3c253fa92e96c1baa9d3d87c1c4c
