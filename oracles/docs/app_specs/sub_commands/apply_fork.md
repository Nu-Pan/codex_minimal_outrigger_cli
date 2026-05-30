# `cmoc apply fork`

## 概要

- `cmoc apply fork` は、Codex CLI による調査・修正ループを実行する
- この調査・修正ループは以下の状態を目標とする
    - `<repo-root>` の実装を `<repo-root>/oracles` の正本仕様断片と一致している
    - `<repo-root>` の実装が最低限度の品質を満たしている
- `cmoc apply fork` が正常に実行完了したからといって、目標達成が保証されるわけではない
    - あくまで、調査・修正ループの実行し、目標達成のために努力する所までが `cmoc apply fork` の責任範囲である
    - i.e. ベストエフォート的な振る舞いで良い
- `cmoc apply fork` は `<cmoc-session-branch>` と作業用コピーを直接汚すことはしない
    - `<cmoc-apply-branch>` を作成し、そこにコミットを積み上げる

## 引数

- 位置引数なし
- オプション引数 `--repeat-investigate-and-fix` を受け取る
- オプション引数 `--repeat-improove-fixing-list` を受け取る
- オプション引数 `--scope={rolling|session|full}` を受け取る
    - ショートネームは `-s`
    - デフォルト値は `rolling`

## 事前条件

以下の場合はエラー終了する。

- 現在のブランチが `<cmoc-session-branch>` ではない
- 対応する `<cmoc-session-state-file>` が存在しない
- 対応する `<cmoc-session-state-file>` の `session.state` が `active` ではない
- 対応する `<cmoc-session-state-file>` の `apply.state` が `ready` ではない
- git 未コミット差分が存在する

## 実行作業

1. `<repo-root>/.cmoc` が git の追跡対象外であることを保証する
2. 現在の `<cmoc-session-branch>` HEAD を `<oracle-snapshot-commit>` として取得する
3. 一意な `<apply-run-id>` を生成する
4. `<oracle-snapshot-commit>` から `<cmoc-apply-branch>` を作成する
5. `<cmoc-apply-branch>` を checkout した専用 `<cmoc-apply-worktree>` を作成する
6. `<cmoc-session-state-file>` の状態を更新
7. `<cmoc-apply-worktree>` 上で調査・修正ループを実行する
    1. 調査対象となる oracles ファイル・実装ファイルを列挙する
    2. Codex CLI に、列挙したファイルリストを元に要修正点をリストアップさせる
    3. 要修正点リスト改善ループ (最大 M 回)
        1. Codex CLI に、要修正点リストを改善させる
        2. 改善点がなければここで要修正点リスト改善ループを抜ける
        3. 要修正点リスト改善ループ先頭に戻る
    4. 改善後の要修正点リストが空であれば、要修正点が検出されなかったものとしてループを終了する
    5. 修正作業ループ（改善後の要修正点リストに対する for-each）
        1. 要修正点 1 つに対する修正作業を Codex CLI に依頼する
        2. `<repo-root>/oracles` などの編集禁止ディレクトリに未コミット差分が有る場合はエラー終了
        3. 全ての未コミット差分を git にコミット（コミットメッセージは Codex CLI で適切なものを生成）
    6. 調査・修正ループ先頭に戻る
8. `<cmoc-session-state-file>` の状態を更新
9. 作業結果をレポートする

## `cmoc apply fork` の責務境界

- `cmoc apply fork` の責務は、指定された最大回数の範囲で調査・修正ループを実行し、その結果を人間が判断できる形でレポートすることである
- `cmoc apply fork` は、要修正点が残っていないことを保証しない
- `cmoc apply fork` は、全ての要修正点を漏れなく発見することは保証しない（あくまでベストエフォート的に振る舞う）
- ループが回数上限に達した場合も、コマンド実行としては正常系として扱う
- 回数上限到達後にさらに `cmoc apply fork` を再実行するか、`cmoc review oracles` や人手レビューを行うか、作業を打ち切るかは人間が判断する

## 調査対象 oracles ファイルの snapshot 原則

- `cmoc apply fork` 開始時点の `<cmoc-session-branch>` HEAD を `<oracle-snapshot-commit>` として固定し、その snapshot から `<cmoc-apply-branch>` を作成する。
- `cmoc apply fork` 開始後に `<cmoc-session-branch>` が進んでも、実行中の apply はその変更を取り込まない。
- `cmoc apply fork` の収束・未収束判定は `<oracle-snapshot-commit>` に対する判定である。

## `<cmoc-session-state-file>` 状態遷移

- 調査・修正ループ開始直前
    - `apply.state` を `running` に遷移させる
    - `apply` セクションの各フィールドを、適切な値で更新する
- 調査・修正ループ完了直後
    - i.e. 全ての処理が正常に完了出来た場合
    - `apply.state` を `completed` に遷移させる
    - `apply` セクションの各フィールドを、適切な値で更新する
- 途中でエラーが発生して処理を中止した場合
    - `apply.state` を `error` に遷移させる

## git worktree と編集操作

- `<cmoc-apply-worktree>` 上の `oracles/` は編集禁止である。
- Codex CLI による実装修正が `<apply-worktree>/oracles` を変更した場合はエラー終了する。
- 一方、apply 実行中にユーザーが `<cmoc-session-branch>` 側で `oracles/` を編集・commit しても、実行中の apply には取り込まれない。

## ループの反復回数の決め方

- 調査・修正ループ
    - サブコマンドの引数 `--repeat-investigate-and-fix` で調査・修正ループの反復回数を受け取る
    - デフォルト値は 5 とする
- 要修正点リスト改善ループ
    - サブコマンドの引数 `--repeat-improove-fixing-list` で要修正点リスト改善ループの反復回数を受け取る
    - デフォルト値は 3 とする

## 調査対象ファイルリストアップの仕様

### 対象となる git スナップショット

`cmoc apply fork` の評価対象は開始時点の `<oracle-snapshot-commit>` に固定される。
つまり、例えば、 `cmoc apply fork` の実行開始後にユーザーによって oracles ファイルの編集が `<cmoc-session-branch>` へ commit された場合、その編集内容は既に実行開始した `cmoc apply fork` の調査対象には含まれない。

### 候補ファイルリスト、ダーティフラグ

- `cmoc apply fork` の対象なるファイルの候補は「oracles ファイル全て」「実装ファイル全て」である
- この候補ファイルリストを元に、本当に調査すべきファイルの絞り込みが行われる
- この絞り込み処理は「ダーティフラグ」で管理される
- ダーティフラグが true のファイルのみ、実際にファイル単位調査が行われる

### スコープモード、ダーティフラグ

- `cmoc apply fork` は以下の 3 つのスコープモードを持つ
    - `--scope rolling` ならローリングスコープ（デフォルト値）
    - `--scope session` ならセッションスコープ
    - `--scope full` ならフルスコープ
- ローリングスコープ
    - 候補ファイルリストを、「最後に join された apply の `<oracle-snapshot-commit>`」から「今回の apply の `<oracle-snapshot-commit>`」の間に変更があったファイルだけに絞り込む
    - そのセッションの最初の apply の場合は、セッションモードにフォールバックする
    - i.e. 前回の `cmoc apply fork` 後に変更があったファイルについて、最低 1 回は調査が行われるということ
- セッションスコープ
    - 候補ファイルリストを、 `<session-start-commit>..<oracle-snapshot-commit>` で変更されたファイルだけに絞り込む
    - i.e. そのセッション上で変更のあったファイルについて、最低 1 回は調査が行われるということ
- 全体適用スコープ
    - 候補ファイル全てのダーティフラグを true で初期化する
    - i.e. 全候補ファイルについて、最低 1 回は調査が行われるということ

## ダーティフラグの更新規則

- ダーティフラグは `cmoc apply fork` 処理の過程で逐次更新される
- 規則は以下の通り
    - 改善済みの最終的な要修正点リスト上、修正内容と関係すると判定されたファイルはダーティフラグを true に、そうではないファイルは false にする
    - Codex CLI による修正作業の結果として差分が発生したファイルはダーティーフラグを true にする

## 要修正点リストアップの仕様

- Codex CLI の呼び出し 1 回で 1 つのファイルを起点とした要修正点リストアップ作業を Codex CLI に依頼する
- この「起点とした」とは
    - `codex exec` に渡すプロンプトで、調査するべきファイルを指定することを指す
    - ただし、この指定は「だけ」の意味ではない
    - i.e. 指定したファイルは以外のファイルも、調査のために必要ならば読むべきである
- このファイル起点の依頼は、事前に列挙したファイルリスト上のファイル全てに対して個別に行う
    - i.e. 調査対象となる oracles ファイルが N 件と実装ファイルが M 件存在するのであれば `codex exec` を N + M 回呼び出すということ
- このファイル起点の依頼は並列に実行する
    - i.e. N + M 並列で実行するということ
- 要修正点リストは Structured Output で受け取る

## 「要修正点」の定義

- oracles ファイルと実装との明確な不整合
    - 「oracles ファイル上で記述されている仕様」と「実装」とが明確に不整合している点を指す
    - oracles は仕様断片であるから、明記されていない仕様の隙間は AI の裁量であり、原則として不整合とはみなさない
    - しかしながら、仕様文言から推測可能な意図と実装とが著しく乖離する場合は要修正点とみなす
- 実装上の明確な問題点
    - 実装だけから見た成果物の品質としての問題を指す
    - バグのような致命的な問題だけを対象とする
    - 「こうした方が良い」のようなクオリティアップ的な話は対象としない
    - 当然ながら、修正後の実装は oracles ファイル上で記述されている仕様を満たしている必要がある

## 要修正点リスト改善の仕様

- ファイルごとに個別に列挙された要修正点リストを１つに連結する
- 連結した要修正点リストの改善作業を Codex CLI に依頼する
- 改善作業完了後、要修正点リストは以下の要件を満たしている事を目指す（ベストエフォートで良い）
    - 要修正点の内容の品質に明確な問題が存在しないこと
    - 要修正点同士に内容的な重複がないこと
    - 要修正点同士が相互に矛盾していないこと
    - 要修正点の内容が、 `<cmoc-apply-branch>` 上の過去の修正内容を考慮したものになっていること
    - 要修正点が False-Positive ではないこと
    - 要修正点を先頭から順番に対応した時に、それが作業順序として適切であること
    - 要修正点リスト改善の過程で発見した「漏れ」が要修正点リストに追加されていること
- 改善後の要修正点リストが空の場合のみ「検出された要修正点なし」と扱う
    - これは「この調査結果においては」という但し書きが付くが、要修正点の完全解消は `cmoc apply fork` の目的ではないので、これでよい
- 改善語の要修正点リストは Structured Output で受け取る

## 要修正点リストの Structured Output schema

```json
{
    "type": "object",
    "additionalProperties": false,
    "required": [
        "git_head_commit_hash",
        "fixing_points"
    ],
    "properties": {
        "git_head_commit_hash": {
            "type": ["string", "null"],
            "description": "要修正点を発見した時点での git HEAD commit hash。後で機械的にフィルされるので AI による出力は null で良い。"
        },
        "fixing_points": {
            "type": "array",
            "description": "実装に対する要修正点のリスト。空配列の場合のみ要修正点なしとみなす。",
            "items": {
                "type": "object",
                "additionalProperties": false,
                "required": [
                    "title",
                    "evidences",
                    "oracle_requirement",
                    "observed_implementation",
                    "reason",
                    "suggested_fix"
                ],
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "要修正点の短い見出し。"
                    },
                    "evidences": {
                        "type": "array",
                        "description": "要修正点の根拠となる文言の位置情報。oracles・実装どちらかのファイルが必ず 1 つは根拠として存在するはずであるから空配列は想定しない。",
                        "items": {
                            "type": "object",
                            "additionalProperties": false,
                            "required": [
                                "path",
                                "line_start",
                                "line_end",
                                "summary"
                            ],
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "要修正点の根拠となるファイルの絶対パス。"
                                },
                                "line_start": {
                                    "type": ["integer", "null"],
                                    "description": "要修正点の根拠となる記述の開始行。行番号を特定できない場合は null。"
                                },
                                "line_end": {
                                    "type": ["integer", "null"],
                                    "description": "要修正点の根拠となる記述の終了行。行番号を特定できない場合は null。"
                                },
                                "summary": {
                                    "type": "string",
                                    "description": "該当箇所の短い要約。位置情報がズレた場合にそれを検知するための冗長情報。"
                                }
                            }
                        }
                    },
                    "oracle_requirement": {
                        "type": "string",
                        "description": "oracle が要求している仕様。実装のみから発見した要修正点であったとしても必ず関係する仕様を記載する。"
                    },
                    "observed_implementation": {
                        "type": "string",
                        "description": "調査時点の実装が実際にどうなっているか。"
                    },
                    "reason": {
                        "type": "string",
                        "description": "なぜ、明確に問題があり修正が必要であると言えるのか。推測や未確認事項は含めない。"
                    },
                    "suggested_fix": {
                        "type": "string",
                        "description": "問題を解決するために必要な実装修正の方針。"
                    }
                }
            }
        }
    }
}
```

## 要修正点対応作業の仕様

- リストアップされた要修正点に対する修正作業を Codex CLI に依頼する
- 要修正点１つにつき１回 Codex CLI を起動する
- 作業のためのヒントとして要修正点の情報をプロンプトに注入する
    - 「絶対に従わなければならない指示書」としては**扱わない**
    - 修正作業を行うエージェントは、この要修正点情報を無視しても良い
- Codex CLI に依頼する作業は要修正点として指摘されている問題の修正作業そのものを目的とする
    - 作業結果が、要修正点で述べている目的を達成したことの保証は求めない
    - ベストエフォート的に振る舞えばそれで良いものとする

## 回数上限でループを抜けた場合

- エラーとみはみなさず、作業結果の区分「未収束」として処理を続行する

## 作業レポートの仕様

- レポートの形式は markdown + YAML Front Matter とする
- YAML Front Matter に必ず含める項目
    - `<cmoc-session-branch>`
    - `<cmoc-apply-branch>`
    - apply worktree path
    - oracle snapshot commit
    - session head at apply start
    - session head at apply finish
- レポート本文に必ず含める項目
    - 作業結果
        - 収束 : 「検出された要修正点リストが空」によりループを終了した
        - 未収束 : 「回数上限に達した」によりループを終了した
        - エラー : 途中でエラーが起きてループを正常に終了出来なかった
    - 要修正点件数の推移
        - ループごとに何件の要修正点を見つけたかを書く
        - 「未収束」の場合は、まだ要修正点が残っている可能性を定型文で追記する
    - `<cmoc-apply-branch>` 上の全ての変更内容に対する要約
        - この `cmoc apply fork` で行った作業内容だけの要約に限定する
        - 変更内容の意味論に基づいたカテゴリ分けを行うこと
- レポート本体は `<repo-root>/.cmoc/reports/apply/fork/<time-stamp>.md` にファイルに保存する
- 作成したレポートのフルパスを標準出力に流すこと (内容は流さない)

## `<cmoc-apply-branch>` 上の全ての変更内容に対する要約の生成方法

- `<cmoc-apply-branch>` 上の全ての変更内容に対する要約は機械的に生成出来ないので Codex CLI に執筆を依頼する
- 要約は Structured Output で出力させる
- Structured Output を元に Markdown にレンダリングするのは cmoc の責任である
- schema は以下の通り
```json
{
    "type": "object",
    "additionalProperties": false,
    "required": [
        "changes"
    ],
    "properties": {
        "changes": {
            "type": "array",
            "description": "`<oracle-snapshot-commit>` から `<cmoc-apply-branch>` の HEAD までの差分を、変更内容の意味論に基づいてカテゴリ分けした要約。空配列は想定しない。",
            "items": {
                "type": "object",
                "additionalProperties": false,
                "required": [
                    "category",
                    "summary",
                    "changed_paths"
                ],
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "変更内容の意味論に基づくカテゴリ名。例: 実行制御、レポート生成、テスト、ルーティング文書。"
                    },
                    "summary": {
                        "type": "string",
                        "description": "このカテゴリで行った変更内容の人間向け要約。カテゴリ名の再掲だけではなく、何をどう変えたかを書く。"
                    },
                    "changed_paths": {
                        "type": "array",
                        "description": "このカテゴリに属する主な変更ファイルのリポジトリ相対パス。網羅よりも、要約の根拠として有用な主要ファイルを列挙する。",
                        "items": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
}
```

## サブコマンドの終了コード

- 収束・未収束・エラーの３種類を区別可能であること
