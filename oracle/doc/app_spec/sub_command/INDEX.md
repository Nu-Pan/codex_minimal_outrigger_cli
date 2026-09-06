# `doctor.md`

## Summary
- `cmoc doctor` の実行契約を定義し、引数なしで doctor preprocess を呼び出すコマンドの入口。
- doctor preprocess の検証・修復内容そのものではなく、実行結果を primary report として保存する終了時の報告要件を扱う。

## Read this when
- `cmoc doctor` の引数、事前条件、実行手順を確認するとき。
- doctor 実行の全終了経路で保存する primary report の内容、保存先、共通メタデータを確認するとき。

## Do not read this when
- doctor preprocess が実施する検証・修復の正本仕様を確認するとき。
- doctor 以外のコマンドの実行手順やレポート要件を確認するとき。

## hash
- 35ddacab31389bb490d979027e9409dcb0ecc2728ec48f8ebb294d20968d99a6

# `editing_run.md`

## Summary
- 編集 run を開始・終了する共通ライフサイクル仕様。realization apply/refactor と feedback report の run 種別、隔離資源、差分、join・abandon、状態遷移、report、merge 後処理を定義する。
- workload 固有仕様から共通の run 開始条件、同時実行制約、join・abandon の扱いを確認するための上位入口。

## Read this when
- 編集 run の fork、join、abandon、self-joining feedback run のライフサイクルを実装・変更・調査するとき。
- run state、branch、worktree、fork commit、想定内差分、merge、cleanup、terminal report の共通要件を確認するとき。
- realization_apply、realization_refactor、feedback_report の workload 固有仕様が共通 lifecycle とどう接続するかを確認するとき。

## Do not read this when
- 編集 run の対象 workload 固有の intake、issue 処理、publication、refactor 同期などの詳細だけを確認したいときは、対応する workload 固有仕様を直接読む。
- session lifecycle、session state の正本定義、run isolation の詳細、console・file log の表示仕様だけを確認したいときは、本文が参照する各正本仕様を直接読む。
- read-only investigation、cmoc oracle edit、run を作らない機械的更新、または session join の conflict 解消だけを扱うとき。

## hash
- dd852eb1fef4a5b5ea26d3de6cf1ffd6030375ff5a7dd66d7ef5a0ece7ba521f

# `feedback_report.md`

## Summary
- `cmoc feedback report` の仕様を定義し、feedback observation の intake、issue の normalization・remediation、issue 単位の commit、wave 処理、自動 join、publication、interruption・error recovery、および report・終了コードの契約を示す。

## Read this when
- `cmoc feedback report` の公開 CLI 契約、開始・再開条件、feedback remediation run の隔離境界を確認するとき。
- observation を issue identity に正規化し、remediation agent の呼び出し、差分検査、verification、commit、rollback の扱いを決めるとき。
- intake wave と high-watermark、正常 publication、`incomplete`、user interruption、error 後の recovery を実装または確認するとき。
- feedback report の保存形式、掲載対象、current evidence、状態遷移、終了コードを確認するとき。

## Do not read this when
- raw observation の収集規則だけを確認する場合は feedback observation の正本を読む。
- feedback の用語・結果分類だけを確認する場合は feedback の正本を読む。
- repository-local state や atomic publication の schema・永続化契約だけを確認する場合は feedback_state の正本を読む。
- 編集 run 共通の join・abandon・隔離規則だけを確認する場合は editing_run および関連する共通仕様を直接読む。
- normalization または remediation agent の prompt、起動パラメータ、Structured Output schema を確認する場合は対応する oracle の実装・schema を直接読む。

## hash
- 1e84569cf6a67570ac9cf21bbe4e4ddf0bb41d927be73a6aa72e22e5fe14facb

# `indexing.md`

## Summary
- 対象は `cmoc indexing` サブコマンドの仕様で、現在の work-root を明示的にインデクシングする実行条件・手順・完了報告を定義する。
- インデクシング対象の仕様や全体ルールを確認する入口であり、インデクシング処理の実装詳細や診断サブコマンド単体の仕様を直接扱う文書ではない。

## Read this when
- `cmoc indexing` の引数、未コミット差分に関する事前条件、doctor preprocess を含む実行手順を確認したいとき。
- インデクシングの成功・失敗を問わず保存される primary report の内容、保存先、実行結果の要約要件を確認したいとき。
- `INDEX.md` の生成・更新や commit 結果を含む、明示的なインデクシング実行の終了時報告を確認したいとき。

## Do not read this when
- インデクシングそのものの詳細な仕様や対象範囲を確認したいときは、参照先のインデクシング仕様を直接読む。
- doctor preprocess の診断動作や個別の診断サブコマンドの仕様だけを確認したいとき。
- 実装コードの内部構造、INDEX.md のルーティング規則、または report の一般形式だけを確認したいときは、それぞれを定義する文書へ直接進む。

## hash
- 7f59d1e48db892dee054e3cab8ec4c81b4d66fec40e6244f1ada935636859ae4

# `oracle_edit.md`

## Summary
- `cmoc oracle edit` は、oracle file へのユーザー指示の反映と、その成功後の仕様削減を、2 回の独立した `codex exec` agent call として直列実行するサブコマンドです。
- editor input、doctor preprocess、indexing preflight、起動前条件検査、agent call、primary report 保存、terminal result 通知までの実行ライフサイクルを扱います。
- oracle file のみを agent の編集対象とし、既存の未コミット差分を分離せず、agent call 成功時の最終差分を人間が確認・管理する契約を定義します。

## Read this when
- `cmoc oracle edit` の実行順序、起動条件、agent call の構成、失敗時の扱いを確認するとき。
- oracle edit における editor input、prompt 構築、仕様削減 agent call、編集境界を確認するとき。
- primary report、ログ、terminal result、Windows toast、終了状態、既存差分の扱いを確認するとき。

## Do not read this when
- oracle file の一般的な編集判断基準を確認したいだけで、`cmoc oracle edit` 固有の実行契約を扱わないとき。
- prompt 構築、`codex exec` 共通規約、indexing、doctor preprocess、session state、Windows toast の詳細仕様を直接確認するときは、それぞれ指定された正本文書を読む。
- 実装ファイルや realization file の責務を確認するとき。

## hash
- 3483a795b3621100f089c637943763303b9bb45e5bbad323238fc70dee7b3cda

# `oracle_investigation.md`

## Summary
- oracle file に関するユーザーの調査指示を受け取り、正本仕様を根拠に Codex CLI の TUI で調査結果を回答するサブコマンド。
- エディタ入力のライフサイクルと専用 builder による起動パラメータ構築を経て TUI を起動し、oracle file の変更や realization file の読み書きは行わない。

## Read this when
- oracle file の内容を根拠にユーザーの調査指示へ回答する実行経路を確認するとき。
- エディタから調査指示を受け取り、専用の TUI 起動パラメータを構築して Codex CLI を起動する流れを確認するとき。
- 調査結果の言語、根拠の示し方、oracle file・realization file・自動 commit の扱いを確認するとき。

## Do not read this when
- oracle file 自体の内容や判断基準を直接確認したいときは、対象の oracle file または oracle_and_realization.md を読む。
- エディタ入力 handoff の共通仕様を確認したいときは、editor_input_handoff.md または prompt_editor_input.md を直接読む。
- TUI の一般的な起動仕様や Windows toast 通知の仕様を確認したいときは、sub_command/tui.md または windows_toast_notification.md を直接読む。
- 実装上の正確な prompt 文面や prompt part、workload 固有パラメータを確認したいときは、launch_tui.py の builder を直接読む。

## hash
- 4487f91958b4632b99f9eb99b032d1370317f94a21179bdc5c9aa5d168c8e11c

# `realization_apply.md`

## Summary
- 直近の git commit 群から読み取れる oracle file の変更を realization file へ反映する fork の実行契約を定める。
- 差分範囲の決定、oracle file の rename を含む追従対象、単一の本命 agent call、realization file のみの変更、INDEX.md の生成、commit と run state の更新を扱う。
- fork の終了 report、feedback observation、join 後の session 更新まで含む realization apply の運用入口である。

## Read this when
- realization apply fork で追従すべき差分範囲と対象 file を判断するとき。
- 本命 agent call の実行条件、変更可能な file、commit・rollback・run state の完了条件を確認するとき。
- fork report に記録する終了結果、差分始点、変更 path、feedback observation、および join 後 hook を確認するとき。

## Do not read this when
- fork・join・abandon に共通する lifecycle の詳細だけを確認したいときは、編集 run の共通仕様を直接読む。
- prompt 文面、prompt part、builder 引数、起動パラメータの構築方法を確認したいときは、指定された launch_exec 実装を直接読む。
- oracle file に対する realization file の適合性や追従要否の判定基準だけを確認したいときは、oracle と realization の適合性仕様を直接読む。
- 実際の realization file の実装内容や、ファイル単位の網羅的な refactor を確認したいときは、該当する realization file または realization refactor の仕様を直接読む。

## hash
- 41f5a4d9ac92f2fba1eec966f8b47708a0cf72919da57ad559a9ff8549532812

# `realization_refactor.md`

## Summary
- realization refactor の fork workload として、oracle file・realization file の追従調査、修正、検証、state 同期、commit、完了判定を定義する。
- current fork の unresolved target を除外しながら、調査対象の選択から処理単位の結果確定までを管理する。
- refactor state の履歴管理、fork の中断・エラー処理、終了 report と lifecycle の要件を定義する。

## Read this when
- realization refactor fork の開始条件、調査対象、処理順序、1 処理単位の判定を確認するとき
- unresolved target を含む refactor loop の継続条件や完了理由を確認するとき
- refactor state の同期規則、commit 単位、中断・エラー時の処理、終了 report の要件を確認するとき

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを確認するとき
- fork・join・abandon の共通 lifecycle の詳細だけを確認するとき
- oracle file に対する realization file の適合性基準そのものを確認するとき

## hash
- 89a4c3d54e560fdd40193e5abeb550e014035545baa750d2f8e11b434d025205

# `session_abandon.md`

## Summary
- アクティブな cmoc session を home branch へ merge せず破棄するサブコマンドの正本仕様。事前条件、破棄対象と保護対象、cleanup 手順、状態遷移、失敗時の rollback、primary report の要件を定義する。

## Read this when
- session の成果物や未 join の編集 run を本流へ取り込まず破棄したいときのコマンド仕様を確認する場合
- session abandon の事前検証、branch 切替・削除、session state 更新、終了結果または report の要件を調べる場合
- session join との違い、run abandon が必要となる境界、cleanup 失敗時の再実行条件を確認する場合

## Do not read this when
- session を完了して home branch へ成果物を取り込む手順を確認したい場合は session join の仕様を読む
- 未 join の編集 run 自体を破棄する方法を確認したい場合は run abandon の仕様を直接読む
- session の状態や共通事前条件の定義そのものを確認したい場合は session_state.md を直接読む

## hash
- dcee5ddd525edb5597a77c5f94ebceb3acd123378add92e2dec284ca25ab3c9d

# `session_fork.md`

## Summary
- 現在のローカルブランチから新しい cmoc セッションブランチを作成し、session 情報・初期状態を保存するサブコマンドの仕様。
- 実行前提、分岐元と命名規則、任意 start point を受け取らない仕様、成功時の terminal result、および全終了経路の primary report 保存を定義する。

## Read this when
- cmoc session fork の実行条件、拒否される branch や作業状態、分岐・checkout・session state 保存の手順を確認するとき。
- セッションブランチ名、session ID、実行前後の状態、失敗時の rollback・残存資源、診断ログを含む fork 実行結果や report の仕様を確認するとき。

## Do not read this when
- セッション fork 以外の session サブコマンドの仕様を確認したいとき。
- branch の役割や分岐関係そのものの正本を確認したいときは branch_model.md を、session state の schema や状態遷移を確認したいときは session_state.md を直接読む。
- timestamp の形式だけを確認したいときは timestamp.md を直接読む。

## hash
- f93cd284058e02e3f271421643c5f19985e5a2f248e543480684c68d69d53b4b

# `session_join.md`

## Summary
- 完了済みの session branch を home branch へ戻す `cmoc session join` の実行契約を定義する。branch 切替・no-ff merge・conflict 解消・session state 更新・branch cleanup・primary report までの完了経路とエラー時の扱いを確認する入口。

## Read this when
- `cmoc session join` の引数、事前条件、merge source/target、home branch が進んだ場合の挙動を確認するとき
- merge conflict の解消手順、oracle file の編集優先順位、agent call の扱いを確認するとき
- session state、session branch cleanup、primary report の生成内容や終了経路を実装・検証するとき

## Do not read this when
- 通常の git branch 間 merge wrapper の仕様を確認したいとき
- session の状態定義や共通事前条件そのものを確認したいときは、session_state の該当仕様を直接読む
- branch model、feedback state、error handling の正本詳細を確認したいときは、それぞれの oracle file を直接読む

## hash
- d3f0a973b31b73db9b53f0b3b79a1d9f4aced09554aa040a086b399e1680d1df

# `tui.md`

## Summary
- ユーザーのオリジナルプロンプトに cmoc 固有契約を注入し、doctor preprocess、エディタ入力、起動パラメータ構築を経て AI Agent CLI/TUI を起動する `cmoc tui` の全体仕様。
- 全バックエンド共通の規定、TUI 起動前の indexing preflight、feedback observation、Windows toast 通知、および Codex CLI 固有の起動条件への入口。

## Read this when
- `cmoc tui` の実行手順、未コミット差分がある場合の実行条件、または TUI 起動時に適用される cmoc 固有契約を確認したいとき
- TUI 起動に関する共通規定や Codex CLI の起動条件を調査する入口を探しているとき

## Do not read this when
- プロンプトのエディタ入力 lifecycle の詳細を確認したいとき
- prompt part の選択、workload 固有の起動パラメータ、またはその選択理由の実装を確認したいとき
- oracle file と realization file の責務・適合性、indexing、feedback observation、Windows toast 通知の詳細仕様を直接確認したいとき

## hash
- 12855333eacd44ad20a4d4bc55056d10d8fd1a57db3faf3c4a55337c7e8079b2
