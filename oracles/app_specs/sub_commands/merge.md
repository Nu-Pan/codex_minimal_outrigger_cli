# `cmoc merge`

## 概要

`cmoc merge` は、現在 checkout している `<cmoc-session-branch>` を、その session metadata に記録された `<cmoc-session-home-branch>` へ merge する。

`cmoc merge` は、session を完了して `<cmoc-session-home-branch>` へ戻すためのコマンドである。
通常の git branch 同士の汎用 merge wrapper ではない。

`<repository-default-branch>` は特別扱いしない。
merge 先は常に session metadata の `<cmoc-session-home-branch>` である。

## 引数

- 引数なし
- merge source も merge target も引数では受け取らない

## 事前条件

`cmoc merge` は `<cmoc-session-branch>` 上でのみ実行できる。

以下の場合はエラー終了する。

- 現在 branch が `<cmoc-session-branch>` ではない
- git 未コミット差分が存在する
- session metadata が存在しない
- session metadata の `state` が `active` ではない
- metadata に記録された `<cmoc-session-home-branch>` が存在しない
- `<cmoc-session-home-branch>` が `<cmoc-managed-branch>` である
- 同じ session に、現在の `<cmoc-session-branch>` へ未統合の `<cmoc-apply-branch>` が存在する

## 実行手順

1. 現在 branch から `<session-id>` を取得する
2. `.cmoc/sessions/<session-id>/session.json` を読む
3. metadata から `<cmoc-session-home-branch>` を取得する
4. `<repo-root>/.cmoc` が git の追跡対象外であることを保証する
5. `git switch <session-home-branch>` を実行する
6. `git merge --no-ff <cmoc-session-branch>` を実行する
7. conflict が発生した場合は、Codex CLI に conflict marker 解消を依頼する
8. merge が完了したら session metadata の `state` を `merged` にする
9. 安全に削除できる場合のみ `<cmoc-session-branch>` を削除する

## `<cmoc-session-home-branch>` が進んでいた場合

`<cmoc-session-home-branch>` が session 作成後に進んでいてもエラーにはしない。
`cmoc merge` は、実行時点の `<cmoc-session-home-branch>` HEAD に `<cmoc-session-branch>` を merge する。

merge conflict が発生した場合は通常の conflict として扱う。

## `git merge` がコンフリクトした場合

### 解決手順

1. cmoc は Codex CLI に conflict marker 解消を依頼する
2. Codex CLI には `git add` と `git commit` を禁止する
3. cmoc は conflict marker が残っていないことを確認する
4. cmoc は conflict 対象ファイルを `git add` する
5. unmerged path が残っていないことを確認する
6. cmoc が merge commit を作成する

### 編集禁止ルールとコンフリクト解決の優先順位

例えば `<repo-root>/oracles` は AI 編集禁止領域であるが、同時にコンフリクト解決の対象にもなりうる。
そういった、編集禁止ルールとコンフリクト解決のための編集が衝突した場合、コンフリクト解決を優先して良い。

ただし、Codex CLI に依頼する作業は conflict marker の解消に限定する。
仕様内容の意味的な改訂や、conflict 対象外の oracle 編集は禁止する。

## その他、コマンドが想定外に失敗した場合

- その時点で処理を打ち切り、ロールバック等はしない
- 手動解決が必要な事を stderr 経由でユーザーに知らせる

## `<cmoc-managed-branch>` 削除の条件

- 安全であること（ブランチ削除により作業結果が失われないこと）の裏付けが取れた場合のみ `<cmoc-session-branch>` の削除を実行する
- 確認に失敗した場合 `<cmoc-managed-branch>` は削除せず、 warning 扱いでユーザーに通知して続行する
