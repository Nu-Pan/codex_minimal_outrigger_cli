# `cmoc session fork`

## 概要

- `cmoc session fork` は、現在 checkout している `{{local-branch}}` を `{{cmoc-session-home-branch}}` とし、その HEAD から `{{cmoc-session-branch}}` を作成する。
- `{{cmoc-session-home-branch}}` は、その session の分岐元であり、最終的な merge 先でもある。
- `{{repository-default-branch}}` は特別扱いしない。

## 引数

- 引数なし

## 事前条件

`cmoc session fork` は `{{local-branch}}` 上でのみ実行できる。

以下の場合はエラー終了する。

- detached HEAD 上で実行された
- `{{remote-tracking-branch}}` や commit hash など、`{{local-branch}}` ではない場所から実行された
- `cmoc/session/...` や `cmoc/run/...` など `{{cmoc-managed-branch}}` 上で実行された
- git 未コミット差分が存在する
- 現在の `{{cmoc-session-home-branch}}` に active な `{{cmoc-session-branch}}` が既に存在する

## 実行手順

1. doctor preprocess を呼び出す
2. 現在 checkout している `{{local-branch}}` 名を `{{cmoc-session-home-branch}}` として取得する
3. 現在の HEAD commit を `{{cmoc-session-fork-commit}}` として取得する
4. 一意な `{{session-id}}` を生成する
5. `{{cmoc-session-branch}}` を作成して checkout する
6. `{{repo-root}}/.cmoc/gu/ar/session/{{session-id}}.json` に session 情報と初期状態 `run.state=ready` を保存する
7. terminal result のサブコマンド固有結果に、作成した `{{cmoc-session-branch}}` 名と `{{cmoc-session-home-branch}}` 名を含める

## `{{cmoc-session-branch}}` の命名規則

- `{{cmoc-session-branch}}` の実際の branch 名は `cmoc/session/{{session-id}}` とする。
- `{{session-id}}` は `{{time-stamp}}` とする。

## 任意 start point の扱い

- `cmoc session fork` は任意の start point を受け取らない
- 分岐元を変えたい場合は、ユーザーが事前に目的の `{{local-branch}}` へ移動してから `cmoc session fork` を実行する

## session の原則

- 1 つの `{{cmoc-session-home-branch}}` に対して active な `{{cmoc-session-branch}}` は高々 1 つとする。
- detached HEAD, `{{remote-tracking-branch}}`, commit hash, `{{cmoc-managed-branch}}` は `{{cmoc-session-home-branch}}` として扱わない。

## primary report

- `natural_completion` と `error` のすべての終了経路で、session fork 実行要約を primary report として保存する。doctor preprocess または事前条件で終了した場合も対象とする。
- report は Markdown と YAML Front Matter で構成し、`{{repo-root}}/.cmoc/gu/ar/report/session/fork/{{time-stamp}}.md` に保存する。
- front matter には、command、生成日時、repo root、terminal result の共通分類、終了コード、session ID、home branch、session branch、session fork commit、および session state の実行前後の値を含める。確定できなかった値は `null` とする。
- 本文には、branch の作成と checkout、session state file の作成と状態遷移、失敗時の rollback または残存資源、warning またはエラー、必要な次の操作、および関連する診断用サブコマンドログを要約する。
