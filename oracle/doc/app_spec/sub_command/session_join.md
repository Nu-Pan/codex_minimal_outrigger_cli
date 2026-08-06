# `cmoc session join`

## 概要

- `cmoc session join` は、session を完了して `{{cmoc-session-home-branch}}` へ戻すためのコマンドである。
- i.e. `cmoc session join` は、現在 checkout している `{{cmoc-session-branch}}` を `{{cmoc-session-home-branch}}` へ merge する。
- 通常の git branch 同士の汎用 merge wrapper ではない。
- `{{repository-default-branch}}` は特別扱いしない。

## 引数

- 引数なし
- merge source も merge target も引数では受け取らない

## 事前条件

以下の場合はエラー終了する。

- 現在のブランチが `{{cmoc-session-branch}}` ではない
- 対応する `{{cmoc-session-state-file}}` が存在しない
- 対応する `{{cmoc-session-state-file}}` の `session.state` が `active` ではない
- 対応する `{{cmoc-session-state-file}}` の `run.state` が `ready` ではない
- 対応する `{{cmoc-session-state-file}}` から `{{cmoc-session-home-branch}}` を特定出来ない
- `{{cmoc-session-branch}}` 側の worktree に git 未コミット差分が存在する

## 実行手順

1. doctor preprocess を呼び出す
2. 事前検証
    - 事前条件を満たしている事を確認する
3. マージ処理
    1. `git switch {{session-home-branch}}` を実行する
    2. `git merge --no-ff {{cmoc-session-branch}}` を実行する
    3. conflict が発生した場合は、Codex CLI に conflict marker 解消を依頼する
4. 後始末
    1. `{{cmoc-session-state-file}}` の `session.state` を `joined` にする
    2. 安全に削除できる場合のみ `{{cmoc-session-branch}}` を削除する

## `{{cmoc-session-home-branch}}` が進んでいた場合

`{{cmoc-session-home-branch}}` が session 作成後に進んでいてもエラーにはしない。
`cmoc session join` は、実行時点の `{{cmoc-session-home-branch}}` HEAD に `{{cmoc-session-branch}}` を merge する。

merge conflict が発生した場合は通常の conflict として扱う。

## `git merge` がコンフリクトした場合

### tracked feedback state の優先処理

- `{{work-root}}/.cmoc/gt/ar/feedback` 内の conflict は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の append-only record 規則を先に適用する。
- 同じ path の内容が byte-for-byte で同一なら 1 件へ統合してよい。
- 同じ path の内容が異なる場合は、observation、normalization result、または human disposition を失う可能性があるため、自動解決せず merge を中止する。
- divergent な feedback record を conflict marker 解消用 agent call へ渡してはならない。

### 解決手順

1. cmoc は conflict 対象ファイルを列挙する
2. conflict marker 解消用の agent call を行う
3. cmoc は conflict marker が残っていない事を確認する
4. cmoc は conflict 対象ファイルを `git add` する
5. unmerged path が残っていないことを確認する
6. cmoc が merge commit を作成する

## conflict marker 解消用の agent call

- この agent call の詳細仕様は `build_session_join_conflict_resolution_parameter` を正本とする
- この agent call は `{{work-root}}` に対する編集操作を伴うため、必ず直列に実行すること
- builder は `build_conflict_resolution_standard` の規範だけを conflict 解消用規範として固定で prompt へ注入する
- oracle edit、oracle review、または realization refactor のための規範を conflict 解消へ転用してはいけない

### oracle file 規則と conflict 解消の優先順位

- conflict 対象 oracle file は、marker 解消に必要な範囲だけ例外的に編集してよい
- conflict 解消後も oracle file は realization file の正本であり、realization file の都合に合わせて oracle file の意味を変更してはいけない
- conflict marker の解消に不要な仕様変更、実装改善、または別 file の変更を行ってはいけない

## その他、コマンドが想定外に失敗した場合

- その時点で処理を打ち切り、ロールバック等はしない
- 手動解決が必要な事を stderr 経由でユーザーに知らせる

## `{{cmoc-managed-branch}}` 削除の条件

- 安全であること（ブランチ削除により作業結果が失われないこと）の裏付けが取れた場合のみ `{{cmoc-session-branch}}` の削除を実行する
- 確認に失敗した場合 `{{cmoc-managed-branch}}` は削除せず、 warning 扱いでユーザーに通知して続行する
