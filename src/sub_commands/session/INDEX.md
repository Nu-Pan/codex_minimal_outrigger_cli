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

- `src/sub_commands/session/abandon.py` は `cmoc session abandon` の本体実装で、現在の session branch を merge せずに破棄し、home branch へ戻す処理を担います。
- `session.state` と `apply.state` の前提条件を検証し、`.cmoc` の ignore 保証、home branch への switch、session branch の削除、`session.state=abandoned` への更新を順に実行します。
- cleanup 失敗時は rollback で branch と state を再実行しやすい状態へ戻し、手動復旧を促すエラーを整形します。

## Read this when

- `cmoc session abandon` の実装・修正・レビュー・テストを行うとき。
- session branch を merge せずに破棄する前提条件や、`session.state` / `apply.state` の検証条件を確認したいとき。
- .cmoc の ignore 保証、home branch への switch、`session.state=abandoned` の更新、session branch の強制削除の順序を追いたいとき。
- cleanup 失敗時の rollback や、再実行前に手動で整合を取るべき箇所を確認したいとき。

## Do not read this when

- `cmoc session fork` の作成条件や active session の重複防止だけを確認したいとき。
- `cmoc session join` の merge 処理や conflict 解消だけを確認したいとき。
- `cmoc apply abandon` など、apply 側の破棄仕様だけを確認したいとき。
- `src/sub_commands/session` パッケージ全体の役割や `__init__.py` だけを確認したいとき。

## hash

- c7c43e136ef9dba82d64c4ebf89d1d4af3b24f40d8de1a6cdd99ffe4843515c4
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

# `join.py`

## Summary

- src/sub_commands/session/join.py は cmoc session join の本体実装で、session branch を join 可能か検証して home branch へ merge する。
- session.state / apply.state の確認、.cmoc の ignore 保証、git switch と git merge --no-ff の実行、merge 後の state 更新と branch 削除可否判定を扱う。
- merge conflict 時は Codex CLI に conflict marker の解消を依頼し、禁止領域や oracles の扱いを制御したうえで手動復旧が必要な場合を案内する。

## Read this when

- src/sub_commands/session/join.py の処理順、前提条件、後始末を実装・修正・レビュー・テストしたいとき。
- session.state と apply.state の検証、git merge --no-ff、conflict 時の Codex CLI 依頼と merge 復旧の流れを確認したいとき。
- merge 後の session 反映、oracles を含む conflict marker の扱い、安全な session branch 削除条件を追いたいとき。

## Do not read this when

- cmoc session fork や cmoc session abandon の仕様だけを確認したいとき。
- cmoc apply 系の開始・終了・破棄の流れだけを確認したいとき。
- 一般的な git merge の説明だけで足り、session.state 更新や conflict 解消の実装詳細が不要なとき。

## hash

- 3795ab267af95849b2e58b851d68371b21daa19c47b2b9f412cda213f9c448f7
