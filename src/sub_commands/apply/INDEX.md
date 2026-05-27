# `__init__.py`

## Summary

- - `src/sub_commands/apply/__init__.py` は `cmoc apply` 系サブコマンドのパッケージ宣言だけを担う最小モジュールです。
- - 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- - `src/sub_commands/apply` が Python パッケージとして宣言されていることを確認したいとき。
- - `cmoc apply` 系サブコマンドの入口となるパッケージ構造を把握したいとき。

## Do not read this when

- - 個別の `cmoc apply fork/join/abandon` の実行フローや状態遷移を確認したいときは、このファイルではなく各実装モジュールを読むべきです。
- - `cmoc apply` の仕様断片や利用手順だけを確認したいときは、`oracles/app_specs/sub_commands/` 側を読むべきです。

## hash

- 5646cb02b7ca8e507d8725e2d5f87e9580881d66ce1a67505595830d53c239d6

# `abandon.py`

## Summary

- `cmoc apply abandon` の本体処理を実装します。
- apply worktree と apply branch を削除し、session state の `apply.state` を `ready` に戻します。

## Read this when

- `cmoc apply abandon` の実装・修正・レビュー・テストを行いたいとき。
- 未 join の apply run を破棄する前提条件、cleanup 対象、`apply.state` の更新、warning の扱いを確認したいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正ループや要修正点一覧の生成だけを確認したいとき。
- `cmoc apply join` や `cmoc session abandon` など、別サブコマンドの終了・統合手順だけを確認したいとき。

## hash

- b1aeea9d255ad377da593edfd71750a2c0351cb774026e2d5715ccb11078e083

# `fork.py`

## Summary

- `cmoc apply fork` の本体処理を実装するモジュールです。
- session state の前提条件検証から、apply branch / worktree の作成、要修正点の調査・改善反復、コミット、レポート出力までを扱います。
- Structured Output の検証、対象ファイル列挙、禁止領域チェック、apply report の YAML Front Matter 付与も含みます。

## Read this when

- `cmoc apply fork` の全体フローを実装・修正・レビューしたいとき。
- session state の検証、apply branch / worktree の作成、調査・修正ループ、report 保存の流れを確認したいとき。
- 部分適用・全体適用の切り替え、要修正点リストの改善、コミットや状態遷移の責務を整理したいとき。

## Do not read this when

- `cmoc apply join` や `cmoc apply abandon` の挙動だけを確認したいとき。
- `cmoc session fork/join/abandon` など、apply 以外のサブコマンドだけを追いたいとき。
- `cmoc apply fork` のレポート生成や要修正点調査ではなく、別ファイルの共通基盤だけを見たいとき。

## hash

- 005e484ce657980d05fd0d3afdfde49f833bbaa81b1115af66d7386c3d138eae

# `join.py`

## Summary

- `src/sub_commands/apply/join.py` は `cmoc apply join` の本体処理を実装します。
- 完了済み apply branch を session branch に取り込み、想定外差分の検出・強制復旧・merge conflict の報告・state 更新・後始末までを扱います。

## Read this when

- `cmoc apply join` の実装・修正・レビューで、処理順と例外条件を確認したいとき。
- 想定外差分の通常モードと `--force-resolve` の分岐、`session.state` / `apply.state` の更新条件を確認したいとき。
- merge 後の apply branch と apply worktree の削除条件、warning の出し方を確認したいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正ループやレポート保存の仕様だけを確認したいとき。
- `cmoc apply abandon` の破棄手順や cleanup 条件だけを確認したいとき。
- `cmoc session join` など session 側の統合手順だけを確認したいとき。

## hash

- 873ce192533a75fbd927b6531ea8bc5aaa6d04d067c1e8e7207ee57f5de7fa66
