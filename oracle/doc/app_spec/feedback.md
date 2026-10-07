# repair-first feedback

## 目的

feedback subsystem は、cmoc の作業中に見つかった問題を収集し、`cmoc feedback report` で安全な automatic remediation を先に完了する。

利用者が通常の確認・操作対象とするのは、最新状態に残る未終了の案件である。人間対応が必要だと確認できた案件と、許可された情報では判定できない案件を区別して提示する。自動修正済みの問題や終了した案件の経緯は history に分離する。

人間が外部で解決した `inconclusive` 案件は、`cmoc feedback close` で明示的に終了できる。過去の終了を再発の抑止には使用しない。

feedback の有無や内容は、feedback 以外の workload の成功判定、state、retry、または recovery を変更しない。feedback コマンド自身の run、merge、publication、および終了結果は、各サブコマンドの成否として扱う。

観測源は、次の 2 種類に限定する。

- agent が `cmoc_feedback.submit_observation` で自己申告した observation
- cmoc が allowlist 済み rule で構造化 log event から生成した observation

観測時には raw observation だけを保存する。issue identity の確定、現在状態の確認、修正、および結果分類は、`cmoc feedback report` の実行時に行う。

## 用語と結果分類

feedback 全体で使用する用語と issue remediation の結果を次に示す。他の oracle file は、この表の意味を再定義せず参照する。

| 用語 | 意味 |
|---|---|
| observation | 1 回の作業で観測された事実または申告。publication で入力の消費が確定するまでは pending とする。 |
| issue candidate | observation と直前の active state から組み立てた、identity 確定前または remediation 前の候補。 |
| issue identity | normalization 後に同一 issue として扱う安定した識別単位。 |
| issue ID | issue identity を表す識別子。案件 ID とは区別する。 |
| 案件 | ある issue を未解決として登録してから終了するまでの対応単位。案件 ID で指定し、終了後の再発には別の案件 ID を使用する。 |
| active issue | 最新状態に残る未終了の案件。最新の agent 判定は `human_required` または `inconclusive` である。 |
| 最新状態 | 最後に publication で確定した active の集合とその判定・根拠。確定後の未確認の変化まで検証済みであることは表さない。 |
| history（履歴） | 更新前の判定と、問題の解決・案件終了の経緯を保持する記録。通常の問題一覧とは分離する。 |
| 手動クローズ | 外部解決を確認した人間が、理由を伴う宣言によって `inconclusive` 案件を終了する操作。agent の remediation result ではない。 |
| intake wave | 1 回の feedback remediation run 内で固定した、未処理または再確認対象の issue identity と根拠の immutable な入力集合。 |
| high-watermark | collector が durable に受理済みであることを atomic に確定した observation の上限境界。 |
| 判定根拠 | issue の結果分類が依存した状態。対象ファイルに加え、依存設定、検査の条件と結果など、判断に必要な根拠を含む。 |
| 有効な結果 | 現在の状態に対して判定根拠の有効性を確認でき、再確認を必要としない issue の結果。 |
| `fixed` | realization file の修正と必要な検証が完了した。現在の案件一覧へ掲載しない。 |
| `already_resolved` | 処理時点ですでに問題が存在しない。現在の案件一覧へ掲載しない。 |
| `not_actionable` | feedback の報告基準を満たさない。現在の案件一覧へ掲載しない。 |
| `human_required` | 問題が現在も存在し、oracle の変更、人間意図の確定、外部状態の変更など、realization file の編集だけでは満たせない具体的な対応が必要である。現在の案件一覧へ掲載する。 |
| `inconclusive` | 許可された情報では結果を判定できない、または再確認・再修正が同じ状態を往復して収束できないことが確認された。具体的な理由を持つ `incomplete` 診断として扱い、`human_required` へ変換しない。 |
| invocation error | agent call failure、Structured Output 受理失敗、差分検査失敗、commit 失敗、merge 失敗、publication 失敗など、feedback issue の状態ではなく invocation の処理失敗である。issue remediation の結果へ変換しない。 |

理論上は realization file だけで修正できる可能性がある問題は、今回の agent call で完了できなかったという理由だけで `human_required` としてはならない。

agent の判定は、その時点の判定根拠に対する結果である。`cmoc feedback report` の後続処理で判定根拠が変わった場合は、結果分類を問わず再確認を必要とする。ファイル内容の変化だけで旧判定の誤りや問題の解消を断定してはならない。また、記載された 1 ファイルが不変であることだけを、判定全体の有効性の証明にしてはならない。

判定根拠の表現と変更検知の具体的なアルゴリズムは、これらの要求を満たす範囲で実装者へ委ねる。

### 最新状態の要約

最新状態の要約は、active に `inconclusive` があれば `incomplete`、それがなく `human_required` があれば `attention`、どちらもなければ `ok` とする。`incomplete` の確定は、判定不能という結果を保存できたことを表し、問題の解決や判定の成功へ読み替えない。

この要約と、状態を更新・確認しようとした invocation の成否は区別する。invocation error によって新たな issue result を作らない。確定点前後の失敗で保持する状態は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「最新状態の atomic publication」に従う。

## 処理モデル

`cmoc feedback report` は、同一 invocation 内で自己完結する feedback remediation run を使用する。run branch 上で、issue ごとの remediation と commit を逐次実行する。処理中に受理された新しい issue も、immutable な intake wave として可能な限り処理する。

issue の結果分類を確定するための再確認と必要な再修正・判定更新は、同じ invocation 内で report cut の封印前に完了する。wave loop の自然完了の条件は、最終 high-watermark までに新しい未処理 issue identity がなく、run branch の最終状態に対して再確認が必要な判定も残っていないことである。

封印後の自動 join では、封印済み結果を維持するためのマージ調整と検証を認める。調整の範囲、検証記録、publication の停止条件、および join 後の recovery は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「自動 join と join 後の確定」と「join 後の publication failure」を正本とする。report の publication は、join 後の状態に対して有効な結果だけで確定する。

自動 join と必要な検証が成功した report は、`inconclusive` を含む場合も最新状態を publication する。未終了の案件は次回の report で active の記録から再確認する。手動 close の CLI と対象判定は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_close.md` の「CLI 契約」「対象と理由」を正本とする。

## 正本仕様の分担

feedback の仕様は、責務ごとに次の正本へ分ける。同じ schema、判断基準、または state transition を複数箇所で定義しない。

| 正本仕様 | 決めること |
|---|---|
| 本書の「用語と結果分類」「最新状態の要約」 | feedback 共通の用語、agent の結果分類、および最新状態の要約 |
| `{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「feedback observation の収集」 | observation の報告基準、収集経路、受け入れ検査、機械 detector、および raw 保存 |
| `{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「feedback の repository-local state」 | 最新状態と履歴の保存、identity と案件の対応・遷移、intake wave、high-watermark、checkpoint、publication、および入力の消費・cleanup |
| `{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の `cmoc feedback report` | CLI の事前条件、run、normalization、issue 処理単位、agent call、commit、merge、publication、表示、および終了結果 |
| `{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_close.md` の `cmoc feedback close` | 手動クローズの CLI、対象・理由、事前条件、再実行・recovery、表示、および終了結果 |
| `{{cmoc-root}}/oracle/doc/app_spec/id.md` の「共通 ID」 | 案件 ID を含む共通 ID の書式と採番 |

正確な agent 向け prompt、Structured Output schema、および agent call 設定は、各意味仕様が明示する oracle src へ委譲する。

## 既存 workload との境界

既存 workload の成果物は、明示的な agent submission または allowlist rule がない限り、observation や active issue へ自動変換しない。

自動変換しない成果物には、次のものが含まれる。

- realization refactor の finding、resolution、および unresolved target
- agent call 固有の Structured Output
- run、session、および TUI の完了結果
- feedback remediation run 自身の agent、tool、validation、差分検査、commit、merge、publication、または orchestration の失敗

realization 作業中に oracle の問題を自己申告できるのは、次の場合に限る。

- oracle file 間に矛盾がある
- 要求を実現できない
- 外部挙動を左右する人間意図の選択が必要である

実装詳細が未定義であること、複数の妥当な実装があること、または一般的な改善案だけを報告してはならない。

accepted observation は、TUI の終了、ユーザー中断、または Codex process の異常終了にかかわらず保持する。本命成果物の commit または rollback と連動させない。

## 共通原則

- feedback の report、active issue、および history を、通常の後続 Codex call へ自動注入しない。
- AI-generated kaizen を後続の Codex CLI 呼び出しへ自動注入しない。kaizen の意味と非注入の理由は、`{{cmoc-root}}/oracle/doc/considered_alternative/memory_alternative.md` の「AI-generated kaizen を自動的に次回実行へ反映しない理由」を参照する。
- 別 clone、別 machine、または Git remote への feedback data の複製は保証しない。
- realization apply と realization refactor の既存の意味を変更しない。refactor state を feedback issue queue として流用しない。

## non-goal

feedback subsystem は、次の処理を行わない。

- 各 agent call の Structured Output へ共通 feedback field を追加すること
- raw call log を後から別 agent に読ませて新しい問題を探索すること
- 自由文の広範な正規表現など、不安定な根拠から machine observation を作ること
- realization file 以外の変更で issue を自動解決すること
- write 権限を持つ issue remediation agent を並列実行すること
- 過去の Markdown report を active state、deduplication、または最新 report の判定に使用すること
- `inconclusive` 以外への手動 close の拡張、reopen、恒久 suppression、または履歴管理用の追加 CLI
- 手動クローズを agent の自動判定へ混ぜるための Structured Output 拡張
