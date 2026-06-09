# `__init__.py`

## Summary

- `src/sub_commands/session/__init__.py` は `cmoc session` 系サブコマンドのパッケージ宣言だけを担う最小モジュールです。
- 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- `src/sub_commands/session` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc session` 系サブコマンドの入口となるパッケージ構造を把握したいとき。

## Do not read this when

- 個別の `cmoc session fork/join/abandon` の実行フローや状態遷移を確認したいときは、このファイルではなく各実装モジュールを読むべきです。
- `cmoc session` の仕様断片や利用手順だけを確認したいときは、`oracles/docs/app_specs/sub_commands/` 側を読むべきです。

## hash

- cae1fe2deaf0b783c45fb2b0cb686d48eb34f14259fb35febfc5cb7ed819653a

# `abandon.py`

## Summary

- `src/sub_commands/session/abandon.py` は `cmoc session abandon` の本体実装で、現在 checkout 中の session branch を merge せずに破棄して home branch へ戻します。
- 実行前に現在 branch、session/apply state、記録済み home branch の存在、`.cmoc` の ignore / clean 状態を確認し、必要な退避情報を保持します。
- 失敗時は session state と branch HEAD を元に戻して再実行可能な状態へ復旧し、詳細付きの `CmocError` を投げます。

## Read this when

- `cmoc session abandon` の実装・修正・レビュー・テストを行うとき。
- session branch を merge せずに破棄する前提条件や、`session.state` / `apply.state` の検証条件を確認したいとき。
- `.cmoc` の ignore 保証、home branch への切り替え、session branch 削除、`session.state=abandoned` 更新の順序を追いたいとき。
- cleanup 失敗時の rollback と、再実行前に手動復旧が必要な箇所を確認したいとき。

## Do not read this when

- `cmoc session fork` や `cmoc session join` の開始・統合処理だけを確認したいとき。
- `cmoc apply abandon` など、apply 側の破棄仕様だけを確認したいとき。
- `src/sub_commands/session` パッケージ全体の入口構造だけを確認したいとき。
- `cmoc session abandon` の利用手順ではなく、`oracles/docs/app_specs/sub_commands/session_abandon.md` の仕様断片を直接確認したいとき。

## hash

- 5da92a3340c53316b3b73f9c5d2d60b6603b36ea7c087ad2fc427a1f323db5d4

# `fork.py`

## Summary

- `src/sub_commands/session/fork.py` は `cmoc session fork` の本体実装で、現在 checkout 中の local branch を session home branch として、その HEAD から `cmoc/session/<session-id>` を作成します。
- detached HEAD、local branch 以外、cmoc 管理 branch、未コミット差分、既存 active session を検査し、`.cmoc` の非追跡保証も確認します。
- session 作成はロックで直列化され、timestamp ベースの一意な branch 名を最大 10 回まで試行し、session state の保存失敗時には作成済み branch を rollback します。

## Read this when

- `cmoc session fork` の実装・修正・レビュー・テストを行うとき。
- 現在 checkout 中の local branch を session home branch とみなす条件や、detached HEAD / remote-tracking branch / cmoc 管理 branch の扱いを確認したいとき。
- 未コミット差分の検査、既存 active session の排他、`.cmoc` の非追跡保証を含む事前条件を確認したいとき。
- session branch 名の生成、作成時の直列化、state 保存、保存失敗時の rollback や再試行の流れを追いたいとき。

## Do not read this when

- `cmoc session join` や `cmoc session abandon` の終了・破棄処理だけを確認したいとき。
- `cmoc apply` 系サブコマンドの開始・統合・破棄だけを確認したいとき。
- `src/sub_commands/session` パッケージ全体の入口構造や、一般的な git branch 操作だけを確認したいとき。
- 実装ではなく、`oracles/docs/app_specs/sub_commands/session_fork.md` の仕様断片だけを確認したいとき。

## hash

- 1d8f03df4976dc975e2982a0864d5e953404d961a93544b2ae69743ca57df07c

# `join.py`

## Summary

- `src/sub_commands/session/join.py` は `cmoc session join` の本体実装で、現在の session branch を記録済みの session home branch に `git merge --no-ff` で取り込みます。
- session / apply state の検証、現在 branch と home branch の確認、`.cmoc` の ignore 確認、merge 後の state 更新と branch 削除までをまとめて扱います。
- merge conflict が起きた場合は Codex CLI に conflict marker 解消を依頼し、解消後の整合性確認と merge commit 作成まで後始末します。

## Read this when

- `cmoc session join` の前提条件、merge 手順、conflict 解消、完了後の後始末を実装・修正・レビュー・テストしたいとき。
- `session.state` / `apply.state` の検証条件や、記録済みの session home branch の復元・存在確認を追いたいとき。
- `.cmoc` の ignore 保証、Codex CLI への conflict marker 解消依頼、merge 後の `session.state=joined` 更新と安全な branch 削除条件を確認したいとき。

## Do not read this when

- `cmoc session fork` や `cmoc session abandon` の開始・破棄フローだけを確認したいとき。
- `cmoc apply` 系の実装や状態遷移だけを確認したいとき。
- `src/sub_commands/session` ディレクトリ全体の入口構造だけを確認したいとき。
- `cmoc session join` の正本仕様断片だけを確認したいときは、`oracles/docs/app_specs/sub_commands/session_join.md` を読むべきとき。

## hash

- 269614e01176dbff82033544cd0cdf233ba03e618f49f262d6e2e6fb1492e5ee
