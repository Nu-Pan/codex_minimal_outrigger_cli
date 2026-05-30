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

- `src/sub_commands/session/abandon.py` は `cmoc session abandon` の本体実装で、現在の session branch を merge せずに破棄して home branch に戻します。
- `session.state` / `apply.state` の事前検証、`.cmoc` の ignore 保証、home branch への switch、`session.state=abandoned` への更新、session branch の強制削除を扱います。
- cleanup 失敗時は branch/state を再実行しやすい状態へ戻す rollback と、手動復旧を促すエラー整形まで含みます。

## Read this when

- `cmoc session abandon` の実装・修正・レビュー・テストを行うとき。
- session branch を merge せずに破棄する流れや、`session.state` / `apply.state` の前提条件を確認したいとき。
- cleanup 失敗時の rollback や、再実行前に手動で整合を取るべき箇所を確認したいとき。

## Do not read this when

- `cmoc session fork` の作成条件や、active session の重複防止だけを確認したいとき。
- `cmoc session join` の merge 処理や conflict 解消だけを確認したいとき。
- `cmoc apply abandon` など、apply 側の破棄仕様だけを確認したいとき。

## hash

- 48b22231b5a8c15575b449fc037ffbeb0f7a841b8a05e55df5506063996ad615
<!-- cmoc-index-kind: file -->

# `fork.py`

## Summary

- `src/sub_commands/session/fork.py` は `cmoc session fork` の本体実装で、現在 checkout 中の local branch を session home branch とみなし、その HEAD から session branch を作成します。
- detached HEAD、local branch 以外、`cmoc` 管理 branch、未コミット差分、既存 active session を検査し、`.cmoc` の非追跡保証と session state の保存を扱います。
- session 作成の直列化、timestamp ベースの一意な branch 名生成、state 保存失敗時の rollback まで含みます。

## Read this when

- `cmoc session fork` の実装・修正・レビュー・テストを行うとき。
- 現在 checkout 中の local branch を session home branch とみなす条件や、detached HEAD / remote-tracking / commit hash の扱いを確認したいとき。
- active session の重複防止、`.cmoc` の非追跡保証、session branch 名の生成、state 保存失敗時の rollback を確認したいとき。

## Do not read this when

- `cmoc session join` / `cmoc session abandon` / `cmoc apply` 系の終了・破棄・統合だけを確認したいとき。
- branch model 全体や一般的な git 操作だけを確認したいとき。
- session 開始ではなく、session 終了や別コマンドの仕様を確認したいとき。

## hash

- a95a1f2a7b766935b5c1cfb30ee749bfdfa4ee0963a71ad87105f821892f8dad
<!-- cmoc-index-kind: file -->

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

- `cmoc session fork` や `cmoc session abandon` の仕様だけを確認したいとき。
- `cmoc apply` 側の開始・終了・破棄の手順だけを確認したいとき。
- 一般的な `git merge` の説明だけで足り、`session.state` 更新や conflict 解消の実装詳細が不要なとき。

## hash

- a9a7bed03d38ab27825d79fff4759b5a7af4d03d8885a9fe9bd279dd2ce207bf
<!-- cmoc-index-kind: file -->
