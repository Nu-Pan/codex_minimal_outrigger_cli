# `doctor.md`

## Summary
- `cmoc doctor` コマンドの仕様を定義するエントリー。doctor preprocess の明示的な呼び出し、引数・事前条件、終了経路ごとの primary report 保存要件を確認する入口。

## Read this when
- `cmoc doctor` の引数、実行手順、事前条件を確認するとき
- doctor preprocess の実行結果を含む primary report の保存先・内容・対象終了経路を確認するとき
- `cmoc doctor` のコマンド仕様を変更または実装と照合するとき

## Do not read this when
- doctor preprocess 自体の検証・修復内容を確認したいときは、正本である `oracle/doc/app_spec/doctor_preprocess.md` を直接読む
- doctor に関連する診断用サブコマンドの個別仕様だけを確認するとき

## hash
- 3ac841bd58e673fbd25a431f4a8ea2222c30c0231315714db459e02ca50c9f8a

# `editing_run.md`

## Summary
- 編集 run を開始する workload と終了方法、同時実行制約、共通事前条件・開始処理、編集差分の扱いを定義する共通仕様。
- realization_apply・realization_refactor の明示的 join、feedback_report の self-join、run join／abandon の事前検証・差分検査・merge・cleanup・state 遷移を確認するための入口。
- fork・join・abandon の report 要件、terminal result、エラー時の扱い、および関連する正本仕様との責務境界を確認するための共通参照。

## Read this when
- 編集 run の lifecycle、active run の同時実行制約、run state の遷移を実装・変更・調査するとき。
- cmoc run join または cmoc run abandon の引数、事前条件、差分検査、merge、post-join、cleanup の挙動を確認するとき。
- realization_apply、realization_refactor、feedback_report の run 開始・終了経路や self-joining の扱いを確認するとき。
- fork・join・abandon report または terminal result の共通項目、保存、エラー報告を確認するとき。

## Do not read this when
- oracle file の詳細な run 隔離規則や session state schema 自体を確認する場合は、本文が指定する run_isolation.md または session_state.md を直接読む。
- realization_refactor 固有の refactor state 同期規則を確認する場合は、指定された realization_refactor.md を直接読む。
- feedback_report 固有の intake、issue commit、publication、recovery の詳細を確認する場合は、feedback.md と workload 固有仕様を直接読む。
- console と file log の terminal result の出力順序・共通 field の正本を確認する場合は、指定された console_and_file_log.md を直接読む。
- editing run lifecycle に該当しない oracle edit、read-only investigation、機械的更新、または session lifecycle の仕様だけを確認する場合。

## hash
- 8fc83d0c4d2fc37cc8769411fadbe4ca9751333ae331541861ef8f15e4b2a724

# `feedback_report.md`

## Summary
- `cmoc feedback report` の一回の invocation における feedback observation の検証・正規化、issue 単位の realization 修正、commit、wave 処理、自動 join、publication、recovery、および終了結果を定義する CLI 仕様。
- feedback remediation run の開始条件、隔離境界、agent call の制約、差分受理条件、issue state の確定、エラー・中断時の保持範囲を確認するための入口。

## Read this when
- `cmoc feedback report` の CLI 契約、run 開始・再開、wave loop、issue remediation、commit、automatic join、publication、または終了コードを実装・変更・検証するとき。
- feedback observation を issue に正規化する条件や、`human_required`・`incomplete`・`error` の扱いを確認するとき。
- feedback report、invocation report、current pointer、raw observation の保存・cleanup・recovery の整合性を調べるとき。

## Do not read this when
- feedback observation の収集規則そのものを確認したいときは `feedback_observation` の正本を読む。
- feedback の用語、結果分類、または repository-local state の一般契約を確認したいときは、それぞれの正本仕様を直接読む。
- 編集 run の共通仕様、branch model、run isolation、session state、Codex exec、または interruption の一般規則だけを確認する場合は、対応する oracle を直接読む。
- `cmoc feedback report` に固有でない realization 実装や、個別の remediation 対象の内容を調べる場合。

## hash
- ca3f852578588c18d97f0cc9931237a9b461b1eeae26e086570c6cd477784447

# `indexing.md`

## Summary
- `cmoc indexing` サブコマンドの仕様を定義する。現在の作業ツリーを明示的にインデクシングし、doctor preprocess、前提条件、実行手順、primary report の保存内容と終了経路を確認する入口。

## Read this when
- `cmoc indexing` の引数、未コミット差分がある場合の扱い、doctor preprocess を含む実行手順を確認するとき
- インデクシング実行要約の保存先、Front Matter、本文に含める報告項目を確認するとき

## Do not read this when
- インデクシング仕様そのものの詳細を確認する必要があり、参照先の indexing 仕様を直接読むべきとき
- `cmoc indexing` 以外のサブコマンドの仕様を確認するとき

## hash
- cf37de227f8fd370f800fa7436d45825224c6e50e93afbcfef7fbf1c5a76fdd3

# `oracle_edit.md`

## Summary
- `cmoc oracle edit` のサブコマンド仕様を扱う入口。oracle file の編集指示から、本命と仕様削減の agent call を実行する条件・順序・編集境界・終了報告を確認できる。

## Read this when
- `cmoc oracle edit` の引数、ユーザー指示の prompt 構築、doctor preprocess・indexing preflight・agent call の実行順序を確認したいとき。
- 本命または仕様削減 agent call の起動条件、失敗時の扱い、oracle file の編集範囲を確認したいとき。
- primary report、ログ、terminal result、Windows toast、未コミット差分の扱いを確認したいとき。
- このサブコマンドが通常の edit run と異なり、fork・join・worktree・run section を使わないことを確認したいとき。

## Do not read this when
- oracle file の一般的な判断基準や編集内容そのものを確認したいときは、本文で参照される `oracle_and_realization.md` または対象の oracle file を直接読む。
- prompt editor input の共通 lifecycle や codex exec の共通受け渡し規約だけを確認したいときは、参照先の app specification を直接読む。
- doctor preprocess、indexing、feedback、Windows toast の詳細仕様だけを確認したいときは、それぞれ本文で指定された正本仕様を直接読む。
- `cmoc oracle investigation` の file access 権限や realization file の責務を確認したいとき。

## hash
- 08ab5671397b699b8c36b1b7fb105b912c738d5e71efcb748eadac06454fa80f

# `oracle_investigation.md`

## Summary
- oracle file に関するユーザーの調査指示を受け取り、oracle file を根拠とする調査結果を回答する Codex CLI の TUI 起動入口。
- doctor preprocess、prompt editor input、起動パラメータ構築、および Codex CLI 起動までのサブコマンド手順を扱う。
- oracle file の調査境界と、調査結果から根拠となる oracle file を特定可能にする回答方針を示す。

## Read this when
- oracle file についてユーザーから調査指示を受け、調査用 TUI の起動経路や入力ライフサイクルを確認するとき。
- oracle file を根拠とする調査結果を Codex CLI の TUI で回答するサブコマンドの責務と制約を確認するとき。

## Do not read this when
- oracle file を扱う判断基準そのものを確認したいときは、本文が参照する oracle_and_realization の正本を直接読むとき。
- TUI の正確な prompt 文面、prompt part、workload 固有パラメータ、または選択理由を確認したいときは、builder の実装を直接読むとき。
- エディタ入力 handoff の共通仕様を確認したいときは、本文が参照する editor_input_handoff の正本を直接読むとき。
- Codex CLI の TUI 起動時に適用される設定範囲や終了時通知を確認したいときは、本文が参照する各 app_spec の正本を直接読むとき。

## hash
- 9ec4f066220f0d964e268d571b1dd20c9dde74a07f557f5667c8f8ddfdd19888

# `realization_apply.md`

## Summary
- 直近の oracle file 差分を realization file へ反映する realization apply fork の目的、追従範囲、agent call、終了処理を定義する仕様。

## Read this when
- realization apply fork の差分始点・終点や、oracle 変更の追従範囲を確認するとき。
- fork の agent call 実行条件、想定内差分、エラー処理、report 保存、join 後 hook を確認するとき。

## Do not read this when
- 編集 run に共通する fork・join・abandon の lifecycle だけを確認したいとき。
- oracle file と realization file の適合性基準そのものを確認したいとき。

## hash
- 56077d711ba3736e5cb7467db9983f244644f8e2b3ea2262d3c9ae30987b6512

# `realization_refactor.md`

## Summary
- realization refactor の fork workload として、oracle file・realization file の調査要求を状態管理し、current fork 内で未解決 target 以外を反復処理する仕様への入口。
- 調査・修正 agent call、変更 path の検証、refactor state の同期、処理単位の commit、および unresolved target の扱いを定義する。
- 自然完了・未解決付き完了・中断・エラーにおける完了条件、report、終了状態、終了コードを確認するための対象。

## Read this when
- realization refactor fork の開始、対象 file の選択、調査ループ、state 更新、変更確定の挙動を実装または確認するとき。
- current fork で unresolved target を扱う方法、完了理由、run state、report の要件を確認するとき。

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを確認したいとき。
- oracle file と realization file の適合性そのものを確認する場合は、正本である oracle_and_realization.md を直接読むとき。
- fork・join・abandon の共通 lifecycle や中断の共通動作だけを確認する場合は、対応する共通仕様を直接読むとき。

## hash
- b89f383f2adc33af8d1825bd79aa3ff07eebcb0b26b698b28538b8728f812e76

# `session_abandon.md`

## Summary
- アクティブな cmoc session を home branch に merge せず破棄し、session state の abandoned 遷移、branch 切替・削除、失敗時の rollback、primary report 保存までを定義するサブコマンド仕様。

## Read this when
- session の成果物を本流へ取り込まず session 自体を終了・破棄する処理を実装、変更、検証するとき。
- session abandon の事前条件、未 join の編集 run との関係、破棄してよい資源と保護対象、cleanup の手順や失敗時の復旧を確認するとき。
- session abandon の terminal result や primary report に必要な終了経路・状態遷移・診断情報を確認するとき。

## Do not read this when
- session の成果物を home branch に取り込む正常終了処理を扱うときは、session join の仕様を直接読む。
- 未 join の編集 run だけを破棄する処理を扱うときは、cmoc run abandon の仕様を直接読む。
- session state の共通事前条件や状態モデルそのものを確認するときは、参照先の session_state.md を直接読む。
- join 済みの結果を取り消す rollback を扱うときは、この仕様を rollback コマンドの仕様として用いない。

## hash
- 8a75eeaaaf59d96ecf78cf980cf29d9355faff7506c4a69006ede831f7925b03

# `session_fork.md`

## Summary
- `cmoc session fork` の引数なしサブコマンドについて、実行可能なブランチ条件、未コミット差分などの事前条件、セッションブランチ作成から初期状態保存までの実行手順を定義する。
- セッションブランチの命名、分岐元変更時の扱い、terminal result へのブランチ情報、および全終了経路で保存する primary report の要件を扱う。
- session fork のCLI挙動、セッション状態保存、ブランチ操作、終了報告の仕様を確認する際の入口となる。

## Read this when
- `cmoc session fork` の実装またはテストで、実行前提条件や処理順序を確認するとき
- セッションブランチの命名規則や任意 start point を受け付けない仕様を確認するとき
- session state の初期化、terminal result の固有結果、または primary report の保存内容を扱うとき
- fork の失敗経路、doctor preprocess、rollback、残存資源の報告要件を確認するとき

## Do not read this when
- ブランチの一般的な役割や分岐関係だけを確認したい場合は、正本である `oracle/doc/branch_model.md` を直接読むとき
- session state の schema や状態遷移の詳細だけを確認したい場合は、`oracle/doc/app_spec/session_state.md` を直接読むとき
- timestamp の形式だけを確認したい場合は、`oracle/doc/app_spec/timestamp.md` を直接読むとき
- `cmoc session fork` 以外のサブコマンドの固有仕様を確認するとき

## hash
- 9463c501aad0b1af8be915ed4edf1b2a8161a0a8b2d80958cf60ff31c54af4a8

# `session_join.md`

## Summary
- `cmoc session join` が、現在の session branch を session home branch へ戻すための専用 merge コマンドであること、引数・事前条件・実行手順・後始末を定義する。
- session 終了時の merge conflict 解消、oracle file の扱い、session state 更新、session branch 削除条件を確認するための入口となる。
- session join の全終了経路で保存する primary report の記録要件を定義する。

## Read this when
- `cmoc session join` の実装、変更、動作確認で、session branch と home branch の merge 手順を確認するとき。
- session join の事前条件、doctor preprocess、session state の `joined` 遷移、branch cleanup の扱いを確認するとき。
- merge conflict 発生時の conflict marker 解消、oracle file の優先順位、関連 agent call の要件を確認するとき。
- session join の primary report に必要な終了結果、branch HEAD、merge commit、state、conflict、cleanup、診断ログの内容を確認するとき。

## Do not read this when
- 汎用的な git merge の仕様や repository の branch model 全体だけを調べるとき。
- session の開始や active session context の共通事前条件を直接確認したいとき。
- repository-local feedback state の所有範囲や配置だけを確認したいとき。
- エラー分類やスタックトレースの共通規則だけを確認したいとき。

## hash
- 0cf233cba3cb4ef8a419bfd111dbb05d3dabdac849d7d247b07255fec090b76a

# `tui.md`

## Summary
- ユーザー入力へ cmoc 固有契約を注入し、適切な起動パラメータで AI Agent CLI/TUI を直接起動する `cmoc tui` サブコマンドの仕様入口。
- プロンプト編集入力、indexing preflight、feedback、Windows 通知、Codex CLI 固有の起動条件を確認できる。

## Read this when
- `cmoc tui` の実行手順、引数や事前条件を確認するとき。
- ユーザープロンプトへの cmoc 基本規定の注入条件や、TUI 起動前後の共通処理を確認するとき。
- Codex CLI を `codex` として起動するための設定・handoff 条件を確認するとき。

## Do not read this when
- プロンプトエディタ入力の正本仕様だけを確認したいときは、プロンプトエディタ入力仕様を直接読む。
- 起動する prompt part や workload 固有パラメータの選定理由を確認したいときは、`build_tui_launch_tui_parameter` の仕様を直接読む。
- oracle と realization の責務・適合性、indexing、feedback、Windows 通知など個別領域の詳細だけを確認したいときは、それぞれの正本仕様を直接読む。

## hash
- 061943035cf5aa2001c48985fe858fd6aca4df6597985f9a9db86094ca132fbf
