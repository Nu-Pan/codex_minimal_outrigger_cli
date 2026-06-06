# `cmoc review oracles`

## 概要

- 現在の `<repo-root>/oracles` のスナップショットに致命的な問題が無いか評価し、評価結果を人間にレポートする

## 引数

- 位置引数なし
- オプション引数 `--scope={session|full}` を受け取る
    - ショートネームは `-s`
    - デフォルト値は `session`
- オプション引数 `--repeat-improve-issues-list` を受け取る

## 事前条件

- なし

## 実行手順

1. `<repo-root>/.cmoc` が git の追跡対象外であることを保証する
2. oracles ファイルを列挙
3. 部分評価モードの場合、列挙した oracles ファイルリストを「`<cmoc-session-branch>` 上で変更があった oracles ファイル」のみに絞り込む
4. 列挙した oracles ファイルリストに対して、ファイルごとの評価を行う
5. 問題点リストを改善する
6. 改善済みの問題点リストをレポートとしてレンダリングする

## 評価対象はスナップショットである

- `cmoc review oracles` は、コマンド開始時点で現在チェックアウトされている `<repo-root>/oracles` ツリーを「閉じた oracle スナップショット」として評価する
- 過去にあった状態遷移は評価対象としない
  - i.e. このコマンドは git 履歴・base commit・過去の oracle スナップショットとの差分を oracle の存在可否や仕様欠落の根拠としては扱わない。
  - e.g. 現在の `<repo-root>/oracles` に存在しないファイル（過去に削除されたファイル）は評価対象にしない。
- 現在の oracle スナップショット上の記述だけから、判断可能な問題は問題として報告して良い
  - e.g. 参照切れ、INDEX の不整合、主要ワークフローの仕様不足、完了判定不能
  - この場合も、問題の根拠としてよいのは、現在存在するファイルの記述だけである（過去に存在したファイルではない）

## レビュー対象候補

- `cmoc review oracles` の対象となるファイルの候補は「oracles ファイル全て」である
- この候補ファイルリストを元に、本当に調査するべきファイルの絞り込みが行われる
- この絞り込み処理は「ダーティフラグ」で管理される
- ダーティフラグが true のふぁいるのみ、実際にファイル単位レビューが行われる

## スコープモード、ダーティーフラグ

- `cmoc review oracles` は以下の 2 のスコープモードを持つ
    - `--scope session` ならセッションスコープ
    - `--scope full` ならフルスコープ
- セッションスコープ
  - レビュー対象ファイルリストを `<session-start-commit>..<oracle-snapshot-commit>` で変更されたファイルだけに絞り込む
  - i.e. そのセッション上で変更のあったファイルがレビュー対象となる
- フルスコープ
  - レビュー対象ファイルリストに対してレビューを行う
- `<cmoc-session-branch>` 上に居る場合
    - `--full` がついている場合は全体評価モードへ
    - `--full` が付いていない場合は部分評価モードへ
- `<cmoc-session-branch>` に居ない場合 (e.g. `master` ブランチ上)
    - 全体評価モードへ


## 「致命的な問題」の定義

- 実装を参照せずに、仕様だけからの判断として、以下の問題が発生しうるものを「致命的な問題」と定義する。
    - 主要ワークフローが破綻する
    - 各サブコマンドが作業完了の判定をできない
    - cmoc の中核目的を満たしたと判定できない
- ただし、以下の緩和を持ち込む
    - 仕様を元に実装が一意に定まらなくても良いものとする（そのために oracles が過剰に詳細になってしまうと、人間の負担が増えて oracles のビジョンと反してしまう）
- この定義は `codex exec` のプロンプトに「リポジトリ固有の事情に依存しない汎用的な評価観点」として注入する。

## Codex CLI 呼び出しの規則

- 以下の作業を Codex CLI に依頼する時、この規則を適用する
    - ファイル毎の評価
    - 問題点リストを改善
- `codex exec` は読み取り専用で実行する。
- 評価にあたってエージェントは以下のファイルを読んで良い
    - 対象 oracle ファイル
    - `<repo-root>/oracles` 配下の関連 oracles ファイル
    - 関連判断に必要な `<repo-root>/oracles` 配下の `INDEX.md`
- 逆に、評価にあたってエージェントは以下のファイルを読んではいけない
    - oracles 外のファイル
    - e.g. 実装ファイル、テストファイル、設定ファイル、ビルド成果物
- 関連する oracles ファイルの選定方法
    - `oracles/INDEX.md` から始まる `INDEX.md` の Summary / Read this when / Do not read this when を根拠に行う

## 「ファイル毎の評価」の詳細

- 1 回の `codex exec` 呼び出しで oracles ファイル 1 つを評価し、問題点リストを生成する
- このファイルごとの評価は並列に実行する
- 問題点リストは Structured Output で受け取る
- 評価作業のヒントとして以下の情報をプロンプトで渡すこと
    - oracles ファイルの内容に対する指摘が必要であること
    - この指摘を人間が読んで oracles ファイルの修正を行うこと
    - `INDEX.md` は自動生成されるため、評価対象ではないこと

## 「問題点リストを改善」の詳細

- ファイル毎に生成した問題点リストを１つに単純結合する
- 結合された問題点リストを元に、意味論的に統合・改善された新しい問題点リストの生成を `codex exec` に依頼す
- 作業完了後、問題点リストは以下の要件を満たしている事を目指す（ベストエフォートで良い）
    - 問題点の内容の品質に明確な問題が存在しないこと
    - 問題点同士に内容的な重複がないこと
    - 問題点同士が相互に矛盾していないこと
    - 問題点が False-Positive ではないこと
- この改善作業は繰り返し実行する
  - 最大で 3 回 (`--repeat-improve-issues-list` で指定された場合そちらを優先) 繰り返す
  - 入力として与えた問題点リストと、出力として返ってきた問題点リストとが完全一致する場合はそこでループを打ち切る
- 問題点リストは Structured Output で受け取る

## 問題点リストの Structured Output schema

- 「ファイル毎の評価」「問題点リストを改善」共に、以下の schema を使用する。
- そのため、出力は常に問題点単位の `issues` 配列だけを持つ。
- 評価対象ファイル単位のメタ情報は schema に含めない。
- 問題がない場合は `issues: []` を返し、その場合は参照ファイル情報も出力しない。

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": [
    "issues"
  ],
  "properties": {
    "issues": {
      "type": "array",
      "description": "検出した問題点。問題がない場合は空配列。",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "severity",
          "title",
          "oracle_path",
          "oracle_line_start",
          "oracle_line_end",
          "referenced_paths",
          "affected_workflow",
          "requirement",
          "problem",
          "reason",
          "suggested_oracle_change",
          "specification_only_basis"
        ],
        "properties": {
          "severity": {
            "type": "string",
            "enum": ["fatal", "warning", "inconclusive"],
            "description": "問題点の分類。"
          },
          "title": {
            "type": "string",
            "description": "問題点の短い見出し。"
          },
          "oracle_path": {
            "type": "string",
            "description": "この issue の帰属先となる評価対象 oracle ファイルの絶対パス。"
          },
          "oracle_line_start": {
            "anyOf": [
              {
                "type": "integer",
                "minimum": 1
              },
              {
                "type": "null"
              }
            ],
            "description": "この issue の帰属先となる oracle 記述の開始行。特定できない場合は null。"
          },
          "oracle_line_end": {
            "anyOf": [
              {
                "type": "integer",
                "minimum": 1
              },
              {
                "type": "null"
              }
            ],
            "description": "この issue の帰属先となる oracle 記述の終了行。特定できない場合は null。"
          },
          "referenced_paths": {
            "type": "array",
            "description": "この問題点の評価時に参照した oracle / INDEX ファイルの絶対パス。oracle_path 自身は含めても含めなくてもよいが、レポートでは重複排除する。",
            "items": {
              "type": "string"
            }
          },
          "affected_workflow": {
            "type": "string",
            "description": "影響を受ける workflow / subcommand / concept。例: cmoc apply fork, cmoc review oracles, overall。"
          },
          "requirement": {
            "type": "string",
            "description": "oracle が要求している、または要求すべき仕様。"
          },
          "problem": {
            "type": "string",
            "description": "仕様上の問題点。"
          },
          "reason": {
            "type": "string",
            "description": "なぜその severity と判断したのか。fatal の場合は致命的問題の定義との対応を明示する。"
          },
          "suggested_oracle_change": {
            "type": "string",
            "description": "oracle をどう修正すべきか。"
          },
          "specification_only_basis": {
            "type": "string",
            "description": "この問題点の評価が oracles 配下の仕様断片と INDEX だけに基づくことの説明。"
          }
        }
      }
    }
  }
}
```

## 問題点リストの Structured Output の後処理・事後検証

- `issues[*].oracle_path` が oracles ファイルではない場合、それはエラーとしては扱わない
- その他は AI の裁量で決めて良い

## レポート

### レポートの体裁

評価レポートは Markdown ファイルとし、yaml frontmatter と本文で構成する。

## 問題点単位の集約

- 最終レポートでは、評価対象ファイル単位ではなく、検出された問題点単位で結果を並べる。
- 1 つの oracle ファイルから複数の問題点が検出された場合、それぞれを独立した項目として扱う。
- `cmoc` は全ファイルの `issues` 配列を連結し、問題点ごとの一覧を作る。
- 問題点は severity ごとに以下の順序で表示する。

  1. `fatal`
  2. `inconclusive`
  3. `warning`
- 同一 severity 内の順序は、原則として評価対象ファイルの列挙順、および各ファイル内の `issues` 配列順を維持する。
- `cmoc` は問題点に安定した report-local id を付与する。

  - fatal: `FATAL-001`, `FATAL-002`, ...
  - inconclusive: `INCONCLUSIVE-001`, `INCONCLUSIVE-002`, ...
  - warning: `WARN-001`, `WARN-002`, ...

### yaml frontmatter

frontmatter には少なくとも以下の項目を書く。

- `schema_version`
- `command`
- `generated_at`
- `repo_root`
- `oracle_root`
- `mode`
- `full_requested`
- `branch`
- `is_cmoc_branch`
- `base_commit`
- `head_commit`
- `oracle_count_total`
- `oracle_count_evaluated`
- `fatal_issue_count`
- `warning_issue_count`
- `inconclusive_issue_count`
- `result`

`result` は以下のいずれかとする。

- `ok`
  - 評価対象の範囲では問題点が検出されなかった。
- `fatal`
  - `fatal` issue が 1 件以上検出された。
- `inconclusive`
  - `fatal` issue は検出されていないが、`inconclusive` issue が 1 件以上検出された。
- `warning`
  - `fatal` / `inconclusive` は検出されていないが、`warning` issue が 1 件以上検出された。
- `no_targets`
  - 評価対象 oracle が 0 件だった。
- `error`
  - 評価処理またはレポート生成に失敗した。

### 本文セクション

本文には以下のセクションをこの順番で必ず含める。

1. `# cmoc review oracles report`
2. `## Summary`
3. `## Verdict`
4. `## Evaluated oracle files`
5. `## Fatal issues`
6. `## Inconclusive issues`
7. `## Warnings`
8. `## Referenced files`

### `Summary`

`Summary` には、少なくとも以下を書く。

- 評価結果 `result`
- 評価モード
- 評価対象 oracle ファイル数
- 検出された `fatal` / `inconclusive` / `warning` issue 数

### `Verdict`

`Verdict` には、人間が次に何を判断すべきかを書く。

- `fatal` の場合
  - oracle スナップショットには、仕様だけから判断して主要ワークフロー、完了判定、または中核目的を壊しうる問題があることを書く。
- `inconclusive` の場合
  - 致命的問題ありとは断定できないが、仕様評価として判断不能な点があることを書く。
- `warning` の場合
  - 致命的ではないが、仕様品質・可読性・将来の実装安定性に問題があることを書く。
- `ok` の場合
  - 今回評価した範囲では問題点が検出されなかったことを書く。
  - ただし、問題点の不存在を完全保証するものではないことも書く。

### `Evaluated oracle files`

評価対象 oracle ファイルを一覧表示する。

この一覧は、レポートの主結果ではなく、評価範囲を確認するための補助情報である。

例:

```markdown
| No. | Oracle file | Issues |
|---:|---|---:|
| 1 | `oracles/app_specs/sub_commands/review_oracles.md` | 2 |
| 2 | `oracles/app_specs/workflow.md` | 0 |
```

### `Fatal issues`

`severity = fatal` の問題点を、問題点単位で列挙する。

例:

```markdown
### FATAL-001: レポートの成功判定条件が曖昧

- Oracle file: `oracles/app_specs/sub_commands/review_oracles.md`
- Lines: `72-80`
- Affected workflow: `cmoc review oracles`
- Requirement:
  - 評価結果を人間が判断可能な形でレポートする。
- Problem:
  - レポート本文の形式が固定されておらず、致命的問題の有無を安定して確認できない。
- Reason:
  - `cmoc review oracles` の中核目的は oracle スナップショットの致命的問題を人間に報告することだが、報告形式が曖昧だと作業完了を判断できない。
- Suggested oracle change:
  - レポート本文の必須セクションと issue 項目の必須フィールドを仕様化する。
```

### `Inconclusive issues`

`severity = inconclusive` の問題点を、問題点単位で列挙する。

### `Warnings`

`severity = warning` の問題点を、問題点単位で列挙する。

### `Referenced files`

ファイルごとの `referenced_paths` を重複排除して一覧表示する。

- どの oracle / INDEX ファイルが評価根拠として使われたかを確認するための補助情報である。
- 実装ファイル、テストファイル、設定ファイル、ビルド成果物が混入していないことを人間が確認しやすくする。

## レポートの提示方法

- 評価レポートは `<repo-root>/.cmoc/reports/review_oracles/<time-stamp>.md` にファイルに保存する
- レポートファイルのフルパスを stdout に流す

## 評価時のワークフロー解釈

cmoc の利用ワークフローは、人間が各コマンドの間で状態を確認・修正することを前提とする。

各サブコマンド仕様は、原則として「そのコマンドが呼び出された時点」の契約を述べるものであり、直前の cmoc コマンドの終了状態から次の cmoc コマンドの開始状態までを、cmoc が完全に自動遷移させることまでは要求しない。

したがって、以下はそれだけでは致命的問題とみなさない。

- 前のコマンドが、次のコマンドの事前条件を自動的に満たすとは書かれていない
- 人間が branch checkout、working tree の整理、`/oracles` の修正、commit / revert、再実行判断などを行えば、次のコマンドの事前条件を満たせる
- 想定ワークフローが概略手順であり、各人間判断ステップの内部操作を網羅していない

ただし、以下は致命的問題として扱ってよい。

- 人間が許容された操作をしても、主要ワークフローを完了可能な状態にできない
- ある仕様が「cmoc が自動で保証する」と明示している状態と、別の仕様が要求する状態が矛盾している
- あるコマンドの完了判定が、そのコマンド呼び出し時点の情報だけでは定義できない
