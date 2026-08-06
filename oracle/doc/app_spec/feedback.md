# 人間向け feedback subsystem

## 目的

feedback subsystem は、cmoc が起動した Codex の作業中に判明した人間対応対象を、全 session の途中経過を読み直さなくても把握できる形へ集約する。

観測源は次の 2 種類に限定する。

- agent が共通 MCP tool `cmoc_feedback.submit_observation` を使って自己申告した内容
- cmoc が allowlist 済み rule で構造化 log event から検出した diagnostic

観測時点では raw observation だけを保存する。人間向け issue への意味的な正規化は、`cmoc feedback report` が呼ばれるまで行わない。

## 正本仕様の構成

feedback の詳細は、責務ごとに次の正本仕様へ分ける。同じ schema、判断基準、または状態遷移を複数文書へ重複させない。

- `{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md`
    - local stdio MCP reporter/client、collector、共通 prompt instruction、機械 detector、および raw observation を定める。
- `{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md`
    - normalized issue、machine assessment、human disposition、および増分処理 record を定める。
- `{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md`
    - `cmoc feedback report` の事前条件、増分 normalization、commit、再開、および表示を定める。

## non-goal

feedback は診断と人間への提示だけに使用する。次の用途には使用しない。

- 各 agent call の Structured Output への共通 field または共通自己申告要件の追加
- Codex call 終了後に別の agent が raw call log を読み直す問題発見
- agent による feedback 保存 file の直接編集
- 自然言語 error message への広範な正規表現など、不安定な根拠による機械検出
- task の成功判定、run state、他サブコマンドの終了コード、retry、または自動 recovery の入力
- agent-facing transport の変更を理由とする feedback normalization、state、または report semantics の変更
- issue または AI-generated kaizen の後続 Codex call への自動注入
- sandbox、config、oracle file、realization file、または feedback の根拠となった対象の自動修正

normalization 専用 agent call のように、用途が 1 種類へ閉じた成果物契約には、その call 固有の Structured Output を使用してよい。

## 用語と責務

feedback の状態は、実行記録、機械評価、人間判断を混在させない。

- observation
    - 1 回の作業中に観測された事実、または agent の自己申告である。
    - 保存後に変更しない実行記録である。
- issue
    - 1 件以上の observation を、同じ人間対応対象として正規化した論理 aggregate である。
    - 安定した issue ID を持つ。
- machine assessment
    - 現在も問題が存在する可能性と、現在状態に対する再検証の必要性を、cmoc または normalization agent が評価した記録である。
- human disposition
    - 人間が決定した `open | acknowledged | resolved | ignored | superseded` のいずれかの状態である。
    - 人間がまだ判断していない状態は、disposition record が存在しないことで表す。機械が `open` を初期値として作成してはならない。
- feedback report
    - issue、machine assessment、および human disposition を、人間の認知負荷が低い形へ決定論的にレンダリングした成果物である。

machine assessment と human disposition は別 record とする。agent、collector、detector、normalizer、および report renderer は、human disposition record を作成、変更、削除、または別状態として解釈してはならない。

agent-facing の送信面は、call-scoped な local stdio MCP reporter/client が公開する `cmoc_feedback.submit_observation` だけとする。MCP reporter/client は request を invocation-scoped collector へ転送する。保存 context は collector が call capability から確定し、raw observation は collector だけが `.cmoc/gu` へ atomic に保存する。agent と MCP reporter/client は保存先を直接操作しない。

全体のデータフローを次に示す。

```text
agent
  -> Codex MCP tool `cmoc_feedback.submit_observation`
  -> call-scoped local stdio MCP reporter/client
  -> invocation-scoped collector IPC ----------------+
                                                      +-> cmoc collector -> raw observation -> cmoc feedback report -> tracked issue state -> report
structured log event -> allowlist detector -----------+                                                                    ^
                                                                                                                           |
human disposition ---------------------------------------------------------------------------------------------------------+
```

## 既存 workload との接続

### realization 作業中の oracle 問題

`cmoc realization apply fork` 固有の agent call と report の接続は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_apply.md` を正本とする。

realization 作業中に oracle 起因として自己申告するのは、次のように人間意図が必要な場合に限る。

- oracle file 間の矛盾
- oracle 要求の実現不能
- 外部挙動を左右する人間意図の選択
- どの解釈でも別の明示要求へ違反する状態

実装詳細が未定義であること、複数の妥当な実装があること、または一般的な改善案だけを oracle 問題として報告してはならない。

### 固有成果物との分離

次の成果物は feedback observation または human disposition ではない。明示的な reporter submission または allowlist rule がない限り、自動変換しない。

- realization refactor の findings、resolution、および unresolved target
- oracle review の findings と verdict
- indexing の結果
- Structured Output の固有 field
- run、session、および TUI の完了結果

既存成果物を evidence として参照する場合も、その成果物固有の判定基準、保存先、lifecycle、および終了コードを維持する。

### TUI、中断、および異常終了

TUI の複数 turn は 1 TUI process の Codex call context に対応付ける。accepted observation は TUI の終了理由にかかわらず保存する。

subcommand のユーザー中断後は新しい normalization や発見用 agent call を開始しないという既存規則を維持する。中断までに reporter が accepted を返した observation は、本命成果物の commit または rollback と独立して保持する。

feedback report、issue、assessment、および AI-generated kaizen を後続 Codex call へ自動注入してはならない。この境界は `{{cmoc-root}}/oracle/doc/considered_alternative/memory_alternative.md` と同じ方針に従う。
