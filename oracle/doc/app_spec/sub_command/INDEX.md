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
- 編集 run を開始する workload 固有コマンドと、`cmoc run join`／`cmoc run abandon` で終了する共通 lifecycle の仕様を定義する。fork の共通事前条件・開始処理、想定内差分、state 遷移、join 時の差分検査・merge・hook・cleanup、abandon 時の破棄・cleanup、report と terminal result の要件を確認するための入口。

## Read this when
- `cmoc realization apply fork` または `cmoc realization refactor fork` の編集 run lifecycle を実装・変更・検証するとき。
- `cmoc run join` または `cmoc run abandon` の引数、事前条件、差分処理、state 遷移、merge、cleanup、report、terminal result の挙動を確認するとき。
- 編集 run と session lifecycle、oracle edit、read-only investigation、機械的更新の責務境界を判断するとき。

## Do not read this when
- `cmoc session join` や `cmoc session abandon` など外側の session lifecycle だけを扱うとき。
- `cmoc oracle edit`、read-only investigation、cmoc 自身による機械的更新、または session join の conflict 解消だけを扱うとき。
- run の隔離資源・一般 lifecycle、session／run 永続 state、refactor state 同期、feedback の正本仕様を直接確認する必要があるときは、それぞれ指定された oracle 文書を読む。

## hash
- dd99237359f5683ad98c8a9b7b2f29b4fa310b22b18f6fda9df34f4a458b9c9d

# `feedback_report.md`

## Summary
- pending observation と直前の active state を report cut に固定し、検証済み issue を新しい active state と Markdown report へ publication する `cmoc feedback report` の挙動仕様。
- normalization・verification agent の委譲境界、candidate の検証条件、正常 publication と `incomplete` 診断 report の分岐を定義する。
- state corruption、validation failure、AI call failure、ユーザー中断、cleanup failure などに対する state 保持、再開、report 保存、終了コードを定義する。

## Read this when
- `cmoc feedback report` の CLI 契約、事前条件、処理順序、report cut、agent call、publication、再開、または終了コードを確認するとき。
- feedback observation や feedback state の正本仕様を参照しつつ、report 処理全体の責務境界と失敗時の扱いを把握するとき。
- normalization agent または verification agent の呼び出し条件・入力制限・output 受理条件を確認するとき。

## Do not read this when
- raw observation の収集規則だけを確認したい場合は feedback observation の仕様を読むとき。
- feedback state の schema、lifecycle、active generation、または incomplete 診断 report の保存規則だけを確認したい場合は feedback state の仕様を直接読むとき。
- normalization や verification の正確な prompt、起動パラメータ、Structured Output schema を確認したい場合は、それぞれの builder と schema を直接読むとき。
- `INDEX.md` の更新手順だけを確認したい場合は indexing の仕様を直接読むとき。
- 中断時の共通動作だけを確認したい場合は subcommand interruption の仕様を直接読むとき。

## hash
- 301c021961d85989d77dab4d5646caa54025fec7e4276a62aeb5e0e3a6fdeb81

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
- 直近の git commit 群から読み取れる oracle file の変更を realization file へ反映する `realization apply fork` workload の目的、追従対象差分、agent call、実行手順、エラー処理、report、join 後 hook を定める仕様書。
- fork の正常終了時に、注入された commit 差分に対応する oracle file と realization file の齟齬を解消するための実行入口。

## Read this when
- realization apply fork の引数、差分の始点・終点、oracle file の rename を含む追従範囲を確認するとき
- 本命 agent call の起動方法、cwd、回数制約、realization file と oracle file の変更境界を確認するとき
- fork の実行手順、終了状態、commit・rollback、report 保存、feedback 記録、join 後の session 更新を確認するとき

## Do not read this when
- ファイル単位の網羅的な realization 追従や realization refactor の仕様を確認したいとき
- fork・join・abandon に共通する編集 run lifecycle の正本仕様を確認したいとき
- oracle file と realization file の適合性の一般原則を確認したいとき
- apply fork の launch parameter の正確な prompt や選択理由を確認したいとき
- feedback の共通収集・report 仕様を確認したいとき

## hash
- 2a1a36bf6ab24f0c17a20c9041a95a7581bd18921c91dd1538694213b4178bed

# `realization_refactor.md`

## Summary
- realization refactor fork の目的、対象範囲、apply との責務分担を確認したいときの正本仕様。
- refactor state の保存・同期、調査対象の選択、処理単位、unresolved target の扱いを確認するための実行仕様。
- fork の完了、中断、エラー、report・終了イベント、join 後 hook の振る舞いを確認するためのライフサイクル仕様。

## Read this when
- realization refactor fork の実装や挙動を調査・変更するとき。
- refactor state の schema、entry 集合の同期、調査要求の更新、選択順を確認するとき。
- agent call 後の変更 path 検証、所見の正規化、commit、unresolved target の管理を確認するとき。
- natural_completion、completed_with_unresolved、user_interruption、error の完了条件や report 内容を確認するとき。
- fork、join、abandon を含む realization refactor の編集 run lifecycle を確認するとき.

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを確認したいとき。
- oracle file と realization file の適合性基準そのものを確認したいときは、oracle_and_realization.md を直接読む。
- fork 共通の join・abandon lifecycle だけを確認したいときは、editing_run.md を直接読む。
- ユーザー中断の共通仕様だけを確認したいときは、subcommand_interruption.md を直接読む。
- 変更要約の生成規則だけを確認したいときは、change_summary.py とその委譲先を直接読む。

## hash
- 71841e43aa8208fe20ae53393d46c5d15a2da84776c52a7f38171c817f286b24

# `session_abandon.md`

## Summary
- `cmoc session abandon` は、現在の session branch を home branch に merge せず破棄し、session state を `abandoned` に更新する session 終了コマンド。join 済み結果の rollback や未 join 編集 run の破棄は担当せず、後者は `cmoc run abandon` を先に実行する。
- doctor preprocess、事前条件検証、home branch への切替、state 更新、session branch の強制削除、および失敗時の rollback を含む cleanup 手順を確認できる。
- 正常終了・エラー終了を問わず保存される session abandon の primary report 要件と、破棄対象・残存資源・次の操作・診断ログの記録内容を確認できる。

## Read this when
- session の成果物を本流へ取り込まず破棄したいとき。
- `cmoc session join` との違い、session branch と home branch の扱い、未 join の編集 run が残る場合の前提を確認したいとき。
- session abandon の実行手順、状態遷移、cleanup 失敗時の再実行条件、primary report の保存要件を確認したいとき。

## Do not read this when
- session の成果物を home branch に取り込む完了処理を確認したいときは、`cmoc session join` の仕様を直接読む。
- 未 join の編集 run を破棄したいときは、`cmoc run abandon` の仕様を直接読む。
- 既に join 済みの session 結果を取り消す rollback を確認したいとき。

## hash
- fd16472d23f6a9537220c8bb8f67d30faa267025f942dfd586175583630fa11f

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
- 日本語の技術文書として、session join の役割と実行責務を簡潔に示す入口。
- アクティブな session を home branch に統合して終了するコマンドの仕様を扱う。
- 事前検証、merge、conflict 解消、session state 更新、branch cleanup、primary report の終了経路を確認するための対象。

## Read this when
- `cmoc session join` の引数なしの実行契約や、session branch と home branch の関係を確認するとき。
- session 終了処理の事前条件、branch merge、merge conflict 時の解消委譲、state 遷移を調べるとき。
- join 実行の成功・エラーを含む primary report の保存内容や、cleanup・warning・次操作の扱いを確認するとき。

## Do not read this when
- 汎用的な git merge の仕様や branch model 全体を確認したいだけのときは、branch model の正本を直接読む。
- session の状態定義や共通事前条件だけを確認したいときは、session state の正本を直接読む。
- repository-local feedback state の所有範囲だけを確認したいときは、feedback state の正本を直接読む。
- 実装上の conflict resolution parameter の詳細だけを確認したいときは、対応する oracle 実装を直接読む。

## hash
- 205b001e606a930121c09d43acee7746b9312820813016ff04bbaee1338fa03f

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
