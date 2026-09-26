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
- realization apply/refactor と feedback report に共通する編集 run のライフサイクルを定め、個別 workload の fork 処理と共通の join・abandon 処理の接点を説明する。
- 同時実行の制約、共通の開始・commit 規則、feedback report の自動 join、競合解消、report と cleanup を扱う。

## Read this when
- 複数の編集 workload に共通する run の開始条件・進行中の制約や、join・abandon の事前条件と状態遷移を確認するとき。
- join 時の差分検査、merge と競合解消の責務、失敗時の rollback、post-join と cleanup の扱いを確認するとき。
- feedback report が自動 join する共通 lifecycle や、明示的な join・abandon との関係を確認するとき。

## Do not read this when
- realization apply/refactor の個別手順、編集対象、workload 固有 report や hook を調べるときは、それぞれの workload 仕様を読む。
- feedback report の intake、issue 単位の修正、publication や recovery の詳細を調べるときは、その workload 仕様を読む。
- run の隔離資源や session・run state の詳細定義が必要なときは、それぞれを正本として定める文書を直接読む。
- session lifecycle、oracle の編集、read-only investigation、または run を作らない機械的更新を扱うとき。

## hash
- 60e1ab8b01f14b5a8ecab4ddf427dc7288f0097ce272973d2c6837932710d702

# `feedback_report.md`

## Summary
- 収集済み observation の検証・整理から、issue の確認と安全な修正、run の join、結果の publication、中断・失敗時の回復までを定めるコマンド仕様です。

## Read this when
- `cmoc feedback report` の処理順序や、issue の判定・修正から join・report 公開に至る挙動を理解または変更するとき。
- このコマンドの再開条件、中断・エラー時の扱い、report の出し分けを確認するとき。

## Do not read this when
- observation の報告基準、MCP 受付、raw 保存だけを調べるときは、収集仕様を直接読んでください。
- feedback の永続 state や atomic publication の契約だけを調べるときは、state 仕様を直接読んでください。
- agent に渡す正確な prompt や Structured Output schema だけを調べるときは、それぞれの定義元を直接読んでください。

## hash
- 7ef0e73f3a4097c6b67a5f4116ecf0c0d71f96c693603dffa86f5d31f398f2a5

# `indexing.md`

## Summary
- `cmoc indexing` による文書索引の明示同期について、doctor preprocess から同期・資源解放までのコマンド固有の手順を定める。
- 同期の未開始・更新・無変更・失敗を含む実行要約の報告を定め、索引同期の共通契約へ案内する。

## Read this when
- 明示的な索引同期を実行するとき、またはその開始条件・処理順序・失敗時の扱いを確認するとき。
- 同期前に失敗した場合を含む実行要約の内容や、doctor の修復結果と同期結果の区別を確認するとき。
- 通常検索と明示同期のコマンド上の役割の違いを確認するとき。

## Do not read this when
- 検索対象の許可条件、閲覧範囲、同期整合性、cache、排他などの共通仕様を確認・変更するときは、文書検索の共通仕様を直接読む。
- doctor の検証・修復手順そのものを確認・変更するときは、doctor preprocess の仕様を直接読む。
- 検索 query の処理や検索結果の扱いを確認するときは、明示同期の手順ではなく文書検索の共通仕様を読む。

## hash
- a394183acb71eb8177bdabbbe60948126723ad9527921d4d28f7dc46bd0c91b3

# `oracle_edit.md`

## Summary
- `cmoc oracle edit` の workload 仕様。ユーザーの指示から oracle file の目標状態を定め、編集 agent call、差分の扱い、実行結果の報告までを説明する。
- oracle file を編集するこの workload の実行条件や境界を確認する入口。調査専用の処理や realization の編集 run とは責務が異なる。

## Read this when
- `cmoc oracle edit` の入力確定、実行前提、2 回の agent call、編集権限、終了状態の仕様を確認・変更するとき。
- 両回で共有する prompt と設定、未コミット差分の扱い、primary report や通知など、この workload 固有の動作を確認するとき。

## Do not read this when
- oracle file の調査や読み取り専用の回答が目的なら、調査 workload の仕様を読む。
- realization file の apply・refactor や run の join・abandon が目的なら、該当する workload と編集 run 共通仕様を読む。
- prompt の正確な文面や起動パラメータの構築方法、共通の editor input・Codex 実行・ログ・通知規則を確認するなら、それぞれを定義する builder または共通仕様を直接読む。

## hash
- 35f31833db093b935f3234c574cd179ae60a72fd025d97c07e52d42ab9b1c840

# `oracle_investigation.md`

## Summary
- oracle file の調査指示を受け、入力から Codex CLI の TUI 起動、回答までを扱う `cmoc oracle investigation` 固有の動作と調査境界を定める。
- 調査結果の根拠提示、TUI agent の読み書き範囲、共通仕様や起動パラメータ builder への責務委譲を確認する入口。

## Read this when
- oracle file の調査・回答を担当するコマンドの実行手順、根拠提示、TUI agent の調査範囲や書き込み可否を実装・確認するとき。
- このコマンドで editor input handoff を使う連携や、調査サブコマンド固有の起動条件を確認するとき。

## Do not read this when
- oracle file の編集作業や編集 lifecycle を調べる場合は、`cmoc oracle edit` の仕様から確認するとき。
- 共通のエディタ入力 lifecycle だけなら prompt editor input の仕様を、Codex TUI の共通起動規則だけなら `cmoc tui` の仕様を読むとき。
- 正確な調査 prompt、prompt part の選択、workload 固有の起動パラメータを調べる場合は、builder の定義を直接読むとき。

## hash
- ee3a09265429f10dd0e74b5a729a3b236b3fccacf2d187898d88d845b7f6270b

# `realization_apply.md`

## Summary
- 直近のコミットに含まれる oracle file の変更を realization file へ追従する apply fork workload の目的と範囲を定める。
- apply 固有の追従手順と join 後の比較範囲更新を扱い、短い変更追従の入口となる。ファイル単位の網羅的な調査は refactor workload が担う。

## Read this when
- 直近の oracle 変更を realization file へ反映する apply workload の対象や完了条件を確認するとき。
- apply とファイル単位で調査を繰り返す refactor のどちらを使うか判断するとき。

## Do not read this when
- fork、join、abandon に共通する編集 run の手順だけを確認するときは、編集 run の共通仕様へ進む。
- oracle file と realization file をファイル単位で網羅的に調査・修正する手順を確認するときは、realization refactor の仕様へ進む。

## hash
- b945d7be83974c39ec8ab7dcfcc9a6492a6728683b5347d786fa0f81b421c06c

# `realization_refactor.md`

## Summary
- oracle file と realization file を対象に、ファイル単位の調査・修正を繰り返す realization refactor fork の挙動を定める。調査状態の同期と対象選択、処理結果、完了・中断・エラー時の扱い、終了記録を確認する入口。
- 短い変更ループを担う realization apply や編集 run の共通 lifecycle とは責務が分かれており、refactor 固有の動作を扱う。

## Read this when
- realization refactor fork でどの file が調査対象になるか、調査要求や unresolved target が fork の進行にどう影響するかを確認・変更するとき。
- 調査結果と実差分の扱い、状態更新、正常完了・中断・エラー時の結果や report を確認・変更するとき。

## Do not read this when
- fork・join・abandon の共通 lifecycle だけを確認・変更するときは、編集 run の共通仕様を参照する。
- oracle file に対する realization file の適合性や所見判断の基準だけを確認するときは、その正本仕様を直接参照する。
- 調査 call の正確な prompt、prompt part、起動パラメータを確認・変更するときは、それらを構築する実装を直接参照する。
- oracle file と realization file の分類・列挙規則だけを確認するときは、file enumeration の仕様を直接参照する。

## hash
- a9398f5f1df5c675a4d58a974c3016bdc5ecfbb0b9d283b5f3b34189c40a3b41

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
- `cmoc tui` がユーザーのプロンプトを受け取り、doctor preprocess 後に cmoc 固有契約を付加して AI Agent CLI/TUI を起動する意味仕様を定める。
- 実行条件、バックエンド共通の起動契約、Codex CLI 固有の条件を示し、プロンプト入力のライフサイクルや起動パラメータの詳細を別の正本へ委ねる境界を示す。

## Read this when
- `cmoc tui` の実行順序や、未コミット差分があっても実行する条件を確認するとき。
- TUI に適用する cmoc 固有規定や installed skill との優先関係、共通の起動条件を確認するとき。
- Codex CLI を使う `cmoc tui` で有効にする handoff 機能や Codex 固有の起動条件を確認するとき。

## Do not read this when
- エディタ入力ファイルの作成・確定・保存や handoff の共通ライフサイクルを確認するときは、それらを定める仕様を読む。
- prompt の正確な文面・部品や起動パラメータの構成と選定理由を確認するときは、それらを構築する builder を読む。
- oracle file の調査や編集など、別サブコマンド固有の目的・権限・実行手順を確認するときは、そのサブコマンドの仕様を読む。
- feedback observation の収集・保持や Windows toast 通知の共通動作を確認するときは、それぞれの意味仕様を読む。

## hash
- 1aec0b9633a4498180fded849898e627fc5c99e73e263484a466365a3b3e10fe
