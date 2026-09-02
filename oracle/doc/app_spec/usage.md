# cmoc 使用方法

## 呼び出し方法

- `{{cmoc-root}}/bin` を環境変数 `PATH` に追加し、`cmoc` コマンドで呼び出す。

## 最初に 1 回だけ行うこと

1. 人間が `cmoc doctor` を呼び出す。

## 想定 workflow

1. 人間が作業対象の `{{local-branch}}` へ移動する。
2. 人間が `cmoc session fork` を呼び出す。
    - cmoc は現在の branch を `{{cmoc-session-home-branch}}` として記録する。
    - cmoc は `{{cmoc-session-branch}}` を作成して checkout する。
3. 短い仕様変更・実装変更 loop を繰り返す。
    1. 必要に応じて `cmoc oracle investigation` で read-only の調査を行う。
    2. 人間が oracle file を直接編集するか、main worktree の active な `{{cmoc-session-branch}}` 上で `cmoc oracle edit` を呼び出す。
    3. 人間が oracle file の変更を commit または破棄する。破棄した場合は必要に応じて loop の先頭へ戻る。
    4. 人間が `cmoc realization apply fork` を呼び出す。
    5. 人間が `cmoc run join` で apply run を取り込むか、`cmoc run abandon` で破棄する。
    6. 人間が現状の実装で問題ないと判断するまで繰り返す。
4. 必要に応じて、ファイル単位の網羅的な追従を行う。
    1. 人間が `cmoc realization refactor fork` を呼び出す。
    2. 人間が `cmoc run join` で確定済み成果物を取り込むか、`cmoc run abandon` で破棄する。
    3. 調査要求が残っている場合は、join 後に新しい `cmoc realization refactor fork` を開始する。
5. 必要に応じて、人間が `cmoc feedback report` を呼び出す。
    - session worktree と staging area は clean にする。
    - cmoc は run 上で安全な realization file の修正を issue ごとに commit し、処理中の新しい issue も intake wave で可能な限り処理する。
    - 正常経路では run を自動 join し、`human_required` issue だけを report する。`inconclusive` があれば `incomplete` 診断 report を保存する。
    - 自動 join 前に run が残った場合は `cmoc run join` または `cmoc run abandon` を使用する。自動 join 後の publication または cleanup は、次の `cmoc feedback report` が再開する。
6. 人間が `{{cmoc-session-branch}}` 上で `cmoc session join` を呼び出す。
    - cmoc は `{{cmoc-session-branch}}` を `{{cmoc-session-home-branch}}` へ merge する。

## workload の使い分け

各 workload の目的と境界は、次の仕様を正本とする。

- realization apply: `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_apply.md` の「目的」
- realization refactor: `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「目的」
- oracle edit: `{{cmoc-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md` の「目的」
- feedback report: `{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の `cmoc feedback report`

editing run に共通する lifecycle は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「編集 run の共通仕様」を参照する。
