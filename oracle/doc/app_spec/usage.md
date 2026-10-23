# cmoc 使用方法

## 呼び出し方法

- `{{cmoc-root}}/bin` を環境変数 `PATH` に追加し、`cmoc` コマンドで呼び出す。

## 準備・修復と索引更新

処理対象の work-root で `cmoc doctor` を呼び出す。通常起動で準備不足を案内された場合も、診断に従って修復する。処理内容、正常終了の意味、および結果の確認先は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/doctor.md` の「cmoc doctor」に従う。

## 想定 workflow

1. 人間が作業対象の `{{local-branch}}` へ移動する。
2. 人間が `cmoc session fork` を呼び出す。
    - cmoc は現在の branch を `{{cmoc-session-home-branch}}` として記録する。
    - cmoc は `{{cmoc-session-branch}}` を作成して checkout する。
3. 人間が現状の実装で問題ないと判断するまで、仕様変更と実装変更の短い loop を繰り返す。
    1. 必要に応じて `cmoc oracle investigation` で read-only の調査を行う。
    2. 人間が oracle file を直接編集するか、main worktree の active な `{{cmoc-session-branch}}` 上で `cmoc oracle edit` を呼び出す。
    3. 人間が oracle file の変更を commit または破棄する。破棄した場合は必要に応じて loop の先頭へ戻る。
    4. 人間が `cmoc realization apply` を呼び出す。cmoc は追従作業を確定し、同じ invocation 内で session branch へ自動 join して終了する。
4. 必要に応じて、仕様への適合と必要な回帰検出能力を保ち、テストと実装のムダを網羅的に削減する。
    1. 人間が `cmoc realization refactor` を呼び出す。
    2. 巡回の進捗、確定済み変更、測定済みのテスト時間を見て、人間が適当な時点で `Ctrl+C` を押す。変更なしの巡も反復し、全件処理や数値目標の達成では自動終了しない。
    3. cmoc は子 process の停止と未確定作業の rollback を終え、確定済み成果物と refactor state を自動 join して正常中断を完了する。
    4. 続ける場合は、新しい `cmoc realization refactor` を開始する。選択順序は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「調査対象の選択」に従い、同じ run の実行途中は復元しない。
5. 必要に応じて、人間が `cmoc feedback report` を呼び出す。
    - session worktree と staging area は clean にする。
    - cmoc は run 上で安全な realization file の修正を issue ごとに commit し、処理中の新しい issue も intake wave で可能な限り処理する。
    - 自然完了では、自動 join と必要な検証の成功後、最新状態と publication report を確定する。今回の primary report には最終 state と cleanup の結果も載せる。現在の案件一覧には `human_required` と `inconclusive` を区別して示し、過去の経緯は history から確認する。
    - `Ctrl+C` による正常中断では、実行中の処理を停止・整合化し、確定済み issue commit を成果として自動 join する。publication は行わず、保持した observation と最新の active record を次回 report で再確認する。
    - `inconclusive` があれば結果は `incomplete` となるが、案件 ID と判定根拠は active に保存される。以後の確認・操作には最新状態の案件 ID を使う。
    - 人間が外部で解決を確認した `inconclusive` 案件は、`cmoc feedback close <案件ID> --reason "外部で修正し、人間が解決を確認した"` で閉じる。成功直後の最新一覧から対象が除かれ、理由と経緯は history に残る。
    - 後から同じ問題が観測された場合も、通常の検出・判定を経て新しい案件として現れる。以前の案件 ID に対する close の再実行は再発分へ作用しない。
6. 人間が `{{cmoc-session-branch}}` 上で `cmoc session join` を呼び出す。
    - cmoc は `{{cmoc-session-branch}}` を `{{cmoc-session-home-branch}}` へ merge する。

## 異常時の run 復旧

正常終了した workload に追加の手動 join は不要である。異常時は primary report の失敗段階・残存資源・次の操作を確認し、`cmoc run join` で取り込みを再試行するか確定済み部分成果を取り込み、または `cmoc run abandon` で残る隔離資源を破棄する。取り込み済みの session commit は abandon でも取り消されない。

自然完了経路で自動 join 済みの feedback run は、`cmoc feedback report` で未完了の確定処理を再開する。中断後の非 publication 経路は共通の手動復旧に従う。各操作の可否は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「join の失敗と復旧」を参照する。

## workload の使い分け

各 workload の目的と境界は、次の仕様を正本とする。

- realization apply: `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_apply.md` の「目的」
- realization refactor: `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「目的」
- oracle edit: `{{cmoc-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md` の「目的」
- feedback report: `{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の `cmoc feedback report`
- feedback close: `{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_close.md` の `cmoc feedback close`

editing run に共通する lifecycle は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「編集 run の共通仕様」を参照する。

## TUI の会話を続ける

例えば、終了済みの `cmoc tui` または `cmoc oracle investigation` の実行 ID が `exec_000010_2026-09-29_15-04` なら、同じ repository で次のように再開する。

```bash
cmoc resume exec_000010_2026-09-29_15-04
```

元の TUI 種別は実行ログから自動判定される。入力エディタを経由せず、追加指示は再開した TUI で入力する。今回表示される新しい実行 ID も、終了後に次の `cmoc resume` に指定できる。

再開する会話は、`{{cmoc-root}}/oracle/doc/app_spec/codex_tui_rule.md` の「TUI の固定 session ID」に従う。初回 exec の成功後に TUI の準備・起動が失敗した場合や、TUI が異常終了した場合も、下記の適格性を満たせば同じ入口で再開できる。元の prompt は再送せず、初回作業を繰り返さない。初回 exec 自体の失敗・取消は再開対象外とする。

`cmoc oracle edit` など非 TUI の実行 ID は拒否される。対象条件・ログ不足や未終了時の拒否・会話選択は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/resume.md` の「ログからの種別解決」「対象の適格性と会話選択」を参照する。ID の書式と採番は、`{{cmoc-root}}/oracle/doc/app_spec/id.md` の「ID のフォーマット」「採番と順序保証」を共用する。
