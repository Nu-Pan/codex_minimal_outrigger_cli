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

- `src/sub_commands/session/abandon.py` は `cmoc session abandon` の本体処理で、現在の session branch を merge せず破棄して home branch に戻します。
- 事前条件の検証、`session.state` と `apply.state` の確認、`.cmoc` が ignore 対象であることの保証、branch 切り替え、session state の `abandoned` 更新、session branch の強制削除、失敗時の rollback を扱います。
- cleanup に失敗した場合は、再実行しやすい状態へ戻す rollback と、利用者へ手動復旧を促す `CmocError` の整形まで含みます。

## Read this when

- `cmoc session abandon` の実装・修正・レビュー・テストを行いたいとき。
- session branch を merge せずに破棄する流れや、`session.state` と `apply.state` の前提条件を確認したいとき。
- cleanup 失敗時の rollback や、再実行前に手動で整合を取るべき箇所を確認したいとき。

## Do not read this when

- `cmoc session fork` の作成手順や active session の競合回避だけを確認したいとき。
- `cmoc session join` の merge 処理や conflict 解消だけを確認したいとき。
- `cmoc apply abandon` など、apply run 側の破棄仕様だけを確認したいとき。

## hash

- 7d65a039f9fe0c4bc6376396290a92051ab9e7041b039bacc83c58e13f6b1fa6

# `fork.py`

## Summary

- `cmoc session fork` の本体処理を実装するモジュールです。
- 現在 checkout している local branch の HEAD を起点に session branch を作成し、session state を記録します。
- detached HEAD、cmoc 管理 branch、未コミット差分、既存 active session を検査し、`.cmoc` の非追跡保証、session branch の一意作成、保存失敗時の rollback までを扱います。

## Read this when

- `cmoc session fork` の実装・修正・テスト・レビューを行うとき。
- 現在 checkout 中の local branch を session home branch とみなす条件や、session branch 名の生成・作成手順を確認したいとき。
- active session の重複防止、`.cmoc` の非追跡保証、session state の保存、失敗時の rollback や再試行挙動を確認したいとき。

## Do not read this when

- `cmoc session join` や `cmoc session abandon` の終了・統合・破棄手順だけを確認したいとき。
- `cmoc apply` 系の開始条件や apply branch / worktree の扱いだけを確認したいとき。
- branch model 全体や一般的な git 操作の説明だけで足りるとき。

## hash

- fe6da28add467a18855905a82c0007d6d3baba995fe4b6056a894125515bb9ea

# `join.py`

## Summary

- `src/sub_commands/session/join.py` は `cmoc session join` の本体処理を実装するモジュールです。
- session state の検証、`<cmoc-session-home-branch>` への `git merge --no-ff`、conflict 解消依頼、`session.state` の `joined` 更新と branch cleanup を扱います。

## Read this when

- `cmoc session join` の実装・修正・レビューで、事前条件と実行順を確認したいとき。
- session branch を home branch に merge し、`session.state` を `joined` に更新する処理を追いたいとき。
- merge conflict の解消依頼、`.cmoc` の非追跡保証、後始末としての branch 削除条件を確認したいとき。

## Do not read this when

- `cmoc session fork` の開始条件や session branch 作成だけを確認したいとき。
- `cmoc session abandon` の破棄手順だけを確認したいとき。
- `cmoc apply` 系の実行条件や一般的な `git merge` の説明だけで足りるとき。

## hash

- 7a093ee1dc89fa8e88e1a96399c64f0d62234363dc0ac1828c93764ffebf8718
