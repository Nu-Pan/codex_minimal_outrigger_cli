
# サブコマンド実行作業隔離規則

## 概要

- comc サブコマンドが実際に実行する作業のことを run と呼ぶ
- この run が他の何者か（大抵は人間）の操作と衝突しないように、cmoc は作業環境の隔離を行う
- 具体的には作業用に git branch, worktree を利用する

## 前提

- comc サブコマンド呼び出し 1 つに対して run 1 つが存在する
- `{{repo-root}}` は git で管理されている
- 人間が直接触るのは `{{repo-root}}` だけである
- 人間が `{{run-root}}` を直接触ることはない
- `{{cmoc-session-branch}}` 上では他の何者かがコミットを積み上げる可能性がある

## git branch

- run 開始時点での `{{cmoc-session-branch}}` HEAD を元に `{{cmoc-run-branch}}` を作成する
- `{{cmoc-run-branch}}` は抽象概念であり、具体的なブランチ名はサブコマンドによって異なる
    - e.g. `cmoc review oracle` --> `{{cmoc-review-branch}}`
    - e.g. `cmoc apply fork` --> `{{cmoc-apply-branch}}`
- run の作業は全て `{{cmoc-run-branch}}` 上で記録される
- run の作業完了後の `{{cmoc-run-branch}}` --> `{{cmoc-session-branch}}` マージ規則
    - サブコマンドによって、マージ規則は異なる
    - e.g. `cmoc apply join` により、半自動ワークフローで慎重にマージされる
    - e.g. `cmoc review oracle` により自動でマージされる

## git worktree

- cmoc の run 作業は、必ず `{{cmoc-run-worktree}}` 上で行う
- `{{cmoc-run-worktree}}` は抽象概念であり、具体的なブランチ名はサブコマンドによって異なる
    - e.g. `cmoc review oracle` --> `{{cmoc-review-worktree}}`
    - e.g. `cmoc apply fork` --> `{{cmoc-apply-worktree}}`
- cmoc の run 作業は `{{cmoc-run-worktree}}` 上で `{{cmoc-run-branch}}` を checkout した状態で行う

## `{{run-root}}` 外への書き込み例外規則

- 原則として、cmoc の run 作業は `{{run-root}}` ツリー内のみ読み書き可能である
- ただし、例外として明示したケースにおいては、cmoc の run 作業として `{{repo-root}}` 配下のファイルを読み書きしても良い
    - e.g. cmoc 実行中のログ・ステートファイルは `{{run-root}}/.cmoc/gu` ツリー内ではなく `{{repo-root}}/.cmoc/gu` ツリー内に書き込まなければならない
