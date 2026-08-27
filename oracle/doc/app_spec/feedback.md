# 人間向け feedback

## 目的

feedback subsystem は、cmoc の作業中に見つかった問題のうち、現在も未解決であり、現在の作業外にいる人間の対応が必要なものだけを正常 report で提示する。

verification verdict が `inconclusive` の candidate がある場合は、正常 publication を行わない。代わりに、確定済みの判定と判定不能の原因を `incomplete` 診断 report で提示する。

feedback は診断と報告のための独立した仕組みである。feedback の有無や内容は、本命 workload の成功判定、state、retry、または recovery を変更しない。`cmoc feedback report` 自身の成否だけは、同サブコマンドの終了結果へ反映する。

観測源は、次の 2 種類に限定する。

- agent が `cmoc_feedback.submit_observation` で自己申告した observation
- cmoc が allowlist 済み rule で構造化 log event から生成した observation

観測時には raw observation だけを保存する。issue の同一性判断と現在状態の検証は、`cmoc feedback report` の実行時に行う。

## 処理モデル

feedback は、観測時の申告と report 時の判断を分離する。

| 用語 | 意味 |
|---|---|
| observation | 1 回の作業で観測された事実または申告。report へ反映されるまでは pending とする。 |
| issue candidate | observation と直前の active state から組み立てた検証対象。候補であるだけでは人間向け report に掲載しない。 |
| active issue | report cut 時点で `unresolved` と検証された issue。次回の検証に必要な compact record を保持する。 |
| report cut | 1 回の report が評価する observation、直前の active state、および現在状態の参照を固定した入力境界。 |
| feedback report | 全 candidate が `unresolved | resolved | not_actionable` のいずれかに確定した場合に、正常 publication する active state と Markdown report の組。 |
| `incomplete` 診断 report | 全 candidate の verification output を受理でき、1 件以上が `inconclusive` だった場合に保存する Markdown report。正常 publication と active state には含めない。 |

issue の同一性を機械的に確定できない場合だけ、normalization agent を使用する。normalization agent は、入力候補との同一性だけを判断する。

各 issue candidate の現在性と actionability は、verification agent が `unresolved | resolved | not_actionable | inconclusive` のいずれかで判断する。正常 report には `unresolved` だけを掲載する。`inconclusive` は active issue にせず、`incomplete` 診断 report にだけ掲載する。

全体の流れを次に示す。

```text
agent submission ─┐
                  ├─> pending observation ─> report cut ─> normalization ─> verification
machine detector ─┘                                                        │
                                                                            ├─> normal publication
                                                                            │    active state + Markdown report
                                                                            └─> incomplete diagnostic
                                                                                 Markdown report only
```

## 正本仕様の分担

feedback の仕様は、責務ごとに次の文書へ分ける。同じ schema、判断基準、または state transition を複数文書で定義しない。

| 正本仕様 | 決めること |
|---|---|
| `{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「feedback observation の収集」 | observation の報告基準、収集経路、受け入れ検査、機械 detector、および raw 保存 |
| `{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「feedback の repository-local state」 | repository-local state、report cut、checkpoint、atomic publication、および cleanup |
| `{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の `cmoc feedback report` | `cmoc feedback report` の事前条件、処理順序、normalization、verification、表示、および終了結果 |

## 共通原則

feedback report、`incomplete` 診断 report、active issue、および AI-generated kaizen を、後続の Codex call へ自動注入しない。

別 clone、別 machine、または Git remote への feedback data の複製は保証しない。

## 既存 workload との境界

既存 workload の成果物は、明示的な agent submission または allowlist rule がない限り、observation や active issue へ自動変換しない。

自動変換しない成果物には、次のものが含まれる。

- realization refactor の finding、resolution、および unresolved target
- oracle review の finding と verdict
- indexing の結果
- agent call 固有の Structured Output
- run、session、および TUI の完了結果

realization 作業中に oracle の問題を自己申告するのは、oracle file 間の矛盾、要求の実現不能、または外部挙動を左右する人間意図の選択が必要な場合に限る。実装詳細が未定義であること、複数の妥当な実装があること、または一般的な改善案だけを報告してはならない。

accepted observation は、TUI の終了、ユーザー中断、または Codex process の異常終了にかかわらず保持する。本命成果物の commit または rollback と連動させない。

## non-goal

feedback subsystem は、次の処理を行わない。

- agent に feedback 保存 file を直接編集させること
- 各 agent call の Structured Output へ共通 feedback field を追加すること
- raw call log を後から別 agent に読ませて新しい問題を探索すること
- 自由文の広範な正規表現など、不安定な根拠から machine observation を作ること
- sandbox、config、oracle file、realization file、または問題の根拠を自動修正すること
- issue を task の成功判定、run state、retry、または自動 recovery の入力にすること
- 過去の report を active state、deduplication、または最新 report の判定に使用すること
