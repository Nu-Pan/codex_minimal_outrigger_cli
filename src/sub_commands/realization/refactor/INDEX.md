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
- realization refactor fork の実行全体を束ね、対象の選択、ファイル単位の調査・修正、finding と refactor state の管理、差分検査と処理単位の commit を扱います。
- 完了・中断・失敗時の状態公開や cleanup、fork report の作成までを担う、refactor fork 固有の実行フローへの入口です。

## Read this when
- refactor fork の進行順序、対象の再調査、未解決 finding の扱い、差分検査や処理単位の確定を調べる・変更するとき。
- fork の完了条件、joinable/error への遷移、中断・失敗時の回復や report 内容を調べる・変更するとき。

## Do not read this when
- CLI コマンドの登録や公開方法を調べるときは、コマンド登録の実装へ進んでください。
- agent に渡す指示や入力パラメーター、出力スキーマの構築を調べる・変更するときは、対応する builder へ進んでください。
- サブコマンド共通の run lifecycle、process tracking、report 作成、refactor state の共通処理を調べる・変更するときは、それぞれの共通 runtime 実装へ進んでください。

## hash
- 4b13eec228054b5d48d9df815607da5f779ad5f87d346fe0df343df8e838b7ab
