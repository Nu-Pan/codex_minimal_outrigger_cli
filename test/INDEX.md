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
- doctor CLI を対象 worktree のカレントディレクトリで実行するテスト支援関数を提供する。doctor サブコマンドの CLI テストで、実行結果の成功確認と参照に使う共通入口。

## Read this when
- doctor CLI の実行結果をテストから取得したいとき
- 対象 worktree をカレントディレクトリとして CLI を実行するテストを追加・変更するとき

## Do not read this when
- doctor CLI の仕様や前処理の正本を確認したいときは、対応する oracle doc を直接読む
- doctor CLI 以外のテスト支援や CLI 実行処理を変更するとき

## hash
- 04ee47c861ffe5b25223ffec1083362f42f865aca8b550498bd0a06378362cf0

# `_codex_support.py`

## Summary
- Codex 実行経路のテストで共用する補助関数と fake result を定義するテストサポートモジュール。隔離された Codex/Ollama 用環境の準備、Codex パラメータ生成、CLI 引数・設定の解析、Codex override の stub 化を下位テストから利用する入口。

## Read this when
- Codex runtime wrapper、TUI、Structured Output、CLI override のテストを追加・変更するとき
- テスト内で隔離 Codex home、既定 AgentCallParameter、Codex 引数解析の共通処理が必要なとき

## Do not read this when
- Codex 実行経路の実装自体を変更・調査するとき
- このモジュールの共通テストヘルパーを使わない別領域のテストを扱うとき

## hash
- 6698e05b59d5277c59d5808c9ebf1aa58b962fe0dcd2d39630961bc262839119

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
- テスト用 Git リポジトリを初期化する共通ヘルパーと、現在のブランチ名を取得する関数を提供する。Git のユーザー設定・署名・フック・ignore 設定をテスト環境向けに固定し、最小のコミット済みリポジトリや、ignore 対象だが追跡済みの oracle ファイルを作成するテストの入口となる。

## Read this when
- cmoc CLI の Git 状態やリポジトリ初期化を検証するテストを追加・変更するとき。
- テスト用リポジトリの作成条件や Git の環境依存設定を確認するとき。

## Do not read this when
- Git テスト用リポジトリを使わないテストを扱うとき。
- 個別の CLI 実装や oracle 仕様の詳細を確認したいとき。

## hash
- 1ecaade4dee17221fe4bca8c1837bef8e9d28957fd6bee025a6b52c299aea9e1

# `_ollama_support.py`

## Summary
- 実経路統合テスト向けに、case-local Ollama の導入・モデル準備・GPU-only 推論確認・cache の安全な materialize/atomic publish・process group teardown を一体で扱う支援モジュール。通常のモデル設定を動的なローカル Ollama provider へ差し替える入口も提供する。

## Read this when
- 実経路統合テストで case-local Ollama の起動、モデル cache、GPU 利用確認、provider 設定、終了処理を変更・調査するとき。

## Do not read this when
- 通常の Ollama やモデル provider の本番実装を変更するとき。個別の統合テスト本体の検証ロジックだけを変更するとき。

## hash
- 05a91d9bcaa87673390175fa9a02ca7c11ceaf6d760ad5b472ed0846c7b92019

# `test_acp_builder_editing_run_parameters.py`

## Summary
- editing run workload 向けの ACP builder adapter を検証するテスト。apply builder の commit 範囲・raw diff・入れ子のコードフェンス保持と、refactor builder の canonical structured-output schema、実行設定、prompt 境界保持を確認する。関連する oracle builder 実装・schema の挙動を検証する入口。

## Read this when
- editing run の apply または refactor builder の prompt 生成、実行設定、structured-output schema 連携を変更・調査するとき
- raw diff にコードフェンスや prompt 境界風の文字列が含まれる場合の安全な埋め込みを検証するとき

## Do not read this when
- builder の実装自体を変更せず、他の ACP builder 領域や一般的なテスト規約だけを調べるとき
- このテストが対象とする apply/refactor の editing run parameter 以外の機能を直接確認するとき

## hash
- c8b7ae1a1a6659e02b2543f9a74b5cb003662ab6f3312f073cd62d840b171570

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
- oracle review ACP builder 群の parameter、structured-output schema、互換 module の公開面、model・reasoning・file access 設定を検証する回帰テスト。
- enumerate、judge、merge、advocate、challenger 各 builder の oracle schema 一致、動的入力保持、symlink path、placeholder 展開を確認する。
- 動的 prompt に埋め込む Markdown code fence や section・placeholder 風文字列が実際の prompt 境界と誤認されず保護されることを検証する。

## Read this when
- oracle review builder の parameter や structured-output schema を変更・調査するとき。
- review builder の公開 API、互換 module の __all__、model class、reasoning effort、file access mode を確認するとき。
- 動的 prompt の code fence 保護、section 境界、placeholder 展開、入力保持の挙動を変更・検証するとき。

## Do not read this when
- review builder 以外の ACP builder の実装やテストだけを扱うとき。
- schema や prompt 境界ではなく、review 実行フロー・所見処理・CLI 統合を直接調査するときは、対応する実装または専用テストを読む。

## hash
- 4c5b51431a96b031e804828b21e575faf6b2c36b230a63173b222075c468784b

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
- Root/worktree と path model の runtime 契約を検証するテスト。root placeholder の解決、repo root と linked worktree の区別、process-global cwd を扱う pushd の排他、run worktree の作成・検索・削除における管理領域・branch 対応・Git 登録・symlink・dot component・stale path の安全性を対象とする。

## Read this when
- path placeholder、repo/work root、linked worktree、pushd の並行実行を調査・変更するとき
- run worktree の作成・検索・削除に関する path 検証や安全性を調査・変更するとき
- runtime の Git 設定隔離や worktree 境界に関するテストを確認するとき

## Do not read this when
- CLI コマンド固有の挙動、runtime path 以外のテスト、または一般的な path helper の実装詳細だけを確認するときは、対象実装・対応テストを直接読む

## hash
- 98e1b1e4d0eb6f862a6a11931411d3d2ea90194268796c91b90f20e81e9535d3

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
- TUI 起動直前の CLI 前処理を外部挙動から検証するテスト。エディタ入力の保存、prompt 解決、Codex TUI 起動パラメータ、完全 prompt の生成、linked worktree でのログ・schema・ignore 配置を扱う。

## Read this when
- TUI サブコマンドの起動前処理や Codex 起動設定を変更・検証するとき
- エディタ入力ファイルの timestamp 衝突、prompt の standard 選択、linked worktree 対応を確認するとき
- TUI 関連の CLI テスト失敗を調査するとき

## Do not read this when
- TUI 以外のサブコマンドや、起動前処理と無関係な共通ユーティリティだけを変更・調査するとき
- Codex 実行基盤そのものの詳細を確認したい場合は、対応する runtime 実装・テストを直接読むとき

## hash
- 5246687320a9532814fd8c76cbe305e350e1ea2e80de4cc9c7f9fb384c9874cb

# `test_codex_runtime_errors.py`

## Summary
- Codex 実行の異常系と CLI 不在時の挙動を検証するテスト。JSONL の不正・非 object イベント、終了コード 0 でも不正出力となるケース、Codex CLI 不在時の CmocError と失敗ログ、Codex 呼び出し通知の call log path・未開始表示を扱う。

## Read this when
- Codex 実行処理の JSONL parser、異常分類、エラー文、CLI 不在時の例外やログ出力を変更・調査するとき
- Codex 呼び出しの console 表示や失敗時の subcommand log を検証するとき

## Do not read this when
- Codex 実行の正常系や resume 処理だけを変更・調査するときは、正常系を直接扱うテストを読む
- Codex 以外のサブコマンドのログや外部コマンド実行を変更・調査するときは、対象の実装・テストを直接読む

## hash
- 15da258720b211de819bbd206db3f20937d1c83e1ab783b0e4698df7b7570530

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
- Codex exec の Structured Output 検証失敗、capacity retry、JSONL エラー、中断時の失敗記録、retry 上限、agent diff 保持を、subprocess 呼び出し回数・call log・subcommand event と併せて検証するテスト群。run_codex_exec の異常系状態機械を確認する入口。

## Read this when
- Codex exec の retry 判定、失敗時ログ、JSONL エラー処理、Structured Output 検証、capacity retry、中断時挙動を変更・調査するとき。
- call log や subcommand event の status、returncode、error、ログパス、retry 上限、backoff の外部挙動を確認するとき。
- capacity retry 後の agent diff 保持や、stdout JSONL 外のエラーマーカーを無視する挙動を確認するとき。

## Do not read this when
- Codex exec の正常系だけ、または retry・失敗時ログに関係しない入出力変換を確認するときは、対象の実装・正常系テストを直接読む。
- 共有ログ schema の正本や retry 方針そのものを確認する場合は、このテストではなく参照されている oracle ドキュメントを先に読む。

## hash
- a0d3ee61dd2a5c14a5eee7b99cf16e1bf174abbee88364624b2eb2e148238ce3

# `test_codex_runtime_subprocess.py`

## Summary
- Codex サブプロセス実行とプロセスグループ停止に関する realization test。tracking file への child 情報記録、専用 process group の識別、pidfd を用いた安全な signal 配信、tracking 更新失敗時の cleanup、割り込み時の追跡維持を検証する。
- run process tracking の不正 encoding・負の start time・symlink・特殊ファイルを拒否または stale として扱う挙動、および missing cwd などの subprocess エラー伝播を検証する。
- `commons.runtime_codex_profile` または `commons.runtime_run` の Codex 起動、プロセス同一性確認、停止処理、tracking file 保護を変更・レビューするときのテスト入口である。

## Read this when
- Codex subprocess の起動・追跡・終了処理を変更するとき
- process group、pidfd、signal、leader の再利用防止など cleanup の安全性を確認するとき
- run process tracking file の読み書き、検証、異常系挙動を変更するとき
- 関連する runtime 実装の回帰テストや失敗原因を調査するとき

## Do not read this when
- Codex subprocess や process tracking、process group cleanup と無関係な機能を変更するとき
- CLI の通常の入出力や別サブコマンドの仕様だけを調査するとき
- テスト対象の runtime 実装を直接確認する必要がある場合は、まず対応する `commons.runtime_codex_profile` または `commons.runtime_run` を読むべきとき

## hash
- 4d35998659b89e61eacdf372195dd2b8c09a55be6700f46fce950edf91fb2c04

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
- doctor preprocess の修復 lifecycle と外部契約を検証する統合テスト。Git 状態、config、refactor state、共有 lock、linked worktree、既存の staged・unstaged 差分や index flag の保持を、CLI と直接呼び出しの両方で確認する。

## Read this when
- doctor preprocess の修復処理や Git index 保持挙動を変更・検証するとき
- doctor の CLI/config、lock、linked worktree、修復 commit の統合テストを追加・調査するとき

## Do not read this when
- doctor preprocess 以外の機能を変更するとき
- 単独の Git helper、CLI helper、または doctor 実装の詳細だけを確認する場合は、まず対応する実装・helper・正本仕様を読むとき

## hash
- bd3acdaed00b950c34ab15df5f295d4e7a0cd1d598cd5c7351bd0a422d68def1

# `test_editing_run_cli.py`

## Summary
- workload fork と共通 run lifecycle の統合テストを収録する。editing run の session state、run worktree・branch、fork report、Codex process tracking、INDEX 更新、join/abandon、rollback、cleanup、refactor cycle の状態遷移と失敗時挙動を検証する。
- realization apply/refactor fork と run join/abandon が共有する lifecycle fixture・状態遷移を一続きで検証する統合テストの入口である。

## Read this when
- realization apply または realization refactor の fork 処理を変更・調査するとき
- run join、run abandon、editing run の state・worktree・branch cleanup を変更・調査するとき
- fork report、lifecycle report、process tracking、Codex child 停止、INDEX refresh、rollback の挙動を検証するとき
- run 開始・完了・中断・失敗・競合時の state 遷移や成果物 merge のテストを確認するとき

## Do not read this when
- 個別の CLI 実装責務や正本仕様だけを確認したいときは、対応する realization 実装または oracle file を直接読む
- run lifecycle と無関係なサブコマンド、単純な parser、共通 utility の単体テストだけを確認するとき

## hash
- b4da0d6f7f86b0c0baa8845651b68b2e913f4bcd4437448d31801b22a584bb79

# `test_indexing_cli.py`

## Summary
- `cmoc indexing` の CLI と preflight／commit lifecycle を外部挙動として検証するテスト。doctor による初期化、現在の worktree の選択、dirty 状態の拒否、INDEX.md の生成・更新、Codex の Structured Output 利用、hash による再生成省略、INDEX.md のみの commit、Git 差分失敗処理を扱う。indexing 実装や仕様変更時の回帰確認の入口となる。

## Read this when
- `cmoc indexing` の CLI 動作、preflight、worktree 対応、INDEX.md 更新、Codex 呼び出し、commit 条件を変更または調査するとき。
- indexing の clean／dirty repository、既存差分、linked worktree、設定読み込み、fresh hash の挙動を確認するとき。

## Do not read this when
- INDEX.md エントリー生成の Structured Output schema 自体を確認したいときは、指定された oracle schema を直接読む。
- indexing の内部実装や正本仕様の詳細を調べるだけの場合は、対応する実装または oracle 文書を直接読む。

## hash
- 3ac50f0119f112ac4b2defefcd24876871abeb65162baee557d3c1d65123e07a

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
- `cmoc oracle edit` の main-worktree TUI 起動を検証するテスト。TUI 実行時のイベント順序、AgentCallParameter、oracle 差分の保持、session state と run lifecycle の非変更、TUI 失敗時の終了を確認する。
- oracle edit の起動前提として、main worktree、session branch、active session、clean worktree が必要であることを、各違反ケースの利用者向け例外で検証する。

## Read this when
- `cmoc oracle edit` の CLI 起動処理、TUI 呼び出し、oracle 編集後の状態保持を変更または調査するとき。
- oracle edit の起動前提条件や、indexing preflight・clean worktree 検査・TUI 実行の順序を確認するとき。
- 関連する oracle edit 実装やテストの挙動を検証するとき。

## Do not read this when
- oracle edit 以外のサブコマンドの実装やテストだけを扱うとき。
- TUI の内部実装そのものや oracle 文書の編集仕様を直接確認したいときは、それぞれの実装ファイルまたは oracle 文書を直接読む。

## hash
- a61bdf40a7dbc1e1c1e25b26188714fa9e912825b0d9a8bb53dec26a692ee884

# `test_oracle_investigation_cli.py`

## Summary
- `cmoc oracle investigation` CLI の起動条件を検証するテスト。セッション前提なしで main worktree から起動できること、oracle 専用のファイルアクセスモードと調査指示を含む prompt が渡されることを確認する。

## Read this when
- oracle investigation サブコマンドの起動条件や session 前提を変更・確認するとき
- oracle investigation から Codex TUI へ渡すファイルアクセスモードや prompt の検証を確認するとき

## Do not read this when
- oracle investigation 以外のサブコマンドの CLI 起動条件を調べるとき
- oracle investigation の実装詳細や oracle 仕様本文を確認することが目的のときは、対応する実装または oracle 文書を直接読む

## hash
- cc83e904333f6e395618532c5f0b7e5972e5b46b426d468c0e1c44b7db03eeda

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
- oracle review の report 生成・表示と CLI 出力を検証する回帰テスト群。中断・処理失敗時の report、finding の severity/verdict 別分類、評価対象数、path 集計、Markdown/YAML エスケープ、scope option、timestamp 衝突回避などを扱う。oracle review report contract の構築から表示までを一体で確認する入口。

## Read this when
- oracle review の report schema、finding 表示、CLI 出力、エラー／中断時の挙動を変更・調査するとき
- oracle review の回帰テストや Structured Output callback の期待契約を確認するとき

## Do not read this when
- oracle review の通常処理実装そのものを確認したいときは、対応する sub_commands の実装を直接読む
- oracle review の正本仕様を確認したいときは、列挙された oracle doc や schema 定義を直接読む

## hash
- 0b5880a67b77bf66a9fbaca514bd12e082cff340a5a1b919904a81d0d542d9ec

# `test_oracle_review_targets.py`

## Summary
- oracle review の対象ファイル列挙と finding path 解決を検証する realization test。placeholder 付きパス、symlink、repository 内の oracle 判定、tracked/ignored file、session/full scope、fork commit 基準、除外対象、対象なしレポートを扱う。oracle review の対象選定・パス解決ロジックを確認する入口である。

## Read this when
- oracle review の対象列挙や finding の oracle path 解決を変更・調査するとき
- session/full scope、tracked ignored file、symlink、fork commit 基準の挙動を確認するとき
- oracle review CLI の対象なし結果や Codex 呼び出し回数を検証するとき

## Do not read this when
- oracle review 以外のサブコマンドや、対象列挙・パス解決と無関係な CLI 処理を変更するとき
- Codex CLI の実推論や出力品質を検証する実経路統合テストを探しているとき
- oracle review の所見マージ・妥当性検証・採否判定の詳細実装を直接確認したいとき

## hash
- 9113e685069c202fce5d8a6896ad9e71cbe5268f33057e218a8d36c42cce0271

# `test_oracle_review_worktree.py`

## Summary
- oracle review の review worktree lifecycle 全体を検証する回帰テスト。linked worktree・session snapshot からの fork、run target 衝突、割り込みや例外時の cleanup、未コミット差分の拒否、active run 中の実行を扱う。
- review worktree で生成された INDEX.md および preflight がコミットした INDEX.md の session への統合、INDEX.md 以外の差分拒否、削除競合の解決、Git quoted path の扱いを検証する。
- review branch・worktree の cleanup 失敗や dangling symlink をエラーとして扱う制御も対象とする。

## Read this when
- oracle review サブコマンドの worktree 隔離、snapshot commit、branch lifecycle、割り込み時 cleanup を変更・調査するとき
- oracle review における INDEX.md の生成、preflight commit、merge、conflict resolution、差分制限を変更・調査するとき
- review run のリソース削除失敗や異常終了時のレポート生成を検証するとき

## Do not read this when
- oracle review の通常の finding 列挙・検証ロジック自体を変更・調査するだけで、worktree lifecycle や INDEX 統合に関係しないとき
- session fork、一般的な run lifecycle、INDEX 生成の単体挙動を直接確認する場合は、それぞれの実装・専用テストを先に読むとよい

## hash
- 51e93a1b5de976527c68c889871520faa47c612d4a0a15c7f3b25c0a76925efc

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
- 実 Codex CLI と case-local Ollama を使い、独立 process・PTY 上で全末端サブコマンドの本番経路を検証する受け入れテスト。終了 code、report・state・Git・Codex call log、TUI の応答完了と終了操作を確認し、LLM の回答品質は判定しない。

## Read this when
- CLI の全末端サブコマンドが本番 process 経路で正常完了することを確認・変更するとき
- 独立 process、隔離済み Codex home、case-local Ollama、Codex call log の検証方法を調べるとき
- TUI の PTY 操作、端末 capability query、応答完了後の終了処理を確認するとき
- サブコマンド実行後の report・session/run state・worktree・Git 状態の受け入れ条件を確認するとき

## Do not read this when
- LLM の回答内容や推論品質そのものを評価するとき
- 単一の内部 helper や非本番の単体テストだけを変更・調査するとき
- 本番経路を使わない parser、設定、Git 操作の局所テストを確認するとき

## hash
- baee4f3bdda5986f3adb498af3af14e164195c39475de4e24cd16867fd87187a

# `test_prompt_parts.py`

## Summary
- 標準 prompt parts の rendering と complete prompt の組み立てを検証する回帰テスト。各標準ルールの見出し・主要語、file access mode ごとの内容、prompt への注入条件、placeholder の保持・展開、既定時の省略を確認する。

## Read this when
- prompt builder の標準ルールや complete prompt の構成を変更・調査するとき
- prompt parts の StructDoc rendering、root token、placeholder 展開、注入オプションの回帰を確認するとき

## Do not read this when
- prompt builder の実装詳細や標準ルール本文そのものを確認したいときは、対応する oracle/src または realization/src の実装を直接読む
- prompt builder と無関係なテストや一般的なテスト実行方法を調べるとき

## hash
- 4596cc03246518c3109d3d161ce34c574965d70ac82ed0368a7e0fb58973a563

# `test_runtime_cli.py`

## Summary
- CLI の error report、終了コード、stdout/stderr 境界、サブコマンドログ、duration 表示を検証する runtime 回帰テスト。
- doctor preflight、work root 制約、completion probe、引数解析、wrapper 起動失敗、Git ignore 更新と symlink 保護を扱う。
- CLI lifecycle に共通する runner・work root・subcommand event の外部契約を確認するテスト入口。

## Read this when
- CLI の例外処理、error report、終了コード、KeyboardInterrupt の扱いを変更・調査するとき
- サブコマンドログ、並列 logger、ログ flush 失敗、duration 表示を変更・調査するとき
- doctor preflight、work root 検証、completion の副作用抑制、CLI 引数解析を変更・調査するとき
- bin/cmoc の起動失敗や Git ignore ファイル更新の安全性を変更・調査するとき

## Do not read this when
- 特定サブコマンドの本体ロジックや個別ドメイン処理だけを変更・調査するとき
- CLI lifecycle の外部挙動や共通 runner、ログ、preflight、completion に関係しない単体 helper を確認するとき
- テスト対象の正本仕様や実装詳細を直接確認する必要があるときは、対応する oracle または src の対象を先に読む

## hash
- 540f62c9a6b70104fa0f111a5fb9f483634abf7f4804e33d1d3caf7dbd82f76d

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
- Codex の sandbox argv が permission profile に依存しないことを検証する pytest。全 FileAccessMode で sandbox 引数のみを生成し、profile や権限関連 config・path 別例外入力が存在しないこと、実 Codex CLI が生成 argv を受理することを確認する。

## Read this when
- Codex override argv の生成・準備処理を変更またはレビューするとき
- sandbox、permission profile、権限関連 config の回帰を調査するとき
- Codex CLI に渡す sandbox 引数の互換性を検証するとき

## Do not read this when
- Codex override argv や権限設定に関係しない機能を変更・調査するとき
- Codex CLI の通常の出力品質や、別の実行経路のテストを確認するとき

## hash
- 7ca36ea288b94389652c5e77b19c60368c595ad6e1c51c477b55038b69f646a2

# `test_runtime_codex_profile.py`

## Summary
- Codex argv の model・sandbox・provider 上書き契約を検証するテスト。全 FileAccessMode の sandbox 変換、承認設定、model/reasoning 指定、不要な設定の非出力、未知 mode や未定義 provider の早期拒否、選択 provider の TOML argv 変換を扱う。関連する Codex 実行ルールと model/provider 仕様のテスト入口。

## Read this when
- Codex 起動時の override argv、sandbox、model、reasoning、provider 連携を変更・検証するとき。
- FileAccessMode の追加や provider 設定のシリアライズ、Codex CLI の TOML override 形式を調査するとき。

## Do not read this when
- Codex argv の構築や model/provider 上書きに関係しないテスト・実装を扱うとき。
- Codex 実行ルールの正本仕様そのものを確認する必要があり、oracle の仕様文書を直接読むべきとき。

## hash
- 542b624fa7880aef8adeab46f24328813cc41db9b742fc7f1645361ff45dcfe8

# `test_runtime_config.py`

## Summary
- CmocConfig と設定ランタイムのテスト。既定値、JSON 化時のキー順、設定ファイルの読み書き、欠落・破損・非通常ファイル・symlink へのエラー処理を検証する。
- Codex の model provider、model spec、reasoning effort、各種ループ回数などの入力型・値検証と、provider-local な JSON/TOML 値の保持・拒否を検証する。
- 設定の永続化境界で不正な in-memory 値を拒否し、recovery 試行回数を読み書きできることも確認する。CmocConfig の設定仕様やエラー処理、設定ランタイムを変更・検証するときの入口となる。

## Read this when
- 設定の既定値、JSON 変換、config.json の読み書き、入力検証、設定エラーの挙動を変更または調査するとき
- Codex model provider・model・reasoning effort の設定形式や provider-local 値の検証を確認するとき

## Do not read this when
- 設定ランタイムの実装詳細ではなく、oracle 側の設定仕様そのものを確認するときは oracle/src/oracle/other/cmoc_config.py を読む
- 設定以外の CLI、ACP、oracle review の挙動だけを扱うとき

## hash
- 24553394eaa0da9549ccc4c238db340ce698abf2916884db1e1acdc7a551859d

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
- FileAccessMode の永続化値が JSON schema 共有用の文字列として定義されていることと、各アクセスモードが Codex sandbox mode へ正しく変換されることを検証するテスト。

## Read this when
- FileAccessMode の値や file access mode から Codex sandbox mode への変換契約を変更・確認するとき。

## Do not read this when
- FileAccessMode の実装自体を変更するときは basic.acp の定義を直接確認する場合。
- Codex 実行時の sandbox 制約全般を確認するときは、対応する実行規則や変換実装を直接読む場合。

## hash
- 4115b2fd0a1a6350e8acec4a57b5a039c8f768d3660b0b75a0579ed96addb571

# `test_runtime_refactor.py`

## Summary
- realization refactor の永続 state 同期・検証・target 選択をテストする。oracle/realization file 集合の追跡、変更時の再調査判定、調査履歴保持、未調査・最古 entry の優先選択を扱う。
- path escape、directory・gitlink・欠落 file、特殊 path、dangling symlink、state schema 不正、symlink 経由の書き込み、非 UTF-8・NUL・非正規 timestamp などの安全性・入力検証も検証する。

## Read this when
- refactor state の同期、永続化、schema 検証、調査対象選択の実装またはテストを変更・レビューするとき
- oracle/realization file classifier の path 境界、git tree 判定、symlink 処理を確認するとき
- refactor state に関するテスト失敗の原因を調査するとき

## Do not read this when
- refactor state や file classifier の挙動に関係しない機能を変更・調査するとき
- INDEX.md のルーティングや正本仕様そのものを確認する必要があるときは、先に対応する oracle 文書を読む

## hash
- 016840c10e5059714ccb2d688ad0896ef616741ba182f8d59f39bcd757df12e4

# `test_runtime_state.py`

## Summary
- session/run state の永続化 schema と managed branch 解析に関する realization test。
- branch 形式からの session ID 解決、state file の読み込み・書き込み、JSON/UTF-8 不正値、必須値・型・未定義 field の検証を確認する。
- session 部分の独立読み込みと、process 間で共有される session fork lock の排他性も検証する。

## Read this when
- session state または run state の schema 検証を変更・追加するとき
- managed branch から state file や session ID を解決する処理を変更するとき
- session fork lock の process 間同期や関連する失敗時挙動を調査するとき
- runtime state 実装の変更後に対応する realization test を確認するとき

## Do not read this when
- CLI の一般的な session/run 操作や oracle の編集処理だけを調べるとき
- runtime state の実装詳細を直接確認したいときは、まず対応する実装ファイルを読むべき場合
- このテストが対象とする schema、branch 解析、lock 以外のテスト領域を調べるとき

## hash
- 73d0415c9047809d9548d219c67d6a3cd695c77deef51bfd69ddbc063171f813

# `test_session_cli.py`

## Summary
- session fork/join/abandon の CLI 外部挙動を統合的に検証するテスト。session branch と state の生成・更新・削除・復元、linked worktree、dirty worktree 拒否、cleanup rollback、join の conflict 解消、Codex sandbox・prompt 境界、エラー出力を扱う。session 状態遷移に関する回帰テストの入口。

## Read this when
- session fork、join、abandon の挙動や回帰を確認・変更するとき
- session state のライフサイクル、branch cleanup、linked worktree 対応を調査するとき
- session join の conflict 解消、Codex 呼び出し境界、エラー出力を確認するとき

## Do not read this when
- session CLI 以外のサブコマンドや、単体の内部 helper の実装だけを調査するとき
- session state の正本仕様を確認する場合は、まず対応する oracle 文書を読むとき

## hash
- 05fda609787853f37b99bf1a763df322a79683a455a09de5453a1cd39982ae48

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
