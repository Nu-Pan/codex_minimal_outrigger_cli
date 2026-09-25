# join の競合解消

## 目的と適用範囲

`cmoc run join`、`cmoc feedback report` の自動 join、および `cmoc session join` は、通常の Git merge を先に試みる。内容の競合が発生した場合は、追加フラグなしで agent に統合を委ねる。目的は、関連する oracle と両 branch の変更意図を踏まえ、必要な付随修正と検証を含む整合したマージ結果を完成させることである。

本書は、競合解消の共通判断基準と責務を所有する。汎用 Git merge wrapper、新しい人間意図の決定、または元の workload の権限拡大を目的としない。コマンド固有の契約は次の正本に従う。

- `{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「cmoc run join」：run の差分検査、編集範囲、取り込み、失敗時の復旧、post-join、および cleanup。
- `{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「自動 join と join 後の確定」「join 後の publication failure」：封印後の調整・検証と publication の境界。
- `{{cmoc-root}}/oracle/doc/app_spec/sub_command/session_join.md` の「git merge がコンフリクトした場合」「その他、コマンドが想定外に失敗した場合」：session の編集範囲と失敗時の扱い。

## 統合の判断基準

agent は競合の両側と関連する oracle を調査し、両立する意図と挙動を保持する。競合箇所の選択だけでなく、関連ファイルの組み直し、rename・削除、テストの調整、および初期の競合一覧にないファイルの付随編集も、統合に必要な範囲で自律的に判断する。複数の妥当な実装方法があることや、両側を組み直す必要があることだけを理由に、人間へ判断を戻さない。

関連する oracle と変更意図からも決められない相反する要求の採否など、新しい人間意図の選択が必要な場合は、推測で一方を破棄せず未解消として報告する。実装都合から oracle の意味を逆算・変更してはならない。

共通の正本責務と判断基準は、`{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization.md` の「oracle doc と oracle src の正本責務」から「正本責務に基づく優先関係」まで、および「oracle file を扱う判断基準」「realization file を扱う判断基準」に従う。編集と検証は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「詳細なファイルアクセス制限」「書き込み主体の責任分界」と各 join の編集範囲内で行う。アクセス禁止の情報を Git 履歴経由で参照したり、禁止対象を付随編集したりする権限は与えない。

## agent と cmoc の責務

agent は、調査、内容の統合、必要な検証、および根拠を伴う完了判断を担当する。検証には対象リポジトリの手順を用い、実行できなかった検証を成功として扱わない。編集可能な対象の内容上の競合が解消され、必要な検証により統合結果の妥当性を確認できた場合に解消完了を報告する。未解消事項や必要な検証の不足があれば、その理由を報告する。

cmoc は次の管理処理を担当する。

- 各 join の事前条件を検査し、merge 前の両 branch の HEAD と初期の競合状態を把握する。
- 内容の競合を解消する agent call を直列に実行し、その完了判断、検証結果、および未解消事項を確認する。文書検索の提供は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「文書検索 MCP」に従う。
- refactor state の競合を解消する。refactor state は agent の直接編集対象にせず、この管理物だけが競合した場合は内容解消用 agent call を必要としない。
- 解消後の内容と管理物について、未解消の conflict marker がないことを確認する。初期の競合 path に限定せず、付随する追加・変更・rename・削除も staging し、unmerged entry が残っていないことを確認して merge commit を作成する。
- 各 join の state 更新、生成物の同期、report、および cleanup を行う。

agent は staging、commit、merge の開始・中止、branch・worktree 操作、または cmoc の管理 state の直接更新を行わない。agent の編集だけでは Git index の unmerged entry は解消されないため、内容の解消完了と cmoc による staging 後の確認を区別する。管理物の競合や staging 待ちの unmerged entry が残ることだけを agent の未解消理由にしない。ただし、それらにより必要な検証ができなければ、その不足を報告する。cmoc が更新する管理物以外のアクセス禁止対象に内容の競合が残る場合は、merge を成立させない。agent を呼び出した場合は、その明示的な解消完了も確認できなければならない。

refactor state の同期内容は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「entry 集合の同期」を正本とし、cmoc が管理する調査履歴と調査要求の扱いを競合解消 agent に委ねない。run join の同期時点は、`{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「editing run の join での同期時点」と、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「merge と post-join」に従う。

## 受理と報告

cmoc の差分検証は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「agent call の差分検証」に従う。マージ結果が片側の内容と一致すること、または編集 path が初期の競合 path 集合と一致することを受理条件にしない。元の workload の差分受理条件は維持し、マージ調整の受理条件と混同しない。機械検査に意味的な正しさの証明を要求せず、agent の判断と検証記録を、cmoc の機械検査結果と区別して扱う。

各 join の report から、次を読み取れるようにする。agent は内容判断に関する情報を返し、cmoc は実際の commit、state、復旧、および cleanup の結果と結び付ける。

- 統合した両 commit と初期の競合。
- 採用した判断、その根拠となる oracle と両側の変更意図。
- 付随編集の対象と必要性。rename・削除と、初期の競合一覧外の編集を含む。
- 実行した検証、その対象と結果、および未実行・失敗の理由。
- 解消完了か、未解消か。未解消の場合は、残る要求、アクセス境界、人間意図の選択、または検証不足などの具体的な理由。

## agent への入力と正確な定義の委譲

cmoc は merge を行っている worktree を call の cwd とし、merge 前に確定した source と target の commit ID を渡す。agent はその repository で共通祖先、両側の変更、および進行中の競合状態を必要な範囲で取得する。差分本文や競合 path 一覧を初期 prompt に埋め込まない。参照入力と取得失敗の扱いは、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「Git 差分の参照入力」に従う。

正確な agent 向け表現と構築を次へ委譲する。受信 agent が cmoc の内部仕様を読まなくても作業できる、自己完結した目的、入力、制約、判断基準、および報告事項を渡す。

- `{{cmoc-root}}/oracle/src/oracle/prompt_builder/policy/conflict_resolution.py` の `build_conflict_resolution_policy`：共通の統合・検証方針の文面と、完了判定を含む報告の正確な表現。
- `{{cmoc-root}}/oracle/src/oracle/prompt_builder/merge_conflict_resolution.py` の `build_merge_conflict_resolution_prompt`：共通の objective、commit 参照入力、および prompt part の構築。
- `{{cmoc-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt`：完全 prompt への共通規定と追加文面の統合。
- `{{cmoc-root}}/oracle/src/oracle/other/cmoc_config.py` の `CmocConfigCodex.agent_calls`：競合解消 call の provider、model、および reasoning effort の設定値。

call 固有の編集範囲と起動定義の委譲先は各 join の仕様で定める。新しい Structured Output schema、永続 state、または解消後の追加レビュー call は設けない。

## 確認ケース

以下は共通方針とコマンド固有契約を照合する代表例であり、実装方式を固定するものではない。

| 状況 | 確認する結果 |
|---|---|
| 通常の内容競合 | 追加フラグなしで agent が両側の意図を統合し、検証と判断根拠を報告する。 |
| rename・削除を伴う競合 | marker の有無だけで完了とせず、参照先と関連挙動も整合させ、cmoc が rename・削除を含め staging する。 |
| 初期の競合一覧外に必要な修正がある | アクセス境界内の付随編集を行い、対象と必要性を報告する。一覧外という理由だけで拒否しない。 |
| 内容の解消後に管理物の競合や staging 待ちの unmerged entry が残る | agent は内容と必要な検証に基づいて完了を判断し、残る管理処理を報告する。cmoc が管理物と staging を処理し、未解消競合を確認する。 |
| run 開始後に session 側の realization が commit 済みである | join 前にその変更を拒否せず、run の変更と統合する。元の workload の禁止対象検査は維持する。 |
| feedback 修正の内容が変わっても封印済みの結果を維持できる | 影響を受ける判定を merge commit 前に検証し、封印済み artifact を変えず、最終取り込み結果との対応を publication completion record に残す。 |
| feedback のマージ調整中に、封印済み結果分類を変更する必要が判明する | 自動 join の merge commit と publication を停止し、封印済み artifact、観測データ、および recovery 用資源を保持する。 |
| oracle の要求が相反し、人間意図の選択が必要である | agent が推測で採否を決めず、未解消の理由を報告し、merge を成立させない。 |
| 解消または必要な検証に失敗する | run join は付随編集も含め merge 開始前へ戻して run を保持する。session join はその時点で停止する。取り込み確定後の失敗には各コマンドの recovery を適用する。 |

仕様の照合や oracle src の prompt 構築確認だけを、realization の動作検証済みとして扱ってはならない。
