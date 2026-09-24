# `__init__.py`

## Summary
- realization のリファクタリング作業を扱うパッケージ。関連するリファクタリング処理への入口となる。

## Read this when
- realization のリファクタリング作業の内容や構成を確認するとき。

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき。

## hash
- d070e139f0ebc38e439ff4bf3b37f76a7a536a3424248e4afcc0525de0573746

# `fork.py`

## Summary
- `realization refactor fork` サブコマンドのフルサイクル実行を担う。対象選択、Codex による realization file の調査・修正、変更単位の検証とコミット、未解決 finding の管理、完了判定、joinable run の公開、fork report の保存までを一つの進捗状態で処理する。
- refactor state、run worktree、プロセス追跡、割り込み・失敗時の rollback／error state 更新を連携させるため、refactor fork の実行 lifecycle や cleanup、完了結果の生成を確認したい場合の入口となる。

## Read this when
- realization refactor fork の実行フロー、対象選択から report 保存までの状態遷移を確認したいとき
- refactor unit の agent 呼び出し、変更パス検証、commit、未解決 finding、完了判定の挙動を調べたいとき
- 割り込み・実行失敗・cleanup 失敗時の rollback、run state、エラー報告の処理を確認したいとき

## Do not read this when
- refactor 対象選択や state のデータ操作だけを確認したい場合は、直接 `commons.runtime_refactor` の実装を読むとよい
- 個別の file review／change summary agent に渡すパラメータ定義だけを確認したい場合は、対応する `acp.builder.realization.refactor.fork` の builder を直接読むとよい
- fork report の描画形式だけを確認したい場合は、`commons.runtime_run_report` を直接読むとよい
- realization refactor fork 以外のサブコマンドの実行 lifecycle を調べる場合は、このファイルを入口にしない

## hash
- 7542a2e19bf12f229981f05177ab389c957a9bde56273b4d6c4343933d568912
