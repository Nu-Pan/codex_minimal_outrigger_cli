# `cmoc realization refactor fork`

## 目的

realization refactor は、仕様への適合と必要な回帰検出能力を保ちながら、テストと実装のムダをファイル単位で網羅的に調査・削減し、テスト実行時間の短縮を図る workload である。全 oracle file と全 realization file を調査の起点にし、人間が `Ctrl+C` で止めるまで一巡を繰り返す。変更がない巡も継続する。

長時間の反復と、任意の段階から確定済み成果を取り込める状態へ速やかに正常終了できることを、並ぶ契約とする。停止要求に対して長い調査や検証の完了を待たせず、未確定作業を取り消し、検証済みの確定成果を保持する。

適合性の共通基準と refactor 固有の改善基準は、`{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization.md` の「oracle file に対する realization file の適合性」「realization refactor の改善判断」を正本とする。installed skill の有無で判断基準を変えない。直近の oracle 変更へ素早く追従する realization apply の目的は拡張しない。

## agent call への委譲

所見調査・修正 call の正確な prompt 文面、prompt part の選択、workload 固有の起動パラメータ、およびその選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/realization/refactor/fork/file_review_and_fix.py` の `build_realization_refactor_fork_file_review_and_fix_parameter` へ委譲する。所見、対応結果、および処理単位全体の検証結果を返す Structured Output の構造と field の意味は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/realization/refactor/fork/file_review_and_fix.json` のルート object へ委譲する。

fork、join、abandon の共通 lifecycle は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「編集 run の共通仕様」を正本とする。

## refactor state

### 保存先と JSON schema

refactor state の保存先は `{{work-root}}/.cmoc/gt/realization/refactor/state.json` とする。

JSON のトップレベルは、正規化済みの `{{work-root}}` 相対 path を key、各 file の調査状態を value とする object である。調査状態は、次の field を持つ object とする。

| field | 型・値 |
|---|---|
| `investigation_required` | boolean。再調査の要求があれば `true`。 |
| `last_investigation_result` | `not_investigated`、`no_findings`、`findings` のいずれか |
| `last_investigated_sha256` | 調査時点の file 内容に対する SHA256 文字列、または `null` |
| `last_investigated_at` | `{{time-stamp}}`、または `null` |

`last_investigated_at` は調査日時であり、`{{cmoc-root}}/oracle/doc/app_spec/timestamp.md` の「タイムスタンプのフォーマット」に従って保存する。ID は使用しない。

- `not_investigated` の entry は hash と日時をともに `null` とする。
- absolute path と `..` による `{{work-root}}` 外参照を禁止する。
- JSON object の記載順に意味を持たせない。
- state file は agent ではなく cmoc が更新する。

### entry 集合の同期

- entry の対象は、`{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization_file_enumeration.md` の「分類結果」に従い、同期時点で存在する全 oracle file と全 realization file の和集合とする。
- 対象 file と entry の過不足のない一致は、cmoc が同期を完了した時点の不変条件とする。同期時点には、doctor preprocess、refactor の各処理単位、run join 後などがある。人間の編集直後を含め、常時一致することは要求しない。
- 新規 file には `investigation_required=true`、`last_investigation_result=not_investigated`、hash と日時が `null` の entry を作成する。
- 削除 file の entry は削除する。rename は削除と追加として同期する。
- 現在の file の SHA256 が `last_investigated_sha256` と異なる場合は、既存の調査履歴を保持したまま `investigation_required=true` にする。
- 同期だけで既存の調査要求を解除したり、一巡を開始・完了したことにしたりしない。

### 調査履歴と巡回の区別

state は確定済みの調査履歴と再調査要求を次の fork へ引き継ぐ。`no_findings` や `investigation_required=false` は、改善余地の不存在、収束、または将来の巡での調査不要を意味しない。一巡内で調査機会を与えたかどうかは、この履歴とは区別して管理する。

## 引数と想定内差分

- 引数なし。
- agent が変更する作業成果物は realization file だけとする。起点 file に限らず、関連する複数 file の改善を一つの処理単位に含めてよい。
- agent が変更する realization file と cmoc が更新する refactor state を想定内差分とする。
- 一時作業領域の利用は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「一時作業領域」に従う。

## 一巡の境界

一巡は、列挙した対象を一通り調査する区切りであり、改善余地の不存在を判定する区切りではない。

1. fork の開始時は、doctor preprocess と編集 run の共通開始処理を行う。
2. 各巡の開始時は run worktree 上で entry 集合を同期し、全 entry をその巡の対象にする。前から残る調査要求を保持し、`false` の entry にも `investigation_required=true` を設定する。この state 更新を run branch に確定してから調査を始める。
3. その巡の全対象に調査機会を与えたら、変更や unresolved の有無にかかわらず次巡へ進む。調査機会を与えたとは、その target の処理単位を確定したことをいい、中断・失敗で rollback した単位は数えない。

巡回中の削除 file は以後の対象から外し、削除そのものを調査実績として数えない。追加 file と変更により生じた再調査要求は、遅くとも次巡で扱う。同じ対象の再修正や新規 file の追加によって、すでに順番を待っている他の対象が後回しになり続けてはならない。

一巡を管理する内部表現と、追加・削除・変更を反映する細かな scheduling は、この網羅性と公平な処理機会を満たす範囲で実装に委ねる。一巡の途中を同じ run で復元する永続 checkpoint は設けない。

## refactor loop

### 調査対象の選択

- その巡でまだ調査機会を与えていない対象を選び、同じ対象の再選択より優先する。
- 前の巡または fork から引き継いだ調査要求を、新たに設定した要求より先に扱う。その中では `last_investigation_result=not_investigated` を先に選び、その後は `last_investigated_at` の古い順、同値なら path の昇順とする。日時の比較には保存したミリ秒精度の値を使う。
- 関連 file を編集・参照しただけでは、その file 自身を起点とする調査機会を与えたことにしない。

### 一巡内の unresolved target

処理単位の確定結果に `resolution.status=unresolved` の所見が残る target を、その巡の unresolved target として保留する。保留は一巡内だけで有効とし、次巡では再検討する。current fork 全体や次の fork の選択対象から除外してはならない。

存在し続ける保留対象の entry には `last_investigation_result=findings` と `investigation_required=true` を残す。巡内の保留集合を永続的な skip・checkpoint として保存しない。終了時には、確定済みの未解決理由を report に残し、次の fork では現時点の原文を調べ直す。

### 1 処理単位

1. 対象 file の現在の SHA256 を調査時点の hash として取得する。
2. `build_realization_refactor_fork_file_review_and_fix_parameter` の作業入力には対象 path だけを渡す。一つの起点に関係し、検証・確定・rollback を一体として扱える小さなまとまりを選び、所見調査、realization file の修正、および検証を 1 回の agent call で行う。全 repository の改善を一つの call で完遂することは要求しない。
3. agent call が正常終了した後、「Structured Output の受理と正規化」に従って処理結果を決め、「確定前の検証」を満たすことを確認する。
4. 調査時点の hash、日時、および正規化後の所見有無を対象 entry に保存する。
    - 所見なし: `last_investigation_result=no_findings`, `investigation_required=false`
    - 所見あり: `last_investigation_result=findings`, `investigation_required=true`
5. agent call が変更した全 realization file を `investigation_required=true` にし、追加・rename・削除後の entry 集合を同じ処理単位で同期する。
6. 「不可分な確定区間」に従い、realization file の差分と refactor state の更新を同じ処理単位の commit として確定する。所見、変更 path、検証結果、および commit の対応を、その後の進捗と report に利用できるよう記録する。
7. 対象にその巡の調査機会を与えたことを記録し、unresolved が残れば巡内で保留する。停止要求がなければ、次の対象または次巡へ進む。

#### Structured Output の受理と正規化

cmoc は、申告された変更 path 集合と実際の変更 path 集合が一致する場合だけ Structured Output を受理する。両集合は次のように定め、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「機械的検証と正式な結果」に従って照合する。

| 集合 | 定義 |
|---|---|
| 実際の変更 path 集合 | agent call の開始時点を基準として出力時点に残る realization file の net 差分を、schema の `changed_paths` と同じ path 表現へ正規化した集合。 |
| 申告された変更 path 集合 | 全所見の `changed_paths` の和集合。同じ path を複数の所見が申告してよいが、`evidences[].path` は含めない。 |

受理した Structured Output から、次の条件で処理結果を決定する。

| 条件 | 処理結果 |
|---|---|
| `findings` が空である。 | 所見なしとする。 |
| `findings` が 1 件以上あり、全所見の `resolution.status` が `fixed` で、実際の変更 path 集合が空である。 | 所見なしへ正規化する。 |
| それ以外。 | 返された所見を処理結果の所見とする。 |

`resolution.status=fixed` と検証結果は agent の申告であり、それだけで修正の意味的な正しさを証明したことにはならない。所見なしへの正規化は cmoc の処理判定だけに適用し、元の Structured Output と Codex call log を改変・破棄せず保持する。synthetic `unresolved` への変換や、この正規化のための手動承認 workflow は追加しない。

#### 確定前の検証

realization file の変更は、対象 repository が定める品質検証を、処理単位内の最後の変更後に通してから確定する。cmoc 自身の code 変更では、`{{cmoc-root}}/oracle/doc/dev_rule/test_execution.md` の「fresh な完了ゲートを実行する」「完了を判定する」に従い、full test を含む所定のゲートを各変更単位の確定前に完了する。focused test だけで変更を積み上げ、全体検証を一巡後へ先送りしてはならない。

検証対象・追加検証の選択は、同文書の「通常検証と追加検証を選択する」に従う。Real Codex CLI を使う test の実行には、ユーザーの明示指示が必要である。refactor の開始や改善目標の指定だけを、その実行指示として扱わない。

cmoc は、realization file の net 差分がある場合、処理単位全体の検証結果が成功であることを commit の必要条件とする。未実行・途中・失敗を成功として扱わず、検証結果が不十分な変更は確定しない。これは出力の構文的な受理と別の条件であり、出力補正で検証不足を解消したことにしてはならない。

差分がなく state だけを更新する単位には、変更のための full test を新たに要求しない。必要な回帰検出能力とテスト削除・統合の判断は、`{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization.md` の「realization refactor の改善判断」と、cmoc 自身については `{{cmoc-root}}/oracle/doc/dev_rule/test_rule.md` の「テストの削除・統合」を参照する。

#### 処理単位の境界

cmoc は、想定外 path の変更と変更禁止対象への書き込みを、`changed_paths` の照合とは別に検査する。共通規則は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「agent call の差分検証」を正本とする。

所見なしへの正規化によって、差分検査、確定前の検証、または commit・rollback 失敗の扱いを緩和しない。unresolved があること自体は rollback や終了の理由にしないが、残す変更はすべて確定前の検証を満たさなければならない。

agent call には commit 差分、変更 commit の列、または変更要約を注入しない。

#### 不可分な確定区間

検証と state 更新の準備を終えた後、未処理の停止要求がないことを確認してから、成果物・state の commit と対応する確定記録を一体として確定する。この短い区間だけは、開始後に停止要求を受けても次の整合した境界まで完了させる。

agent 作業、全件テスト、計測、全対象の列挙・同期などの長い処理を、この区間に含めてはならない。巡の開始に伴う state だけの確定にも同じ境界を適用する。

## 終了理由

通常の終了経路はユーザー中断とする。全件処理、調査要求の一時的な解消、数値目標の達成、改善の停滞、周回数、または実行予算による自動停止条件を設けない。改善余地の不存在や反復の収束を自動判定することも要求しない。対象が空でも、停止要求を受け付けながら再同期して継続する。

継続不能なエラーは、通常の終了と区別して停止する。ファイル単位調査で全問題を発見できること、LLM の回答品質、または agent の申告・作業内容の意味的な正しさは保証しない。

## ユーザー中断

この fork は中断可能サブコマンドとし、共通動作は `{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` の「サブコマンドのユーザー中断」を正本とする。

- `Ctrl+C` は、開始準備、調査、編集、検証、計測、巡の切替、回復待ち、report 作成を含む任意の段階で受け付ける。
- 停止要求を受けたら、新しい処理単位・巡・agent call・品質検査・計測を開始しない。要約のための agent call や、確定するための追加テストも行わない。
- 不可分な確定区間の外では、開始準備・列挙・同期を含む実行中の処理を打ち切り、agent、test、計測、および作業用子 process を停止する。書き込み得る process の停止を確認してから、未確定の一処理単位全体を直前の確定状態へ rollback する。長い作業の自然完了を待つ経路を通常の停止処理にしない。
- 子 process の終了待ちは、作業の自然完了に依存しない有限の猶予とし、終了しなければ停止手段を切り替えて回収する。停止を確認できないまま rollback したり `joinable` にしたりしてはならない。停止や rollback 自体が失敗した場合は「その他のエラー」に従う。
- rollback は、その単位が導入した追加・変更・rename・削除と、巡開始の準備を含む未確定の refactor state 更新を取り消す。成果物と調査状態の片方だけを確定せず、取り消した作業を調査済み・検証済みとして数えない。確定済み commit と調査要求を保持する。
- doctor preprocess または共通開始処理が途中の場合にも同じ確定・rollback の境界を適用し、その準備が導入した未確定の更新と作成資源を取り消す。開始前から存在する資源や人間の未コミット差分を取り消さず、未完了の前処理を成功と記録しない。run の成立前に終了した場合は、存在しない run や `joinable` state を作らず、その段階を report する。
- 成立済みの run は、上記の整合化後に `run.state=joinable` にし、report を保存して終了コード 0 で終える。通常の中断で run worktree に未確定差分を残さない。
- その後は `cmoc run join` で確定済み成果物と調査状態を取り込むか、`cmoc run abandon` で破棄する。続ける場合は join 後に新しい `cmoc realization refactor fork` を開始し、調査要求を引き継ぐ。同じ run branch または worktree の実行途中を復元する仕組みは設けない。

## その他のエラー

- Codex CLI call の続行不能な失敗、想定外 path の変更、必要な検証の未完了・失敗、確定・停止・rollback の失敗などでは、未確定作業を整合させて停止し、成立済みの run を `error` にする。
- 未検証の変更をエラー処理のために commit してはならない。不可分な確定区間内では、その区間の整合性を回復する。
- 続行不能なエラーと、対応できない所見を示す `resolution.status=unresolved` を区別する。
- 確定済み commit と refactor state を保持する。整合化に失敗した場合は、残存資源と未確定差分を明示し、成功や `joinable` として扱わない。

停止を確認できなかった作業用 process がある場合は、`error` への遷移だけで停止済みとみなさない。後続の join は、その process の停止と未確定差分の解消を確認できるまで開始しない。abandon でも、process の停止を確認してから資源を破棄する。確認できなければ、復旧に必要な資源と診断を保持する。

## 改善の計測

テスト時間は、比較基準となる revision、検証範囲、実行環境、command、および計測条件を固定して実測する。比較対象でも同じ条件と必要な検出能力を維持し、変更した test の件数だけで検証範囲の同等性を判断しない。比較条件を満たす通常の検証結果は計測にも再利用してよい。

full test 1 回の所要時間と、検査の実行回数などによる orchestration 全体の所要時間を分けて評価する。検査回数を減らしただけの短縮、対象 test の除外、または必要な検出能力の低下を、full test の高速化として報告してはならない。

完了した比較可能な計測だけから短縮率を求め、対応する revision と条件を残す。測定途中・失敗・条件不一致・未計測を区別し、推測や期待効果を実測値にしない。未確定変更上の測定はその旨を示し、rollback 後に確定済み成果の測定結果として採用しない。

数値目標は改善の評価と人間の停止判断に使う。例えば 10% は固定必須値ではなく、各巡での短縮も義務としない。具体的な目標値、その指定方法、計測回数・統計方法・頻度は未定義とする。

## 実行中の進捗

`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「非対話サブコマンドの console 出力」に従い、stderr に次を簡潔に表示する。

- 現在の巡と処理段階、対象総数、その巡で確定した調査数、未処理数、および巡内保留数。
- 確定済みの変更の要約と、現在進行中で未確定の作業の区別。
- 比較基準と比較可能な測定済みテスト時間・短縮率。計測中または利用できる計測がない場合は、その状態。
- 停止要求の受付と、子 process 停止・rollback または確定区間の終了を待っている状態。

調査数は各巡の確定実績で数え、過去の履歴や単なる関連 file の参照で進捗を増やさない。表示のために新しい agent call を行わない。

## feedback との境界

成果物と feedback の境界は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「既存 workload との境界」を正本とする。

## fork report、終了 log、および終了コード

### 保存と掲載内容

実行 ID と共通掲載内容は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「実行 ID の開始表示」「共通掲載内容」に従う。

すべての終了経路で、`{{repo-root}}/.cmoc/gu/report/realization/refactor/fork/{{execution-id}}.md` に primary report を保存する。共通 fork 事前条件違反など、run や通常の report 生成処理より前のエラーも対象とする。共通 run 項目に加え、refactor state のフル path と `completion_reason` を含める。`completion_reason` は `user_interruption | error` とする。

本文には次の内容を含める。

- 完了した巡の数、終了時の巡・処理段階、その巡の対象数・確定調査数・未処理数・保留数。
- current fork で 1 回以上処理単位を確定した target path の重複のない件数と、確定した処理単位の件数。
- 巡内の unresolved target の件数と path。
- 各 target の確定済みの最新結果に残る未解決所見、その理由、および対応する Codex call log または Structured Output のフル path。前の巡から再調査を待つ未解決所見も含め、巡内の保留対象と区別する。
- 処理単位ごとの正規化後の所見数、変更と検証の結果。所見なしへ正規化した単位は 0 件とする。
- entry 総数、調査要求あり件数、各 `last_investigation_result` の件数。これらの履歴集計を、その巡の未処理数や改善目的での調査済み実績と混同しない。
- 確定済みの変更要約、比較基準と測定済みテスト時間・短縮率、未完了または比較不能な計測。
- 中断・エラー時の子 process 停止と rollback・確定の結果、取り消した未確定作業、および次に可能な join/abandon または復旧操作。

確定していない項目は `null`、未実行、または未完了として区別する。失敗した処理段階、エラー、および関連ログを記録する。

### 変更要約

変更要約は、各処理単位で確定した変更 path、所見、対応結果、および検証記録から cmoc が作成する。取り消した単位を成果に含めず、確定済み成果物の net 差分と、途中の変更履歴を区別する。確定済み成果物に差分がなければ変更なしと示す。

終了時専用の変更要約 agent call は設けない。ユーザー中断後またはエラー後にも新しい agent call や品質検査を開始せず、保存済みの記録を用いて report を作る。

### 終了 log と終了コード

サブコマンド終了イベントには `completion_reason`、巡内の unresolved target の件数、および report のフル path を含める。report、terminal result、および終了イベントからユーザー中断とエラーを判別可能にする。

`user_interruption` は正常系の終了コード 0、`error` は非 0 とする。一巡完了や unresolved の存在に対応する独立した終了理由は設けない。

## join 後 hook

workload 固有の hook は持たない。merge 後の refactor state 同期は共通 lifecycle が行う。
