# `doctor.md`

## Summary
- `cmoc doctor` による doctor preprocess の明示実行と、実行結果を要約する primary report の保存要件を定める。
- 共通の検査・修復の内容は Doctor Preprocess の仕様が担い、この項目はコマンドの呼び出しと報告の入口となる。

## Read this when
- `cmoc doctor` の実行手順や、正常完了・エラー終了時の primary report の要件を確認するとき。

## Do not read this when
- doctor preprocess が行う検査・修復、その順序、reporter の事前検証や commit の条件を調べるときは、Doctor Preprocess の仕様を読む。
- doctor preprocess 後に検証される別サブコマンド固有の事前条件や処理手順を調べるときは、そのサブコマンドの仕様を読む。

## hash
- e004c75b5a42802cdae0ddd2d023d7ccf4b5fcc7f7065f6ee33a285dd6ad1330

# `editing_run.md`

## Summary
- realization apply、realization refactor、feedback report の編集 run に共通する開始条件、状態遷移、同時実行制約、差分確定、join・abandon の lifecycle を扱う。
- 共通の join 検査、merge と競合解消、後処理、cleanup、report の入口となる。workload 固有の処理や隔離資源・session state の正本定義は、それぞれの仕様に委ねる。

## Read this when
- 編集 run を開始できる条件や、active run の状態によって許される操作を確認するとき。
- join・abandon の共通事前条件、差分検査、merge、競合解消、失敗時の復旧、cleanup、report の扱いを確認するとき。
- realization apply・refactor の明示的 join と feedback report の自動 join に共通する lifecycle の範囲を確認するとき。

## Do not read this when
- realization apply の比較範囲、本命 call、fork report、join 後 hook の詳細を確認するときは、その workload 固有仕様を読む。
- realization refactor の state、調査 loop、処理単位、完了条件を確認するときは、その workload 固有仕様を読む。
- feedback report の intake、issue remediation、publication、固有 recovery を確認するときは、その workload 固有仕様を読む。
- run の隔離資源や session state の正本定義を確認するときは、各共通定義を直接読む。session fork・join・abandon、oracle edit・investigation、run を作らない更新、session join の競合解消も、それぞれの専用仕様を読む。
- workload または競合解消 call の正確な prompt、引数、起動パラメータを確認するときは、該当する builder 実装を読む。

## hash
- 0d7455112605d5b68550bed8daface9bacf931f6288aaee020e7a9cc4ce43570

# `feedback_report.md`

## Summary
- `cmoc feedback report` 固有の実行フローを定め、observation の取り込み・issue の正規化と修正・wave 処理・自動 join・report 公開をつなぐ。
- 正常完了、`incomplete`、中断、失敗時の公開・recovery・report・終了コードの扱いを確認する入口。共通 lifecycle や state schema の仕様は関連文書に委譲する。

## Read this when
- `cmoc feedback report` の開始条件、run の再開、issue 処理、wave の停止条件を確認または変更するとき。
- 自動 join、join 後の検証、正常または `incomplete` の publication と recovery を扱うとき。
- 中断・続行不能な失敗時の state 保持、invocation report、終了コードを確認するとき。

## Do not read this when
- observation の収集、入力形式、互換処理を確認するときは `feedback_observation.md` を読む。
- issue の用語や結果分類を確認するときは `feedback.md` を読む。
- feedback state の構造、checkpoint、report cut、atomic publication を確認するときは `feedback_state.md` を読む。
- run の共通 lifecycle や中断規則を確認するときは `editing_run.md` または `subcommand_interruption.md` を読む。
- agent の正確な prompt、Structured Output schema、起動設定を確認するときは本文が参照する builder・schema・config の対象を読む。

## hash
- a6c40521a4dcee74fce3a28555940e37e839f1dc0d44906229153232226bba4c

# `indexing.md`

## Summary
- `cmoc indexing` の引数、未コミット差分がないことを求める事前条件、doctor preprocess からインデクシングを実行する順序を定める。
- 正常終了とエラー終了の両方で保存する実行要約レポートの扱いを定める。

## Read this when
- `cmoc indexing` の実行条件、手順、エラー時の挙動を調べる・変更する場合。
- 実行要約レポートがいつ保存され、何を記録するか確認する場合。

## Do not read this when
- インデクシング自体の規則や `INDEX.md` エントリーの内容を調べる場合は、一般のインデクシング仕様を直接読む。
- doctor preprocess の責務や動作を調べる場合は、そのサブコマンドの仕様を直接読む。

## hash
- 8a2acc19195064829931578f12875ea420efb5ab64e1889c6c68e9ebfbad5381

# `oracle_edit.md`

## Summary
- `cmoc oracle edit` がユーザーの最終状態の指示を受け取り、同じ入力と設定で独立した編集 agent call を2回直列実行する流れを定める。
- 実行条件、oracle file に限る編集範囲、差分の保持と人間の確認責任、終了状態および実行報告の扱いを規定する。

## Read this when
- `cmoc oracle edit` の入力確定後の準備、2回の実行順序、設定の共用、または2回目が読む状態を確認するとき。
- 起動前条件、indexing の位置づけ、編集できるファイル、失敗時の差分保持、report や通知の流れを確認するとき。
- oracle file の編集を行うこのコマンドと、調査など別のサブコマンドとの責務境界を判断するとき。

## Do not read this when
- エディタ入力や handoff の共通 lifecycle 自体を確認するときは、その共通仕様を読む。
- Codex 呼び出し、失敗時の共通処理、ログや通知、doctor preprocess、indexing の一般規則を確認するときは、それぞれの共通仕様を直接読む。
- oracle file を変更せず TUI で調査結果を回答する手順を確認するときは、oracle investigation の仕様を読む。

## hash
- 5ec76df312829d2ce80ff45c7ea71133e733d5cc18e30621e48ac3f0151e9501

# `oracle_investigation.md`

## Summary
- `cmoc oracle investigation` 固有の処理順、調査用 TUI の起動、回答での根拠提示、および TUI agent のファイルアクセス境界を定める。
- oracle file の調査 command としての動作を確認する場合に参照する。共通の入力・handoff・起動規則は、それぞれの正本に委譲している。

## Read this when
- oracle file 調査 command の実行順、TUI 起動責務、調査回答の要件、または TUI agent のファイルアクセス境界を変更・照合するとき。
- oracle file の調査と、共通 TUI の動作や oracle file 編集 command との責務境界を判断するとき。

## Do not read this when
- プロンプトエディタの共通 lifecycle や editor input handoff の契約自体を変更するときは、それらを直接定める仕様を読む。
- 共通 TUI の起動条件、Codex CLI の設定、toast 通知、または indexing の規則自体を変更するときは、それぞれを直接定める仕様を読む。
- oracle file の編集 run を扱うときは、調査 command ではなく oracle 編集 command の仕様を読む。

## hash
- 5b8a4e5a85be4f752837abf5e689d6c7a775c36bc3f674e179f9fd458d6d4eb0

# `realization_apply.md`

## Summary
- 直近の commit 範囲から oracle file の変更を特定し、realization file へ素早く反映する `realization apply` の責務と完了条件を定める。
- 比較対象の決め方、追従作業の実行条件、fork report、および join 後に次回の比較始点を進める条件を扱う。

## Read this when
- 直近の oracle file 変更を realization file に反映する apply の対象差分、実行、報告、join 後 hook を確認するとき。
- 追従を完了できなかった変更を、次回 apply の比較範囲に残す仕様を確認するとき。

## Do not read this when
- oracle file と realization file をファイル単位で繰り返し調査する workload の仕様を確認するときは、realization refactor の項目を読む。
- fork、join、abandon の共通 lifecycle や run の共通差分検査・cleanup だけを確認するときは、編集 run の共通仕様を読む。

## hash
- 38bf98098c3488224d3d5b8f3dc778bfad358f2e3fcea02564d7867350ddd244

# `realization_refactor.md`

## Summary
- realization refactor fork の workload 仕様。oracle file と realization file をファイル単位で反復調査し、必要な realization 修正、調査状態の同期、未解決対象の扱いを定める。
- 調査対象の選択、処理単位と Structured Output の判定、完了・中断・エラー、report と終了結果を確認する入口。prompt の詳細と起動パラメータは専用 builder に、共通 lifecycle は共通仕様に委譲する。

## Read this when
- realization refactor fork の反復調査、refactor state、未解決対象、処理単位の確定、完了条件、中断後の扱い、report や終了結果を実装・変更・確認するとき。

## Do not read this when
- 短い変更ループを担う realization apply の仕様を確認するとき。
- oracle と realization の適合性判断基準だけを確認するときは、適合性の正本仕様へ進むとき。
- fork・join・abandon の共通 lifecycle やサブコマンドの共通中断動作だけを確認するときは、それぞれの共通仕様へ進むとき。

## hash
- f91f82d256a9ef4a85e0d11a467f2f691012756a42ac4f90610cf2c0f651c82e

# `session_abandon.md`

## Summary
- `cmoc session abandon` が、session branch を home branch に merge せず終了する際の条件と手順、破棄・保持する資源、失敗時の扱いを定める。session join 後の変更を取り消す用途には使えない。
- session の状態遷移、branch cleanup、terminal result と primary report の要件を確認する入口。

## Read this when
- active session 全体を home branch に取り込まず破棄する正規の手順や、実行前提・保持すべき資源を確認するとき。
- abandon の途中で失敗した場合の rollback と再実行、および各終了経路での report 要件を確認するとき。

## Do not read this when
- session branch を home branch に merge して完了する手順や conflict の扱いを確認するときは、`cmoc session join` の仕様へ進む。
- 未 join の編集 run だけを破棄し、session を保持する手順を確認するときは、編集 run の共通仕様へ進む。
- session と編集 run の共通 state schema や事前条件を確認するときは、共通 lifecycle の仕様へ進む。

## hash
- ffd3b1f597884c62786ac8e70163fb71116742e2d3a73500231b187d2e2b9f36

# `session_fork.md`

## Summary
- `cmoc session fork` の事前条件、local branch からの session branch 作成、初期状態の保存、および実行要約の扱いを定める。

## Read this when
- 新しい session の分岐元や fork の実行条件、branch 作成・初期化、失敗時を含む実行要約の仕様を確認または変更するとき。

## Do not read this when
- session の取り込みや破棄を扱うときは、それぞれの join または abandon の仕様へ進む。
- branch の共通命名・役割や session state の共通スキーマ・遷移だけを調べるときは、それぞれの正本へ進む。

## hash
- ecba04632a0bb7a01b4f1564c7c549999206201fe1c990f8297f3d9ed56e3267

# `session_join.md`

## Summary
- `cmoc session join` が現在の session branch を session の home branch に merge して session を完了する際の、コマンド固有の実行と後処理を定める。
- home branch の進行、競合解消の呼び出しと失敗時の扱い、安全な branch cleanup、実行要約の保存を確認する入口。

## Read this when
- `cmoc session join` の実行順序、session state の遷移、merge 後の cleanup や実行要約を変更・調査するとき。
- session join が home branch への merge をどう進め、競合解消や失敗をどう扱うか確認するとき。

## Do not read this when
- session の作成や、merge せずに破棄する手順を確認するときは、それぞれの session fork / abandon の仕様を読む。
- branch と commit の共通定義、session の共通事前条件・state schema、共通の競合解消判断やエラー分類が必要なときは、それらを定める仕様を直接読む。この文書は session join 固有の利用方法を定める。
- `cmoc run join` や feedback report による自動 join の実行手順を確認するとき。これらは別のコマンド仕様で扱う。

## hash
- ec27889b327dd0f6adbc0741aa24d24339f24cb60e6a69a06a3f955f01b9e926

# `tui.md`

## Summary
- `cmoc tui` の実行順序、未コミット差分がある場合の扱い、AI Agent CLI/TUI 起動に共通する契約と Codex CLI 固有の契約を定める。
- 起動パラメータの詳細や関連する各 lifecycle の意味仕様への委譲先を示し、TUI 起動全体の責務分担を確認する入口となる。

## Read this when
- `cmoc tui` の前処理からプロンプト受領、起動パラメータ構築、TUI 起動までの流れや実行条件を確認するとき。
- TUI に注入する cmoc 基本規定の適用境界、または Codex CLI 起動時の契約を確認するとき。

## Do not read this when
- エディタ入力の確定手順や editor input handoff の詳細を確認するときは、それぞれの共通仕様を直接読む。
- TUI の正確な prompt part、文面、workload 固有パラメータ、またはその選択理由を確認するときは、委譲先の builder 定義を読む。
- 注入される oracle・realization 規定の意味、indexing、feedback observation、Windows toast の詳細を確認するときは、それぞれの正本仕様を直接読む。
- Codex CLI の環境変数、preflight validation、設定上書き、editor input handoff MCP の詳細を確認するときは、Codex CLI 共通規則を直接読む。

## hash
- bf2c7386391bfad7fdb2fbd081d3d5fda57bf91649fb4f3d12c2862e79fce97c
