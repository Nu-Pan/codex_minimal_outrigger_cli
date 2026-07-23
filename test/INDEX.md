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
- Codex 実行経路をテストするための共通ヘルパー群。fake 結果、隔離した CODEX_HOME、Codex パラメータ、CLI 引数・設定の解析、実行時 override の固定化を提供する。

## Read this when
- Codex runtime wrapper、apply fork、test-local Ollama 経路、Codex CLI override のテストを追加・修正するとき。

## Do not read this when
- Codex 実装本体や oracle の仕様を確認したいとき。単一テストの固有 fixture だけを扱うとき。

## hash
- 054a356acb5f2c0245d877b7d8d4a9c8dfee983608c94c76cd566f19bdeaafb8

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
- editing run workload 用の realization apply/refactor builder adapter を検証するテスト。apply builder の commit 範囲・oracle raw diff の prompt 埋め込みと実行設定、refactor builder の canonical structured output schema・モデル設定・ファイルアクセスモードを確認する。

## Read this when
- realization apply または refactor の fork launch-exec parameter builder を変更・レビューするとき
- commit range や oracle raw diff の prompt 反映を検証するとき
- refactor 用 structured output schema や実行設定の接続を確認するとき

## Do not read this when
- builder の実装詳細や prompt 定義そのものを調査する場合は、対応する src の builder 実装を直接読む
- editing run と無関係な ACP builder や一般的なテスト実行方法を調べる場合

## hash
- c0aafbd858ae8c179ae7e51d4bc257cd732f65c4b063d65e4e4c28c86fc9290d

# `test_acp_builder_indexing_parameters.py`

## Summary
- indexing 用 INDEX エントリービルダーのパラメータ設定、Structured Output schema の必須条件、互換モジュールの公開面を検証するテスト。indexing のパラメータや schema、互換 export を変更・確認する際の入口。

## Read this when
- indexing 用 INDEX エントリービルダーの model、reasoning、file access、preflight 設定を変更するとき
- INDEX エントリーの Structured Output schema の必須項目や配列制約を変更するとき
- indexing の互換モジュール公開 API を変更・確認するとき

## Do not read this when
- INDEX エントリーの生成ロジック自体を変更・確認するときは、対応する realization implementation や正本を直接読む
- indexing と無関係な builder、schema、公開 API の変更を扱うとき

## hash
- 970cc49aa2c0d2e2141dc376ed218d3ab7cd81a7016068d67403061821059631

# `test_acp_builder_oracle_review_parameters.py`

## Summary
- oracle review ACP builder の parameter、schema、adapter 公開面を検証するテスト。各 review builder の公開関数、モデル・推論設定・ファイルアクセス設定、oracle source との schema 一致、placeholder 補正、動的入力保持、canonical builder との互換性を確認する。

## Read this when
- oracle review の ACP builder、parameter 設定、structured output schema、互換 adapter の公開面を変更・調査するとき。

## Do not read this when
- oracle review 以外の ACP builder を扱うとき。実装本体や oracle source の仕様を直接確認する必要がある場合は、対応する oracle または realization 実装・schema を先に読むとき。

## hash
- 23c3d444daff832799471366a74db102cc64090eed9379618407ca32bc7f43c8

# `test_acp_builder_session_join_parameters.py`

## Summary
- session join の conflict resolution 用パラメータ生成に関する契約を検証するテスト群。公開モジュールの公開面と、生成されるパラメータの権限・モデル選択・索引前提の有無を確認したいときに読む。

## Read this when
- session join の conflict resolution builder の公開 API が何を返すべきか確認したいとき。
- conflict 対象ファイルを渡したときの生成パラメータの権限、推論強度、モデル選択、プロンプト条件を確認したいとき。
- 公開モジュールが内部実装を露出していないか、エクスポート境界を点検したいとき。

## Do not read this when
- session join の通常 join 処理や別の builder の契約を確認したいとき。
- conflict resolution の実装詳細や prompt 組み立ての内部構造を追いたいときは、対応する実装側の本文を直接読むべきとき。
- ファイルアクセス方針やモデル選択の共通定義そのものを確認したいときは、テストではなく基礎となる定義ファイルを読むべきとき。

## hash
- f1b9f037d93dce9aed913c05500c19041aae57dc069365c274a9e4a73e4f6d51

# `test_acp_builder_tui_parameters.py`

## Summary
- TUI の resolve parameter builder について、生成されるパラメータの標準設定・prompt 埋め込み・schema ファイルの内容・公開 API を検証するテスト。元の依頼文や標準 prompt の一部が含まれること、4 つの standard 選択項目だけを持つ schema であること、互換 module の公開名が限定されていることを確認する。

## Read this when
- TUI の resolve parameter builder、生成 prompt、structured output schema、またはその公開 API を変更・調査するとき
- TUI parameter builder の標準設定や schema の互換性を検証するとき

## Do not read this when
- TUI の resolve parameter builder や resolve parameter schema に関係しないテスト・実装を扱うとき
- builder の実装詳細を直接確認したいときは、対応する oracle または realization implementation を先に読む

## hash
- bc1e1ccdda8e103b81a6cec702713901f8eb27a51b5db9420a99ab2ccdc3fa95

# `test_basic_runtime.py`

## Summary
- Root/worktree と path model の runtime 契約を検証するテスト。placeholder path の解決、repo root と linked worktree の区別、cwd 変更の直列化、run worktree の作成・削除時における管理領域・branch・symlink・登録状態の検証を扱う。

## Read this when
- path placeholder や repo/worktree root の解決動作を確認するとき
- run worktree の作成・削除に関する安全性や拒否条件を変更・検証するとき
- pushd の並列利用や test repository の Git 設定隔離を確認するとき

## Do not read this when
- CLI の通常コマンド動作や、path model・worktree runtime と無関係なテストを調査するとき
- 実装の詳細を確認する必要があり、対応する runtime 実装や oracle file を直接読むべきとき

## hash
- f2d7b2680ef96098e820ee826f39cc114cf83b592b6d3cbb6b9da87d7c910261

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
- Codex CLI の実行ランタイムを検証するテスト。実 Codex CLI と test-local Ollama を用いた GPU 統合テストに加え、Codex の argv、stdin、作業ディレクトリ、出力スキーマ、model provider override、CODEX_HOME 設定未生成、リポジトリ書き込みをモック実行で検証する。Codex 実行経路や override 引数の挙動を確認する際のテスト入口。

## Read this when
- run_codex_exec の実行仕様、Codex CLI 引数、prompt の stdin 渡し、output schema の配置や内容を変更・調査するとき
- model provider、model class、reasoning effort、sandbox、approval 設定の Codex override 連携を変更・検証するとき
- Codex HOME に設定ファイルを生成しない制約や、実 Codex CLI と test-local Ollama の統合動作を確認するとき

## Do not read this when
- Codex 実行ランタイムの実装詳細そのものを変更・調査する場合は、まず対応する src 側の実装を読むとき
- Codex 以外のサブコマンド、provider 設定一般、または Ollama の補助機能だけを扱うとき
- Codex CLI 出力品質や LLM の応答内容そのものを検証したいとき

## hash
- 4903c028bb01578f54c6efb5981e484f3f12e94bf7c9fb94871aae6100143894

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
- Codex サブプロセス実行と apply 用プロセス追跡のテスト。専用 process group の記録、member pidfd によるシグナル送信、SIGTERM の遅延、leader 終了後や割り込み後の追跡保持、継承 tracking 環境変数の無視を検証する。

## Read this when
- Codex subprocess の process group 管理や apply abandon の cleanup 挙動を変更・検証するとき
- run_codex_subprocess または run_tracked_codex_subprocess の追跡・シグナル処理を確認するとき

## Do not read this when
- Codex subprocess の実装詳細ではなく、apply abandon の正本仕様を確認したいときは oracle 側の仕様を直接読む
- 対象が CLI 出力や別の subprocess 機能に限定されるとき

## hash
- 6fbaec44d70c3932f12b659e286f214d9b64ea297b9a60bb8cd3198020bc1549

# `test_codex_runtime_tui.py`

## Summary
- Codex TUI 実行の統合テスト。完成済み prompt の読み込み、アクセスモードと CLI 引数、作業ディレクトリ、call log、サブコマンドイベント、コンソール要約、CLI 不在・割り込み・非 0 終了時の失敗処理を検証する。

## Read this when
- Codex TUI の呼び出し仕様、prompt のアクセス境界、実行引数、ログ出力、終了コードや例外時の挙動を変更・調査するとき。
- TUI 実行の統合テストを追加・修正するとき。

## Do not read this when
- TUI 以外の Codex 実行経路や、Codex CLI の prompt 生成規則そのものだけを調査するときは、対応する実装・oracle test を直接読む。
- 一般的な Git 操作、設定モデル、または無関係なサブコマンドのテストを扱うとき。

## hash
- 1a9773f7f481161720601ea46a1dd7ac0547357ded25986187cd873ec7be3b4c

# `test_doctor_cli.py`

## Summary
- doctor preprocess の統合テスト。CLI と直接呼び出しを通じて、Git 状態・設定・refactor state・共有 doctor lock の lifecycle を検証する。
- 修復 commit が事前の staged/unstaged 変更、rename、`.cmoc/gu` の既存ローカルファイルを不適切に上書き・取り込みせず保持することも確認する。

## Read this when
- doctor preprocess の実装や外部契約を変更・レビューするとき
- doctor の Git 修復、config 生成・同期、linked worktree、lock 待機、index 保持に関するテストを追加・修正するとき

## Do not read this when
- doctor preprocess と無関係な CLI、設定、Git 操作の実装やテストを扱うとき
- doctor の正本仕様や実装責務を確認することが目的で、まず oracle 文書または実装本体を読むべきとき

## hash
- aac4d38ab98c24c3e3fe88510b2930d22ce950c11e935057c92047a06062bddc

# `test_editing_run_cli.py`

## Summary
- workload fork と共通 run join/abandon の統合 realization test。editing run の session state・run worktree・fork report・join/abandon lifecycle を対象とし、変更 path、rename 制約、apply/refactor fork、run join の merge・rollback・force-resolve、oracle investigation の起動条件を検証する。関連する lifecycle fixture と state 遷移を共有する統合テストの入口。

## Read this when
- editing run、realization apply/refactor fork、run join の lifecycle や session state を変更・調査するとき
- fork report、変更 path、rename、merge、rollback、force-resolve、割り込み処理の挙動を確認するとき
- run worktree と session branch 間の成果物統合や doctor/refactor state 同期を検証するとき

## Do not read this when
- 単一の実装関数や CLI 単体の挙動だけを確認する場合
- INDEX 生成処理そのものや oracle 文書の仕様だけを調査する場合は、対応する実装・oracle file を直接読む

## hash
- 6bcc5c7dc1d0ff90546b2ce0d844da969a45caa03440972f3388978632bc0198

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
- `commons.indexing` の INDEX.md エントリー生成・解析・更新とディレクトリ traversal を直接検証するテスト。入力検証、hash 再利用・不正エントリー再生成、空ディレクトリ、安定した兄弟順序、並列更新、cwd lock、memo・symlink・特殊ファイルの扱い、symlink 置換、linked worktree 間の lock 共有を扱う。CLI lifecycle から indexing の挙動を切り離して確認する入口。

## Read this when
- INDEX.md の render/parse/update_indexes の仕様や入力検証を変更・調査するとき
- INDEX 更新の traversal、並列実行、cwd lock、symlink、特殊ファイル、memo 除外の挙動を変更・調査するとき
- INDEX 更新に関する回帰テストを追加・修正するとき

## Do not read this when
- CLI lifecycle やサブコマンド全体の統合挙動を確認する場合
- INDEX entry の生成仕様そのものを確認する場合は、まず oracle の indexing 仕様・schema・entry standard を読む

## hash
- df66bf63ee43656c807a40fdebf51e8d5061e90bb16d97696223fb11c651ead7

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
- oracle review の finding loop を検証するテスト。対象 oracle ごとの finding 分離、main worktree のパス照合、challenger/advocate 間の理由引き継ぎ、割り込み時の部分結果保持、merge 応答の意味検証と再試行・失敗上限を、fake Codex callback と隔離 worktree で確認する。

## Read this when
- oracle review の finding 列挙・検証・判定 loop を変更またはレビューするとき
- oracle review の worktree、prompt、Structured Output、割り込み時状態、merge retry のテストを追加・修正するとき

## Do not read this when
- oracle review 以外のサブコマンドや finding loop と無関係なテストを扱うとき
- oracle review の実装詳細だけを確認したい場合は、まず対応する realization implementation と oracle 仕様を読むとき

## hash
- 7fd44528a6ab3fa927b89f0e7112ae8e7cab64c738892c0e9fd2ed608fe2c8ac

# `test_oracle_review_merge_operations.py`

## Summary
- oracle review の merge operation 適用処理を対象とするテスト。delete・replace・merge の kind 契約、finding 更新と採番、追加件数、不正な payload・対象・重複 target の拒否を検証する。

## Read this when
- oracle review の finding merge operation の契約や適用結果を変更・確認するとき
- apply_finding_merge_operations の入力検証、対象再利用防止、finding 生成をテストするとき

## Do not read this when
- oracle review の merge operation 以外の処理を変更・確認するとき
- 実装本体の責務や CLI 全体の仕様を確認するときは、まず対応する oracle 仕様または実装ファイルを読む

## hash
- eaa1dc20ee2f54edab5af2bf2d23511177ba13df99ac87b446831e01aaf747f8

# `test_oracle_review_report.py`

## Summary
- oracle review の report 生成と CLI 出力を検証するテスト。空・accepted/rejected・中断・処理失敗時の report 内容、finding の分類・件数・評価済み oracle 範囲、scope オプション、path alias や symlink の集計、Structured Output 呼び出しを確認する。

## Read this when
- oracle review の report 形式、finding の verdict 分類、エラー・中断時の出力、評価対象 oracle file の集計、または `oracle review` CLI の回帰テストを変更・調査するとき。

## Do not read this when
- oracle review の実装詳細そのものを変更・調査する場合は、まず対応する実装ファイルと oracle 仕様を読む。
- oracle review と無関係な CLI、report、oracle file 列挙の作業では、このテストを直接読む必要はない。

## hash
- 9c4057723901124f788038c4cc6ce15d7be9e6dcf8d7561b0ebda00259787788

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
- oracle review の worktree 分離、snapshot commit からの fork、未コミット差分の拒否、active editing run 中の実行可否を検証するテスト。
- review worktree で生成された INDEX.md のみを session に統合し、preflight 由来の INDEX.md、削除競合、入れ子の未追跡 INDEX.md を扱えることを確認する。
- INDEX.md 以外の差分を review worktree から統合せず、エラーとして報告することを検証する。

## Read this when
- oracle review の worktree 作成元、session branch、snapshot commit、worktree cleanup の挙動を変更・調査するとき。
- oracle review における INDEX.md の生成・統合・commit・merge conflict 解決を変更・調査するとき。
- oracle review が未コミット差分、非 INDEX.md 差分、active editing run をどう扱うか確認するとき。

## Do not read this when
- oracle review の実装詳細だけを確認したい場合は、対応する sub_commands の実装と oracle review 仕様を直接読む。
- 一般的な INDEX.md 生成規則や通常の indexing 処理だけを調査する場合は、indexing の仕様・実装・テストを直接読む。

## hash
- 66dd75b853341fc33dae7b95f2eec1d159f10170273d3399fc99da42d7c96d9b

# `test_packaged_import.py`

## Summary
- packaged layout 上での import 境界と公開 API を検証するテスト。oracle review/edit builder、ACP basic、cmoc config の実装を隔離環境から読み込み、パッケージ配置、prompt・schema・設定値、正本定義の再公開、公開 namespace を確認する。

## Read this when
- packaged layout での Python import が失敗する場合
- oracle review または oracle edit builder の prompt・schema・実行パラメータを変更する場合
- ACP basic の canonical 定義再公開や config の公開面を変更する場合
- setuptools の package discovery または package-dir 設定を変更する場合

## Do not read this when
- 単一の builder 内部処理や prompt 内容そのものを変更する場合は、まず対応する実装・oracle source・schema を直接読む
- packaged import、公開 API、setuptools 設定に関係しないテストや機能を変更する場合

## hash
- 276c9c30b57445950f6f3243de461281796d36a9a7d8278ef62adf1402e88a28

# `test_production_cli.py`

## Summary
- 実 Codex CLI と case-local Ollama を使う独立 process の本番経路受け入れ試験。全末端サブコマンドについて、終了 code、report・state・Git 状態、Codex call log、TUI の応答完了と終了操作を検証する。LLM の回答品質は判定対象外で、cmoc の制御と外部から観測できる副作用を確認する。

## Read this when
- 末端 CLI サブコマンドの本番経路、実 Codex 呼び出し、local Ollama 利用、状態遷移、Git・report・call log の検証を変更または調査するとき。
- TUI の PTY 操作、端末 capability query、応答完了後の終了処理を確認するとき。

## Do not read this when
- LLM の回答品質やプロンプト内容そのものを評価するとき。
- 単体の内部 helper や非本番経路だけを変更・調査するときは、対応する実装テストを直接読む。

## hash
- eaf3857b454c2e09befb1d89d2bf25bcad69656f3b71437cd1244c04930182a6

# `test_prompt_parts.py`

## Summary
- 標準 prompt parts と complete prompt の組み立て結果を検証するテストファイル。各 standard のタイトル・主要文言・出力内容、file access mode ごとの規則、complete prompt への標準文書の注入可否、root placeholder の保持、既定値での省略を確認する。prompt parts や complete prompt の挙動を変更・調査する際のテスト側の入口となる。

## Read this when
- prompt parts の本文・タイトル・主要規則を変更したとき
- complete prompt の標準文書注入、省略、root token 展開の挙動を変更・検証するとき
- file access mode、routing rule、index entry standard、oracle/realization standard のテストを確認するとき

## Do not read this when
- prompt の実装詳細だけを調査し、テスト期待値の変更が不要なとき
- このテストが対象とする標準文書や complete prompt と無関係な機能を変更するとき
- 具体的な standard の正本仕様を確認したいとき（対応する oracle source を直接読む）

## hash
- 1b9212587256b870f1375a0ac202ce570f593d22eafa867ae62059809c0b0530

# `test_runtime_cli.py`

## Summary
- CLI の error、log、preflight、completion 境界を検証するテスト。duration 表示、サブコマンドログの衝突・並列書き込み、doctor/pre-log 失敗時の記録、構造化 Markdown error 出力、CLI 解析エラー、scope 制約、work root 検証、completion の副作用抑制、起動 wrapper の失敗報告、.gitignore 更新、worktree ごとの doctor 対象を扱う。runtime CLI や error/logging 実装の挙動を変更・検証するときの入口。

## Read this when
- CLI のエラー出力、終了コード、stdout/stderr 境界を変更または検証するとき
- サブコマンドログ、doctor preflight、pre-log check の失敗処理を変更または検証するとき
- shell completion の preflight・副作用抑制や起動 wrapper の error report を変更または検証するとき
- cmoc の .gitignore 更新や worktree 対象 root の扱いを変更または検証するとき

## Do not read this when
- 個別サブコマンド固有の業務処理や indexing/oracle review/editing の内部ロジックだけを変更するときは、対応する実装・テストを直接読む
- CLI の出力や runtime の error/logging 境界に関係しないテストを調査するとき

## hash
- e65c0ee1deaef5d73e7e793ce610ce7bf80997a85ffdd71afa42067135adb814

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
- CmocConfig の既定値、JSON 形式のメンバー順、設定ファイル欠落時の案内、入力値の型・値検証、provider-local 設定の保持、永続化境界の検証をテストする realization test。設定モデルや config_from_dict・config_to_dict・load_config の挙動を変更・調査するときの入口。

## Read this when
- CmocConfig の既定値や論理 model class・reasoning effort の対応を確認するとき
- 設定の読み込み・JSON 化・provider 定義・model 定義・oracle_review の入力検証を変更または調査するとき
- 不正設定時の CmocError や、設定ファイル欠落時の doctor 案内を検証するとき
- provider-local の JSON/TOML 共通値や legacy FALV 設定の扱いを確認するとき

## Do not read this when
- 設定実装そのものの責務や正本仕様を確認する場合は、記載された oracle src・oracle doc を直接読むとき
- 設定以外のランタイム機能、CLI コマンド、モデル実行処理だけを変更・調査するとき
- CodexConfig 以外のテスト対象を確認するとき

## hash
- d825514c82911ad94fe09169dedec4a188e5df777f7c20e4a7aa9e2f3cdfd4ba

# `test_runtime_content.py`

## Summary
- `is_binary` が通常のテキスト内容と NUL バイトを含む内容を正しく判定することを検証するテスト。indexing における binary file 除外判定の挙動確認への入口。

## Read this when
- indexing の content 判定や binary file 除外処理を変更・検証するとき
- `is_binary` のテキスト／binary 判定に関するテストを確認するとき

## Do not read this when
- indexing の仕様根拠そのものを確認したいときは、参照先の oracle doc を直接読む
- `is_binary` の実装詳細を確認したいときは、実装モジュールを直接読む

## hash
- c6132bad711dc59ae537534245564ab610bea5f1cbf873635394d54ee99c8046

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
- realization refactor の永続 state について、oracle と realization の対象 file 集合、調査履歴の保持、変更 file の再調査化、target 選択優先順位、path escape・非正規 path・不正 timestamp の拒否を検証する pytest テスト。実装変更や state schema の検証を始める際の入口となる。

## Read this when
- refactor state の同期・読み込み・書き込み・target 選択規則を変更または調査するとき
- state の履歴保持、変更検知、調査優先順位、path や timestamp の入力検証を確認するとき

## Do not read this when
- refactor state 以外の runtime 機能を変更または調査するとき
- 正本仕様の詳細を確認することが目的で、oracle の仕様文書を直接読むべきとき

## hash
- c11606c83a00ea2a6520dcec63e98cb0a6c02622fe871aacaac4b3b6ab00350a

# `test_runtime_state.py`

## Summary
- session/run state の永続化 schema 検証と、managed branch からの session ID・state file 解決を検証する realization test。状態 payload の型・必須項目・未定義 field・run kind の拒否、session 部分の単独読み込み、state 書き込み時の検証、process 間で共有される session fork lock を扱う。

## Read this when
- session/run state の schema 検証や永続化のテストを変更・追加するとき
- session branch・run branch の解析、branch からの state 読み込み、session fork lock の挙動を確認するとき
- runtime state 実装の変更後に、異常系や process 間ロックの回帰を確認するとき

## Do not read this when
- runtime state の実装詳細そのものを変更・調査する場合は、対応する src の実装を先に読むとき
- CLI の一般的な入出力や、session state と無関係なテストを扱うとき

## hash
- 230615a6de84c403b6f62a62c9877daa6669d1cc56d86607634e506154c6021c

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
