# `cmoc session abandon`

## 概要

- `cmoc session abandon` は、現在の `{{cmoc-session-branch}}` を `{{cmoc-session-home-branch}}` に merge せず破棄する。
- session を完了させる `cmoc session join` とは異なり、session の成果物を本流へ取り込まない。
- `cmoc session join` 済みの結果を取り消す rollback コマンドではない。
- cmoc 管理下の session を破棄する正規の手段であり、ユーザーが手作業で `{{cmoc-session-branch}}` を削除する代わりに使う。

## 引数

- 引数なし

## 事前条件

`cmoc session abandon` は `{{cmoc-session-branch}}` 上でのみ実行できる。

以下の場合はエラー終了する。

- 現在のブランチが `{{cmoc-session-branch}}` ではない
- 対応する `{{cmoc-session-state-file}}` が存在しない
- 対応する `{{cmoc-session-state-file}}` の `session.state` が `active` ではない
- 対応する `{{cmoc-session-state-file}}` の `run.state` が `ready` ではない
    - 未 join の編集 run が残っている場合は、先に `cmoc run abandon` で破棄する
- `{{cmoc-session-home-branch}}` が存在しない
- `{{cmoc-session-branch}}` 側の worktree に git 未コミット差分が存在する

## 破棄対象

`cmoc session abandon` は以下を破棄してよい。

- `{{cmoc-session-branch}}`
- `{{cmoc-session-branch}}` 上にだけ存在する commit
- `{{cmoc-session-branch}}` 上で行われた oracle 改訂
- `{{cmoc-session-branch}}` 上で行われた実装修正

`cmoc session abandon` は以下を破棄してはいけない。

- `{{cmoc-session-home-branch}}`
- `{{cmoc-session-home-branch}}` 上の commit
- `{{cmoc-session-state-file}}` 自体
- 既に保存済みの report
- 未 join の編集 run
    - editing run が残っている場合は `cmoc session abandon` では処理せず、`cmoc run abandon` を要求する

## 実行手順

1. doctor preprocess を呼び出す
2. 事前検証
    - 事前条件を満たしている事を確認する
3. クリーンアップ
    1. `git switch {{cmoc-session-home-branch}}` を実行する。
    2. `{{cmoc-session-state-file}}` の `session.state` を `abandoned` に更新する。
    3. `{{cmoc-session-branch}}` を強制削除する。
4. 破棄と cleanup の結果を terminal result のサブコマンド固有結果として表示する。

## 状態遷移

- `cmoc session abandon` が正常終了した場合、`session.state` は `abandoned` になる。
- `abandoned` になった session は active session ではない。
- したがって、同じ `{{cmoc-session-home-branch}}` から新しい `cmoc session fork` を実行してよい。

## クリーンアップの途中で失敗した場合

- クリーンアップで行った操作をロールバックし、再実行可能な状態にする
- ユーザーに「問題の手動解決したうえで `cmoc session abandon` 再実行」を促す

## primary report

- `natural_completion` と `error` のすべての終了経路で、session abandon 実行要約を primary report として保存する。doctor preprocess または事前条件で終了した場合も対象とする。
- report は Markdown と YAML Front Matter で構成し、`{{repo-root}}/.cmoc/gu/ar/report/session/abandon/{{time-stamp}}.md` に保存する。
- front matter には、command、生成日時、repo root、terminal result の共通分類、終了コード、session branch、home branch、破棄対象 branch の開始時 HEAD commit、および session state の実行前後の値を含める。確定できなかった値は `null` とする。
- 本文には、破棄対象、branch 切替、state 遷移、branch 削除と cleanup、失敗時の rollback または残存資源、warning またはエラー、必要な次の操作、および関連する診断用サブコマンドログを要約する。
