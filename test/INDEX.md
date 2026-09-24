# `_acp_builder_support.py`

## Summary
- テストから acp_builder の正本 schema を参照するための共有 helper。schema を複製せず、参照先の Path を返します。

## Read this when
- acp_builder の正本 schema を使うテストを追加・修正し、テスト側の参照先を確認するとき。

## Do not read this when
- 正本 schema の定義や仕様を確認・変更するときは、schema 自体を参照するとき。
- acp_builder の実装動作を調べるときや、schema を使わないテストを扱うとき。

## hash
- 6fd184bad0b16e6bce9c32dac57e2187a8272303ece3f3c8d350acaeacf5824b

# `_cli_support.py`

## Summary
- CLI テストで共有する呼び出しと出力解析の補助をまとめる。指定した worktree で doctor を実行して終了コードを確認し、CLI 出力から primary report のパスを取得する。
- CLI テストで使う共有の CliRunner も提供する。

## Read this when
- CLI テストで doctor を対象 worktree 上で実行したいとき。
- CLI の結果や出力から primary report のパスを取り出したいとき。
- 複数の CLI テストで共有している CliRunner を確認したいとき。

## Do not read this when
- コマンドの仕様や診断・レポート内容を調べるときは、該当する仕様またはコマンド実装へ直接進む。
- cwd の切り替えや排他制御の挙動が論点なら、ディレクトリ切り替えユーティリティへ直接進む。

## hash
- 77fc1a0c23afa228b0235135b24525d1823f6332923c8ea7c430c89dc6871020

# `_codex_support.py`

## Summary
- 複数のテストで共用する Codex CLI 用のテストダブル、隔離環境、呼び出しパラメーター、引数検査、実行時オーバーライドをまとめた支援モジュール。
- Codex 呼び出しを扱うテストで、共通ヘルパーの役割や変更箇所を確認する入口。

## Read this when
- 複数のテストに共通する Codex CLI 用のテスト環境や引数処理を変更・確認するとき。
- テストで Codex の実行結果を置き換える方法や、実行時設定を固定する方法を調べるとき。

## Do not read this when
- 本番の Codex CLI 呼び出しの挙動を調べるときは、実行処理の実装から確認する。
- 単一テストの期待値や個別の動作を調べるときは、そのテストの記述から確認する。

## hash
- 143fb59f7aea70bdf2acb90fdf4cd24e8d1b4f0481ef54983bbfe88dce60d482

# `_command_support.py`

## Summary
- テストから起動する偽の外部コマンド用に、Python スクリプトを書き込み、実行可能にする共通ヘルパー。
- 個々の偽コマンドの処理や製品動作は定義せず、複数のテストが使うスクリプト生成処理を担う。

## Read this when
- テストで起動する偽の外部コマンドについて、スクリプトの作成方法や実行権限の付与方法を確認・変更するとき。
- 複数のテストで共有する偽コマンド生成処理の利用例を確認するとき。

## Do not read this when
- 製品コードの外部コマンド実行や、その動作を検証する個別テストの内容を調べるときは、それぞれの実装やテストを直接読む。
- テストで実行可能な Python スクリプトを生成しない場合。

## hash
- 37672f2473fdf889a2210635d4294e5f807fefd04034b00449f411bffcf86ae8

# `_git_support.py`

## Summary
- CLI テストで共有する一時 Git リポジトリ用ヘルパーを提供し、Git コマンドの実行、現在ブランチの取得、初期 commit 済みリポジトリの作成、ignore 対象だが追跡済みの oracle file の fixture 作成を担う。

## Read this when
- テスト用リポジトリの共通初期状態や、Git コマンド実行・ブランチ取得のヘルパー動作を調査または変更するとき。
- ignore 対象だが追跡済みの oracle file を使うテスト fixture の作成方法を確認するとき。

## Do not read this when
- 特定サブコマンドの挙動や個別テストケースを調べるときは、該当する実装やテストへ直接進む。
- 本番コードの Git 操作や ignore 判定の仕様・実装を調べるときは、その正本仕様や本番コードへ直接進む。

## hash
- 1ecaade4dee17221fe4bca8c1837bef8e9d28957fd6bee025a6b52c299aea9e1

# `_handoff_support.py`

## Summary
- handoff 関連テストで共有する入力値と、正本 builder を使った期待本文を作るテスト補助。

## Read this when
- editor input handoff の MCP、ライフサイクル、TUI 連携テストで共通の入力や期待本文の生成元を確認するとき。

## Do not read this when
- handoff 本文の仕様やレンダリングを確認するときは、正本仕様または body builder を直接読む。
- MCP 応答や target の動作を調べるときは、実装または個別のテストを直接読む。

## hash
- 0bf82cfbb81f22d3a0345534414f77b906a61181b469c36b8a9e3d8b260afc31

# `_real_path_integration`

## Summary
- 実経路統合テストの子プロセスで、AI 呼び出しパラメータのモデル設定を最小モデル・低い推論強度に固定するテスト用フックを担う。

## Read this when
- 実経路統合テストの子プロセスで適用されるモデル設定や、そのテスト用上書きを調べる・変更する場合。

## Do not read this when
- ACP の一般的な型や本番時のパラメータ構造を調べる・変更する場合は、テスト用上書きではなく正本の ACP 型定義を直接確認する。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `conftest.py`

## Summary
- pytest 全体で使う Windows toast の外部副作用隔離と、editor input handoff 用 MCP context を準備する共有 fixture を定義する。
- テスト共通の隔離設定や handoff 用 context の準備を変更するときの入口。

## Read this when
- 複数のテストに適用される Windows toast の隔離方法を変更するとき。
- editor input handoff のテストで共有する送信元 context や環境変数の準備を変更するとき。

## Do not read this when
- Windows toast の個別動作や handoff protocol の詳細を調べるときは、対応する実装・仕様・個別テストから確認を始める場合。

## hash
- 89282cf36f1b504ac55859e2268d465bac3bfaa45fff87a0b807fa3532ca791f

# `test_acp_builder_editing_run_parameters.py`

## Summary
- editing run が使う apply fork・変更要約・ファイルレビュー／修正の各 builder について、互換入口と正本 builder の関係、および生成される起動パラメータと prompt の期待を検証するテスト。
- commit 範囲、作業用 worktree、アクセス設定、事前 indexing、schema 選択など、builder 呼び出し時の契約をテスト側から確認する入口。

## Read this when
- editing run から各 builder を呼ぶ経路の互換性や、prompt と起動パラメータの期待をテスト観点で確認・更新するとき。
- commit 範囲や対象ファイルが prompt に正しく反映されるか、または実行設定が期待どおりかを切り分けるとき。

## Do not read this when
- prompt 文面や起動パラメータの組み立て自体を調べる・変更する場合は、対応する正本 builder の実装から読む。
- Structured Output の出力契約の詳細を調べる・変更する場合は、対応する正本 schema を直接読む。

## hash
- 9811a6d8c31daae31e7187ca1374ce39dd66748b6e25b9e2f230cce0ab6a9d6e

# `test_acp_builder_indexing_parameters.py`

## Summary
- indexing 用 INDEX エントリー生成 agent call の固定設定と prompt の組み立てを検証する。
- schema の意味項目を空にできないことと、互換 import が正本の builder を再公開することも確認する。

## Read this when
- indexing 用 agent call の prompt 構成、ファイルアクセス設定、実行条件に関する回帰を調べるとき。
- schema の必須性や互換 import の公開面に関するテスト範囲を確認するとき。

## Do not read this when
- prompt の正確な文面や起動条件、schema の制約を決定・変更するときは、それらの定義へ直接進む。
- INDEX エントリーの生成・解析、鮮度判定、ディレクトリ走査や並列更新の挙動を調べるときは、共通の indexing 実装とそのテストを確認する。

## hash
- 7c7a612ceb0fea7d93b9194617a30b8e09dc6d821a83222afc7b9f97cacb9287

# `test_acp_builder_session_join_parameters.py`

## Summary
- session join の競合解消 call builderについて、互換 import の公開契約と、merge 中に使う起動パラメータの構成を検証する。
- commit 参照や Git の統合状況を prompt に渡し、共通の競合解消方針を組み込む契約を確認する。

## Read this when
- session join の競合解消 call の互換 export、権限・作業場所・preflight、commit 参照、prompt 構成を確認または変更するとき。
- この call 境界の契約テストや fixture を編集するとき。

## Do not read this when
- builder の実装詳細を追うときは、このテストが参照する正本の builder 定義を直接読む。
- 共通の競合解消 prompt の方針や要件を調べるときは、共通 prompt builder または対応する正本仕様を直接読む。

## hash
- 6dc9d53c6ec3cdb482f8a6a0020e53ee0cf047992dbff3416a154d9cd9269a4d

# `test_acp_builder_tui_parameters.py`

## Summary
- TUI 起動用 builder が固定する実行設定と prompt policy の構成を検証する。
- 互換 import 経路が canonical builder のみを公開することも確かめ、これらの回帰確認の入口となる。

## Read this when
- TUI 起動 parameter、prompt policy の組み込み、オリジナルプロンプトの受け渡しに関する回帰確認を調べるとき。
- TUI builder の互換 import 経路や公開 API を確認するとき。

## Do not read this when
- 起動 parameter の根拠となる要件を確認するときは、対応する oracle source を直接読む。
- TUI コマンドの入力・起動フローや実行時の挙動を調べるときは、それらを担当する CLI または runtime の実装・テストから読む。

## hash
- e60167087fe0542be76036687c3caf8679ddbe8bc90fbaefe0fb27ac2c1a6a97

# `test_basic_runtime.py`

## Summary
- repo-root / work-root と root placeholder の解決を、Git repository・worktreeの違いや並行処理を含めて検証するruntime回帰テスト。
- cmoc管理run worktreeのbranchとpathの対応、作成・検索・削除時のsymlinkや無効なGit登録の拒否、およびテスト用repositoryのGit設定分離も確認する。

## Read this when
- root placeholderやagent-call path contextが、main・linked worktreeやnested repositoryなどでどう解決されるかを調べるとき。
- 管理run worktreeのpath対応や、安全な作成・検索・削除の回帰を調べるとき。

## Do not read this when
- root placeholderの正本実装やbranch・run worktreeの命名とlifecycle規約を確認・変更するときは、それぞれの正本へ直接進む。
- 時刻・ログ形式やrun processの停止など、このテストが扱わないruntime責務を調べるときは、その責務の実装へ直接進む。

## hash
- 9942c6dcd1ebb9875a3cacf18573018053cbbc306956d52ee8c53ef0dcfbc1b8

# `test_cli_command_tree.py`

## Summary
- 公開 CLI の末端コマンド構成、help の描画、Typer と Click の互換性、および feedback report の引数・option の有無を検証するテストです。
- CLI の公開構成や help の形を確認するときに、実行時のコマンド動作を扱うテスト群と区別して参照します。

## Read this when
- 公開 CLI コマンドの追加・削除・階層変更が期待される末端コマンド集合に反映されているか確認するとき。
- Typer と Click の help 互換性や feedback report のコマンド固有引数・option を変更するとき。

## Do not read this when
- 個別コマンドの登録や CLI 構成の定義を調べるときは、CLI の構成を定義する実装を直接確認してください。
- コマンドの実行処理、引数解析エラー、実行時の副作用を調べるときは、それらを扱う実装や実行時テストから確認してください。

## hash
- 77aebc373c15cf6692bb9c39a413565fdefa923862c1df11f90e805a52bf85e8

# `test_cli_tui.py`

## Summary
- CLI 統合テストとして、`tui` の前処理から入力編集、完全プロンプトの組み立て、Codex TUI 起動までの連携と、メイン・リンク worktree 間の入力記録や `.cmoc` の ignore を検証する。
- `tui`・oracle investigation・oracle edit に共通する入力の確定保存失敗時に、原文を保持して agent 起動を防ぐ境界も扱う。

## Read this when
- `tui` の CLI 実行フローや、入力編集から TUI 起動までの統合、worktree をまたぐ記録・ignore の挙動を変更または調査するとき。
- 3 コマンドに共通する入力の保存失敗が、agent 起動前の処理に与える影響を確認するとき。

## Do not read this when
- 入力の予約・検証・保存やエディタ選択の内部動作だけを調べるときは、共通入力処理の単体テストから確認する。
- handoff target の通信・上書き lifecycle、プロンプト builder の内容や起動パラメータ、Codex CLI の実行引数・hook を調べるときは、それぞれの専用テストから確認する。
- oracle investigation または oracle edit 固有の CLI フローを調べるときは、それぞれのコマンド専用テストから確認する。

## hash
- 1ff4d587a17f56b59547b7499cb74d28c374c35ddb5360802200648987c7cfe4

# `test_codex_runtime_errors.py`

## Summary
- Codex exec の JSONL 異常入力の失敗扱いと、Codex CLI 不在時の例外・失敗ログを確かめるテスト。
- Codex 実行の異常系のうち、破損した JSONL と CLI 起動時の不在を扱う。

## Read this when
- Codex exec が不正な JSONL を受け取った場合の失敗分類や、CLI 不在時の起動失敗とログを確認するとき。

## Do not read this when
- 有効な JSONL に対する quota・一時障害の分類、再開や再試行を調べるときは、Codex の回復・再試行テストへ進む。
- TUI 経由の Codex 呼び出しで CLI 不在時の挙動を調べるときは、TUI の実行テストへ進む。
- Codex 実行の規範的な挙動を確認・変更するときは、テストではなく正本仕様を読む。

## hash
- 07979859bab4cda55abd4b43e4dc967a660621050bc3eadf13c4875315480b73

# `test_codex_runtime_exec.py`

## Summary
- Codex exec の呼び出しとテスト環境を通した結合テストをまとめる。
- Codex CLI への prompt の渡し方、実行時の override、出力の扱い、テスト用 home の分離を確認する。

## Read this when
- Codex exec の起動引数や prompt の受け渡し、provider 設定の反映、Codex home への設定ファイル生成を変更・調査するとき。
- schema-less 出力の不正 UTF-8 を含め、Codex exec の呼び出しから結果構築までの結合動作を確認するとき。

## Do not read this when
- sandbox や provider の argv 変換だけを調べるときは、専用の builder テストを読むとき。
- JSONL エラー、再試行、process 停止、cwd・schema 保存先、CODEX_HOME の preflight が対象なら、それぞれを扱う専用テストを読むとき。

## hash
- a72672ae97c44047a25bbd6c69f01de61b6b28ff35b4989a7c36bd442d245b28

# `test_codex_runtime_home.py`

## Summary
- Codex 実行時の home の選択・解決と、CLI 起動前の home 検証を確認するテストです。環境変数の扱い、欠落やディレクトリ以外の拒否、auth.json の有無や種別に依存しないことを扱います。

## Read this when
- CODEX_HOME または既定 home の選択・解決規則を変更するとき、その実行時検証や CLI 起動前の拒否を確認するとき。
- Codex home の事前検証が provider 固有の認証ファイル形式に依存しないことを確認するとき。

## Do not read this when
- Codex home の選択・解決・事前検証に関係しない、Codex 実行処理の別の挙動を調べるときは、その挙動を直接扱う実装やテストから確認してください。

## hash
- bc743e02399ef8134394a417b4a2e8450ecd8c77298ec2a840f1581e004d2ff7

# `test_codex_runtime_paths.py`

## Summary
- Codex exec が使う時刻付きログ一式のパス確保、agent-call cwd の実プロセスと `--cd` への反映、file-access mode の sandbox 引数への反映を検証する。
- リンク済み worktree での schema 保存先と、補助的な指示ファイルの実在 path から個別 permission を追加しない挙動も扱う。

## Read this when
- 同時起動時にログのパスが衝突しないか、関連ログと output が call ごとに分離されるかを調べるとき。
- agent-call cwd が `--cd` と子プロセス cwd に反映され、PURE_ORACLE_READ が read-only sandbox 引数になる経路を確認するとき。
- リンク済み worktree での schema 保存場所や、補助的な指示ファイルの path が sandbox permission に変換されないことを確認するとき。

## Do not read this when
- Codex home の解決や環境変数、provider/config override、通常の exec 起動設定だけが論点なら、呼び出し設定を直接扱うテストを読む。
- Structured Output の JSON/schema parse・validation・補正や出力エラーが論点なら、その処理を直接扱うテストを読む。
- quota/capacity recovery、session resume、subprocess の追跡・停止・中断が論点なら、回復または subprocess lifecycle を直接扱うテストを読む。

## hash
- 3fce01a93d9cc4f80fa645ab437655c26db9d0e70d501a2fbf1056fe47aa42ef

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex quota 切れ後の復帰経路を検証する。保存済みログからの session ID 復元、利用可能性 probe、session の再開または元 prompt の再実行を扱う。
- probe の構築と実行条件、失敗・中断時の伝播、ログ記録、および並行 call による probe の共有を検証する。

## Read this when
- Codex の quota 復帰 probe や、復帰後の session 再開・prompt 再実行を変更または調査するとき。
- probe の実行条件や記録、失敗処理、中断処理、並行待機中の probe 共有を確認するとき。

## Do not read this when
- quota 復帰ではなく、capacity や一時障害の再試行、Structured Output の補正・schema 検証だけを扱うときは、それらの個別テストから確認する。
- probe の prompt 内容だけを変更するときは、probe builder とその正本定義を直接確認する。このテストは主に builder と runtime の接続を検証する。

## hash
- b064e65d5a12c90799165a171fc4fd43a81bc0bb2ddda8ed065f0f4f057a659b

# `test_codex_runtime_recovery.py`

## Summary
- Codex CLI の JSONL 結果分類と、quota / transient 障害からの回復フローを検証するテスト群。
- 回復理由の切替、設定継承、元セッションの再開、Structured Output 修正中の回復、probe 失敗・中断・並行呼び出しの待機共有を扱う。

## Read this when
- Codex CLI の失敗分類と、probe 成功後に処理をどう再開するかを調べるとき。
- 回復中の設定・作業・セッション・修正枠の維持、probe 停止、中断、同条件呼び出しの共有を確認するとき。

## Do not read this when
- CLI の起動引数、provider・sandbox 設定、home や subprocess の起動・追跡だけを確認するときは、profile / subprocess の専用テストへ進む。
- quota probe の prompt や parameter の構築、個別の quota retry 統合を調べるときは、quota probe / retry の専用テストへ進む。

## hash
- 5c09a5f373424954eac3cb90c0d1d5eda654bfc9fdef346a4e20ece3e4a4f9b5

# `test_codex_runtime_retry.py`

## Summary
- Codex exec の Structured Output 補正と capacity エラー時の再試行を検証し、call の記録や作業差分の保持・復元も扱う。

## Read this when
- Structured Output の検証失敗時の補正、同一 session の継続、補正回数の上限や失敗記録を調べるとき。
- capacity エラーの再試行や、回復待ちを挟んだときの作業差分の扱いを調べるとき。

## Do not read this when
- quota 枯渇時の probe、待機、session 再開を調べるときは、その専用テストから読む。
- 回復理由の分類、複数 worker 間の回復共有、中断処理を調べるときは、回復制御のテストから読む。
- Codex の作業ディレクトリ、schema 保存先、sandbox 引数を調べるときは、呼び出し経路のテストから読む。

## hash
- ff9d9a04dcae7390fea5f8d9287ae6b816209609722b234027514527f545cfd8

# `test_codex_runtime_subprocess.py`

## Summary
- Codex subprocess の起動・追跡実行と、run 子プロセスの停止処理に関する回帰テスト。期限や割り込み、tracking の検証・更新、プロセス同一性の確認、process group の cleanup、起動 callback の境界を扱う。

## Read this when
- Codex subprocess の起動、キャンセルや timeout、child tracking、起動 callback、終了時の cleanup の挙動を調べたり変更したりするとき。
- run の子プロセス tracking や、leader 終了後を含む process group の安全な停止・同一性確認を調べたり変更したりするとき。

## Do not read this when
- Codex の argv や profile 設定、retry、quota、TUI など subprocess の起動・追跡・停止に関係しない runtime 挙動を扱うとき。
- apply/refactor の CLI ワークフロー、run state、commit、rollback など呼び出し元の統合動作を扱うときは、そのワークフローを直接検証するテストから確認するとき。

## hash
- 2893f867c3ff571d08c7983f73b53027556ed0283114e3b25184cb32a5efa447

# `test_codex_runtime_tui.py`

## Summary
- Codex TUI 呼び出しの動作を検証するテスト群。prompt と実行条件の引き渡し、通知 hook と補完時の分岐、設定検証の順序、linked worktree での editor input handoff を扱う。
- TUI 呼び出しに伴う成功・失敗ログ、timestamp 衝突、並行呼び出しの対応を確認する。TUI 固有の回帰調査では、共有処理のテストよりこの対象から始める。

## Read this when
- Codex TUI の prompt、CLI 引数、アクセス境界、通知 hook や補完時の挙動を変更・調査するとき。
- TUI 起動前の agent call/provider 検証や、linked worktree からの editor input handoff を調査するとき。
- TUI の call log、サブコマンドイベント、異常終了、並行呼び出しの回帰を調べるとき。

## Do not read this when
- TUI に限らない Codex subprocess の共通実行処理を調べるときは、共有ランタイムの実装・テストへ進む。
- editor input handoff 自体のプロトコルや overwrite の動作を調べるときは、そのプロトコルの実装・テストへ進む。
- Codex provider や agent call 設定の定義・読み込みを調べるときは、設定の実装・テストへ進む。

## hash
- 70ce6cd37f686120885539250196367c2908062c63aa3235331336062cde4a4e

# `test_doctor_cli.py`

## Summary
- doctor の修復 lifecycle を外部挙動から検証する統合テストです。CLI と直接呼び出しを通じて、修復順序、reporter の利用不能時の扱い、linked worktree 間の排他制御、修復 commit と既存 Git index の保持を確認します。

## Read this when
- doctor の前処理による Git 状態・config・refactor state の修復や同期、修復失敗時の復元を調べる、または変更するとき。
- staged・unmerged・intent-to-add など既存の Git index 状態や、linked worktree と共有する lock への doctor の影響を調べるとき。
- doctor 前処理中の reporter 利用不能・中断・予期しないエラーの扱いを確認するとき。

## Do not read this when
- サブコマンドの登録、引数解析、help 表示だけを調べるときは、CLI の command tree を扱うテストへ進んでください。
- config の単独の検証・保存形式や、refactor state の個別同期規則だけを調べるときは、それぞれの runtime テストへ進んでください。
- feedback reporter 自体の送信・保存動作だけを調べるときは、feedback のテストへ進んでください。

## hash
- b3994a1a204bf11f73ad6d9cd229074f8ba06a3b7b4f356336d6d74b7a2a89d8

# `test_editing_run_cli.py`

## Summary
- realization apply/refactor fork と共有 editing run の join/abandon を、session state・run worktree・report・indexing・process cleanup にまたがる CLI 統合テストで検証する。
- 共通の lifecycle fixture で、実行中の失敗や中断、変更の commit/rollback、join 時の統合・cleanup まで追うため、複数の run lifecycle 境界に及ぶ変更の確認先となる。

## Read this when
- apply/refactor fork の開始から joinable または error 状態への遷移まで、失敗時の rollback、割り込み後の回復、report の整合性を横断して確認するとき。
- run join/abandon における session state、変更の統合、indexing や doctor との連携、worktree・branch cleanup の CLI 上の結果を確認するとき。
- 単一 helper の動作ではなく、複数の run lifecycle 処理をまたぐ変更の統合動作を確認するとき。

## Do not read this when
- session/run の state schema、branch 解析、state 読み書きだけを確認するときは、その状態管理に絞った実装やテストから読む。
- 共通 CLI の error・log・preflight・completion 境界だけを確認するときは、その CLI runtime 境界のテストから読む。
- feedback の observation 受付、report、remediation 固有の動作を確認するときは、feedback workflow の実装やテストから読む。
- 特定の runtime helper や fork command の内部処理だけを確認するときは、対象実装とその範囲に絞ったテストから読む。

## hash
- 93b10a964fa895b9431249ac88203162c88301e322f50b18a67cc38c714c9928

# `test_editor_input_handoff.py`

## Summary
- エディターの待機中に MCP 経由で送られる入力の受け渡しを検証します。target の有効期間、リポジトリとの対応、接続認証、上書きの安全性と完了境界を確認する入口です。

## Read this when
- エディター待機中の入力受け渡しで、どの target が受理されるか、上書きがいつ確定するか、終了時や異常な接続で入力を保護できるかを確認するとき。

## Do not read this when
- MCP の JSON-RPC、公開ツール、入力検証やエラー応答の契約を確認するときは、MCP インターフェースを直接扱う項目へ進んでください。
- 入力ファイルの予約、エディター選択、終了後の読み取りや保存を確認するときは、エディター入力の外部挙動を扱う項目へ進んでください。

## hash
- 088bde51380894981f43f6047b770565f86fa008ea589eda7f25ed4cf3ea4fa9

# `test_editor_input_handoff_mcp.py`

## Summary
- Codex TUI から呼び出される editor input handoff の stdio MCP interface と、guide 取得・overwrite の応答契約を検証する。
- 入力と送信元の検証、正本の本文生成との連携、入力内容を漏らさない失敗応答、送信結果が不明な場合の扱いも確認する。

## Read this when
- MCP tool の公開、JSON-RPC request の検証、guide・overwrite の呼び出しや応答変換を変更・調査するとき。
- 入力内容の秘匿、受付結果と送信結果不明の区別、正本の本文生成へ渡す連携を確認するとき。

## Do not read this when
- 待機中 target の開始・終了、server 側の上書き受理、書き込み先の検証や安全性だけが対象なら、target の lifecycle と上書き境界を扱うテストを読む。
- 正本の入力制約や guide・本文の生成規則そのものを確認するなら、仕様・schema・生成実装を直接読む。

## hash
- 02264d471c42f20fd659f91f36dc50f6670a9778acd46d586d7b8dd61b1baf82

# `test_feedback.py`

## Summary
- feedback observation の受付・保存から候補化、remediation、公開、cleanup までを横断して検証する。reporter と collector の通信、machine detector、active state の確定と回復も扱う。
- 公開後に compact な active state だけが残ることや、失敗・中断時の rollback と recovery を確認する。

## Read this when
- agent-facing reporter や collector の受付、観測の保存・秘匿処理、machine detector の回帰を追うとき。
- feedback report の wave 処理から remediation・publication まで、または失敗・中断・state corruption 時の動作を横断して調べるとき。

## Do not read this when
- 判定用 worktree evidence の収集・除外だけを調べる場合は、判定根拠に特化したテストから始める。
- 主報告の表示・保存だけを調べる場合は、primary report に特化したテストから始める。
- remediation checkpoint の再確認や sealed result の recovery だけを調べる場合は、その状態遷移に特化したテストから始める。

## hash
- 4afca4ec220c0ab7f49b4416764709e6a41f77f9c82c08882e5e2b0d5ffef8f9

# `test_feedback_decision.py`

## Summary
- feedback 判定根拠に含める worktree 入力の収集とハッシュ化を検証する。入力の除外、安全なパス処理、Git mode の扱い、nested `.git` の判別に関する回帰テストが中心。

## Read this when
- 判定根拠の入力対象や除外対象を変えるとき、その変更が `worktree_inputs` の回帰条件に与える影響を確認する。
- 入力内容・実行 mode のハッシュ化、nested repository の metadata 判定、削除済みパスや worktree 外パスの扱いを調べる。

## Do not read this when
- feedback の報告・修復フローや生成物全般の振る舞いを調べるときは、統合テストを扱う `test_feedback.py` から確認する。
- checkpoint、再確認履歴、修復の収束判定を調べるときは、`test_feedback_reconfirmation.py` へ進む。

## hash
- d5bd58b9507279e39eada8a25463b14cfc95ca656eebd5c8d46bb2ce59c0eacf

# `test_feedback_reconfirmation.py`

## Summary
- Feedback remediation の既存判定が、依存内容・同期結果・追加証拠の変化を受けて再確認される条件と、修復サイクルの収束・停止を検証する。
- 再確認処理に関わる wave や checkpoint の整合性と復旧、seal 後の join/recovery、active issue への判定根拠の引き継ぎまでを扱う回帰テスト群。

## Read this when
- 依存ファイルや同期処理、追加証拠の変更が既存の修復結果を再確認させる挙動や、再確認ループの終了条件を変更するとき。
- wave・checkpoint の検証や参照復旧、seal 後に判定根拠が変化した場合の join/recovery、active issue への検証根拠の保存を変更するとき。

## Do not read this when
- collector の MCP protocol、raw observation の受け付け・保存、candidate の正規化や照合だけを変更し、remediation の再確認ライフサイクルに関係しないとき。
- feedback の通常実行・中断・publication の統合動作を変更し、再確認、checkpoint 復旧、seal 後の join/recovery 条件に関係しないとき。

## hash
- dcbcaf52641db642b7c4a03a73a63eeaf49515f0f0e5c829ffe2d38c7e4c26f5

# `test_file_inventory.py`

## Summary
- oracle/realization file の全ツリー列挙を full-glob 基準と照合し、除外境界、nested repository ごとの Git ignore 判定、Git metadata、symlink・特殊 file の扱い、候補数が増えた場合の Git 処理量を検証する統合テスト。
- 列挙結果を refactor state の entry 集合や SHA256・調査要否の同期につなぎ、単一路径の分類も確認する。ignore helper 単体や state の選択・永続化ではなく、列挙を軸にした連携と境界を調べる入口。

## Read this when
- ファイル列挙・分類、pruning、nested repository の ignore 規則、安全な path の扱いを変更するとき。
- 列挙結果が refactor state の entry 集合や既存 entry の調査履歴にどう反映されるかを確認するとき。

## Do not read this when
- ファイルの分類・pruning 条件そのものを決めるときは、正本の列挙仕様を読む。
- Git ignore の共通 helper や refactor state の保存形式・選択規則を変更するときは、それぞれの実装と専用テストを読む。
- realization refactor のコマンド lifecycle や agent 呼び出しを変更するときは、その処理を扱う仕様とテストを読む。

## hash
- da73a7c13009bf9a158acb7588923d43cea4dc320c8c451c03f5843438f61fec

# `test_indexing_cli.py`

## Summary
- `cmoc indexing` の CLI が、初期化や作業ツリーの選択から INDEX 更新、commit、実行報告まで進む外部挙動を検証する。
- Codex の生成結果の反映、fresh な INDEX の再利用、未コミット差分の扱い、INDEX だけを commit する条件も確認する。

## Read this when
- `cmoc indexing` の実行条件や、通常・linked worktree での対象選択を変更またはレビューするとき。
- INDEX 更新の成功・失敗報告や、INDEX 更新後の commit と他の staged・unstaged 差分の扱いを確認するとき。

## Do not read this when
- INDEX 対象の探索、entry の生成・描画、ハッシュによる再利用の内部を調べる場合は、共通 indexing 処理の直接テストを読む。
- Codex 呼び出しや TUI から起動する preflight の制御を調べる場合は、preflight 専用テストを読む。
- Codex 呼び出し parameter や schema の構築自体を調べる場合は、builder の indexing parameter テストを読む。

## hash
- 10dd535ac20670cbc1dd042d1e3d4b366d2574b606a774bfd45c058ee9272f7d

# `test_indexing_common.py`

## Summary
- INDEX 更新の共通 runtime に対する直接回帰テストで、entry の描画・読み取り、hash による再利用や再生成、Codex 呼び出しへの対象 path の受け渡しを扱う。
- 対象ディレクトリの列挙、深さ順の更新、失敗時の復元、安全なファイル処理、並列更新と lock の共有も一体として検証する。

## Read this when
- entry の描画や不正 entry の再生成、target hash の判定、Codex 呼び出し時に対象内容や既存 index 内容を渡さない runtime 境界を変更・調査するとき。
- index 対象の選定や順序、空ディレクトリ、更新失敗時の復元、symlink・特殊ファイルの処理、並列実行や lock を変更・調査するとき。

## Do not read this when
- `cmoc indexing` コマンドの事前条件、worktree 選択、報告、commit の外部挙動を調べるときは、CLI lifecycle のテストから確認する。
- Codex 呼び出し前に実行する preflight の起動条件、順序、対象 worktree、lock 待機を調べるときは、preflight のテストから確認する。
- entry 生成用の prompt、schema、parameter 構築や互換公開面を変更するときは、ACP builder のテストから確認する。

## hash
- d3cf3c7f0c1a35a4bce7ef500d7ef0d2c1cc15e11ff4c2a39ca25d78b3b0af3c

# `test_indexing_preflight.py`

## Summary
- Codex exec/TUI の直前に INDEX 更新 preflight を挟む統合動作を検証するテストです。
- 実行順、対象 worktree、repository lock、preflight の無効化、失敗後の再 indexing を抑止する挙動を扱います。INDEX 生成アルゴリズム自体ではなく、Codex 呼び出し境界の契約を確認する入口です。

## Read this when
- Codex exec/TUI と INDEX 更新の順序や、exec 経路での呼び出し前処理を調べるとき。
- preflight の対象 worktree、lock 待機、呼び出し単位の無効化、file access failure 後の挙動を変更・調査するとき。

## Do not read this when
- INDEX entry の parse・生成・hash 検証・directory traversal の挙動を調べるときは、indexing 本体の直接テストから確認してください。
- Codex 子プロセスの起動・停止や timeout、process tracking を調べるときは、subprocess 管理のテストから確認してください。

## hash
- 5878530ec013a4ea9588eb60f8583810a0c93a296a44a31e05ab1166106905c8

# `test_oracle_edit_cli.py`

## Summary
- `cmoc oracle edit` CLI の回帰テスト。エディター入力を一度確定し、同じ実行パラメーターと設定で編集を2回行う流れを、成功時と各段階の失敗時で検証する。
- 起動前提、既存の作業差分とセッション状態の保持、変更の残り方、端末通知・レポート、ユーザー指定ログ参照の維持も確認する。コマンド全体の制御を調べる入口。

## Read this when
- oracle edit のエディター入力から2回の実行までの流れや、初回後に入力・設定を再構築しない条件を調べるとき。
- 起動前提や準備段階の失敗、作業差分・セッション状態の保持、通知・レポートの期待を確認するとき。
- プロンプトがユーザー指定のログ参照を保つか確認するとき。

## Do not read this when
- oracle edit が満たすべき要求や制約の正本を確認するときは、対応する仕様文書を読む。
- 共有の CLI 実行機構や Git・Codex 用テスト補助の動作自体を調べるときは、それぞれの実装や補助のテストを読む。

## hash
- eaa41a87a8bd5054ee2ad125d27a678e189b66e671f29c10c101f099e8907ce5

# `test_oracle_investigation_cli.py`

## Summary
- `cmoc oracle investigation` の CLI 結合テスト。session のない main worktree からの起動、doctor・入力編集・TUI 起動の連携、および調査用 builder adapter の公開範囲を検証する。コマンドの意味上の仕様や正確な prompt 構築ではなく、CLI 起動時の回帰確認に進む入口。

## Read this when
- `oracle investigation` の CLI 起動経路を変更し、session なしでの起動や doctor・入力編集・indexing preflight・TUI の連携を確認するとき。
- 調査用 builder adapter の公開範囲を変更し、その回帰確認が必要なとき。

## Do not read this when
- 調査の意味上の責務、事前条件、権限を確認するときは、正本のサブコマンド仕様を読む。
- 正確な prompt 文面や workload 固有の起動パラメータを変更するときは、builder の定義を読む。
- 共通の editor input lifecycle や CLI コマンド登録を変更するときは、それぞれを定義・検証する対象へ進む。

## hash
- ec63d04edc9397e6172b4306dc9a7e18f0935249a144a79e953a67c8b76b661b

# `test_packaged_import.py`

## Summary
- ソースを隔離した packaged layout に複製して実行し、package discovery、import の成立、公開 namespace と canonical 再公開の境界を検証するテスト。配布配置や import/export の整合を調べる際の入口。

## Read this when
- setuptools の package discovery 設定や、隔離された配布配置での import 可否を変更・調査するとき。
- builder/editor の import、canonical basic 型の再公開、config の公開 namespace を packaged layout で確認するとき。これらをまとめて実行検証する対象であるため。

## Do not read this when
- packaged layout の import・公開境界が論点でなく、quota probe の機能、editor 入力の振る舞い、config 値の意味だけを調べるときは、対応する実装や機能別テストへ直接進む。

## hash
- 1b5023e29e0828faf31783bfe1d3048396aaef177bab55bbb4349648cfdfb7cd

# `test_primary_report.py`

## Summary
- 非対話末端サブコマンドの primary report 完了処理を検証するテスト群。早期エラー、中断、fallback 生成、実行記録の反映、保存失敗時の扱いを対象とする。

## Read this when
- 共通の primary report 保存や terminal result 確定処理を変更し、終了経路ごとの report 保存と表示を確認するとき。
- Codex 出力や受理済み observation の実行記録への反映、report の更新・保存確認時の失敗処理を変更するとき。

## Do not read this when
- 特定サブコマンド固有の処理手順や report 項目だけを調べるときは、そのサブコマンドの実装・仕様・専用テストへ進む。
- primary report に関係しない共通ログや terminal result の挙動を調べるときは、該当する実装・仕様・テストを直接読む。

## hash
- a672eb69f2cda5f790a344f3cc71d1b9bfa9867daa1b7f42e6e4c5a473f0432e

# `test_production_cli.py`

## Summary
- 全末端サブコマンドの代表的な正常系を、利用者向け CLI の本番経路で確かめる受け入れテスト。
- 独立プロセスで実 Codex と実推論を使い、CLI 結果、call log、report、session/run state、Git 状態など外部から見える結果を検証する。TUI では PTY、editor handoff、通知も扱い、LLM の回答品質は評価しない。
- 実推論を含む本番経路全体の挙動を調べる入口。個々のコマンド内部や実行時機能を対象にする focused test とは責務が異なる。

## Read this when
- 全末端コマンドを独立プロセスで実行し、実 Codex を通した代表的な本番経路や、その外部可視な状態変化を確認・変更するとき。
- TUI の PTY 上の応答完了・終了、通知、editor handoff が実 Codex の実行と連携するかを調べるとき。

## Do not read this when
- 個々のコマンドや runtime の内部ロジック、決定論的な状態遷移を調べるときは、その機能を直接扱う focused test から始める。
- PTY helper 単体のタイミング挙動だけを調べるときは、その helper を直接検証するテストを読む。
- LLM の回答品質や agent の判断の正しさを評価するとき。このテストはそれらを判定対象としていない。

## hash
- 9b68e218cbbd2ee0d24575fc50fd428b1d6e5cdb065bf32cc18daed34fbd5ff5

# `test_production_cli_support.py`

## Summary
- 実経路統合テストで使う PTY 操作 helper のうち、信頼確認 prompt の描画後に Enter を送るタイミングを検証する。

## Read this when
- 信頼確認 prompt の描画中に入力が破棄されないことや、次の poll で Enter を一度だけ送る挙動を確認・変更するとき。

## Do not read this when
- 本番 CLI の起動から終了までの統合フローを調べるときは、そのフローを検証するテストへ進む。

## hash
- 67687d4517bc714cca1ab03754abb96c90a374dbc48b788c0eed9ca2e6d1e5d1

# `test_prompt_editor_input.py`

## Summary
- プロンプト編集入力の予約・エディタ起動・確定保存について、呼び出し側から見た挙動と入力保全を検証する。
- 編集入力の一連の処理を変更・調査する際、外部挙動の回帰境界を確認する入口となる。

## Read this when
- 編集入力を予約し、エディタで変更して確定する流れや、入力ファイルの検証・保存・失敗時の保持を変更または調査するとき。
- 編集処理から handoff target を開始・終了する連携や、その終了処理を確認するとき。

## Do not read this when
- handoff target のプロトコル、上書き規則、ガイド提供、MCP interface のみが対象なら、handoff 専用のテストを直接読む。
- 本番コードの内部構造を把握することが目的なら実装側から読み始め、外部挙動の確認が必要な場合にこのテストへ進む。

## hash
- 53dad9b8decf47c7c9ac6e7e002ac9caac68d5fba6fe9e3797bdb30cb582c379

# `test_prompt_parts.py`

## Summary
- 各 prompt policy builder の出力と、完全 prompt の組み立て結果を回帰確認するテスト群です。カテゴリ順や主要文言、policy の注入、objective と追加 prompt の並び、file access mode、root placeholder の統合と競合時の失敗を検証します。

## Read this when
- 完全 prompt の構成、任意 section や policy flag の反映、placeholder 処理を変更・調査するとき。
- policy の描画内容やカテゴリ順、file access mode ごとの出力に対する回帰確認が必要なとき。

## Do not read this when
- 個別 policy の規範や実装の詳細を確認するときは、該当する正本仕様または policy builder を直接参照してください。
- editor input の保存・確定や handoff 通信の実動作だけを調べるときは、それらの外部動作を扱う専用テストを参照してください。

## hash
- 347074435cc4236f0e03aaf9098fa4c867f1c150e1588d26d2dacefb3d9acf45

# `test_runtime_cli.py`

## Summary
- 共有 CLI runner の終了処理を検証し、成功・失敗・ユーザー中断時の表示、終了コード、診断ログ、通知の関係を扱う。
- 引数解析、補完 probe、doctor と pre-log の前処理、work root の扱いに加え、共通ログと時間表示も検証する。

## Read this when
- 共通 runner の結果分類やエラー表示、診断ログ、終了通知のタイミングを変更するとき。
- doctor や pre-log の前処理、work root と linked worktree の選択、補完 probe の副作用境界を見直すとき。
- 共通サブコマンドログの記録方法、timestamp、duration 表示を変更するとき。

## Do not read this when
- 特定サブコマンド固有の引数、処理結果、レポートを調べるときは、そのコマンドのテストから読む。
- Windows toast の payload・transport や Codex TUI の prompt・subprocess の詳細を調べるときは、それぞれの専用テストから読む。

## hash
- f07e289f6592e907070c242eb85d114d70a1e548926337745a91ac7e905f6eb7

# `test_runtime_codex_conflicts.py`

## Summary
- session join の競合解消用 agent call で、commit 参照値を prompt に渡し、値を反転しても起動 argv が同一であること、`REPO_WRITE` が `--sandbox workspace-write` になること、commit 値や詳細な権限設定が argv の設定上書きに現れないことを検証する回帰テストです。
- 個別 builder の生成契約や Codex runtime 全般の規則ではなく、session join 固有の入力から Codex 起動引数への受け渡しを確認する入口です。

## Read this when
- session join の競合解消で、commit 参照を prompt に保ち、commit 値を Codex 起動引数へ混入させない条件を確認・変更するとき。
- session join 用の `REPO_WRITE` 設定が Codex sandbox 引数へ反映され、詳細な権限設定の上書きを追加しない条件を確認するとき。

## Do not read this when
- builder 自体の公開経路、prompt、cwd、schema、preflight の契約を確認する場合は、個別 builder の契約テストから確認してください。
- 全 file access mode の sandbox 対応や、Codex argv の汎用上書き規則を確認する場合は、runtime profile 全般のテストから確認してください。

## hash
- 7566dc363da52fc232d712c2475b89454e6e229823475d8c030c5d99ea315806

# `test_runtime_codex_permissions.py`

## Summary
- Codex argv builder API がパス別の権限例外を受け取れないことを回帰検証する。sandbox の mode 変換や argv 全般ではなく、`build` と `prepare` の両方で旧来のパス指定引数が拒否される契約に絞ったテスト。

## Read this when
- Codex argv builder の引数を変更するとき、またはパス単位の read/write 例外を再導入しないことを確認するとき。

## Do not read this when
- FileAccessMode と sandbox の対応、model/provider の設定、通知など argv の構成全般を調べるときは、それらの契約を検証するテストか実装を直接読む。

## hash
- 647b0984d15205ef401da1ccdb65378808a7ad39e4b303a152cbf4809a4a278b

# `test_runtime_codex_profile.py`

## Summary
- Codex CLI 呼び出し設定について、sandbox、model/provider、MCP と環境変数、TUI 通知 callback の構成が期待どおりになる契約を検証するテスト。
- schema の保存時に元の bytes を保つことと、不正な encoding や過剰にネストした JSON output を失敗として扱う境界も確認する。

## Read this when
- Codex CLI の argv 構築、provider 設定、file access mode に応じた sandbox、または MCP 設定と環境変数の分離を変更・確認するとき。
- TUI 通知 callback の設定や、対応する Codex CLI の版を限定する挙動を変更・確認するとき。
- schema 保存や JSON output 読み取りの境界を変更・確認するとき。

## Do not read this when
- Codex 実行設定の正本ルールを確認するとき。oracle の仕様文書を直接読む。
- process tracking・終了処理、CODEX_HOME の preflight、または Codex 実行全体の回復挙動を確認するとき。このテストはそれらの動作を網羅しない。

## hash
- dc52f560b4025b34db754b946cac5acbe1df364a045d3e95daa3276db01972a3

# `test_runtime_config.py`

## Summary
- CmocConfig の既定値、agent call・model provider 設定、JSON 変換と永続化の契約を検証する。設定値や読み書きの挙動を変更するときの入口。
- 不正な設定値や JSON、危険なパスの拒否と、利用者向けエラーへの変換を検証する。

## Read this when
- agent call や model provider の設定項目、既定値、受理条件、JSON 化や round-trip の挙動を変更するとき。
- 設定ファイルの読み書き、壊れた入力や不正なパスの扱い、関連するエラー報告を変更するとき。

## Do not read this when
- 設定を読み込んだ後の Codex 実行、再試行、profile 変換などの挙動が対象なら、それらを直接検証するテストから確認するとき。
- doctor コマンド自体の処理や表示が対象なら、コマンドの挙動を直接検証するテストから確認するとき。

## hash
- e7e0c40130910aecef985e114ebdf7550cad086ee933e2c562cbdb089cb15798

# `test_runtime_content.py`

## Summary
- runtime content helper の binary 判定と、内容ハッシュ名で保存する際の安全性を検証するテストです。NUL byte の判定と、保存先が symlink の場合にリンク先を変更せず保存する動作を扱います。

## Read this when
- NUL byte を含む内容の binary 判定を確認・変更するとき。
- 内容ハッシュで保存する処理について、保存先が symlink の場合にリンク先を保護する動作を確認・変更するとき。

## Do not read this when
- runtime content helper の実装や処理の詳細を調べる・変更するときは、実装を直接確認してください。
- 索引付けや Codex 実行規則の仕様全体を調べるときは、正本仕様を確認してください。このテストは helper の限定的な動作だけを扱います。

## hash
- 1d7cd925d0b731ec53366c6eb796bed8c9be466df205b88ae5f6b9f8f07ad5c3

# `test_runtime_file_access.py`

## Summary
- FileAccessMode の永続化値と、各モードを Codex sandbox mode に変換する対応関係を検証する。これらの契約を変更・確認するときの回帰テストの入口。

## Read this when
- FileAccessMode の JSON 向け値や、ファイルアクセスモードから sandbox mode への変換を変更・確認するとき。

## Do not read this when
- アクセス制御の意図や適用条件を調べるときは、正本の仕様・ポリシーを参照する。変換処理の実装を変更するときは、実装を直接確認する。

## hash
- cbbb2e829ce17df28aa8f61a44c8978c34f2f90b4d0c24406732cbd6c2843f63

# `test_runtime_git_ignore.py`

## Summary
- Git ignore 判定と cmoc 用 ignore 設定のランタイム挙動を検証するテスト。追跡状態やパス名の解釈、既存設定の保持、安全でない ignore ファイルの拒否、判定失敗時のエラーを扱う。

## Read this when
- Git ignore 判定の変更や、追跡済み・未追跡のファイルの扱いを確認するとき。
- cmoc 用 ignore 設定を追加・更新するとき、既存ルールの保持や ignore ファイルの安全性を確認するとき。
- ignore 判定の失敗や、無視された symlink の扱いを調査するとき。

## Do not read this when
- ファイル分類全体の正本ルールを確認するときは、該当する仕様文書を直接読む。
- Git ignore 以外のランタイム機能を変更・調査するときは、その機能を担当するテストから確認する。

## hash
- cd4002d7f6293b03a9d07d5d099490cc545f8643d83156258709df390981e93f

# `test_runtime_refactor.py`

## Summary
- realization refactor の調査 state と対象選択に関する runtime 回帰テストの入口。
- 対象集合の同期、履歴保持と変更時の再調査、state の検証・保存、選択優先度に加え、oracle/realization 分類が調査対象へ反映される境界を確認する。

## Read this when
- realization refactor の state 同期、履歴保持、変更時の再調査、state の拒否条件、候補選択の優先順を変更または調査するとき。
- 対象ファイルの分類や branch 上の file 判定が refactor state に与える影響を、nested repository や symlink・非通常 file の境界に沿って調べるとき。

## Do not read this when
- コマンド全体の処理手順、完了・中断、所見判定など workload の正本仕様を確認するときは、realization refactor の仕様本文を直接読む。
- 列挙や Git ignore の契約・性能要件そのもの、または refactor と無関係な Git/worktree 動作を調べるときは、列挙仕様か該当する Git runtime の実装・テストへ進む。

## hash
- 0785f76765f3a591a9ac1a41891bbf1ffa0371bd036cb7251804aea58e820d63

# `test_runtime_state.py`

## Summary
- session/run の永続状態を扱う runtime のテスト。state schema と managed branch 解析、state file の読み書きに関する境界条件、session fork lock の process 間排他を確認する。

## Read this when
- session/run state の schema 検証や branch からの state 解決、state file の入出力エラー処理を確認・変更するとき。
- session fork lock が process 間で排他されることを確認するとき。

## Do not read this when
- session/run の field や状態遷移の正本仕様を定めるときは、仕様文書を直接読む。
- 個別コマンドの fork・join・abandon の workflow や CLI 振る舞いを調べるときは、そのコマンドのテストを直接読む。

## hash
- 32811ae0b83c739ed0c9b39d68097f7c1070c6b84ba11da5216b054ca0ba8c48

# `test_runtime_wrapper.py`

## Summary
- 起動 wrapper の回帰テストとして、仮想環境 Python の検査、失敗時のエラー報告、利用可能な場合の CLI 本体への引数転送を確認する。
- 補完プローブ時の出力抑制も扱い、起動 wrapper の挙動を調べる入口となる。

## Read this when
- 仮想環境 Python の検出や起動確認、失敗報告を変更・調査するとき。
- 補完プローブ時の経路や、wrapper から CLI 本体への引数・環境変数の転送を変更・調査するとき。

## Do not read this when
- 仮想環境の作成・インストール手順を調べるときは、開発環境の仕様を確認する。
- CLI 本体のコマンドや内部動作を調べるときは、該当機能の実装・テストを確認する。

## hash
- 707b3f26990edb78254d6b4a9b15a2b50f704cf7f8afd6c89b609f3ce72be6d5

# `test_session_cli.py`

## Summary
- session fork・join・abandon の CLI 外部挙動を検証し、branch と state の遷移、linked worktree、失敗時の後始末、join の競合解決を扱う。

## Read this when
- session の fork・join・abandon が branch や state をどう変更するか、またはその失敗時の挙動を確認・変更するとき。
- linked worktree での session 操作や、join 時の競合・後始末を含む CLI 回帰範囲を確認するとき。

## Do not read this when
- 共有の競合解決処理や個別の補助機能だけを調べるときは、それぞれの実装と専用テストへ進む場合。
- session 以外の CLI コマンドや run のライフサイクルを調べるとき。

## hash
- d0291e38c7e44507926ae3a54e4b2ae8f73d09ace19b20b0ccd28d3a5dc42f37

# `test_skill_metadata.py`

## Summary
- リポジトリ内ローカルスキル定義の YAML frontmatter に関する共通条件を検査し、新しいスキルも対象に含めるテスト。

## Read this when
- ローカルスキルの追加・移動や frontmatter の登録情報を変更し、この検査への影響を確認するとき。
- この検査の対象範囲や検出条件を変更するとき。

## Do not read this when
- 個別スキルの用途や指示内容を確認・編集するときは、該当するスキル文書を直接読む。
- frontmatter の登録情報に関係しないテストや実装を扱うとき。

## hash
- bf735875997b038795c375af2a689094f308e7a286145efe3996c3ce9cd796d8

# `test_struct_doc_rendering.py`

## Summary
- 構造化文書ノードの Markdown 描画と `basic.struct_doc` 互換 API の挙動を検証するテスト。空行の縮約、コードフェンス、参照ブロック、規定カテゴリ、互換 re-export、子要素の型エラーを扱う。

## Read this when
- Markdown 描画の整形や参照ブロック、SDPolicy の表示を変更・調査するとき。
- `basic.struct_doc` から公開する型や renderer の互換性を変更・調査するとき。
- SDHeader または SDTagBlock の不正な単一子要素に対する型エラーを変更・調査するとき。

## Do not read this when
- 正本 renderer の実装詳細や構造化文書ノードの仕様を確認するときは、正本の `oracle/src/oracle/other/struct_doc.py` を直接読む。
- このテストが扱う Markdown 描画・互換 API と関係しない、構造化文書の利用側だけの挙動を調べるとき。

## hash
- 59777795fc220c56f39c46ca4ee6aa2b3d9cb6b4f47edec071c540bc15734205

# `test_windows_toast.py`

## Summary
- Windows toast の表示内容と安全な PowerShell transport、通知失敗の非伝播、自動補完中の無効化を検証するテストです。
- Codex TUI callback の root session 判定、turn ごとの重複抑止、入力内容の秘匿、呼び出し単位の state 管理と cleanup も扱います。

## Read this when
- toast の内容・transport・失敗時の挙動や、自動補完中の通知境界を変更または調査するとき。
- TUI の通知 callback が root session の turn 完了を一度だけ扱う条件や、一時 state の並行実行・cleanup を調査するとき。

## Do not read this when
- CLI が terminal result 確定時に通知を呼ぶ条件や回数を調べるときは、CLI runtime の統合テストを確認してください。
- Codex TUI 起動時に通知設定や session-start hook を渡す構成を調べるときは、Codex TUI runtime の統合テストを確認してください。

## hash
- 89f0cf57ba1d258d5355d60731bd03d20be0b8aaf008deeb38e0494173394cfb
