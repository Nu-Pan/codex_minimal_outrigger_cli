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
- 編集 run の共通ライフサイクル仕様。realization apply/refactor と feedback report の開始条件、同時実行境界、差分管理、join・abandon、cleanup、report と terminal result を横断して定める。
- 個別 workload の処理内容ではなく、複数の編集 workload に共通する run の状態遷移と終了処理を確認するための上位入口。

## Read this when
- 編集 run の開始可否、active run の排他、run worktree・branch の扱いを確認するとき。
- cmoc run join または cmoc run abandon の事前条件、差分検査、merge、cleanup、失敗時の状態を確認するとき。
- feedback_report の self-joining と、realization workload の明示的 join の共通 lifecycle を比較するとき。
- 編集 run の report や terminal result に必要な実行情報・状態・cleanup 結果を確認するとき.

## Do not read this when
- realization apply や realization refactor 固有の編集内容、join 後 hook、refactor state 同期の詳細だけを確認したいときは、それぞれの workload 固有仕様を先に読む。
- feedback report の intake wave、issue commit、publication、recovery など固有の処理だけを確認したいときは feedback_report.md を直接読む。
- oracle edit、read-only investigation、session lifecycle、または run isolation・session state の正本規則だけを確認したいときは、それぞれの専用仕様へ進む。

## hash
- 815c36f5e5d037913b54066f93d4d474cec59a0a6f7f05df9142860bf2a5ab50

# `feedback_report.md`

## Summary
- `cmoc feedback report` の仕様。feedback run の開始・再開、observation の validation／normalization、issue 単位の remediation・commit・rollback、intake wave、auto join、publication、recovery を定める。
- feedback observation や state、branch／run isolation などの関連仕様を参照しながら、問題報告を収集して安全な realization file 修正を統合する処理の入口となる。

## Read this when
- `cmoc feedback report` の CLI 契約、開始条件、既存 run の recovery、issue 処理、publication 結果を確認したいとき。
- feedback observation を issue identity にまとめ、remediation agent の結果を検証して issue 単位で commit・join する流れを調べるとき。
- 正常結果、`incomplete`、validation／agent／commit／merge／publication failure の扱いを確認するとき。

## Do not read this when
- raw observation の収集形式や reporter input の詳細だけを確認したいときは、feedback observation の仕様を直接読むべきである。
- feedback state の schema、checkpoint、high-watermark、report cut、atomic publication の詳細だけを確認したいときは、feedback state の仕様を直接読むべきである。
- 一般的な編集 run の隔離、join、abandon、差分検査を確認したいときは、editing run の共通仕様を直接読むべきである。
- 実装の起動パラメータや Structured Output schema を確認したいときは、参照先の oracle source を直接読むべきである。

## hash
- a9c8c19650d4628e4654a07688d5595439bb5ee072799887bcb59d083de542e7

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
- oracle file `cmoc oracle edit` の目的、入力確定と共通 prompt 構築、2 回の独立した編集 agent call、編集境界、実行順序、終了状態、primary report・ログ通知、および中断・排他制御を定めるサブコマンド仕様。

## Read this when
- `cmoc oracle edit` の実行条件、2 回の編集 call の扱い、agent に許可する編集範囲を確認したいとき。
- oracle edit の prompt 構築、差分の扱い、終了結果、report やログの保存規則を確認したいとき。

## Do not read this when
- oracle file の調査・参照だけを行う `oracle investigation` の仕様を確認したいとき。
- oracle 以外の編集や INDEX.md 生成の仕様を確認したいときは、対応するサブコマンド仕様へ直接進む。

## hash
- 255690eafe5c6b213f5dd57a1538bdeadd4339645c1fbfb37b5b2e8e3a7948e8

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
- `cmoc realization refactor fork` サブコマンドの正本仕様。realization file と oracle file の調査状態を同期・追跡し、agent call による所見調査、realization file の修正、Structured Output の受理、current fork の完了・中断・エラー処理、および report 生成までの一連の refactor workload を定義する。

## Read this when
- realization file または oracle file の調査要求を反復処理する refactor fork の挙動、state の同期と選択規則、処理単位の commit・rollback、完了理由、ユーザー中断、エラー、report、または join 後 hook を確認したいとき。

## Do not read this when
- realization file と oracle file の適合性そのものの判定基準を確認したいときは `oracle_and_realization.md` を読む。編集 run の共通 fork・join・abandon lifecycle を確認したいときは `editing_run.md` を読む。agent call の機械的検証や差分検証を確認したいときは `codex_exec_rule.md` を直接読む。

## hash
- f03d689699133f81eea5b16c82cb1393493535db076b1108b9fab41d0531c230

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
- 現在の session branch を session home branch に non-fast-forward merge し、session state を joined に更新して session を完了するサブコマンドの正本仕様。
- 引数は受け取らず、branch と session state は対応する session context から決定する。
- doctor preprocess、事前条件確認、branch 切替、merge、conflict 解消、state 更新、条件付き branch 削除、および全終了経路の primary report 保存を定める。

## Read this when
- session join の実行条件、branch の決定方法、merge 手順、session 完了処理を確認・変更するとき。
- session join で merge conflict が発生した際の agent call、oracle と realization の優先関係、解消完了条件を確認するとき。
- session join の成功・失敗時に保存する primary report の内容と保存先を確認するとき。

## Do not read this when
- 通常の git branch 間 merge wrapper の仕様を調べるとき。この対象は汎用 merge を定めていない。
- session の共通事前条件、branch model、feedback state、error handling そのものの正本を確認するときは、本文が参照する各共通仕様を直接読むべきである。
- conflict 解消用 prompt の正確な文面や起動パラメータを確認するときは、指定された conflict resolution builder の仕様を直接読むべきである。

## hash
- cd3cf49f29efd787f8d759d82b7560f022326356e177b7aedd18d874c837eb39

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
