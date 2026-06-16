# `cmoc review oracle`

## 概要

- 現在の `<work-root>/oracle` に致命的な問題が無いかレビューし、レビュー結果を人間にレポートする

## 引数

- 位置引数なし
- オプション引数 `--scope={session|full}` を受け取る
    - ショートネームは `-s`
    - デフォルト値は `session`
- オプション引数 `--enumerate-findings-loop` を受け取る
- オプション引数 `--merge-findings-loop` を受け取る
- オプション引数 `--refine-findings-loop` を受け取る

## 事前条件

以下の場合はエラー終了する

- 現在のブランチが `<cmoc-session-branch>` ではない
- 対応する `<cmoc-session-state-file>` が存在しない
- 対応する `<cmoc-session-state-file>` の `session.state` が `active` ではない
- git 未コミット差分が存在する

## 実行手順

1. `<work-root>/.cmoc` が git の追跡対象外であることを保証する
2. run の隔離実行を開始する
3. 所見リストを空配列で初期化
4. 所見リスト列挙ループ
    1. レビュー対象ファイルを列挙
    2. ファイルごとに「新規所見の列挙」を Codex CLI に依頼、新規所見を所見リストに結合
    3. 全ファイルのダーティフラグが false であれば所見リスト列挙ループをここで打ち切る
    4. 所見リストマージループ
        1. 所見リストのマージを Codex CLI に依頼
        2. この周回で所見のマージが無ければ、所見リストマージループを打ち切る
        3. 所見リストマージループの先頭に戻る
    5. 所見リスト列挙ループ先頭に戻る
5. 所見リスト検証ループ
    1. 所見ごとに「その所見が妥当ではない理由の記述」を Codex CLI に依頼する
    2. 所見ごとに「その所見が妥当である理由の記述」を Codex CLI に依頼する
    3. 全所見のダーティフラグが false であれば所見リスト検証ループをここで打ち切る
    4. 所見リスト検証ループ先頭に戻る
6. 所見ごとに「その所見の採用・不採用の判定」を Codex CLI に依頼する
7. run の隔離実行を終了する
8. 所見リストをレポートとしてレンダリングする

## 「run の隔離実行」とは

- その範囲内で、実際の作業を `<cmoc-review-worktree>` 上で隔離実行することを指す
- 隔離実行については `<cmoc-root>/oracle/doc/app_specs/run_isolation.md` を参照すること
- 隔離実行の終了時、`<cmoc-session-branch>` へのマージを自動で行う
    - `<cmoc-review-branch>` 上で更新される可能性があるのは `INDEX.md` のみである
    - `INDEX.md` は自動生成ファイルであるため `<cmoc-review-branch>` 側の変更が失われても何ら問題ない
    - よって `INDEX.md` のコンフリクトは `<cmoc-session-branch>` 側を採用することで機械的に解決する

## `cmoc review oracle` の責務境界

- `cmoc review oracle` の責務であること
    - oracle file に対する所見をリスト化して人間にレポートとして提示する
    - 人間の認知コストを節約するために、指定された最大回数の範囲内で所見リストを高品質化する
    - oracle file に基づいたレビューを行う
    - oracle file 上の「間違っていることが明白な要素」を人間に知らせる
    - oracle file のスナップショットをレビューする
- `cmoc review oracle` の責務ではないこと
    - 漏れなく所見を発見出来ていることは保証しない
    - `cmoc review oracle` の結果を元に次に何をするべきか判断するのは人間の責任であり cmoc の責任ではない
    - cmoc によって自動生成されたファイル (e.g. `INDEX.md`) に対するレビュー対象ではない
    - 実装ファイルを交えたレビューは目的ではない
    - 「oracle file もっと良くするには」の人間への提案は目的ではない
    - 過去 oracle file に何があったか (i.e. 編集・追加・削除) はレビュー対象ではない

## 「所見」の定義

- 致命的な問題 (fatal) を対象とする
    - 仕様断片同士に明確な矛盾がある
    - 仕様に従って実装した時に、実装者の裁量では解消不能な問題が発生する
- 単純な問題 (minor) を対象とする
    - 日本語的な誤り（e.g. 誤字、脱字、助詞の抜け）
    - 用語の不統一・表記揺れ・typo
    - その他ケアレスミスの疑いが濃厚なもの
- 以下の問題は対象としない
    - oracle file だけからは問題だとは言い切れない
    - 仕様からは実装が一意に定まらない
- これら定義は `codex exec` のプロンプトに「リポジトリ固有の事情に依存しない汎用的なレビュー観点」として注入する。

## Codex CLI によるファイルアクセス規則

- `codex exec` は読み取り専用で実行する。
- レビューにあたってエージェントは...
    - `<work-root>/oracle` 配下のファイルを自由に読んで良い
    - `<work-root>/oracle` 以外のファイルは読んではいけない
    - 指定されたファイルだけでなく、関連する oracle file も読みに行く
    - どの oracle file が関連するかは `INDEX.md` を根拠に判断する

## 所見の ID 管理

- cmoc は、所見リストへ所見を追加する時点で安定した `finding_id` を付与する
- Codex CLI が特定の所見を一意に指し示す必要がある場合 (e.g. 所見リストのマージ) は、この `finding_id` を参照する

## 「所見リスト列挙ループ」の詳細

- このループでは、所見リストを可能な限り網羅的にする事を目的とする
- oracle file  1 つごとにダーティーフラグを用意する
- ダーティーフラグが true のファイルのみを Codex CLI による「新規所見の列挙」の対象とする
- ダーティーフラグの初期値はスコープモードによって変わる
    - セッションスコープ (`--scope session`) の場合、`<cmoc-session-fork-commit>` から `<cmoc-review-fork-commit>` の間で変更があったファイルのみ、ダーティフラグを true とする
    - フルスコープ (`--scope full`) の場合、全ての oracle file のダーティフラグを true とする
- ダーティフラグは以下のルールで更新される
    - 「新規所見の列挙」の結果、新規所見なしと判断された場合、そのファイルのダーティフラグを false にする
- ループ回数の上限
    - `--enumerate-findings-loop` で指定される
    - デフォルト値は 3

## 「新規所見の列挙」の詳細

- 1 回の `codex exec` 呼び出しで 1 つの oracle file をレビューする
- プロンプトで「現状の所見リストのうち、今回のレビュー対象ファイルと関連するもの」を渡す
- Codex CLI は新規所見（既知でない所見）のリストを Structured Output で出力する
- Structured Output schema として `<cmoc-root>/oracle/schemas/structured_output/review/oracle/enumerate_findings.json` を使用する
- 所見リストが既に十分網羅的であるなら、新規所見なしとなるはずである
- このファイルごとのレビューは並列に実行する

## 「所見リストマージループ」の詳細

- このループでは、所見リストの冗長性・不整合を解決することを目的とする
- ループ回数の上限
    - `--merge-findings-loop` で指定される
    - デフォルト値は 3

## 「所見リストのマージ」の詳細

- 所見リストの冗長性・不整合の解決を `codex exec` に依頼する
- プロンプトで、現状の所見リストを Codex CLI に渡す
- Codex CLI は問題解決に必要な編集操作のリストを Structured Output で出力する
- Structured Output schema として `<cmoc-root>/oracle/schemas/structured_output/review/oracle/merge_findings.json` を使用する
- 作業完了後、所見リストが以下の要件を満たしている事を目指す（ベストエフォートで良い）
    - 所見同士に内容的な重複がないこと
    - 所見同士が相互に矛盾していないこと
- 所見リストが既に十分コンパクトで整合的であるなら、編集操作リストは空となるはずである

## 「所見リスト検証ループ」の詳細

- このループでは、所見が妥当である・妥当ではない理由を出し尽くす事を目的とする
- 所見 1 つごとにダーティーフラグを用意する
- ダーティーフラグが true の所見のみを Codex CLI によるレビューの対象とする
- ダーティーフラグの初期値はすべて true とする
- ダーティフラグは、その周回で「その所見が妥当ではない理由」「その所見が妥当である理由」が 1 つも出なかった場合に false にする
- ループ回数の上限
    - `--refine-findings-loop` で指定される
    - デフォルト値は 3

## 「その所見が妥当ではない理由の記述」「その所見が妥当である理由の記述」の詳細

- 1 回の `codex exec` 呼び出しで 1 つの所見をレビューする
- プロンプトで、レビュー対象の所見の詳細を Codex CLI に渡す
- Codex CLI は新規の理由のリストを Structured Output で出力する
- Structured Output schema として `<cmoc-root>/oracle/schemas/structured_output/review/oracle/validate_findings_challenger.json`, `<cmoc-root>/oracle/schemas/structured_output/review/oracle/validate_findings_advocate.json` を使用する
- その所見が妥当ではない・妥当であるとする理由は以下の原則に従う
    - 具体的な根拠 (e.g. 事実と異なる) を必ず示す
    - 「かもしれない」「可能性がある」は根拠としない
    - 「妥当である（ではない）理由」と対応する「妥当ではない（である）理由」に対する反論をする
- 理由が既に出尽くしているなら、新規理由なしとなるはずである
- この所見ごとのレビューは並列に実行する

## 「その所見の採用・不採用の判定」の詳細

- その所見を、要確認項目として人間に見せるべきかの判定を `codex exec` に依頼する
- 1 回の `codex exec` 呼び出しで 1 つの所見を判定する
- プロンプトで、レビュー対象の所見を Codex CLI に渡す
- Codex CLI は判定結果を Structured Output で出力する
- Structured Output schema として `<cmoc-root>/oracle/schemas/structured_output/review/oracle/judge_findings.json` を使用する

## レポート

### レポートの体裁

レビューレポートは Markdown ファイルとし、yaml frontmatter と本文で構成する。

### 所見単位の集約

- 最終レポートでは、レビュー対象ファイル単位ではなく、所見単位で結果を並べる。
- 所見は以下の順序で表示する。
    1. 採用と判定された `fatal`
    2. 採用と判定された `minor`
    3. 不採用と判定された `fatal`
    4. 不採用と判定された `minor`

### yaml frontmatter

frontmatter 以下の項目を書く（いずれも、不明な場合は null 可）

- `command`
- `generated_at`
- `repo_root`
- `scope`
- `session_branch`
- `session_fork_commit`
- `review_branch`
- `review_fork_commit`
- `review_join_commit`
- `oracle_count_total`
- `oracle_count_evaluated`
- `fatal_findings_accepted_count`
- `minor_findings_accepted_count`
- `fatal_findings_rejected_count`
- `minor_findings_rejected_count`
- `result`

`result` は以下のいずれかとする。

- `ok`
    - レビュー対象の範囲では問題点が検出されなかった。
- `fatal`
    - `fatal` 所見が 1 件以上検出された。
- `minor`
    - `fatal` は検出されていないが、`minor` な所見が 1 件以上検出された。
- `no_targets`
    - レビュー対象 oracle が 0 件だった。
- `error`
    - レビュー処理またはレポート生成に失敗した。

### 本文セクション

本文には以下のセクションをこの順番で必ず含める。

1. `# cmoc review oracle report`
2. `## Verdict`
3. `## Evaluated oracle file`
4. `## Fatal findings`
5. `## Minor findings`

### `Verdict`

- `fatal` の場合
    - oracle ファイルに、直ちに修正するべき問題が存在することを書く
- `minor` の場合
    - oracle file に、致命的ではない、細かい問題があることを書く
- `ok` の場合
    - oracle file に、問題は何ら見つからなかったことを書く
    - ただし、問題点の不存在を完全保証するものではないことも書く
- `no_targets`
    - レビュー対象 oracle が 0 件だったことを書く
- `error`
    - レビュー処理が途中で失敗したことを書く

### `Evaluated oracle file`

- 実際にレビューした oracle ファイルを、表形式で一覧表示する
- e.g.
```markdown
| No. | Oracle file | Findings |
|---:|---|---:|
| 1 | `oracle/doc/app_specs/sub_commands/review_oracle.md` | 2 |
| 2 | `oracle/doc/app_specs/workflow.md` | 0 |
```

### `Fatal findings`

- `fatal` な所見を列挙する

### `Minor fIndings`

- `minor` な所見を列挙する

## レポートの提示方法

- レビューレポートは `<repo-root>/.cmoc/reports/review_oracle/<time-stamp>.md` にファイル保存する
- レポートファイルのフルパスを stdout に流す
