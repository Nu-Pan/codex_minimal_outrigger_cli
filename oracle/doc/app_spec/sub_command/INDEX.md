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
- 編集系 workload の run 開始・終了、同時実行制約、共通事前条件、隔離・commit 責務を定義する共通仕様。
- realization apply/refactor の明示的 join と feedback report の self-join、run join/abandon の事前検証・差分検査・merge・cleanup・report要件を扱う。
- run isolation、session state、workload固有仕様、ログ出力規則への入口となる上位ライフサイクル仕様。

## Read this when
- 編集 run を開始する workload の共通条件、active run の排他、run state 遷移、branch/worktree の扱いを確認するとき。
- cmoc run join または cmoc run abandon の対象解決、差分検査、merge・cleanup・report要件を確認するとき。
- feedback_report の自動 joinや、realization_apply/refactor の明示的 joinのライフサイクルを確認するとき。

## Do not read this when
- 個別 workload の編集内容や固有の preflight、許可ファイル、join 後 hookを確認したい場合は、realization_apply、realization_refactor、feedback などの workload 固有仕様を直接読むとき。
- run の隔離資源の詳細や session state のフィールド定義だけを確認したい場合は、run_isolation.md または session_state.md を直接読むとき。
- コンソール・ファイルの共通出力形式だけを確認したい場合は、console_and_file_log.md を直接読むとき。
- oracle edit、read-only investigation、session lifecycleなど、この editing run lifecycle の対象外の操作を調べるとき。

## hash
- 6628d03f20fa0263aac00c7fad8a0f7c4fee22daff0ac0537af0b1a2a5f9f50a

# `feedback_report.md`

## Summary
- `cmoc feedback report` の実行契約を定義する正本仕様で、feedback observation の validation・normalization・issue remediation・issue 単位の commit/rollback・intake wave・自動 join・publication と recovery の境界を扱う。
- feedback 報告処理の開始条件、run 状態、想定内差分、結果分類、human_required を含む正常 publication および incomplete/error の扱いを確認する入口。

## Read this when
- feedback report サブコマンドの処理フロー、実行前提、run の再開条件を確認したいとき。
- observation から issue を形成し、remediation agent を呼び、差分を commit して自動 join・publication する仕様を確認したいとき。
- validation failure、state corruption、merge failure、publication failure などの recovery 境界を確認したいとき。

## Do not read this when
- raw observation の schema や collector の収集契約だけを確認したいときは feedback_observation.md を読む。
- feedback state の schema、checkpoint、high-watermark、report cut、atomic publication の詳細だけを確認したいときは feedback_state.md を直接読む。
- 一般的な編集 run の join、abandon、隔離、差分検査契約だけを確認したいときは editing_run.md を読む。
- 実際の normalization agent の prompt 構築や Structured Output schema を確認したいときは oracle/src/oracle/acp_builder/feedback/normalize_issue.py と normalize_issue.json を直接読む。

## hash
- 3f5ad345b2853ee7abf7a9368cf52acf4930ca304778e37f6e9161a5f1546401

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
- `cmoc oracle edit` の仕様を定めるサブコマンド文書。ユーザー指示から共通の prompt と設定を一度構築し、同じ worktree に対して独立した編集 agent call を最大 2 回、所定の前処理・条件検査・報告とともに実行する流れを扱う。
- 引数、agent への指示境界、oracle file の編集範囲、未コミット差分の扱い、実行順序、終了状態、primary report・ログ・通知、中断および排他制御の規則を確認するための入口。

## Read this when
- `cmoc oracle edit` の起動条件、2 回の編集 agent call の順序、共通 prompt・設定の確定方法を確認したいとき
- oracle edit が編集できる対象、禁止される Git/worktree 操作、未コミット差分の扱いを確認したいとき
- 成功・失敗時の終了状態、差分維持、primary report、console・ログ・通知の責務を確認したいとき

## Do not read this when
- oracle file の編集判断基準そのものを確認したい場合は `oracle_and_realization.md` を直接読むとき
- prompt の共通 editor lifecycle や Codex 実行・Git 差分受け渡しの詳細を確認したい場合は、本文が参照する共通仕様を直接読むとき
- 実装の具体的な起動処理や設定定義を確認したい場合は、本文が指定する `oracle/src` の builder・設定ファイルを直接読むとき

## hash
- 331cdb1c138438ca4393601b2d3e9561affde06dcda5a4f09cee77c99db8f1c6

# `oracle_investigation.md`

## Summary
- `cmoc oracle investigation` サブコマンドの正本仕様。oracle file に関する調査指示をエディタから受け取り、doctor preprocess、TUI 起動パラメータ構築、Codex CLI TUI の起動、調査結果の提示までの責務と境界を定める。調査サブコマンド全体の実行手順・入力・TUI 引き渡し・結果と変更の扱いを確認する入口であり、個別の prompt 文面や builder の詳細仕様に代わるものではない。

## Read this when
- oracle file を対象とする調査サブコマンドの実行手順、入力方式、TUI 起動条件、agent の権限、調査結果の扱いを確認・変更するとき。
- 調査サブコマンドが参照する関連仕様や、builder へ委譲される責務の境界を確認するとき。

## Do not read this when
- 正確な TUI prompt 文面、prompt part の選択、workload 固有パラメータ、またはその選択理由を確認したいときは、指定された launch TUI builder の正本仕様を直接読む。
- エディタ入力 handoff、oracle/realization の分類、Codex CLI 共通起動規則、indexing の詳細を確認したいときは、それぞれ本文中で参照される専門仕様を直接読む。
- 実装コードやテストの具体的な挙動だけを調べるときは、対応する realization code や realization test を直接読む。

## hash
- 5d3dd339645564c99bee0caf6691554fdbcafc0838ffcc69d2d2cf41383831c7

# `realization_apply.md`

## Summary
- realization apply fork の目的、追従対象となる oracle 差分、単一 agent call による realization 更新、実行手順、エラー処理、report、join 後の状態更新を定義する正本仕様。

## Read this when
- realization apply fork の追従範囲、oracle と realization の対応判断、agent call の実行制約、成果物の検査・report、または join 後の session 更新を確認・変更するとき。

## Do not read this when
- 編集 run 全体に共通する fork・join・abandon lifecycle だけを確認したいときは、共通 lifecycle の仕様を直接読む。
- realization apply の builder 実装における prompt、引数、起動パラメータの具体的な構築を確認したいときは、指定された builder の正本実装を直接読む。
- 実際の realization 実装やテストの挙動を確認したいときは、対応する src または test を直接読む。

## hash
- a0db197eb14906040824ae799d0e65afbb3e9bf8eba59b1eb6602e42b37fa9e8

# `realization_refactor.md`

## Summary
- `cmoc realization refactor fork` の正本仕様。oracle file と realization file を対象に、refactor state の同期、current fork の unresolved target 管理、ファイル単位の調査・修正・検証ループ、Structured Output の受理、完了・中断・エラー時の扱い、report と終了コード、join 後の境界を定義する。

## Read this when
- realization refactor fork の処理対象選択、調査状態、unresolved の扱い、処理単位の commit、完了理由を確認するとき
- realization file の調査・修正 agent call、変更 path 検証、refactor state、fork report の仕様を変更・実装するとき
- realization refactor の fork 開始から loop、ユーザー中断、エラー、joinable 終了までの workload 固有動作を確認するとき

## Do not read this when
- realization file への短い変更ループや apply workload の仕様だけを確認したいときは realization_apply.md を読む
- fork・join・abandon の共通 lifecycle、run isolation、共通事前条件を確認したいときは editing_run.md および参照先の共通仕様を読む
- oracle file と realization file の分類・適合性そのものを確認したいときは、本文で参照される oracle_and_realization.md や oracle_and_realization_file_enumeration.md を直接読む
- INDEX.md の生成規則や索引の更新処理そのものを確認したいときは indexing.md を読む

## hash
- f433e3411f3b2ea38db6893c05435fc315c9e73f4eca934a107ea7739b689317

# `session_abandon.md`

## Summary
- 現在のセッションブランチをホームブランチへ merge せず破棄し、状態更新・ブランチ削除・失敗時 rollback・primary report 保存までを定める `cmoc session abandon` の正本仕様。
- `cmoc session join` の取り消しや未 join 編集 run の破棄を扱う仕様ではなく、それらは別のセッション／run 操作へ進むための入口。

## Read this when
- セッションブランチを merge せず abandon するコマンドの事前条件、破棄対象、実行手順、状態遷移を確認するとき。
- abandon 実行時の cleanup 失敗時 rollback や primary report の保存内容を確認するとき。

## Do not read this when
- join 済み結果の rollback を確認したいとき。
- 未 join の編集 run の破棄方法を確認したいとき。
- セッション共通の事前条件や状態モデルそのものを確認したいときは、session_state.md を直接読む。

## hash
- ffd3b1f597884c62786ac8e70163fb71116742e2d3a73500231b187d2e2b9f36

# `session_fork.md`

## Summary
- 現在のローカルブランチを起点にセッション用ブランチを作成・checkoutし、初期セッション状態と実行結果を保存する `cmoc session fork` の仕様。

## Read this when
- セッション用ブランチの作成条件、分岐元、命名規則、初期状態保存、または実行結果レポートの仕様を確認したいとき。

## Do not read this when
- 既存セッションの操作や通常のブランチ運用を確認したいとき。分岐元を任意の start point で指定する方法を探しているときは、このサブコマンドではなく事前のブランチ切替を確認するとき。

## hash
- ecba04632a0bb7a01b4f1564c7c549999206201fe1c990f8297f3d9ed56e3267

# `session_join.md`

## Summary
- `cmoc session join` の正本仕様。引数なしで現在の session branch を home branch へ merge し、conflict 解消、session state 更新、branch cleanup、primary report 保存までの完了条件と失敗時の扱いを定める。

## Read this when
- session を完了して home branch に戻す処理の事前条件・merge 対象・実行手順を確認するとき
- session join 中の merge conflict 解消、oracle と realization の優先関係、branch 削除条件を確認するとき
- session join の終了経路、警告・エラー、primary report の記録内容を実装または検証するとき

## Do not read this when
- session の状態表現や active session context の共通事前条件だけを確認したいときは session_state.md を直接読む
- branch と commit の一般的なモデルを確認したいときは branch_model.md を直接読む
- session join 以外の session 操作や通常の編集 run の仕様を確認するとき

## hash
- 07ab427429ba278647f2fd6eeb6e68567cd026f8a3784fd3266c9e60c28e7919

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの正本仕様。ユーザープロンプトの受領、doctor preprocess、起動パラメータ構築、AI Agent CLI/TUI の直接起動、および未コミット差分を許容する実行条件を扱う。
- TUI 起動時の共通契約、indexing・feedback・通知の参照先、Codex CLI 固有の起動条件と editor input handoff の入口を示す。

## Read this when
- `cmoc tui` の実行手順、引数、未コミット差分の扱い、TUI 起動条件を確認・変更するとき。
- TUI に注入する cmoc 固有契約、起動パラメータ委譲、indexing preflight、feedback observation、Windows 通知の仕様上の関係を確認するとき。
- Codex CLI を TUI バックエンドとして起動する際の `codex` コマンド、環境変数、設定上書き、editor input handoff の適用条件を確認するとき。

## Do not read this when
- プロンプトをエディタから受け取る lifecycle の詳細だけを確認する場合は、指定された prompt editor input の正本文書を直接読むとき。
- 起動パラメータの正確な prompt part、文面、workload 固有設定、選択理由を確認する場合は、`build_tui_launch_tui_parameter` の正本実装を直接読むとき。
- indexing、feedback observation、Windows toast、editor input handoff の詳細仕様だけを確認する場合は、本書から参照される各専門文書を直接読むとき。
- TUI の実装コードやテストの挙動だけを調べる場合は、対応する realization implementation または realization test を直接読むとき。

## hash
- bf2c7386391bfad7fdb2fbd081d3d5fda57bf91649fb4f3d12c2862e79fce97c
