# 人間向け feedback subsystem

## 目的

feedback subsystem は、cmoc が起動した Codex の作業中に判明した問題から、現在も未解決であり、作業外にいる人間の対応が必要な issue だけを提示する。

feedback state は、現在の report に必要な小さな active state として管理する。

観測源は次の 2 種類に限定する。

- agent が共通 MCP tool `cmoc_feedback.submit_observation` を使って自己申告した内容
- cmoc が allowlist 済み rule で構造化 log event から検出した diagnostic

観測時点では raw observation だけを保存する。issue の集約と現在状態の検証は、`cmoc feedback report` が呼ばれるまで行わない。

## 正本仕様の構成

feedback の詳細は、責務ごとに次の正本仕様へ分ける。同じ schema、判断基準、または lifecycle を複数文書へ重複させない。

- `{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md`
    - local stdio MCP reporter/client、collector、共通 prompt instruction、機械 detector、および raw observation を定める。
- `{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md`
    - repository-local な active issue、threshold 未満の machine aggregate、report cut の一時 state、および atomic publication を定める。
- `{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md`
    - `cmoc feedback report` の事前条件、機械処理、normalization、verification、再開、および表示を定める。

## 用語と責務

feedback の処理段階は、観測、同一性判断、現在状態の検証、および publication を混在させない。

- observation
    - 1 回の作業中に観測された事実、または agent の自己申告である。
    - active state へ反映されるまでは pending な raw observation として保存する。
- issue candidate
    - 機械的な検証、deduplication、集約、および必要な normalization を通過し、verification の対象となった問題候補である。
    - 候補であることだけを理由に人間向け report へ掲載してはならない。
- active issue
    - report cut 時点で `unresolved` と検証された issue である。
    - 現在の人間向け report と次回 verification に必要な compact record を 1 件だけ持つ。
- report cut
    - 1 回の report が評価する pending observation、直前の active state、および現在状態の参照を固定した入力境界である。
- normalization agent
    - 機械的な完全一致では決められない agent observation と既存 issue candidate の同一性だけを判断する agent である。
- verification agent
    - report cut で固定した参照だけから、各候補を `unresolved | resolved | not_actionable | inconclusive` のいずれかへ分類する agent である。
- feedback report
    - 全候補の verification が確定した場合だけ publication される人間向け成果物である。
    - issue 一覧には `unresolved` だけを含める。

normalization agent は現在性、actionability、または report 掲載可否を判断しない。verification agent は候補外の問題を探索せず、feedback state または根拠となった対象を編集しない。

問題が現在も存在するかは、report cut ごとの verification verdict だけで判断する。

agent-facing の送信面は、call-scoped な local stdio MCP reporter/client が公開する `cmoc_feedback.submit_observation` だけとする。MCP reporter/client は request を invocation-scoped collector へ転送する。保存 context は collector が call capability から確定し、raw observation は collector だけが `.cmoc/gu` へ atomic に保存する。agent と MCP reporter/client は保存先を直接操作しない。

全体のデータフローを次に示す。

```text
agent
  -> Codex MCP tool `cmoc_feedback.submit_observation`
  -> call-scoped local stdio MCP reporter/client
  -> invocation-scoped collector IPC ----------------+
                                                      +-> cmoc collector -> pending observation --+
structured log event -> allowlist detector -----------+                                         |
                                                                                                 v
previous active state ---------------------------------------------------------------> cmoc feedback report
                                                                                                 |
                                               deterministic processing -> normalization -> verification
                                                                                                 |
                                                         atomic publication -> current active state + Markdown report
```

raw observation、active state、および report の一時 state は `{{repo-root}}/.cmoc/gu` に属する。session または run の join と abandon は、feedback state を取り込み、破棄、または巻き戻さない。feedback state の別 clone、別 machine、または Git remote への複製は保証しない。

## non-goal

feedback は診断と人間への提示だけに使用する。次の用途には使用しない。

- 各 agent call の Structured Output への共通 field または共通自己申告要件の追加
- Codex call 終了後に別の agent が raw call log を読み直す問題発見
- agent による feedback 保存 file の直接編集
- 自然言語 error message への広範な正規表現など、不安定な根拠による機械検出
- task の成功判定、run state、他サブコマンドの終了コード、retry、または自動 recovery の入力
- agent-facing transport の変更を理由とする normalization、verification、active state、または report semantics の変更
- issue または AI-generated kaizen の後続 Codex call への自動注入
- sandbox、config、oracle file、realization file、または feedback の根拠となった対象の自動修正
- report-time agent による候補外の新規問題探索
- 別 clone または別 machine への feedback state の複製

用途が 1 種類へ閉じた normalization agent call と verification agent call には、その call 固有の Structured Output を使用する。

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

次の成果物は feedback observation または active issue ではない。明示的な reporter submission または allowlist rule がない限り、自動変換しない。

- realization refactor の findings、resolution、および unresolved target
- oracle review の findings と verdict
- indexing の結果
- Structured Output の固有 field
- run、session、および TUI の完了結果

既存成果物を evidence として参照する場合も、その成果物固有の判定基準、保存先、lifecycle、および終了コードを維持する。

### TUI、中断、および異常終了

TUI の複数 turn は 1 TUI process の Codex call context に対応付ける。accepted observation は TUI の終了理由にかかわらず保存する。

subcommand のユーザー中断後は、新しい normalization、verification、または発見用 agent call を開始しないという既存規則を維持する。中断までに reporter が accepted を返した observation は、本命成果物の commit または rollback と独立して保持する。

feedback report、active issue、および AI-generated kaizen を後続 Codex call へ自動注入してはならない。この境界は `{{cmoc-root}}/oracle/doc/considered_alternative/memory_alternative.md` と同じ方針に従う。
