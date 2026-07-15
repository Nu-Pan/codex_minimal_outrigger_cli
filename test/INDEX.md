# `_acp_builder_support.py`

## Summary
- テストから正本 schema への参照先を組み立てる共通 helper のための案内。oracle 側の schema 配置を前提に、テストがどの path を参照すべきかを確認したいときに読む。
- テスト用の path 解決を変える必要があるときの入口。oracle schema の場所や階層変更に合わせて、ここ経由の参照方法を直す前提で読む。

## Read this when
- テストから `oracle/src/oracle/acp_builder` 配下の schema を参照する path を組み立てるとき。
- oracle schema の配置変更に伴って、テスト側の参照 path を追従させる必要があるとき。
- `acp_builder` 関連の test helper を確認し、正本 schema への依存の持ち方を知りたいとき。

## Do not read this when
- アプリ本体の実装や schema 定義そのものを確認したいとき。
- test helper ではなく、oracle 側の正本 schema の内容を確認したいとき。
- この helper を使わない別のテストや補助コードを読んでいるだけのとき。

## hash
- 6fd184bad0b16e6bce9c32dac57e2187a8272303ece3f3c8d350acaeacf5824b

# `_apply_support.py`

## Summary
- apply の session state から apply 用の管理 worktree パスを復元する補助関数。apply ブランチ命名規則と session state の `apply.apply_branch` を前提に、テストが期待値を独立に組み立てるために使う。

## Read this when
- apply の worktree 位置を、session state の内容から直接復元する期待値をテストで作りたいとき。
- apply ブランチ名の構造と session state の `apply` 情報を使って、実装側の worktree 解決ロジックと切り離した検証が必要なとき。

## Do not read this when
- apply state の保存・更新・遷移そのものを確認したいときは、session state 本体や該当コマンドの実装を見る。
- worktree 解決の共通実装や実運用側の経路を知りたいときは、テスト補助ではなく production 側の実装を見る。

## hash
- e191a24648017edf89acfbbbf207fe8f4a5298bdd76d168b1ab450d1a4e52fde

# `_cli_support.py`

## Summary
- Typer ベースの CLI を共通のテストランナーで起動するための共有テスト補助。CLI の外部挙動を確認するテストだけが読む。

## Read this when
- Typer アプリを `runner.invoke(...)` で呼ぶテストを書くとき。
- 複数の CLI テストで同じ起動方法を共有したいとき。

## Do not read this when
- CLI 以外の純粋な関数や runtime ロジックを確認するとき。
- 個別のテストで独自の runner 設定や入出力の差し替えが必要なときは、ここではなく各テスト側の補助を読む。

## hash
- f8067659d5647e5eb7180b42c0741136aba6b2baf99cf70dd459a35da30d4d12

# `_codex_support.py`

## Summary
- Codex subprocess controlのテストで共有する補助関数群です。Fake Codex結果、`AgentCallParameter` の最小構築、`--config` 解析、sandbox/permission override の抽出と検証をまとめて扱います。

## Read this when
- Codex 実行ラッパーや TUI ラッパーの argv 構築、Structured Output schema 名、sandbox writable roots、permission filesystem override を検証するテストを書くとき。
- 複数のテストで同じ Codex テスト前提を共有したいとき。

## Do not read this when
- Codex 本体の実装やプロンプト仕様そのものを変更したいとき。
- runtime 呼び出しの共通処理や permission 判定ロジックの本体を理解したいときは、より直接の実装側へ進む。

## hash
- a97ee9567a6cb5aac3e38b22a27eff1cb47d8c29ed95493f5dd5f1908f68029b

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
- `cmoc doctor` をテストから呼ぶための共通ヘルパー。`doctor` を作業ツリーの cwd で実行し、実運用と同じ per-user cmoc managed Ollama を前提にした検証を行う場面で読む。

## Read this when
- `doctor` をテストコードから起動する共通化が必要なとき。
- テストが fake な Ollama ではなく、本番と共有する cmoc managed Ollama を使う前提を確認したいとき。
- `doctor` の対象 worktree を cwd で切り替える実装意図を確認したいとき。

## Do not read this when
- `doctor` 本体の処理順や修復ロジックを知りたいときは、`cmoc doctor` の実装側を直接読む。
- cmoc managed Ollama の管理主体、配置先、可用性、GPU 推論要件を確認したいときは `oracle/doc/app_spec/cmoc_managed_ollama.md` を読む。
- テスト用の fake service ライフサイクルを扱いたいときはこのヘルパーではなく、テスト境界の別資料を読む。

## hash
- 282f5e743ce5a9253c28103a9ed999c8f8c8a5f09c801c63acb31bec1d727776

# `test_acp_builder_apply_parameters.py`

## Summary
- `acp.builder.apply.fork` の各 parameter 生成と、対応する正本 schema 参照を検証するテスト群。packaged layout での import 契約、標準 prompt の組み立て、root の扱い、schema 適合性を確認したいときに読む。

## Read this when
- `apply fork` の parameter 生成が期待どおりの prompt・root・model 設定になるか確認したいとき。
- 正本 schema への参照先や、生成物が schema に適合するかを確認したいとき。
- packaged layout で import できることや、相対 target path の受け付け条件を確認したいとき。

## Do not read this when
- `apply fork` の実際の builder 実装や prompt 本文そのものを直すときは、対応する実装側を読む。
- `oracle` 配下の正本 schema や文面の原本を確認したいときは、このテストではなく `oracle/src/oracle/acp_builder/apply/fork/` 側を読む。
- `apply` 全体の仕様や他サブコマンドの routing が知りたいだけなら、このテストではなく上位の INDEX を読む。

## hash
- 8a949fc871a630c776cdcf2cf532e4a305c9d1868a273a18be891b60ab179e70

# `test_acp_builder_indexing_parameters.py`

## Summary
- `cmoc indexing` の `INDEX.md` エントリー生成用 builder の互換性を検証するテスト群。生成パラメータの公開面と、モジュールの再公開範囲が正しいかを見る入口。

## Read this when
- `cmoc indexing` の目次エントリー生成で、最低モデル・低 reasoning・読み取り専用・事前検査なしの組み合わせを確認したいとき。
- `acp.builder.indexing.index_entry` が外部に公開すべき builder だけを再公開しているか確認したいとき。
- INDEX.md エントリー生成の互換性回帰を、この周辺のテストから追いたいとき.

## Do not read this when
- エントリー文面そのものの仕様や記述方針を確認したいときは、対応する正本仕様側を見るほうが直接的。
- この builder 以外の `cmoc indexing` 実装や別サブコマンドの挙動を追いたいとき。
- 出力 JSON の構造やルーティング文書の一般ルールだけを確認したいとき。

## hash
- 6620858a1b19c28dc4a58a098a7b66f32c83851ae4a9982a766320e96ebc699f

# `test_acp_builder_review_oracle_parameters.py`

## Summary
- review oracle ACP builder の `parameter`・`structured_output_schema`・互換公開面を検証するテスト群。`,
- `build_review_oracle_*_parameter` の公開挙動、schema 一致、`{{oracle-root}}` / `{{oracle-path}}` の保持を確認したいときの入口。

## Read this when
- review 系 oracle builder の出力互換性を確認したいとき。
- parameter のモデル設定、prompt への動的文字列の保持、schema ファイルと正本 oracle schema の一致を追いたいとき。
- compatibility module の `__all__` や内部実装の公開漏れを検証したいとき。

## Do not read this when
- review 以外の ACP builder を扱うとき。
- schema の正本定義そのものを確認したいときは、このテストではなく対応する `oracle/src` 側へ進むとき。
- 単純な実装本体の制御フローだけを追いたいとき。

## hash
- 82876c8164a49b87b790ea3c1b688fb56664e5a3652e196c7d21fa64f544f97e

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
- `acp.builder.tui.resolve_parameter` の TUI 向け生成結果を検証するテスト群。呼び出し側が参照する最終的な prompt 断片、出力 schema、公開 API の最小範囲を確認したいときに読む。

## Read this when
- TUI 用の resolve parameter 生成で、埋め込まれる元依頼文や正本由来の文脈が期待どおりか確認したい。
- structured output schema の必須項目、各項目の型、`file_access_mode` の許容値が実装意図に沿っているか確認したい。
- モジュールの公開名が必要最小限に保たれているか確認したい。

## Do not read this when
- `resolve_parameter` の生成ロジックそのものを追いたい場合は、対象モジュール本体を読む。
- TUI 以外の ACP builder や別パラメータ種別の挙動を確認したい場合は、このテストではなく該当する別テストを読む。
- 正本仕様の本文そのものを確認したい場合は、コメントに示された oracle 側の文書を読む。

## hash
- 19e5bf97431f200912436962cee9ec7cece4b99d082816ed5cd788469ccfe4a1

# `test_apply_abandon_cli.py`

## Summary
- `apply abandon` の CLI 外部挙動を確かめるテスト群。worktree・branch・state の cleanup、実行位置の補正、tracked process の停止、異常状態の拒否と警告扱いをまとめて確認する。低レベルな process helper の契約は別のテストへ分離している。

## Read this when
- `apply abandon` の返す成功・警告・失敗の分岐を確認したいとき。
- apply 実行中の state や補助情報の破損、別 session の混入、古い branch 参照など、破棄前に止めるべき境界条件を見たいとき。
- CLI を apply worktree から呼んだ場合でも repo 側 state を正として扱う挙動を確認したいとき。

## Do not read this when
- process 起動・停止そのものの低レベル契約を見たいとき。
- session fork や apply fork の生成手順だけを確認したいとき。
- apply abandon 以外の apply サブコマンドの仕様を追いたいとき。

## hash
- 7999be0330a58f529a8e0b97d47cd1c84d22249d343e0ae807476edeb1bf572c

# `test_apply_fork_cli.py`

## Summary
- `cmoc apply fork` の CLI 挙動、状態遷移、worktree/branch 管理、gitignore 反映、中断・異常系を検証するテスト群をまとめた入口。apply の実行フローや session state との整合性を追う変更で読む。
- このファイルは `apply fork` の総合テストを持つため、個別の小さな helper の実装差ではなく、CLI の外部挙動や state file / worktree の更新順を確認したいときに進む。
- target normalization の独立テストではないので、対象ファイル選択だけを見たい場合は別のテストモジュールを優先する。

## Read this when
- `cmoc apply fork` の正常系・中断系・失敗系の振る舞いを確認したいとき
- session state、apply branch、apply worktree、report、process id の更新関係を追いたいとき
- `.gitignore` 反映や config 修復など、apply 実行前後の周辺整合性を見たいとき

## Do not read this when
- target の正規化だけを確認したいときは、このファイルではなく対象正規化の専用テストを見る
- apply の内部 helper の細部だけを追いたいときは、より直接の実装モジュールを読む
- `cmoc apply fork` 以外のサブコマンドの仕様確認が目的なら、このファイルは後回しにする

## hash
- e8b5fc9e167de6fd32ba7675e428916027ac085a0115812118369c7a8fe9b3a7

# `test_apply_fork_report_cli.py`

## Summary
- CLI から見た `apply fork` の report 生成と再検査制御を検証する統合テスト群。所見の適用、commit、変更要約、front matter、収束判定、error report、rolling 実行までを同じ観測点で確認する入口。

## Read this when
- `apply fork` の report 文言、front matter、結果判定、変更要約の表示を変えるとき。
- apply 後に変更ファイルを再調査する条件や、未収束・error・収束の扱いを確認したいとき。
- rolling 実行時に、前回の apply 結果をどこまで対象にするかを確認したいとき。

## Do not read this when
- 所見の抽出ロジックそのものを直したいときは、まず所見列挙側の実装を読む。
- report の見た目ではなく、`apply fork` の適用処理や session state 更新の本体を追いたいときは、CLI 検証より実装側を読む。
- join 側の挙動や session fork の初期化だけを確認したいときは、このテスト群は後回しにする。

## hash
- 2441049a57de807281b9a3e34478e989520e1d0a81ff61230de132e652b7914b

# `test_apply_fork_target_normalization.py`

## Summary
- apply fork に渡す候補 path の正規化と絞り込みを検証する回帰テスト群。`oracle` / `realization` / 管理用ディレクトリの境界、`git check-ignore` 相当の扱い、symlink と binary の分類を確認したいときに読む。

## Read this when
- apply fork の対象判定が、root 直下の `memo` 除外、`.cmoc/gu` の除外、`AGENTS.md` や `INDEX.md` の除外、tracked ignored file の扱い、symlink の repo path 判定、binary file の扱いのどれかに関係する変更をする。
- 対象候補の重複排除や、同じ実体を指す path を別対象として扱う境界を確認したい。

## Do not read this when
- apply fork の実際の適用処理や副作用を追いたい場合は、対象の実装側を読む。
- apply fork 以外のコマンドの入出力や一般的な CLI 振る舞いを確認したい場合は、このテストではなく該当コマンドのテスト群を読む。

## hash
- 8a09d494abb8f29892f6a3333ec796b3ceb5e149cf99d5ef51c10982c7c2a254

# `test_apply_join_cli.py`

## Summary
- `cmoc apply join` の CLI 挙動を検証するテスト群。apply 実行結果の取り込み、state 更新、report 生成、worktree/branch cleanup、dirty worktree、想定外差分、rename、merge conflict までを一箇所で確認したいときに読む。`apply join` の成功条件と拒否条件、通常モードと `--force-resolve` の差を追う入口であり、個別の補助関数より外部挙動ベースの確認を優先する。

## Read this when
- `cmoc apply join` の仕様変更、失敗条件、レポート文面、state 遷移、cleanup 条件を確認したいとき
- apply 側と session 側の差分分類や、想定外差分を通常モードで止めるか強制モードで revert するかを追いたいとき
- INDEX.md コンフリクト自動解決、dirty worktree の拒否、merge conflict の扱いを含む end-to-end の CLI テストを見たいとき

## Do not read this when
- `apply fork` や `session fork` など `apply join` 以外の subcommand の仕様を見たいとき
- 個別 helper の内部実装だけを追いたいときは、まず対応する実装ファイルや下位の仕様を読むべきで、このテスト群は後から確認する
- `apply join` とは無関係な汎用テスト方針や他機能の挙動を確認したいとき

## hash
- b49c851181d6c17487f43a4e6cd05c0969177f89223913d90b00d02bcde07dff

# `test_basic_runtime.py`

## Summary
- `path_model` と run/worktree 周りの runtime 契約を検証するテスト群。パス表記の復元、repo root と linked worktree の切り分け、`pushd` の cwd 競合防止、run worktree の生成・削除での不正パス拒否を確認する。

## Read this when
- Root/worktree の判定や `{{run-root}}` / `{{work-root}}` の扱いを変えるとき。
- `basic.path_model` のプレースホルダ解決や、run worktree の作成・削除条件を確認したいとき。
- 並列実行時の cwd 管理や、実ワークツリー外への書き込み防止を検証したいとき。

## Do not read this when
- CLI の引数処理やサブコマンド分岐だけを追いたいとき。
- git 操作の一般的なユーティリティやテスト補助だけを確認したいとき。
- このテストが参照する契約の本体ではなく、実装側の詳細設計だけを追いたいとき。

## hash
- 2ba2ec4bb9e2eaa83fdf73d982c633737c062ff17b0a3766100cf8960240c45b

# `test_cli_tui.py`

## Summary
- `cmoc tui` の外部挙動を検証するテスト群。エディタ入力、prompt の整形、parameter 解決、Codex TUI 起動、linked worktree での保存先や `.cmoc` ignore の境界を確認したいときに読む。

## Read this when
- `tui` サブコマンドの起動前後の振る舞い、保存される `_orig.md` / `_cmpl.md`、または backend 起動時に渡す parameter の期待値を確認したいとき。
- エディタ選択、prompt の編集反映、linked worktree で repository 側へ保存する扱い、`.gitignore` やログ配置の挙動を変える修正をするとき。

## Do not read this when
- `cmoc tui` の実装内部の分割や補助関数の設計だけを見たいときは、まず `src/sub_commands/tui.py` 側を読む。
- `doctor` 全体や他サブコマンドの入出力を確認したいだけなら、このテストではなく該当サブコマンドのテストを読む。

## hash
- 0faa73afc45de3c6828ac050dc605087ff238c2b615c80462cf6ee8ee14dbbc3

# `test_codex_runtime_errors.py`

## Summary
- `run_codex_exec` の異常終了経路を確認するテスト群。Codex JSONL の非 object/不正行の扱いと、CLI 不在時に失敗ログが残ることを扱う。

## Read this when
- Codex CLI 呼び出しの異常系、特に JSONL 解析失敗や CLI 未検出時のエラー扱いを変えるとき。
- Codex 呼び出しの失敗をサブコマンドログへどう記録するかを確認したいとき。

## Do not read this when
- 通常の成功系や一般的な `codex exec` の引数組み立てだけを確認したいときは、より上位の呼び出し仕様や実行フローの対象を読む。
- コンソール表示やサブコマンド全体のログ書式だけを確認したいときは、このテストではなくログ規則側を読む。

## hash
- 2d2995885452ad45447ee286cbeb7212a5611ad3a926642a8a5dbbdd51bf4c3d

# `test_codex_runtime_exec.py`

## Summary
- `run_codex_exec` と `prepare_codex_override_args` の結合を検証するテスト群。実際の Codex CLI 起動、`cmoc_managed_ollama` への切り替え、`CODEX_HOME` に利用者設定を作らないこと、実行時に必要な override と prompt/schema の受け渡しを確認する。

## Read this when
- Codex 実行経路の実結合を変えたとき。
- local SLM を使うときの override 構築や Ollama preflight の呼び出し条件を変えたとき。
- Codex CLI への argv、stdin、出力 schema、`CODEX_HOME` の扱いに関する互換性を確認したいとき。

## Do not read this when
- 純粋なコマンド引数整形だけを確認したいときは、より下位の override 生成側を読む。
- managed Ollama 側のサービス仕様そのものを確認したいときは、Codex 実行テストではなく Ollama の仕様側を読む。
- repo 書き込みや `.gitignore` など一般的なファイル操作だけを確認したいときは、別の実行・FS テストを読む。

## hash
- bcc0c6632169da84e1fc312ad49b1f09ca12bbdca18050c3711b27246281f197

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 起動前の `CODEX_HOME` 解決と preflight validation を検証するテスト。未設定時の既定値、設定済み相対値の扱い、`auth.json` 不在や不正な `CODEX_HOME` で子プロセスを起動しないことを確認したいときに読む。

## Read this when
- Codex 実行前に使う home ディレクトリの決め方や検証条件を変えるとき。
- `CODEX_HOME` の未設定時既定値、相対値の保持、`auth.json` の存在確認、失敗時に subprocess を始めない保証を確認したいとき。
- 起動前の失敗メッセージや next action の内容を調整するとき。

## Do not read this when
- Codex 実行コマンドの argv 構成やプロンプト保存を変えるだけのとき。
- 認証情報の内容そのものや Codex home 以外のファイルアクセス規約を変えるだけのとき。
- 別の起動前検証や一般的なエラー処理を扱う実装・テストを読むほうが直接的なとき。

## hash
- de2dd9c21179c0180f12976f3fad22355fca0429820470e45e7488ae569df0b5

# `test_codex_runtime_paths.py`

## Summary
- `codex exec` の呼び出し規約と、ファイルアクセス制限のプロンプト化・権限上書きの結合を検証するテスト。`cwd` の決定、Structured Output の schema 保存先、ログ系 path の予約、linked worktree からの実行時の path 解決を確認するときに読む。
- Codex CLI に渡す permission profile や追加 read path の組み立てが、`oracle` 側の正本仕様どおりかを見たいときの入口。`.agents` を write 対象にしないことや、repo-local read dirs の許可境界を確認するときに読む。

## Read this when
- `run_codex_exec` が `--cd`、`--output-schema`、`--output-last-message`、stdout/stderr などをどう扱うかを確認したい。
- linked worktree から実行したときに、schema 保存先や実行 cwd が repo root 側の規則に従うかを確認したい。
- 同一 timestamp で並列実行しても、call/prompt/stdout/stderr/output/schema の各 path が衝突しないことを確認したい。
- `PURE_ORACLE_READ` や `REPO_WRITE` で、`oracle` と `realization`、追加 read path、`.agents` の扱いが正しく反映されるかを確認したい。

## Do not read this when
- Codex exec の一般的な実装全体や、`oracle` 以外の入出力変換だけを追いたい。
- `INDEX.md` の生成方針や、他のルーティング文書の内容を確認したい。
- Codex CLI の認証やモデル選択だけを見たい。
- ファイルアクセス規則そのものの正本仕様を読みたい場合は、ここではなく参照されている `oracle` 側の文書と実装を直接読む。

## hash
- 7d466862ca130435a77280541e9bbfcf14060781bf20c736a2041572aa7079d9

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex exec の quota 枯渇後リトライ制御を扱う回帰テスト群。代表 probe の共有、resume token の復元、同一プロンプトの再実行、並列待機の集約、呼び出しログとサブコマンドログ、`CODEX_HOME` と `cwd` の解決をまとめて確認する。
- quota 待機への遷移と復帰の外部挙動を確認したいときに読む。特に、失敗理由ごとの分岐、再試行の可否、待機中の進捗表示、待機状態の後始末を追う入口になる。

## Read this when
- Codex exec が quota 不足・usage limit・spend cap から復帰する流れを変更したいとき。
- 代表 probe を 1 回だけ実行する共有制御や、resume できない場合の再実行方針を確認したいとき。
- 並列に待機へ入った呼び出しの扱い、call log / stdout log / output log / subcommand log の整合性を確認したいとき。
- `CODEX_HOME` の解決、`cwd` 基準の相対パス解釈、KeyboardInterrupt や probe 失敗の伝播を確認したいとき。

## Do not read this when
- quota 以外の通常の Codex 呼び出し引数やプロンプト生成だけを変更したいときは、より上流の builder や呼び出し規約側を読む。
- 一般的な subprocess ラッパーの振る舞いだけを追いたいときは、quota retry に依存しない共通 runtime 側を見る。
- quota 復帰に関係しないファイルアクセス制限や Structured Output の正本仕様を確認したいときは、oracle 側の該当文書を読む。
- このファイルの個別ケースだけでなく、全体の呼び出し規約を確認したいときは `codex exec` の規約文書を先に読む。

## hash
- edc881fe5e8f0c447eaab2a9cc659f2af73730c124c45059b40d8b8a6dbcc133

# `test_codex_runtime_retry.py`

## Summary
- `run_codex_exec` の再試行・失敗時ログ・中断扱いを外部挙動として検証するテスト群。Structured Output の検証失敗、capacity 再試行、JSONL の未知エラー、KeyboardInterrupt、差分保持とログ記録の境界をまとめて確認する。

## Read this when
- `run_codex_exec` の retry 回数、失敗判定、最終エラー、呼び出しログ、サブコマンドログの整合を変える作業をする時。
- Structured Output の parse/validation 失敗、capacity 失敗、stdout JSONL 外の error marker、中断時の扱いを変える時。
- Codex 呼び出し後に生成される差分やログが、再試行や失敗でも保持・記録されるかを確認したい時。

## Do not read this when
- Codex CLI の引数組み立てや基本的な呼び出し規約だけを変える時は、`codex_exec_rule` 側を先に読む。
- コンソール表示やサブコマンド全体のログ書式だけを変える時は、`console_and_file_log` 側を読む。
- retry とは無関係な通常成功系、別サブコマンド、別のログ種別のテストを探している時。

## hash
- 4af9f9de2c8501601fb0889a657c8b53fd2ca1b5665e0f043eb8dc028112e07d

# `test_codex_runtime_subprocess.py`

## Summary
- `commons.runtime_codex_profile` の subprocess 追跡と、apply cleanup 用の tracking 情報の扱いを検証するテスト群。process group の記録、SIGTERM の配信タイミング、communicate 中断後の tracking 維持、継承された apply tracking 環境の遮断を見るときに読む。

## Read this when
- Codex subprocess を tracked で起動する挙動を変えるとき。
- apply cleanup に必要な process group / pidfd / tracking file の扱いを確認したいとき。
- SIGTERM や KeyboardInterrupt の後に tracking 情報を残すか消すかの判定を変えるとき。
- 子プロセスに inherited apply tracking 環境を渡さない制御を確認したいとき。

## Do not read this when
- `cmoc apply abandon` の CLI 引数、状態遷移、出力文面を確認したいだけのときは、対応する oracle doc を先に読む。
- `commons.runtime_codex_profile` 以外の subprocess 実装や別コマンドの起動経路を追いたいとき。
- 単なる一般的な pytest 事例や別のテストファイルを探しているだけのとき。

## hash
- 3abf68012089ad162631753b1970173035861649bb11ae5ad4bde49838a3983b

# `test_codex_runtime_tui.py`

## Summary
- `commons.runtime_codex.run_codex_tui` の TUI 実行まわりを検証するテスト群。追加読み取りパスの事前検査、完成済み prompt の扱い、worktree 付き実行時のアクセス上書き、call log とサブコマンドイベント、CLI 不在・例外・非 0 終了の失敗経路を読むときに進む。

## Read this when
- `run_codex_tui` の引数整形、prompt 読み込み、アクセス制約、Codex 起動前後のログ出力や失敗時挙動を確認したいとき。
- TUI 実行に付随する call log の生成・重複回避・サブコマンド logger への記録を確認したいとき。
- linked worktree での実行や、`PURE_ORACLE_READ` と `REPO_WRITE` の分岐が関係するとき。

## Do not read this when
- `run_codex_tui` の実装詳細そのものを追いたいときは、対応する実装側のファイルへ進む。
- ファイルアクセスルールや prompt 生成の仕様だけを確認したいときは、このテスト群ではなく該当する oracle 側の文書や実装を読む。
- CLI 全体の他サブコマンドや一般的なログ基盤だけが目的なら、この TUI 専用テストは読まなくてよい。

## hash
- 5b8457f85b5ff274813916d8885359cdc71bb2d2c7cb4cfe039313872822688f

# `test_development_validation_config.py`

## Summary
- 開発用の依存関係と検証ツールの設定が、実行時依存やワークスペース設定と混ざっていないかを確認したいときに読む。`pyproject.toml` の開発向け分離、`ruff`/`mypy`/`pytest-timeout` の固定条件、VS Code の Python formatter 設定を対象にする。

## Read this when
- 開発用ツールを runtime dependency から分けるルールを確認したいとき。
- `pyproject.toml` の検証設定が、lint・型チェック・テストタイムアウトの前提をどう固定しているかを確認したいとき。
- ワークスペースの Python formatter を Ruff に寄せる設定や、Black を使わない前提を確認したいとき。

## Do not read this when
- アプリ本体の CLI 挙動やコマンド構成を確認したいだけのとき。
- 依存関係の追加先やバージョン方針を直接知りたいだけで、開発検証設定ではないとき。
- テストの振る舞いや実装ロジックそのものを確認したいとき。

## hash
- 2ad6f30b4b01908bdaa522a86085e4d558cf39566ef40ca1a3698dacbe68720c

# `test_doctor_cli.py`

## Summary
- `doctor preprocess` の外部契約を、CLI 呼び出しと直接関数呼び出しの両方から確認する統合テスト群。`.cmoc/gu`、`.agents`、設定、共有 doctor lock、managed Ollama、Git index の相互作用をまとめて検証する。

## Read this when
- doctor preprocess の修復後に、作業 tree と Git index の両方がどう保たれるかを確認したいとき。
- linked worktree で doctor / preprocess を実行したときの共有 lock、設定の参照先、修復 commit の副作用を追いたいとき。
- 共有 Ollama の再利用や `.cmoc/gu` の追跡・除外の境界を、他の doctor 系テストではなくこの統合テストから確認したいとき。

## Do not read this when
- 単体の設定同期や個別 helper の挙動だけを見たいときは、より対象の狭いテストへ進む。
- doctor preprocess 以外のサブコマンドや別の worktree 操作を調べたいときは、このファイルではなく該当するサブコマンド別のテストを読む。
- managed Ollama だけの仕様を確認したいときは、Ollama 専用の仕様・テストを読む。

## hash
- bfac4be0bdb1d27ce444e661b9b70df994e9e7715546d6e767f8da67662f2cf8

# `test_indexing_cli.py`

## Summary
- `cmoc indexing` の CLI から preflight、INDEX.md 生成、commit までの外部挙動を検証するテスト群。
- 通常の indexing、linked worktree、dirty/worktree 判定、既存差分の扱い、Codex 呼び出し条件、commit 対象の絞り込みを確認する入口。
- `commit_index_updates` の git 操作エラー扱いなど、indexing 共通処理の失敗時挙動もここで押さえる。

## Read this when
- `cmoc indexing` の CLI 振る舞いを変えたとき。
- preflight や worktree 判定、INDEX.md 更新後の commit 条件を確認したいとき。
- Codex structured output の利用や、fresh な INDEX.md を再生成しない条件を確認したいとき。
- indexing 共通処理の git エラー扱いを見たいとき。

## Do not read this when
- `cmoc indexing` 以外の CLI を見たいときは、より直接のコマンド別テストを読む。
- INDEX.md の生成ロジックそのものを追いたいときは、CLI テストではなく indexing 共通処理や実装側を見る。
- 個別の git 操作ユーティリティの一般仕様だけを見たいときは、対応する共通ユーティリティ側を読む。

## hash
- 36b551e09e00c75966084096350fb55f167f5a64d7d0face8bbfa7d30ddd7dc6

# `test_indexing_common.py`

## Summary
- `commons.indexing` の INDEX 生成と更新判定を直接検証するテスト群。
- 入力検証、既存 hash の再利用、空ディレクトリ、兄弟項目の順序、並列生成、memo 配下と symlink cycle の扱いをまとめて見る入口。

## Read this when
- `render_index_entry` の受け入れ条件や拒否条件を確認したいとき。
- `update_indexes` が既存の INDEX を再生成・削除・追加する条件を確かめたいとき。
- directory traversal の範囲、並列実行、ログ伝播の挙動を確認したいとき。

## Do not read this when
- CLI の引数、事前条件、commit lifecycle を見たいだけなら `cmoc indexing` 側のテストを見る。
- prompt 文面や agent call の正本仕様だけを確認したいなら oracle 側を見る。
- `commons.indexing` の実装詳細を追うだけならこのテストではなく実装本体を読む。

## hash
- e5828e6724da053456ce98b3f1ef2f1af15411f71679509f05db15fb993579ca

# `test_indexing_preflight.py`

## Summary
- - `run_codex_exec` / `run_codex_tui` に入る直前の indexing preflight の実行有無、順序、対象 worktree の選択、repository lock 待機、回復処理の抑止を検証するテストがある。
- - Codex 呼び出しに付随する indexing の事後挙動を、`commons.indexing` と `commons.runtime_codex_preflight` の連携を通して確認する。
- - `cmoc` の file access violation 後に recovery 用の indexing を追加しないことを確認するテストがある。

## Read this when
- - Codex 実行前に indexing preflight が走る条件や走らない条件を確認したいとき。
- - linked worktree を含む root 選択の扱いを確認したいとき。
- - repository lock がある状態で preflight が待機するかを確認したいとき。
- - file access violation 後に recovery 用の追加 indexing を抑止する挙動を確認したいとき。

## Do not read this when
- - indexing で生成される `INDEX.md` の目次内容そのものを確認したいとき。
- - `commons.indexing` の内部実装や lock 取得の詳細を追いたいとき。
- - Codex CLI 呼び出し引数や prompt 生成の正本仕様を確認したいとき。

## hash
- 5a3983f011162d984249db6bdbb3213cf05ccceb7faac6cef5452516b55ad8c7

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
- `oracle.prompt_builder` の各 standard と `build_complete_prompt` の組み立て結果を検証するテスト群。新しい prompt part を追加・変更したときや、既存 part の文言・含有条件・既定の有無を確認したいときに読む。

## Read this when
- `build_complete_prompt` がどの標準文書を常に含めるか、オプションで含めるかを確認したい。
- `file_access_mode` ごとのルール文言や、`oracle standard` / `realization standard` / `routing rule` / `index entry standard` / `review oracle standard` / `apply review standard` の含有条件を変える。
- `{{work-root}}` などのプレースホルダ保持や、Markdown レンダリング結果に現れるべき語句を調整する。

## Do not read this when
- prompt 部品そのものの仕様や本文を直接変更したい場合は、各 `oracle/src/oracle/prompt_builder/parts/*` の正本仕様を読む。
- CLI の実行フローやサブコマンドの挙動を確認したい場合は、このテストではなく該当する `src/sub_commands/*` 側を読む。
- 個別の構造化文書レンダリング実装や型定義を見たいだけなら、`basic.struct_doc` や関連の実装テストを読む。

## hash
- 0441f439e8568197fae2682dd5d7c85e8e7936329617001a66c386da6cee4b35

# `test_review_oracle_loop.py`

## Summary
- `cmoc review oracle` の finding loop を検証するテスト群。oracle ごとの列挙、同一周回の検証結果の受け渡し、merge 再試行、中断時の部分結果保持など、review oracle のループ制御に関わる変更を確認する入口。
- 隔離 worktree と Codex 呼び出しコンテキストを固定して、review oracle の各 agent call が正しい prompt と実行基準を使うかを確かめる。

## Read this when
- `cmoc review oracle` の finding 列挙・merge・validate・judge のループ制御を変えるとき。
- review oracle の中断処理や、完了済み判定だけを保持する挙動を確認したいとき。
- review oracle が Codex 呼び出しへ渡す prompt、purpose、cwd/root の整合性を検証したいとき。
- review oracle のテスト fixture や helper が、隔離 worktree と repo root の分離に関係するとき。

## Do not read this when
- `cmoc review oracle` のレポート本文や frontmatter の整形だけを変えるとき。
- Codex CLI の一般的な呼び出し規約や Structured Output の共通仕様だけを確認したいとき。
- review oracle 以外のサブコマンドや、別の review 系テストを変更するとき。
- oracle file の内容そのものを編集するとき。

## hash
- ac1c57dca840549eccab59a890973ff6eb6632360bd8fe8bb94306eeab1b5d57

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
- `review oracle` のレポート生成と CLI 結果を検証するテスト群。報告書の節順、所見の採否分類、`oracle-root` と symlink の集計、`-s` の受け渡し、中断・失敗時の報告までを扱う。

## Read this when
- `review oracle` の出力形式、所見の分類、件数集計、終了時の報告内容を変えるとき。
- `review oracle` の CLI 引数や `eval-oracle` からの委譲が report 生成にどう反映されるかを確認したいとき。
- 中断時・処理失敗時にどの report が残るべきか、どのメッセージが表示されるべきかを確認したいとき。

## Do not read this when
- `review oracle` の実装ロジックそのものを追うだけなら、まず対応する実装ファイルを読む。
- 他のサブコマンドや別種の report のテストを探しているなら、このファイルではなく該当サブコマンドのテストを読む。
- 一般的な oracle 仕様の本体を確認したいだけなら、`oracle/doc/app_spec/sub_command/review_oracle.md` 側を読む。

## hash
- d71e57ea40ce6d2c9f2c60c201181f8390ba8fba35be91bd4e289ff602096b1d

# `test_review_oracle_targets.py`

## Summary
- `review oracle` の対象列挙と finding path 解決のテストをまとめている。`oracle` 配下の相対・絶対・symlink・ignored file の扱い、`session` と `full` の対象差、`AGENTS.md` と `INDEX.md` の除外を確認したいときに読む。

## Read this when
- `review oracle` のレビュー対象ファイルの列挙条件や、finding から oracle file への path 解決を変えるとき
- git ignore、symlink、`memo` 配下、`AGENTS.md`、`INDEX.md` の扱いが対象判定に影響するか確認したいとき
- `session` scope の起点・終点や、`full` scope の総対象数の見え方を確認したいとき

## Do not read this when
- `review oracle` のレポート文面や採否判定ロジックだけを変えるときは、対象列挙より先に `review oracle` 本体を読む
- 対象選定ではなく、他の review サブコマンドや別の CLI の実行手順を変えるとき

## hash
- dcfa1ced2402f61ad1e346817fa3021e15ee55f1ab3d07a26552a090e1ab85f9

# `test_review_oracle_worktree.py`

## Summary
- `cmoc review oracle` の実行で使う worktree、ブランチ、`INDEX.md` 統合、preflight に関する振る舞いを検証するテストが入っている。
- `review oracle` が session worktree だけを対象にすること、未コミット差分を拒否すること、review worktree で更新された `INDEX.md` が session 側へ取り込まれること、`INDEX.md` 以外の差分を作った場合に失敗することを確認したいときに読む。

## Read this when
- `cmoc review oracle` の worktree 隔離やブランチ解決の挙動を追加・修正するとき。
- review 対象の範囲、未コミット差分の拒否、`INDEX.md` のマージ解決、preflight が作る `INDEX.md` の扱いを変更するとき。
- `review oracle` の回帰テストを追加・整理するとき。

## Do not read this when
- `review oracle` の実装本体や CLI 引数仕様そのものを確認したいだけのときは、実装側や仕様文書を先に読む。
- `INDEX.md` の一般的な生成仕様だけを確認したいときは、インデクシング側の文書を先に読む。
- `session fork` や通常の branch model だけを確認したいときは、このテストではなく branch model 側を読む。

## hash
- 6d41d19e151b4d24b6e230867386fca9294f4bda468b5ab0de801915550ceacd

# `test_runtime_apply.py`

## Summary
- `commons.runtime_apply` の停止処理に対する低レベル契約を確認したいときに読む。親 process と child group の停止順、PID reuse の扱い、pidfd と process group の安全な停止、apply process id ファイルの再読込やロック待ちを検証するテスト群への案内として置く。
- `test_apply_abandon_cli.py` ではなく、CLI を介さない runtime 層の挙動を追いたいときに読む。apply abandon の外部 CLI 挙動より、pid file・advisory lock・pidfd・process group の契約確認が主目的のときに読む先を分ける。

## Read this when
- apply runtime の process tracking や停止契約を変更したとき
- apply process id ファイルの読み取りや lock 待ちの仕様を確認したいとき
- 親 process 終了後の child group 再読込、stale PID の無視、終了済み process への signal 送信抑止を検証したいとき

## Do not read this when
- apply abandon の CLI 出力や引数など、外部 CLI 挙動だけを確認したいときは `test_apply_abandon_cli.py` を読む
- runtime_apply 以外の subcommand 仕様や別の process 制御を確認したいときは、このテスト群ではなく該当する別の対象を読む

## hash
- d30fdeb2cf5c1b9706ac5155164ce60e269e1e827c4bf7ea963da6427c3fff3a

# `test_runtime_cli.py`

## Summary
- CLI の起動境界、エラー整形、preflight、サブコマンドログ、shell completion の振る舞いを検証するテスト群。`main`、`commons.runtime_cli`、`commons.runtime_logging`、`cmoc_runtime` の跨ぎを確認したいときに読む。

## Read this when
- CLI が利用者向けに stdout / stderr のどちらへ何を出すべきか確認したいとき。
- `CmocError` の表示形式、parse error の扱い、work root 外実行の拒否、completion probe で副作用を出さない条件を確認したいとき。
- preflight や doctor preprocess、サブコマンドログ、gitignore 更新の境界を確認したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジックや indexing / review / apply の詳細仕様だけを見たいとき。
- `INDEX.md` の生成方針やルーティング規則そのものを確認したいときは、ここではなく対象階層の案内文を読むべき。
- `path_model` などの単体仕様だけを確認したいときは、このテスト群より直接の定義を見るべき。

## hash
- 2d587029ae8930097a76565528d2304e102088a9fc9ed9253b08b9fa2b50c144

# `test_runtime_codex_conflicts.py`

## Summary
- `cmoc session join` の conflict 対象に対する Codex の書き込み許可判定を検証するテスト群。`build_codex_override_args` が conflict 解消用の追加書き込み許可をどう正規化し、`oracle/INDEX.md`・`oracle/AGENTS.md`・ルート直下の `INDEX.md`・`AGENTS.md`・`.git` などの禁止対象を拒否し、`README.md` のような許可対象を通すかを確認するときに読む。

## Read this when
- session join の conflict 解消で使う書き込み許可パスの判定や制限を変えるとき
- Codex の permission root 生成・検証ロジックを、`oracle` 配下やルート直下の特定名ファイルを含めて見直すとき
- conflict resolution 用 parameter と、実際の writable roots の対応をテストで確認したいとき

## Do not read this when
- merge conflict 解消用 prompt 本文そのものを直したいだけのとき
- `build_session_join_conflict_resolution_parameter` の prompt 文面やモデル設定だけを変更するとき
- 一般的な file access rule の全体仕様を追いたいだけなら、まず対象の実装や共通ルール側を読むべきとき

## hash
- f3a04d3957a9b9c61f3fcf03ab8338e8fa5e0b5272b03d781c745e70229955bb

# `test_runtime_codex_permissions.py`

## Summary
- Codex CLI 呼び出し用のファイルアクセス権限を、モード別の上書き argv と追加 writable path の制約まで含めて確認するテスト群。`build_codex_override_args` が意図した保護領域を外さず、必要な例外だけを通すかを見たいときに読む。

## Read this when
- Codex の read/write 許可領域、`extra_writable_paths`、または mode ごとの保護範囲の変更を扱うとき。
- `git ignore` や tracked / untracked の境界が、権限生成に混入していないかを確認したいとき。
- 生成した argv が実際の Codex CLI で受理されるか、少なくとも権限プロファイルとして破綻していないかを確認したいとき。

## Do not read this when
- プロンプト本文や正本仕様の記述そのものを直したいときは、対応する oracle 側の文書や builder を先に読む。
- ファイルアクセス以外の Codex 実行規約、doctor preprocess、あるいは一般的な runtime 初期化を見たいとき。
- 権限の内部実装分割や補助関数の構成だけを変えたいときは、まず関連する実装ファイルを読む。

## hash
- af4a9b6c13cc37d280491df2c06ba02f0e5a01cf046636f64bac77a846018d34

# `test_runtime_codex_profile.py`

## Summary
- Codex CLI 呼び出し用の上書き引数が、ファイルアクセス制限・書き込み範囲・`.cmoc` の特例・symlink の外部解決拒否・linked worktree 時の追加 read root を正しく反映するかを確認するテスト群。
- 同じ領域で、ローカル SLM を `cmoc managed ollama` 経由で使う設定が選ばれ、モデル名と model provider の上書きが整合するかも確認する。

## Read this when
- Codex 呼び出しの sandbox / permission / writable root の組み立てが正しいかを確認したいとき。
- repo 外へ解決する symlink、extra writable/read root、linked worktree の扱いなど、アクセス境界の事後確認が必要なとき。
- `cmoc managed ollama` を使うときに、Codex 側へ渡る model provider 設定とモデル選択を検証したいとき。

## Do not read this when
- ファイルアクセス規則そのものの正本仕様を確認したいときは、対応する oracle 側の仕様断片を読む。
- Codex 呼び出しの入出力保存や stdout / stderr / schema の規約を確認したいときは、このテストではなく `codex exec` 規約側を読む。
- `cmoc managed ollama` のサービス運用、GPU 推論の保証、永続化資源のライフサイクルを確認したいときは、ollama 管理の仕様側を読む。

## hash
- 74c05e39a60683fdaa529b6ae02e72c716a115a928b1ad84c3aee5df4b90be01

# `test_runtime_config.py`

## Summary
- `CmocConfig` の既定値、JSON 往復、設定ファイル読み込み時の永続化先、入力検証の失敗挙動を確認するテスト群。
- `cmoc config` の論理的な既定値と、`cmoc doctor` が生成する設定ファイルとの整合を確かめたいときに読む。

## Read this when
- `CmocConfig` の既定値や、`ModelClass` / `ReasoningEffort` の対応を変える予定がある。
- 設定 JSON のキー順、enum の value 化、`num_try_falv_recovery` の保持方法を変える予定がある。
- 設定ファイルが無い場合や、設定値の型・値が不正な場合のエラー扱いを確認したい。

## Do not read this when
- `cmoc apply fork` や `cmoc review oracle` の個別挙動だけを変えたい。
- 設定の読み書きではなく、別のランタイム機能や CLI サブコマンドのテストを探している。
- `cmoc doctor` の生成処理そのものや、エラーレポートの共通仕様だけを確認したい。

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
- `FileAccessMode` の永続化値と、Codex sandbox の変換対応範囲を確認する契約テスト。ファイルアクセス権の文字列表現や sandbox mode 変換を変えるときに読む。

## Read this when
- `FileAccessMode` の列挙値を永続化・JSON 共有可能な文字列として固定したいとき。
- ファイルアクセス権から Codex sandbox mode への変換で、どのモードまで欠落なく対応すべきか確認したいとき。

## Do not read this when
- CLI 引数や実行フロー全体の仕様を追いたいときは、テスト本体より上位のワークフロー文書を読む。
- sandbox 実行の内部実装や変換の細部だけを追いたいときは、対応する実装側を直接読む。

## hash
- 19361995f4afc23f26eea207116d1ee3ff1c522b700829c9d7cc91644168b0fd

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
- `commons.runtime_state` の `SessionState` 永続化と、session/apply の branch 名から state を復元・検証する境界テストをまとめたもの。
- `session_fork_lock` の process 間排他が成立することも含むため、state 形状だけでなく fork/join 周辺の並行制御を確認したいときに読む。
- session/apply の CLI 振る舞いそのものではなく、branch 解析・state 読み書き・lock の共有性を確かめる実装とテストの入口。

## Read this when
- session/apply state ファイルの JSON 形状や検証条件を変える。
- `cmoc/session/...` や `cmoc/apply/...` の branch 名から state を読む/書く処理を修正する。
- session fork の排他や、別 process から見ても同じ lock になることを確認したい。

## Do not read this when
- session fork/join の CLI 引数、merge 手順、エラーメッセージ全体を追いたい場合は `src/sub_commands/session/` 側を読む。
- apply 側の fork/join の CLI 挙動を確認したい場合は `test/test_apply_*.py` 側を読む。
- state ファイルの配置規約そのものを確認したいだけなら、対応する oracle doc を直接読む。

## hash
- 22b1f87c9f35afd65af5720151a23a425df5df6117418949ab1a1e5357705c30

# `test_session_cli.py`

## Summary
- `session` サブコマンドの `fork` / `join` / `abandon` に関する外部挙動をまとめて確認する回帰テスト群。session branch と session state の生成・更新・削除、linked worktree からの実行、dirty worktree の拒否、conflict 解消と cleanup の成否を一度に追いたいときに読む。
- 個別の session 実装や正本仕様を直接読む前に、この CLI 変更が branch/state ライフサイクル全体へどう波及するかを把握したい場合の入口として使う。

## Read this when
- session の fork / join / abandon の変更で、branch 作成・切替・削除と session state の遷移をまとめて確認したいとき。
- linked worktree から実行したときの home branch / session branch の扱いを確認したいとき。
- session join の conflict 解消、REPO_WRITE 境界、unmerged path、conflict marker 検出、delete conflict resolution を確認したいとき。
- session abandon の前提条件、cleanup 失敗時のロールバック、preprocess の順序、dirty worktree 拒否を確認したいとき。

## Do not read this when
- session 以外のサブコマンドの挙動を見たいときは、対応する別の test 本文へ進む。
- session の仕様そのものを把握したいだけなら、ここではなく対応する oracle 側を読む。
- 個別 helper の細かな実装差だけを追いたいときは、この統合テスト群ではなく該当実装を直接読む。

## hash
- 5eefdcc6a9be601afe119924f3026a8c76a0be618b311aee21f9b4e066b24bb9

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
