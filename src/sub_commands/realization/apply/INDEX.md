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
- `cmoc realization apply fork` の実行本体を担う。editing run の作成、apply agent の起動、差分検査、INDEX 生成物を含む処理単位の commit、joinable/error state への更新、fork report 保存までを一連の CLI runtime として管理する。
- apply agent が作成した想定外差分や commit、遅延 Codex child の書き込み、preflight commit を検出・整理し、成功時は join 可能な成果物へ、失敗時は rollback 後の error run へ遷移させる。
- apply 固有の diff base commit と accepted feedback observation を fork report の追加情報として記録する。内部の差分検査・cleanup・error report の詳細を確認する必要がある場合の実装入口でもある。

## Read this when
- `cmoc realization apply fork` の CLI 動作、run lifecycle、apply agent の実行境界を調査または変更するとき。
- apply agent の許可差分、INDEX.md 生成差分、agent commit 検出、遅延 child 停止、rollback と error state の扱いを確認するとき。
- realization apply fork report の生成条件、成功・失敗時の state 更新、diff base commit や feedback observation の記録方法を確認するとき。

## Do not read this when
- realization apply の agent prompt や launch parameter の内容だけを確認したいときは、launch parameter builder の実装を直接読む。
- editing run の共通ライフサイクル、join、abandon、state 管理の一般仕様だけを確認したいときは、共通 runtime lifecycle または該当する sub-command の実装を直接読む。
- INDEX.md の生成規則そのものだけを確認したいときは、indexing の仕様・実装を直接読む。

## hash
- f86ffe80c0ee70f5a6859f3126a8992c136648efc983d699cc729579e284f04d
