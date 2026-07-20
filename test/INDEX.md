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
- Codex 実行ラッパー関連テストで共有する、最小の fake result・Codex home 初期化・parameter 生成・CLI 引数解析・override 固定化ヘルパーを定義する。runtime_codex_exec / runtime_codex_tui の subprocess 制御テストから利用される支援モジュール。

## Read this when
- Codex 実行ラッパーや TUI の subprocess argv、Structured Codex result、テスト用 CODEX_HOME、AgentCallParameter のテスト支援を変更・調査するとき。

## Do not read this when
- Codex 実行機能そのものの実装や oracle 仕様を確認するとき。直接 runtime 実装または対応する oracle file を読むべき場合。

## hash
- 2232754bf7a438d2e988596e3ddeb2ab54a9111a772f98d4ded4d92c4d86ac80

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
- 実経路統合テスト用に、case-local Ollama のインストール・モデル cache 検証、atomic publish、case working set の materialize、専用 process の起動・待機・終了を一括管理する補助モジュール。テスト設定を動的 port の Ollama provider に向ける入口も提供する。

## Read this when
- 実経路統合テストで Ollama を起動・停止したいとき
- Ollama の install cache、モデル cache、atomic publish、process isolation または cache lock の挙動を確認・変更するとき
- テスト用 CmocConfig を case-local Ollama に接続する方法を確認するとき

## Do not read this when
- 通常の Ollama provider 設定や本番実行経路を変更するとき
- Ollama を使わない単体テストや一般的なテスト fixture を扱うとき
- モデル実装や CLI の業務ロジック自体を確認するとき

## hash
- 25d79acd78960d4c8c899130aecfbab433d84d0c474bd6d842ee854444996691

# `test_acp_builder_editing_run_parameters.py`

## Summary
- editing run workload 向けの canonical builder adapter を検証するテスト。apply 用 builder が commit range と raw diff を prompt に埋め込み、適切なアクセスモードと schema 未指定を設定することを確認する。refactor 用 builder については、モデル設定・アクセスモード・canonical structured output schema・prompt 引数の反映を検証する。

## Read this when
- editing run の apply/refactor fork builder の parameter 生成や structured output schema の接続を変更・検証するとき
- builder が prompt に commit、diff、対象ファイルを反映する挙動を確認するとき

## Do not read this when
- builder 実装そのものの責務や prompt 組み立て規則を調べるとき
- editing run 以外のテストや、builder と無関係な CLI 挙動を調べるとき

## hash
- 1d99c0b1c51eb685149d6312b9df27c06d1961703169f29a063bd53f5f6a26b7

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
- oracle review ACP builder の parameter builder、schema、adapter 公開面に対する互換性テスト。モデル・推論・アクセス設定、schema 一致、placeholder 補正、動的入力保持、互換 module の公開 API を検証する。対応する正本は oracle/src/oracle/acp_builder/oracle/review/。

## Read this when
- oracle review の ACP builder や互換 adapter の挙動を変更・確認するとき
- review 用 parameter の schema、prompt placeholder、動的入力保持、公開 export を検証するとき

## Do not read this when
- review 以外の ACP builder を扱うとき
- 実装や正本 schema の詳細を直接確認する必要があり、対応する src または oracle を読むべきとき

## hash
- 3380468130016786cb49fc97bd2e3f3c112943c1d4deed0ba21d986a359aec8e

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
- Root/worktree と path model の runtime 契約を検証するテスト。placeholder path の解決、repo root と linked worktree の区別、cwd 変更の直列化、run worktree の作成・削除時における管理領域・branch・symlink・Git 登録状態の検証を扱う。

## Read this when
- path placeholder の解決や repo/worktree root の挙動を変更・調査するとき
- pushd の並列利用や process-global cwd の安全性を確認するとき
- run worktree の作成・削除に関するパス検証、symlink 防止、Git 登録確認を変更・調査するとき
- 対応する runtime 実装の契約をテストから確認するとき

## Do not read this when
- CLI の一般的な入出力や、path model・worktree runtime と無関係な機能を変更・調査するとき
- 具体的な実装詳細を確認する必要があり、対応する runtime 実装を直接読む方が適切なとき

## hash
- 1278a7d1b4fb9f2854bfedaca9903a9b46a9faef558f17c1a5c6f03d2fee7bf3

# `test_cli_command_tree.py`

## Summary
- Typer/Click で構築された公開 CLI の leaf コマンド集合を oracle 仕様と照合するテスト。`doctor`、`indexing`、`oracle`・`realization`・`run`・`session` 配下のコマンド、および `tui` を対象とする。CLI ヘルプが Typer/Click 互換性エラーなく描画され、主要なコマンド群を含むことも確認する。公開 CLI コマンドツリーの変更やヘルプ描画の検証が必要な場合の入口。

## Read this when
- 公開 CLI のコマンド追加・削除・階層変更を検証するとき
- Typer と Click の互換性や CLI ヘルプ描画を確認するとき

## Do not read this when
- 個別サブコマンドの処理内容や実行結果を確認したいとき
- CLI 以外の機能や内部実装のテストを調査するとき

## hash
- f390482771c9ef3f56a46c33a84d07f3b8e864ccd68974e924abd9b1c6b98006

# `test_cli_tui.py`

## Summary
- TUI 起動直前の CLI 前処理について、prompt editor 入力の衝突回避、編集済み prompt の解決、Codex TUI 起動パラメータ、linked worktree での保存先、`.cmoc` の ignore 挙動を外部挙動として検証するテスト群。TUI 起動実装や関連する preflight・prompt 編集・Codex 呼び出しの変更時に参照する。

## Read this when
- `tui` サブコマンドの起動前処理、prompt 編集・保存、parameter 解決、Codex TUI 起動の挙動を変更またはレビューするとき。
- linked worktree における complete prompt・schema・ログの保存先や `.gitignore` 更新を確認するとき。
- TUI 起動に関する回帰テストや、canonical builder と互換 adapter の関係を確認するとき。

## Do not read this when
- TUI 以外のサブコマンドの挙動だけを変更・調査するとき。
- TUI 起動後の画面操作や Codex 自体の出力品質を確認したいときは、まず対応する実装・oracle 仕様を直接読む。
- prompt editor や preflight の共通処理だけを調査し、TUI の外部フローを確認する必要がないとき。

## hash
- 0774c0c63f90fd213ac21da3a34d0b036aff0b0d70f9bf87a3ea6530be597d37

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
- Codex CLI 実行ランタイムの統合テスト。実際の Codex CLI と case-local Ollama を使った結合動作、Codex exec の argv・stdin・出力スキーマ・provider override、リポジトリ書き込み、CODEX_HOME 設定未生成を検証する。

## Read this when
- Codex exec の起動引数、sandbox・approval・model/provider override、prompt の stdin 渡しを変更または調査するとき
- Codex CLI 実行結果、出力スキーマの保存、call log、リポジトリ書き込み動作を検証するとき
- ローカル Ollama provider との統合や CODEX_HOME 設定ファイル未生成の挙動を確認するとき

## Do not read this when
- Codex 実行ランタイムの実装自体を変更する場合は、まず対応する src 側の runtime 実装と設定実装を直接読む
- Codex CLI と無関係なテスト、または単体の設定値・parser の挙動だけを調査するときは、この統合テストを読む必要はない

## hash
- 9d01f5ad14025a817d49a94e0af4f21a51bbabecda1b56b62df147fafc5af507

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
- doctor preprocess の統合テスト。CLI と直接呼び出しを通じて、Git 状態・config・refactor state・`.agents`・`.cmoc/gu` の修復、repair commit、lock 待機、linked worktree 対応を検証する。
- preprocess 実行前の staged index、unstaged hunk、rename、既存 staged deletion、既存 `.cmoc/gu` ファイルを保持・非追跡化する外部契約も検証する。
- doctor preprocess の挙動、修復対象、Git index 保全、共有 lock、config 同期を変更・レビュー・デバッグするときの統合テスト入口。

## Read this when
- doctor preprocess の外部挙動や lifecycle を確認するとき
- doctor による Git 修復 commit、config 生成・同期、`.cmoc/gu` の非追跡化を変更するとき
- linked worktree、共有 doctor lock、既存 staged/unstaged 差分の保持を検証するとき

## Do not read this when
- doctor preprocess の内部実装や正本仕様を確認する場合は、対応する `src` または `oracle/doc/app_spec` を先に読むとき
- doctor 以外の CLI サブコマンドや、単独の Git ヘルパー・CLI 実行ヘルパーを変更・検証するとき

## hash
- 51f7c052a60ed2ddf2b0d8caf3725e3cd75eadc2e784fe155b8559a3a4a5b80c

# `test_editing_run_cli.py`

## Summary
- workload fork と run join/abandon に関する統合 realization test。realization apply fork、refactor fork、run join の状態共有・差分解決・マージ失敗時ロールバック・割り込み復旧を検証する。oracle investigation のセッション前提や refactor 中の INDEX 更新・再レビューも確認する。関連する run lifecycle、fork、refactor、INDEX 更新の挙動を横断して検証する入口。

## Read this when
- realization apply fork または refactor fork の統合フローを変更・調査するとき
- run join の状態遷移、force-resolve、マージ失敗時ロールバック、再実行を変更・調査するとき
- refactor fork の永続サイクル、割り込み復旧、変更ファイルの INDEX 再更新を確認するとき
- oracle investigation のセッション前提や AgentCallParameter のアクセスモードを変更するとき

## Do not read this when
- 単一の lifecycle helper や fork 実装の内部ロジックだけを変更し、その外部統合挙動を確認する必要がないとき
- CLI の一般的な起動・doctor・session fork のみを調査するとき
- INDEX 更新処理そのものの単体仕様を確認するときは、対応する実装・単体テストを直接読む

## hash
- 0229d64386e71c34fc389b5156eaf51694465d086d491f66dbd195b6abc38f22

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
- Codex 呼び出し直前の indexing preflight を検証する pytest テスト群。通常の exec/TUI 経路での実行順序、linked worktree の選択、repository lock 待機、パラメータによる無効化、file access violation 後の recovery indexing 禁止を、git 状態や外部 Codex の fake を用いて確認する。

## Read this when
- indexing preflight の実行条件・順序・対象 worktree・lock 待機を変更またはレビューするとき
- Codex exec/TUI 経路と indexing の連携テストを追加・修正するとき
- file access violation 時に recovery 処理を実行しない制約を確認するとき

## Do not read this when
- INDEX.md の生成ロジック自体や indexing 実装の詳細を調べるときは、commons.indexing の実装・専用テストを直接読む
- Codex 呼び出し全般の仕様や runtime 実装だけを調べるときは、codex preflight 実装を直接読む

## hash
- ae1a286ddd5014f7dd47268fc42f7df5e0f8ba69c10175d5860fc11c1c48c126

# `test_oracle_edit_cli.py`

## Summary
- `cmoc oracle edit` の main worktree TUI 制御を検証するテスト。編集前提条件、indexing preflight・clean worktree 検査・TUI 呼び出し順、AgentCallParameter、編集結果、失敗時の終了コード、session state 非変更を確認する。

## Read this when
- `oracle edit` CLI の起動条件や main worktree 制約を変更・調査するとき
- oracle 編集 TUI の呼び出しパラメータ、前処理順序、失敗時挙動を変更・検証するとき
- oracle edit 実行後の変更保持や session/run lifecycle 非干渉を確認するとき

## Do not read this when
- oracle edit 以外のサブコマンドの挙動を調査するとき
- 実装詳細ではなく oracle 編集仕様そのものを確認するときは、対応する oracle 文書や `sub_commands/oracle/edit` の実装を先に読む

## hash
- 665369f15bc0f7fd223d10da1e2f77caca288d50fe2db85d1259ba6857a998c2

# `test_oracle_review_loop.py`

## Summary
- oracle review の finding loop を検証するテスト群。対象 oracle ごとの finding 絞り込み、worktree 実行コンテキスト、challenger/advocate の reason 連携、割り込み時の部分結果保持、merge response の意味検証と再試行・失敗を確認する。

## Read this when
- oracle review の finding 列挙・検証・judge・merge loop の挙動を変更または調査するとき
- oracle review の worktree 分離、finding path の関連付け、割り込み時の結果保持を確認するとき
- merge の意味的な不正 response に対する再試行条件や上限を確認するとき

## Do not read this when
- oracle review の実装詳細ではなく、正本仕様そのものを確認したいときは oracle/doc/app_spec/sub_command/oracle_review.md を読む
- Codex 実行や Structured Output の一般規則だけを確認したいときは oracle/doc/app_spec/codex_exec_rule.md を直接読む
- finding loop と無関係なサブコマンドやテストの挙動を調査するとき

## hash
- 394574d8cff57158e33461e3fc952a467746b59691c50a8c024c8a1fd807243b

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
- oracle review の report 生成と CLI 出力を検証するテスト。レビュー中断・処理失敗時の report、所見の accepted/rejected 分類、severity 別集計、oracle path alias・symlink の扱い、scope option、Structured Output schema 呼び出し、エラーメッセージやログを確認する。

## Read this when
- oracle review サブコマンドの report 形式、所見判定、レビュー中断・失敗時の挙動を変更または調査するとき
- oracle review の CLI option、Structured Output callback、完了済み oracle の集計を変更または検証するとき
- oracle review の report 出力テストを追加・修正するとき

## Do not read this when
- oracle review 以外のサブコマンドや report の実装を扱うとき
- CLI 共通 runner、git fixture、設定定義そのものを直接変更・調査するときは、それぞれの実装・テストを先に読む

## hash
- 28a96f53f60518457cd69a7d10c5f06e088a4830038456d193a8abb4bba27e53

# `test_oracle_review_targets.py`

## Summary
- oracle review の対象パス解決と対象列挙を検証するテスト。finding path の placeholder・絶対パス・symlink 処理、oracle 配下の追跡状態や除外規則、session/full scope の対象数とレポート、review fork 基準の差分を扱う。oracle review の対象選定ロジック変更時に確認する入口となる。

## Read this when
- oracle review の finding path 解決や oracle file 列挙を変更・調査するとき
- session/full scope、追跡済み ignored file、symlink、AGENTS.md・INDEX.md の除外挙動を確認するとき

## Do not read this when
- oracle review のレポート本文生成や finding 内容の判定だけを変更するとき
- 対象列挙・パス解決と無関係な CLI コマンドや共通テスト支援を変更するとき

## hash
- 81f7c2e30158c0e470deb0eaee4253e9ac068a527feb0492405bf34490b9aabc

# `test_oracle_review_worktree.py`

## Summary
- oracle review の worktree 分離、session branch の snapshot 起点、未コミット差分の拒否、INDEX.md のみの統合と競合解決を検証するテスト。oracle review の実行経路や INDEX 更新の統合挙動を確認するための realization test。

## Read this when
- oracle review が対象 worktree・branch・oracle を正しく選ぶか確認するとき
- review 実行後に INDEX.md だけを session 側へ統合する処理、preflight の INDEX 更新、merge conflict 解決を変更・検証するとき
- review worktree に INDEX.md 以外の変更を許可しない制御を確認するとき

## Do not read this when
- oracle review の実装詳細ではなく、通常の INDEX.md 生成規則だけを確認したいときは indexing の oracle doc を直接読む
- session fork や run isolation の一般仕様だけを確認したいときは対応する oracle doc を直接読む
- oracle review と無関係な CLI サブコマンドやテストを変更・調査するとき

## hash
- 61d7fa994f2e4af81afbd80e4fbec21cb3487ffe5a55b0aacbcb7b95a8733e07

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
- 実 Codex CLI と case-local Ollama を用い、全末端サブコマンドを独立 process または PTY 上の本番経路で検証する受け入れテスト。CLI 終了 code、report・state・Git・Codex call log、TUI の応答完了と終了操作を確認し、LLM の回答品質自体は判定しない。

## Read this when
- 全末端サブコマンドの本番経路、独立 process 実行、実 Codex provider 呼び出し、状態遷移、Git 副作用、call log を検証・変更するとき。
- Codex TUI の PTY harness、端末 capability query、応答完了後の終了操作を調査するとき。

## Do not read this when
- 単一サブコマンドの内部実装や通常の単体テストだけを変更・調査するとき。
- LLM の回答品質や prompt 内容そのものを評価するとき。

## hash
- b15f30598d113fd2442a5f525ea32cc6c7ea60ff68c102db077761d4bfd9bbd0

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
- CLI の実行境界と runtime 共通処理を外部挙動から検証するテスト。duration・サブコマンドログ・並列イベント記録、CmocError の Markdown 出力、stdout/stderr、CLI 引数解析、work root 制約、completion probe、preflight、gitignore 更新、worktree 単位の doctor 処理を扱う。runtime CLI・logging・error handling・completion・doctor・関連サブコマンド仕様の実装変更や回帰調査におけるテスト入口。

## Read this when
- CLI のエラー報告、終了コード、stdout/stderr 出力、引数解析を変更または調査するとき
- サブコマンドログ、並列 logger、quota wait、duration 表示を変更または調査するとき
- completion probe、work root 制約、preflight/doctor の副作用や失敗時処理を変更または調査するとき
- cmoc の gitignore 更新、worktree 対応、関連する CLI 境界の回帰を検証するとき

## Do not read this when
- CLI runtime の実装詳細を確認するだけなら、まず対応する src の runtime CLI・logging・error handling 実装を読むとき
- 個別サブコマンドの内部ロジックや oracle/indexing の仕様だけを確認し、CLI 境界・共通 runtime 挙動を扱わないとき
- completion や doctor の仕様本文を確認する必要があるときは、対応する oracle doc を直接読むとき

## hash
- 785f2ff1a888d5e6374d1ffa8f3a9c1d26322e39cd385f4c1edd9d4a07304232

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
- Codex argv の model、sandbox、provider 上書き契約を検証するテスト。全 FileAccessMode の sandbox 変換、承認・model・reasoning 設定、未知 mode や未定義 provider の拒否、汎用 provider 設定の TOML argv 変換を扱う。

## Read this when
- Codex 起動時の override argv、sandbox 対応、model/provider 設定の変換や検証を変更・調査するとき。
- FileAccessMode と Codex sandbox の対応、provider の選択・転送・欠落時エラーを確認するとき。

## Do not read this when
- Codex argv の override や model/provider lifecycle に関係しない機能を変更・調査するとき。
- Codex 実行処理そのものではなく、別の CLI 入出力や設定読み込みだけを確認するとき。

## hash
- f11cc9b305c7c8070a55ffe713ae19988cd2a6eee2a58d548801fbee625040f0

# `test_runtime_config.py`

## Summary
- CmocConfig の既定値、JSON 化時のメンバー順、設定ファイル読み込み、入力検証、provider-local 設定値の保持・拒否、recovery 試行回数を検証するテスト。ランタイム設定の挙動や設定エラーを確認する際の入口。

## Read this when
- CmocConfig の既定値や設定の永続化形式を変更・確認するとき
- codex、oracle_review、model provider、reasoning effort の入力検証を変更・確認するとき
- 設定ファイル欠落時や不正値のエラー挙動を変更・確認するとき

## Do not read this when
- 設定実装そのものを調査するときは、対応する runtime/config 実装と oracle の設定仕様を直接読む
- 設定以外の CLI 動作、oracle review 処理、一般的なテスト基盤を調査するとき

## hash
- 30520fe82d8308e91f103ff23937d1215bba93e5bde8376a667f0b18768c9e23

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
- realization refactor の永続 state について、oracle・realization 対象集合との同期、調査履歴の保持、変更ファイルの再調査化、調査対象の優先選択、パス逸脱の拒否を検証するテスト。runtime_refactor の state 管理・対象選択実装を変更または検証する際の入口。

## Read this when
- refactor state の同期や読み書き、調査履歴の更新規則を変更・検証するとき
- 未調査対象や最古の調査対象を選ぶ優先順位を変更・検証するとき
- refactor state におけるパス逸脱などの不正入力処理を変更・検証するとき

## Do not read this when
- runtime_refactor の実装詳細を直接変更・調査する場合は、まず対応する実装ファイルを読むとき
- refactor state と無関係な CLI 機能やテストを扱うとき

## hash
- 9be17fbe6f0e1d3b704f7ba152cf8595674ecb695314d803d247b3a4ebd9a135

# `test_runtime_state.py`

## Summary
- session/run state schema の不正入力検証と managed branch からの state/session 読み込みを検証する realization test。状態値・payload・run kind・未知 field の拒否、run branch の session ID 解決、run section を限定的に検証する session 読み込みを扱う。
- session fork lock がプロセス間・スレッド間で共有され、排他されることも検証する。

## Read this when
- session/run state の schema 検証や JSON 復元処理を変更・レビューするとき
- managed branch の session ID 解析、branch からの state 読み込み、session 部分読み込みを変更・レビューするとき
- session fork lock のプロセス間排他を変更・レビューするとき
- これらの挙動に関するテストケースや失敗条件を確認するとき

## Do not read this when
- CLI 出力、oracle file、実装本体以外のテストを確認したいとき
- session/run state や managed branch 解析の実装詳細を確認したい場合は、まず対応する realization implementation を読むとき

## hash
- 7c04a4207948a053c72fc4182779904eeec7176497341266ac166b5a0099a118

# `test_session_cli.py`

## Summary
- session fork/join/abandon の CLI 外部挙動を、実リポジトリと linked worktree の両方で検証する回帰テスト。session branch・state の生成、更新、cleanup、rollback、衝突解消、事前処理、dirty worktree 拒否、エラー出力、Codex 実行境界を扱う。
- session ライフサイクルと state 遷移に関する実装変更や、fork・join・abandon の失敗時挙動、linked worktree 対応、oracle conflict resolution の検証入口となる。

## Read this when
- session fork、join、abandon の CLI 挙動を変更・レビュー・デバッグするとき
- session state の生成・cleanup・rollback、branch 操作、linked worktree 対応を確認するとき
- session join の conflict resolution、Codex sandbox、repo root/cwd、エラー出力を確認するとき
- session CLI 回帰テストや関連する oracle 仕様の検証範囲を把握するとき

## Do not read this when
- session CLI と無関係なサブコマンドや、session state を参照しない機能を扱うとき
- session の内部実装詳細だけを確認する場合は、まず対応する realization implementation または oracle file を直接読むとき
- Codex 共通実行規則や state schema の正本仕様だけを確認する場合は、対応する oracle document/source を直接読むとき

## hash
- 513c377b882f2fd92fbf965c33eacafa754450ed5a7657a93688b336233445c4

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
