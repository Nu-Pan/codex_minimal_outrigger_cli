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
- 事前条件の検証、`session.state` と `apply.state` の確認、`.cmoc` が ignore 対象であることの保証、branch 切り替え、session state の `abandoned` 更新、session branch の強制削除を扱います。
- cleanup に失敗した場合は、再実行しやすい状態へ戻す rollback と、利用者へ手動復旧を促すエラー整形まで含みます。

## Read this when

- `cmoc session abandon` の実装・修正・レビュー・テストを行いたいとき。
- session branch を merge せずに破棄する流れや、`session.state` と `apply.state` の前提条件を確認したいとき。
- cleanup 失敗時の rollback や、再実行前に手動で整合を取るべき箇所を確認したいとき。

## Do not read this when

- `cmoc session fork` の作成条件や、active session の重複防止だけを確認したいとき。
- `cmoc session join` の merge 処理や conflict 解消だけを確認したいとき。
- `cmoc apply abandon` など、apply 側の破棄仕様だけを確認したいとき。

## hash

- a552bb18cc7eb190fea9f3ed5d0b642a952c071315cf1379e8ff99d49b374b04

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
- 現在の session branch が join 可能であることを検証し、session home branch へ `git merge --no-ff` します。
- conflict が起きた場合は Codex CLI に marker 解消を依頼し、`session.state` 更新と branch 削除可否判定まで行います。

## Read this when

- `src/sub_commands/session/join.py` の処理順、事前条件、後始末を実装・修正・レビュー・テストしたいとき。
- `session.state` と `apply.state` の検証、`git merge --no-ff`、conflict 時の Codex CLI 依頼の流れを確認したいとき。
- merge 後の `session` 反映、`oracles` を含む conflict marker の扱い、安全な session branch 削除条件を追いたいとき。

## Do not read this when

- `cmoc session fork` や `cmoc session abandon` の実装・修正・レビューだけを確認したいとき。
- `cmoc apply` 系の開始・終了・破棄の流れだけを確認したいとき。
- 一般的な `git merge` の説明だけで足り、`session.state` 更新や conflict 解消の実装詳細が不要なとき。

## hash

- 61f4b42440c3fda5ead506427f77739e3c6008309da010ff51e4ade2c87317a9
