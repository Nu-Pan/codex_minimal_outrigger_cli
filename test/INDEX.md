# `_acp_builder_support.py`

## Summary
- ACP builder テストから、正本 schema への参照 path を一貫して組み立てるための共通補助を集める。テスト側で schema ファイルの実体を直接複製せず、oracle 側の定義を参照する前提を支える。

## Read this when
- ACP builder 系テストで、oracle/src/oracle/acp_builder 配下の schema ファイルを参照する path が必要なとき。
- テスト実装で、正本 schema の場所を組み立てる方法を 1 か所に寄せたいとき。

## Do not read this when
- ACP builder 以外のテストや実装で、oracle schema 参照が不要なとき。
- schema の内容そのものや、各テスト対象の個別仕様を確認したいとき。

## hash
- dc4d17530938ad5f6e6f02b8dbc3c5aedf5043898414e8da6fab7fbd51965305

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
- Typer CLI を共通の `CliRunner` で呼び出すための test support です。CLI の外部挙動テストで、複数の test module から同じ runner を使いたいときに参照します。

## Read this when
- CLI コマンドを共通の runner で invoke する test を追加・更新するとき。
- Typer の CLI 出力や exit code を、他の CLI test と同じ呼び出し経路で確認したいとき。

## Do not read this when
- CLI 以外の実装や、独自の invoke 設定を使う test を作るとき。
- 個別の command helper やテスト用 repository fixture を探しているとき。

## hash
- 33b0c8871904c2ecfda13d625de6c4970ac753a13c325110e0e1f1fd986aa0fc

# `_codex_support.py`

## Summary
- Codex 実行ラッパーのテストで共有する補助関数と最小 fake result を提供する。認証済み Codex ホームの準備、Ollama preflight のスタブ、AgentCallParameter の生成、Codex CLI 引数・設定上書き値の検査、実行/TUI 共通の override 引数スタブを扱う。

## Read this when
- Codex 実行ラッパーまたは TUI の subprocess 引数構築テストを追加・修正するとき
- Codex の認証環境、作業ディレクトリ、sandbox、model、reasoning effort、設定上書きのテスト補助が必要なとき
- 共有 fake Codex 結果や managed Ollama preflight のテストスタブの利用方法を確認するとき

## Do not read this when
- Codex 実行処理や TUI の本体実装を変更・調査するとき
- 共有テスト補助ではなく、個別の機能ロジックや oracle 仕様を確認するとき
- Codex CLI 引数構築以外のテストで、このファイルの補助関数を使わないとき

## hash
- be887fd655f1a9968a988597d78cdae7ecee13d49c6637669f18efa0547a9afe

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
- `cmoc` のテストから、prod と共有する managed Ollama を使った実行を共通化する補助モジュール。`doctor` のように実サービス前提の経路をテストするときに読む。
- テスト用の固定 SLM 名、`doctor` の実行コンテキスト切り替え、`click` 実行結果の成功確認をまとめて扱う。Fake サービスの起動やライフサイクル制御を探す場所ではない。

## Read this when
- Real Codex CLI 経路のテストで、共有する managed Ollama を使う前提を確認したいとき。
- `doctor` を対象に、cwd を切り替えて実行するテスト補助を探しているとき。
- テストで使う SLM 名と、`click.testing.Result` を返す実行ラッパーの境界を知りたいとき。

## Do not read this when
- Fake Codex CLI やモック中心のテスト方針を確認したいときは、より上位のテスト規約を見る。
- managed Ollama のサービス管理、配置先、再起動条件を知りたいときは `cmoc_managed_ollama` の正本を見る。
- `doctor` コマンド自体の仕様や実行手順を知りたいときは `cmoc doctor` の正本を見る。

## hash
- 0a7df68374a0b70abaceee4ad0c60a25ce377b65970b001aa5098fb816136275

# `test_acp_builder_apply_parameters.py`

## Summary
- `cmoc apply fork` の parameter 生成と正本 schema 参照を検証するテストを扱う。`change_summary` と `file_review_and_fix` の import 契約、prompt 組み立て、root の使い分け、相対パスの受理/拒否を確認したいときに読む。

## Read this when
- `cmoc apply fork` の各 builder が正本 schema と対応しているかを確認・変更するとき。
- packaged layout での import 契約や、builder が返す prompt の共通文面を検証したいとき。
- `repo-root` と `work-root` の使い分け、`target-path` の解決、相対パスの扱いを確認したいとき。
- `change_summary` または `file_review_and_fix` の parameter 生成を調べるとき。

## Do not read this when
- apply ループ本体の実行制御、状態遷移、レポート生成を確認したいときは、対応する実装や上位の仕様を読む。
- 所見の抽出ロジックや修正判断の内容を追いたいときは、このテストではなく各 builder の実装側を読む。
- `cmoc apply fork` 以外のサブコマンドの parameter や schema を調べたいとき。

## hash
- fb46374903988f4efc4849fbb1e0bfeb15e1cd7ad5e9cd0291c6e0bbe7005078

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
- `test/test_acp_builder_review_oracle_parameters.py` は、review oracle ACP builder の各 parameter builder が返す公開面を固定する回帰テスト群。ここではモデル種別、推論強度、ファイルアクセス制御、structured output schema、互換公開モジュールの export 範囲、prompt 内の置換保持を確認する。
- 同じ review oracle 系の別テストではなく、この 1 ファイルを読むべきなのは、parameter builder の互換性と schema 一致を横断して検証しているから。個別の builder 実装や schema 本体を追う前の入口として使う。

## Read this when
- review oracle ACP builder の公開パラメータが変わったか確認したいとき。
- `__all__` の export 範囲、prompt に残すべきプレースホルダ、structured output schema の一致を変えた可能性があるとき。
- review oracle まわりの互換性回帰を、このテストがどこまで守っているかを把握したいとき。

## Do not read this when
- review oracle の実装ロジックそのものを追いたいだけなら、対応する `src/acp/builder/review/oracle/` 側を先に読む。
- schema の正本内容だけを確認したいなら、oracle 側の schema 定義を直接読む。
- 他の ACP builder 分野の parameter 仕様を見たいときは、このファイルではなく該当分野のテストへ進む。

## hash
- f28ac32f2a381f2b5ac50d8566e682e78ec7870580f6a17ef2ffeb2d47be01eb

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
- TUI の実行パラメータ選定を担う `resolve_parameter` 実装と、その出力 schema を確認したいときに読む。プロンプトへ何を埋め込むか、出力パラメータの型と公開名を固める対象。

## Read this when
- `build_tui_resolve_parameter_parameter` の出力内容、埋め込まれる元プロンプト、利用するモデル設定やファイルアクセス設定を確認したいとき。
- TUI 向けの structured output schema と、公開される名前が最小構成になっているかを確認したいとき。

## Do not read this when
- TUI の起動手順や画面制御だけを見たいときは `launch_tui` 側を読む。
- TUI 以外の ACP builder のパラメータ生成や、一般的な prompt 生成規約だけを見たいとき。

## hash
- 87985407de4b67a693a94776f23ef0d76bb425c2fe1c0c3b4503192528c51378

# `test_apply_abandon_cli.py`

## Summary
- `apply abandon` の外部挙動を固定する CLI テスト群。worktree・branch・state の cleanup、実行位置の扱い、実行中 process の停止、破損状態や別 session 混入の拒否を確認したいときに読む。

## Read this when
- `apply abandon` の成功時・警告時・失敗時の見え方を変える変更をする。
- apply run の state 遷移や、cleanup 前後で残る/消える repo 状態を確認したい。
- `apply` 系 CLI から実行位置をまたいで破棄できるか、または process 停止を伴うかを確認したい。

## Do not read this when
- low-level な process helper の契約を直したいだけなら、ここではなく `test_runtime_apply.py` を読む。
- `apply fork` の生成ロジックだけを変えるなら、破棄側の外部挙動確認は優先度が低い。
- 内部実装の分割や helper の配置を見たいだけなら、このテスト本文ではなく対象の実装ファイルを読む。

## hash
- 1b91b6f5b69cbfe334b359dba4c9fd95cb74dd82c5e02175bee11c8f3d16bac2

# `test_apply_fork_cli.py`

## Summary
- `apply fork` CLI の回帰テスト群。セッション作成後の apply ランの開始・完了・中断、単一レビュー・修正 call、state/worktree 更新、`doctor` 前処理、`.gitignore` 反映、config 読み込み失敗と復旧、初期化失敗後の `abandon` 回収までを確認する。
- CLI の lifecycle と repository/session fixture を使うので、このファイルを読む。target 正規化のように CLI 全体の状態遷移を要さない観点は別テストへ分ける。

## Read this when
- `apply fork` の開始条件、終了条件、state ファイル、worktree、process id、report 生成のどれかを変えるとき。
- `doctor` の事前処理順、`.gitignore` の追跡除外、linked worktree からの開始点、Ctrl+C 時の挙動を確認したいとき。
- apply run の失敗復旧や `abandon` の扱いを変更するとき。

## Do not read this when
- target path の正規化だけを変えるときは、このファイルではなく target 正規化側のテストを見る。
- apply fork 以外のサブコマンドや共通 helper のみを変更するときは、まずその責務の近いテストを読む。
- CLI lifecycle や repository/session fixture に触れない単発の所見生成ロジックだけを変えるときは、より局所的なテストを読む。

## hash
- 53494a7efc93b28510e24d010cda6fb27de70e23543443f6df10efa1f3a11d75

# `test_apply_fork_report_cli.py`

## Summary
- `apply fork` の report 生成と再検査ループの外部挙動をまとめて追う回帰テスト群。単一 call 後の再調査、空所見差分の拒否、変更要約、収束/未収束/error の判定、rolling apply の対象切り替え、session state 更新までを CLI 境界で確認する。
- report に出る result、所見数の推移、変更内容要約、commit message、session state の更新順や表示内容を変えるときに読む。
- 変更差分の抽出条件として、未追跡 file、削除済み tracked file、commit 前の working tree 差分をどう report に反映するかを確認したいときに読む。

## Read this when
- `apply fork` の report 文面や保存先、再検査の収束条件、rolling apply の対象決定を変えるとき。
- レビュー・修正後に再調査対象が増えるか、空所見で収束するか、所見あり差分なしで未収束になるかを確認したいとき。
- 変更要約がどの差分を拾うか、どの path を report に残すかを確認したいとき。

## Do not read this when
- `apply fork` の引数や開始前の前提条件だけを見たいなら、より広い `apply fork` CLI テスト群を読む。
- 対象 path の正規化だけを見たいなら、このテスト群ではなく対象正規化専用のテストを読む。
- `apply join` や `review oracle` の report を変えたいなら、それぞれのコマンド側のテストを読む。

## hash
- 598834575d3ee6a610ebaa43b636070a541ca1635b05c489258e8c7c8657a85b

# `test_apply_fork_target_normalization.py`

## Summary
- `sub_commands.apply.fork` の対象正規化で、`oracle` / `realization` / 管理領域 / ignored / symlink / binary の扱いを確認したいときに読む回帰テスト。対象外のファイル種別や状態をどう落とすかより、残すべき境界条件の判定を知るための入口。

## Read this when
- apply fork の対象候補の正規化結果を変える修正をするとき。
- `memo` や `.cmoc`、`.agents`、`INDEX.md`、`AGENTS.md` の扱い、tracked ignored file、symlink、binary file の扱いに関わるとき。
- `normalize_apply_targets` や `dedupe_apply_targets` の判定境界を確認したいとき。

## Do not read this when
- apply fork の実行ループ、レポート生成、状態遷移そのものを変えるときは、`cmoc apply fork` の本体仕様側を読む。
- `oracle` 側の基本定義そのものを確認したいだけなら、対応する正本仕様断片を先に読む。
- 対象正規化ではなく、引数解釈やコマンド全体の入出力を見たいだけなら、このテストより上位の CLI 仕様を見る。

## hash
- f9920c524764405fbddeb33be4cbbbdb60a68e9acd39be3c7ddca1d1e0eb7f4e

# `test_apply_join_cli.py`

## Summary
- `apply join` の CLI 挙動を検証する統合テスト群。apply worktree の cleanup、state 更新、report 生成、dirty worktree、想定外差分、merge conflict、force 復旧、path 分類の境界を確認したいときに読む。
- 同じ join 操作でも、session/worktree の起点や cleanup 可否、差分分類、競合処理のどれを確かめたいかでこのファイルを入口にする。CLI の外部挙動をまとめて見るための場所であり、個別 helper の実装確認には向かない。

## Read this when
- `apply join` の成功条件・拒否条件・force 時の戻し方を CLI から確認したい。
- apply worktree と session worktree のどちらを cwd にした場合でも join がどう振る舞うかを見たい。
- state 更新、report 出力、tracked process 停止、merge conflict の扱い、想定外差分の分類基準を確認したい。

## Do not read this when
- `apply join` の実装ロジックそのものを追いたい場合は、CLI 本体の実装側を見る。
- 一般的な差分分類や path 判定の規則だけを知りたい場合は、対応する仕様断片を直接読む。
- session fork や apply fork の流れだけを確認したい場合は、それぞれの fork 系テストを読む。

## hash
- 70d84017d9c0510246caedf759c2947ab3d52246324a5834a57183b5db18dd43

# `test_basic_runtime.py`

## Summary
- `basic.path_model` と `cmoc_runtime` の実行時契約を、`make_repo` を使った実リポジトリ操作込みで確認する統合テスト群。RootPathPlaceHolder の解決、repo/root/run/work の境界、pushd の cwd 排他、run worktree の作成・削除の拒否条件を読むときに進む。

## Read this when
- root/worktree の解決規則や、run isolation の境界が壊れていないかを確認したいとき。
- Git worktree の登録状態、symlink 混入、main worktree と linked worktree の扱いなど、実行環境依存の制御が正しいかを見たいとき。
- `basic.path_model` と `cmoc_runtime` をまたぐ振る舞いを、個別実装ではなく結合点で確認したいとき。

## Do not read this when
- 純粋な path 変換の仕様だけを追いたいなら、`oracle/src/oracle/other/path_model.py` 側を先に読む。
- run isolation の文章仕様だけを確認したいなら、`oracle/doc/app_spec/run_isolation.md` を読むほうが直接的。
- 個別のサブコマンド実装や、Git 操作の詳細挙動を追いたいだけなら、このテストファイルは後回しでよい。

## hash
- 987091e981097602236859f634eb1f10cd45ad4fbabc46087654f0516b57113b

# `test_cli_tui.py`

## Summary
- TUI 起動直前の CLI 前処理に関する外部挙動を検証するテスト。編集済み prompt の解決、Codex TUI 起動パラメータ、既定のファイルアクセスモード、prompt 保存先、linked worktree と `.cmoc` ignore の扱いを確認する。TUI 前処理や関連する保存・worktree 挙動を変更・調査するときのテスト入口。

## Read this when
- `tui` サブコマンドの prompt 編集後処理、parameter 解決、Codex TUI 起動を変更するとき
- TUI の prompt ログ保存先、linked worktree、`.cmoc` の ignore 挙動を変更するとき
- TUI 前処理の外部挙動を検証・回帰確認するとき

## Do not read this when
- TUI 起動前処理ではなく、通常の CLI サブコマンドや Codex 実行基盤そのものを変更・調査するとき
- TUI の正本仕様を確認することが目的の場合は、先に `oracle/doc/app_spec/sub_command/tui.md` を読むとき
- TUI 内部の単体実装詳細だけを確認し、外部挙動や保存・worktree 連携を検証しないとき

## hash
- 3fb1bd5bfef3908d630d935fa5eef6a6584a33760082cacb09ab81ae3d7b128b

# `test_codex_runtime_errors.py`

## Summary
- `codex exec` の JSONL 解析境界と、Codex CLI 不在時の失敗処理を確認するときに読む。`codex` の出力が壊れている場合の扱いと、失敗時にサブコマンドログへ残す内容をこのテストで固める。

## Read this when
- Codex CLI の stdout 解析が object 以外や不正 JSON を失敗として扱えているか確認したいとき。
- `Codex CLI が見つかりません` のような外部実行失敗を、例外だけでなくサブコマンドログの `codex_call` 記録まで含めて確認したいとき。
- `codex exec` 周辺の異常系を追加・修正した後に、既存のエラーカテゴリ分けとログ出力の整合を見たいとき。

## Do not read this when
- 通常の `codex exec` 成功系の引数生成やプロンプト組み立てを確認したいときは、`codex exec` 呼び出し規約側の本文を先に読む。
- サブコマンド全体のログ形式やコンソール出力規則を見たいだけなら、個別の runtime error テストではなくログ規約の本文を読む。
- JSONL 以外の実行失敗や、`codex` 以外の外部コマンドのエラーを調べたいときは、このテストではなく該当する runtime / CLI のテストを読む。

## hash
- c34be783256449d535cbd88ab17eeb23808bb28b33c41a56c099def966f39529

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 実行とローカル SLM 用 managed Ollama provider の結合テスト。argv、stdin、sandbox、override 設定、出力スキーマ、ログ、CODEX_HOME 非変更、リポジトリ書き込み、Ollama preflight を検証する。関連する Codex 実行・override 実装や Codex 実行仕様の変更時に確認する入口。

## Read this when
- Codex CLI の実行引数、stdin 経由の prompt、output schema、call log を変更・調査するとき
- ローカル SLM、managed Ollama provider、Ollama preflight、Codex override の連携を変更・検証するとき
- CODEX_HOME 設定ファイルを生成しない制約や sandbox・リポジトリ書き込み動作を確認するとき

## Do not read this when
- Codex 実行経路や managed Ollama 連携に関係しない機能を変更・調査するとき
- 実装の詳細を直接確認する必要があり、commons.runtime_codex または commons.runtime_codex_profile を読む方が適切なとき

## hash
- 5c3da5bebc8b9481cfc9b992c8e5a102f090d21dadd07ecf611a7305e3a09d73

# `test_codex_runtime_home.py`

## Summary
- `run_codex_exec` の Codex home 解決と起動前検証を確認する回帰テスト群。`CODEX_HOME` の未設定・相対値・絶対値の扱い、`auth.json` の存在確認、CLI を起動する前に失敗する条件をまとめて扱う。

## Read this when
- `CODEX_HOME` の解釈や、そこから決まる Codex home の検証条件を変えたいとき。
- `run_codex_exec` が Codex subprocess を呼ぶ前に失敗すべき条件を追加・修正したいとき。
- 相対 `CODEX_HOME` が subprocess の cwd 基準で解決されるか、call log にどう残るかを確認したいとき。

## Do not read this when
- Codex subprocess の argv 構築、schema 配置、retry、quota、JSONL 判定を見たいだけなら別の `run_codex_exec` テストや本体側を読む。
- Codex home 以外の実行環境やサンドボックスの挙動だけを調べたいとき。

## hash
- 4c565df6392255aeecc1a0120efd958bb96931292071cdf90d594f065d9ab7ce

# `test_codex_runtime_paths.py`

## Summary
- Codex exec の実行時パスと sandbox argv を検証するテスト。並列実行時の timestamp 予約、指定 cwd、pure-oracle read の read-only sandbox、リンク済み worktree での schema 保存先、.agents パス権限の非注入を扱う。Codex 実行パスやファイルアクセス制御の変更時に読む入口。

## Read this when
- Codex exec の cwd、出力 schema の保存場所、ログ path の一意性を変更・調査するとき
- FileAccessMode から Codex sandbox 引数への変換や .agents の扱いを変更・調査するとき
- リンク済み worktree や並列 Codex 実行に関する回帰を確認するとき

## Do not read this when
- Codex exec のプロンプト生成内容や一般的なファイルアクセス規則そのものを確認したいときは、参照されている oracle 文書・oracle src を先に読む
- Codex runtime のパスや sandbox argv と無関係な CLI 機能・テストを変更するとき

## hash
- 28f97967ce6eca999f85d8458f97f089fab2914100c7341b0bdffa291bc55754

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex の quota 超過後における probe・待機・resume・再実行の外部挙動を検証する回帰テスト。代表 probe の共有、resume token、失敗伝播、poll 上限、ログ、subcommand log、CODEX_HOME と cwd の扱いを対象とする。quota retry 制御の実装・テストを確認する入口である。

## Read this when
- Codex exec の quota 超過、quota availability probe、resume または prompt 再実行の挙動を変更・調査するとき
- quota 待機中の並行呼び出し、probe 失敗、poll 上限、KeyboardInterrupt の伝播を確認するとき
- Codex call log、subcommand log、CODEX_HOME、cwd の quota retry 連携を検証するとき

## Do not read this when
- quota retry や Codex exec の外部挙動に関係しない機能を変更・調査するとき
- quota probe の実装詳細だけを確認する場合は、probe parameter builder の実装・テストを先に読むとき

## hash
- f757d974763df49ef62fc1de924a70a062b9756883000ce328a9e9dc0d733185

# `test_codex_runtime_retry.py`

## Summary
- `run_codex_exec` の再試行と失敗ログを、外部挙動として検証するテスト群。Structured Output の意味的失敗、capacity retry、JSONL の異常、KeyboardInterrupt、差分保持までを一つの状態機械として扱う。
- Codex 呼び出しの retry 判定、call log、subcommand event の整合を確認したいときに読む。再試行の有無だけでなく、最終結果と途中ログの両方が重要な変更で参照する。
- Codex 実行の正常系だけを触る変更や、この再試行・失敗記録の対象外の CLI 挙動を扱う変更では優先して読む対象ではない。

## Read this when
- Codex 実行の再試行条件や失敗時の記録方法を変えるとき。
- Structured Output の検証失敗、capacity 失敗、JSONL error、中断の扱いを確認したいとき。
- call log と subcommand event の対応関係を壊していないか見たいとき。

## Do not read this when
- retry や失敗ログに関係しない Codex 実行の基本入出力だけを変えるとき。
- このファイルの対象外のサブコマンド追加や UI 変更だけを扱うとき。
- 再試行ではなく別のエラーパスや別モジュールのロギングを確認したいとき。

## hash
- c3341f70409dafe7f8649603c9e3ce0b07f1be24605890e05b7b7f5f692cc9a9

# `test_codex_runtime_subprocess.py`

## Summary
- `commons.runtime_codex_profile` の subprocess 周辺挙動を検証するテスト群。apply 破棄時に必要な process group 追跡、pidfd ベースの signal 配信、SIGTERM の遅延配信、leader 終了後の tracking 維持、割り込み時の tracking 維持、継承した apply tracking 環境の無視を確認したいときに読む。

## Read this when
- `run_tracked_codex_subprocess` と `run_codex_subprocess` の現行挙動を変える前に、外部から見える subprocess 管理の期待値を確認したい。
- apply abandon の cleanup と、child tracking が残る条件・消える条件を確認したい。
- process group の signal 送信を pgid ではなく member ごとの pidfd にしている理由を、テスト観点から確認したい。

## Do not read this when
- CLI の引数解析、session 状態遷移、report 文面など subprocess 管理以外を見たい場合は、より直接の実装や別テストを先に読む。
- `apply_abandon` の仕様そのものを知りたいだけなら、このテストではなく根拠の oracle doc を読む。
- OS 依存の pidfd 実装や signal API の詳細仕様を知りたいだけなら、このテストではなく実装側と関連ヘルパーを読む。

## hash
- c8a4ffd0749ccca20154ea78ecfaae51d1422c721adae339e778424ebc938ce4

# `test_codex_runtime_tui.py`

## Summary
- Codex TUI 実行ランタイムの統合テスト。完成済み prompt の読み込み、PURE_ORACLE_READ と REPO_WRITE のアクセス境界、linked worktree での実行、CLI 引数、成功・CLI 不在・KeyboardInterrupt・非 0 終了時の例外処理を検証する。あわせて TUI call log、サブコマンドイベント、コンソール要約の出力と timestamp 衝突時のログ保持を確認する。

## Read this when
- Codex TUI の prompt 読み込みや sandbox 引数を変更・調査するとき
- Codex TUI の成功・失敗時の call log、イベント、コンソール出力を変更・調査するとき
- Codex CLI 不在、割り込み、非 0 終了、linked worktree の挙動を検証するとき

## Do not read this when
- Codex TUI 以外の Codex 実行経路や、個別の prompt 生成仕様だけを調査するとき
- 単体の設定モデル、git 操作、または共通ログ実装だけを変更・調査するとき

## hash
- 2b000fe8f5c17976f9dce638b85a88f2cc160ecc87deed0307a54601dcb7fb0a

# `test_doctor_cli.py`

## Summary
- `doctor` / `doctor preprocess` の外部契約を、CLI 実行と直接呼び出しの両方から確認する統合テスト。`.cmoc/gu` と `.agents`、config、managed Ollama の修復、共有ロック、linked worktree、pre-existing Git index の保持に関する変更を入れるときに読む。

## Read this when
- `doctor preprocess` の副作用や修復対象が変わるとき。
- linked worktree から実行したときの repository/worktree の扱いを確認したいとき。
- Git index を壊さずに修復するか、既存の staged 変更を保持するかを確認したいとき。
- managed Ollama の生成・再利用・保持の契約を確認したいとき。

## Do not read this when
- `doctor` 以外のサブコマンドだけを変更するとき。
- lock 実装や config I/O の単体仕様だけを確認したいときは、より直接の実装・単体テストを読む。
- Git 操作の共通 helper だけを直したいときは、この統合テストより先にその helper のテストを読む。

## hash
- 82c5ade8fbf932b0a4abc1088bf16fbdd17c73f85cd45e2b9ee249c5b2a0be7a

# `test_indexing_cli.py`

## Summary
- `cmoc indexing` の CLI 挙動を、事前条件・doctor 呼び出し・INDEX 更新・commit まで含めて検証するテスト群。
- 通常の repository、linked worktree、dirty worktree、既存差分、fresh な INDEX.md、preflight の有無など、indexing 周辺の外部挙動を確認する入口。
- `cmoc indexing` と `INDEX.md` 自動更新の仕様根拠は `{{work-root}}/oracle/doc/app_spec/indexing.md` と `{{work-root}}/oracle/doc/app_spec/sub_command/indexing.md`。

## Read this when
- `cmoc indexing` の CLI 事前条件やエラー終了条件を変えるとき。
- doctor preprocess、worktree 判定、INDEX.md 更新、Codex 呼び出し、commit 対象の境界を確認したいとき。
- preflight の有無や、既存差分がある状態での indexing の挙動を確認したいとき。
- linked worktree と apply worktree での indexing 経路を修正するとき。

## Do not read this when
- INDEX.md エントリー本文そのものの生成ロジックだけを確認したいときは、対応する実装側の indexing モジュールを先に読む。
- git 操作の共通処理や INDEX 更新の下位ロジックだけを追いたいときは、このテストより共通 helper のテストを先に読む。
- CLI 以外の doctor 単体や Codex 予備処理の仕様だけを見たいときは、より直接の対象を読む。

## hash
- 6f034e6de312aa49b855a893d1593bdb56af29361441c502e1bbbf7e71dc1fd7

# `test_indexing_common.py`

## Summary
- `commons.indexing` の直接テストをまとめる。
- `render_index_entry` と `update_indexes` の入力検証、既存ハッシュの再利用、ディレクトリ走査、並列生成を CLI の流れから切り離して確認する。

## Read this when
- `commons.indexing` の入出力や更新判定を変えたので、その外部挙動を確認したいとき。
- 不正な INDEX entry の扱い、空ディレクトリへの INDEX.md 作成、兄弟要素や祖先関係のない要素の並列処理を確認したいとき。
- `build_index_entry` の差し替えや、Codex 実行時のログ連携が indexing 更新経路にどう伝播するかを確認したいとき。

## Do not read this when
- CLI の起動手順やサブコマンド全体の流れだけを見たいときは、`cmoc indexing` 側の仕様を先に読む。
- INDEX.md 形式そのものの正本仕様を確認したいだけなら、テストではなく indexing 関連の oracle 側を読む。
- `commons.indexing` 以外のサブコマンドや、インデクシング以外のログ・preflight・コミット処理だけを変えるときは、このテストから入らなくてよい。

## hash
- cb28d083cf1337f9a20d09bd17330fa769aa181aa6611b01430961c422923ff9

# `test_indexing_preflight.py`

## Summary
- `commons.runtime_codex_preflight` の indexing preflight まわりを検証するテスト群。Codex 実行・TUI 実行の直前に indexing が走ること、linked worktree の選択、repository lock 待ち、preflight 無効化、回復用の追加 indexing をしないことを確認する入口。

## Read this when
- Codex 呼び出しの前に indexing を挟む制御を変更したいとき。
- worktree 選択や repository lock の待機条件を確認したいとき。
- preflight を明示的に無効化した場合の挙動や、file access violation 後の回復経路を確認したいとき。

## Do not read this when
- indexing 自体の更新ロジックを見たいときは、対応する indexing 実装か oracle 側の仕様を先に読む。
- Codex 実行本体や TUI 実行本体の詳細を見たいときは、このテストではなく実装側を読む。

## hash
- b8c6ef24df2cb04b044566a3c41abd8a9fce73fa1cf4ed25b86adbc7a04b5bdb

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
- `oracle.prompt_builder.complete_prompt` が組み立てる標準 prompt の各部品を、実際の描画結果で検証するテスト群。
- `file_access_rule`、`routing_rule`、`apply_review_standard`、`realization_standard`、`index_entry_standard`、`review_oracle_standard` が complete prompt に含まれる条件と、各部品の主要文言を確認する。
- `{{work-root}}` や `{{repo-root}}` の置換、code block 内の文字列保持、デフォルトで省略される部品の有無など、prompt 合成時の境界条件を確認する入口。

## Read this when
- complete prompt にどの標準部品が入るべきか、または省略されるべきかを変更したとき。
- 標準部品の文言や見出しが、組み立て後の prompt にどう現れるかを確認したいとき。
- `build_complete_prompt` の出力が、root token の展開や code block 内の文字列保持を壊していないか確かめたいとき。

## Do not read this when
- 各標準部品そのものの詳細な仕様だけを確認したいときは、対応する oracle 側の定義を先に読む。
- prompt 合成ではなく、個別部品の内部実装や分割方針を追いたいときは、このテストではなく対象の realization 実装を読む。
- INDEX ルーティングの書き方だけを確認したいときは、このテストではなく `index_entry_standard` 本体や routing 関連の文書を読む。

## hash
- cc6ca40c9d508f280b4d8d8f14a052fb17978b3172c12decda27140696acef14

# `test_review_oracle_loop.py`

## Summary
- `review oracle` の finding loop とその周辺の制御を検証するテスト群。findings の列挙・同一周回の検証結果の受け渡し・merge の再試行・judge 中断時の部分結果保持など、`sub_commands.review.oracle` と `sub_commands.review_loop` の組み合わせで崩れやすい振る舞いを確かめる。

## Read this when
- review oracle の反復処理、finding の集約や更新、merge/judge/validate の連携を変更するとき。
- review 側が隔離 worktree を使って実行されること、または interrupt 時の途中結果の扱いを確認したいとき。
- codex 実行結果の Structured Output を受け取る流れや、finding ごとの prompt 内容の伝播を変えるとき。

## Do not read this when
- review oracle の仕様そのものを知りたいだけなら、対応する oracle doc を先に読むべきで、このテストは結果確認用なので起点にしない。
- merge 以外の review サブコマンドや、finding loop と関係しない CLI 振る舞いを追いたいとき。
- 単体の helper 生成や repo 作成の詳細だけを見たいときは、より直接の実装ファイルや共通テスト補助を読むべきで、このファイルは読む必要が薄い。

## hash
- 2c106f26f6e98e37b8bffd8ad0165c9be9aded189c127bf0510ff61ba5f3352c

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
- `review oracle` の report 形式、件数集計、fatal/minor の分類、未判定や中断時の表示、CLI 引数の受け渡しを確認したいときに読む。`eval-oracle` から `review oracle` 実装へ委譲されるかどうかも含む。

## Read this when
- review oracle の出力レイアウトや節順を変える可能性がある。
- review oracle の finding 集計、accepted / rejected の分岐、symlink や `{{oracle-root}}` alias の扱いを確認したい。
- 中断・失敗時に保存される report と、CLI の `review oracle` / `eval-oracle` の接続を確認したい。

## Do not read this when
- review oracle の内部実装手順だけを追いたい場合は、まず `sub_commands/review/oracle.py` 側を読む。
- CLI 全般の共通引数や実行基盤だけを確認したい場合は、より上位の CLI 定義や実行支援側を読む。
- 個別 oracle 文書の内容そのものを確認したいだけなら、このテストではなく対象の oracle 文書を読む。

## hash
- ca71f327fef06294be1a8520faa22042f1cfc387d5639b9d14761b31451bb29e

# `test_review_oracle_targets.py`

## Summary
- review/oracle の対象選定を検証するテスト群。finding から解決した oracle path と、レビュー対象に含める/除外する oracle file の境界を確認したいときに読む。

## Read this when
- review/oracle の対象列挙が、追跡済み・未追跡・ignored・symlink・`INDEX.md`/`AGENTS.md` の扱いで期待どおりか確認したいとき。
- session scope と full scope でレビュー対象の数や選別条件が変わる理由を追いたいとき。
- finding 側の `oracle_path` を repository の実パスにどう解決するか、`{{work-root}}` と `{{oracle-root}}` の扱いを確認したいとき。

## Do not read this when
- review 実行の本文出力形式や報告レイアウトを知りたいだけのとき。
- oracle file 自体の内容や個別の正本仕様を確認したいとき。
- レビュー対象の判定ではなく、session fork や Git 操作の一般的な挙動だけを追いたいとき。

## hash
- 763206b9c0b673578301cf86a2b46423c0be824b380eda063e88817b53c45c0d

# `test_review_oracle_worktree.py`

## Summary
- `review oracle` の worktree 選択、`INDEX.md` 統合、preflight 連携、未コミット差分の拒否、merge conflict 解決を検証するテスト群の入口。レビュー対象の作業領域と、review 実行時に確認すべき分岐だけを見たいときに読む。
- 個別の CLI 入力変換や実装内部ではなく、`review oracle` の実行時に worktree・branch・生成物・差分検査がどう振る舞うかを確認したいときに読む。

## Read this when
- `review oracle` の対象 worktree の選択や session branch 連携を変える作業をするとき。
- `INDEX.md` の生成結果を review 実行後に session 側へ統合する流れを確認したいとき。
- preflight が作る `INDEX.md` の扱い、または review 中に許可される差分と拒否される差分の境界を確認したいとき。
- review 時の merge conflict 解決や、worktree の隔離条件を検証するテストを追加・修正するとき。

## Do not read this when
- `review oracle` の報告書内容そのものだけを確認したいときは、報告書検証の別テストを読む。
- `review oracle` 以外の `review` 系 CLI の引数や一般的なパラメータ変換を見たいときは、対応する parameter テストを読む。
- `INDEX.md` の一般的な更新ロジックだけを見たいときは、indexing 側のテストや実装を読む。
- CLI 全体の起動や共通ランタイムの挙動だけを見たいときは、このファイルではなく共通 runtime や CLI のテストを読む。

## hash
- a085771c8005d370964dc28ae58e4d85cf2161c1216ba2c6ac430d5bc0eacbcf

# `test_runtime_apply.py`

## Summary
- `commons.runtime_apply` の停止・監視契約を、PID file と advisory lock、pidfd、process group のレベルで検証するテスト群。apply abandon の CLI そのものではなく、親 process の再読込、child group の停止、PID reuse、終了済み process の扱いを確認する入口。
- `apply_process_id` の読み取りとロック待ち、`stop_apply_process` と `stop_child_process_group` の失敗時 warning 結合、signal 送信の例外吸収など、apply runtime の中核挙動を変更するときに読む。

## Read this when
- apply 停止の実装や `commons.runtime_apply` の契約を変えるとき。
- 親 PID と child PID の追跡形式、PID reuse 判定、pidfd 送信、process group 停止の順序や失敗時挙動を確認したいとき。
- tracked child process の再読込や、更新中の apply process ID file をロックで保護する挙動を変えるとき。

## Do not read this when
- apply abandon の CLI 引数や出力、サブコマンド経路だけを確認したいときは、ここではなく `test_apply_abandon_cli.py` を読む。
- `commons.runtime_apply` 以外の CLI、設定、永続状態の仕様を追いたいとき。
- 一般的な process 管理の実装方針を探しているだけで、この apply 追跡契約に関係しないとき。

## hash
- 39842c108aa35019bef81cbfe316cefea4f743d4aeda724942f2fb5c042eebdb

# `test_runtime_cli.py`

## Summary
- `test/test_runtime_cli.py` は、CLI のエラー表示、ログ記録、preflight、completion、gitignore 修復の境界をまとめて検証する入口。`cmoc_runtime` と `commons.runtime_cli`、`main` のつなぎ込みを確認したいときに読む。

## Read this when
- CLI の想定済み error が stdout の Markdown report に出るか確認したいとき。
- サブコマンドログの生成条件、doctor preprocess、pre-log check、completion probe の副作用境界を確認したいとき。
- `.gitignore` への cmoc 無視パターン追加や work root 判定のような preflight 周辺の挙動を確認したいとき。

## Do not read this when
- 各サブコマンドの業務ロジック自体を知りたいときは、該当サブコマンドの実装側を読む。
- 個別の log フォーマットや duration 表示だけを確認したいときは、対応する runtime 生成側の実装を直接読む。
- CLI 全体の引数定義やコマンド構成だけを見たいときは、テストではなく起点の CLI 定義を読む。

## hash
- 0ba7b4cef0b4fccd388f831d0559c4363e7fd44703a08758285867059b8c0a96

# `test_runtime_codex_conflicts.py`

## Summary
- session join の conflict path が prompt にのみ反映され、path 別 sandbox 設定や Codex override の permissions に変換されないことを検証するテスト。対象 path の場所にかかわらず共通の sandbox argv が生成されることも確認する。

## Read this when
- session join の conflict resolution、prompt 生成、sandbox argv、または Codex override 設定の挙動を変更・検証するとき
- conflict path を sandbox の path 別権限へ変換していないことを確認したいとき

## Do not read this when
- session join conflict や Codex override の挙動ではなく、一般的な sandbox 実装や別の runtime テストを調べるとき
- conflict resolution の実装仕様そのものを確認する必要があり、対応する oracle source と oracle document を直接読むべきとき

## hash
- d0e15965dbe48f45c3a6b01ae8b01ea27c20bb69e22e81837af1abd4600af13c

# `test_runtime_codex_permissions.py`

## Summary
- Codex sandbox argv が permission profile や path 別権限設定に依存しないことを検証するテスト。各 FileAccessMode、作業ツリー内容の変化、実 Codex CLI parser への sandbox 引数受理を対象とする。

## Read this when
- Codex 実行時の sandbox 引数、permission profile、path 別権限入力の回帰を確認するとき。
- runtime_codex_profile の argv 生成仕様や関連テストの変更影響を調べるとき。

## Do not read this when
- Codex sandbox argv の実装を変更・調査する場合は、先に runtime_codex_profile の実装と対応する oracle 仕様を読むとき。
- Codex 実行以外のテストや一般的な CLI 入出力を扱うとき。

## hash
- fb2c9362d22d1689d276546864b2f7f71303fef2649c57b98159f36927b49336

# `test_runtime_codex_profile.py`

## Summary
- Codex argv の model、sandbox、reasoning effort、provider 上書き契約を検証するテスト。FileAccessMode の sandbox 変換、未知 mode の拒否、通常 provider での worktree 非走査、ローカル SLM 用 Ollama provider 設定を扱う。Codex 起動引数や runtime profile の変更時に挙動確認の入口となる。

## Read this when
- Codex の override argv 生成・準備処理を変更またはレビューするとき
- FileAccessMode と Codex の --sandbox 変換契約を確認するとき
- 通常 provider または cmoc managed Ollama provider の設定を変更するとき

## Do not read this when
- Codex argv や provider 上書き処理に関係しない機能を変更するとき
- Codex の一般的な実行フローや CLI 入出力だけを確認したいときは、まず対応する実装・仕様ファイルを読む

## hash
- 30ba3740defaec7fa9ec03a690fe19d4bb75e1b6436c2db74f239e83c57d61ca

# `test_runtime_config.py`

## Summary
- `CmocConfig` の既定値、JSON 化の順序保持、読み込み失敗時の案内文、入力検証を扱う回帰テスト群。設定の永続化や `cmoc config` 相当の変換・検証・エラー文言を変えるときに読む。
- `oracle.other.cmoc_config` の定義と `error_handling` 規則に対する期待を固定する。内部実装の分割や補助関数の置き場所ではなく、外から見える設定内容と失敗時の振る舞いを確認したい場合に進む。

## Read this when
- `CmocConfig` の既定値、`codex` 配下のモデル/ reasoning effort の値、回復試行回数を変える。
- 設定の dict 変換や JSON 直列化で、キー順や値の表現が変わる可能性がある。
- 設定ファイル欠落時に出すエラー要約や次アクションを変える。
- 設定値の型・空文字・不正な model spec を受け付けるかどうかを見直す。

## Do not read this when
- `cmoc_config` の定義そのものを変更したいなら、先に `{{work-root}}/oracle/src/oracle/other/cmoc_config.py` を読む。
- エラー終了時の全般ルールだけを確認したいなら、個別テストではなく `{{work-root}}/oracle/doc/app_spec/error_handling.md` を読む。
- 設定以外のサブコマンド挙動や別の runtime 変換を変えるだけなら、このテスト群は直接の対象ではない。

## hash
- d61000a89d068474857acbe96cb49419d70a5df73ef0ccc967c05f43f320b81e

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
- Codex の実行環境で使うファイルアクセス契約を確認したいときに読む。`FileAccessMode` の永続化値と sandbox 変換の対応がずれないかを確かめる役割で、関連する実装やルール文書へ進む入口になる。

## Read this when
- `FileAccessMode` の追加・変更で、保存値や sandbox 変換の互換性を確認したいとき。
- Codex 実行時のファイルアクセス制御が、別のルール定義と食い違っていないかを見たいとき。

## Do not read this when
- 単に `FileAccessMode` の列挙内容そのものを確認したいだけなら、定義元の実装を直接読む。
- sandbox 以外の実行制御や別の権限ルールを調べたいなら、この対象ではなく該当するルール定義を読む。

## hash
- c91b2b64872d80328afcf73f0974799243f0855a418f76b4c6ed5130e451cc33

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
- `session` と `apply` の永続 state 形状、branch 名からの session/apply 解析、そして session fork lock の process 間排他を検証するテスト。state ファイルの入出力や branch 由来の識別ロジックを変えるときに読む。

## Read this when
- session/apply state の JSON 構造、必須/nullable フィールド、検証エラーの扱いを変える。
- `cmoc session fork` や `cmoc session join` のための branch 解析・state 読み出しの境界を確認したい。
- session fork lock の共有範囲や、複数 process から同じ repository を直列化する挙動を確認したい。

## Do not read this when
- CLI の引数解釈や表示文言だけを変える。
- git 操作の細部や一般的な repository ヘルパーだけを確認したい。
- `session`/`apply` state ではなく、別の runtime 設定や review/apply ルートの挙動を追いたい。

## hash
- 45329475c441dc44a7cd729aa73a9030689a470ed59cd1a36d5a0f93beb4b393

# `test_session_cli.py`

## Summary
- session fork、join、abandon の CLI 外部挙動を横断的に検証するテスト。session branch と state の生成・更新・削除、linked worktree、事前処理、dirty worktree 拒否、競合解消、失敗時のロールバックやエラー出力を扱う。session 状態遷移に関する回帰テストの入口。

## Read this when
- session の fork、join、abandon の挙動を変更・調査するとき
- session state、branch cleanup、linked worktree、conflict resolution の外部挙動を検証するとき
- session CLI の失敗時処理、出力、ロールバック、doctor preprocess 連携を確認するとき

## Do not read this when
- session CLI や session state と無関係な機能を変更・調査するとき
- session サブコマンドの実装詳細を直接確認する必要があり、対応する src や oracle file を読む方が適切なとき
- Codex の出力品質そのものや、session 状態遷移以外のテスト方針を確認するとき

## hash
- 63b9282fd6e0617dd25c92edc26de7913963ef80a7ba3dcf136305ffaa0444fc

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
