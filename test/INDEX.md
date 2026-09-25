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
- Codex の runtime・CLI テスト間で共用する test double、隔離環境の準備、parameter 作成、引数検査、Codex override の差し替えをまとめた補助コード。個別のテストケースではなく、複数のテストが共有する準備や検証方法を確認するときの入口。

## Read this when
- Codex 関連テストの共通環境、偽の構造化出力、引数・config の検査、override のスタブを変更または利用するとき。
- この共有補助を使う複数のテストで、セットアップや Codex 呼び出しの検証方法を追うとき。

## Do not read this when
- Codex の実際の runtime 挙動や agent call parameter の仕様を調べるときは、該当する実装または正本仕様から確認する。
- 特定のテストケースだけの期待値や振る舞いを調べるときは、そのテストを直接読む。

## hash
- a14ef0fb9af4979abd7ca7fa0abd9a033435ab3f292268df5b4192dfc4565571

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
- TUI コマンドで、エディター入力の編集後にプロンプトを組み立てて Codex TUI を起動するまでの外部挙動を検証する。
- linked worktree でのルート選択やログ保存に加え、入力の確定保存に失敗した際に agent 呼び出しを防ぐ共通の挙動も扱う。

## Read this when
- TUI コマンドのエディター起動後から Codex TUI 呼び出しまでの流れや、doctor 前処理・indexing preflight の順序を変更するとき。
- linked worktree 起動時の TUI 作業ルート、入力記録、`.cmoc` の ignore 挙動を確認するとき。
- TUI・oracle investigation・oracle edit で、入力の確定保存失敗時に本文を保持して agent 呼び出しを止める挙動を変更するとき。

## Do not read this when
- 共通のエディター入力保存や受け渡しそのものを調べるときは、その仕組みを直接検証するテストから確認する。
- Codex TUI の subprocess 実行や低水準の起動パラメーターだけを調べるときは、runtime またはパラメーター生成を直接検証するテストから確認する。
- oracle edit または oracle investigation の個別 CLI 挙動だけを調べるときは、それぞれの専用 CLI テストから確認する。

## hash
- 260d155884d2157c62fb5fe1a99d9c50f7caae3e6767555ff2d8b2b6ebbfc5d9

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
- Codex exec の通常起動について、CLI 引数と設定上書き、作業ディレクトリ、prompt の stdin 渡し、結果の読込をテストする。
- 実行環境の分離、汎用 model provider の設定反映、CODEX_HOME に設定ファイルを作らないこと、schema なしの出力に不正 UTF-8 が含まれる場合の扱いも確認する。通常 exec の呼び出し契約を調べる入口となる。

## Read this when
- Codex exec に渡す引数や設定上書き、作業ディレクトリ、prompt の stdin 渡しを確認・変更するとき。
- model provider の設定反映や、Codex の設定ファイルを生成しない実行環境の扱いを調べるとき。
- Structured Output schema を使わない場合の出力読込、特に不正 UTF-8 の扱いを確認するとき。

## Do not read this when
- Structured Output の検証・補正、postcondition、容量回復や再開を調べるときは、出力補正や回復処理を扱うテストから確認する。
- Codex 子プロセスの追跡、停止、PID の同一性確認などを調べるときは、プロセス管理を扱うテストから確認する。

## hash
- ebc007d7ca7eab3f2ec012970839a4777a728997189f7af2426147b3219e6db8

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
- Codex exec の実行時パスと sandbox 引数を、並行呼び出しや linked worktree を含む起動経路で確認する。

## Read this when
- Codex のログ path の一意性、呼び出し cwd、linked worktree での schema 保存先を変更・調査するとき。
- FileAccessMode に応じた sandbox argv と、実在する `.agents` path を個別権限へ注入しない境界を調べるとき。

## Do not read this when
- model/provider 設定、prompt の受け渡し、Structured Output の検証・補正、retry や recovery の一般動作を調べるときは、それぞれの専用実行・回復テストを読む。
- file access policy の文面や mode ごとの制限を変更するときは policy 定義と専用テストを、path context の導出規則を変更するときは path model の正本を直接読む。

## hash
- eacd012f2ffec59214a0f1d5f8fb786d292fd49987ca3ba8a64dbe9a2ea663fa

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex exec の quota 枯渇後、代表 probe による回復確認から session の再開または prompt の再実行までを検証する実行時テストです。
- probe の共有、記録とログ、失敗・中断時の伝播、quota probe adapter の連携も扱います。

## Read this when
- Codex exec の quota 待機・回復判定・再開または再実行の動作を変更するとき。
- quota probe の実行、並行呼び出しでの共有、ログや失敗処理との連携を変更するとき。

## Do not read this when
- quota と無関係な Codex exec の引数構築、権限、パス解決などを変更するときは、その責務を直接扱う対象から確認してください。
- quota probe の正本プロンプト自体を変更するときは、プロンプトを定義する oracle の対象から確認してください。

## hash
- 64aab45c5218ca3db49dbe2a8eb30841cf2e9a9d830e47651cee99f8baa742aa

# `test_codex_runtime_recovery.py`

## Summary
- Codex exec の JSONL 終了結果の分類と、回復待ち・確認 probe 後の同一 session 再開を検証するテスト。
- 回復理由の切替、設定継承、Structured Output 補正中の回復、中断処理、条件が一致する並列 call の probe 共有も扱う。

## Read this when
- quota や capacity を含む JSONL 結果の分類、回復待ち・probe・session 再開の動作を変更または調査するとき。
- 設定継承、補正中の回復、中断の優先、並列 call 間の probe 共有を確認するとき。

## Do not read this when
- 回復後の呼び出しを対象とせず、Codex exec の通常起動時の引数や provider 設定だけを調べるときは、通常起動のテストを直接読む。
- 対話型 Codex TUI の起動・終了や通知フックを調べるときは、TUI 専用のテストを読む。

## hash
- aa87e4c68fe649e580f908cfeec3cb73d9adfb49051926facf48cd412a31d6f7

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
- Codex TUI の起動経路について、prompt と CLI 設定、通知フック、worktree のアクセス境界を検証する回帰テスト。
- TUI 呼び出しの成功・失敗ログと、並行する editor-input MCP handoff の送信元対応を検証する。

## Read this when
- Codex TUI の起動設定、バージョンに応じた通知フック、設定検証やシェル補完中の挙動を変更・調査するとき。
- TUI のログ記録、worktree での prompt・handoff、並行呼び出し時の送信元対応を変更・調査するとき。

## Do not read this when
- Codex exec の prompt stdin、出力処理、結果構築を調べるときは、exec 経路のテストを直接読む。

## hash
- f8c1590da9efbf22d28178bf61c08701a25070929beb1a1e15c3383032a045b8

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
- `cmoc oracle edit` の CLI 制御を検証し、入力編集から main worktree での2回の実行までの順序と、成功・失敗時の状態保持を確認する。
- 起動前提や準備段階の失敗、端末結果とレポートを含む、oracle edit 固有の実行境界を扱う。

## Read this when
- `cmoc oracle edit` の入力収集、2回の実行、設定や実行パラメーターの共有といった CLI orchestration を変更・調査するとき。
- 初回・2回目の実行失敗、起動前提、Git 差分や session state の保持、端末結果・レポートを変更・調査するとき。
- oracle edit が編集用 prompt skeleton と確定入力をどう実行へ渡すかを確認するとき。

## Do not read this when
- 共有 editor handoff の通信・上書き・終了処理を調べるときは、handoff の専用テストから確認する。
- editor input の共通予約、保存、エディター選択、読み取り・検証を調べるときは、prompt editor input の専用テストから確認する。
- 別の oracle サブコマンドの CLI 実行制御を調べるときは、そのサブコマンドに対応する CLI テストから確認する。

## hash
- b72d080d187079772caf025d723fa1a204c0723ec15f14ec0d4056952979c952

# `test_oracle_investigation_cli.py`

## Summary
- oracle investigation CLI の起動条件と、前処理・エディタ入力・起動パラメータ構築から TUI 起動までの連携を検証する。
- 専用 builder adapter の公開範囲も確認する。

## Read this when
- session のない main worktree からの起動可否や、このサブコマンド固有の入力・indexing preflight・TUI 起動の連携を変更または調べるとき。
- 専用 builder adapter の公開範囲を変更するとき。

## Do not read this when
- 調査責務や agent に渡す prompt の正確な内容を変更するときは、サブコマンド仕様または専用 builder を直接読む。
- 共通の editor input lifecycle や indexing の仕様・処理だけが対象で、このサブコマンドからの呼び出し連携に影響しないとき。

## hash
- fd594e5f3a8e768854c1e07b7262f4e0f6361568e9df1219e3d3f3aee804f55b

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
- 非対話末端サブコマンドに共通する primary report の完了経路を検証します。開始前エラーや中断時の report 保存、実行記録と Codex 出力の表示、保存・更新失敗時の扱いを横断して確認できます。

## Read this when
- 共通の report fallback、終了時の確定処理、実行記録や Structured Output の表示、保存失敗時の処理を変更・調査するとき。
- 開始前エラーや中断の report、Codex 出力や受理済み observation の記録に回帰がないか確認するとき。

## Do not read this when
- 特定サブコマンド固有の処理手順、report 項目や保存先を確認するときは、そのサブコマンドの正本仕様と専用テストを参照してください。この対象は共通の完了経路を横断しており、個別コマンドの仕様全体は扱いません。

## hash
- ac067735d0d445fd372647e4c8dc9a2d7e6b3aa4457409b11d089282a6171932

# `test_production_cli.py`

## Summary
- 実 Codex CLI と実推論を使い、利用者向け CLI の全末端コマンドを独立 process で実行する本番経路の受け入れテスト。LLM の回答品質ではなく、終了状態や report・state・Git・call log など外部から観測できる cmoc の制御を検証する。
- 非対話コマンドでは indexing、oracle edit、feedback 修復、run/session の状態遷移を確認し、TUI コマンドでは PTY 上の応答完了、editor input handoff、通知、副作用の境界を確認する。

## Read this when
- CLI の公開末端コマンドを追加・削除するとき、全末端を本番経路のシナリオが網羅しているか確認する。
- 実 Codex CLI の起動、呼び出し設定・ログ、indexing や feedback の実推論を含む制御経路を変更するとき。
- TUI の PTY 実行、応答完了、editor input handoff、通知、または run/session の状態遷移を変更するとき。

## Do not read this when
- 個別コマンドの内部ロジックや狭い出力を調べており、対象を絞った単体テストまたはコマンド別テストで確認できるとき。
- LLM の回答品質やプロンプトの意味的な良し悪しを評価するとき。このテストは回答品質を判定しない。

## hash
- aec02fe416e0f17c5ad5f9d35b9e45518fb5a97a2f63f6712c0ee78233460d8c

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
- 複数の policy builder の出力と complete prompt の組み立てを、共通の描画経路で横断して確認するテスト。policy の構造や順序、有効化、placeholder 統合、アクセスモード別の出力など、個別 builder のテストだけでは分からない統合上の責務を担う。

## Read this when
- complete prompt のセクション順・policy の有効化・Markdown 描画、または placeholder や file access mode の統合動作を変更するとき。
- 複数の policy 出力が complete prompt 上で重複なく正しい位置に現れるか確認するとき。

## Do not read this when
- エディター入力の予約・編集・収集や不正パス拒否だけを変更するときは、外部入力の挙動を扱う専用テストから確認する。
- 単一 policy の内部実装や文面だけを変更するときは、まず該当 builder とその個別の検証を確認する。complete prompt への統合も変わる場合は、このテストも読む。

## hash
- 7afed2cb658de09548264d3a9a44db958df5b9fc3a7c3aa85b763e66f3d5380c

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
- Codex CLI の引数・設定上書きと MCP 環境の分離に関するテスト。sandbox、model/provider、通知 hook、schema 保存、JSON 出力の境界条件を扱います。
- Codex 起動設定や通知 callback、schema-less 出力の変更時に、既存の契約と失敗時の扱いを確認する入口です。

## Read this when
- agent call の sandbox・model/provider 設定、MCP 注入や call context の環境変数分離を変更するとき。
- 通知 hook の有効条件、Codex 版確認、schema の保存方法、schema-less JSON 出力の不正値処理を変更するとき。

## Do not read this when
- process tracking file、PID や process group の検証・停止など、Codex subprocess の追跡と終了処理を調べるとき。これらを扱う実装や専用テストを直接確認してください。
- Codex 実行結果の recovery や、agent call 全体の実行制御を調べるとき。この対象は起動設定と一部の出力処理に範囲が限られます。

## hash
- c829e208c603d5ced36943feafc93d74593279486bc541a6af88531bb2d2e4a2

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
- FileAccessMode の永続化値と、既知の論理モードから Codex sandbox mode への変換契約を検証するテスト。
- Codex 実行時の sandbox 変換境界を確認する入口。

## Read this when
- FileAccessMode の永続化値が保たれるか確認するとき。
- 既知の file access mode と sandbox mode の対応を変更・調査するとき。

## Do not read this when
- mode ごとの詳細なファイルアクセス制限や prompt 文面を調べるときは、policy の構築・適用条件を扱うテストを読む。
- sandbox を含む Codex argv の組み立てや未知 mode の失敗条件を調べるときは、Codex 実行プロファイルの統合テストを読む。

## hash
- da671493f26abe84c50a963e608fef2af59ab84a099bb946321c5c38401ad4a2

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
