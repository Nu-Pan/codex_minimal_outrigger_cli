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

# `_apply_support.py`

## Summary
- apply session state の apply_branch を検証し、管理対象 worktree のパスを組み立てるテスト用補助関数。セッション状態から production worktree を解決する処理の入口。

## Read this when
- apply session state から managed worktree のパスを導出する処理や、その入力検証を確認するとき。

## Do not read this when
- session state の仕様自体を確認するときは、参照される oracle 文書を直接読む。
- worktree 解決以外のテスト支援処理を確認するとき。

## hash
- ad8de2962ec0f4ac6ed391bc83eabcb7ba5cfac37c0930ea94394610f36e4d82

# `_cli_support.py`

## Summary
- Typer CLI テストで共有する CliRunner インスタンスを提供する補助モジュール。CLI テストの実行入口として参照する。

## Read this when
- Typer CLI のテストを追加・修正し、CliRunner を使った実行が必要なとき

## Do not read this when
- CLI テスト以外の実装やテストを扱うとき
- CliRunner を使わないテストの挙動を確認するとき

## hash
- f8067659d5647e5eb7180b42c0741136aba6b2baf99cf70dd459a35da30d4d12

# `_codex_support.py`

## Summary
- Codex 実行ラッパーのテストで共有する補助関数と最小 fake result を定義する。認証済み Codex home、managed Ollama preflight の無効化、既定パラメータ生成、CLI 引数・設定 override の検査、Codex override argv の固定化を提供するテスト用入口。

## Read this when
- Codex subprocess の argv 構築、config override、cwd・file access mode、runtime wrapper のテストを追加・変更するとき。
- Codex 実行テストで一時的な CODEX_HOME や共有 service の stub が必要なとき。

## Do not read this when
- Codex 実行ラッパーの本体実装や正本仕様を確認する作業。
- Codex と無関係なテスト、またはこの共有テスト helper を利用しないテスト。

## hash
- 14ff0ed40e6128820d06b4dd110ed96418d5a2ac73f2d1e88a80e678487c39d9

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
- doctor テストから共有の managed Ollama service を利用するための共通定数・実行 helper。指定 root を cwd にして CLI の doctor を呼び出し、成功結果を返す。

## Read this when
- managed Ollama を使う doctor テストを追加・修正するとき
- doctor 実行時の worktree 指定、production service、固定 endpoint、テスト用モデルの扱いを確認するとき

## Do not read this when
- doctor コマンド自体の実装や仕様を確認するときは、doctor の実装・oracle spec を直接読む
- fake service lifecycle や Ollama service の起動・停止処理を変更するとき

## hash
- 142e4d277c91d98d33dec1ec0fcad02b1118bd3a681727a41753c016980684ed

# `test_acp_builder_apply_parameters.py`

## Summary
- apply fork ACP builder の parameter、prompt、root、file access mode、および oracle schema 参照・適合性を検証する pytest。apply fork builder の import 契約と packaged layout も確認する。

## Read this when
- apply fork の change summary または file review and fix parameter を変更・検証するとき
- apply fork の prompt、root token、realization_write 制約、モデル設定を確認するとき
- 対応する oracle schema との整合性や builder の packaged layout import を調査するとき

## Do not read this when
- apply fork 以外の ACP builder の挙動だけを調査するとき
- 実装や正本 schema の詳細を直接確認する必要があり、対応する builder・oracle schema を読む方が適切なとき
- 単に一般的な pytest 実行方法や共通テスト基盤を確認したいとき

## hash
- 997305818e7538b3206fbcbd3cb960d2d4ed4067024ce110ebfb76dcb7d972c0

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

# `test_acp_builder_review_oracle_parameters.py`

## Summary
- review oracle ACP builder の parameter builder、JSON Schema、互換公開面を検証するテストファイル。enumerate、judge、merge、advocate/challenger validation のモデル設定・ファイルアクセス・prompt placeholder・動的入力保持・schema 整合性を確認し、review oracle 実装の回帰検証の入口となる。

## Read this when
- review oracle の ACP builder、parameter、structured output schema、prompt placeholder、互換 module の公開 API を変更または調査するとき
- review oracle の builder が oracle source の schema や canonical builder と一致するか確認するとき
- symlink path や動的 finding テキストの保持など、review prompt の path/input 変換を検証するとき

## Do not read this when
- review oracle 以外の ACP builder の実装やテストを扱うとき
- oracle source の仕様そのものを確認したいときは、対応する oracle 配下の実装・schema を直接読む
- 一般的な review 処理や finding の業務ロジックを調査するとき

## hash
- 6c6aa47f3f11ee247a13c73c79810235bb101aacba2fe1f189301dbd70c74178

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
- TUI の resolve parameter builder と関連 schema を検証するテスト。元の prompt および標準ルールが生成 prompt に埋め込まれること、モデル・推論・アクセスモード・schema path が適切であることを確認する。
- schema の必須項目、追加プロパティ禁止、logical enum 値、boolean flag の構造を検証する。
- 互換 module の公開 API が必要な名前だけを提供し、旧 renderer を公開しないことを確認する。

## Read this when
- TUI resolve parameter の prompt 埋め込み、出力 parameter、structured-output schema、または module の公開 API を変更・検証するとき。

## Do not read this when
- TUI 以外の builder や、resolve parameter と無関係な CLI/TUI 動作を調査するとき。

## hash
- 232eb1d17ac4317f19df655b083f411b4ba54e3add76a732b4c86bdb139b2b6f

# `test_apply_abandon_cli.py`

## Summary
- `apply abandon` CLI の外部挙動を検証するテスト。worktree・branch・state の cleanup、実行位置の切り替え、tracked process の停止、警告・失敗条件を扱う。低レベル process helper の契約は対象外で、`test_runtime_apply.py` が入口となる。

## Read this when
- `apply abandon` の成功時 cleanup や警告出力を変更・検証するとき
- apply process の停止順序、実行中 state の扱い、process identity 欠落時の失敗を確認するとき
- repo root・linked session worktree・apply worktree からの実行位置に関する挙動を確認するとき
- 不正な apply branch、別 session の branch、stale branch、linked session の dirty 状態に対する拒否条件を確認するとき

## Do not read this when
- 低レベルな process helper 自体の契約や実装を確認するときは `test_runtime_apply.py` を直接読む
- `apply abandon` 以外の apply サブコマンドの挙動だけを確認するとき
- CLI 外部挙動ではなく、oracle の一般的な realization 方針を確認するときは参照されている oracle file を直接読む

## hash
- a5cc9797dc823424804cb06fac7b1605d60ebe3772374af9311f8470ea611661

# `test_apply_fork_cli.py`

## Summary
- `apply fork` CLI の回帰テスト群。Codex loop、apply state・branch・worktree のライフサイクル、割り込み・初期化失敗からの復旧、doctor 前処理、gitignore 更新、設定エラー、linked worktree 起点などの外部挙動を検証する。apply fork の実装や仕様変更時に、同一 fixture を共有する lifecycle シナリオ全体の回帰確認へ進む入口となる。

## Read this when
- `apply fork` の state、branch、worktree、report、PID 管理を変更または調査するとき
- apply fork の割り込み、設定エラー、初期化失敗、abandon 復旧の挙動を確認するとき
- doctor 前処理や gitignore の自動修正が apply fork に与える影響を検証するとき
- linked worktree からの apply fork 開始や snapshot 起点を確認するとき

## Do not read this when
- 対象正規化の仕様やテストだけを確認したいときは、独立した対象正規化テストを直接読む
- apply fork の実装責務や実行順序の正本仕様を確認したいときは、指定された apply fork の oracle 文書を直接読む
- apply fork と無関係な CLI、session、設定、worktree 機能を調査するとき

## hash
- 700d3313fb7916ef7a320ce7e3dd7d5b16b40d7b379e847668f2a927c7be759a

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 統合テスト。レビュー・修正ループの収束／未収束／エラー、変更ファイルの再検査、report 生成、変更要約、commit、session state 更新、rolling fork の対象範囲を検証する。

## Read this when
- apply fork の終了状態、所見ループ、変更ファイル再検査、report 内容を変更・調査するとき
- apply fork の未追跡・削除済みファイルを含む変更要約や fallback 挙動を確認するとき
- rolling apply fork が前回 join 後の変更だけを対象にする制御を確認するとき

## Do not read this when
- apply fork の内部実装そのものを変更する場合は、まず対応する src の実装と oracle file を読むとき
- apply fork report 以外の CLI コマンドや一般的な session fork の挙動だけを調査するとき
- Codex CLI や LLM の出力品質自体を検証するテストを探しているとき

## hash
- ba1beda9c3af63714cad3d740f030aeedfdbf7df9756c836c466ba01a5c19e2c

# `test_apply_fork_target_normalization.py`

## Summary
- apply fork の対象 file 正規化を検証する回帰テスト。root 直下 memo や管理用 path、未追跡 ignored file を除外し、入れ子の memo、binary file、tracked ignored file、symlink を repository path に基づいて正しく扱う挙動を確認する。

## Read this when
- apply fork の対象 file 判定・正規化・重複排除を変更または調査するとき
- oracle、realization、memo、管理用ディレクトリ、git ignore、symlink の対象分類に関する回帰を確認するとき

## Do not read this when
- apply fork の対象正規化や分類を扱わず、他の apply fork 処理だけを変更・調査するとき
- 対象 file の分類仕様そのものを確認したい場合。対応する oracle 文書・ソースを直接読むべき

## hash
- 8a09d494abb8f29892f6a3333ec796b3ceb5e149cf99d5ef51c10982c7c2a254

# `test_apply_join_cli.py`

## Summary
- apply join の CLI 結合処理を、成功条件・後片付け・state/report 更新・異常検出・競合処理まで含む統合テストで検証する。

## Read this when
- apply join の実装、仕様、テストを変更・調査するとき
- apply worktree や branch の cleanup、session への merge、state 更新、report 生成の挙動を確認するとき
- dirty worktree、想定外差分、symlink、rename/delete、merge conflict、force-resolve の扱いを確認するとき

## Do not read this when
- apply fork や apply join 以外のサブコマンドだけを調査するとき
- apply join の内部実装ではなく、個別の共通テストヘルパーを直接確認すべきとき

## hash
- 0fe4aaee90ee2140a830bbe14c0772f656b98a3d7b0279bebbb6d4ca7924dfc6

# `test_basic_runtime.py`

## Summary
- Root/worktree と path model の runtime 契約を検証するテスト。root placeholder の解決、repo root と linked worktree の区別、並列 pushd の cwd 直列化、run worktree の作成・削除時における管理領域・branch・Git 登録・symlink 制約を扱う。

## Read this when
- path model の placeholder 解決や repo/worktree root の挙動を確認・変更するとき
- pushd の process-global な cwd 保護を確認・変更するとき
- run worktree の作成・削除に関する安全性検証やテストを追加するとき

## Do not read this when
- CLI コマンドの一般的な実行フローや、path model・worktree runtime と無関係な機能を変更するとき
- 実装の詳細を直接確認したい場合は、根拠として示された oracle file と対応する runtime 実装を先に読むとき

## hash
- 7cd1d1118ec850cc289b1287b657aaa74e923fe32a08822098a9282ac9a0e378

# `test_cli_tui.py`

## Summary
- TUI 起動直前の CLI 前処理を外部挙動から検証するテスト。編集済みプロンプトの解決、Codex パラメータ、ログ・ignore 配置、既定値、linked worktree での保存先を扱う。TUI サブコマンドの前処理や関連テストを確認する入口。

## Read this when
- TUI サブコマンドの前処理・プロンプト編集・Codex 起動連携を変更またはレビューするとき
- TUI のログ保存先、ignore 設定、linked worktree 対応、ファイルアクセス既定値の挙動を確認するとき
- TUI 起動に関する外部挙動の回帰テストを追加・修正するとき

## Do not read this when
- TUI の内部実装を直接変更・調査する場合は、まず TUI サブコマンド実装と正本仕様を読むとき
- TUI と無関係な CLI サブコマンド、共通ライブラリ、または Codex 出力品質だけを調査するとき

## hash
- ffd4116cbf2131c02c6f5795cc4939c79297106b9ad9d0df19b954ce9bb60478

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
- Codex CLI 実行ランタイムの結合・契約テスト。実 Codex またはスタブ Codex に対する argv、stdin、sandbox、approval、override 設定、ローカル SLM 用 managed Ollama provider、出力スキーマ、ログ、CODEX_HOME 非変更、リポジトリ書き込み結果を検証する。

## Read this when
- Codex exec の呼び出し契約、override 引数、ローカル SLM / managed Ollama 連携を変更または調査するとき。
- Codex 実行結果、出力スキーマ配置、プロンプトログ、CODEX_HOME の副作用を検証するとき。

## Do not read this when
- Codex 実行ランタイムの挙動やテスト契約を扱わず、他の CLI 機能・設定・テストだけを変更または調査するとき。
- 単体の補助関数の内部実装を確認するだけで、Codex exec の外部契約を確認する必要がないとき。

## hash
- 7810bcd202e133caeaf3feb8cb249161c595f6f7c981bcaa337292bf7061256d

# `test_codex_runtime_home.py`

## Summary
- Codex 実行時の CODEX_HOME 解決・引き継ぎと、Codex 起動前の home/auth.json 検証を確認する pytest。Codex subprocess が正しい環境・作業ディレクトリで呼ばれること、および不正な認証環境を事前に拒否して起動しないことを検証する。

## Read this when
- run_codex_exec の CODEX_HOME、認証情報、preflight validation、または Codex subprocess 起動条件を変更・調査するとき
- Codex 実行失敗時の CmocError 内容や、相対 CODEX_HOME の解決基準を確認するとき

## Do not read this when
- Codex 実行環境や home 検証に関係しない CLI 機能・テストを変更するとき
- 実装の詳細ではなく、Codex 実行全体の仕様を確認したい場合は、対応する oracle doc を先に読む

## hash
- 841e4926e3a25131ea850d93bdfc16acb9bed4e8de82c492b8ad95a4d4161964

# `test_codex_runtime_paths.py`

## Summary
- Codex 実行時のパスと sandbox 境界を検証するテスト。並列実行時のログパス予約、cwd の選択、リンク worktree における schema 保存先、PURE_ORACLE_READ の read-only sandbox、`.agents` パスを権限設定へ注入しないことを扱う。

## Read this when
- `run_codex_exec` の cwd、ログ・出力・schema の保存先、sandbox 引数、並列実行時のパス衝突回避を変更・検証するとき。

## Do not read this when
- Codex 実行パス以外のプロンプト生成、設定、CLI 動作を調査するとき。sandbox 変換の単体ロジックだけを確認する場合は、対応する実装・oracle file を直接読む。

## hash
- 1c68ace616ef78a31fd6db76c9787cb1cf9d111ea166a926e7fb00849dc502a0

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex quota exceeded 後の quota probe・待機・resume・再実行を検証する回帰テスト群。resume token の復元、代表 probe の共有、並行呼び出し、失敗伝播、poll 上限、ログ・出力・CODEX_HOME・cwd の観測可能な挙動を扱う。Codex exec の quota 復帰制御に関するテストの入口。

## Read this when
- Codex quota exceeded 後の待機、quota availability probe、resume または prompt 再実行の挙動を変更・調査するとき
- quota 復帰処理の並行実行、probe 失敗、KeyboardInterrupt、poll 上限、状態解除を検証するとき
- Codex 呼び出しログ、subcommand log、resume token、CODEX_HOME、cwd の回帰を確認するとき

## Do not read this when
- quota 復帰制御や Codex runtime のテスト対象ではなく、通常の Codex exec 実行仕様だけを確認するとき
- quota probe の実装そのものを変更・調査する場合は、まず対応する実装モジュールと正本仕様を読むとき

## hash
- 2970fe3aba0cf7fdfbf11d69eade3439e847e4a5c7181c3436deef02c0fb5ce9

# `test_codex_runtime_retry.py`

## Summary
- Codex exec の retry と失敗時ログを検証するテスト。Structured Output の意味的失敗・解析失敗、capacity retry、未知の JSONL error、中断、agent diff 保持、stdout JSONL 外のエラーマーカー、retry 上限と backoff を、最終結果・subprocess 呼び出し回数・call log・subcommand event の外部挙動として確認する。

## Read this when
- Codex exec の retry 条件、失敗分類、retry 上限や backoff を変更・調査するとき
- Codex exec の call log、subcommand event、失敗時コンソール出力を変更・調査するとき
- Structured Output の検証失敗、JSONL error、中断、capacity failure の挙動を確認するとき

## Do not read this when
- Codex exec の retry や失敗時ログに関係しない機能を変更・調査するとき
- Codex exec の通常成功時の引数構築や出力変換だけを確認するときは、まず対応する実装・仕様を直接読む

## hash
- e872132d06a77346516caa6a6c6f6319d1cbb4006a7cecb59aeea97387a696dd

# `test_codex_runtime_subprocess.py`

## Summary
- Codex サブプロセス実行と apply 用プロセス追跡の挙動を検証するテスト。専用 process group の記録、member pidfd によるシグナル送信、SIGTERM の遅延、leader 終了後や割り込み後の tracking 保持、継承 tracking 環境変数の無視を扱う。runtime の subprocess 制御実装を確認・変更する際のテスト入口。

## Read this when
- Codex subprocess の起動・終了・シグナル処理や apply tracking を変更するとき
- プロセスグループ、pidfd、SIGTERM、KeyboardInterrupt、環境変数継承に関する不具合を調査するとき
- commons.runtime_codex_profile の実装変更後に対応する外部挙動を検証するとき

## Do not read this when
- Codex subprocess や apply tracking と無関係な CLI 機能を変更・調査するとき
- テスト対象の実装詳細ではなく、別のサブコマンド固有の入出力だけを確認するとき

## hash
- 6df388bf8a7ca92bd23b1f2672d01af4d38b2d6e2779a3eedb77dd2a34c380f7

# `test_codex_runtime_tui.py`

## Summary
- Codex TUI 実行ランタイムの統合テスト。prompt 読み込み、ファイルアクセスモード、Codex CLI 引数、作業ディレクトリ、call log、サブコマンドイベント、コンソール要約、終了コード、CLI 不在・割り込み・非 0 終了時の失敗処理を検証する。Codex 呼び出しやログ仕様に関する実装変更・テスト追加の入口となる。

## Read this when
- Codex TUI 実行、Codex CLI の引数や sandbox 設定、prompt のアクセス境界を変更・レビューするとき
- Codex 呼び出しの成功・失敗ログ、終了コード、コンソール出力の挙動を変更・検証するとき
- TUI call log の保存、timestamp 衝突回避、サブコマンドイベント記録を調査するとき

## Do not read this when
- TUI 以外の Codex 実行経路だけを変更・調査するとき
- prompt 生成仕様そのものを確認する場合は oracle の prompt 仕様を直接読むとき
- 一般的な Git 操作、設定読み込み、または TUI と無関係なテストを扱うとき

## hash
- a173eaad0fbac41ecd8fc0abe233b2f27fd0af962bc7db97945acd03427bd9cf

# `test_doctor_cli.py`

## Summary
- doctor preprocess の統合テスト。CLI と直接呼び出しの両方で、config・Git 状態・linked worktree・共有 lock・managed Ollama の修復 lifecycle と、既存 Git index の staged/unstaged 変更保持を検証する。doctor の外部契約を一体的に確認するテスト入口。

## Read this when
- doctor または互換 alias `dector` の挙動を変更・調査するとき
- doctor preprocess の config 生成・同期、Git 修復 commit、ignore、tracked/untracked 状態を確認するとき
- linked worktree、共有 doctor lock、managed Ollama の model/service 準備を変更・検証するとき
- 既存の staged 変更、unstaged 差分、rename、削除を doctor が保持する契約を確認するとき

## Do not read this when
- doctor preprocess と無関係な CLI、設定、Git、Ollama 機能を調査するとき
- doctor の内部実装詳細や正本仕様を確認したいときは、対応する実装または oracle 文書を直接読む

## hash
- bfac4be0bdb1d27ce444e661b9b70df994e9e7715546d6e767f8da67662f2cf8

# `test_indexing_cli.py`

## Summary
- `cmoc indexing` の CLI と preflight、worktree 対応、Codex による INDEX.md 生成、hash による再生成抑制、INDEX.md のみを対象とする commit lifecycle を外部挙動として検証するテスト。

## Read this when
- `cmoc indexing` の CLI 事前条件・doctor 実行・worktree 選択・dirty 状態の拒否を確認または変更するとき。
- INDEX.md の生成、Codex structured output の利用、fresh hash 時の Codex 呼び出し省略を確認するとき。
- INDEX.md だけを commit し、既存の非 INDEX 差分を保持する preflight と commit 条件を確認するとき。

## Do not read this when
- INDEX.md エントリーのレンダリング仕様そのものを確認する場合は、指定された Structured Output schema と indexing の仕様文書を直接読む。
- indexing CLI 以外のサブコマンドや、Codex 実行基盤そのものの内部実装だけを調べる場合。

## hash
- 18f6f2e15bd0dc91ad5aab6124407919ef9da1b31a6bc5859be15fdc1068f90e

# `test_indexing_common.py`

## Summary
- `commons.indexing` の直接テストを集約し、INDEX entry の入力検証・再生成・hash 再利用、ディレクトリ traversal、symlink cycle 回避、空ディレクトリ処理、安定順序、並列実行とログ伝播を検証する。indexing の実装挙動を CLI lifecycle から分離して確認する入口。

## Read this when
- INDEX entry の render/parse/update 検証を変更・調査するとき
- ディレクトリ traversal、memo 除外、symlink cycle、空ディレクトリの INDEX 生成を変更・調査するとき
- INDEX 更新の並列実行、cwd lock、Codex worker のログ伝播を変更・調査するとき

## Do not read this when
- CLI lifecycle やサブコマンド全体の統合挙動を確認するときは、対応する CLI テストを直接読む
- INDEX entry の正本 schema や仕様を確認するときは、参照されている oracle 文書・oracle src を直接読む
- indexing 実装そのものを変更・調査するときは、まず `commons.indexing` の実装を読む

## hash
- d082ee84872186039e811fddac3ee07c8e6c57ede4045f3b7c6192ab0b51cc38

# `test_indexing_preflight.py`

## Summary
- Codex 呼び出し前の indexing preflight を検証するテスト。exec/TUI 経路での実行順序、linked worktree の選択、repository lock 待機、パラメータによる無効化、file access violation 後の recovery indexing 禁止を、git 状態や外部呼び出しの観測を通じて確認する。

## Read this when
- indexing preflight の実行条件・実行順序・lock 制御を変更またはレビューするとき
- Codex exec/TUI 呼び出しと linked worktree の indexing 対象の関係を確認するとき
- file access violation 後に recovery 処理を追加・変更するとき

## Do not read this when
- INDEX.md 生成処理そのものの仕様や実装を確認したいときは、indexing 実装および対応する oracle file を直接読む
- Codex 呼び出し経路と無関係なテストや機能を調査するとき

## hash
- 01f64b45368fc2e43171f5b0089eb952c53d26d45c3a1cfe1a6efc93282f6f18

# `test_packaged_import.py`

## Summary
- packaged layout での import 境界と公開面の崩れを検証するテスト群。oracle 側の正本定義が配布形態でもそのまま参照され、`acp.builder` と `config` の公開 import が余計な実装を漏らさないことを確認したいときに読む。

## Read this when
- packaged layout を前提にした import 失敗や公開漏れの回帰を確認したい。
- oracle 側の定義を複製せずに再公開しているか、または配布後の環境でも正本を参照できるかを確かめたい。

## Do not read this when
- 通常の単体ロジックや CLI 挙動だけを確認したい。
- packaged layout ではなく通常のソースツリー上の内部実装を追いたい。
- 個別の builder 実装や config 定義の内容そのものを読みたい。

## hash
- 52612d997cee015efa9da672fc11c668e6ed407722cc2e0d7c56dcab87cd5e1b

# `test_production_cli.py`

## Summary
- 実 Codex CLI と cmoc managed ollama を使い、独立 process・PTY 上で全末端サブコマンドの本番経路を検証する受け入れテスト。終了 code、report・state・Git の状態、Codex call log、TUI の応答完了と終了を確認し、LLM の回答品質自体は判定しない。

## Read this when
- CLI の全末端サブコマンドが本番同等の独立 process 経路で動作するか確認するとき
- Codex 呼び出し、managed ollama 設定、call log、report、session/apply の状態遷移を検証するとき
- 実 Codex TUI の PTY 操作、応答完了、正常終了を検証するとき
- 新しい公開末端 command の本番経路試験への反映漏れを確認するとき

## Do not read this when
- 個別コマンドの内部実装や単体ロジックだけを変更・調査するとき
- LLM の回答品質やプロンプト内容そのものを評価するとき
- 実 Codex CLI・managed ollama・独立 process・PTY を使わないテストを確認するとき

## hash
- e0bc129486b94a059dff92999096aeffa3ee1e67786bd62162fbbc5652c9aa74

# `test_prompt_parts.py`

## Summary
- 標準 prompt parts と complete prompt の組み立て結果を検証するテスト。各標準ルールのタイトル・主要内容・complete prompt への包含条件、file access mode ごとの内容、root placeholder の保持、既定時の除外を確認する。prompt builder の標準部品や complete prompt の変更時に挙動を確認する入口となる。

## Read this when
- prompt parts の標準文面、complete prompt の構成、file access rule のモード別出力を変更またはレビューするとき
- root placeholder の展開・保持や、標準ルールの既定包含条件を変更または検証するとき
- prompt builder 関連テストの失敗原因を調査するとき

## Do not read this when
- prompt builder の実装詳細ではなく、個別標準ルール本文の仕様だけを確認したいとき
- prompt builder と無関係な CLI 機能やテストを扱うとき

## hash
- ae5bb3960df3cb20ffce2e846a36a7b8587ed01a3fcb822da309767fe3a3c587

# `test_review_oracle_loop.py`

## Summary
- review oracle の finding loop を検証するテスト。対象 oracle ごとの finding 分離、検証周回の reason 引き継ぎ、中断時の部分結果保持、merge response の意味検証と再試行・失敗を確認する。隔離 worktree と Codex Structured Output の呼び出しコンテキストも検証する。

## Read this when
- review oracle の finding 列挙・merge・validate・judge loop の挙動を変更または調査するとき
- review agent call の repo root、cwd、worktree 分離を確認するとき
- merge の意味的失敗時の再試行や KeyboardInterrupt 時の結果保持を確認するとき

## Do not read this when
- review oracle loop のテスト対象ではなく、通常の review oracle 実装や prompt 定義だけを確認するとき
- finding schema や設定値の正本仕様を確認したいときは、記載された oracle doc・oracle src を直接読む

## hash
- 0e5acc2c069f56295d9a53f6e7a5780a71a1700f036eebcd82e67e374deb71c1

# `test_review_oracle_merge_operations.py`

## Summary
- `cmoc review oracle` の所見マージ操作の契約を検証するテスト。`delete` / `replace` / `merge` の対象指定や payload 制約、同じ `finding_id` の再利用禁止を確認したいときに読む。

## Read this when
- 所見リストを `delete` / `replace` / `merge` で整理する挙動の契約を確認したいとき。
- merge 操作の入力検証や、複数 operation 間で同じ `finding_id` を再利用した場合の拒否条件を確認したいとき。
- `cmoc review oracle` の所見マージ周辺のテスト追加・修正をするとき。

## Do not read this when
- 所見の列挙・検証・判定の契約を見たいときは、より直接に `review oracle` 本体側の仕様や実装を読む。
- `cmoc review oracle` 全体の実行手順や report 体裁を確認したいだけなら、このテストではなく `review oracle` の正本仕様を読む。
- テスト規約全般を確認したいだけなら、この個別テストではなくテスト方針側を読む。

## hash
- 8f58e561044e98e048ad9d7fcfa64b2d72f97670424a7999f6ed86968dd03976

# `test_review_oracle_report.py`

## Summary
- review oracle の report 生成と CLI 委譲を検証するテスト。中断時の評価範囲、正常・異常時の report 保存、finding の severity/verdict 別分類と件数、oracle-root alias・symlink の集計、scope オプション、出力節順およびエラーメッセージを確認する。

## Read this when
- review oracle または eval-oracle の report 形式・CLI 出力・中断処理・失敗処理を変更または検証するとき。
- finding の受理・棄却、severity 別集計、oracle path の解決や集計ロジックを変更するとき。

## Do not read this when
- review oracle の実装や report 出力に関係しない機能を変更・調査するとき。
- テスト共通基盤や個別の git・Ollama・CLI fixture の実装を直接調査する必要があり、それらのサポートファイルへ進むべきとき。

## hash
- c36b766533eb90ea3ec669522bfcf7c23ab2ad9407d1361df561f283a63f5c08

# `test_review_oracle_targets.py`

## Summary
- review oracle の finding path 解決と oracle 対象列挙を検証するテスト。相対・placeholder・絶対 symlink の path 処理、repository 外判定、session/full scope の対象数・差分基準・no_targets、追跡済み ignored file、symlink、AGENTS.md/INDEX.md 除外を確認する。

## Read this when
- review oracle の対象範囲、finding path 解決、session/full scope の差分基準を変更・調査するとき。
- oracle file の git 追跡状態、ignored file、symlink、対象除外条件に関するテストを確認するとき。

## Do not read this when
- review oracle 以外の review 機能や、対象列挙・path 解決に関係しない CLI の変更を扱うとき。
- finding の内容判定や Structured Output schema 自体を変更・調査するときは、対応する実装・schema テストを直接読む。

## hash
- 509a286c34f176b9897c62f1a1992d1c5e7a9d6328b284fa354aee92fb51511b

# `test_review_oracle_worktree.py`

## Summary
- review oracle の worktree 分離・未コミット差分検出・INDEX.md のみの統合・競合解決を検証する pytest。review 対象の branch/oracle、preflight で生成された INDEX.md、禁止された非 INDEX 差分、review worktree の後処理を確認するテスト群への入口。

## Read this when
- review oracle サブコマンドの worktree、session branch、oracle のレビュー対象、INDEX.md 統合、差分制限、merge conflict 解決を変更・調査するとき。
- review oracle や indexing の挙動を end-to-end に近い形で検証したいとき。

## Do not read this when
- review oracle の実装詳細だけを確認する場合は `src/sub_commands/review/oracle.py` などの実装を直接読む。
- INDEX.md の通常の生成ロジックだけを確認する場合は `src/commons/indexing.py` と対応する直接テストを読む。
- Codex CLI の出力品質そのものを調査する場合。

## hash
- b5951590a8180d4510354311e5c75aef58839c4b0518be26c891c1a8d54fac75

# `test_runtime_apply.py`

## Summary
- apply 実行時の process tracking と停止契約を、CLI を介さず低レベル API で検証するテスト。pid file の child PID 読み込みと advisory lock 待機、pidfd による PID identity 検証、process group 停止、親終了後の再読込、競合終了や PID reuse の扱いを対象とする。apply abandon の CLI 外部挙動を確認するテストへの入口ではない。

## Read this when
- apply 実行プロセスの追跡情報、pid file、advisory lock、pidfd、process group、停止時の warning や PID reuse 防止を変更・調査するとき。
- commons.runtime_apply の低レベル停止処理が、親 process と記録済み Codex child process を安全に扱うことを検証するとき。

## Do not read this when
- apply abandon コマンドの CLI 入出力や外部挙動を変更・調査するときは、test_apply_abandon_cli.py を直接読む。
- apply runtime の process tracking や停止処理に関係しない機能を変更・調査するとき。

## hash
- 67147ef59cbbd27fbe91af2efc727e8d5f74d139a8392b69cb7ca83817a86a29

# `test_runtime_cli.py`

## Summary
- CLI の error report、サブコマンドログ、duration 表示、doctor preflight、pre-log check、completion probe、work root 制約、gitignore 修復の外部挙動を検証するテスト。関連する CLI 境界やログ・初期化副作用の変更時に、仕様適合性を確認する入口となる。

## Read this when
- CLI のエラー出力形式、stdout/stderr 分離、終了コード、引数解析、scope 制約を変更・調査するとき
- サブコマンドログの生成、timestamp 衝突、doctor preflight、pre-log check、worktree の扱いを変更・調査するとき
- shell completion probe の副作用抑制や起動 wrapper の error report を変更・調査するとき
- `.cmoc` の gitignore 修復や duration 表示を変更・調査するとき

## Do not read this when
- CLI 内部の個別サブコマンド処理や oracle の内容自体を変更・調査する場合は、対応する実装・oracle 文書を直接読むとき
- CLI と無関係な機能のテストや内部 helper の実装詳細だけを変更・調査するとき

## hash
- 2d587029ae8930097a76565528d2304e102088a9fc9ed9253b08b9fa2b50c144

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
- Codex CLI の sandbox argv 生成を検証する pytest。全 FileAccessMode で permission profile や path 別例外を注入しないこと、作業ツリー内容に依存しないこと、生成された sandbox 引数を実 Codex CLI が受理することを確認する。

## Read this when
- Codex の sandbox argv、permission profile、path 別 read/write 例外の扱いを変更・検証するとき
- build_codex_override_args または prepare_codex_override_args の API・出力を変更するとき
- Codex CLI parser との sandbox 引数互換性を確認するとき

## Do not read this when
- Codex sandbox argv や permission profile に関係しない機能のテストを調査するとき
- 実装本体の一般的な設定処理や、個別の CLI サブコマンドの挙動を直接確認するとき

## hash
- d69dabe02e2acbadf3e6a25fde436391e442f073d3b5393199757f65daf8c5fd

# `test_runtime_codex_profile.py`

## Summary
- Codex 起動引数における model、sandbox、provider 上書き契約を検証するテスト。各 FileAccessMode の sandbox 変換、承認設定、reasoning effort、未知 mode の拒否、通常 provider での worktree 非走査、cmoc 管理 Ollama provider の設定を確認する。

## Read this when
- Codex argv の sandbox・model・provider 上書き仕様を変更または検証するとき
- FileAccessMode と Codex 起動引数の対応を確認するとき
- cmoc 管理 Ollama provider の Codex 設定を変更または検証するとき

## Do not read this when
- Codex argv の構築実装そのものを変更・調査するときは、参照されている runtime 実装と oracle 仕様を先に読む
- Codex 起動引数と無関係なテストや設定を扱うとき

## hash
- ef8efcced62957c7c008e9f2ab391f208d1db6ff2d4099f12161c4ed701c8c9c

# `test_runtime_config.py`

## Summary
- CmocConfig の既定値、JSON 化時の定義順、設定ファイルの読み込み、入力値の型・内容検証、Codex の recovery 試行回数の保持を検証するテスト。設定ランタイムや CmocConfig の挙動を変更・確認する際の入口。

## Read this when
- CmocConfig の既定値や Codex model・reasoning effort の対応を変更するとき
- 設定の JSON 入出力、欠落時エラー、section・map・数値項目の入力検証を変更するとき
- 設定ランタイムのエラー案内や recovery 試行回数の保持を確認するとき

## Do not read this when
- 設定機能の実装詳細を直接確認する必要があるときは、テストの根拠として示された oracle src や設定実装を先に読むとき
- 設定とは無関係な CLI、fork、oracle review、ACP の挙動だけを調査するとき

## hash
- a39a98af225c33ce88ae6a34c67d4e27e2f9836cdffaec3607d38cf1659c4f55

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

# `test_runtime_ollama.py`

## Summary
- Ollama ランタイム管理のテストを集約し、systemd ユーザーサービスの更新・起動・再起動条件、実行プロセスと listener の検証、HTTP 応答によるサービス検証、モデルの pull/load、GPU runtime の VRAM 確認を検証する。Ollama 関連の実装挙動やエラー条件を変更・調査する際のテスト入口となる。

## Read this when
- Ollama サービスの systemd 管理、プロセス検証、起動確認を変更または調査するとき
- Ollama モデルのロード、pull、GPU 実行確認、VRAM 判定を変更または調査するとき
- Ollama ランタイムの HTTP 応答や利用者向けエラー処理に関するテストを確認するとき

## Do not read this when
- Ollama 以外のランタイムや共通エラー処理だけを変更・調査するとき
- 実装ではなく、Ollama の正本仕様そのものを確認するときは oracle の仕様文書を直接読む

## hash
- 48b3bd4f5ffe7c4418dd15449808c1fc11e91af88fce370acb7d4be9d5d2dea1

# `test_runtime_state.py`

## Summary
- session/apply state の入力形状検証、branch 名解析、状態ファイル読み込み時の不正形式検出を担うテスト。session fork lock の process 間共有と直列化も検証する。runtime state 実装や session fork 仕様の挙動確認に入るためのテスト入口。

## Read this when
- session/apply state のフィールド型・null 許容・不正値処理を変更または確認するとき
- session branch や apply branch の解析規則、状態ファイルの branch 対応付けを変更または確認するとき
- session fork lock の repository 単位の process 間排他を変更または確認するとき

## Do not read this when
- session/apply のサブコマンド本体の処理フローだけを確認したいときは、対応するサブコマンド実装や oracle 仕様を直接読む
- runtime state の実装詳細を確認したいときは、まず commons.runtime_state の実装を直接読む

## hash
- fbf9b2216eb0685b34c2b417691c61d2450c18a06114603fa4837f9e842e2ce8

# `test_session_cli.py`

## Summary
- session の fork・join・abandon CLI における外部挙動を、実 Git リポジトリと linked worktree を使って検証する回帰テスト群。branch と永続 state の生成・遷移・cleanup、rollback、session-id 衝突、dirty worktree や破損 state の拒否、oracle conflict 解消、Codex 実行時の sandbox・prompt・root/cwd 境界、stdout/stderr の error report を扱う。session 状態ライフサイクル全体を観測するテスト入口。

## Read this when
- session fork、join、abandon の CLI 挙動や回帰テストを変更・調査するとき
- session branch、session state、linked worktree、state cleanup、rollback の仕様や不具合を確認するとき
- session join の conflict resolution、Codex sandbox、prompt、repo root/cwd の受け渡しを検証するとき
- session CLI の出力先、終了コード、preprocess、dirty worktree 拒否を確認するとき

## Do not read this when
- session CLI 以外のサブコマンドや、session の実装詳細だけを直接調査する場合
- session state の正本仕様を確認する場合は、対応する oracle doc を直接読む
- 共通テスト補助関数や Git/Ollama test fixture の実装を確認する場合は、それぞれの support module を直接読む

## hash
- 3ef6f1b66b65cdf83f9ff4b65cfdea2d98144d8c3201123d00abc33c22aef2a7

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
