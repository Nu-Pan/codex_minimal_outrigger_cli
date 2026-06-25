# `abandon.py`

## Summary
- `cmoc session abandon` の実処理。active session を home branch へ戻し、session state を abandoned に更新して session branch を削除する。
- cleanup 失敗時の state/branch rollback と利用者向けエラーを扱う。

## Read this when
- session abandon の事前条件、branch 切り替え、state 更新、branch 削除、rollback 挙動を確認または変更したいとき。
- session abandon の CLI 出力や cleanup 失敗時の CmocError を追いたいとき。

## Do not read this when
- session fork や session join の処理を確認したいとき。
- SessionState、git helper、branch 判定などの共通 runtime 実装だけを確認したいとき。

# `fork.py`

## Summary
- `cmoc session fork` の実処理。通常 branch から session branch を作成し、session state file を初期化する。
- cmoc-managed branch の拒否、clean worktree 確認、既存 active session 検出、`.cmoc` ignore 確保を扱う。

## Read this when
- session fork の事前条件、session branch 名、session state 初期値、成功時出力を確認または変更したいとき。
- 通常 branch から session branch を開始する lifecycle 前半を追いたいとき。

## Do not read this when
- session join/abandon や merge conflict resolution を確認したいとき。
- Typer への command 登録や CLI option 宣言だけを確認したいとき。

# `join.py`

## Summary
- `cmoc session join` の実処理。active session branch を home branch へ merge し、state を joined に更新して session branch 削除を試みる。
- merge conflict 時は Codex CLI 用 parameter を組み立て、marker/unmerged path の残存確認後に merge commit を完了する。

## Read this when
- session join の事前条件、home branch への merge、state 更新、branch cleanup warning、conflict resolution を確認または変更したいとき。
- session join conflict resolution の Codex 呼び出し境界を追いたいとき。

## Do not read this when
- session fork/abandon の lifecycle を確認したいとき。
- conflict resolution prompt の文面や AgentCallParameter 構築の詳細だけを確認したいとき。

# `__init__.py`

## Summary
- session subcommand package の入口。実処理の再公開や初期化は持たない。

## Read this when
- package としての存在確認だけが必要なとき。

## Do not read this when
- session 各コマンドの実処理を確認したいとき。
