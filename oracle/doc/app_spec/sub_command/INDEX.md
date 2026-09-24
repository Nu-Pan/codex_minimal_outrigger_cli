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
- `cmoc feedback report` のコマンド固有仕様。raw observation の intake と issue の正規化、issue ごとの確認・修正・検証・commit、session branch への自動 join を定める。
- wave 処理の完了、publication と recovery、正常・incomplete・中断・エラー時の report と終了結果を定める。正常な人間向け issue 一覧には `human_required` の issue を掲載する。

## Read this when
- `cmoc feedback report` の事前条件、run 開始・再開、intake、issue 処理、修正受理条件の実装や適合性を確認するとき。
- feedback run の wave 完了、自動 join、report の publication、失敗後の recovery、中断・エラー時の表示や終了結果を調べるとき。

## Do not read this when
- observation の報告基準、MCP 受付、機械検出、raw observation の保存だけを扱うときは、feedback observation の収集仕様から読む。
- issue の結果分類の意味や feedback 全体の目的・既存 workload との境界だけを扱うときは、feedback の全体仕様から読む。
- repository-local state の artifact、checkpoint、report cut、atomic publication、cleanup の契約だけを扱うときは、feedback state の仕様から読む。
- 編集 run の一般的な join・abandon lifecycle や隔離規則だけを扱うときは、編集 run の共通仕様から読む。

## hash
- 82adddf2397f1d4791e2b306f2f8c97d8a225833eeb4524f5805950a82212028

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
- oracle file の最終状態を指示に沿って編集する `cmoc oracle edit` の仕様を定める。共通の prompt と設定で新しい Codex session を直列に 2 回呼び出す手順、編集範囲、終了条件、実行報告を確認する入口。

## Read this when
- `cmoc oracle edit` の実行順序、2 回の agent call、入力や設定の確定方法を変更・確認するとき。
- oracle edit の agent に許される編集範囲や、差分を保持する終了条件を確認するとき。
- oracle edit の事前条件、失敗時の扱い、primary report や通知の要件を調べるとき。

## Do not read this when
- oracle file の調査や質問への回答など、編集を伴わない oracle workload の責務を確認するとき。
- realization apply/refactor や feedback report の fork・join・abandon 共通 lifecycle を確認するとき。
- 共有の editor input handoff lifecycle や Codex exec 共通規則そのものを確認するとき。

## hash
- 78c1f11b1bdeec091edb32b1cc541deed2884539ea8e67ca9d03374b9dfcc485

# `oracle_investigation.md`

## Summary
- oracle file に関する調査指示を受け取り、oracle file を根拠に TUI で回答するサブコマンドの意味上の仕様を定める。
- 調査指示の入力から TUI 起動、調査結果の扱いまでを確認する入口。正確な prompt と workload 固有の起動パラメータは実装側の builder に委譲される。

## Read this when
- oracle file の調査を実行するサブコマンドの責務や処理順序を確認するとき。
- 調査結果の回答方法や、調査中の oracle file と realization file の扱いを確認するとき。

## Do not read this when
- oracle file を編集するサブコマンドの仕様を確認するときは、編集専用の仕様へ進む。
- 汎用 TUI の起動条件や共通設定を確認するときは、汎用 TUI の仕様へ進む。
- エディタ入力の共通 lifecycle や正確な prompt 構築を確認するときは、それぞれの共通仕様または実装側の builder を直接読む。

## hash
- 5d3dd339645564c99bee0caf6691554fdbcafc0838ffcc69d2d2cf41383831c7

# `realization_apply.md`

## Summary
- realization apply fork の workload 固有仕様。commit 範囲内の oracle 変更を関連する実装へ反映し、追従結果と次回比較範囲の更新を定める。

## Read this when
- oracle 変更を commit 範囲に沿って realization へ反映する apply の対象範囲、実行、報告、または join 後の扱いを確認するとき。

## Do not read this when
- fork・join・abandon の共通 lifecycle や競合解消だけを確認するときは、編集 run の共通仕様を読む。
- oracle と realization の適合性の一般基準だけを確認するときは、その適合性を定める共通仕様を読む。
- commit 範囲に限らない網羅的な realization 調査を行うときは realization refactor を、正確な prompt や起動パラメータを確認するときは apply の起動処理を読む。

## hash
- 157bca255b589aa3e1b86622a0c1f0102bc0a9a83a6a7ed5c63396de014c082f

# `realization_refactor.md`

## Summary
- realization refactor fork のファイル単位調査を定義し、対象 file の調査状態、同期、選択順、および full refactor cycle の進行を扱う。
- 処理単位ごとの調査・修正結果の受理、所見の正規化、unresolved target の扱い、完了・中断・エラー時の状態と report を定める。

## Read this when
- realization refactor fork の対象集合、refactor state、調査順、または loop の動作を調べる・変更する場合。
- この fork 固有の所見処理、commit 境界、unresolved 付き完了、終了 report や終了コードを確認する場合。
- ファイル単位で全体を調査する refactor と、直近の oracle 変更を反映する apply の責務の違いを確認する場合。

## Do not read this when
- fork・join・abandon の共通 lifecycle だけを確認する場合は、編集 run の共通仕様へ進む。
- 所見調査 call の正確な prompt、prompt part、workload 固有の起動パラメータを確認する場合は、委譲先の builder へ進む。
- oracle file と realization file の分類・列挙方法や、適合性の共通判断基準だけを確認する場合は、それぞれの正本仕様へ進む。
- サブコマンド共通のユーザー中断規則だけを確認する場合は、中断の共通仕様へ進む。

## hash
- f433e3411f3b2ea38db6893c05435fc315c9e73f4eca934a107ea7739b689317

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
