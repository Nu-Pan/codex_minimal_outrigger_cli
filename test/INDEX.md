# `_acp_builder_support.py`

## Summary
- `test` 配下で、`acp_builder` の正本 schema をテストから参照するための共通 path helper を置く補助対象である。`test` 側に schema を複製せず、oracle 側の `acp_builder` 定義へ直接つなぐ必要があるときに読む。

## Read this when
- `acp_builder` の正本 schema をテストから参照する共通 helper の挙動を確認・変更したいとき。
- テスト用に正本 schema をコピーせず、oracle 側を参照する方針がどこで支えられているかを確認したいとき。
- `acp_builder` 関連のテスト helper が他にあるかではなく、この path 解決 helper の責務を見たいとき。

## Do not read this when
- 個別の `acp_builder` 仕様や builder 本体を確認したいときは、対応する oracle 側の本文を読む。
- テスト全体の CLI 挙動や他の共通サポートを確認したいときは、この helper ではなく該当する別の test support を読む。
- `INDEX.md` のルーティング方針そのものを確認したいときは、この helper ではなく上位の案内を読む。

## hash
- de5d24592d722cda97a3290b3f356479ac2cea7bc27a0e17c7391864eced41f9

# `_apply_support.py`

## Summary
- `apply` セッション状態から管理対象の作業先パスを復元するテスト補助関数。状態スナップショットに含まれるブランチ表現を直接解釈し、通常の作業先探索経路に依存しない形で期待パスを組み立てる。

## Read this when
- `apply` の状態から作業先パスを導く仕様を確認したいとき。
- ブランチ名の妥当性検証と、その結果としてどの作業先が選ばれるかをテスト側で合わせたいとき。
- `oracle/doc/branch_model.md` と `oracle/doc/app_spec/session_state.md` にある branch / state の約束に合わせて、apply 周辺のテストを調整したいとき。

## Do not read this when
- 通常の作業先探索や実運用のパス解決を追いたいとき。
- apply セッション以外の状態変換や、パス生成以外のテスト補助を探しているとき。
- branch モデルや session state の正本仕様そのものを確認したいとき。

## hash
- af6fe5225afe056c9a64fb9b2b027117b7068638e52fe8a37ce897e8ec8965da

# `_cli_support.py`

## Summary
- Typer CLI テストで共通に使う `CliRunner` の初期化をまとめた支援ファイル。CLI 実行を検証するテストから、この runner を使ってコマンド呼び出しを統一したいときに読む。

## Read this when
- Typer ベースの CLI テストで、同じ `CliRunner` 初期化を繰り返したくないとき。
- CLI の入出力や終了コードを `typer.testing.CliRunner` で検証するテストを書きたいとき。

## Do not read this when
- CLI 実装本体やコマンド定義を確認したいとき。
- `CliRunner` 以外のテスト支援や汎用 fixture を探しているとき。

## hash
- 33b0c8871904c2ecfda13d625de6c4970ac753a13c325110e0e1f1fd986aa0fc

# `_codex_support.py`

## Summary
- Codex 実行時の引数組み立てと、テストからそれを安定して検証するための支援関数を集めたファイル。Codex 実行ルール本体、サンドボックス上書き、Codex Home の最小認証状態、既存実装の引数検証に使う小さな共通補助を読むときに進む。

## Read this when
- Codex 実行コマンドの生成や上書き設定の検証方法を確認したいとき。
- テストで使う最小限の Codex Home や、引数・設定の共通補助を再利用したいとき。
- 実行ルールやファイルアクセス制御の仕様を、テスト用の補助実装にどう反映しているかを追いたいとき。

## Do not read this when
- Codex 実行ルールそのものの仕様本文を読みたいときは、対応する oracle doc を先に読む。
- ファイルアクセス規則や sandbox の本仕様を確認したいだけなら、該当する正本仕様断片を直接読む。
- 実運用コードや CLI 本体の処理を追いたいだけなら、この補助ファイルではなく実装側へ進む。

## hash
- 11951f81dd839ac3bd08346386a834b152c2b4bc86b0245bbca537cf35641eb3

# `_command_support.py`

## Summary
- `test` 配下のテストで、`PATH` 上に置く偽の外部コマンドを現在の Python で起動する実行可能スクリプトとして作る共通補助をまとめる。UTF-8 で書き出し、実行権限も付与する入口を読むときに使う。

## Read this when
- 外部コマンドを差し替えるテストで、実行可能なスタブを共通の方法で作りたい。
- テスト用の fake command を Python スクリプトとして生成し、`PATH` に置ける形にしたい。
- `<work-root>/oracle/doc/dev_rule/development_environment.md` にある文字コード条件に合わせて、テスト補助の書き込み方法を確認したい。

## Do not read this when
- 個別テスト対象の振る舞いだけを追いたいときは、呼び出し元の test 本文を直接読む。
- 偽コマンドではなく、`CliRunner` や他の汎用テスト補助を探しているときは別の helper を読む。
- シェルスクリプトや永続的な補助ファイルの設計を確認したいだけなら、このファイルではなく該当する実装側を見る。

## hash
- 78d7ba1ca351ee033f9cbc2503f4e112b9201a9250051383121074d940cca412

# `_git_support.py`

## Summary
- `git` を使う CLI テスト用の最小リポジトリを作る共通ヘルパー。`run_git` で失敗時に例外化し、`current_branch` で現在ブランチを検証しやすくし、`make_repo` で初期コミット済みの土台を作る。`add_tracked_ignored_oracle_file` は、追跡対象だが ignore ルールにも掛かる oracle ファイルをテスト上で用意するために使う。

## Read this when
- 複数の CLI テストで共通の git 初期化や repository fixture をどう作っているか確認したいとき。
- テスト用リポジトリが user 設定や hook 設定に依存しない前提をどこで固定しているか知りたいとき。
- 追跡済みだが ignore される oracle ファイルを使うテストの前提を確認したいとき。

## Do not read this when
- 個別の CLI 挙動や分岐を追いたいだけなら、各 test ファイルを直接読む。
- git 操作そのものの実装やエラー処理方針を知りたいなら、ヘルパーではなく呼び出し側のテスト本文を読む。
- INDEX.md のルーティング方針や仕様断片の本文を探しているなら、この補助ヘルパーではなく oracle 側の文書を読む。

## hash
- 1d48e6c7b42a457fcda7915b700f259d7f835104a190f530d7ee27c40bc6c33e

# `_ollama_support.py`

## Summary
- `doctor` CLI のテストから、指定した worktree を cwd にして `doctor` を実行し、cmoc managed Ollama を本番共有のまま使うための共通補助です。`doctor` の呼び出し方と、テスト境界として fake サービス管理を含めない前提を確認したいときに読む対象です。

## Read this when
- `doctor` コマンドのテストや呼び出し補助を実装・修正するとき
- worktree を cwd で識別する前提や、cmoc managed Ollama を本番と共有する前提を確認したいとき

## Do not read this when
- `doctor` 以外の CLI 補助を探しているとき
- fake な Ollama サービスのライフサイクル管理や、サービス起動/停止そのものの仕様を確認したいとき

## hash
- bba6138ff1b9985aaaa86beda1fc713f0ff4ef3211b3e1b13b60e054a4ac6008

# `test_acp_builder_apply_parameters.py`

## Summary
- `acp.builder.apply.fork` 配下の parameter 生成が、正本 schema の参照先・prompt・モデル設定を意図どおりに組み立てるかを確認するテスト。パッケージ配置からの import 可否、`<repo-root>` と `<work-root>` の解決、`<target-path>` の扱い、schema 一致を見たいときに読む。

## Read this when
- `apply/fork` 用の parameter builder が、どの正本 schema を指すべきか確認したいとき。
- prompt に含める標準文面や root の埋め込み方、`<repo-root>` / `<work-root>` / `<target-path>` の使い分けを変更したいとき。
- packaged layout でも import できること、または target path の相対指定に関する制約を確認したいとき。

## Do not read this when
- `acp.builder.apply.fork` の実装本体や prompt 生成ロジックそのものを追いたいときは、対応する `src` 側を直接読む。
- 正本 schema の中身や運用ルールを知りたいだけなら、このテストではなく対応する `oracle` 側の schema・doc を読む。
- `apply/fork` 以外の subcommand の parameter 生成を見たいときは、各 subcommand の個別テストへ進む。

## hash
- 35db896a2f164d366da03dc8a72d687703b985e3f8f6014835460e60210d86f0

# `test_acp_builder_indexing_parameters.py`

## Summary
- `acp.builder.indexing.index_entry` の互換ビルダーが、indexing 用の実行条件を最小権限・低負荷に固定して返すことを確認するテスト。あわせて、このモジュールの公開面が互換ビルダーだけに絞られていることを検証する。

## Read this when
- indexing 用の INDEX エントリー生成が、どの `ModelClass`・`ReasoningEffort`・`FileAccessMode` を選ぶべきか確認したいとき。
- モジュールの公開面を整理していて、互換ビルダー以外の補助実装を見せないことを確かめたいとき。

## Do not read this when
- indexing の正本仕様そのものを確認したいときは、対応する oracle 側の定義を読む。
- indexing 以外のエントリー生成や、実装内部の分割方針を調べたいときはこのテストではなく該当する実装側を見る。

## hash
- 9cf2e5899a2e454b72d47eba735854f4be26d61d7705ad61f2975e2012497c8d

# `test_acp_builder_review_oracle_parameters.py`

## Summary
- review oracle ACP builder の各 parameter builder が返す `AgentCallParameter` の公開面と、対応する structured output schema を検証するテスト群。互換ラッパーの export 範囲、モデル設定、schema ファイル一致、prompt 内の `<oracle-root>` 置換や動的文字列保持を確認する。

## Read this when
- review oracle 向け builder の公開 API を変えるとき
- schema JSON との一致や prompt 置換規則を確認したいとき
- 互換公開面の export 範囲や余計な内部記号の露出を検査したいとき

## Do not read this when
- review oracle builder の実装本文や prompt 生成ロジックそのものを追いたいときは、対応する `oracle/src/oracle/acp_builder/review/oracle/` 側を読む
- review 以外の ACP builder の parameter や schema を調べたいとき
- oracle 仕様本文の修正方針を決めたいだけのとき

## hash
- 92b72d198438ac9a435b293e2a21024fb995ae292469b834d42ebec573ab4059

# `test_acp_builder_session_join_parameters.py`

## Summary
- `acp.builder.session.join.conflict_resolution` の公開面と、conflict resolution 用パラメータの契約を検証するテスト。ビルダ以外を export しないこと、repo write 権限で高強度推論を使うこと、prompt に conflict 対象ファイルが含まれることを確認する。

## Read this when
- session join の conflict resolution builder がどの公開 API を持つべきか確認したいとき。
- conflict resolution 用の agent call パラメータが、モデル種別・推論強度・ファイルアクセス権限・事前 indexing の有無をどう固定しているか確認したいとき。
- 公開モジュールから内部依存が漏れていないかを検証するテストを追加・更新したいとき。

## Do not read this when
- conflict resolution の実装本体や prompt 組み立てロジックの詳細を追いたいときは、対応する実装側を直接読むべき。
- session join 以外の builder や他の agent parameter の契約を確認したいときは、このテストではなく該当領域のテストを読むべき。
- 一般的な ACP パラメータ仕様を知りたいだけなら、このファイルではなく型定義や共通実装を読むべき。

## hash
- eaf28ad4dbb1c7591faa34e604dfdeb606731bcf327b153ff757134f3a5181c7

# `test_acp_builder_tui_parameters.py`

## Summary
- TUI 用の resolve_parameter ビルダーと、その返却値の正本仕様との対応を確認するテスト群。ビルダーが埋め込む元プロンプト、選択されるモデル系パラメータ、公開されるモジュール名、生成される structured output schema の整合性をまとめて検証する。

## Read this when
- `acp.builder.tui.resolve_parameter` の出力内容を変えるとき。
- TUI から生成する実行パラメータの既定値や、返却オブジェクトに埋め込む説明文を確認したいとき。
- structured output schema の必須項目、型、列挙値、公開 API の変化を検証したいとき。

## Do not read this when
- TUI resolve_parameter の内部実装や補助関数の分割だけを確認したいときは、対象の実装本文を読む。
- 他の builder や別コマンドのパラメータ定義を追いたいときは、その対象のテスト群を読む。
- 単に正本仕様の内容そのものを確認したいときは、対応する oracle 側の本文を読む。

## hash
- 56aeb783a50189d8710750fb7c69c5001b71827cf413ed53f9cf438f83d75956

# `test_apply_abandon_cli.py`

## Summary
- `cmoc apply abandon` の CLI 挙動を、実行位置・状態検証・worktree/branch/state の後始末・追跡中 process の停止まで含めて確認するテスト群。破棄成功、cleanup 警告、running/error の停止順序、破損 state の拒否をまとめて扱う。
- 同じ apply abandon の外部挙動を一箇所で読めるようにし、`apply` の開始や join、他のサブコマンドではなく abandon 専用の境界条件を確認したいときの入口にする。

## Read this when
- `cmoc apply abandon` の成功時 cleanup と失敗条件を CLI 経由で確認したいとき。
- active apply run の破棄時に、worktree と branch の削除、apply state の遷移、実行中 process の停止順序を確認したいとき。
- session branch / apply branch 上からの実行可否や、破損した state を拒否する条件を確認したいとき。

## Do not read this when
- `cmoc apply fork` の生成条件や active apply run の作成手順を見たいとき。
- `cmoc apply join` の挙動や、join 後の state 遷移を見たいとき。
- process 停止の共通実装だけを見たいときは、CLI テストより `src/commons/runtime_apply.py` を先に読む。

## hash
- d99ea492d950d98b52b59750dbab3a7debcaf7d2a32c2a7e53de994ddc45d83a

# `test_apply_fork_cli.py`

## Summary
- `apply fork` CLI の回帰テスト群。Codex ループ、session/apply state の遷移、linked worktree からの開始、doctor preprocess、`.gitignore` への反映、設定欠落時の失敗、report 直前の state 更新を確認する。
- 対象の正規化ルール自体は別テストモジュールで扱うため、このファイルは CLI のライフサイクルと副作用の検証に読む。

## Read this when
- `apply fork` の実行前後で session state、apply branch、apply worktree、process state、report 生成順を確認したいとき。
- `.gitignore` や `.cmoc/local/` の ignore 反映が、clean な worktree を保ったまま行われるか確認したいとき。
- 設定不足・設定破損時に apply run を開始しないこと、また Codex 呼び出しに進まないことを確認したいとき。

## Do not read this when
- target path の正規化だけを追いたいときは、別の apply fork target normalization テストを読む。
- `session fork` 単体の仕様や、apply 以外の sub command を確認したいとき。
- CLI 本体ではなく、report 出力の詳細だけを確認したいとき。

## hash
- a57a31b0e157475c6e5b7711e1d7126909053304420e2d00c40101d6ec5fbe7e

# `test_apply_fork_report_cli.py`

## Summary
- `apply fork` の report 生成、未収束・error 判定、変更要約、再検査対象の選び直し、rolling apply の対象切替を CLI 経由で確認したいときに読む。`fork` 実行後の report 形式と、session state への反映までをまとめて扱う。
- `sub_commands.apply.fork_report` や `sub_commands.apply.fork` の個別実装を読む前に、report に何を載せるべきかと、どの状況で収束・未収束・error になるかの境界を知りたいときの入口にする。

## Read this when
- `apply fork` の report 文面、front matter、変更内容要約、所見数の推移、result 判定を変更・確認したい。
- 所見適用後に再調査対象をどう選ぶか、変更ファイルが増えたときにどこまで再検査するかを確認したい。
- rolling apply で前回の apply join 後の変更だけを対象にする扱いを確認したい。

## Do not read this when
- 所見の抽出条件そのものを知りたいだけなら、apply fork の report ではなく所見列挙側を読む。
- session 作成や join の一般的な流れだけを確認したいなら、この report テストではなく session 側を読む。
- 変更要約の共通化や差分抽出の詳細だけを知りたいなら、report の CLI 期待値より `sub_commands.apply.fork_report` 側を優先して読む。

## hash
- 4656bd2a986b5c68262f80b1b2922840f2ba82324b14a610d84a5c9fd11b0fb8

# `test_apply_fork_target_normalization.py`

## Summary
- `sub_commands.apply.fork` の対象正規化ロジックを回帰検証するテスト群。`memo`/`.cmoc/local`/`.codex`/`.agents`/`AGENTS.md`/`INDEX.md` を除外しつつ、`oracle` 配下・入れ子の管理名・binary file・tracked ignored file・symlink の扱いを確認する変更時に読む。

## Read this when
- apply fork の対象選別や正規化条件を変えるとき。
- `oracle` 配下の file を対象に含めるか、`memo` や `.cmoc/local` などの管理領域を除外するかを調べるとき。
- tracked ignored file や symlink の扱いを含む対象集合の境界を確認するとき。

## Do not read this when
- apply fork の本体の適用処理や file 内容の変換を追うだけなら、`sub_commands.apply.fork` の実装側を先に読む。
- `oracle` 側の正本仕様そのものを確認したいだけなら、対応する oracle doc を読む。
- 対象選別ではなく commit や git 操作の実装を見たいだけなら、git helper 側を読む。

## hash
- c86830c3a4925f70cf4ed41babafd6f2d9f2a757e94f99a44c8663a36a365b44

# `test_apply_join_cli.py`

## Summary
- apply join の CLI 挙動を検証するテスト群。apply/session の join 成功、cleanup、state 更新、report 出力、dirty worktree、想定外差分、merge conflict、force 解決をまとめて確認する入口として使う。
- 同じ join 操作でも、branch/state/report などの外部挙動の可否判定を読むときにこのファイルへ進む。内部 helper の分割や実装詳細を追う目的では読まない。

## Read this when
- apply join の成功条件と拒否条件を CLI レベルで確認したいとき。
- worktree の cwd、dirty 状態、stale branch、想定外差分、rename、merge conflict、force 解決のどれかを含む join 挙動を確認したいとき。
- join 後に apply worktree、branch、session state、report がどう変わるかを知りたいとき。

## Do not read this when
- apply join の実装手順や内部関数の分割だけを知りたいときは、対応する実装側を読む。
- apply/join 以外の CLI や別サブコマンドの振る舞いを調べたいとき。
- fixture の作り方や git 操作の共通部だけを追いたいときは、支援モジュールを読む。

## hash
- c3debd038d7c93a0405813627ed399c4beeee25e120569885b97cfd50d2e9e8a

# `test_basic_runtime.py`

## Summary
- `basic.path_model` と `cmoc_runtime` の境界契約を検証するテスト群。`<run-root>` と `<cmoc-root>` の復元、repo root / work root / run root の区別、そして managed worktree 以外への作成・削除を拒否する挙動を確認したいときに読む。

## Read this when
- root placeholder から実パスを復元する規則を確認したいとき。
- linked worktree で repo root と run/work root をどう分けるかを確認したいとき。
- run worktree の作成・削除が managed 範囲外の path を拒否するかを確認したいとき。

## Do not read this when
- path token の設計や path model の本体実装を追いたいときは、対応する oracle src を読む。
- worktree の生成・削除ロジックの詳細な実装経路を見たいときは、runtime 側の実装ファイルを読む。
- git 操作の一般的なヘルパー実装や別の runtime 契約を確認したいときは、このテストではなく該当する別テストや実装を読む。

## hash
- f5de1d86db23e269cd8495acdd9de7005de81f92c10e8b2b24cdc926431819c9

# `test_cli_tui.py`

## Summary
- `cmoc tui` の外部挙動を検証するテスト群。エディタ入力の取り扱い、解決済みパラメータの生成、Codex TUI 起動、`_orig.md` / `_cmpl.md` の保存先と `linked worktree` での保存先切り替え、`.cmoc` の ignore を確認したいときに読む。

## Read this when
- `cmoc tui` の起動前処理や起動後のふるまいを変更するとき。
- オリジナルプロンプトのエディタ編集、解決パラメータ、TUI 起動引数、ログ保存先、`linked worktree` 対応を確認したいとき。
- `.cmoc` 配下の ignore や、repository 側と linked worktree 側のどちらへ保存されるかを確認したいとき。

## Do not read this when
- `cmoc tui` の仕様そのものを把握したいだけなら、対応する正本仕様の `oracle/doc/app_spec/sub_command/tui.md` を先に読む。
- 他のサブコマンドの CLI 挙動だけを変える作業では、このテストは直接は読まなくてよい。
- TUI 以外の共通 runner や補助関数の変更だけなら、まずそれらの実装・テストを読む。

## hash
- 5e6abb73dc0cd395eb8bc5baf6b8d98a6e9872b67d47c04672902426c659fe9d

# `test_codex_runtime_errors.py`

## Summary
- Codex 実行時の異常系を確認するテスト群。JSONL の不正イベント分類と、Codex CLI が見つからない場合の例外内容およびサブコマンドログの失敗記録を扱う。

## Read this when
- Codex 実行まわりのエラー分類を変更するとき。
- JSONL 解析失敗時の扱い、または CLI 不在時の失敗ログを確認したいとき。

## Do not read this when
- 通常の成功系や別サブコマンドのテストを探しているとき。
- ログ形式そのものの全体仕様や実行フロー全般を確認したいときは、対応する仕様文書や実装側を先に読むべきとき。

## hash
- 2415ad737a5a1b3e278627d80c1d4d71c4f3128d5cfaab52e08db2d2c3db088a

# `test_codex_runtime_exec.py`

## Summary
- `run_codex_exec` と `prepare_codex_override_args` の結合動作を確認するテスト群。実 Codex CLI の起動、`cmoc_managed_ollama` provider の選択、出力 schema の受け渡し、`CODEX_HOME` 設定ファイルを作らないことを扱う。
- `runtime_codex` の引数組み立てや、`runtime_doctor` による managed ollama 事前確認の境界を変える作業で読む。`codex_exec_rule` と `cmoc_managed_ollama` の仕様差分を確認したいときの入口にする。

## Read this when
- Codex 実行経路の統合テストを追加・修正するとき
- local SLM を `cmoc_managed_ollama` 経由で使う条件や preflight の扱いを変えるとき
- 出力 schema の保存先や `CODEX_HOME` に設定を書かない保証を確認したいとき

## Do not read this when
- CLI の他サブコマンドや一般的な prompt 生成だけを扱うとき
- `runtime_doctor` 単体の診断ロジックだけを変更するとき
- Codex 実行以外のファイルアクセスやリポジトリ操作の仕様を確認したいとき

## hash
- 3c2621c63ad7de247ec70672f51926e715bf8c75ded3b74af30b0dded31c02de

# `test_codex_runtime_home.py`

## Summary
- `run_codex_exec` の `CODEX_HOME` 解決と preflight validation を扱う回帰テスト群。未設定時の既定値、相対パスの解決、`auth.json` の存在確認、起動前に失敗する条件をまとめて確認したいときに読む。
- Codex subprocess を起動せずに失敗させる境界を押さえる入口でもある。`CODEX_HOME` の観測値と `call_log` の整合、子プロセス呼び出しの遮断を確認したい場合に読む。

## Read this when
- `CODEX_HOME` の未設定・相対指定・不正な実体の扱いを見直したいとき。
- `auth.json` の有無やファイル種別を理由に、Codex subprocess を起動する前に失敗するか確認したいとき。
- 実際に子プロセスへ渡る `CODEX_HOME` と、実行ログに残る解決済み path の一致を確認したいとき。

## Do not read this when
- `CODEX_HOME` 以外の Codex 実行引数、sandbox、権限、出力 schema を見たいときは別の Codex 実行テストを読む。
- Codex subprocess を起動した後の stdout/stderr 解釈や再試行を見たいときは、このファイルではなく実行結果系のテストを見る。

## hash
- 7ca625849cc63f8af4edaad358028fcc5df06290c621978ed9247d4e6455728c

# `test_codex_runtime_paths.py`

## Summary
- `run_codex_exec` の cwd 解決、出力 schema 保存先、権限 override の境界を検証する統合テスト群。`codex` 実行時の引数や権限マップが変わる作業で読む。
- 並列実行時の timestamp 衝突回避、linked worktree からの repo-local read 許可、`.agents` を write 対象に含めないことを確認したいときの入口。

## Read this when
- `run_codex_exec` の起動前後で、実行先ディレクトリや schema 保存先の決まり方を確認したい。
- cwd が `None` の場合と明示指定の場合で、`--cd` と実際の実行先が一致するかを確認したい。
- linked worktree から repo-local の追加 read path を許可する条件や、`.agents` tree を権限 override に含めない条件を確認したい。
- 同一 timestamp の並列実行でもログ path が衝突しないことを確認したい。

## Do not read this when
- `run_codex_exec` の内部実装や引数構築の詳細だけを追いたい場合は、関連する実装側を直接読む。
- 出力 schema の内容そのものや prompt 文面の仕様を確認したい場合は、このテストではなく正本仕様断片を読む。
- Git worktree 操作や test helper の一般仕様を知りたいだけなら、このファイルではなく対応する helper 側を読む。

## hash
- 51483245b0dcbe237824d80231cb14a68849406e48d4000295e1d7e7b9d307f3

# `test_codex_runtime_quota_retry.py`

## Summary
- `Codex` の quota 枯渇後に、probe 実行・resume token 復元・再実行・並行待機の制御を確認したいときに読む。外部挙動としては、初回失敗後の待機、代表 probe の一回化、resume の有無による再実行分岐、probe 失敗時の伝播、ロギング内容が主対象。
- この対象は、quota retry の状態機械を一箇所で追うための回帰テスト群として機能する。同じ fake Codex 呼び出し列を使う観点が強く、probe 共有・resume・call log・subcommand log をまとめて確認したい変更で優先して読む。
- `Codex` の quota retry 以外の一般的な実行経路や、quota と無関係な CLI 振る舞いを確認したい場合は優先度が低い。実装内部の helper 分割や個別の細かい制御よりも、quota 復帰の観測点が重要なときに読む。

## Read this when
- quota 超過後の再試行や resume 制御を変更した
- 代表 probe の共有や並行待機の扱いを確認したい
- call log, subcommand log, `CODEX_HOME`, `cwd` の観測結果をまとめて見たい
- resume token の復元や quota probe のエラーハンドリングを追いたい

## Do not read this when
- quota retry と無関係な通常実行のテストを探している
- 実装内部の helper 配置だけを確認したい
- CLI の一般的な引数解析や出力形式だけを確認したい
- quota 復帰ではなく別の失敗系を見たい

## hash
- f828e8dcc3b88dbe806c2f4429a37031c5824aa1361f43ec5a43b838cbcff9d8

# `test_codex_runtime_retry.py`

## Summary
- `run_codex_exec` の再試行判定と失敗時ログを確認したいときに読むテスト。Structured Output の検証失敗、capacity retry、JSONL error、KeyboardInterrupt、中断後の差分保持、stdout 以外の error marker の扱いを外部挙動として押さえている。

## Read this when
- Codex 実行の再試行条件や失敗時の記録方法を変更するとき。
- Structured Output のパース失敗や schema 不一致をどう扱うかを確認したいとき。
- capacity / quota まわりの retry 判定や、ログイベントの status・error・returncode の整合性を確認したいとき。
- 中断やエラー時に既存の差分や生成物が残るべきかを確認したいとき。

## Do not read this when
- Codex 実行の引数組み立てやプロンプト生成そのものを見たいときは、より近い実装側のファイルを読む。
- 一般的なログ基盤やサブコマンド共通ログの仕様だけを確認したいときは、対応するドキュメントやロガー実装を先に読む。
- Codex CLI 以外の実行経路や別サブコマンドの挙動を確認したいときは、このテストではなく該当経路のテストを読む。

## hash
- cc15d29643a56a9f8000ac8fbd57ef74936a0115f2c0c58d8a523b5f60d692a8

# `test_codex_runtime_subprocess.py`

## Summary
- `commons.runtime_codex_profile` の `run_codex_subprocess` / `run_tracked_codex_subprocess` に対する振る舞いを確認するテスト群。apply 実行中の Codex subprocess の process group 記録、`communicate()` 中断時の tracking 維持、継承された tracking 環境変数を無視する扱いを検証する。

## Read this when
- Codex subprocess の起動方法や process group の扱いを変えるとき。
- apply 実行中の child process tracking の記録・保持・削除条件を変えるとき。
- `CODEX_HOME` や `CMOC_APPLY_PROCESS_ID_PATH` の継承や無視の境界を確認したいとき。

## Do not read this when
- Codex CLI の一般的な error 判定や JSONL 解釈だけを変えるときは、`commons.runtime_codex_profile` 本体側を先に読む。
- apply abandon の pid file 排他制御や start time 判定だけを変えるときは、関連する他の apply/runtime テストを先に読む。

## hash
- f7111f256da1db596baf66d16b6f67c544eee649d1025388a6945b851747a2ab

# `test_codex_runtime_tui.py`

## Summary
- `codex_runtime_tui` の起動条件、追加読み取りパスの検査、Codex 呼び出し引数、ログ記録、失敗時の扱いをまとめた TUI ランタイム検証テスト群。
- `<work-root>/oracle/doc` と `<work-root>/oracle/src` の仕様断片に対して、実装が守るべき外部挙動を確認する入口。

## Read this when
- TUI 実行の事前検査や、許可外パス・完成済み prompt・linked worktree での振る舞いを確認したいとき。
- Codex 呼び出しの `--cd`、`--output-schema`、`--profile` などの引数制御を確認したいとき。
- call log、サブコマンドイベント、コンソール要約、非 0 終了、CLI 不在、KeyboardInterrupt の記録条件を確認したいとき。

## Do not read this when
- TUI 以外の Codex 実行経路や、ファイルアクセスルールの正本仕様そのものを確認したいときは、対応する実装・仕様ファイルを先に読む。
- prompt 生成の内部ロジックやログ形式の全体定義を知りたいだけなら、このテストではなく対応する oracle 側の仕様断片を読む。

## hash
- 23c5fda6dc970145b638f73ddfbb62660af10be2f97db602f9a4ccc75044cb76

# `test_doctor_cli.py`

## Summary
- doctor コマンドの事前修復と設定生成の外形挙動を検証する統合テスト群。`.cmoc` 周辺の修復、git 状態の保持、linked worktree の扱い、Ollama 連携、`dector` 互換までをまとめて扱う。
- 個別の内部実装ではなく、`doctor` 実行後に残るファイル状態・commit 内容・ignore 状態・サービス設定・モデル取得順序を確認したいときに読む。

## Read this when
- `doctor` / `dector` の CLI 挙動を変える、またはその修復処理を調べたいとき。
- `.gitignore`、`.agents/.gitkeep`、`.cmoc/config.json`、`.cmoc/local`、linked worktree の扱いなど、doctor 実行後のリポジトリ状態を確認したいとき。
- Ollama の managed service とモデル取得の順序・対象がどうなるかを確認したいとき。

## Do not read this when
- doctor 以外の CLI サブコマンドの外形挙動を調べるときは、そちらのテスト群を先に読む。
- Ollama のインストール手順や service 定義そのものの仕様を知りたいだけなら、doctor テストではなく該当する runtime / config 側を読む。
- 内部 helper の細かな実装順や git 操作の逐語的な流れだけを追いたいときは、まず対応する実装ファイルを読む。

## hash
- 0f3cdb2204056fdd5676af62d25bad7649e3577560f56ce362b0901f1e386620

# `test_indexing_cli.py`

## Summary
- `indexing` CLI の外部挙動を固定する回帰テスト群。INDEX.md の生成・更新、preflight、commit、linked worktree、dirty repo、hash 既存判定、壊れた既存エントリーの再生成までを扱う。
- INDEX 更新ワークフローの入出力や境界条件を変える作業で読む。実装内部の分割や汎用 helper の追加より、CLI と indexing_common の観測可能な振る舞いを確認したいときに進む。

## Read this when
- `indexing` サブコマンドの成否条件、commit 対象、preflight の対象 root、既存差分の扱い、linked worktree での更新先を変更するとき。
- INDEX.md の生成物の内容、hash による再生成抑止、壊れた既存エントリーの扱い、empty directory や symlink cycle の扱いを変えるとき。
- `sub_commands.indexing` と `commons.indexing` の境界で、CLI 回帰として確認すべき外部挙動を増減したいとき。

## Do not read this when
- `indexing` 以外の CLI や、git 支援関数そのものの変更だけを扱うとき。
- preflight や commit の共通基盤ではなく、別サブコマンドの routing や出力仕様を変更するとき。
- 純粋な実装整理だけで、INDEX.md の生成・更新・拒否条件に影響しないとき。

## hash
- 96900fca457f8ac6dbf01113b73b79d1c4cb69297bb0c7fb66c39df2b204c73f

# `test_indexing_preflight.py`

## Summary
- `run_codex_exec` と `run_codex_tui` の実行前に indexing preflight が走る条件、順序、worktree 選択、ロック待機、回復用の再実行抑止を検証するテスト群。`commons.runtime_codex_preflight` と `commons.indexing` の呼び出し契約を確認したいときに読む。
- このファイルは、Codex 呼び出し経路ごとの preflight 挙動と、repository lock / file access violation / preflight 無効化の分岐をまとめて確認する入口であり、個別の実装詳細ではなく外部挙動を見たいときに進む。

## Read this when
- Codex 実行直前の indexing 実行有無や順序を確認したいとき。
- linked worktree があるときに、どの root を indexing 対象に選ぶか確認したいとき。
- repository lock 待機や、preflight 無効パラメータ時のスキップ条件を確認したいとき。
- file access violation 後に recovery 用の indexing を追加しない挙動を確認したいとき。

## Do not read this when
- indexing の具体的な更新ロジックそのものを追いたいときは、`commons.indexing` 側を読む。
- Codex 実行や TUI 実行の本体フローを追いたいときは、preflight 呼び出し元の実装を読む。
- repository lock の取得方法や worktree 検出の詳細を知りたいだけなら、このテストではなく対象実装を読む。

## hash
- b9541a16a87bb68b98185065df5b1ec574a05c2da05fd884b13d04c4ed9116d7

# `test_packaged_import.py`

## Summary
- `packaged layout` での import 境界と公開面の検証をまとめたテスト群。`oracle` 配下の正本定義が配布物側で正しく再公開されるか、余計な公開が混入しないかを確認したいときに読む。
- 対象は `acp.builder.review.oracle` の builder、`acp.builder.basic` の canonical 型再公開、`config.cmoc_config` の公開面制約で、個別の実装ロジックや oracle 本文の仕様確認よりも import 契約の確認が主目的。

## Read this when
- packaged layout で `acp.builder.review.oracle` の builder が正しく import できるかを確認したいとき
- 正本の `AgentCallParameter` や `ModelClass` が realization 側で複製されず再公開されているかを確認したいとき
- `config.cmoc_config` の公開面が設定定義だけに絞られているかを確認したいとき
- 配布物として組み立てた tree で import 境界や `__all__` の契約を検証したいとき

## Do not read this when
- oracle の仕様断片そのものを追加・修正したいときは、対応する `oracle/src` 側を見るべきで、このテストは読まなくてよい
- builder のプロンプト内容や schema 本文の仕様を確認したいときは、対応する正本実装や prompt builder 側を直接読むべきで、このテストは主対象ではない
- packaged layout ではなく通常の実行時挙動や CLI 全体の流れを追いたいときは、より上位の実装・テストを読むべきで、このファイルは後回しでよい

## hash
- 392997d67501bad02e59642e8c08a3bcdaff1e1a87aee044e57561d96efa9c5a

# `test_prompt_parts.py`

## Summary
- 標準 prompt parts と complete prompt の Markdown 組み立て結果を検証する realization test。各標準文書 builder が期待する核となる語句・タイトルを描画すること、complete prompt が指定された標準群・file access rule・root placeholder 情報を含めるまたは省くことを外部挙動として確認する。
- prompt builder の標準文書出力、file access mode ごとの read/write rule、review/apply review/index entry/realization/routing standard の注入制御、root token と `<work-root>` placeholder の保持に関する変更時の入口になる。

## Read this when
- 標準 prompt part の文面、タイトル、または render 結果に含まれるべき主要語句を変更する。
- complete prompt が標準文書を含める条件、既定で省く条件、または routing rule を常に含める挙動を変更する。
- file access mode ごとの禁止・許可ルール文面や mode とタイトルの対応を変更する。
- `<repo-root>`、`<work-root>`、`<cmoc-root>`、`<run-root>` などの root token を prompt 内で保持・記録する挙動を変更する。
- index entry standard や review oracle standard など、動的に注入される標準 prompt の回帰をテストで確認したい。

## Do not read this when
- prompt builder の実装責務や標準文書の正本内容そのものを確認したい場合は、対応する実装または oracle 側の標準定義を直接読む。
- CLI コマンド、永続状態、ファイル探索、agent 実行制御など prompt 組み立て以外の挙動を調べている。
- StructDoc や Markdown renderer の汎用仕様を確認したいだけで、complete prompt や標準 prompt parts の期待出力に関心がない。

## hash
- a61448d13fe6b11acc398a8f268160b43e11b800fb149526e056ef20a992fdad

# `test_review_oracle_loop.py`

## Summary
- `cmoc review oracle` の所見列挙・所見マージ・所見検証の周回制御をまとめて確認するテスト群。Codex 呼び出しの受け渡し条件、merge operation の適用条件、再試行時の失敗条件を読む入口にする。

## Read this when
- review oracle の finding loop の順序、打ち切り条件、ダーティフラグ更新を確認したいとき。
- merge operation の kind 契約、target_ids の妥当性、重複 target の扱いを確認したいとき。
- validate / advocate / judge への prompt 伝播や、隔離実行のコンテキストを確認したいとき。
- merge の意味的な不正入力に対する再試行回数や、最終的なエラー終了条件を確認したいとき。

## Do not read this when
- `cmoc review oracle` の仕様そのものだけを知りたいときは、対応する app_spec 側を先に読む。
- Codex CLI 呼び出し規約や Structured Output の保存規則だけを知りたいときは、個別の呼び出し規約側を読む。
- テストの実装詳細ではなく、共通のテスト方針や開発規約を確認したいときは、dev_rule 側を読む。

## hash
- 337660aea5c73e0ac91f3719f0bcf3d477d90f80edd1ff196bb368429cdc6cd8

# `test_review_oracle_report.py`

## Summary
- `cmoc review oracle` のレポート生成と CLI 挙動を検証する統合テスト群。`review oracle` の出力順、集計件数、`--scope` の反映、処理失敗時の error report、`eval-oracle` からの委譲確認を扱う。

## Read this when
- `review oracle` の Markdown レポート本文や frontmatter を変更するとき。
- 所見の採用・不採用の分類、fatal/minor の集計、`<oracle-root>` や symlink の集計ルールを変えるとき。
- `review oracle` の `--scope` やエラー時出力、`eval-oracle` からの委譲経路を変えるとき。

## Do not read this when
- `review oracle` 以外のサブコマンドの一般的な CLI 仕様だけを変えるとき。
- Codex CLI 呼び出しの共通規約や schema 定義そのものだけを変えるとき。
- 個別の oracle 仕様本文を編集したいだけで、レポート生成や CLI 出力の検証を触らないとき。

## hash
- d5e6ae8091d689c498d140cd3645217e43e375c475e8ba4b1408d81619464e1d

# `test_review_oracle_targets.py`

## Summary
- `review oracle` の対象抽出と `finding` からの oracle path 解決の境界を検証するテスト群。`, `session scope` と `full scope` の対象選定、追跡済みだが ignore される oracle file の扱い、AGENTS.md / INDEX.md の除外、symlink の分類基準を確認したいときに読む。
- `review oracle` の CLI 挙動そのものより、対象列挙と path 解決の仕様を確かめる入口として読む。`finding` の Structured Output をどう解釈して review 対象へ落とすか、レビュー結果の選定ロジックを追いたいときに直接進む。

## Read this when
- `review oracle` のレビュー対象がどの oracle file になるべきかを確認したい。
- `finding` に含まれる `oracle_path` を `review` 実行時の基準位置からどう解決するかを確認したい。
- ignore されるが追跡済みの oracle file、symlink、`AGENTS.md`、`INDEX.md` の扱いを確認したい。
- `session` スコープと `full` スコープで対象集合が変わる条件を確認したい。

## Do not read this when
- review 実行の出力整形、レポート本文の文言、Codex 呼び出しの詳細だけを追いたい場合は、より上位の CLI 実装や出力生成側を読む。
- oracle file の総論や開発規則だけを知りたい場合は、このテストではなく参照先の正本仕様断片を読む。
- 対象列挙以外の review サブコマンド全般を追いたい場合は、このファイルではなく `review` 本体の実装を読む。

## hash
- d3d8ad6407f7587debc0e5a25474e42d4bda8f74fcde35d97f6777f55b071790

# `test_review_oracle_worktree.py`

## Summary
- `cmoc review oracle` の worktree 選択と INDEX 統合の振る舞いを確認する統合テスト群。linked worktree の session branch で実行されること、review 用 worktree が分離されること、INDEX 変更が取り込まれること、競合時の解決方針、review 実行中に INDEX 以外の差分が混ざった場合の拒否を扱う。

## Read this when
- `cmoc review oracle` の対象 worktree がどれになるべきかを確認したいとき。
- review 実行時に INDEX.md の生成・マージ・競合解決がどう扱われるかを確認したいとき。
- review 中に未コミット差分や INDEX.md 以外の差分がある場合の拒否条件を確認したいとき。

## Do not read this when
- review oracle の所見列挙・採否判定・レポート本文だけを確認したいときは、review ループや report 側のテストを読む。
- `cmoc review oracle` 以外の一般的な CLI 挙動や別サブコマンドの振る舞いを確認したいとき。
- 対象 oracle の選定そのものだけを確認したいときは、対象抽出側のテストを読む。

## hash
- c51cf53de335391985ea9d46ba1e4e54417e79ea1f34a15d858b0bf44a69dd93

# `test_runtime_cli.py`

## Summary
- CLI 実行時の境界を検証するテスト群。エラー整形、work root 判定、preflight と completion の副作用有無、サブコマンドログの生成条件を確認したいときに読む。

## Read this when
- CLI のエラー表示先やエラーレポート形式を変えるとき。
- work root 判定、pre-log check、doctor preprocess、shell completion の実行順や副作用条件を変えるとき。
- サブコマンドログの生成条件や、`cmoc` 起動 wrapper の位置情報の出し方を変えるとき。

## Do not read this when
- 個別サブコマンドの業務ロジックを変えるだけで、CLI 境界に影響しないとき。
- ログやエラー表示の内部ヘルパー実装だけを調べたいときは、まずそれぞれの実装側を直接読む。
- completion 以外のコマンド実行経路だけを追いたいとき。

## hash
- 58a6c5466689168cadefce448d6adcf7327c5fe41c23b36cec62b8d0d97ae818

# `test_runtime_codex_conflicts.py`

## Summary
- セッション参加の conflict 解決で、Codex の追加書き込み許可がどのパスに付与されるか、また予約済みパスを拒否するかを検証するテスト群。
- 書き込み許可のルート解決、拒否条件、`CmocError` の発生条件を変えるときに読む。

## Read this when
- セッション参加 conflict の解決結果をもとに Codex の書き込み許可を組み立てる処理を変更する。
- Oracle 配下や実行時予約領域のような、追加書き込みを許してはいけないパスの判定を変更する。
- 許可ルートの解決結果や拒否時のエラー条件を確認したい。

## Do not read this when
- 一般的なセッション参加処理や conflict 解決の内部手順だけを変える場合は、まずその実装側を読む。
- 書き込み許可の組み立てではなく、通常の runtime Codex プロファイルや別の権限制御を変える場合はここを読まない。
- 他のサブコマンドの出力形式や設定項目だけを変える場合は対象外。

## hash
- 004b0a573df98b02c1c192ad8e8f61d2f2fbb4f9260a75395f24120487016a67

# `test_runtime_codex_permissions.py`

## Summary
- Codex の実行時ファイルアクセス権限を検証するテスト群。`build_codex_override_args` が読み取り専用・実装書き込み・純 Oracle 読み取り/書き込み・リポジトリ全体書き込みの各モードで、どの path を書き込み可/不可にするかと、`extra_writable_paths` の追加許可条件をどう扱うかを確認する。

## Read this when
- Codex の filesystem 権限オーバーライドの可否を変えたとき。
- `FileAccessMode` ごとの書き込み範囲、`memo` や `.agents`、`.cmoc/local`、`.codex`、`AGENTS.md`、`INDEX.md` の保護条件を確認したいとき。
- 追加書き込み許可 path が、モードごとの許可範囲内かどうかの判定を変えたとき。

## Do not read this when
- ファイルアクセスルールの正本仕様そのものを確認したいときは、対応する Oracle の本文を読む。
- git 追跡状態や ignore 判定の実装詳細を確認したいときは、権限オーバーライド生成側や git 補助の実装を読む。
- 権限ではなく CLI の別モードやプロンプト生成の変更を扱うだけなら、このテストは読まなくてよい。

## hash
- 874e61fd4ce7237fa112495a17795f7d6f2ed7f37939819396ae1e467ed9bd05

# `test_runtime_codex_profile.py`

## Summary
- `codex exec` の model・reasoning effort・sandbox/permission 上書きと、`cmoc managed ollama` の provider 切り替えを検証する統合テスト群。
- ファイルアクセス制限の root/readonly/readwrite 境界、`oracle` と realization の分離、linked worktree での `cmoc/local` 読み取り許可まで含めて確認する。

## Read this when
- Codex CLI へ渡す上書き引数の構成や、`FileAccessMode` ごとのアクセス境界を変えるとき。
- `cmoc managed ollama` を使うモデル選択・provider 設定・web_search 無効化の挙動を確認したいとき。
- linked worktree や extra read root を含むファイルアクセス許可条件、または許可領域外エラーの扱いを変えるとき。

## Do not read this when
- 個別の prompt 文面や file access rule の正本仕様そのものを確認したいときは、対応する oracle 側を読む。
- Codex CLI の一般的な呼び出し規約や cmoc managed ollama のサービス運用方針だけを知りたいときは、対応する oracle doc を直接読む。
- このテストの内部ヘルパー実装だけを追いたいときは、まず本体の実装ファイルを読む。

## hash
- 0848882e10388cbc7c65a0c46a46f0c2d2b68b0449600d6471660ce9c8e0109f

# `test_runtime_config.py`

## Summary
- `CmocConfig` と設定入出力の仕様を検証するテスト群。既定値、JSON 変換時の順序保持、設定ファイル未存在時の案内、型・値検証、復元用数値の保持を確認したいときに読む。

## Read this when
- 設定の既定値や `CmocConfig` の振る舞いを変えたとき。
- 設定の JSON 変換・復元・読み込み失敗時のエラー案内を変えたとき。
- 設定値の型検証や、許可しない値の扱いを確認したいとき。

## Do not read this when
- 設定の実装そのものを追いたいときは、対応する実装側を直接読む。
- 設定以外の runtime 挙動や別機能のテストを探したいとき。
- 設定の入出力形式やエラーメッセージを変更していないとき。

## hash
- 1e5ca12366b3c1a968fda5cf0179a1404f3f54a7ecc3e695bf4bd54ba909d8fc

# `test_runtime_content.py`

## Summary
- `commons.runtime_content.is_binary` の判定が、通常のテキストと NUL 文字を含む内容で分かれることを検証するテスト。

## Read this when
- `runtime_content` のバイナリ判定の境界を確認したいとき。
- NUL 文字を含む入力をバイナリ扱いにする挙動を変更する可能性があるとき。

## Do not read this when
- `is_binary` の内部実装方式や判定アルゴリズムを確認したいだけのとき。
- `commons.runtime_content` 以外の内容判定ロジックを探したいとき。

## hash
- 85b61e7dbf84d03903062b96ba5df65b0c4a595ae9a66aa84d5637e06e5c5f10

# `test_runtime_file_access.py`

## Summary
- FileAccessMode の永続化値と Codex sandbox への変換の対応関係を固定するテスト群。論理的なファイルアクセスモードの追加・改名・値変更、または sandbox 変換の見直しをするならここを読む。

## Read this when
- `FileAccessMode` の列挙値や永続化文字列を変えるとき。
- 論理モードから Codex sandbox mode への変換を追加・変更するとき。
- ファイルアクセス権限の契約が JSON schema や runtime 側と食い違っていないか確認したいとき。

## Do not read this when
- ファイルアクセス以外の runtime 挙動だけを変更するとき。
- prompt 文生成や個別の実行フローだけを調整するとき。
- `FileAccessMode` と sandbox 変換の契約に触れない修正のとき。

## hash
- ab49dc866cba181e7b05dfaf189b683bd1b5cf41a7e8abd242da1afb2b2d679b

# `test_runtime_ollama.py`

## Summary
- `commons.runtime_ollama` のサービス管理・接続確認・モデル準備の挙動を検証するテスト群。`cmoc` が管理する Ollama の再起動条件、systemd ユーザーサービス生成、起動後の疎通確認、モデルのロード確認が中心。

## Read this when
- `commons.runtime_ollama` の修正で、Ollama サービスの修復条件・再起動条件・検証失敗時の例外挙動を確認したいとき。
- `cmoc` 管理下の Ollama を systemd ユーザーサービスとして扱う仕様や、`%h` を使った service file の出力を確認したいとき。
- モデルの事前ロードや GPU 推論確認の判定条件を変えるとき。

## Do not read this when
- Ollama 以外のランタイムや別サブコマンドの仕様を確認したいとき。
- CLI の引数解析、コマンド一覧、設定項目の全体像を知りたいときは、より上位のコマンド定義や仕様文書を読むべきで、このテストは直接の入口ではない。
- サービス管理ではなく、一般的な HTTP クライアントや subprocess ラッパーの共通実装だけを確認したいとき。

## hash
- f62c704b643c0ba9f6bd600f8957917763457eb3c98548114354a16bb27b45b0

# `test_runtime_state.py`

## Summary
- `session` と `apply` の state 形状検証、および branch 名から session id を取り出す境界条件を確認するテスト群。`commons.runtime_state` の state 変換・読込・ branch 解析に不整合がないかを確かめたいときに読む。

## Read this when
- `SessionState` の辞書変換や復元で、`state` や各 payload フィールドの型制約を確認したいとき。
- `branch_session_id` や `apply_branch_session_id` が、余分な区切りや要素不足を不正入力として拒否するか確認したいとき。
- `load_state_for_branch` が壊れた `apply` branch 名を誤って受理しないか確認したいとき。

## Do not read this when
- `SessionState` の永続化形式そのものを変更したいだけなら、実装側の state 定義や読込処理を先に読む。
- branch 命名規則の全体仕様を確認したいだけなら、より上位の session / apply 仕様本文を読む。
- このテストの追加・整理ではなく、runtime state の実装変更だけが目的なら、まず `commons.runtime_state` 側を読む。

## hash
- 78b2a84796519b9b9c6c970910d4ca16803256de9634f28cd98111a7098aba13

# `test_session_cli.py`

## Summary
- `session fork` / `join` / `abandon` の外部挙動をまとめて確認したいときに読む統合テスト。session branch と session state の遷移、linked worktree、state cleanup、dirty worktree 拒否、conflict 解消の境界を一箇所で押さえる。
- この対象は、個別の内部 helper ではなく CLI レベルの回帰を見たいときの入口になる。session の状態遷移や `run_codex_exec` 経由の conflict resolution の観測点を確認したい場合に優先して読む。
- 一方で、`session state` の保存形式や各サブコマンドの仕様そのものを深く追う必要がある場合は、ここよりも対応する oracle doc や oracle src 側を直接読むほうが近い。

## Read this when
- session CLI の回帰テスト全体を追いたいとき
- `fork` / `join` / `abandon` のどれかで branch 遷移や state 更新の期待値を確認したいとき
- linked worktree での session 操作や、preprocess の順序・dirty worktree 拒否・cleanup rollback の観点を見たいとき
- conflict resolution 時の Codex 呼び出し境界や、未解決 path が残る失敗条件を確認したいとき

## Do not read this when
- session の実装方針や内部関数の詳細だけを知りたいときは、対応する oracle src を先に読む
- 個別の仕様文言や責務境界を確認したいだけなら、対応する oracle doc を直接読む
- session 以外の CLI 回帰を見たいときは、この対象ではなく該当サブコマンドのテスト群へ進む

## hash
- f3c69dba698a676cbe742d6b1bbf0967d5593977d92c1416475af0394caf1fc0

# `test_struct_doc_rendering.py`

## Summary
- StructDoc の Markdown renderer が通常テキストとコードブロック内の連続空行をどのように畳むかを検証する単体テスト。renderer の整形互換性、特に不要な空行の圧縮とコードフェンス内の空行保持境界を確認する入口になる。

## Read this when
- StructDoc から Markdown へ変換する処理の空行整形を変更・確認したいとき。
- render_as_markdown の出力に含まれる通常テキストの連続空行、またはコードブロック内の連続空行の期待値を確認したいとき。
- Markdown renderer の分割根拠に対応する realization test を探しているとき。

## Do not read this when
- StructDoc のデータ構造や renderer 実装そのものを確認したいだけのときは、実装側を直接読む。
- Markdown renderer 以外の prompt builder、oracle、CLI 挙動のテストを探しているとき。
- INDEX.md エントリー生成規則やルーティング文書の書き方を確認したいとき。

## hash
- 51580019f3a5f35c894b459980668eec4b098eecee22f1645f571c7c2084f811
