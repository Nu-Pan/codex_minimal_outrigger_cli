# `__init__.py`

## Summary
- realization refactor workload のパッケージレベルの位置づけを示します。

## Read this when
- realization refactor パッケージの大枠の役割を確認するとき。

## Do not read this when
- realization refactor fork の実行フローや調査・修正処理を確認するときは、その実装の項目へ直接進んでください。

## hash
- d070e139f0ebc38e439ff4bf3b37f76a7a536a3424248e4afcc0525de0573746

# `fork.py`

## Summary
- `cmoc realization refactor fork` の一連の処理を統括し、対象選択、レビューと修正の実行、状態・INDEXの同期、処理単位のcommit、完了判定とreport保存を扱う。
- 中断や失敗時の子プロセス停止、rollback、run状態とreportの回収も含む、refactor forkの実行ライフサイクルへの入口。

## Read this when
- refactor fork全体の進行、current run内の未解決所見の管理、処理単位の確定、完了・中断・失敗時の挙動を調べたり変更したりするとき。

## Do not read this when
- レビュー用または変更要約用のagent指示や出力契約だけを調べるときは、それぞれのbuilderを直接読む。
- refactor stateの形式・同期・次の調査対象の選択だけを調べるときは、そのstate管理処理を直接読む。

## hash
- 7542a2e19bf12f229981f05177ab389c957a9bde56273b4d6c4343933d568912
