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
- 編集 run を開始・終了する共通 lifecycle の正本で、対象 workload、同時実行境界、開始・編集・join・abandon の共通規則、report と terminal result の要件を定める。
- realization apply/refactor の明示 join と feedback report の self-joining、差分検査・merge・post-join・cleanup の扱いを確認する入口。

## Read this when
- 編集 run の開始条件、active run の制約、run state の遷移、隔離資源、想定内差分を確認するとき。
- cmoc run join または cmoc run abandon の事前条件、差分検査、merge/破棄、cleanup、report 内容を実装・調査するとき。
- feedback_report の自動 join、recovery、publication 前後の扱いを確認するとき。

## Do not read this when
- cmoc session join/abandon など外側の session lifecycle を扱うとき。
- cmoc oracle edit、read-only investigation、run を作らない機械的更新、または session join の conflict 解消だけを扱うとき。
- workload 固有の apply/refactor/feedback の詳細仕様、session state、run isolation の正本を直接確認すべきとき。

## hash
- a43d81e74fa9176411a2415754f3e14f3415e2ec3df14f0ab6a6c7e0f89709fc

# `feedback_report.md`

## Summary
- `cmoc feedback report` の公開 CLI 契約と、feedback remediation run の開始、隔離、issue 処理、wave loop、自動 join、publication、recovery、中断、エラー、および終了コードを定義する正本仕様。
- feedback observation を validation・normalization・deduplication し、issue 単位で realization file を修正・検証・commit する処理全体の入口。
- 正常 report、`incomplete` 診断 report、user interruption・error 時の invocation report における保存内容と表示境界を定義する。

## Read this when
- `cmoc feedback report` の CLI 挙動や実行順序を実装・変更・検証するとき。
- observation の取り込み、issue identity の確定、remediation call、差分検証、issue commit、rollback、再確認を扱うとき。
- intake wave、high-watermark、自動 join、join 後検査、publication、cleanup、recovery の条件を確認するとき。
- 正常完了、`incomplete`、user interruption、または error の state・report・終了コードを確認するとき。

## Do not read this when
- raw observation の schema、収集、または reporter input v1 の互換処理だけを確認したい場合は、feedback observation の仕様を直接読む。
- feedback state の schema、current pointer、report cut、high-watermark、または atomic publication の詳細だけを確認したい場合は、feedback state の仕様を直接読む。
- branch、fork、join、run isolation、または編集 run の一般共通契約だけを確認したい場合は、branch model、run isolation、または editing run の仕様を直接読む。
- normalization・remediation の prompt、起動パラメータ、または Structured Output schema だけを確認したい場合は、対応する ACP builder と schema を直接読む。
- 一般的な realization refactor の処理単位規則だけを確認したい場合は、realization refactor の仕様を直接読む。

## hash
- ac9ab808f6ed768933216ba55c49579e2906144bfff56ff4fd2851b1dd267f1b

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
- `cmoc oracle edit` の目的、入力、実行前条件、本命・仕様削減の2回の agent call、編集境界、終了状態、primary report、ログ通知、および中断・排他制御を定義するサブコマンド仕様。

## Read this when
- `cmoc oracle edit` の引数、ユーザー指示からの prompt 構築、doctor preprocess・indexing preflight・agent call の実行順序を確認したいとき。
- 本命 agent call と仕様削減 agent call の判断材料、失敗時の扱い、oracle file の編集権限を確認したいとき。
- primary report、console・ログ・Windows toast、未コミット差分の扱い、終了状態を確認したいとき。

## Do not read this when
- oracle file の個別編集基準そのものを確認したいときは、参照先として指定された oracle 関連仕様を直接読むべきとき。
- 共通の editor input lifecycle、codex exec 規約、doctor preprocess、indexing、session state、feedback、toast の詳細だけを確認したいとき。
- `cmoc oracle edit` 以外のサブコマンドの仕様や、実装コードの具体的な構造を確認したいとき。

## hash
- 4d0e72b7a281b70933dcbc795febfc3b58b6db36e9480c8a24b9c00fda43d87d

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
- realization apply の fork における追従対象差分、agent call、成果物確定までの実行契約を定義する仕様。
- oracle file の変更を realization file へ反映する apply 処理の開始条件、差分範囲、エラー、report、join 後の状態更新を確認する入口。

## Read this when
- realization apply の fork がどの commit 範囲を対象にし、どのファイルを追従させるか確認するとき。
- apply 固有の agent call を一回実行する条件、変更可能なファイル、完了判定、エラー処理を確認するとき。
- fork report の記録内容や、join 成功後に次回 apply の比較始点を更新する条件を確認するとき.

## Do not read this when
- fork・join・abandon に共通する編集 run の lifecycle だけを確認したいときは、共通 lifecycle の正本を直接読む。
- oracle file と realization file の一般的な適合性判断だけを確認したいときは、その適合性を定義する正本を直接読む。
- realization file の網羅的な refactor や apply 以外の sub-command の挙動を確認するとき。

## hash
- 3765d5cf947931bec3b322703a1a07634977bff3b813031fc2eadb9f3bdff421

# `realization_refactor.md`

## Summary
- oracle file と realization file の追従調査・修正を繰り返す realization refactor fork の実行仕様。
- refactor state、current fork の unresolved target、処理単位の検証と結果正規化、state 同期、commit を定義する。
- 自然完了、unresolved 付き完了、中断、エラーにおける report、終了状態、終了コードを定義する。

## Read this when
- realization refactor fork の目的、起動条件、引数、想定内差分を確認したいとき。
- 調査対象の選択、agent call、変更差分検証、state 更新、unresolved target の扱いを確認したいとき。
- fork の完了条件、中断・エラー時の整合性、report 内容、終了イベントを確認したいとき。

## Do not read this when
- realization apply の短い変更ループの仕様だけを確認したいとき。
- fork、join、abandon に共通する編集 run の lifecycle だけを確認したいとき。
- oracle file と realization file の適合性判定、または Codex call の共通機械検証規則だけを確認したいとき。

## hash
- 83a2e63ac671c56b95f913a6e844a621fcbe7af9781b259f646189cf6844a3da

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
- `cmoc session fork` の仕様を扱うサブコマンド文書。現在のローカルブランチからセッション用ブランチを作成・checkoutし、セッション情報と初期状態を保存する処理の入口。
- 実行可能な前提条件、分岐元・命名規則、実行手順、終了時の primary report 保存要件を確認するための文書。

## Read this when
- `cmoc session fork` の引数、実行前提、分岐元、ブランチ命名、セッション初期化の仕様を確認するとき。
- fork の成功・失敗を含む終了経路で、session fork report に何を保存するかを確認するとき。

## Do not read this when
- セッションブランチの役割や分岐関係そのものを確認したい場合は、正本である branch model の概要を直接読むとき。
- セッション状態の項目定義や schema を確認したい場合は、session state の仕様を直接読むとき。
- タイムスタンプの形式だけを確認したい場合は、timestamp の仕様を直接読むとき。

## hash
- 0ca77525d7360574d63612f48aa5628a98bc9fab2847214250fe5d35bc30a127

# `session_join.md`

## Summary
- `cmoc session join` の責務、実行手順、conflict 解消、session state 更新、primary report を定義する session 完了用コマンド仕様。
- 現在の session branch を home branch へ merge して session を joined にする処理の入口であり、merge source・target の判断や branch model の確認が必要な場合に読む。
- merge conflict、oracle file の扱い、conflict 解消 agent call、branch cleanup、終了 report の要件を確認するための仕様。

## Read this when
- session を完了して home branch へ戻す `cmoc session join` の挙動、事前条件、merge、state 更新、cleanup を確認するとき。
- merge conflict の解消手順や oracle file の編集優先順位、conflict 解消用 agent call の委譲条件を確認するとき。
- join の全終了経路で保存する primary report の記録項目や、エラー時の次の操作を確認するとき。

## Do not read this when
- 通常の git branch 間 merge wrapper の仕様を確認したいとき。
- session join 以外の session 作成・編集・終了共通事前条件の詳細を確認したいときは、対応する session state 仕様を直接読む。
- merge source・target や default branch の正本定義を確認したいときは branch model を直接読む。
- feedback state の所有範囲と配置を確認したいときは feedback state 仕様を直接読む。

## hash
- 55b31bff3d705923a067bfaec3867b159b0e39a91b28e7bc48ae81937b73ef0e

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
