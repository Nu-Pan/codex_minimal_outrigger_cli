# `cmoc eval-oracles`

## 概要

- 現在の `<repo-root>/oracles` のスナップショットに致命的な問題が無いか評価し、評価結果を人間にレポートする

## 引数

- 位置引数なし
- オプション引数 `--full` (`-f`) を受け取る

## 事前条件

- なし

## 部分・全体評価モード

- `cmoc eval-oracles` は部分評価・全体評価の２つのモードを持つ
- `<cmoc-branch>` 上に居る場合
    - `--full` がついている場合は全体評価モードへ
    - `--full` が付いていない場合
        - `<cmoc-branch>` 上で `oracles` ファイルの削除が有る場合は全体評価モードへ
        - そうでなければ部分評価へ
- `<cmoc-branch>` に居ない場合 (e.g. `master` ブランチ上)
    - 全体評価モードへ

## 実行手順

1. `<repo-root>/.cmoc` が git の追跡対象外であることを保証する
2. `oracles` ファイルを列挙
3. 部分評価モードの場合、列挙した `oracles` ファイルリストを「`<cmoc-branch>` 上で変更があった `oracles` ファイル」のみに絞り込む
4. 列挙した `oracles` ファイルリストに対して、ファイルごとの評価を行う
6. これまでに出した評価を１つのレポートにまとめる

## 「致命的な問題」の定義

- 実装を参照せずに、仕様だけからの判断として、以下の問題が発生しうるものを「致命的な問題」と定義する。
    - 主要ワークフローが破綻する
    - 各サブコマンドが作業完了の判定をできない
    - cmoc の中核目的を満たしたと判定できない
- ただし、以下の緩和を持ち込む
    - 仕様を元に実装が一意に定まらなくても良いものとする（そのために `oracles` が過剰に詳細になってしまうと、人間の負担が増えて `oracles` のビジョンと反してしまう）
- この定義は `codex exec` のプロンプトに「リポジトリ固有の事情に依存しない汎用的な評価観点」として注入する。

## 「ファイル毎の評価」の詳細

- 1 回の `codex exec` 呼び出しで、ファイル 1 つを評価する
- `codex exec` は読み取り専用で実行する。
- 評価にあたってエージェントは以下のファイルを読んで良い
    - 対象 `oracle` ファイル
    - `<repo-root>/oracles` 配下の関連 `oracles` ファイル
    - 関連判断に必要な `<repo-root>/oracles` 配下の `INDEX.md`
- 逆に、評価にあたってエージェントは以下のファイルを読んではいけない
    - `oracles` 外のファイル
    - e.g. 実装ファイル、テストファイル、設定ファイル、ビルド成果物
- 関連する `oracles` ファイルの選定方法
    - `oracles/INDEX.md` から始まる `INDEX.md` の Summary / Read this when / Do not read this when を根拠に行う
- レポートには以下のことを明示する
    - 評価が「仕様だけ」に基づくとする根拠
    - 参照した oracle / INDEX ファイル
    - 致命的問題の有無と根拠
- 評価結果は Structured Output で受け取るとする

## 「ファイルごとの評価」の Structured Output schema

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": [
    "target_oracle_path",
    "referenced_paths",
    "specification_only_basis",
    "issues"
  ],
  "properties": {
    "target_oracle_path": {
      "type": "string",
      "description": "評価対象 oracle ファイルの絶対パス。"
    },
    "referenced_paths": {
      "type": "array",
      "description": "評価時に参照した oracle / INDEX ファイルの絶対パス。対象 oracle 自身も含める。",
      "items": {
        "type": "string"
      }
    },
    "specification_only_basis": {
      "type": "string",
      "description": "この評価が oracles 配下の仕様断片と INDEX だけに基づくことの説明。"
    },
    "issues": {
      "type": "array",
      "description": "評価対象 oracle から検出した問題点。問題がない場合は空配列。",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "severity",
          "title",
          "oracle_path",
          "oracle_line_start",
          "oracle_line_end",
          "affected_workflow",
          "requirement",
          "problem",
          "reason",
          "suggested_oracle_change"
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
            "description": "問題点の根拠となる oracle ファイルの絶対パス。通常は target_oracle_path と同じだが、関連 oracle 側に問題がある場合はそのファイルを指してよい。"
          },
          "oracle_line_start": {
            "type": ["integer", "null"],
            "description": "問題点の根拠となる oracle 記述の開始行。特定できない場合は null。"
          },
          "oracle_line_end": {
            "type": ["integer", "null"],
            "description": "問題点の根拠となる oracle 記述の終了行。特定できない場合は null。"
          },
          "affected_workflow": {
            "type": "string",
            "description": "影響を受ける workflow / subcommand / concept。例: cmoc apply, cmoc eval-oracles, overall。"
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
          }
        }
      }
    }
  }
}
```

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
- `deleted_oracles_detected`
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

1. `# cmoc eval-oracles report`
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
| 1 | `oracles/app_specs/sub_commands/eval_oracles.md` | 2 |
| 2 | `oracles/app_specs/workflow.md` | 0 |
```

### `Fatal issues`

`severity = fatal` の問題点を、問題点単位で列挙する。

例:

```markdown
### FATAL-001: レポートの成功判定条件が曖昧

- Oracle file: `oracles/app_specs/sub_commands/eval_oracles.md`
- Lines: `72-80`
- Affected workflow: `cmoc eval-oracles`
- Requirement:
  - 評価結果を人間が判断可能な形でレポートする。
- Problem:
  - レポート本文の形式が固定されておらず、致命的問題の有無を安定して確認できない。
- Reason:
  - `cmoc eval-oracles` の中核目的は oracle スナップショットの致命的問題を人間に報告することだが、報告形式が曖昧だと作業完了を判断できない。
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

- 評価レポートは `<repo-root>/.cmoc/reports/eval-oracles/<time-stamp>.md` にファイルに保存する
- レポートファイルのフルパスを stdout に流す
