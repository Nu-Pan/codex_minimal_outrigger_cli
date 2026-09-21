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
- 編集 run の共通ライフサイクル仕様。realization apply/refactor と feedback report の開始条件、同時実行境界、run の開始・join・abandon、差分検査、merge、cleanup、report および terminal result を定める。
- 個別 workload の仕様へ進む前に、編集 run に共通する state 遷移と lifecycle 操作の基準を確認するための入口。

## Read this when
- 編集 run を開始・継続・join・abandon する処理の共通条件や state 遷移を確認するとき。
- run branch/worktree の差分検査、merge、conflict、cleanup、report の共通仕様を確認または変更するとき。
- realization_apply、realization_refactor、feedback_report の workload 固有仕様と共通 lifecycle の境界を確認するとき。

## Do not read this when
- cmoc oracle edit、read-only investigation、run を作らない機械的更新、session lifecycle の仕様だけを確認するとき。
- 特定 workload の preflight、編集対象、join 後 hook、feedback publication などの詳細だけを確認する場合は、対応する workload 固有仕様を直接読むとき。
- run の隔離資源や session state の正本仕様そのものを確認する場合は、run_isolation.md または session_state.md を直接読むとき。

## hash
- 830fbfc103458377b86486a6a495a1e518466d7bdf95616b8e9314bd775a34a0

# `feedback_report.md`

## Summary
- `cmoc feedback report` の仕様を定義し、同一 invocation 内で raw observation を検証・正規化し、issue 単位の realization 修正と検証を行い、安全な変更を commit して session branch へ自動 join し、結果を publication する処理の入口。

## Read this when
- feedback observation から issue の intake、normalization、remediation、commit、wave 処理、自動 join、publication の動作条件を確認したいとき
- `cmoc feedback report` の CLI 契約、run 開始・再開条件、入力検証、結果分類、差分検査、rollback、recovery 境界を確認したいとき

## Do not read this when
- raw observation の収集や reporter input の互換処理だけを確認したいときは feedback_observation.md を直接読む
- feedback の用語・結果分類・repository-local state の詳細だけを確認したいときは feedback.md または feedback_state.md を直接読む
- 一般的な編集 run の lifecycle、branch、join、隔離規則だけを確認したいときは editing_run.md や branch_model.md、run_isolation.md を直接読む
- normalization または remediation agent の prompt、起動設定、Structured Output schema を確認したいときは対応する oracle/src の定義を直接読む

## hash
- ddee2abe29119930c791c1228a0a205c2569ffd2d8df708f8fea538548cb7ada

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
- `cmoc oracle edit` の引数なしサブコマンド仕様。ユーザー指示から共通の prompt と設定を構築し、同一 worktree 上で独立した新規 Codex session による編集 agent call を最大 2 回直列実行する流れ、編集境界、終了状態、差分維持、primary report・ログ・通知の扱いを定める。

## Read this when
- `cmoc oracle edit` の起動条件、prompt 構築、2 回の agent call の実行順序を確認するとき。
- oracle file の編集だけを許可する agent 境界、未コミット差分の扱い、成功・失敗時の終了条件を確認するとき。
- oracle edit 実行の report、console、ログ、Windows toast、feedback observation の記録責務を確認するとき。

## Do not read this when
- oracle file の調査・参照専用処理の仕様を確認したいときは、`oracle investigation` の仕様を読む。
- prompt editor input、Codex 実行規則、session state、indexing、共通設定の詳細だけを確認したいときは、本書から参照される各正本文書を直接読む。
- oracle edit の実装詳細やテストケースだけを確認したいときは、対応する realization の実装・テスト対象を直接読む。

## hash
- 0deac4c1d7d4f50c8ab16b5efd16281ee5a772515a6c6a7d7d1ec18011b858f5

# `oracle_investigation.md`

## Summary
- `cmoc oracle investigation` サブコマンドの正本仕様。引数なしでユーザーの oracle file 調査指示を受け取り、所定の前処理と prompt editor input lifecycle を経て、builder が構築したパラメータで Codex CLI の TUI を起動し、oracle file を根拠とする日本語中心の調査結果を回答する責務と、変更禁止・自動 commit 禁止などの境界を定める。

## Read this when
- `cmoc oracle investigation` の利用者向け挙動、実行手順、調査対象の境界、TUI 起動の扱い、調査結果や oracle file・realization file の変更可否を確認したいとき
- oracle file を調査するサブコマンドの仕様を確認するとき

## Do not read this when
- 正確な prompt 文面、prompt part、workload 固有の起動パラメータ、agent 向け instruction の実装を確認したいときは、委譲先の `build_oracle_investigation_launch_tui_parameter` を直接読む
- エディタ入力の共通 lifecycle や editor input handoff の共通仕様を確認したいときは、参照先の正本を直接読む
- Codex CLI TUI の共通起動規則や indexing の共通条件だけを確認したいときは、該当する共通仕様を直接読む

## hash
- f071044ce9ce3924239a96edce9ed9d4a6c1382db5ed8de32482d70f7256b3c8

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
- realization refactor fork の目的、refactor state 同期、current fork の unresolved target 管理、処理単位と loop、完了・中断・エラー、report 生成までの正本仕様。
- oracle file と realization file の適合性をファイル単位で調査・修正し、調査要求がなくなるまで継続する workload の入口。

## Read this when
- realization refactor fork の動作、調査対象の選択、state の保存・同期、agent call の結果判定を確認するとき。
- unresolved target を含む fork の完了理由、中断時の rollback、終了 report や終了コードの仕様を確認するとき。
- realization apply とは異なる長期的な反復調査 workload の仕様を調べるとき。

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを確認したいとき。
- fork・join・abandon に共通する編集 run の lifecycle だけを確認したいとき。
- oracle と realization の適合性判定基準そのもの、agent call の共通差分検証、または feedback との境界を直接確認したいときは、それぞれ参照先の正本仕様へ進む。

## hash
- 44a7ea834fec19ac273226484168012fb0a152c1c1c81e94480cb4498512e076

# `session_abandon.md`

## Summary
- `cmoc session abandon` の正本仕様。現在の session branch を home branch に統合せず破棄するための引数、事前条件、破棄対象と保護対象、cleanup 手順、状態遷移、失敗時の rollback、primary report 要件を定義する。

## Read this when
- セッションを merge せず破棄する操作の仕様を確認・変更するとき
- session abandon の事前条件、branch や commit の破棄範囲、session state の遷移、cleanup 失敗時の扱いを確認するとき
- abandon 実行結果の primary report に必要な内容を確認するとき

## Do not read this when
- session fork、session join、run abandon など別サブコマンド固有の仕様を確認するとき
- active session context や編集 run 開始・終了に共通する事前条件だけを確認したいときは、session_state.md を直接読むべきとき
- 実装やテストの具体的な挙動を確認したいときは、対応する realization implementation や realization test を直接読むべきとき

## hash
- 66430bb557888daabc21ed34f04ad44f912bb48eee2e058b50c62f1f7697311a

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
- `cmoc session join` の正本仕様。現在の session branch を session home branch へ merge して session を完了する処理の入口。
- 引数・事前条件・branch 操作・conflict 解消・session state 更新・branch cleanup・primary report の規定を扱う。

## Read this when
- session join の実行条件、merge 対象、conflict 解消、終了状態や報告内容を確認・変更するとき。
- session join の実装やテストが、session 完了処理と merge 後の後始末に適合しているか調べるとき。

## Do not read this when
- session の作成や通常の session 操作など、join 以外のサブコマンドの仕様を確認したいとき。
- conflict 解消用 agent call の具体的な prompt 構築だけを確認する場合は、指定された conflict resolution の oracle source を直接読むとき。
- branch model、session state、feedback state、error handling の共通正本だけを確認したい場合は、本文が参照する各仕様を直接読むとき。

## hash
- 7fa84b7ada96672e9532bbfc8e6eead631a1dda0a186bdba899a319496b11ca3

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの責務と実行手順を定義し、プロンプト入力から AI Agent CLI/TUI 起動までの共通契約と Codex CLI 固有設定への入口を示す。

## Read this when
- `cmoc tui` の引数、事前条件、doctor preprocess、プロンプト入力、起動パラメータ構築、TUI 起動手順を確認するとき。
- TUI に注入する cmoc 基本規定、indexing preflight、feedback observation、終了時通知の適用条件を確認するとき。
- Codex CLI をバックエンドとする TUI 起動で、editor input handoff、環境変数、preflight validation、引数上書きを確認するとき。

## Do not read this when
- プロンプトエディタ入力の詳細な lifecycle を確認したい場合は、prompt_editor_input.md を直接読むとき。
- 起動パラメータの正確な prompt part、文面、workload 固有設定、選択理由を確認したい場合は、launch_tui.py を直接読むとき。
- oracle と realization の責務・適合性、indexing、feedback observation、Windows toast の詳細仕様を確認したい場合は、それぞれ本文中に指定された正本を直接読むとき。

## hash
- aaf4cb73da7956a14562e10acc24d1d7e3d60da93c8c67ba4327debaebf15e79
