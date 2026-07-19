# `__init__.py`

## Summary
- oracle edit サブコマンドの workload を扱うパッケージ。

## Read this when
- oracle edit サブコマンドの workload に関する実装や責務を確認するとき。

## Do not read this when
- oracle edit 以外のサブコマンドを扱うとき。

## hash
- 76a5965a24abb48a2f5ce594bcecdb391b2dcb29b37067d5f857fcbad7e3ff43

# `fork.py`

## Summary
- `cmoc oracle edit fork` サブコマンドの実行制御を担う実装。編集指示の収集、isolated editing run の作成、Codex agent の実行、oracle 差分の検証・commit、run 状態更新、fork report 保存までを一連のワークフローとして扱う。

## Read this when
- `cmoc oracle edit fork` の実行フロー、事前条件、agent 差分の検証、commit、joinable/error 状態、fork report の挙動を変更・調査するとき。

## Do not read this when
- oracle 編集 agent の prompt 生成仕様だけを確認したいときは、launch parameter builder や oracle prompt の正本を直接読む。
- run 共通ライフサイクルの詳細だけを確認したいときは、`sub_commands.run.lifecycle` を直接読む。
- fork report の出力形式だけを確認したいときは、`sub_commands.run.report` を直接読む。

## hash
- 2a34b81bf5e5603a3833e41e5d7384251d3eb2f1922609a5cdfc8cbfc5dcb4dd
