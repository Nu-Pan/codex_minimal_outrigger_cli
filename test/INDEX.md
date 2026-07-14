# `test_acp_builder_parameters.py`

## Summary
- ACP builder の各 parameter builder が、対応する oracle 側の structured output schema と prompt 条件を満たすかを確認するテスト群。apply/review/session/tui/indexing の主要な生成結果と、モジュールの公開面をまとめて検証するため、このテストを読む。

## Read this when
- ACP builder の parameter 生成結果を変更した。
- prompt に埋め込む root 表記や、structured output schema の一致条件を確認したい。
- review/oracle・apply/fork・session/join・tui resolve・indexing の生成物にまたがる互換性を確認したい。

## Do not read this when
- 個別の builder 実装だけを追いたい場合は、対応する `src/acp/builder/...` 側を先に読む。
- oracle 側の正本仕様そのものを確認したい場合は、`oracle/src/oracle/acp_builder/...` 側を読む。
- CLI 全体の入出力や実行フローを追いたいだけなら、この統合テストではなく各サブコマンド周辺を読む。

## hash
- e41e29054eb05095e6cb2dd467f62c95dc60cab965c04be787f521fc3b903fc2

# `test_apply_abandon_cli.py`

## Summary
- `apply abandon` の CLI 振る舞いを検証するテスト群。active apply run の破棄に伴う worktree・branch・state の cleanup、実行中 process の停止順序、破損 state や別セッション混入時の拒否条件、linked worktree 上からの実行可否を確認したいときに読む。

## Read this when
- `apply abandon` の成功時に何を片付けるべきか、どの警告を出しても成功扱いにするか、どの破損状態をエラーにするかを確認したいとき。
- running apply process の停止と git cleanup の順序、pid file の読み取り、stale PID や child process の扱いを確認したいとき。
- apply worktree / linked session worktree / repo root のどこから abandon を実行できるか、どの状態で拒否されるかを確認したいとき。

## Do not read this when
- `apply abandon` 以外の apply コマンドの仕様を知りたいときは、fork や runtime 側の対象を先に読む。
- session 作成や fork の一般仕様だけを知りたいときは、このテスト群より session 系の対象を読む。
- 個別の実装詳細ではなく、CLI の入出力や状態遷移の全体像だけを知りたいときは、より上位の README や対象モジュールの INDEX を先に読む。

## hash
- 7114d6da5666657a42c2c9868ff913eabf66c3840903a71e638ceeb6c14e865a

# `test_apply_fork_cli.py`

## Summary
- `apply fork` CLI の回帰テスト群。セッション fork 後の apply 実行、state と worktree の更新、linked worktree からの開始、doctor preflight、config 読み込み失敗、`.gitignore` の扱い、対象 path 正規化、report 生成順のように、CLI 境界で観測される外部挙動を確認するときに読む。

## Read this when
- `apply fork` のコマンド挙動を変えるとき。
- target 正規化や `.cmoc/local` などの除外境界を変えるとき。
- config 失敗時の開始前停止、state 更新順、report 出力順を確認するとき。
- `.gitignore` や tracked ignored file の扱いを確認するとき。

## Do not read this when
- `apply` の別サブコマンドや session 系の一般仕様だけを変えるとき。
- Codex 実行本体の細部や共通 helper の実装だけを変えるとき。
- CLI 境界ではなく、個別の内部関数の単体挙動だけを確認したいとき。

## hash
- 155dca26d71fdfc0a053ba3d151d36ee77792904a577cec6ef9c1f6566e9ec44

# `test_apply_fork_report_cli.py`

## Summary
- `apply fork` の report 生成、変更要約、再検査、rolling apply の収束条件を CLI から検証するテスト群。`change_summary` と `file_finding_enumeration` の import 可否、report の表示内容、session state 更新、未追跡・削除済み file の扱いをまとめて確認する入口。

## Read this when
- `apply fork` の report 生成や再検査ループの観測結果を変えるとき。
- report に出る result、所見数の推移、変更内容要約、commit message、session state のどれかを直すとき。
- rolling apply fork や change summary の差分抽出条件を確認したいとき。

## Do not read this when
- 所見列挙や適用の個別実装だけを直すなら、対応する実装側のファイルを先に読む。
- CLI の他コマンドや report 以外の apply flow を調べたいだけなら、このテスト群は後回しにする。
- 共通の prompt 断片や schema 定義の正本を確認したいだけなら、oracle 側の定義を読む。

## hash
- 1619b1eb112c0ee77a38e6d8bad7239186617d0e432ec91971d10f7096d23f0f

# `test_apply_join_cli.py`

## Summary
- `apply join` の CLI 挙動を検証するテスト群。apply worktree の後片付け、session state 更新、report 生成、dirty worktree や想定外差分、merge conflict の扱いなど、結合時の外部挙動を確認したいときに読む。

## Read this when
- `apply join` の成功条件や拒否条件を変えるとき。
- worktree 削除、branch 削除、state 更新、report 出力の整合を確認したいとき。
- dirty worktree、想定外差分、rename、symlink、merge conflict の判定や表示を追いたいとき。

## Do not read this when
- `apply fork` 側の生成や分岐条件を確認したいときは、fork 側のテストや実装を先に読む。
- join 以外の session 操作だけを確認したいとき。
- 個別 helper の実装詳細ではなく CLI の入出力だけが目的のときは、このファイルより対応する実装側を先に読む。

## hash
- ad667629064f5a56d12c809d6c0c4a998829eadf38332d7dfbeff6f07b271f0b

# `test_basic_runtime.py`

## Summary
- cmoc の基礎 runtime 境界を横断して検証する回帰テスト群。root 解決、config、エラー表示、subcommand ログ、worktree 操作、file access 判定、Codex sandbox 変換のように、個別機能より前提境界の整合性を確認したいときに読む。
- 各サブコマンド固有の振る舞いより、複数の共通 runtime 契約が一緒に崩れないことを見たい場合の入口にする。共通 fixture と状態解決の文脈が絡むため、分散した個別テストを探す前にここを読む。

## Read this when
- root / work root / run root の解決関係を確認したいとき。
- cmoc config の既定値、JSON 化、入力検証、エラー整形をまとめて追いたいとき。
- CLI の preflight、parse error、subcommand log、doctor 前処理の整合を確認したいとき。
- FileAccessMode ごとの sandbox 変換や許可領域の境界を確認したいとき。
- worktree 作成・削除、branch session id、session state 読み書きの境界を検証したいとき。

## Do not read this when
- 単一サブコマンドの業務ロジックだけを追いたいときは、そのサブコマンド専用のテストを先に読む。
- runtime 境界ではなく、個別の prompt 生成や oracle 側の仕様断片を確認したいときは別の領域を読む。
- 基本的なファイル単体のユーティリティ挙動だけを見たいときは、より小さい helper のテストを直接読む。

## hash
- 100ff0e0dafa1fc0b03c254521df88cc22661f803e9d281efcf55536115172a1

# `test_cli_tui.py`

## Summary
- TUI 起動の前処理に関する外部挙動を確認したいときに読む。`code` 呼び出しで作る元プロンプト、解決済みパラメータの組み立て、`codex` 起動前後のログ出力と作業ツリー選択の整合を扱う。
- 特に、`tui` サブコマンドの動作、`repo_write` などの file access mode 解決、linked worktree で `.cmoc` ログや schema の保存先がどう分かれるかを確認するときの入口になる。

## Read this when
- TUI 起動前の CLI 前処理を変更する。
- `tui` のパラメータ解決、プロンプト整形、ログ保存、linked worktree での保存先判定を確認したい。
- `code` で編集した元プロンプトが最終プロンプトにどう反映されるかを確認したい。

## Do not read this when
- TUI 以外のサブコマンドだけを変更する。
- ACP の一般的な型定義や他のコマンドの出力仕様だけを確認したい。
- `.cmoc` の別用途のログ整理だけを見たい。

## hash
- 81ca52fa1e8ec249ef6d08101f24846b0add6849a2ae440f65f69308ffa3a6ae

# `test_codex_runtime_errors.py`

## Summary
- Codex 実行経路で `codex` CLI が存在しないときのエラー扱いを確認するテスト。`exec` と `tui` の両経路に同じ失敗条件が通るかを見たいときに読む。

## Read this when
- `commons.runtime_codex` の実行前提として、`codex` コマンド未検出時の例外種別とメッセージを確認したい。
- `run_codex_exec` と `run_codex_tui` の両方で、外部 CLI 不在時の共通エラー処理を追加・修正したい。
- Codex 起動まわりの失敗ケースをまとめて検証するテストを探している。

## Do not read this when
- `codex` CLI が見つかった後の実行制御、入出力、再試行、タイムアウトを調べたい。
- `CmocConfig` やテスト支援関数 `_support` の実装を追いたい。
- Codex 実行経路以外のエラーや、別コマンドのテストを探している。

## hash
- 5dae1c9ec4e9b281fbac99de9d607dee501ce21c85439cc1d602e8264420a77d

# `test_codex_runtime_exec.py`

## Summary
- `run_codex_exec` を使った Codex CLI 実行経路の結合テスト群で、argv の上書き、作業ディレクトリ、プロンプト保存、Structured Output、sandbox 権限、cmoc managed ollama 連携を検証する。
- Real Codex CLI を使うケースと Fake Codex CLI を使うケースの両方を含み、`cmoc` が責任を持つ実行構築と保存先の挙動に絞って確認する。

## Read this when
- Codex CLI 呼び出しの組み立て結果を検証したいとき。
- `--model`、`--config`、`--sandbox`、`--output-schema`、`--output-last-message` などの付与条件を確かめたいとき。
- workspace-write と pure read の権限制御、`cwd` 決定、`.agents` を writable roots に含めない制約を確認したいとき。
- schema ファイルの保存先、プロンプトログ、出力ファイルの保存先など、`run_codex_exec` が作る実行アーティファクトを確認したいとき。
- cmoc managed ollama を provider とする Real Codex CLI 経路を、実回答品質ではなく接続・設定・保存の観点で確認したいとき。

## Do not read this when
- Codex CLI 自体や外部 provider の応答品質を検証したいとき。
- `cmoc` の他のサブコマンドや一般的な prompt 生成規則を確認したいとき。
- `run_codex_exec` 以外の subprocess 実行や retry 専用の制御を確認したいとき。
- 個別の oracle 仕様断片そのものを読みたいだけのとき。

## hash
- 17ee2a1d7c74f3654b91746cc2ee0267c2a186ad0f3c3c9f79efeb49815548c2

# `test_codex_runtime_home.py`

## Summary
- `test/test_codex_runtime_home.py` は `run_codex_exec` の Codex home 解決と起動前検証を確認する回帰テストの入口です。`CODEX_HOME` の未設定・相対値・絶対値の扱い、`auth.json` の有無、CLI を呼ぶ前に失敗する条件をまとめて扱います。

## Read this when
- `CODEX_HOME` の解釈や、そこから決まる Codex home の検証条件を変えるとき。
- Codex CLI 起動前に止めるべき条件や、その利用者向けエラーを確認したいとき。
- `run_codex_exec` の home 解決に関する回帰テストを追加・更新したいとき。

## Do not read this when
- Codex subprocess の argv 構築や prompt 入力の扱いだけを確認したいときは、`run_codex_exec` 本体側を読む。
- 認証情報ファイル以外の Codex 実行フローを追いたいときは、このテストより実装側のモジュールを直接読む。
- CLI 起動後の出力解析や完了処理を見たいときは、このテストは対象外。

## hash
- 2cd44e3b41a82e26e9500c59afe4938ba824e16ae3f7310b071f8d05117354f3

# `test_codex_runtime_quota_retry.py`

## Summary
- `test/test_codex_runtime_quota_retry.py` は、Codex 実行で quota 超過後に probe を挟んで resume へ戻る制御と、その失敗分岐をまとめて確認する回帰テスト群。`run_codex_exec` の retry 状態機械、probe 用パラメータ生成、resume token の復元、call log と subcommand log の整合、同時実行時の単一代表 probe を確認したいときに読む。
- 同じ quota retry 経路の外部挙動を一連の fake Codex 呼び出し列として追う必要があるため、関連するサブケースもこのファイルに集約している。probe 生成だけを見たい場合は、実装側の `oracle/src/oracle/acp_builder` や `oracle/src/oracle/prompt_builder` の該当箇所を直接読む。

## Read this when
- Codex 実行が quota exceeded の後に probe と resume をどう切り替えるかを確認したいとき。
- resume token を JSONL ログから復元する処理の挙動を確認したいとき。
- quota retry の成功・失敗・上限到達・並行実行の制御をまとめて回帰確認したいとき。

## Do not read this when
- 通常の Codex 実行や quota と無関係な subprocess 挙動だけを見たいとき。
- probe パラメータの組み立て仕様そのものを読みたいときは、対応する oracle 側の実装断片を優先して読む。
- retry 以外の CLI 入口や TUI 挙動を確認したいときは、別の test ファイルを読む。

## hash
- 716ed0a98768e5d7f68a422a5148dc03c1f5610a6528f90d753f15b925645443

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 呼び出しの再試行と、そのときに記録されるログや返却値を確認したいときに読む。schema 検証失敗、Structured Output の取得失敗、capacity/quota 系の失敗からの再試行、および失敗判定が stdout JSONL に限定されることを扱う。

## Read this when
- `run_codex_exec` の retry 条件や retry 後の出力整合性を変える前に読む。
- codex 呼び出しのイベントログに記録される status・returncode・error・call_log_path の対応を確認したいときに読む。
- capacity retry 後も agent diff や外部副作用が保持されるべきかを確かめたいときに読む。

## Do not read this when
- Codex 実行前の設定生成やプロファイル選択だけを追いたいときは、より上流の runtime / preflight 側を読む。
- CLI の引数解釈やサブコマンド分岐だけを確認したいときは、このテストではなく該当するコマンド実装とそのテストを読む。
- stdout JSONL 以外の一般的な subprocess エラー処理だけを見たいときは、codex 実行全体の別テストを読む。

## hash
- c74ba3bc88dc456c29d55c8f0eb211d5152226245193afb138ef988d829c1244

# `test_codex_runtime_subprocess.py`

## Summary
- `commons.runtime_codex_profile` の subprocess ラッパーが、apply の追跡情報を継承せずに起動されることと、追跡付き起動が専用のプロセスグループと tracking file を維持することを確認するテスト。subprocess 起動時の環境継承、プロセスグループ、追跡ファイルの更新境界を見たいときに読む。

## Read this when
- subprocess 実行まわりの環境変数継承やプロセスグループの扱いを変えるとき
- apply 追跡情報が通常起動に漏れないことを確認したいとき
- 追跡付き起動で tracking file の扱いを保証するテストを追加・修正するとき

## Do not read this when
- CLI 全体の引数解析やサブコマンド設計を見たいとき
- プロセス実行の共通実装そのものを把握したいだけで、外部挙動の確認は不要なとき
- apply 以外の永続状態や別の subprocess ヘルパーを調べたいとき

## hash
- d9f96358767fbb5d265ebd4e8c302ad0f070f1e1765812f32ce388205dabba8d

# `test_codex_runtime_tui.py`

## Summary
- `codex tui` 実行時の入出力・権限判定・呼び出しログを確認するテスト群。`run_codex_tui` の開始前検証、プロンプト読み取り、作業ツリー/リンク先の扱い、終了コードと記録の整合性を読む入口。

## Read this when
- `run_codex_tui` の実行前に、追加の読み取り対象が許可されるかを確認したいとき。
- `codex tui` に渡すプロンプトや作業ディレクトリの扱い、実際の `codex` 呼び出し引数を確認したいとき。
- 成功時・失敗時にサブコマンドログや呼び出し記録へ何が残るかを確認したいとき。

## Do not read this when
- `codex tui` の内部実装方針そのものを直したいだけなら、対応する実装側の本文を先に読むべきで、このテストだけを起点にしない。
- 汎用的なサブコマンドログや設定周りの変更をしたいだけなら、より直接の実装・設定の本文を読むべきで、このテストは後回しでよい。

## hash
- e053a9c36b4b523a8b76171a92045d70417f878fc355423407dda1dc9ae948e2

# `test_doctor_cli.py`

## Summary
- `doctor` サブコマンドの修復処理を検証するテスト群。`.gitignore` と `.agents` の修復、既存 Git 状態の保持、linked worktree での対象選択、cmoc 管理 Ollama の起動とモデル取得までを確認したいときに読む。

## Read this when
- `doctor` 実行時に repo の修復 commit と作業ツリーの復元がどう両立するかを確認したいとき。
- .cmoc/config.json から cmoc 管理 Ollama の起動やモデル取得がどう導かれるか、また linked worktree で main worktree 側設定を使うかを確認したいとき。

## Do not read this when
- 他のサブコマンドの引数解釈や出力だけを確認したいとき。
- .gitignore 修復や worktree 共有 index の扱いではなく、設定ファイルの定義そのものや Ollama 実装の詳細を追いたいとき。

## hash
- 3fae817c71780a30475bfb2beebcc9cec253f70d0123ff57b04146565ff86062

# `test_indexing_cli.py`

## Summary
- `cmoc indexing` の `INDEX.md` 生成・更新と、衝突解消を含む routing 更新の外部挙動を確認する回帰用エントリ。

## Read this when
- `cmoc indexing` の実行条件、更新結果、コミット有無を確認したい。
- `INDEX.md` の自動生成・再生成・差分反映の挙動を変える。
- インデクシングに伴う conflict 解決や linked worktree の扱いを確認したい。

## Do not read this when
- 単に個別の実装ヘルパや内部データ構造を追いたいだけなら、より直接の実装側を読む。
- 手書きの `INDEX.md` 文面を考えるだけで、自動更新や衝突解決の挙動が関係しないなら読む対象ではない。

## hash
- fcd714cf26d0fea5a9b0291ed05130022e89fc81caee999060eaa8665a1418b4

# `test_indexing_preflight.py`

## Summary
- `commons.indexing` による indexing preflight が、Codex 呼び出しの前に実行されることと、その実行順・作業対象・ロック待ちの挙動を検証するテスト群。`run_codex_exec` / `run_codex_tui` の事前処理と、ワークツリーごとの index 更新がずれないかを確認したいときに読む。
- `AgentCallParameter` の設定で indexing preflight を明示的に無効化した場合に、通常経路と連鎖的な回復経路の両方で preflight がスキップされることを検証する。preflight の有効/無効判定を変える実装や、再帰的な実行制御を触るときに読む。
- file access 違反などの失敗処理が indexing preflight を再度誘発しないことを検証する。エラー回復時の再実行制御や、Codex 実行前後の副作用が増えないかを確認したいときに読む。

## Read this when
- Codex 実行の前処理として index 更新を入れる、外す、または順序を変える実装を変更する。
- ワークツリー・cwd・root のどれを index 更新対象にするか、またはロックを待つかどうかを変更する。
- preflight の無効化フラグ、再入防止、失敗時の再実行経路を変更する。

## Do not read this when
- indexing preflight ではなく、Codex 本体の出力形式やプロンプト内容だけを変える。
- CLI 引数の追加や一般的なサブコマンド分岐だけを変更し、事前 index 更新の有無に触れない。
- `INDEX.md` の生成内容そのものだけを変え、preflight の実行条件や制御フローに触れない。

## hash
- 53add1f54659fea880475e18a941754e100865991782abe1acb7cc4bc800827d

# `test_packaged_import.py`

## Summary
- `oracle` と `src` の packaged layout を前提にした import 境界の回帰確認に使う。`pyproject.toml` の package 配置と、`acp.builder.review.oracle` および `acp.builder.basic` と `config.cmoc_config` が packaged layout でも正しい正本を参照しているかを確かめる。

## Read this when
- packaged layout 上で `acp.builder.review.oracle` のビルド経路と structured output schema の生成を確認したいとき。
- `acp.builder.basic` が `oracle` 側の正本定義を再exportしているか、`config.cmoc_config` が設定定義だけを公開しているかを確認したいとき。
- 配布形態を変えたときに import 解決や公開 API の境界が崩れていないかを回帰検証したいとき。

## Do not read this when
- 通常の機能仕様や各 builder の詳細実装を読みたいとき。
- `INDEX.md` の案内やパッケージ配置そのものを変更したいだけで、この import 回帰テストの内容確認が不要なとき。
- 個別の schema 内容や prompt 文面の詳細を追いたいときは、関連する builder 本体や oracle 側の定義を直接読むべきで、このテストは後回しでよい。

## hash
- ed59fc9ad74514656ac722e4f60386946e3868ea9284ecd7656a4bc61d4d6131

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

# `test_runtime_ollama.py`

## Summary
- Ollama 実行時の service 検証と model 読み込みの振る舞いを固定するテスト群。`commons.runtime_ollama` の待機条件、listener 判定、HTTP status 判定、model load の再試行条件を確認したいときに読む。

## Read this when
- managed Ollama の service が期待どおりに見つからない場合の失敗条件を確認したいとき。
- listener が service 本体由来かどうかの判定条件を変える前に、現行の境界を確認したいとき。
- model が利用可能になるまでの `show` / `pull` / 再 `show` の流れや再試行条件を確認したいとき。

## Do not read this when
- Ollama service の実装や起動処理そのものを変えたいときは、対応する runtime 実装を読む。
- 利用者向けエラーレポートの整形だけを確認したいときは、エラー整形側を読む。
- 単なる pytest の共通設定やテスト収集の仕組みを確認したいときは、この対象ではなくテスト基盤側を読む。

## hash
- 90d5c7b3501be284473425dc316ee0a0afc1386fcfadb857cb621fbda4a1bb7b

# `test_session_cli.py`

## Summary
- `session` サブコマンドの CLI 外部挙動をまとめて回帰確認するテスト群の入口です。fork・join・abandon をまたぐ session branch と session state のライフサイクル、linked worktree での挙動、preprocess 順序、cleanup 失敗時の rollback、join 時の conflict 解消と残差検査までを、この 1 本で追うときに読む。
- 個別の実装分割や内部 helper の責務ではなく、session CLI として利用者から見える成功・失敗・警告・状態遷移の契約を確認したいときに優先して読む。

## Read this when
- `cmoc session fork` / `join` / `abandon` の外部挙動を横断して確認・変更したいとき。
- session branch と session state の生成・更新・削除、linked worktree でのブランチ解決、dirty worktree 拒否、cleanup 失敗時の rollback をまとめて追いたいとき。
- join の conflict 解消後に、未解決差分や conflict marker の残存をどう扱うかを確認したいとき。

## Do not read this when
- session の個別実装だけを見たいときは、対応する `fork` / `join` / `abandon` の実装本文を直接読む。
- CLI ではなく共通の git / runner / doctor 補助の契約を見たいときは、`test` 配下の共通 support を読む。
- session 以外のサブコマンドの回帰確認をしたいときは、このファイルではなく該当領域の test entry を読む。

## hash
- 9150f882801dfe3e91a2069f3b02238d382584c3fdf76df4bb36302d10f18683

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
