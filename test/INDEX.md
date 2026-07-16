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
- `test/_apply_support.py` の中で、apply セッション状態から managed worktree パスを復元する補助関数を置く。apply ブランチ文字列の分解と worktree 配置規則の対応を確認したいときに読む。

## Read this when
- apply セッション state から実際の worktree 位置を求める補助が必要なとき
- `cmoc/apply/.../...` 形式の branch 名と `.cmoc/gu/worktree/...` への対応を確認したいとき
- apply 系テストで、期待パスの組み立て規則を共有したいとき

## Do not read this when
- apply セッション state の保存形式そのものを確認したいときは、`oracle/doc/app_spec/session_state.md` を先に読む
- branch 命名や managed branch の役割を確認したいだけなら、`oracle/doc/branch_model.md` を先に読む
- worktree 生成や session/fork/join の主処理を追いたいときは、この補助ファイルではなく該当実装本体を読む

## hash
- 29a0e5787316dcc281e9c898ec982f71dd27db999f541f05ea765e652cd7fed4

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
- テスト用の Codex 実行支援ヘルパーをまとめたモジュール。認証済み Codex ホームの準備、Ollama 事前処理のスタブ、Codex 呼び出しパラメータ生成、CLI 引数・設定値の検査、実行オプションの固定化を提供する。Codex の subprocess 制御や runtime wrapper のテストへ進む入口。

## Read this when
- Codex 実行ラッパーのテストを追加・修正するとき
- Codex CLI 引数、設定上書き、sandbox、model、reasoning effort のテスト支援を確認するとき
- テスト内で CODEX_HOME や managed Ollama の外部依存をスタブ化するとき

## Do not read this when
- Codex 実行支援ではなく、実際の Codex 呼び出し実装を変更・調査するときは runtime_codex_exec や runtime_codex_tui を直接読む
- AgentCallParameter などの正本定義や型仕様を確認するときは oracle/src の定義を直接読む
- Codex と無関係なテスト fixture や共通テスト支援を調査するとき

## hash
- 2a8515946b334989ee0e95965cadc7bafb5786835ca189888876c758572d7649

# `_command_support.py`

## Summary
- テスト用に、現在の Python で起動する実行可能スクリプトを生成する補助が必要なときに読む。外部コマンドの代用品を短く作る責務を持つ。

## Read this when
- テストで外部コマンドの代わりになる Python スクリプトを作りたいとき。
- 生成したファイルに実行権限を付ける必要があるとき。
- `python` の先頭行と UTF-8 での書き込み方法を揃えたいとき。

## Do not read this when
- 通常のコマンド実行や引数処理の実装を探しているとき。
- 外部コマンドを直接呼ぶ実装や、本体ロジックの入出力を追いたいとき。
- テスト補助ではなく永続的な実装や設定の置き場を探しているとき。

## hash
- c323a18940f72ba8f1d3094378dbb64cd0af8f5a2bb7ecd997a90afcab28a81c

# `_git_support.py`

## Summary
- cmoc CLI の Git 状態テストで使う最小限のテストリポジトリ準備と、branch 名取得・tracked かつ ignored な oracle file の再現補助をまとめた共通ヘルパー。git 初期化条件、commit 可能な最小構成、`.gitignore` と tracked ignored file の作り方を確認したいときに読む。

## Read this when
- Git リポジトリを使うテストの土台をどう作っているかを確認したいとき。
- branch 名取得や、Git 設定・hook 依存を切ったテスト前提を共通化している理由を知りたいとき。
- tracked でありながら ignore される oracle file をテストで再現したいとき。

## Do not read this when
- cmoc の個別コマンドや制御ロジックそのものを追いたいときは、対応するコマンド実装やテスト本文を直接読む。
- Git 状態を扱わないテストや、単なるファイル操作のテストならここは不要。
- 既に用意されたテスト用 repo を使うだけでよい場合は、この共通ヘルパーの詳細は読まなくてよい。

## hash
- f6347792d38e055fd753ec111bf7f45dc692d4b4c9de916c26bea862583dd9e0

# `_ollama_support.py`

## Summary
- 本番と共有する管理 Ollama サービスを前提に、doctor コマンドをテストから実行するための共通ヘルパー。テスト用 SLM モデル定数と、対象 worktree をカレントディレクトリとして doctor を呼び出す入口を提供する。

## Read this when
- Ollama 連携や管理サービスを使う doctor テストを追加・修正するとき
- doctor の実行環境、固定エンドポイント、対象 worktree の指定方法を確認するとき

## Do not read this when
- doctor コマンド本体の仕様や実装を確認したいとき
- Ollama サービスの本番設定そのものを変更・調査するとき

## hash
- 282f5e743ce5a9253c28103a9ed999c8f8c8a5f09c801c63acb31bec1d727776

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
- indexing index entry builder のモデル・推論設定、読み取り専用実行、構造化出力スキーマの必須配列、互換公開面を検証するテスト。対応する正本の実装・スキーマを変更するときの挙動確認の入口。

## Read this when
- indexing index entry builder の parameter 設定や構造化出力スキーマを変更・レビューするとき
- 互換公開面やモジュールの __all__ を変更するとき

## Do not read this when
- indexing 以外の ACP builder parameter を変更するとき
- INDEX エントリー生成以外の機能や、対応する正本実装・スキーマを直接確認すべきとき

## hash
- 358121a135f54e2124b64ed1e3d0238c5fa2f0bf8c9e75e8c11439e73da44471

# `test_acp_builder_review_oracle_parameters.py`

## Summary
- review oracle ACP builder の parameter 生成、モデル設定、ファイルアクセスモード、structured output schema、互換公開面を検証するテスト。oracle 側 schema・builder との一致や symlink パス保持、動的 prompt テキストの保持も確認する。review oracle builder の挙動変更や検証失敗の調査におけるテスト入口。

## Read this when
- review oracle の ACP parameter builder、schema、prompt 生成、互換 export を変更または検証するとき
- review oracle の parameter や schema に関するテスト失敗の原因を調査するとき

## Do not read this when
- review oracle builder の実装詳細を直接変更・確認する場合は、対応する src ファイルを先に読む
- oracle 側の schema や builder の正本仕様を確認する場合は、対応する oracle/src ファイルを直接読む
- review oracle と無関係な ACP builder やテストを扱う場合

## hash
- 6949279cd32e99eb4d9d4d9617d7d70559b61f00c07388c1ec14da5a8ecd90cb

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
- TUI の resolve parameter builder が、元の依頼文と必要な運用規約をプロンプトへ埋め込み、効率優先・最大推論・読み取り専用の実行パラメータと構造化出力スキーマを返すことを検証するテスト。
- スキーマの必須項目、論理 enum・boolean 型、追加プロパティ禁止、およびモジュール公開 API が要求された名前だけで構成されることも確認する。

## Read this when
- TUI の resolve parameter builder、出力スキーマ、プロンプト埋め込み、実行パラメータ、または公開 API を変更・調査するとき。

## Do not read this when
- TUI の resolve parameter builder やそのスキーマの挙動を扱わず、他の ACP builder または無関係なテストだけを変更・調査するとき。

## hash
- 74e371fa03f41a56b490e072cd706b250a2db315f3772336bc16acc5165f2eb1

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
- apply fork CLI の回帰テスト群。Codex loop 実行後の state・branch・worktree 更新、割り込み時の commit 保持と未確定差分破棄、linked worktree 起点、doctor preprocess の順序、.gitignore、設定修復・失敗、対象編集、state ライフサイクル、競合検出、初期化失敗からの abandon 復旧を検証する。apply fork の CLI ライフサイクル、永続状態、Git worktree、gitignore 挙動を確認する際のテスト入口である。

## Read this when
- apply fork サブコマンドのライフサイクル、state 遷移、branch/worktree 作成・破棄、割り込みや初期化失敗の復旧を変更・調査するとき
- apply fork の doctor preprocess、設定読み込み・修復、.gitignore 対応、対象ファイル編集、競合時の事前条件を変更・検証するとき
- apply fork の CLI 回帰テストや共有 repository/session fixture の挙動を確認するとき

## Do not read this when
- target normalization の独立したテストだけを変更・調査するとき
- apply fork 以外のサブコマンドや、CLI ライフサイクル・apply state・Git worktree に関係しない処理を確認するとき

## hash
- 82cb2d878d427f1fa5b1f86791cf0fa878d95fdfbf8e8fabe72e39acc2890790

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 統合テスト。レビュー・修正ループの収束／未収束／error、変更ファイルの再検査、rolling fork の対象 commit 制御を検証する。
- 生成される report の front matter、所見数推移、変更内容要約、変更 path、commit 前の差分、未追跡ファイルの扱いを検証する。
- apply fork の report schema や変更要約の挙動を確認・変更する作業の入口となる。

## Read this when
- apply fork の収束判定、再検査対象、rolling fork の差分範囲を確認するとき
- apply fork report の内容、変更要約、error 時の未 commit 差分を確認するとき
- apply fork CLI の統合挙動や関連テストを変更するとき

## Do not read this when
- apply fork のレビュー・修正実装そのものを確認する場合は、先に対応する src の実装を読むとき
- apply fork と無関係な CLI、session、report の挙動を調査するとき

## hash
- 78637b02f45adb548cbd4c0811d41b33089410f9a09a23ce9d8116fdd6a02b14

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
- apply join の CLI 経由テスト。apply worktree と session の結合、後片付け、state・report 更新、実行場所による cleanup の違いを検証する。
- stale または別 session の branch、lock 中の state 変更、error state のプロセス、dirty worktree、想定外差分、rename・削除・symlink・ignored path の分類、merge conflict と force-resolve の挙動を扱う。apply join の成功条件・拒否条件を確認するためのテスト入口。

## Read this when
- apply join の成功・拒否条件や CLI 出力を変更・調査するとき
- apply worktree、session branch、state、report、cleanup の連携を変更するとき
- 想定外差分の分類、force-resolve、INDEX.md 以外の merge conflict 処理を変更するとき

## Do not read this when
- apply join 以外のサブコマンドの挙動だけを変更・調査するとき
- 単体の実装詳細や共通 fixture の変更で、apply join の外部挙動・境界条件を確認する必要がないとき
- apply join の正本仕様を確認したいときは、先に oracle/doc/app_spec/sub_command/apply_join.md を読む

## hash
- b49c851181d6c17487f43a4e6cd05c0969177f89223913d90b00d02bcde07dff

# `test_basic_runtime.py`

## Summary
- Root/worktree と path model の runtime 契約を検証するテスト。root placeholder の解決、repo root と linked worktree の区別、pushd の cwd 直列化、managed worktree の作成・削除におけるパス境界・symlink・未登録パス拒否、および Git 設定分離を扱う。

## Read this when
- path placeholder、repo root、run/work root、linked worktree、pushd の挙動を変更・検証するとき
- managed worktree の作成または削除に関するパス検証・安全性を変更・検証するとき
- テスト用 Git repository の global config や hook の影響を確認するとき

## Do not read this when
- CLI の個別コマンド仕様や一般的な path utility の実装だけを確認するとき
- worktree の作成・削除や runtime の cwd 制御に関係しないテストを調査するとき

## hash
- 2ba2ec4bb9e2eaa83fdf73d982c633737c062ff17b0a3766100cf8960240c45b

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
- Codex CLI 実行ランタイムの統合テスト。実際の Codex 呼び出しまたはスタブを用いて、argv、stdin、sandbox、model/provider override、JSON schema、ログ・出力、リポジトリ書き込み、CODEX_HOME 設定未生成を検証する。
- local SLM 利用時の managed Ollama preflight と Codex override 構築を検証する。Codex 実行経路、provider 設定、モデル選択、出力 schema の挙動を変更・調査する際のテスト側の入口。

## Read this when
- Codex CLI の実行引数、stdin 渡し、sandbox モード、モデルまたは provider override を変更・検証するとき
- managed Ollama を使う local SLM 実行や preflight の呼び出し条件を変更・検証するとき
- Codex 実行結果の schema、call log、prompt log、output path、リポジトリ書き込みを検証するとき
- CODEX_HOME に設定ファイルを生成しない契約を確認するとき

## Do not read this when
- Codex 実行ランタイム自体ではなく、一般的な Codex 設定モデルや CLI パラメータ型の実装だけを調べるとき
- doctor の managed Ollama 起動・提供処理そのものを変更・検証するときは、まず doctor 実装または専用テストを読むとき
- Codex 以外のサブコマンドや無関係な入出力処理を調べるとき

## hash
- 3f69fc2e1875f6626195246a9e076f88cfc6aeb279e5abb188f8f52952c33828

# `test_codex_runtime_home.py`

## Summary
- Codex 実行時の CODEX_HOME 解決と認証情報の事前検証を検証するテスト。未設定時の既定値、相対パス、環境変数の保持、Codex CLI 起動前の異常終了を扱う。

## Read this when
- Codex 実行環境の home ディレクトリ解決や auth.json 検証を変更・レビューするとき
- Codex CLI が不正な環境で起動されないことを確認するとき

## Do not read this when
- Codex 実行処理そのものや CLI 引数構築を変更・調査するとき
- Codex home 以外の実行結果・リトライ・ログ仕様を確認するとき

## hash
- de2dd9c21179c0180f12976f3fad22355fca0429820470e45e7488ae569df0b5

# `test_codex_runtime_paths.py`

## Summary
- Codex exec の実行パスと権限境界を検証するテスト。並列実行時の timestamp 予約、cwd の選択、pure-oracle read の read-only sandbox、schema 状態の repo root 保存、`.agents` パスの権限注入禁止を扱う。runtime_codex のパス生成・実行引数・worktree 対応を確認するテスト入口。

## Read this when
- Codex exec のログ・prompt・stdout・stderr・output の timestamp 付きパスや並列実行時の衝突回避を変更・調査するとき
- Codex exec の cwd、linked worktree、output schema 保存先を変更・調査するとき
- FileAccessMode と Codex sandbox 引数・権限設定の変換を変更・調査するとき

## Do not read this when
- Codex exec のプロンプト本文生成や oracle file の探索規則だけを変更・調査するときは、対応する prompt builder の実装・テストを直接読む
- Codex exec の実行結果解析やエラー処理だけを変更・調査するときは、runtime の結果処理を直接読む

## hash
- c167fd067b11e2c05e6a282d2edd8b5b6f128a91376ddc942e659f4f496d2960

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex quota exceeded 後の quota probe・待機・復帰・再実行を検証する回帰テスト。resume token の復元、代表 probe の共有、並行呼び出し、ログ・subcommand log、CODEX_HOME/cwd、失敗時伝播まで同一の quota retry 状態機械として扱う。

## Read this when
- Codex exec の quota 待機、probe、resume、再実行の挙動を変更・調査するとき
- quota retry の並行性、ログ記録、resume token、CODEX_HOME/cwd の回帰を確認するとき

## Do not read this when
- quota retry や Codex exec の外部挙動を扱わず、別のサブコマンドやテスト領域だけを変更・調査するとき
- quota probe の実装詳細そのものを確認したい場合は、先に quota probe adapter の実装・正本仕様を読むとき

## hash
- cb13c67475165e6aa89903b8550f9e2a93482714fa790ef5617e8f1662ffc3a1

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
- Codex subprocess runtime の追跡・終了制御を検証する pytest。専用プロセスグループの記録、member pidfd を使ったシグナル送信、SIGTERM の遅延、leader 終了後や割り込み後の child tracking 維持、継承された apply tracking 環境変数の無視を扱う。関連する subprocess 実装の挙動確認と変更時の回帰テストとして読む。

## Read this when
- Codex subprocess の process group、pidfd、シグナル処理、apply 用プロセス追跡を変更・調査するとき。
- KeyboardInterrupt や leader 終了後に descendant を追跡する cleanup 挙動を確認するとき。
- Codex 起動時の APPLY_PROCESS_TRACKING_ENV の扱いを確認するとき。

## Do not read this when
- apply サブコマンドの仕様そのものを確認したいときは、先に oracle/doc/app_spec/sub_command/apply_abandon.md を読む。
- Codex subprocess の実装詳細を変更しない通常の CLI 機能や、別の入出力処理を調査するとき。

## hash
- 3abf68012089ad162631753b1970173035861649bb11ae5ad4bde49838a3983b

# `test_codex_runtime_tui.py`

## Summary
- Codex TUI 実行ラッパーの統合テスト。完成済み prompt の読み込み、作業ディレクトリ・sandbox・アクセスモードなどの CLI 引数、call log とサブコマンドイベントの成功・失敗記録、timestamp 衝突時のログ保持、CLI 不在・KeyboardInterrupt・非 0 終了時のエラー処理を検証する。

## Read this when
- Codex TUI の実行引数やファイルアクセス境界を変更・確認するとき
- Codex 呼び出しの call log、コンソール要約、サブコマンドイベントの仕様を変更・確認するとき
- Codex CLI 不在、割り込み、非 0 終了などの失敗時挙動を変更・確認するとき

## Do not read this when
- Codex TUI 以外のサブコマンドや、Codex 呼び出しを伴わない機能を扱うとき
- prompt 生成そのものの仕様を確認する場合。prompt の正本仕様と生成実装を直接読むべきとき
- ログ形式全般を確認するだけで、TUI 呼び出し固有の挙動を扱わないとき

## hash
- c15e9a5767b35735dc6acba5b7df6ca72ec69371c3db59c5ad7dd135cd774c94

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
- `cmoc indexing` の CLI と preflight、worktree 対象判定、doctor による初期化、INDEX.md 生成、Codex structured output 呼び出し、hash による再生成省略、INDEX.md 限定 commit、既存差分・git diff 異常時の拒否を外部挙動として検証するテスト。

## Read this when
- `cmoc indexing` の CLI 挙動や事前条件を変更・調査するとき
- INDEX.md の生成・更新・hash 判定・Codex 呼び出しを変更するとき
- worktree、doctor、preflight、commit 対象パスの制御を変更するとき
- indexing 関連の失敗時挙動やテストカバレッジを確認するとき

## Do not read this when
- INDEX.md のルーティング生成規則そのものを調査するときは、対象の oracle doc と Structured Output schema を直接読む
- indexing 以外のサブコマンドや、CLI から独立した共通処理だけを変更するとき
- Codex 出力品質や LLM の内容自体を検証したいとき

## hash
- e81a545020cd42279e27feb63cc9d6b9e40767d24c581a4f56175d2e39768388

# `test_indexing_common.py`

## Summary
- `commons.indexing` の INDEX エントリー描画・解析・更新とディレクトリ走査を、CLI ライフサイクルから分離して直接検証するテスト。入力スキーマ検証、ハッシュ再利用と不正エントリー再生成、空ディレクトリ、安定した兄弟順序、並列更新、サブコマンドログ伝播、memo 配下の走査方針、シンボリックリンク循環回避を扱う。

## Read this when
- INDEX.md の生成・更新、エントリー入力検証、ハッシュ判定、ディレクトリ traversal、並列 worker、関連ログ伝播の挙動を変更または調査するとき。
- `commons.indexing` の外部挙動や制御ロジックをテストケースから確認するとき。

## Do not read this when
- CLI の引数解析やサブコマンド lifecycle だけを変更・調査するとき。
- Codex の出力品質そのものや、INDEX 生成以外のログ機能だけを確認するとき。

## hash
- e5828e6724da053456ce98b3f1ef2f1af15411f71679509f05db15fb993579ca

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

# `test_prompt_parts.py`

## Summary
- 標準 prompt parts と complete prompt の組み立て結果を検証する pytest テスト。各標準文書の型・タイトル・主要文言、ファイルアクセスモード別の内容、complete prompt への標準文書の包含・省略、root placeholder の保持を確認する。prompt builder の標準文書生成や完全 prompt の構成を変更・調査する際の検証入口。

## Read this when
- prompt parts の標準文書生成を変更するとき
- complete prompt に標準文書を追加・除外する挙動を変更するとき
- ファイルアクセスルール、root token、INDEX entry standard、realization standard のテストを確認するとき
- prompt builder 関連の回帰テストを実行・修正するとき

## Do not read this when
- prompt builder や標準文書生成に関係しない機能を変更するとき
- CLI の実行フローや個別サブコマンドの挙動だけを調査するとき
- テスト対象の実装本文を直接確認すべき場合は、対応する prompt builder の実装ファイルを先に読むとき

## hash
- 9a26cba6c98e4976b43f74dc43b0673255115bc1685adca4c2af09681e747adc

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
- review oracle の finding path 解決と oracle 対象列挙を検証するテスト。相対・絶対・placeholder・symlink の扱い、session/full scope の対象範囲、追跡済み・ignored ファイル、fork commit 基準、除外対象の分類、no_targets 出力を確認する。

## Read this when
- review oracle の対象ファイル列挙、scope、finding path 解決、symlink 分類を変更または調査するとき
- oracle file の追跡・ignore 判定や review fork 差分の挙動を検証するとき

## Do not read this when
- review oracle の path 解決や対象列挙に関係しない review 機能を変更・調査するとき
- CLI の別サブコマンドや一般的な oracle 仕様だけを確認するとき

## hash
- 152b4eadfe2fe41a04daf12e158d837fed7733e2b1f0c6d95f234fa8274b09df

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
- apply runtime の process tracking と停止契約を、CLI を介さず低レベル API で検証するテスト。pid file、advisory lock、pidfd、PID reuse、process group、親終了後の child group 再読込、停止時 warning と signal 挙動を扱う。apply abandon の CLI 外部挙動は対象外で、CLI テストへ進むための境界を示す。

## Read this when
- apply runtime の process tracking、pid file 読み込み、advisory lock 待機、pidfd による停止、PID reuse 防止、process group 停止を変更・検証するとき。
- 親 apply process や記録済み Codex child process の停止順、競合終了、warning 合成の挙動を確認するとき。

## Do not read this when
- apply abandon コマンドの CLI 引数・終了コード・標準出力など外部挙動を確認するときは、CLI 外部挙動を扱う test_apply_abandon_cli.py を直接読む。
- process tracking や停止契約に関係しない機能のテストを調べるとき。

## hash
- c5f5acc3f5ad79da4dd9d941913966d17c1b0ae3700c63da2cab65cdc3d16f59

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
- Codex の sandbox argv が permission profile や path 別権限設定に依存しないことを検証する pytest。全 FileAccessMode での argv/config 制約、builder API の引数固定、worktree 内容に対する不変性、実 Codex CLI parser での sandbox 引数受理を扱う。runtime_codex_permissions 周辺の実装変更に対する回帰テストの入口。

## Read this when
- Codex override argv の sandbox、permission profile、権限設定注入を変更・調査するとき
- prepare_codex_override_args または build_codex_override_args の API や worktree 内容への依存性を変更・検証するとき
- Codex CLI の sandbox 引数互換性に関するテスト結果を確認するとき

## Do not read this when
- Codex の権限 argv や runtime profile と無関係な機能を変更・調査するとき
- Codex override の実装詳細を直接確認したい場合は、先に runtime_codex_profile の実装を読むべきとき

## hash
- 5af6d2cdbd685fe2cf07871ca0b76b972552bfac0258bc5b63bb0b7c3a087916

# `test_runtime_codex_profile.py`

## Summary
- Codex argv の model、sandbox、provider 上書き契約を検証するテスト。全 FileAccessMode の sandbox 変換、未知 mode の拒否、通常 provider での worktree 非走査、ローカル SLM 用 Ollama provider 設定を扱う。runtime_codex_profile の変更や Codex 起動引数・provider 設定の挙動確認に進む入口。

## Read this when
- Codex の model・sandbox・reasoning effort 上書き引数を変更または検証するとき
- FileAccessMode と Codex sandbox の対応、未知 mode のエラーを確認するとき
- cmoc 管理 Ollama provider の argv・設定変換を変更または検証するとき
- Codex argv 構築時の worktree 非走査契約を確認するとき

## Do not read this when
- Codex argv、sandbox、provider 上書き処理に関係しない機能を変更または調査するとき
- 実装の詳細を確認する必要があり、commons/runtime_codex_profile.py や関連 oracle file を直接読む方が適切なとき

## hash
- 44c5dd4666a816f9c272c567361aa1447d6594f24ae88aa17434b932bdc2f579

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
- - `runtime_content` の binary 判定ロジックを検証するテストがある。
- - `commons.runtime_content.is_binary` が、通常のテキストと NUL 文字を含む内容を区別できるかを確認する。

## Read this when
- - `commons.runtime_content.is_binary` の判定条件を変更したとき。
- - binary file を除外する前提で、content 判定の仕様や境界を確認したいとき。
- - `is_binary` のテスト観点を追加・修正するとき。

## Do not read this when
- - runtime content 以外の indexing 手順やファイル列挙の仕様だけを確認したいとき。
- - binary 判定の実装詳細ではなく、別の入出力変換や CLI 挙動だけを変更したいとき。
- - `commons.runtime_content` とは無関係な parser や storage のテストを探しているとき。

## hash
- d0a6ee98df2dc2e19e83563047de66dd0a364e93a73abb40bf342b21797aeb2f

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
- cmoc managed ollama の利用可能性確認に関する実装を検証するテスト。サービス修復、systemd サービスファイルの生成、待受プロセスの一致判定、モデルの pull と再確認、GPU 推論確認の境界を読む入口になる。

## Read this when
- cmoc managed ollama の起動・修復・検証ロジックを変更する時
- systemd サービスの再起動条件やサービスファイル内容を変える時
- モデルの取得確認や GPU 推論確認の扱いを直す時
- cmoc managed ollama の HTTP 応答確認や待受プロセス判定の失敗条件を調べる時

## Do not read this when
- 一般的な CLI 起動や引数解決だけを直す時
- codex profile や doctor の他の検証だけを見たい時
- ollama 以外の runtime テストを探している時

## hash
- 6a1dd3b311012c4c1311448d7fbcfb316addf1a0fa632a24ad883138beced2f9

# `test_runtime_state.py`

## Summary
- session/apply state の形状検証、branch 名からの session ID 解析、branch に対応する state 読み込み、session fork lock の process 間排他を検証するテスト。runtime state や session fork の挙動を変更・調査するときの入口。

## Read this when
- session/apply state のフィールド型・null 許容・不正入力エラーを確認するとき
- session/apply branch の形式検証や state 読み込みを変更・調査するとき
- session fork lock の repository 単位の process 間直列化を確認するとき

## Do not read this when
- session/apply の CLI 操作そのものや branch 作成・join の実装を確認したいときは、対応する oracle doc または realization implementation を直接読む
- runtime state と無関係なテストや、Codex CLI・LLM の出力品質を調べるとき

## hash
- 22b1f87c9f35afd65af5720151a23a425df5df6117418949ab1a1e5357705c30

# `test_session_cli.py`

## Summary
- session fork/join/abandon の CLI 外部挙動を一体で検証する回帰テスト。session branch・state のライフサイクル、linked worktree、競合解消、cleanup、preprocess、dirty worktree 拒否、エラー出力を扱う。

## Read this when
- session サブコマンドの fork、join、abandon の挙動や session state 遷移を変更・調査するとき
- linked worktree、branch/state cleanup、merge conflict 解消、Codex sandbox 境界を変更・検証するとき
- session CLI の成功時・失敗時出力やロールバックを確認するとき

## Do not read this when
- session CLI や session state に関係しない機能を変更・調査するとき
- session サブコマンド内部の単体ロジックだけを確認する場合は、対応する src またはより限定されたテストを先に読むとき

## hash
- 555e736ed0a207aac66175d34c09ae97f374336d528861c8202a244be7036632

# `test_struct_doc_rendering.py`

## Summary
- `basic.struct_doc` の Markdown 変換結果を直接検証するテスト群。改行の圧縮ルールと、`StructBlock` を含む再公開経路の互換性を確認したいときに読む。

## Read this when
- StructDoc の Markdown 出力で空行のまとまり方を変えた可能性があるとき。
- `basic.struct_doc` から公開している `StructBlock` の同一型互換を確認したいとき。
- `{{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py` に対応する整形挙動の受け入れ条件を確かめたいとき。

## Do not read this when
- StructDoc のモデル定義やレンダリング実装そのものを追いたいときは、`basic.struct_doc` 側の実装を直接読む。
- Markdown renderer 以外の prompt builder 部品の仕様を確認したいときは、このテストではなく各部品の対応テストを読む。
- 表示フォーマット全体の設計意図を知りたいだけなら、テストではなく正本側の断片を読む。

## hash
- f16ef862a02a20b4d232381063b11b5da58d01b18234266e802a93b5cc2f07fe
