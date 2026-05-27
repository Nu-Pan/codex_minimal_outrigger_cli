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

- `src/sub_commands/session/abandon.py` は `cmoc session abandon` の本体処理を実装します。
- 現在の session branch が active で、apply.state が ready で、home branch が存在し、未コミット差分がないことを確認したうえで、session branch を merge せず破棄します。
- cleanup では home branch へ switch し、session.state を `abandoned` に更新して session branch を強制削除します。失敗時は state と branch を元に戻して再実行可能な状態にします。

## Read this when

- `cmoc session abandon` の実装・修正・テスト・レビューを行いたいとき。
- 現在ブランチの判定、session/apply state の前提条件、cleanup 失敗時の rollback 仕様を確認したいとき。

## Do not read this when

- `cmoc session fork` や `cmoc session join` の挙動だけを追いたいとき。
- `cmoc apply abandon` など、apply 側の破棄仕様だけを確認したいとき。

## hash

- 8984fd00d2520da960f140181aea341ab7135fc30b1e6afdbbdd4e8848a4160b

# `fork.py`

## Summary

- `cmoc session fork` の本体処理を実装します。
- 現在 checkout している local branch を session home branch とみなし、その `HEAD` から session branch を作成します。
- detached HEAD、cmoc 管理 branch、未コミット差分、既存 active session などの前提条件を検証します。
- `.cmoc` の ignore 確認、session branch の作成、session state の記録、失敗時の rollback までを扱います。

## Read this when

- `cmoc session fork` の実装・修正・テスト・レビューを行いたいとき。
- 新しい session branch の作成条件、`HEAD` の判定、active session の重複防止を確認したいとき。
- `.cmoc` の非追跡保証、session state の保存、失敗時の rollback を確認したいとき。
- session branch 名の生成や、timestamp 衝突時のリトライ挙動を確認したいとき。

## Do not read this when

- `cmoc session join`、`cmoc session abandon`、`cmoc apply` など、別サブコマンドの挙動だけを確認したいとき。
- session の終了や破棄、マージ後処理だけを確認したいとき。
- branch model 全体や一般的な git 操作の説明だけで足りるとき。

## hash

- 4f3b2291933f066fdb59a552059dbea15716aa00a0e66e4a7bef8bea08a52a2b

# `join.py`

## Summary

- `cmoc session join` の本体処理を実装するモジュールです。
- session state の検証、session home branch への `git merge --no-ff`、conflict 解消依頼、`session.state` 更新と branch cleanup を扱います。

## Read this when

- `cmoc session join` の実装・修正・レビューで、事前条件と実行順を確認したいとき。
- session branch を home branch に merge し、`session.state` を `joined` に更新する処理を追いたいとき。
- merge conflict の解消依頼、禁止領域の扱い、後始末としての branch 削除条件を確認したいとき。

## Do not read this when

- `cmoc session fork` の開始手順や session branch の作成だけを確認したいとき。
- `cmoc session abandon` の破棄手順だけを確認したいとき。
- `cmoc apply` 系の実行条件や apply branch の扱いだけを確認したいとき。
- 一般的な git merge の解説だけで足りるとき。

## hash

- 19c5e2e95ccbb157773ce8038ea34bd1c55f42596e98e4ba1364a8c8ce9b7b08
