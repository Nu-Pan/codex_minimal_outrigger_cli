# cmoc branch model

## 概要

cmoc は、通常の `<local-branch>` から `<cmoc-session-branch>` を作り、必要に応じて `<cmoc-session-branch>` から `<cmoc-apply-branch>` を作る。

`<repository-default-branch>` は特別扱いしない。
ユーザーが `cmoc session fork` を実行した時点で checkout している `<local-branch>` をその session の `<cmoc-session-home-branch>` とする。

## branch の種類

### `<repository-default-branch>`

- 典型的には `main` / `master` などのこと。

### `<local-branch>`

- cmoc 管理ではない通常の git local branch。

### `<remote-tracking-branch>`

- cmoc 管理ではない通常の remote-tracking branch。

### `<cmoc-session-home-branch>`

- `cmoc session fork` を実行した時点で checkout されていた `<local-branch>`。
- session の分岐元であり、最終的な merge 先でもある。

### `<cmoc-session-branch>`

- `cmoc session fork` が作成する cmoc 管理 branch。
- 命名規則は `cmoc/session/<session-id>`
- ユーザーはこの branch 上で oracles を編集・コミットし、`cmoc eval-oracles` や `cmoc apply` を呼び出す。

### `<cmoc-apply-branch>`

- `cmoc apply` が 1 回の apply 実行ごとに作成する cmoc 管理 branch。
- 命名規則は `cmoc/apply/<session-id>/<apply-run-id>`
- Codex CLI による実装修正 commit はこの branch に積む。
- ユーザーが oracle 改訂作業を行う場所ではない。

### `<cmoc-managed-branch>`

- cmoc が管理する branch の総称。
- `<cmoc-session-branch>`, `<cmoc-apply-branch>` の上位概念。

## session の原則

- 1 つの `<cmoc-session-home-branch>` に対して active な `<cmoc-session-branch>` は高々 1 つとする。
- detached HEAD, `<remote-tracking-branch>`, commit hash, `<cmoc-managed-branch>` は `<cmoc-session-home-branch>` として扱わない。

## apply の snapshot 原則

- `cmoc apply` は、開始時点の `<cmoc-session-branch>` HEAD を `<oracle-snapshot-commit>` として固定し、その snapshot から `<cmoc-apply-branch>` を作成する。
- apply 開始後に `<cmoc-session-branch>` が進んでも、実行中の apply はその変更を取り込まない。
- apply の収束・未収束判定は `<oracle-snapshot-commit>` に対する判定である。

## `<cmoc-session-state-file>`

## 概要

- cmo セッションの最新の状態を記録する json ファイル
- 保存先は `<repo-root>/.cmoc/sessions/<session-id>.json`
- `<cmoc-session-branch>`, `<cmoc-apply-bramch>` の状態遷移のための補助情報として用いる

## スキーマ定義

```json
{
  "session": {
    "schema_version": 1,
    "session_id": "...",
    "session_branch": "cmoc/session/...",
    "session_home_branch": "...",
    "session_start_commit": "...",
    "state": "active | joined | abandoned | error",
    "created_at": "...",
    "joined_at": null
  },
  "apply": {
    "schema_version": 1,
    "apply_id": "...",
    "apply_branch": "cmoc/apply/.../...",
    "apply_worktree": "...",
    "oracle_snapshot_commit": "...",
    "session_head_at_apply_start": "...",
    "session_head_before_merge": "...",
    "apply_head_before_merge": "...",
    "session_head_after_merge": "...",
    "merge_commit": "...",
    "state": "ready | running | completed | error",
    "session_advanced_during_apply": true,
    "session_advanced_paths_kind": "oracles_only | oracles_not_included | none"
  }
}
```
