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
- `cmoc realization apply fork` の実行処理を担う CLI サブコマンド実装。realization apply agent の起動、oracle 差分の構築、変更検査・INDEX 更新・commit、run の joinable 公開、fork report 保存までを一連の workload として扱う。失敗時は子プロセス停止、変更 rollback、error state 更新、エラーレポート保存を行う。

## Read this when
- realization apply fork の実行フロー、run 状態遷移、agent 差分の許可判定、commit または rollback、fork report の生成を変更・調査するとき。
- realization apply agent の起動条件や oracle 差分の受け渡し、INDEX 更新を含む処理単位を確認するとき。

## Do not read this when
- realization apply の prompt 構築や agent parameter の詳細だけを確認したいときは、呼び出される builder 実装を直接読む。
- run の共通ライフサイクル、プロセス追跡、report 出力の共通仕様だけを確認したいときは、ここで呼び出している commons の実装や対応する oracle 文書を直接読む。

## hash
- a416cbe2c27091e6cbe07dcd6dbd63591c366cda69ad875f3efb0f0afbac03da
