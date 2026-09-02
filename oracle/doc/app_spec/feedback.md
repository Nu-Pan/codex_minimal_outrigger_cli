# repair-first feedback

## 目的

feedback subsystem は、cmoc の作業中に見つかった問題を収集し、`cmoc feedback report` で安全な automatic remediation を先に完了する。

正常な feedback publication は、automatic remediation 後も realization file の編集だけでは解決できず、現在の作業外にいる人間の対応が必要な issue だけを提示する。自動修正済みの issue は active issue または正常な人間向け issue 一覧へ残さない。

`inconclusive` の issue がある場合は、正常 publication を行わない。代わりに、確定済みの結果と判定不能の原因を `incomplete` 診断 report で提示する。

feedback の有無や内容は、feedback report 以外の workload の成功判定、state、retry、または recovery を変更しない。`cmoc feedback report` 自身の run、merge、publication、および終了結果は、同サブコマンドの成否として扱う。

観測源は、次の 2 種類に限定する。

- agent が `cmoc_feedback.submit_observation` で自己申告した observation
- cmoc が allowlist 済み rule で構造化 log event から生成した observation

観測時には raw observation だけを保存する。issue identity の確定、現在状態の確認、修正、および結果分類は、`cmoc feedback report` の実行時に行う。

## 用語と結果分類

feedback 全体で使用する用語と issue remediation の結果を次に示す。他の oracle file は、この表の意味を再定義せず参照する。

| 用語 | 意味 |
|---|---|
| observation | 1 回の作業で観測された事実または申告。正常 publication 後の cleanup 対象として確定するまでは pending とする。 |
| issue candidate | observation と直前の active state から組み立てた、identity 確定前または remediation 前の候補。 |
| issue identity | normalization 後に同一 issue として扱う安定した識別単位。 |
| active issue | 直近の正常 publication で `human_required` と確定した issue。次回の再確認に必要な compact record を保持する。 |
| intake wave | 1 回の feedback remediation run 内で固定した、未処理 issue identity と根拠の immutable な入力集合。 |
| high-watermark | collector が durable に受理済みであることを atomic に確定した observation の上限境界。 |
| `fixed` | realization file の修正と必要な検証が完了した。正常な issue 一覧へ掲載しない。 |
| `already_resolved` | 処理時点ですでに問題が存在しない。正常な issue 一覧へ掲載しない。 |
| `not_actionable` | feedback の報告基準を満たさない。正常な issue 一覧へ掲載しない。 |
| `human_required` | 問題が現在も存在し、oracle の変更、人間意図の確定、外部状態の変更など、realization file の編集だけでは満たせない具体的な対応が必要である。正常な issue 一覧へ掲載する。 |
| `inconclusive` | 許可された情報では結果を判定できない。`human_required` へ変換せず、`incomplete` 診断として扱う。 |
| invocation error | agent call failure、Structured Output 受理失敗、差分検査失敗、commit 失敗、merge 失敗、publication 失敗など、feedback issue の状態ではなく invocation の処理失敗である。issue remediation の結果へ変換しない。 |

理論上は realization file だけで修正できる可能性がある問題を、今回の agent call が完了できなかったことだけを理由に `human_required` としてはならない。

## 処理モデル

`cmoc feedback report` は、同一 invocation 内で自己完結する feedback remediation run を使用する。run branch 上で issue ごとの remediation と commit を逐次実行し、処理中に受理された新しい issue も immutable な intake wave として可能な限り処理する。

run branch を session branch へ自動 join した後に、join 後の tree を基準として publication を確定する。停止条件は、最終 high-watermark までに新しい未処理 issue identity がないことである。新しい異なる issue が継続的に発生する限り、自然完了しない。

## 正本仕様の分担

feedback の仕様は、責務ごとに次の正本へ分ける。同じ schema、判断基準、または state transition を複数箇所で定義しない。

| 正本仕様 | 決めること |
|---|---|
| `{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「feedback observation の収集」 | observation の報告基準、収集経路、受け入れ検査、機械 detector、および raw 保存 |
| `{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「feedback の repository-local state」 | repository-local state、intake wave、high-watermark、checkpoint、publication、および cleanup |
| `{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の `cmoc feedback report` | CLI の事前条件、run、normalization、issue 処理単位、agent call、commit、merge、publication、表示、および終了結果 |

正確な agent 向け prompt、Structured Output schema、および agent call 設定は、各意味仕様が明示する oracle src へ委譲する。

## 既存 workload との境界

既存 workload の成果物は、明示的な agent submission または allowlist rule がない限り、observation や active issue へ自動変換しない。

自動変換しない成果物には、次のものが含まれる。

- realization refactor の finding、resolution、および unresolved target
- indexing の結果
- agent call 固有の Structured Output
- run、session、および TUI の完了結果
- feedback remediation run 自身の agent、tool、validation、差分検査、commit、merge、publication、または orchestration の失敗

realization 作業中に oracle の問題を自己申告するのは、oracle file 間の矛盾、要求の実現不能、または外部挙動を左右する人間意図の選択が必要な場合に限る。実装詳細が未定義であること、複数の妥当な実装があること、または一般的な改善案だけを報告してはならない。

accepted observation は、TUI の終了、ユーザー中断、または Codex process の異常終了にかかわらず保持する。本命成果物の commit または rollback と連動させない。

## 共通原則

- feedback report、`incomplete` 診断 report、active issue、および AI-generated kaizen を、通常の後続 Codex call へ自動注入しない。
- 別 clone、別 machine、または Git remote への feedback data の複製は保証しない。
- realization apply と realization refactor の既存の意味を変更しない。refactor state を feedback issue queue として流用しない。

## non-goal

feedback subsystem は、次の処理を行わない。

- 各 agent call の Structured Output へ共通 feedback field を追加すること
- raw call log を後から別 agent に読ませて新しい問題を探索すること
- 自由文の広範な正規表現など、不安定な根拠から machine observation を作ること
- realization file 以外の変更で issue を自動解決すること
- write 権限を持つ issue remediation agent を並列実行すること
- issue を feedback report 以外の workload の成功判定、run state、retry、または recovery の入力にすること
- 過去の Markdown report を active state、deduplication、または最新 report の判定に使用すること
