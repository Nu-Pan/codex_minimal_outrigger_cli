# `__init__.py`

## Summary

- `src/sub_commands/session/__init__.py` は `cmoc session` 系サブコマンドのパッケージ宣言だけを担う最小モジュールです。
- 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- `src/sub_commands/session` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc session` 系サブコマンドの入口となるパッケージ構造を把握したいとき。

## Do not read this when

- 個別の `cmoc session fork/join/abandon` の実行フローや状態遷移を確認したいときは、このファイルではなく各実装モジュールを読むべきです。
- `cmoc session` の仕様断片や利用手順だけを確認したいときは、`oracles/app_specs/sub_commands/` 側を読むべきです。

## hash

- cae1fe2deaf0b783c45fb2b0cb686d48eb34f14259fb35febfc5cb7ed819653a

# `abandon.py`

## Summary

- `src/sub_commands/session/abandon.py` は `cmoc session abandon` の本体処理を実装する。
- 現在の session branch が active で、apply.state が ready で、home branch が存在し、未コミット差分がないことを確認したうえで、session branch を merge せず破棄する。
- cleanup では home branch へ switch し、session.state を `abandoned` に更新して session branch を強制削除し、失敗時は state と branch を元に戻して再実行可能な状態にする。

## Read this when

- `cmoc session abandon` の実装・修正・テスト・レビューを行いたいとき。
- 現在の branch 判定、session/apply state の前提条件、cleanup 失敗時の rollback 仕様を確認したいとき。
- session branch を merge せず破棄する実行フローと、`abandoned` への状態遷移を追いたいとき。

## Do not read this when

- `cmoc session fork` の開始手順や session branch の作成だけを確認したいとき。
- `cmoc session join` のマージ手順や完了処理だけを確認したいとき。
- `cmoc apply abandon` など、apply 側の破棄仕様だけを確認したいとき。

## hash

- 6c5a7669f7a031c1a3a6a612a65cd074f6905b7db4a8c77259b481dc3c5bc985

# `fork.py`

## Summary

- `cmoc session fork` の本体処理を実装するモジュールです。
- 現在 checkout している local branch を session home branch とみなし、その HEAD から session branch を作成します。
- detached HEAD、cmoc 管理 branch、未コミット差分、既存 active session などの事前条件チェックを扱います。
- `.cmoc` の非追跡保証、session branch の一意作成、session state の記録、失敗時の rollback までを含みます。

## Read this when

- `cmoc session fork` の実装・修正・テスト・レビューを行うとき。
- 新しい session branch の作成条件や、現在 checkout 中の local branch の扱いを確認したいとき。
- active session の重複防止や、`.cmoc` の追跡対象外保証、state 保存と rollback の流れを確認したいとき。
- session branch 名の生成や、timestamp 衝突時のリトライ挙動を確認したいとき。

## Do not read this when

- `cmoc session join` や `cmoc session abandon` の終了・統合・破棄手順だけを確認したいとき。
- `cmoc apply` 系の実行条件や apply branch の扱いだけを確認したいとき。
- branch model 全体や一般的な git 操作の説明だけで足りるとき。

## hash

- b16a9771b9753164ced9d20d2b579b322f01b01e9b080faf4a297fc73bcd03e3

# `join.py`

## Summary

- `src/sub_commands/session/join.py` は `cmoc session join` の本体処理を実装するモジュールです。
- session state の検証、session home branch への `git merge --no-ff`、conflict 解消依頼、`session.state` 更新と branch cleanup を扱います。

## Read this when

- `cmoc session join` の実装・修正・レビューで、事前条件と実行順を確認したいとき。
- session branch を home branch に merge し、`session.state` を `joined` に更新する処理を追いたいとき。
- merge conflict の解消依頼、禁止領域の扱い、後始末としての branch 削除条件を確認したいとき。

## Do not read this when

- `cmoc session fork` の開始条件や session branch 作成だけを確認したいとき。
- `cmoc session abandon` の破棄手順だけを確認したいとき。
- `cmoc apply` 系の実行条件や apply branch の扱いだけを確認したいとき。
- 一般的な `git merge` の解説だけで足りるとき。

## hash

- 12f2627f684bf392d24d438bcb88aeb57c76553f4ba583a468ba9e1be1b1965b
