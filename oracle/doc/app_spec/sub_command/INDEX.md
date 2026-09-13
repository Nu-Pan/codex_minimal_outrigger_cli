# `doctor.md`

## Summary
- `cmoc doctor` コマンドの仕様への入口。doctor preprocess の明示的な呼び出し、引数・事前条件・実行手順、および全終了経路で保存する primary report の要件を扱う。

## Read this when
- `cmoc doctor` の呼び出し方法、実行前提、処理委譲先、または doctor 実行結果の primary report 要件を確認するとき。

## Do not read this when
- doctor preprocess 自体の検証・修復内容を確認したいときは、正本である doctor preprocess の仕様を直接読む。
- `cmoc doctor` 以外のサブコマンドの仕様や、primary report の一般的な仕組みだけを確認したいとき。

## hash
- e004c75b5a42802cdae0ddd2d023d7ccf4b5fcc7f7065f6ee33a285dd6ad1330

# `editing_run.md`

## Summary
- 編集 run を開始する workload、同時実行制約、共通開始・終了処理、join／abandon の検証・差分検査・cleanup、および report と terminal result の共通仕様を定める。

## Read this when
- realization apply／refactor または feedback report の編集 run lifecycle を実装・変更・調査するとき
- cmoc run join／abandon の事前条件、merge、post-join、状態遷移、差分扱い、cleanup を確認するとき
- editing run の report や terminal result に必要な共通情報と終了経路を確認するとき

## Do not read this when
- run の隔離資源や session／run state の正本定義だけを確認したいとき
- realization apply、realization refactor、feedback report の workload 固有処理だけを確認したいとき
- oracle edit、read-only investigation、session lifecycle、または conflict 解消の仕様を確認するとき

## hash
- ba9914a84f850ac36212be33adf25c274aed5767c3045eddb7ab0c0989c78339

# `feedback_report.md`

## Summary
- `cmoc feedback report` の仕様を定義する入口。feedback observation の intake、issue identity の normalization、issue 単位の remediation・commit、wave loop、自動 join、publication、recovery、中断・エラー処理、および終了コードを扱う。

## Read this when
- feedback observation から issue の形成・再確認・remediation・結果分類までの処理を確認するとき
- feedback remediation run の隔離、issue 単位の commit、rollback、自動 join、join 後検査を確認するとき
- 正常 report、incomplete 診断 report、または中断・エラー時の invocation report の保存条件を確認するとき
- `cmoc feedback report` の CLI 契約、事前条件、停止条件、終了コードを変更・検証するとき

## Do not read this when
- raw observation の schema や reporter input v1 の互換処理だけを確認したいときは、参照先の feedback observation 正本を直接読む
- 結果分類や自然完了条件だけを確認したいときは、参照先の feedback 正本を直接読む
- feedback の repository-local state、report cut、high-watermark、atomic publication だけを確認したいときは、参照先の feedback_state 正本を直接読む
- 編集 run の共通 lifecycle、branch model、割り込み、Codex 呼び出し規約などの共通仕様だけを確認したいときは、各参照先の正本を直接読む

## hash
- 291cfb2cd26738a964354acc21a832d52436babaa8688144736dae93b651ce43

# `indexing.md`

## Summary
- `cmoc indexing` の実行契約と、全終了経路で保存するインデクシング実行要約を定義する仕様。
- 作業ツリーの変更確認から doctor preprocess、明示的なインデクシング実行、primary report 保存までの入口。

## Read this when
- `cmoc indexing` の実行条件や実行手順を確認したいとき。
- インデクシング実行の成功・失敗時に必要な報告内容と保存責務を確認したいとき。

## Do not read this when
- インデクシング処理の詳細仕様を確認したいとき。
- 特定の実行結果や診断ログを確認したいとき。

## hash
- 8a2acc19195064829931578f12875ea420efb5ab64e1889c6c68e9ebfbad5381

# `oracle_edit.md`

## Summary
- `cmoc oracle edit` の目的、入力から prompt 構築、前提条件検査、本命・仕様削減 agent call の直列実行、編集境界、終了状態、差分・レポート・ログ通知を定めるサブコマンド仕様。

## Read this when
- oracle file の最終状態に関するユーザー指示を受けて、本命編集と仕様削減を行う処理の流れや起動条件を確認するとき。
- 本命・仕様削減 agent call の判断材料、編集可能範囲、失敗時の扱い、primary report や terminal result の要件を確認するとき。
- `cmoc oracle edit` と他の run lifecycle、indexing、自動 commit、差分管理の境界を確認するとき。

## Do not read this when
- oracle file の内容そのものを調査・編集する場合は、対象の oracle file または oracle file の判断基準を直接読むとき。
- prompt editor input、`codex exec` の共通規則、indexing、doctor preprocess、ログ、toast、session state など個別の正本仕様の詳細だけを確認したいとき。
- `cmoc oracle investigation` など別サブコマンドの処理仕様を確認するとき。

## hash
- ff836e2a782708fefa11b0a223fbc45e465c918c7d025c9699dbea4c01700e32

# `oracle_investigation.md`

## Summary
- oracle file に関するユーザー調査指示を受け取り、doctor preprocess とエディタ入力を経て Codex CLI の TUI で調査・回答するサブコマンドの責務と境界を定義する入口。

## Read this when
- oracle file を根拠にユーザーの調査指示へ回答する TUI の起動フロー、入力 handoff、調査境界、結果の扱いを確認するとき。
- oracle investigation の起動パラメータや、oracle file・realization file・INDEX.md の変更可否を確認するとき。

## Do not read this when
- 正確な TUI 起動 prompt、prompt part、workload 固有パラメータ、または agent 向け instruction の文面を確認したいときは、実装側の builder を直接読む。
- エディタ入力 handoff の共通仕様、oracle file の判断基準、Codex CLI の TUI 共通仕様、Windows toast 通知の仕様だけを確認したいときは、それぞれの正本文書を直接読む。

## hash
- d3102c451d850cc9e224461bc2f2dc326b59688a637d9e9ebb2ba0875205f3cf

# `realization_apply.md`

## Summary
- realization apply の fork workload における目的、追従対象差分、agent call、成果物 report、join 後 hook、終了条件を定義する仕様。realization file への oracle 変更反映処理の入口。

## Read this when
- realization apply の fork が、どの commit 範囲の oracle 変更を対象にするか確認したいとき。
- 追従 agent の呼び出し回数・cwd・変更可能な file の境界や、fork 後の検査・commit・report 保存を確認したいとき。
- apply run の join 後に比較始点 commit が更新される条件、またはエラー時の扱いを確認したいとき。

## Do not read this when
- realization apply の fork 以外の編集 run の共通 lifecycle を確認したいときは、編集 run 共通仕様を直接読むべき。
- oracle file と realization file の適合性そのものの判定基準を確認したいときは、oracle と realization の適合性を定義する仕様を直接読むべき。
- 実装上の prompt、builder 引数、起動パラメータの具体的な構築方法を確認したいときは、指定された launch_exec.py を直接読むべき。

## hash
- 7d6be11e3ab32fcad457ee0a93ece1eefcf33a7ab8688998e820ea044682366b

# `realization_refactor.md`

## Summary
- realization refactor fork の目的、状態同期、current fork の unresolved target 管理、ファイル単位の調査・修正ループ、完了・中断・エラー時の扱い、および report 生成を定義する正本仕様。

## Read this when
- realization refactor fork の処理順序、調査対象の選択、agent call 後の結果判定、state 更新、unresolved の扱いを確認するとき。
- refactor の自然完了・unresolved 付き完了・ユーザー中断・エラーの判定、run state、終了コード、report の要件を確認するとき。
- realization refactor の fork lifecycle、差分検証、変更要約、join 後の共通動作との境界を確認するとき。

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを確認したいとき。
- oracle file と realization file の適合性そのものを確認したいときは、適合性の正本仕様を直接読む。
- 編集 run 全体に共通する fork・join・abandon やユーザー中断の仕様だけを確認したいときは、共通 lifecycle の正本仕様を直接読む。
- feedback workload の既存仕様や境界だけを確認したいとき。

## hash
- 009d9dc67d31ee1921df59a46ac74fcd60f3a2e77df6e187514c1b3552cc45b3

# `session_abandon.md`

## Summary
- 現在の session branch を home branch に merge せず破棄する `cmoc session abandon` の仕様を扱う。
- session abandon の事前条件、破棄してよい対象と保持すべき対象、cleanup 手順、状態遷移を確認するための入口。
- doctor preprocess や事前条件を含む全終了経路で保存される primary report の要件を確認するための入口。

## Read this when
- 現在の session を成果物ごと破棄したいとき。
- session branch の切替・強制削除や `session.state` の abandoned 遷移を確認したいとき。
- cleanup 途中の失敗時に必要な rollback、残存資源、再実行条件を確認したいとき。
- session abandon の primary report に含まれる実行要約や診断ログの扱いを確認したいとき。

## Do not read this when
- session の成果物を home branch に取り込む操作を確認したいときは、`cmoc session join` の仕様を直接読む。
- join 済み結果の rollback を確認したいときは、rollback に対応する仕様を直接読む。
- 未 join の編集 run を破棄する手順を確認したいときは、`cmoc run abandon` の仕様を直接読む。

## hash
- f6eca219a6b9909beb0c996f83111eb2dd9ee14d6d5cccc7dfc7039b01dad1c8

# `session_fork.md`

## Summary
- `cmoc session fork` の引数なし実行について、実行対象ブランチの事前条件、セッションブランチの作成・checkout、初期 session 情報の保存、終了時の primary report を定める仕様。

## Read this when
- 現在のローカルブランチを起点に新しい cmoc セッションを開始する処理の条件や手順を確認するとき。
- セッションブランチの命名、初期状態の保存、または fork 実行結果・失敗時 report の内容を確認するとき。

## Do not read this when
- 任意の start point を指定する操作や、既存セッションの状態遷移そのものを確認したいとき。
- ブランチの役割・分岐関係の正本や session state の schema を直接確認する必要があるとき。

## hash
- e0cb5c94c8eda9ec1bae324fdf4074934553a4e9671a9c02fd7809d2f68e610d

# `session_join.md`

## Summary
- `cmoc session join` の実行契約を定義する仕様。active session の完了、home branch への merge、conflict 解消、session state 更新、session branch cleanup、primary report 保存までの責務を扱う。

## Read this when
- session を完了して home branch へ戻す処理の条件・手順・終了経路を確認するとき
- session join における merge source/target、conflict 解消、oracle file の扱い、branch cleanup、report 内容を確認するとき

## Do not read this when
- 通常の git branch 間 merge の汎用仕様を確認したいとき
- session state の共通事前条件や branch model の正本定義そのものを確認するとき
- feedback state の所有範囲だけを確認するときは、対応する正本仕様を直接読む

## hash
- 19199c4034a95f29b713e01800b4e28eb85496e3042aaf4211601ab1c59fdf0f

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの責務・実行手順・共通の TUI 起動契約を確認するための正本。ユーザープロンプトの受領から起動パラメータ構築、AI Agent CLI/TUI 起動までの意味上の入口を示す。
- Codex CLI をバックエンドとして起動する際の固有条件と、関連する正本仕様への参照先を確認できる。

## Read this when
- `cmoc tui` の引数、事前条件、実行手順、プロンプト入力 lifecycle を確認したいとき
- TUI 起動時に注入される cmoc 固有契約、installed skill との優先関係、indexing preflight、feedback observation、終了通知の適用条件を確認したいとき
- Codex CLI を `codex` として起動する条件、editor input handoff、環境変数や CLI 設定上書きの扱いを確認したいとき

## Do not read this when
- プロンプトエディタ入力の詳細な正本仕様だけを確認したいときは、指定された prompt editor input の正本を直接読む
- 起動パラメータの正確な prompt part、文面、workload 固有パラメータ、選択理由を確認したいときは、`build_tui_launch_tui_parameter` の正本実装を直接読む
- oracle file と realization file の責務・適合性、indexing、feedback observation、Windows toast、editor input handoff、Codex exec rule の詳細だけを確認したいときは、それぞれ本文で参照されている正本文書を直接読む

## hash
- e65bbdac84bff56e975dc0b64353915a6c2f5b0ac1be94bd3249d6a9033c51c2
