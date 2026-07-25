# `_acp_builder_support.py`

## Summary
- 対象ファイルは、テストコードから正本 schema を参照するための path 生成 helper を提供する。`acp_builder` 配下の schema 相対 path を受け取り、リポジトリ内の oracle schema の位置を返す。

## Read this when
- `acp_builder` の schema 参照方法や、テストで正本 schema の path を解決する仕組みを確認・変更するとき。

## Do not read this when
- schema の内容自体を確認・変更するときは、oracle 側の schema ファイルを直接読む。
- `acp_builder` と無関係なテスト補助や、実装本体の path 解決を確認するとき。

## hash
- 6fd184bad0b16e6bce9c32dac57e2187a8272303ece3f3c8d350acaeacf5824b

# `_cli_support.py`

## Summary
- doctor CLI を対象 worktree のカレントディレクトリで実行するための、テスト共通ヘルパー。Typer の CliRunner による実行結果取得と成功終了の検証を提供する。

## Read this when
- doctor CLI のテストを追加・修正するとき
- CLI を特定の worktree を cwd として実行するテスト支援を確認するとき

## Do not read this when
- doctor CLI の実装や仕様を確認したいとき
- doctor 以外の CLI テスト固有の検証ロジックを確認したいとき

## hash
- 4dc5c2cabc4b6e9d6ed90b6bedb5c1f94030cb30e4bef06293c8248a330ba923

# `_codex_support.py`

## Summary
- Codex 実行経路を検証するテスト向けの共通ヘルパーを提供する。Codex の一時ホーム準備、test-local Ollama 用設定、既定パラメータ生成、CLI 引数・設定値の解析、Codex override のスタブ化をまとめた、関連テストの入口となる補助モジュール。

## Read this when
- Codex runtime wrapper、apply fork、TUI の subprocess 制御、または test-local Ollama 経路のテストを追加・修正するとき
- テスト用 Codex 環境、AgentCallParameter、CLI override 引数の共通処理を確認するとき

## Do not read this when
- プロダクションコードの Codex 実行仕様や ACP builder の実装を確認するとき
- Codex 実行と無関係なテストを変更するときは、この共通テストヘルパーではなく対象テストを直接読む

## hash
- 068d30dcbee6bdda393c479d4ee2ed381574f80023e8cc67994def4e0e95b230

# `_command_support.py`

## Summary
- テスト用の fake external command として実行可能な Python スクリプトを書き込むヘルパー。UTF-8 で内容を保存し、実行権限を付与する。

## Read this when
- テストで外部コマンドの代替スクリプトを作成・実行する処理を確認するとき
- テスト用スクリプトの書き込み時のエンコーディングや実行権限を確認するとき

## Do not read this when
- 本番コードの外部コマンド実行処理を確認するとき
- テスト用スクリプト生成を伴わないテストを読むとき

## hash
- 37672f2473fdf889a2210635d4294e5f807fefd04034b00449f411bffcf86ae8

# `_git_support.py`

## Summary
- テスト用 Git repository の初期化・設定・commit と、現在の branch 取得を支援する共有ヘルパー。cmoc CLI の Git 状態や repository 構成を検証するテストから利用する入口。

## Read this when
- cmoc CLI のテストで一時 Git repository を作成する必要があるとき
- テスト対象 repository の checkout 済み branch 名や、追跡対象かつ ignore された oracle file の準備方法を確認するとき

## Do not read this when
- Git repository テストの共通準備や branch 状態の確認を扱わないテストのとき
- cmoc の制御ロジックや oracle 仕様そのものを確認したいときは、対応する実装・oracle file を直接読む

## hash
- e696cf9522455dcc18230828a049a03171d40dbec77215b3e8599a53611a21e2

# `_ollama_support.py`

## Summary
- 実経路統合テスト向けに、case-local Ollama の cache 準備・安全性検証・atomic publish・モデル materialize・GPU-only 推論確認・process group teardown を一体で提供するテスト支援モジュール。統合テストが専用 Ollama provider を必要とする場合の入口。

## Read this when
- Ollama を使う実経路統合テストの実行環境や test provider を確認・変更するとき
- Ollama の cache、モデル取得・再利用、GPU-only 条件、case ごとの process lifecycle を調査するとき
- 統合テストの失敗時に cache isolation、atomic publish、server 起動、推論可否、process teardown を調べるとき

## Do not read this when
- 通常の Ollama 設定や本番 provider 実装を確認したいとき
- Ollama を使わない単体テストや一般的な pytest fixture の実装を調べるとき
- Codex の model provider 定義そのものを変更・確認する場合は、まず設定実装や対応する oracle を読むべきとき

## hash
- 51f828693f90a2f79d04aa298982b904ffe13bd3b626a4e2fd1d238c809fb04f

# `test_acp_builder_editing_run_parameters.py`

## Summary
- editing run workload の canonical builder adapter を検証するテスト。apply builder が commit 範囲と raw diff を prompt に埋め込み、入れ子のコードフェンスや境界風文字列を保持することを確認する。refactor builder については canonical structured output schema、モデル設定、アクセスモード、prompt 内容を検証する。

## Read this when
- editing run の apply/refactor builder の prompt 生成、raw diff の埋め込み、structured output schema、モデル・推論設定、file access mode を変更または検証するとき。

## Do not read this when
- builder 実装や oracle schema の内容を直接変更・調査する必要があるときは、対応する oracle file または builder 実装を直接読む。editing run と無関係なテストや CLI 機能を扱うとき。

## hash
- c422d7488df4ee445a44cea9dfd8d6cdad546df65a96b0a31024e1bae6b08781

# `test_acp_builder_indexing_parameters.py`

## Summary
- indexing 用 INDEX.md エントリー生成 builder のモデル・推論設定、出力 schema の必須配列、対象本文の境界処理、互換公開面を検証するテスト。indexing builder の parameter や schema、prompt 生成の変更時に読む入口となる。

## Read this when
- indexing の INDEX.md エントリー生成 parameter、structured output schema、prompt 本文境界、互換 module の公開 API を変更または調査するとき。

## Do not read this when
- indexing 以外の builder や、INDEX.md エントリー本文の生成ロジック自体を変更・調査するとき。

## hash
- d1a423f4d9870464b843507a8d63a926528ce03fccaaec29ca7246ea61f83d49

# `test_acp_builder_oracle_review_parameters.py`

## Summary
- oracle review 用 ACP builder の parameter 生成、schema 一致、互換 module の公開面、model・reasoning・file access 設定を検証する pytest。動的入力の placeholder 保持と nested code fence 保護も対象とし、review 関連 builder の実装・oracle schema・互換性を確認するテスト入口。

## Read this when
- oracle review の ACP builder、parameter、schema、prompt 生成、互換 module の公開 API を変更または調査するとき
- review builder の動的入力、placeholder 変換、code fence 境界、schema 検証の失敗を調査するとき

## Do not read this when
- review 以外の ACP builder の挙動だけを変更・調査するとき
- 実装ではなく oracle review の schema 定義そのものを確認したいときは、対応する oracle schema を直接読む

## hash
- c34085bba3bd12891120d896287def47fdc8b609f24afdd2b73ea08678204f32

# `test_acp_builder_session_join_parameters.py`

## Summary
- session join の conflict resolution builder 契約を検証するテスト。公開 export の限定、repo write 権限・モデル・推論設定・プロンプト内容、indexing preflight 無効化、および conflict path 内の三連 backtick を含むコードフェンスの安全な生成を確認する。

## Read this when
- session join の conflict resolution 用パラメータ生成を変更・レビューするとき
- 公開 API、実行権限、モデル設定、プロンプト構造、コードフェンスのエスケープ挙動を検証するとき

## Do not read this when
- session join 以外の builder や conflict resolution 本体の実装だけを調査するとき
- テスト実行方法や共通の開発環境を確認するときは、対応する開発・テスト手順を直接読む

## hash
- 3d699182eea4768a184a5970b38ab535057d4cd0c23436bce6e756891daec77c

# `test_acp_builder_tui_parameters.py`

## Summary
- TUI の resolve parameter builder を検証するテスト。元プロンプトの埋め込み、標準 prompt の選定、読み取り専用・モデル・推論設定、構造化出力 schema の存在と4つの standard 選択項目、ネストしたコードフェンスの保持、公開 API の最小化を確認する。TUI resolve parameter 実装やその schema を変更・調査する際のテスト入口。

## Read this when
- TUI resolve parameter builder の挙動や schema を変更・検証するとき
- 元プロンプト内のコードフェンスや終了マーカーの扱いを調査するとき
- resolve parameter module の公開名や標準設定を確認するとき

## Do not read this when
- TUI resolve parameter 以外の builder や一般的な ACP parameter の仕様だけを調査するとき
- 実装の正本仕様を確認する必要があり、対応する oracle source を直接読むべきとき
- INDEX.md のルーティング情報だけを更新・確認するとき

## hash
- 4f9cd433607cb19fbee7b396a535097531e6981b1a626fd1b5d4ad6726238380

# `test_basic_runtime.py`

## Summary
- Root/worktree と path model の runtime 契約を検証するテスト。placeholder path の解決、repo root と linked worktree の区別、並列 pushd の cwd 保護、run worktree の作成・削除における管理領域・branch 対応・symlink・Git 登録状態の検証を扱う。runtime や path model の変更時に、破壊的な worktree 操作を拒否する境界を確認する入口となる。

## Read this when
- path placeholder の解決規則や repo/work/run root の扱いを変更・調査するとき
- pushd の並列実行時に process-global な cwd を安全に扱えるか確認するとき
- run worktree の作成・削除に関する path 検証、symlink 拒否、branch 対応、Git 登録状態を変更・調査するとき

## Do not read this when
- runtime や path model、worktree の挙動を扱わず、他の CLI 機能や独立したテストだけを変更・調査するとき
- テスト対象の具体的な実装責務を確認する必要があり、対応する runtime または path model の実装を直接読むべきとき

## hash
- 002807b994de92bea8bb6227d0d30db59e74dcfb3c5011dc1e69ca3102c53b02

# `test_cli_command_tree.py`

## Summary
- 公開 CLI の Click/Typer コマンドツリーを検証するテスト。oracle 変更後に定められた末端コマンド集合と実際の CLI を照合し、主要グループを含む help が互換性エラーなく描画されることを確認する。

## Read this when
- 公開 CLI のサブコマンド追加・削除・階層変更を実装またはレビューするとき
- Typer と Click の互換性や CLI help の描画問題を調査するとき
- oracle の CLI コマンド列挙と実装の整合性を検証するとき

## Do not read this when
- CLI の個別コマンドの実装詳細や入出力仕様を確認したいとき
- CLI 以外のテストや機能の変更を調査するとき
- コマンドツリーや help 描画に関係しないテストを読むとき

## hash
- cffc47f8ab96e3302d3f3478add14aaa2e1ad86d0722ba6bf95dfd6595e029ab

# `test_cli_tui.py`

## Summary
- TUI 起動直前の CLI 前処理について、editor input の衝突回避、prompt 解決、Codex TUI 起動パラメータ、linked worktree での保存先、`.cmoc` の ignore 挙動を外部挙動として検証するテスト群。TUI サブコマンドや関連する起動・prompt・worktree ログ処理の変更時に参照する入口。

## Read this when
- TUI サブコマンドの起動フロー、editor input 保存、prompt の生成・解決、Codex exec/TUI 呼び出し、linked worktree 対応、`.cmoc` ignore やログ保存の挙動を変更または検証するとき。
- TUI 起動時の固定アクセスモード、structured output schema、選択された standard の prompt 反映を確認するとき。

## Do not read this when
- TUI 以外のサブコマンドの挙動だけを調査するとき。
- TUI 起動処理の実装詳細ではなく、正本仕様そのものを確認するときは、対応する oracle 文書を直接読む。

## hash
- cc674c06ce3ee6624821fab5a637443857a04e6378ab08667f24315a6dedb5c8

# `test_codex_runtime_errors.py`

## Summary
- Codex JSONL の異常系と CLI 不在時の実行時挙動を検証するテスト。非 object・不正 JSONL、終了コード 0 でも不正な stdout、Codex CLI 不在時の CmocError と失敗ログを扱う。Codex 実行処理や関連するエラー分類・resume token・サブコマンドログの変更を確認する入口。

## Read this when
- Codex JSONL の parser 境界や malformed event の扱いを変更・検証するとき
- Codex CLI 実行失敗、CLI 不在時の例外、codex_call 失敗ログを変更・検証するとき
- Codex 実行時のエラー分類や resume token 抽出の挙動を確認するとき

## Do not read this when
- Codex の正常系実行や通常の JSONL event 処理だけを変更・確認するとき
- Codex 以外のサブコマンド、ログ形式、設定処理を直接確認するときは、それぞれの実装・テストを読む

## hash
- cbde29d6c3a596fca3f31434a5a16f599b860a3ec77a95e19fe49a39ee16ebd7

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 実行ランタイムの結合テストと契約テストを担う。Codex exec の argv、stdin、override、provider 設定、出力 schema、作業ディレクトリ、生成結果、CODEX_HOME の設定ファイル非生成を検証する。Codex 実行処理や関連するテスト helper の挙動を確認する際の入口となる。

## Read this when
- Codex exec の起動引数、sandbox・approval 設定、prompt の stdin 渡しを変更・調査するとき
- model provider、local Ollama、model class、reasoning effort の override 連携を変更・調査するとき
- output schema の配置・ハッシュ化、call log、Codex の出力結果を変更・調査するとき
- Codex 実行時のリポジトリ書き込み、作業ディレクトリ、HOME/CODEX_HOME の分離を検証するとき
- Codex runtime の GPU integration test または test-local Ollama を使う結合動作を確認するとき

## Do not read this when
- Codex CLI 実行ランタイムの実装詳細ではなく、一般的な Codex 設定仕様だけを確認したいときは、対応する oracle doc を直接読む
- Codex runtime と無関係なサブコマンド、設定、テスト helper の変更を扱うとき
- Codex exec の外部挙動や制御ロジックを検証する必要がなく、単なるテスト環境・fixture の整理だけを行うとき

## hash
- 2c274231d96e7e854c3ba24ed7523ec22da598405640a9f130a6c820d3eaf34d

# `test_codex_runtime_home.py`

## Summary
- Codex 実行時の CODEX_HOME 解決・引き渡し・検証を検証する pytest テスト。未設定時の既定値、相対パス、欠落・ファイル指定時の preflight failure、auth.json の provider 非依存性を扱う。
- Codex subprocess の起動前検証や実行結果の call log を確認するテストの入口。

## Read this when
- run_codex_exec の CODEX_HOME 処理や preflight 検証を変更・レビューするとき
- Codex home の既定値、相対パス解決、環境変数引き渡しを確認するとき
- 欠落またはディレクトリでない CODEX_HOME のエラー挙動を確認するとき
- auth.json の存在・種別を検証対象に含めるか判断するとき

## Do not read this when
- Codex subprocess の一般的な引数生成やイベント処理だけを変更するとき
- CODEX_HOME と無関係な CLI 設定・モデル選択・ファイルアクセス制御を確認するとき
- 実装の詳細ではなく、Codex 実行全体の別の外部挙動を検証する場合は、対応する runtime テストを直接読むとき

## hash
- b1141e9b112eee26cc28f247328a06e46e8e5cd94ba8dacb8ae6f04f255c4e47

# `test_codex_runtime_paths.py`

## Summary
- Codex exec 実行時のパスと sandbox 設定を検証するテスト。並列実行時の timestamp 付きログパス予約、cwd の選択、pure-oracle read の read-only sandbox、リンク済み worktree での schema 保存先、`.agents` パスを個別権限へ変換しないことを確認する。

## Read this when
- Codex exec のログ・出力・schema の保存先や timestamp 衝突対策を変更・調査するとき
- Codex exec の cwd、worktree、sandbox、FileAccessMode の変換挙動を変更・調査するとき

## Do not read this when
- Codex exec の実装詳細ではなく、prompt 生成や一般的な file access rule の正本仕様だけを確認したいとき
- Codex CLI の出力品質やモデル応答内容を検証したいとき

## hash
- 3ab24820d2425fbfde6bac10e0733b12b58f6ab902aae8edd607fd1a3739790b

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex quota exceeded 発生後の quota availability probe、待機、resume token による再開または prompt 再実行を検証する pytest テスト群。probe の構築条件、失敗伝播、JSONL 検証、並行呼び出しの代表 probe 共有、call log・subcommand log、CODEX_HOME/cwd、状態解除までを同一の quota retry 状態機械として扱う。

## Read this when
- Codex exec の quota 待機・復帰・retry 制御を変更または調査するとき
- quota probe の引数、prompt、ログ、resume token、並行実行時の挙動を検証するとき
- quota 復帰時の失敗処理、出力検証、CODEX_HOME/cwd 解決、待機状態のクリーンアップを確認するとき

## Do not read this when
- quota retry や Codex 実行制御に関係しないテストを変更・調査するとき
- 通常の Codex exec 引数生成や quota probe adapter の実装詳細だけを確認するときは、対応する実装ファイルを直接読む方が適切な場合

## hash
- 645232d5da1dca8a4753e1f697c26ebb881e6139509e48a8beac0684299617dc

# `test_codex_runtime_retry.py`

## Summary
- Codex exec の再試行・失敗処理と関連ログを外部挙動として検証するテスト。Structured Output の意味的失敗や解析失敗、capacity retry、未知の JSONL error、中断、retry 上限、差分保持、stdout 外エラーマーカーの扱いを対象とする。run_codex_exec の状態、subprocess 呼び出し回数、call log、subcommand event を一続きの責務として確認する。

## Read this when
- run_codex_exec の retry 条件、backoff、上限、失敗結果を変更または調査するとき
- Codex 呼び出しの call log や subcommand event の schema・status・保存内容を変更または検証するとき
- Structured Output の検証失敗、JSONL error、KeyboardInterrupt、capacity failure、agent diff 保持の挙動を確認するとき

## Do not read this when
- Codex exec の通常成功経路だけを変更・調査するとき
- retry や失敗時ログに関係しない Codex 実行設定・プロンプト生成を扱うとき

## hash
- cba7a9b0499545ecf4b9e9033c6ac6718506e48f75b4f79ea047e303360367de

# `test_codex_runtime_subprocess.py`

## Summary
- Codex subprocess の process group tracking と終了処理を検証するテスト。child tracking の登録・維持、pidfd を用いた group signal、SIGTERM の遅延、leader 終了後や割り込み時の追跡継続、tracking 失敗時の停止・reap、継承 tracking 環境変数の無視を扱う。runtime の subprocess 実装や apply の abandon/cleanup 挙動を確認する入口となる。

## Read this when
- Codex subprocess の起動、process group・PID tracking、停止や cleanup の挙動を変更・調査するとき
- apply の abandon 処理、割り込み、子孫プロセスの残存、tracking file の異常系を検証するとき
- Codex 起動時の process tracking 環境変数の扱いを確認するとき

## Do not read this when
- Codex subprocess tracking や process group cleanup と無関係な CLI 機能・テストを扱うとき
- apply の仕様そのものを確認する場合。先に oracle の apply/abandon 仕様を読むべきとき
- runtime の別機能の単体テストだけを調査するとき

## hash
- a64cb4f02f4c197c7f251bad98428b2ba2ec1a0021b3f57d0ef199070988435f

# `test_codex_runtime_tui.py`

## Summary
- Codex TUI 実行ランタイムの統合テスト。完成済み prompt の読み込み、作業ディレクトリと sandbox・承認設定、Codex CLI の引数、call log とサブコマンドイベント、コンソール要約を検証する。正常終了、timestamp 衝突、CLI 不在、KeyboardInterrupt、非 0 終了を扱う。

## Read this when
- Codex TUI の prompt 読み込みやファイルアクセス境界を変更・確認するとき
- Codex CLI 呼び出しの引数、作業ディレクトリ、sandbox、承認設定を変更・確認するとき
- TUI の call log、イベントログ、コンソール出力、失敗時処理を変更・確認するとき

## Do not read this when
- Codex TUI 以外のサブコマンドやランタイムのテストだけを扱うとき
- Codex 呼び出しの実装詳細を直接調査する必要があり、対応するランタイム実装を先に確認すべきとき

## hash
- e29f9d50300b34c0bcab1a210497ea92008d2e5e888dc1af11b038f2d636d3f7

# `test_doctor_cli.py`

## Summary
- doctor preprocess の統合テスト。CLI と直接呼び出しの両方で、Git 状態・config・refactor state・共有 doctor lock の修復 lifecycle を検証する。
- 修復 commit が既存の staged/unstaged 差分、index flag、intent-to-add、rename を保持し、`.cmoc/gu` の追跡解除や `.agents/.gitkeep`・config の生成を正しく行うことを確認する。

## Read this when
- doctor preprocess の外部挙動、修復 commit、config 同期、linked worktree 対応を変更または検証するとき
- doctor が共有 repository lock を待機する動作や、既存 Git index の状態保持を調査するとき

## Do not read this when
- doctor preprocess 以外のサブコマンドや、内部 helper 単体の実装だけを変更・確認するとき
- Git・config・refactor state の修復 lifecycle と無関係なテストを調査するとき

## hash
- 4ea4177673451a41ad983338d829152d71fdf209336e75a82145799dc971037e

# `test_editing_run_cli.py`

## Summary
- workload fork と共通 run join/abandon の統合 realization test。editing run の session state・run worktree・fork report・join/abandon lifecycle を対象とし、変更 path、report 衝突回避、oracle/realization 境界、apply/refactor fork の成功・失敗・中断・rollback、run join の merge・検証・同期・force-resolve を検証する。関連する CLI・lifecycle・report・refactor の統合挙動を確認するための入口。

## Read this when
- realization apply/refactor の fork と run join の lifecycle を変更・レビューするとき
- session state、run worktree、branch、report、merge、rollback、force-resolve の統合挙動を調査するとき
- refactor fork の target 処理、unresolved 状態、INDEX 同期、Codex child cleanup を検証するとき

## Do not read this when
- 単一の helper や単独サブコマンドの局所実装だけを確認するとき
- run lifecycle と無関係な CLI 機能や oracle 文書を調査するとき
- 個別の INDEX 生成ロジックだけを確認する場合は、まず indexing 実装・専用テストを読むべき

## hash
- be0084e0a93aaccf3bb3fe91002672405349f1151fd3e062d817ca23981739ad

# `test_indexing_cli.py`

## Summary
- `cmoc indexing` の CLI と preflight、doctor、worktree 対象判定、INDEX.md 更新、Codex structured output、INDEX 専用 commit の外部挙動を検証するテスト。通常の clean/dirty repository、linked worktree、設定継承、hash による再生成省略、Git 異常終了を扱う。

## Read this when
- `cmoc indexing` の CLI 動作や事前条件を変更・確認するとき
- INDEX.md の生成・更新・hash 判定・Codex 呼び出しを変更・確認するとき
- indexing preflight、worktree、doctor、commit 対象パスの挙動を変更・確認するとき

## Do not read this when
- INDEX.md のルーティング生成ロジック自体を変更・確認するときは、対象の実装・仕様ファイルを直接読む
- indexing と無関係な CLI サブコマンドや一般的な Git ヘルパーの挙動だけを調べるとき

## hash
- b63b722197d2f8f3b0e96b65b2a2d26828d20963e4e67ec745cd5f3cadb56f35

# `test_indexing_common.py`

## Summary
- `commons.indexing` の INDEX.md 生成・解析・更新処理を直接検証するテスト。入力検証、ハッシュによる再利用と再生成、空ディレクトリやネストした memo の traversal、symlink・特殊ファイルの除外、安定した描画順、並列更新、logger の伝播、pushd 中の実行、linked worktree 間の lock 共有を扱う。

## Read this when
- INDEX.md の entry schema 検証や render/parse/update の挙動を変更・調査するとき
- ディレクトリ traversal、symlink、特殊ファイル、memo 除外、並列更新、lock の回帰を確認するとき
- INDEX 更新時の Codex worker と subcommand logger の連携を確認するとき

## Do not read this when
- CLI lifecycle や indexing サブコマンド全体の統合挙動を確認したいときは、対応するサブコマンド実装・テストを直接読む
- INDEX entry の正本仕様や生成 prompt の規約を確認したいときは、参照されている oracle 文書・oracle source を読む

## hash
- 02521388eea0b35228ea7766094f0d5cf4725829704b503e335011e53b184550

# `test_indexing_preflight.py`

## Summary
- Codex 実行前の indexing preflight を検証するテスト。exec/TUI 経路での実行順序、linked worktree の選択、repository lock 待機、パラメータによる無効化、file access violation 後に recovery indexing を行わない制約を扱う。indexing と Codex 実行連携の挙動を確認するためのテスト入口。

## Read this when
- Codex 呼び出し前の indexing preflight の実行条件・順序・対象 worktree を変更または検証するとき
- repository lock との排他制御や、preflight 無効化・recovery 禁止の挙動を確認するとき

## Do not read this when
- INDEX.md 生成そのもののアルゴリズムや個別の Codex 実行実装を変更するとき
- preflight と無関係な CLI 機能やテストを調査するとき

## hash
- 721d5257bee16bdb655a64f92321934576c947ac6c7eb8d2ccdfeafa89de574f

# `test_oracle_edit_cli.py`

## Summary
- `cmoc oracle edit` の main worktree TUI 制御を検証するテスト。doctor 済みの隔離 Git リポジトリと session state を準備し、indexing preflight、clean worktree 検査、TUI 呼び出し順、AgentCallParameter、oracle 差分保持、失敗時の終了コード、session state 非変更を確認する。
- `oracle edit` の起動前提として、main worktree、active session branch、clean worktree を要求すること、および linked worktree・非 session branch・inactive session・未コミット差分を利用者向けエラーとして扱うことを検証する。

## Read this when
- `oracle edit` の CLI 実装、TUI 起動処理、indexing preflight、run lifecycle 非使用の挙動を変更または調査するとき。
- `oracle edit` の起動前提、session state、worktree の clean 条件に関するテストを追加・修正するとき。
- TUI 実行成功・失敗時の oracle 差分、終了コード、AgentCallParameter の契約を確認するとき。

## Do not read this when
- `oracle edit` 以外のサブコマンドや、CLI 全体に共通しない機能のテストを調査するとき。
- oracle 仕様そのものの編集や、実装ではなく別の session lifecycle の挙動だけを確認するとき。

## hash
- 713a3077054c43157af509c46b729b57ce58fa2c67183673db67df9bf0fe47cf

# `test_oracle_review_loop.py`

## Summary
- oracle review の finding loop に対する回帰テスト。finding の対象別引き継ぎ、main worktree のパス照合、challenger/advocate の理由伝播、割り込み時の部分結果保持、semantic merge retry と上限到達時の失敗を検証する。
- 同一 review round と fake Codex call 列を通じて、列挙・検証・judge の外部契約をまとめて確認するテスト入口。

## Read this when
- oracle review の finding 列挙・統合・検証・judge loop を変更または調査するとき
- challenger/advocate の prompt 内容や round 間の finding state 引き継ぎを確認するとき
- KeyboardInterrupt 復旧、部分結果、semantic retry の挙動を変更または検証するとき

## Do not read this when
- oracle review 以外のサブコマンドや、finding loop に関係しない一般的なテスト基盤を調査するとき
- 正本仕様そのものを確認する場合。対応する oracle doc と開発ルールを直接読むこと

## hash
- d45fa314f9859cebd6809f9e0d38bb754159fb248f4c14b019c9f0a48b2b4b42

# `test_oracle_review_merge_operations.py`

## Summary
- oracle review の finding merge operation について、delete・replace・merge の kind 契約、finding 更新、採番を検証する pytest。対象 ID・payload の不正、ID の重複利用も拒否されることを確認する。

## Read this when
- oracle review の merge operation の仕様変更や実装変更を検証するとき
- finding の削除・置換・統合、採番、入力検証のテストを確認するとき

## Do not read this when
- oracle review の通常の CLI 入出力や merge operation 以外の処理を確認するとき
- 正本仕様そのものを確認するときは、参照されている oracle review 文書を直接読む

## hash
- 8e42fe28e2b74c0ad87780ea4beaa26109a196a0df587aa2d7ec155cf8296478

# `test_oracle_review_report.py`

## Summary
- oracle review の report 構築と CLI 出力を検証する回帰テスト。所見の受理・棄却、severity 別分類、件数集計、oracle path・symlink の扱い、scope 短縮指定を対象とする。
- 列挙・判定処理の正常終了だけでなく、中断・途中失敗時の report 保存、完了済み oracle のみの表示、error summary、終了出力も検証する。

## Read this when
- oracle review の report schema、finding 表示、CLI 出力、件数集計を変更または調査するとき
- oracle review の中断・エラー時挙動や未完了 finding の扱いを確認するとき

## Do not read this when
- oracle review の実装処理そのものを変更・調査する場合は、まず対応する実装モジュールを読むとき
- oracle review と無関係なサブコマンドや一般的なテスト基盤だけを変更・調査するとき

## hash
- cc289cb4cc9fa68eb7a508f5ddfb7993688df3f82662aabb415a5bcb7c377303

# `test_oracle_review_targets.py`

## Summary
- oracle review の対象列挙と finding path 解決を検証するテスト。相対・絶対・placeholder 付きパス、symlink、外部 oracle path の扱いを確認し、session/full scope における追跡済み oracle file の選定、除外条件、review fork 基準、対象なし時の出力を検証する。

## Read this when
- oracle review の対象ファイル列挙、scope 別のレビュー対象選定、finding path 解決を変更・調査するとき
- oracle file の定義に基づく AGENTS.md・INDEX.md・ignored file・symlink の分類を確認するとき
- oracle review の対象数、no_targets、review fork commit 固定に関するテストを確認するとき

## Do not read this when
- oracle review のレポート生成形式や finding の内容検証だけを変更・調査するとき
- oracle review と無関係な CLI サブコマンドや一般的な git 操作を扱うとき
- 実装の対象列挙・path 解決ではなく、別の oracle review テストの観点を直接確認できるとき

## hash
- 5ff7c6bd4e39ef65acfe8a0626aa25af35e24f7829c3eb37d04fb290a049d430

# `test_oracle_review_worktree.py`

## Summary
- oracle review の review worktree lifecycle を検証する回帰テスト。linked worktree と session branch を対象に、snapshot commit からの fork、未コミット差分や INDEX.md 以外の変更の拒否、active editing run 中の実行、INDEX.md の統合・競合解決、preflight commit、cleanup 失敗の報告を確認する。

## Read this when
- oracle review の linked worktree、review run の fork 元、preflight commit、差分検証、INDEX.md 統合、merge conflict 解決、cleanup 挙動を変更または調査するとき。
- oracle review の worktree 隔離や session branch との連携に関する回帰テストを追加・修正するとき。

## Do not read this when
- oracle review の所見列挙・妥当性検証・判定ロジックだけを変更し、review worktree lifecycle や INDEX.md 統合に関係しないとき。
- 一般的な INDEX.md 生成仕様を確認したい場合は、indexing の oracle 文書や INDEX.md 更新実装を直接読む。

## hash
- b6fd491a938e887a97e6451836cbef0eae10e4ffb75bbe470b6f024a52a0c058

# `test_packaged_import.py`

## Summary
- packaged layout 上での import 境界と公開 API を検証するテスト。oracle review/edit builder、ACP basic、cmoc config の import・再公開・出力契約を、隔離した一時環境で確認する。

## Read this when
- packaged layout での Python import が失敗する問題を調査するとき
- builder や config の公開面、canonical 定義の再公開、structured output 契約を変更・検証するとき

## Do not read this when
- packaged layout や import 境界に関係しない機能を変更するとき
- 個別 builder の内部ロジックだけを調査し、隔離環境での公開契約を確認する必要がないとき

## hash
- 03bfd812e2a27540732f277777e9f2e12787c042b1c95a522ba0537a6b359c82

# `test_production_cli.py`

## Summary
- 実 Codex CLI と case-local Ollama を使い、独立 process・PTY 上で全末端サブコマンドの本番経路を検証する受け入れテスト。CLI 終了 code、report・state・Git・Codex call log、TUI の応答完了と終了を確認し、LLM の回答品質自体は判定しない。

## Read this when
- 本番相当の独立 process で CLI サブコマンドの正常系を検証・変更するとき
- 全末端コマンドの登録漏れ、session/run の状態遷移、Git・state・report の外部副作用を確認するとき
- Codex TUI の PTY 操作、端末 capability query、応答完了、終了処理を調査するとき
- 実 Codex CLI、case-local Ollama、隔離された Codex home と test repository を用いる GPU integration test を実行するとき

## Do not read this when
- 単体の CLI 実装や内部 helper のロジックだけを変更・調査するときは、対応する src または通常の realization test を直接読む
- LLM の回答品質やプロンプト内容そのものを評価するとき
- Codex CLI や Ollama を使わない軽量な unit test を確認するとき

## hash
- 2571c81c78cdc3a6b0d7aea9208002d4ff16e4d02b755f1d165d91255c54d9bd

# `test_prompt_parts.py`

## Summary
- 標準 prompt parts の StructDoc rendering と complete prompt の組み立て結果を検証する回帰テスト群。各標準ルールの見出し・主要文面、file access mode ごとの内容、標準ルールの包含条件、root placeholder の保持と展開を扱う。prompt builder や標準 prompt 文面の変更時に確認する入口となる。

## Read this when
- prompt parts の rendering や complete prompt の包含・除外条件を変更または調査するとき
- file access mode、root placeholder、標準ルール注入の挙動を変更または検証するとき
- prompt builder 周辺の回帰テストを確認するとき

## Do not read this when
- prompt builder の実装詳細や標準 prompt 文面そのものを確認したいときは、対応する src の実装へ直接進む
- StructDoc の一般的な rendering 仕様を確認したいときは、StructDoc の定義・専用テストへ進む
- prompt parts や complete prompt と無関係な CLI 機能・テストを扱うとき

## hash
- e9a44a7913150d1e8a5aa5716df9ccb6df25db99fe210633d91e4b8452906b32

# `test_runtime_cli.py`

## Summary
- CLI の error、log、preflight、completion 境界を検証するランタイム CLI 回帰テスト。
- duration 表示、サブコマンドログの衝突・並列記録、doctor/pre-log 失敗時のログ、構造化 error report、CLI 解析エラー、work root 制約、completion の副作用抑止、起動 wrapper の失敗、gitignore 更新を扱う。

## Read this when
- CLI の error report、終了コード、stdout/stderr 出力、call stack、引数解析失敗を変更・調査するとき。
- サブコマンドログ、logger の並列性・timestamp 衝突、quota wait、preflight または doctor preprocess の失敗処理を変更・調査するとき。
- work root 判定、shell completion probe、起動 wrapper の venv エラー、cmoc 用 gitignore 更新を変更・調査するとき。

## Do not read this when
- 個別サブコマンドの業務ロジックや固有の入出力だけを変更・調査する場合は、対応するサブコマンドのテストを直接読む。
- CLI lifecycle の error、log、preflight、completion に関係しない parser、oracle、realization の単体挙動を調査する場合。

## hash
- e05c2fcc7f97b369cc93efda460acded3190797c379bdb0546382994a5f5e016

# `test_runtime_codex_conflicts.py`

## Summary
- session join の conflict path が prompt にのみ反映され、path 別の sandbox 設定や Codex override argv に変換されないことを検証するテスト。conflict 対象が oracle 配下でも src 配下でも、repo write と共通の workspace-write sandbox を使い、対象 path が argv や権限設定へ漏れないことを確認する。

## Read this when
- session join の conflict resolution、prompt 生成、sandbox/権限引数への変換を変更・検証するとき
- conflict 対象 path の扱いや Codex override 設定の回帰を調査するとき

## Do not read this when
- session join の conflict path と無関係な runtime Codex 機能を変更・調査するとき
- sandbox 設定や prompt への conflict 対象の反映を確認する必要がなく、対象の実装・正本仕様を直接読むべきとき

## hash
- 8a87436b654938a146bd3624bb6125d96a016fc954bfaec1f63c87a6fe83d99c

# `test_runtime_codex_permissions.py`

## Summary
- Codex CLI の sandbox argv が permission profile に依存しないことを検証するテスト。全 FileAccessMode で sandbox 引数だけが適切に生成され、profile や権限関連 config が注入されないことを確認する。
- argv builder API に path 単位の read/write 例外入力が存在しないことを検証する。Codex CLI が生成された sandbox 引数を受理し、権限エラーではなく schema 読み込みエラーに到達することも確認する。

## Read this when
- Codex CLI の sandbox 引数生成、permission profile/config 注入禁止、または FileAccessMode ごとの権限制御を変更・検証するとき
- build_codex_override_args や prepare_codex_override_args の引数を変更するとき

## Do not read this when
- Codex CLI の権限 argv や runtime profile と無関係な機能を変更・調査するとき
- 実装の詳細ではなく、Codex CLI 全体の利用方法や一般的な subprocess テストを確認したいとき

## hash
- 613b6ae1a298d72dcd0f70ee166744147a12c589cd52f915f71c95539fc83128

# `test_runtime_codex_profile.py`

## Summary
- Codex argv の model、sandbox、provider 上書き契約を検証する realization test。全 FileAccessMode の sandbox 変換、承認・model・reasoning 引数、未知 mode や未定義 provider の拒否、選択 provider の TOML argv エンコード、prepare 境界の設定専属性を扱う。runtime_codex_profile の変更や Codex 起動前 override 構築の挙動を確認するためのテスト入口。

## Read this when
- Codex の model、sandbox、provider override 引数の構築・検証を変更するとき
- FileAccessMode と Codex sandbox の対応、provider 設定の argv/TOML 変換、未定義値のエラー挙動を確認するとき

## Do not read this when
- Codex override argv や runtime_codex_profile の挙動に関係しないテスト・実装を扱うとき
- Codex の実際のプロセス起動や prompt 生成の詳細を確認したいとき

## hash
- 195ae336c754e125658cec4f93d5955e0a8b4e436ba305e9bf5cb65322f8e617

# `test_runtime_config.py`

## Summary
- CmocConfig の既定値、JSON 変換時のメンバー順、設定ファイル読み込み、入力検証、provider-local 設定値の保持・拒否を検証するテスト。設定ランタイムの仕様変更や不正設定のエラー挙動を確認する際の入口。

## Read this when
- CmocConfig の既定値や論理 model class・reasoning effort の対応を変更するとき
- config_from_dict、config_to_dict、load_config の入出力・永続化・エラー挙動を変更または検証するとき
- Codex model provider、model spec、provider-local JSON/TOML 値の検証を変更するとき

## Do not read this when
- 設定処理ではなく、CLI コマンドの実行制御や設定以外のランタイム機能を変更するとき
- CmocConfig の実装詳細を直接確認したいときは、対応する実装ファイルを先に読む

## hash
- 30520fe82d8308e91f103ff23937d1215bba93e5bde8376a667f0b18768c9e23

# `test_runtime_content.py`

## Summary
- runtime_content の補助関数を検証するテスト。内容が NUL byte を含むかによる binary 判定と、hash ベースの保存時に既存 symlink のリンク先を上書きせず置換する挙動を扱う。runtime_content の保存処理や binary 判定を変更・調査するときのテスト入口。

## Read this when
- runtime_content の is_binary または write_hashed_file を変更・レビュー・デバッグするとき
- テキスト／binary 判定や、hash path が symlink の場合の安全な保存挙動を確認するとき

## Do not read this when
- runtime_content の実装詳細を確認したいだけで、テストケースや期待挙動の確認が不要なとき
- runtime_content と無関係な機能の実装・テストを調査するとき

## hash
- 1d7cd925d0b731ec53366c6eb796bed8c9be466df205b88ae5f6b9f8f07ad5c3

# `test_runtime_file_access.py`

## Summary
- FileAccessMode の JSON 永続化値と Codex sandbox mode への変換契約を検証するテスト。READONLY 系と各種 write mode の対応を確認する。

## Read this when
- FileAccessMode の値、または file_access_to_sandbox_mode の変換結果を変更・調査するとき
- sandbox モード変換や関連する runtime テストを追加・修正するとき

## Do not read this when
- ACP の FileAccessMode 定義そのものを変更・調査するときは、oracle の根拠ファイルを先に読む
- prompt のファイルアクセス規則を変更・調査するときは、oracle の根拠ファイルを直接読む
- FileAccessMode や sandbox 変換と無関係なテスト・実装を扱うとき

## hash
- 0f39773aec1b938ee1f0a4dbca60b301082daf452c8f045e08f086ea979eb1d8

# `test_runtime_refactor.py`

## Summary
- realization refactor の永続 state について、oracle と realization の file 集合の同期、調査履歴の保持、変更 file の再調査化、調査対象の選択規則を検証するテスト。
- state の path・timestamp・調査結果・UTF-8・NUL を含む path key などの schema 検証も扱う。

## Read this when
- realization refactor の state 同期・履歴保持・target 選択の挙動を変更または検証するとき
- refactor state の不正データ拒否や schema 検証のテストを追加・修正するとき

## Do not read this when
- refactor state と無関係な runtime 機能や別サブコマンドのテストを扱うとき
- 実装の詳細を直接確認する必要があり、対応する runtime 実装または正本仕様を読むべきとき

## hash
- ad5b5d69f6ec18b11429f517c1552079b21723aaceb0145f7bf0cc05dd2e0c19

# `test_runtime_state.py`

## Summary
- session/run state の永続化スキーマと managed branch 解析を検証する realization test。state の型・必須項目・未知 field・不正な run kind、session/run branch からの state 解決、session 部分の部分読み込み、無効 state の書き込み拒否を扱う。session fork lock が process・thread 間で共有されることも確認する。

## Read this when
- session/run state の schema 検証や永続化時のエラー挙動を変更・調査するとき
- managed branch から session ID や state file を解決する処理を変更・調査するとき
- session fork lock の process 間共有や競合制御を変更・調査するとき

## Do not read this when
- session/run state の実装詳細そのものを確認したい場合は、対応する runtime state 実装を直接読む
- CLI の出力や Codex/LLM の品質を調査する場合
- session state と無関係な branch 操作やロックを調査する場合

## hash
- b5636f4a0e9a59b6893094bf492c6061297d0cdbd2f19333daadd4a763e325e8

# `test_session_cli.py`

## Summary
- session fork/join/abandon の CLI 外部挙動を統合的に検証する回帰テスト。session branch と永続 state の生成・更新・削除・rollback、linked worktree、preprocess、dirty worktree 拒否、join の conflict 解消、Codex 実行境界、エラー出力を扱う。session 状態遷移に関するテスト変更の入口となる。

## Read this when
- session fork、join、abandon の挙動や回帰テストを変更・調査するとき
- session state、branch cleanup、linked worktree のライフサイクルを検証するとき
- session join の conflict resolution、Codex sandbox、repo root/cwd、エラー出力を確認するとき
- session CLI の precondition、rollback、dirty worktree 拒否を確認するとき

## Do not read this when
- session CLI と無関係なサブコマンドの実装・テストを調査するとき
- session state の正本仕様だけを確認したいときは、対応する oracle doc を直接読む
- session CLI の実装詳細だけを確認したいときは、対応する sub_commands.session 配下の実装を直接読む

## hash
- f504dadfaa1f9452011d8214518885f4420c2fba5ec89cba0ae21b4ca2fa3452

# `test_struct_doc_rendering.py`

## Summary
- StructDoc の Markdown renderer における整形挙動を検証するテスト。通常の本文と code block 内で連続する空行を一つに縮約すること、および互換モジュールから再公開された StructBlock が renderer で利用できることを確認する。

## Read this when
- Markdown renderer の空行縮約仕様を変更・検証するとき
- StructDoc、StructBlock、StructCodeBlock、render_as_markdown の互換公開や出力形式を変更するとき

## Do not read this when
- renderer 以外の StructDoc 機能や CLI の挙動を確認するとき
- 実装の詳細を調べる必要があり、対応する basic.struct_doc の実装を直接読むべきとき

## hash
- 650a3dab8a023eb6c55dd32e6ed5ce178f4641d3f81b8805b33c18bce039c1db
