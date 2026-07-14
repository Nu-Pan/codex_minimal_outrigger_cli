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
- Codex 実行系のテストで使う最小限の共通補助をまとめる。偽の結果オブジェクト、`CODEX_HOME` のテスト用初期化、Subprocess 引数の抽出、設定差分の展開、書き込み許可の判定補助、実行前の Ollama 前処理の差し替えがここに集約されている。
- 個別の実装や本体ロジックではなく、複数のテストから共通利用される前処理・検証用の足場が必要なときに読む。特に、Codex 実行ラッパーの argv 構築や権限オーバーライドのアサーションを確認したい場合が入口になる。

## Read this when
- Codex 実行ラッパーのテストで、偽の CLI 応答や固定された実行前提を用意したいとき。
- Subprocess に渡した引数から、単一値フラグや重複設定の実効値を検証したいとき。
- 権限オーバーライドから書き込み可否や明示許可の有無を判定する共通ロジックが必要なとき。
- Ollama の共有前処理をテスト対象から外し、argv 構築だけに集中したいとき。

## Do not read this when
- Codex 本体の実装仕様や権限モデルそのものを確認したいとき。まず対応する仕様断片や実装側を読むべきで、この補助ファイルは読解の入口ではない。
- 個別のテストケース固有の入力値や期待値だけを確認したいとき。ここには汎用の足場しか置かれていない。
- 実行時のビジネスロジックやエラー処理の詳細を追いたいとき。これはテスト支援用であり、機能本体の説明にはならない。

## hash
- eb7c1a1c759496d83842d29b42c16a30939d66252f2d43c5a9786a447d52e032

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
- `acp.builder.apply.fork` 系の parameter 生成と、その prompt・schema 参照・root 取り扱い・拒否条件を検証するテスト群を案内する。apply fork の各 builder が正本 schema と標準文面をどう組み立てるか、相対 path の扱いを確かめたいときに読む。

## Read this when
- apply fork の builder 生成結果に含まれる prompt、`structured_output_schema_path`、`model_class`、`reasoning_effort` を確認したい。
- packaged layout での import 契約や、`<repo-root>` と `<work-root>` の使い分けを検証したい。
- root token のない相対 target path を拒否する条件や、finding application / file finding enumeration / change summary の正本 schema 参照を確認したい。

## Do not read this when
- apply fork builder の実装そのものを追いたい場合は、対応する `src/acp/builder/apply/fork/` 側を読む。
- 正本 schema の内容そのものを確認したい場合は、`oracle/src/oracle/acp_builder/apply/fork/` 側を読む。
- apply fork 以外の ACP builder の prompt 構成や schema 参照を探している場合は、このテストではなく該当サブコマンドのテストを読む。

## hash
- 861db2f4835dd0bb7e8df68a55e80b68e1ab2974a87e413e5287b474c41328c7

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
- `test/test_acp_builder_review_oracle_parameters.py` は、review oracle の parameter 生成と schema 互換性をまとめて検証するテスト群です。`acp.builder.review.oracle` の各 builder が返すモデル設定、structured output schema、公開モジュールの export 範囲、prompt 中の `<oracle-root>` / `<oracle-path>` の扱いを確認したいときに読む対象です。

## Read this when
- `acp.builder.review.oracle` の parameter 生成仕様を変更するとき
- review oracle の structured output schema を正本側と突き合わせたいとき
- compatibility 用の薄い公開モジュールの export 範囲や不要な内部公開を確認したいとき
- prompt に埋め込まれる oracle path の表記や、symlink・動的文字列の保持を変える可能性があるとき

## Do not read this when
- review oracle の実装本体を追いたいだけなら、対応する `src/acp/builder/review/oracle/` 側を先に読むべきです
- review oracle 以外の ACP builder や他サブコマンドのテストを探しているなら、この対象ではなく該当領域の test entry を読むべきです
- schema の生成元や正本定義そのものを確認したいだけなら、`oracle/src/oracle/acp_builder/review/oracle/` 側を読むべきです

## hash
- 025353a96b5bd6ae300299bbd7379874cdf604a0d35535bfb006ef6d310cba12

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
- `test/test_apply_abandon_cli.py` は、`apply abandon` の外部挙動を確認する入口である。`worktree`・`branch`・`state` の cleanup、カレント位置の扱い、実行中 process の停止結果を、CLI が返す成功・警告・失敗として検証する内容に限って読む。低レベルな process helper の契約は別テストに分離されている。

## Read this when
- `apply abandon` の CLI 応答や終了コードを変えるとき。
- `worktree` 削除、branch 削除、state 更新の整合を確認するとき。
- CLI をどの作業ディレクトリから呼んでも同じ cleanup になるかを確認するとき。
- 実行中 apply process の停止と、その失敗・警告の扱いを確認するとき。

## Do not read this when
- `apply fork` の生成処理や findings 変換を変えるだけなら、まず別の apply fork 系テストを読む。
- process helper 自体の引数契約や停止ロジックだけを確認したいなら、この CLI テストではなく低レベル helper 側のテストを読む。
- `apply abandon` 以外の session コマンドや一般的な git 補助を確認したいだけなら、このファイルは読まない。

## hash
- 8d8d60f6f4813738816dec47dae7e37c784073dfeb29c21be85dc5db50527cd3

# `test_apply_fork_cli.py`

## Summary
- `apply fork` の CLI 回帰テスト群を案内する。セッション作成後の apply 実行、state/worktree/branch の更新、設定欠落や config 読み込み失敗の停止条件、.gitignore と .cmoc/local の扱い、report 生成前の state 更新を確認したいときに読む。
- 同じ apply fork でも、target 正規化だけを見たい場合は別のテストへ進む。ここは CLI ライフサイクル、リポジトリ fixtures、git 状態、apply 実行順の検証をまとめて持つため、周辺の実装挙動を追う入口として使う。

## Read this when
- `apply fork` のエンドツーエンド挙動を確認したい。
- session branch から apply run を開始し、完了時に state と worktree がどう更新されるかを確認したい。
- 設定欠落・config 読み込み失敗・競合再読込・.gitignore 反映のような lifecycle 回帰を追いたい。

## Do not read this when
- target path の正規化だけを確認したい。
- CLI 本体の実装や helper の分割方針だけを追いたい。
- report 本文の仕様や apply 対象列挙の細部だけを見たい場合は、より直接の実装・仕様ファイルを読む。

## hash
- 85425e2b10d09dd548e33ef58972fa5ddc5fde7cc390ace796ed259b3d4a45a7

# `test_apply_fork_report_cli.py`

## Summary
- `apply fork` の CLI から、レポート生成、収束判定、再検査、rolling 実行、session state 更新までの制御を確認するための回帰テスト群。`apply fork` の report 文面や終了コード、対象 file の再調査条件を変えるときに読む。
- `apply fork` の report 形式や変更要約の算出、未追跡 file や削除 file の扱いを確認したいときの入口。内部 helper の切り分けそのものより、CLI から見える出力と状態遷移を優先して読む。

## Read this when
- `apply fork` の report 出力、front matter、結果ラベル、終了コード、所見数の推移表示を変える。
- 所見の再列挙条件、変更後の再調査、収束と未収束の境界、error への遷移、rolling 実行の対象決定を確認したい。
- 変更要約が commit 前後の差分や未追跡 file、削除済み tracked file をどう扱うかを確認したい。
- `apply fork` 後に session state に保存される値や、report に反映する branch / worktree / commit の対応を確認したい。

## Do not read this when
- `apply fork` の CLI 表示や制御ではなく、変更要約の低レベル生成だけを追いたい場合は、`fork_report` 側の実装を先に読む。
- apply 系の別サブコマンドや、`session fork` の生成処理だけを見たい場合は、この test ではなく各コマンド本体を読む。
- report の見た目ではなく、oracle 側の規範文や用語定義を確認したいだけなら、対応する oracle doc/src を読む。

## hash
- 782f83b416ac144630dca340fd774b76785f594cb1bfcfe01002a2233242a7c7

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
- `apply join` の CLI 挙動を検証するテスト群。apply worktree の結合成功、clean-up、state 更新、report 生成、cwd が apply worktree のときの扱い、linked session worktree からの join を読む入口にする。
- 同じ join 操作の境界条件として、stale branch、別 session 由来 branch、lock 後の state 再読込、error process の停止、dirty worktree、想定外差分、merge conflict、force 解消、許可される差分分類を一箇所で確認する。
- `apply` 側の差分分類と `session` 側の差分分類の境界、`INDEX.md` 以外の conflict の扱い、realization file かどうかの判定を確認したいときに読む。

## Read this when
- `apply join` の成功条件と拒否条件、cleanup と state/report の更新を確認したいとき。
- `apply` と `session` のどちら側の差分として扱うか、また force で戻す対象を確認したいとき。
- dirty worktree、stale apply branch、別 session の branch、merge conflict、lock 中の state 変化などの境界条件をまとめて追いたいとき。

## Do not read this when
- `apply fork` の作成手順や所見生成の詳細だけを見たいときは、join テストではなく apply fork 側を読む。
- 差分分類の汎用ルールだけを見たいときは、このテスト群より差分分類の正本や補助仕様を先に読む。
- `INDEX.md` の内容や別コマンドの出力仕様だけを確認したいときは、この join テスト群は直接読まなくてよい。

## hash
- b20e2dd189be6c40287194028d05698ce162752cafdd7e98740c8b86f3915c0a

# `test_basic_runtime.py`

## Summary
- `basic.path_model` と `cmoc_runtime` の境界条件を検証するテスト群。`<cmoc-root>` / `<run-root>` の解決、linked worktree の扱い、`pushd` の排他性、run worktree の作成・削除時の拒否条件を確認したいときに読む。
- `_git_support` を使うテスト補助も含むが、目的は Git 操作そのものではなく、runtime が managed worktree 以外を誤って受け付けないことの検証にある。

## Read this when
- root/worktree 変換や placeholder 解決の仕様を変更したいとき.
- run worktree の作成・削除条件を見直したいとき.
- `pushd` の同時実行時の cwd 競合や、linked worktree の区別を確認したいとき.

## Do not read this when
- `basic.path_model` の正本仕様を確認したいだけなら `<work-root>/oracle/src/oracle/other/path_model.py` を先に読む.
- Git テスト補助の実装詳細だけが目的ならこのテストより `_git_support` 側を直接読む。

## hash
- 0d3af364956d565500ebbf07e553fdc50534d8c50adf17468eb320cd27a83799

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
- Codex CLI 実行時の `run_codex_exec` と override 生成を検証する統合テスト群。実 CLI 呼び出し、`cmoc` 管理 Ollama 連携、`CODEX_HOME` への設定ファイル不作成、権限制御付き実行の挙動を確認したいときに読む。

## Read this when
- `commons.runtime_codex.run_codex_exec` や `commons.runtime_codex_profile.prepare_codex_override_args` の外部挙動を変えるとき
- local SLM / `cmoc` managed ollama の provider 切り替え、preflight 呼び出し、Codex CLI への override 伝播を確認したいとき
- `CODEX_HOME` 配下に永続設定を作らないことや、repo-write 実行時の書き込み範囲を確認したいとき

## Do not read this when
- `run_codex_exec` の内部実装詳細だけを追いたいときは、対応する実装ファイルを直接読むべき
- Codex 実行以外の一般的な runtime doctor 振る舞いだけを確認したいときは、関連する doctest や doctor 側のテストを優先して読むべき
- このファイルは実行統合の検証が主目的なので、CLI の一般仕様や設定体系の全体像を知りたいだけなら別の仕様文書を読むべき

## hash
- 6b741d7a2f9f486b91be04baaf161ba88ac6fd59e4e8cbb4253e8011277fae34

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
- Codex 実行時の quota 枯渇後に、代表 probe を一度だけ挟んで resume/retry へ進む制御を確認したいときに読む。`Codex exec` の外部挙動、resume token の復元、quota probe の呼び出し列、並行待機の集約が主題。
- quota 待機中の stderr/stdout、call log、subcommand log、`CODEX_HOME` と `cwd` の解決、invalid JSONL や probe 失敗の伝播を追う変更で読む。実装内部の分岐整理や一般的な CLI 設計の議論だけなら他の本文を優先する。

## Read this when
- quota exceeded 後に probe を挟んで再実行する挙動を変える、または回帰確認したいとき。
- resume token の保存・復元、probe の失敗判定、並行待機の集約、`CODEX_HOME`/`cwd` の解決条件を確認したいとき。
- `codex exec` のログ出力や quota 復帰の観測点を合わせて読みたいとき。

## Do not read this when
- quota retry 以外の `codex exec` 一般の仕様だけを追いたいとき。
- probe 以外の builder や別サブコマンドの仕様変更を確認したいとき。
- 実装の内部 helper 分割やリファクタリングだけが目的で、quota 待機の外部挙動を変えないとき。

## hash
- 2f90753aa11a1011f5a064273d8b6a91b55bfb3a981f6320274408e4d93f14fd

# `test_codex_runtime_retry.py`

## Summary
- `run_codex_exec` の再試行・失敗ログ・中断挙動を、実際の subprocess 呼び出し回数とサブコマンドログの両方から確認するテスト群。Structured Output の検証失敗、capacity retry、JSONL error、KeyboardInterrupt、retry 上限到達後の失敗をまとめて扱う。
- この対象を読むのは、Codex 呼び出しの retry 判定や失敗時の外部挙動、call log と event log の整合性、差分保持の確認が必要なとき。実装内部の helper 分割より、最終結果・再試行回数・記録内容を変えないことが重要なときに進む。
- 同じ retry 状態機械でも、出力 schema 以外の一般的な CLI 挙動や別のログ領域を確認したいだけならここは優先しない。構造化出力を伴わない単発成功例や、別サブコマンドのログ仕様を知りたいだけのときも直接の読む先ではない。

## Read this when
- Codex 実行の retry 条件と停止条件を確認したいとき
- call log, stdout log, prompt log, subcommand event の対応関係を追いたいとき
- Structured Output の再試行と capacity retry が同じ実行経路でどう分岐するかを見たいとき
- 中断時に例外を伝播しつつログを残すかを確認したいとき
- retry を挟んだ後も agent diff が保持されるかを確認したいとき

## Do not read this when
- 再試行とは無関係な通常の Codex 実行結果だけを見たいとき
- 別サブコマンドの入出力やログ仕様を調べたいとき
- 内部 helper の実装構造だけを確認したいとき
- call log ではなく別の永続状態や設定ファイルの仕様を読みたいとき

## hash
- 455131d89ee3b66e9095992942650807987ef43a7bb49cd1afcca757df317708

# `test_codex_runtime_subprocess.py`

## Summary
- `commons.runtime_codex_profile` の subprocess 実行まわりを、apply の中断・後始末要件に合わせて検証するテスト。専用プロセスグループの記録、`KeyboardInterrupt` 時の tracking 維持、外部継承した tracking 環境の無視を確認する。

## Read this when
- Codex subprocess の起動条件や tracking ファイルの更新条件を変えるとき。
- apply の abandon/cleanup に関わるプロセス管理や環境変数の扱いを確認したいとき。
- `run_codex_subprocess` / `run_tracked_codex_subprocess` の振る舞いを追加・変更するとき。

## Do not read this when
- CLI 全体の引数解釈やサブコマンド分岐を見たいだけのとき。
- apply 以外の subprocess 利用箇所の一般的な実装を追いたいとき。
- tracking ファイルを使わない通常の Codex 実行経路だけを確認したいとき。

## hash
- 9aad11766f104007dc39c6565f7f234f1a61c6dc280e9b95b5e22962de1ec3b8

# `test_codex_runtime_tui.py`

## Summary
- TUI 経由で `codex` を起動する runtime の振る舞いを検証するテスト群で、追加読み取りパスの境界、prompt の読み方、linked worktree での権限上書き、call log とサブコマンドイベント、CLI 不在や非 0 終了時の失敗処理をまとめて見る入口です。

## Read this when
- TUI 実行まわりの回帰を直したり、`codex` 起動前後のログ・エラー・権限設定の扱いを確認したいとき。
- 追加読み取りパスの許可判定、完成済み prompt の読み込み、linked worktree での実行差分を確認したいとき。
- TUI 呼び出しの call log 生成やサブコマンドイベントの記録仕様を確認したいとき。

## Do not read this when
- prompt 文字列の組み立て仕様そのものを見たいだけなら、関連する prompt builder 側の oracle を先に読むべきです。
- ファイルアクセス境界の正本仕様だけを確認したいなら、TUI テストよりアクセスルールの oracle を直接読むべきです。
- 一般的なサブコマンド実行基盤や他の runtime の挙動を追いたいだけなら、このテストファイルではなく対応する各 runtime の oracle を読むべきです。

## hash
- edaaac5077072f2e53a7e1cf9b43994594b976e10bc561c7b7eb00e8be876d75

# `test_doctor_cli.py`

## Summary
- `doctor preprocess` の共有 lifecycle を、CLI 経由と直接呼び出しの両方から外部挙動で確認する統合テスト群。`.cmoc/local`、`.agents`、config、managed Ollama、Git index の修復と保持を一続きで見る必要があるときに読む。
- `make_repo`、linked worktree、共有 doctor lock、Ollama 副作用、pre-existing staged changes や rename の保持をまたいだ挙動を確認したい場合の入口。個別の単体テストではなく、doctor preprocess 全体の契約を追うために読む。

## Read this when
- `doctor` / `dector` の外部挙動が変わったかを確認したいとき。
- repository/worktree をまたぐ修復、共有 lock、`.cmoc/local` の扱い、`.agents` の再生成、config 追跡、managed Ollama の維持を同時に確認したいとき。
- Git index 上の staged 変更、unstaged hunk、rename、既存 `.cmoc/local` 追跡状態の保持を含めて doctor preprocess の影響範囲を見たいとき。

## Do not read this when
- `doctor preprocess` の内部実装や helper 分割だけを確認したいときは、対応する realization implementation 側を読む。
- Ollama の単体仕様や config の単体仕様だけを確認したいときは、専用の oracle file を読む。
- Git 操作の細部や fixture の共通化方針だけを知りたいときは、この統合テストではなく、より直接の実装・補助ファイルを読む。

## hash
- 8dec0e68f2d6d94b2f4958a0cb519171dd68f8a3ce2059503082104458f3e5ca

# `test_indexing_cli.py`

## Summary
- `cmoc indexing` の CLI 挙動を検証するテスト群。事前条件確認、doctor 実行、worktree の対象選択、INDEX.md 更新、Codex 呼び出し、commit 条件までを外部挙動として扱う。

## Read this when
- `cmoc indexing` のコマンド全体の流れを確認したいとき。
- CLI がどの条件で開始・拒否されるか、また INDEX.md 生成後にどこまで commit されるかを確認したいとき。
- preflight が repository 側設定を使うか、既存差分や fresh な hash をどう扱うかを確認したいとき。

## Do not read this when
- INDEX.md の見出し文面や structured output schema の定義そのものを確認したいときは、対応する oracle doc / oracle src を直接読むべきで、このテスト群はその確認先ではない。
- `cmoc indexing` 以外のサブコマンドの routing や一般的な CLI 基盤を確認したいとき。

## hash
- b8f18f4f34453e17c3374b1d18b1a6ab8783ad6f91e203eea335553525b20b80

# `test_indexing_common.py`

## Summary
- `commons.indexing` の INDEX entry 生成と `update_indexes` の並び替え・再生成・巡回制御を検証するテスト群。CLI lifecycle ではなく、入力検証、hash 再利用、空ディレクトリ、兄弟順序、並列実行、memo 配下と symlink cycle の扱いに関心があるときに読む。

## Read this when
- INDEX entry のスキーマ不一致や空欄・複数行などの入力検証を確認したい。
- 既存の hash を使った再生成判定、空ディレクトリへの INDEX.md 作成、兄弟ファイルの安定順序、非祖先ディレクトリの並列生成を確認したい。
- memo 配下の除外、nested memo directory の扱い、directory symlink cycle の回避、Codex logger の worker 伝播を確認したい。

## Do not read this when
- CLI 引数、サブコマンド登録、実行開始・終了などの lifecycle 全体を追いたいときは、より上位のサブコマンド側を見る。
- INDEX entry の文面や構造の正本仕様そのものを確認したいときは、対応する oracle doc と oracle src を読む。
- indexing 以外の path 操作や git 周辺の汎用支援を探しているだけなら、このテスト群ではなく共通 helper 側を見る。

## hash
- a28c58c6959452820522f14be786bfc035d8a6b29a00f91a6094146c5ef92970

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
- `review_oracle` の finding 生成・統合・検証・判定の loop 挙動を確認するテスト。`sub_commands.review.oracle` と `sub_commands.review_loop` の周辺で、review 実行時の prompt の受け渡し、同一周回の challenger reason の保持、merge 再試行と失敗終了を追うときに読む。

## Read this when
- review oracle のループ制御を変更するとき
- enumerate / merge / validate / judge の prompt や Structured Output の受け渡しを確認するとき
- review 実行時の worktree 分離や Codex 呼び出しコンテキストを確認するとき

## Do not read this when
- review oracle 以外のサブコマンドのテストを探しているとき
- review の結果保存や CLI 引数の定義だけを見たいとき
- 単体の config 定義や prompt 断片だけを確認したいとき

## hash
- fed9e6e5051f630206f5b5526456c9740bc1d5e8eb362984be37c7c43e20627e

# `test_review_oracle_merge_operations.py`

## Summary
- `sub_commands.review.oracle` の merge operation 適用ロジックを検証するテストに進むための入口。kind ごとの契約、無効な operation の拒否、同じ `finding_id` の再利用拒否を確認したいときに読む。
- `review_oracle` の `apply_finding_merge_operations` の振る舞いだけを追う対象で、review 全体の CLI や他の review テストへ広げる必要はない。

## Read this when
- `apply_finding_merge_operations` の kind 契約を変更したか確認したいとき。
- merge operation の入力検証や、複数 operation 間での `finding_id` 再利用の扱いを確認したいとき。
- `review` 配下の他の処理ではなく、oracle 側の merge 適用だけを見たいとき。

## Do not read this when
- merge operation 以外の review 振る舞いを探したいだけのとき。
- `review` サブコマンド全体の仕様や CLI 入出力を追いたいとき。
- `apply_finding_merge_operations` ではない別の merge / update ロジックを確認したいとき。

## hash
- f7714ad7732b9348c4fe7a238e28d6e5fd4218534da6ddca3fa14e81d5ee9425

# `test_review_oracle_report.py`

## Summary
- `review oracle` のレポート生成と CLI 出力の検証が必要なときに読む。`eval-oracle` からの委譲、`review oracle` の report 生成、findings の severity 別集計、`<oracle-root>` や symlink を含む path の扱い、失敗時の error report をまとめて確認するための入口。
- 同じ report でも本文の整形や集計結果を変える変更、または `review oracle` の処理失敗時の出力仕様を触る場合に読む。CLI 引数の短縮形や、report 内の節順・件数・見出し・エラー提示の安定性を確認したいときもここが起点になる。

## Read this when
- `review oracle` の report 生成ロジックや CLI 出力を変更するとき
- `eval-oracle` から `review oracle` 実装への委譲関係を確認したいとき
- finding の severity 別分類、accepted / rejected の集計、`<oracle-root>` 表示、symlink の集計方法を確認したいとき
- 処理失敗時に error report を保存・表示する挙動を確認したいとき

## Do not read this when
- CLI 全般の共通引数や他サブコマンドの仕様だけを見たいときは、対象サブコマンド側の本文を先に読む
- report ではなく finding の抽出・判定・マージの個別アルゴリズムだけを追いたいときは、該当する実装本文を直接読む
- oracle 仕様の正本そのものを確認したいだけなら、このテストではなく参照されている oracle/doc 側を読む

## hash
- 935e77fc35d5f1399bd939bc84ccff0af77f3a3243841beb058ebac306a72e7a

# `test_review_oracle_targets.py`

## Summary
- review oracle の対象選定と finding の oracle_path 解決を検証するテスト群。review 対象に含めるべき oracle file の判定、スコープ差、symlink や ignore の扱い、review_report に渡る対象列挙の境界を確認したいときに読む。

## Read this when
- review oracle の対象ファイル一覧が期待どおりに絞られているかを確認したいとき
- finding 側の oracle_path が `<work-root>` や `<oracle-root>` をどう解決するかを確認したいとき
- AGENTS.md や INDEX.md をレビュー対象から外す境界、または symlink と ignored file の扱いを確認したいとき

## Do not read this when
- review oracle の実行手順全体や report 生成の体裁を知りたいときは、review oracle の本体仕様を読む
- finding の生成条件や妥当性判定の内容を知りたいときは、review oracle の finding 仕様を読む
- oracle/realization の基本定義や開発規則を確認したいときは、基本定義や開発規則側を読む

## hash
- 4ff6e057baf2abd446b7801f8849de7bcdb5e725d49f8020b2d79644cf8cfb96

# `test_review_oracle_worktree.py`

## Summary
- `review oracle` の worktree 分離、`INDEX.md` の統合、未コミット差分の拒否、preflight 由来の変更反映、`INDEX.md` 以外の差分検出を検証する回帰テスト群。

## Read this when
- `review oracle` が session/worktree/branch のどこを対象にするかを確認したいとき。
- review 実行中に `INDEX.md` だけを統合し、それ以外の差分は失敗扱いにしたいとき。
- preflight が review 用 worktree で作った `INDEX.md` をどう扱うか、また merge conflict の解決方針を確認したいとき。

## Do not read this when
- `review oracle` の本体実装や report 生成ロジックを追いたいときは、実装側の `sub_commands.review.oracle` を読む。
- `INDEX.md` の更新規則そのものを知りたいときは、`app_spec/indexing.md` 側を読む。
- session fork や run isolation の一般仕様だけを確認したいときは、個別の実装テストではなく対応する仕様文書を読む。

## hash
- f94e36cff864f0b6cb1c8e218ca36b0fc7ec0dcf813906f946fa64894322a49b

# `test_runtime_apply.py`

## Summary
- `test_runtime_apply.py` は、`cmoc apply abandon` の停止契約を支える `commons.runtime_apply` の低レベル挙動を検証する実現テストです。親 process と child process group の停止順、pidfd による identity 確認、pid file の再読込、advisory lock 待ち、stale PID の扱いを確認したいときに読む対象です。

## Read this when
- `commons.runtime_apply` の process tracking や停止処理を変えるとき
- pid file / advisory lock / pidfd / process group の契約を壊していないか確認したいとき
- `cmoc apply abandon` の実装で、親 process と child process をどう止めるかを判断したいとき

## Do not read this when
- `cmoc apply abandon` の CLI 出力や終了コードだけを調整したいとき
- apply abandon の外部振る舞いを確認したいだけで、低レベル停止契約には触れないとき
- この領域の実現テストではなく、`test_apply_abandon_cli.py` 側の振る舞いを追いたいとき

## hash
- 66f7a26fdcfbe337f576bc26ca807e45648fb30e637b927817c6821992316d28

# `test_runtime_cli.py`

## Summary
- CLI のエラー表示、引数解析、completion の分岐、work root 前提、preflight と subcommand ログの境界を確認するテスト群。`cmoc` の起動時副作用や `CmocError` の出力形式を追いたいときに読む。
- `doctor`、`indexing`、`session fork` などの個別サブコマンドに対する CLI ラッパーの振る舞いを見たいときに読む。`runtime_cli`、`runtime_logging`、`cmoc_runtime`、`main` のいずれか単体だけでは判断しにくい結合部を確認する入口として使う。
- `_cli_support`、`_git_support`、`_ollama_support` を使うテスト補助と、ログ/ignore/worktree 生成の検証を含む。実装本体ではなく、CLI 周辺の統合テストを探すときの入口にする。

## Read this when
- CLI のエラー整形が stdout に出るか、stderr に出ないかを確認したいとき。
- work root 判定、completion probe、doctor preflight、pre-log check、subcommand logger の境界を確認したいとき。
- `apply fork` や `review oracle`、`indexing` の CLI 実行前後の副作用を統合的に追いたいとき。

## Do not read this when
- 個別のコマンド実装そのものを見たいときは、対応する realization implementation を先に読む。
- `CmocError` の定義やログ出力の詳細仕様だけを見たいときは、`cmoc_runtime` や `runtime_logging` を直接読む。
- git ignore 判定や worktree 操作の単体仕様だけを見たいときは、このテストではなく補助実装や関連 oracle を直接読む。

## hash
- dade856da0c8a93ed552ca689c1cd207e4246df1634d127743f5a03ca7185b49

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
- Codex の `build_codex_override_args` が作る書き込み許可の境界を検証するテスト群。`FileAccessMode` ごとの既定許可、`extra_writable_paths` の受理・拒否、`AGENTS.md` / `INDEX.md` / `memo` / `.agents` / `.cmoc/local` / `.codex` / `.git` の保護、ignore された gap path の扱いを確認したいときに読む。
- `src` や `oracle` のような通常の作業領域と、追跡対象・無視対象・ルーティング用ファイルのどこまでを書けるかが論点なら、このテストが入口になる。権限境界そのものではなく、別の CLI 挙動や設定項目の変更ならここは読まなくてよい。

## Read this when
- Codex の read/write 許可領域の判定や、モード別の既定書き込み範囲を変えるとき。
- `extra_writable_paths` を追加・変更し、その許可条件や拒否条件を確認したいとき。
- `AGENTS.md` / `INDEX.md` / `memo` / `.agents` / `.cmoc/local` / `.codex` / `.git` の保護方針を変える可能性があるとき。
- ignore された未追跡パスや gap path を書けるかどうかの扱いを確認したいとき。

## Do not read this when
- Codex の出力文面、プロンプト生成、レビュー判定など、書き込み権限以外の機能を扱うとき。
- 実装の内部分割だけを変えたいときで、許可・拒否の境界が変わらないとき。
- 一般的な Git 操作やファイル作成の話だけを確認したいとき。

## hash
- 8c55e8e1aa250ef75785626205590430a91e08a96cf7782fef12e3cd91ae53da

# `test_runtime_codex_profile.py`

## Summary
- Codex CLI の `build_codex_override_args` が、`FileAccessMode` ごとに model / sandbox / permissions / writable roots をどう上書きするかを確認したいときに読むテストです。
- `cmoc managed ollama` を model provider に選ぶ経路、linked worktree 実行時の追加 read root、`memo` / `.agents` / `oracle` / `src` / `test` の境界が主題です。

## Read this when
- Codex 呼び出し前に生成する argv と permission profile の境界を変える、またはそのテストを追加・修正したいとき。
- `READONLY` / `PURE_ORACLE_READ` / `PURE_ORACLE_WRITE` / `REALIZATION_WRITE` / `REPO_WRITE` の許可範囲や、追加 read/write path の拒否条件を確認したいとき。
- `ModelClass` と `CodexModelSpec` の解決結果、`cmoc_managed_ollama` の provider 設定、`--disable multi_agent` の有無を追いたいとき。

## Do not read this when
- Codex CLI の実行ログ保存や quota/retry の挙動を見たいときは、`runtime_codex.py` 側を読むべきです。
- `CmocConfig` の永続化形式や設定項目の定義そのものを見たいときは、config 側の本文を読むべきです。
- file access ではなく prompt 本文の組み立て規則だけを見たいときは、`oracle/src/oracle/prompt_builder/parts/file_access_rule.py` 側を読むべきです。

## hash
- fbc9a30090b77a12c61da0b2bd836fb37f3731e5d5bd72faa8955183990be6be

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
- `session` / `apply` の状態ファイル形状検証と、branch 名から session id を取り出す境界条件を確認するテスト群。破損した branch 名や不正な state/payload 値を拒否する挙動、`session_fork_lock` の process 間排他を扱う場合に読む。
- この対象を読む理由は、`commons.runtime_state` の入力検証と永続 state の読み書きの仕様を確かめたいとき、および session fork のロック共有を確認したいときに直接関係するため。

## Read this when
- `SessionState.from_dict` や state JSON の許容/拒否条件を変える変更をするとき
- `branch_session_id` / `apply_branch_session_id` の branch 解析ルールを確認したいとき
- `load_state_for_branch` が壊れた branch 名をどう扱うべきかを確認したいとき
- `session_fork_lock` が複数 process から見て同じ排他になっているかを確認したいとき

## Do not read this when
- CLI の引数解析や subcommand の起動条件だけを確認したいときは、各 subcommand 側の INDEX を先に読む
- state の具体的な保存先や path 生成だけを確認したいときは、`commons.runtime_state` 本体を先に読む
- apply/join の処理フロー全体を追いたいだけなら、このテストより対応する subcommand 実装を先に読む

## hash
- 369b191c06b7583dd211ba405d91b594aeb2da787f357f21e9088747b8f93b01

# `test_session_cli.py`

## Summary
- `test/test_session_cli.py` は `session fork` / `join` / `abandon` の外部挙動をまとめて検証する統合テスト群です。session branch と session state の生成・更新・削除、linked worktree での振る舞い、dirty worktree や破損 state、cleanup 失敗、Codex 実行境界の確認を読むときに進みます。
- 同じ session CLI の回帰でも、個別の内部 helper の単体仕様よりも、branch/state のライフサイクルやサブコマンド境界、preprocess 順序、conflict resolution の観測点を確認したい場合にこのファイルを読むのが適切です。
- このファイルは session CLI の回帰検証に特化しているため、別サブコマンドの挙動、一般的な Git 操作、共通テスト支援の実装を知りたいだけなら直接読む先ではありません。

## Read this when
- `session fork` / `session join` / `session abandon` の外部挙動をまとめて確認したいとき。
- session branch の作成・復帰・削除、session state の永続化と cleanup の関係を確認したいとき。
- linked worktree での session 操作、dirty worktree 拒否、破損 state、ID collision、conflict resolution の回帰を追いたいとき。
- Codex 実行時の file access 境界や、session join の conflict 解消フローを観測したいとき。

## Do not read this when
- 個別の session サブコマンドの実装本体だけを追いたいときは、それぞれの `src/sub_commands/session/*.py` を先に読むべきです。
- テスト支援の共通処理や Git 生成系 fixture の責務を知りたいだけなら、まず `_cli_support` / `_git_support` / `_ollama_support` 側を読むべきです。
- session 以外の CLI や汎用の doctor / codex preflight の仕様を知りたいだけなら、この統合テストではなく対応する専用テストを読むべきです。

## hash
- be177cf5149c6a513e56b9a51dbf63442b7a661403128325202afa68278890f0

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
