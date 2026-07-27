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
- realization refactor fork の一連の実行を担う CLI ランタイム。対象選択、file 単位の Codex 調査・修正、所見と refactor state の更新、処理単位の commit、完了判定、joinable/error 状態および fork report の生成までを同じ進捗状態で管理する。
- realization refactor fork の実行フロー、割り込み・エラー時の cleanup、想定外差分の拒否、unresolved finding の追跡、変更概要の生成を確認するための入口である。

## Read this when
- `cmoc realization refactor fork` の実行フローや lifecycle を変更・調査するとき
- refactor target の選択から処理単位の commit、完了条件、unresolved 管理までを確認するとき
- fork の割り込み、error state、report、差分検証の挙動を確認するとき

## Do not read this when
- refactor state の保存・同期・target 選択そのものを変更するときは、`commons.runtime_refactor` の実装を先に読む
- 単一 realization file の調査・修正用 agent parameter を変更するときは、`file_review_and_fix` の実装を読む
- fork report の共通出力形式だけを確認するときは、`commons.runtime_run_report` の実装を読む

## hash
- 103af2d1b998fe896835630d84e6596c7a4113e5fe63a01e136ea17b8322f559
