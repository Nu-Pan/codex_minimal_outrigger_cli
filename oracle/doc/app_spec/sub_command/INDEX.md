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
- realization apply・refactor と feedback report に共通する編集 run の開始条件、状態遷移、同時実行の境界を定める。
- `cmoc run join` と `cmoc run abandon` の共通条件、差分検査、merge 後処理、回復、cleanup、report の入口となる。

## Read this when
- 編集 run の共通事前条件、開始準備、または active run の制約を確認するとき。
- join・abandon の共通動作、想定外差分の扱い、cleanup 条件、report の要件を確認するとき。
- feedback report の自動 join など、個別 workload にまたがる共通 lifecycle の扱いを確認するとき。

## Do not read this when
- apply・refactor・feedback report 固有の処理、許可差分、hook、publication、recovery の詳細を知りたい場合は、その workload の仕様へ進む。
- session lifecycle、run の隔離資源、永続 state の定義、競合解消の判断基準や agent prompt の詳細だけを確認したい場合は、それぞれを定義する仕様へ進む。
- oracle edit や read-only investigation の手順を確認したい場合は、それぞれの仕様へ進む。

## hash
- 0d7455112605d5b68550bed8daface9bacf931f6288aaee020e7a9cc4ce43570

# `feedback_report.md`

## Summary
- feedback report の実行全体を定め、observation の取り込みと issue の正規化、issue 単位の修正・確定、自動 join、publication、各種 report、再開・中断・失敗時の扱いを説明する。正常 publication では、join 後も人手対応が必要な issue を掲載する。

## Read this when
- feedback report の開始条件、新規 run の作成、既存 run の recovery を確認するとき。
- 取り込んだ observation の正規化、remediation call、差分の受理、issue 単位の commit・rollback、wave の停止条件を調べるとき。
- 自動 join と join 後の検証、正常または incomplete の publication、report の内容、終了結果、中断・エラー後の扱いを確認するとき。

## Do not read this when
- observation の報告条件、受け入れ、保存や検出規則を調べるときは、observation 収集の仕様を読む。
- feedback 全体の用語、結果分類、処理モデルを確認するときは、共通 feedback 仕様を読む。
- repository-local state の形式、耐久性、checkpoint、report cut、cleanup の詳細を調べるときは、feedback state の仕様を読む。
- run の共通 lifecycle、隔離境界、join・abandon の一般規則を確認するときは、編集 run の共通仕様を読む。
- agent に渡す正確な prompt や Structured Output schema を確認するときは、それぞれを定める実装側の定義を読む。

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
- Git commit 範囲から特定した oracle file の変更を realization file へ反映する `realization apply` の workload 固有仕様です。
- 追従対象の決め方、本命 agent call の制約、成果物の確定と report、join 後の更新条件を定めます。

## Read this when
- 直近の commit 範囲にある oracle file の変更と realization file の追従要否を確認するとき。
- 変更 path の追加・削除や oracle 内外をまたぐ rename を含め、apply の追従範囲を判断するとき。
- apply の agent call、完了条件、report、または join 後 hook の挙動を確認するとき。

## Do not read this when
- fork・join・abandon の共通 lifecycle を確認するときは `editing_run.md` を読む。
- ファイル単位で unresolved target の調査を続ける refactor の手順を確認するときは `realization_refactor.md` を読む。
- oracle と realization の適合性判断基準そのものを確認するときは `oracle_and_realization.md` を読む。
- apply の正確な prompt 文面や起動パラメータを確認するときは、委譲先の builder 定義を読む。

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
- `cmoc session join` の仕様。現在の session branch を home branch に merge して session を完了する際の処理を定める。
- session 固有の merge、競合解消、状態遷移、報告を確認する入口。

## Read this when
- `cmoc session join` の実装や挙動を確認するとき。
- join 時の競合解消、予期しない失敗、session 完了後の状態や報告の扱いを確認するとき。

## Do not read this when
- session の作成や破棄だけを確認する場合は、それぞれ fork または abandon の仕様へ進む。
- branch の一般的な役割や merge の基準だけを確認する場合は、branch model を読む。
- session 共通の事前条件、競合解消の共通方針、一般的なエラー分類だけを確認する場合は、それぞれの共通仕様へ進む。

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
