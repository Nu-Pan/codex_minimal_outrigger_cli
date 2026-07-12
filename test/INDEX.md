# `_acp_builder_support.py`

## Summary
- テスト側から `<work-root>/oracle/src/oracle/acp_builder` 配下の schema を読むための共通 path 解決をまとめる。oracle tree の schema 参照先をテストごとに重複させたくないときに使う。

## Read this when
- acp_builder 関連テストで、正本 schema ファイルの実体位置を一箇所に集約して参照したい。
- テストが oracle tree の schema を読むが、`test` 配下からの相対計算を個別に書きたくない。

## Do not read this when
- acp_builder 以外のテスト対象で path 解決が必要なら、対象ごとの専用 helper を探す。
- oracle schema 自体の内容や structured output の仕様を確認したいだけなら、oracle tree 側の本文を読む。

## hash
- 4d3dade84c28b5de1c63095a310c1bb8a6a93bfc3a68a86e42f78ea3591b73f5

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
- Codex 実行系テストで共通に使う支援関数群。認証済み `CODEX_HOME` の作成、Codex への override argv の固定、CLI 引数や `--config` の解析をまとめる。
- ファイルアクセス制約の検証補助も含む。sandbox の writable roots や permission filesystem の override を読み取り、実行系が期待どおりの権限引数を組み立てたかを確認する。

## Read this when
- Codex 実行ラッパーや TUI ラッパーの subprocess 引数生成を確認したいとき。
- Codex の認証済みホーム、override 設定、権限まわりのテスト補助が必要なとき。

## Do not read this when
- 実際の Codex サブコマンド実装や権限判定ロジックそのものを追いたいときは、対応する実装側を読む。
- Codex 以外の一般的なテスト共通処理を探しているだけなら、このファイルではなく目的のテスト群の近くを読む。

## hash
- ba4cb11e6ee70e7f8467264bba74cdc97cb3ec5238e9088a72df4d0f8bc02c7e

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
- `test` 配下の Ollama 関連テスト用の共通補助をまとめる。`doctor` を本番と共有する managed Ollama 環境で実行する流れを使うときに読む。
- この補助は `doctor` の呼び出し方と前提条件を固定するためのもの。テストが本番ユーザー用サービスをそのまま使う前提や、`127.0.0.1:11434` の固定エンドポイントを保つ必要がある場合に参照する。
- `fake service` のライフサイクルを扱うテスト、Ollama 以外の CLI 補助、`doctor` 以外の起動経路を探す場合は読む対象ではない。

## Read this when
- Ollama を本番共有の managed service に対して起動するテスト補助が必要なとき。
- `doctor` を実サービス前提で呼び出し、結果の `exit_code` を確認したいとき。
- テスト側で HOME や PATH、固定のローカル Ollama エンドポイントを維持したまま実行したいとき。

## Do not read this when
- fake な Ollama サービスやサービス寿命の制御をテストしたいとき。
- `doctor` 以外の CLI サポートや、別のテスト対象の共通補助を探しているとき。
- Ollama 接続先や実行前提を切り替える必要があるとき。

## hash
- 8244f5a3e425825932ae1324ddc139123d345e1c619a2bae3907480b74034a41

# `test_acp_builder_apply_parameters.py`

## Summary
- `test/test_acp_builder_apply_parameters.py` は、apply fork ACP builder の parameter 生成が参照する root と schema を正本仕様どおりに保つための回帰テスト群を扱う。
- `build_apply_fork_finding_application_parameter` / `build_apply_fork_file_finding_enumeration_parameter` / `build_apply_fork_change_summary_parameter` のプロンプト内容、`ModelClass` / `ReasoningEffort`、および `change_summary.json` の structured output schema 参照を確認する変更で読む。
- `<work-root>/oracle/src/oracle/acp_builder/apply/fork/` 配下の正本 schema と整合しているかを確認したいときに読む。

## Read this when
- apply fork の prompt に含める `<repo-root>` / `<work-root>` の解決方法を確認・変更するとき。
- apply fork の parameter が `EFFICIENCY` / `MAX` を使うか、または change summary の schema 参照先を変えるとき。
- このテストが正本 schema に対して何を保証しているかを確認してから、対応する oracle 側の schema を読む入口にしたいとき。

## Do not read this when
- apply fork の内部実装分割や helper の構成だけを見たいときは、ここではなく `src/acp/builder/apply/fork/` 側を読む。
- `INDEX.md` や `AGENTS.md` のルーティング規則だけを確認したいときは、このテスト本文ではなく上位の案内を読む。
- apply fork 以外の ACP builder の parameter や schema を確認したいときは、別の対象を読む。

## hash
- ad5013ffbb81db63d43cd2df671bb69676c90d090a15ed18326282682768c428

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
- `cmoc session join` の conflict resolution 用エージェントパラメータの契約を確認するテストを読む入口。公開 API がビルダ 1 本に絞られていることと、repo write 前提の実行条件を固定していることを確認したいときにここから入る。

## Read this when
- `cmoc session join` の conflict resolution まわりで、公開されるビルダ API と実行パラメータの契約を確認・変更したい。
- module の公開面を絞る意図や、conflict 対象ファイルを扱うときの実行モードを確認したい。

## Do not read this when
- prompt 本文や conflict 対象ファイルの列挙ルールそのものを見たいときは、対応する oracle src 側を読む。
- 通常の session join 接続処理や他サブコマンドのパラメータ生成だけを見たいときは、ここではなくその責務のファイルを読む。

## hash
- 1f7fc5c95bedda5a2db47987f9878a67578090967083c0cbf66d96941114e4b7

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
- `apply abandon` の外部挙動を CLI 経由で確認するテスト群。active apply run の worktree・branch・state の cleanup、実行位置の違い、running process の停止順序と警告扱いをまとめて検証する。
- 破損 state や別 session 由来の apply branch、実行中 process 情報の欠落など、破棄前に拒否すべき境界条件も含む。関連する apply の終了・停止・識別ロジックを読むときの入口にする。

## Read this when
- `apply abandon` の成功時 cleanup と、警告を伴って成功する条件を確認したいとき。
- running apply process の停止順序、pid file の再読込、PID reuse や stale 判定の挙動を変えるとき。
- apply branch / worktree / session state の整合性チェックや、CLI をどの位置から実行しても repo state を正として扱う挙動を確認したいとき。

## Do not read this when
- `apply fork` の生成処理そのものを知りたいときは、fork 側のテストや実装を先に読む。
- session 管理全般や他の apply サブコマンドの挙動だけを追いたいときは、このファイルではなく該当コマンド側を読む。
- 汎用的な git helper や process helper の実装詳細だけを確認したいときは、対応する support / runtime 側を直接読む。

## hash
- 7dda7a8523bb0c2ec92929a723d19149786a264a7fead78891be287887817151

# `test_apply_fork_cli.py`

## Summary
- `apply fork` の CLI 回帰テスト群です。セッション fork 後の apply 実行が、state 更新・worktree/branch 生成・docter preprocess・gitignore 修復・設定エラーの停止条件・対象 path の編集可否・report 生成前の完了状態反映まで、意図どおりに進むかを確認します。
- `session` や target 正規化の責務はここでは扱いません。apply fork の実行フロー、状態管理、外部副作用、CLI から見える振る舞いを確認したいときに読む対象です。

## Read this when
- `apply fork` の end-to-end 振る舞い、state file の遷移、apply branch / worktree の生成・配置・参照先を確認したいとき。
- doctor preprocess の実行順、`.gitignore` と `.git/info/exclude` の補正、設定不足・設定破損時の失敗条件を確認したいとき。
- 所見対象としての `.gitignore` 編集可否や、完了状態を書いた後に report を生成する順序を確認したいとき。

## Do not read this when
- session fork 自体の生成・正規化・分岐命名だけを確認したいときは、session 側のテストを読むべきです。
- target path の個別正規化や enumerator の単体挙動だけを確認したいときは、より狭い対象のテストを読むべきです。
- 実装詳細の helper 分割だけを追いたいときは、この CLI 回帰テストではなく対応する実装モジュールを読むべきです。

## hash
- 8550fb3bf6e082be28fe1c33fe52dc26ec9fb90fe032ebedd70a85ec2fb9c9ad

# `test_apply_fork_report_cli.py`

## Summary
- `apply fork` の report 生成、変更要約、変更ファイル再調査、rolling 対象の切り替えまでを CLI 経由で検証するテスト群。`change_summary`/`file_finding_enumeration`/`finding_application` のビルド条件と、収束・未収束・error 時の report 記載を読む入口に向く。
- `sub_commands.apply.fork` の内部分割そのものより、外部から見える report 内容、session state 更新、commit 対象の選び方、未追跡 file や削除済み file を含む差分扱いの確認が主目的。

## Read this when
- `apply fork` の report 仕様、変更要約の出し方、再検査ループの収束条件、rolling 実行時の対象選定を確認したいとき。
- `change_summary.json` や所見列挙結果、適用後の diff 反映、session state 更新のどれかが関係する変更をするとき。
- packaged layout から `acp.builder.apply.fork.*` を import できることや、prompt が正本の制約文を含むことを確認したいとき。

## Do not read this when
- `apply fork` 以外の apply 系サブコマンドの挙動だけを確認したいときは、より直接のテストを先に読む。
- report の書式そのものではなく、個別の builder 実装や共通 prompt 定義だけを確認したいときは、対応する実装側へ進む。
- 一般的な oracle/realization 規約だけを確認したいときは、このテストファイルではなく規約本文を読む。

## hash
- 9b9131aac7157d3e975a800e16d5423239be3ee95c4df8e9b332b827de1d20b3

# `test_apply_fork_target_normalization.py`

## Summary
- `cmoc apply fork` の調査対象ファイル正規化を検証する回帰テスト。`apply_fork` の対象判定境界、特に `memo`、`.cmoc/local`、`.agents`、`.codex`、`INDEX.md`、`AGENTS.md`、binary、tracked ignored file、symlink の扱いを確認したいときに読む。

## Read this when
- `cmoc apply fork` の対象ファイル選定や正規化ロジックを修正・検証するとき。
- root 直下の除外と入れ子ディレクトリの許可、管理領域や規範ファイルの除外、tracked ignored file の扱い、binary file の扱い、symlink の分類境界を確認したいとき。

## Do not read this when
- apply fork の CLI 引数、状態遷移、レポート生成、終了コードを確認したいときは、`apply_fork` 本体の仕様を読む。
- apply fork 以外のサブコマンドの対象選定やレポート仕様を調べたいとき。
- 所見列挙や修正依頼の agent call 詳細を確認したいときは、対応する parameter 生成仕様を直接読む。

## hash
- 51657e4c95aa0a047d663a1f57a72aa545e7cf426eb4fc1cf4ee3d896d87c74c

# `test_apply_join_cli.py`

## Summary
- `apply join` の CLI 経路を検証するテスト群への案内。`session fork` と `apply fork` の後に `apply join` を実行し、apply worktree の削除、状態更新、report 生成、現在作業ディレクトリ依存、想定外差分、merge conflict、force resolve まで含めて確認する内容が中心です。
- 同じ join 操作でも、通常の join 成功・拒否条件・worktree 上からの実行・linked session worktree への反映・期待差分と想定外差分の判定・削除対象/非対象パスの境界を読む必要があるときに参照します。

## Read this when
- `apply join` の CLI 挙動を追加・変更・修正するとき。
- apply worktree の後片付け、session state 更新、join report の出力内容を確認するとき。
- dirty worktree、stale apply branch、想定外差分、merge conflict、`--force-resolve` の扱いを確認するとき。
- apply 側と session 側で、どのパス変更が join 対象かを判定するロジックを確認するとき。

## Do not read this when
- `apply fork` 自体の作成処理を確認したいだけのときは、fork 側のテストを読むほうが直接です。
- `session fork` や session 管理の一般仕様だけを追いたいときは、session 系のテストや実装を直接読むほうが適切です。
- CLI 全体の共通ヘルパや git 補助だけを見たいときは、この join 専用テストではなく対応する共通 helper を読むほうが適切です。

## hash
- 0d6fcbd296b8040330a858c52010e552228ccaf7cd043ae6d0fe42543b105d51

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
- `tui` サブコマンドの起動前後で、エディタ編集・正規化済みプロンプト生成・Codex 起動・ログ保存・linked worktree での保存先選択がどうなるかを確認するためのテスト群。
- `file_access_mode` の既定値や、linked worktree では元 worktree 側の `.cmoc/local` 配下を使う境界を見たいときに読む。
- `.gitignore` の更新や `.cmoc/local/log/sub_command` との連携を含む、TUI 前処理の副作用を確かめたいときに進む先。

## Read this when
- `tui` 実行時の前処理が期待どおりか、外部挙動ベースで確認したい。
- 編集前の入力プロンプトと、編集後に Codex へ渡す complete プロンプトの差分や保存内容を検証したい。
- linked worktree で起動した場合に、ログ・schema・ignore 設定の参照先がどこになるかを確認したい。

## Do not read this when
- TUI 本体の実装手順やヘルパー分割を追いたい場合は、`sub_commands/tui` 側を先に読む。
- CLI 全体の起動や共通前処理の責務を見たい場合は、このテストより上位のエントリを読む。
- `tui` 以外のサブコマンドの挙動を知りたい場合は、このファイルは読まず各サブコマンドのテストを読む。

## hash
- 9e0d700b4fd811d3e02456d89c2eedb5ccc42d251d1e9b51791c80f989b16698

# `test_codex_runtime_errors.py`

## Summary
- Codex 実行まわりのエラー処理を確認するための回帰テストで、CLI が起動できない失敗を例外とログの両方で検証する。

## Read this when
- Codex 実行が `FileNotFoundError` で始められない場合の扱い、または失敗時に残る `codex_call` ログの内容を確認したいとき。

## Do not read this when
- 通常の成功系の実行経路だけを追いたいとき。CLI 未検出ではなく、再試行・quota・Structured Output の検証を見たいときは別の実行テストを読む。

## hash
- 93c65cc35c92826c9d1154c06f038f65f764d1ef713c15f24c8cf09fe89a6446

# `test_codex_runtime_exec.py`

## Summary
- `test_codex_runtime_exec.py` は、Codex 実行経路の統合テストをまとめる。`run_codex_exec` が実際の Codex CLI に渡す引数、`prepare_codex_override_args` が組み立てる上書き設定、local SLM 用の managed ollama 事前確認、`CODEX_HOME` 配下に永続設定を作らないことを検証する。
- Codex 呼び出しの接続先や権限、モデル選択、プロンプト・スキーマの受け渡し、production と同じ managed ollama を前提にした挙動を変えるときに読む。実装の内部分割や汎用ヘルパーの整理だけなら、ここは直接読まなくてよい。

## Read this when
- Codex 実行時の CLI 引数や override 設定の形を変えるとき
- local SLM を使う経路で managed ollama の事前確認や provider 選択を調整するとき
- `CODEX_HOME` に設定ファイルを残さないことや、実際の Codex 呼び出しとの接続を確認したいとき

## Do not read this when
- 一般的な config モデル定義や未接続の runtime helper だけを変更するとき
- Codex 以外のサブコマンドや別の入出力変換を扱うとき
- 純粋なユニットテストの細部や内部実装の分割方針だけを確認したいとき

## hash
- 3f9a0023bfa0b79b2da39d3e43aa7709a388c8a89e7c1a75ca5a4d58f78d133e

# `test_codex_runtime_home.py`

## Summary
- Codex 実行ラッパーが `CODEX_HOME` をどう解決し、実行前にどの環境不備で失敗するかを確認するテスト群。既定の home 探索、相対パスの扱い、`auth.json` 必須条件、そして失敗が Codex CLI 起動前に起きることをまとめて検証する。
- `run_codex_exec` の home まわりの外部挙動を変えたときはここを読む。CLI 実行ログや subprocess の起動有無まで含めて、環境検証の境界を確認したい場合の入口になる。

## Read this when
- `run_codex_exec` が使う Codex home の決め方を変えるとき
- `CODEX_HOME` が未設定・相対パス・存在しない・ディレクトリでない場合の失敗仕様を確認したいとき
- Codex CLI を呼ぶ前に落とすべき前提条件を追加・変更するとき

## Do not read this when
- Codex home の探索や妥当性判定の実装そのものを追いたいときは、`commons.runtime_codex` 側を直接読む
- home 以外の `run_codex_exec` の入出力変換や実行制御を見たいときは、このテスト群ではなく該当する実装・別テストを読む
- CLI 本体の挙動や `auth.json` の生成処理を確認したいときは、このファイルではなく Codex 側の実装を読む

## hash
- c9a20de9c8172da28721fd715784c7c730de2ca80fbc9570c61c9a0b85b0024c

# `test_codex_runtime_paths.py`

## Summary
- Codex 実行時の作業ディレクトリ、出力スキーマ保存先、権限オーバーライドの境界を確認するテスト群。リンク済み worktree や repo-local 読み取りの扱い、`.agents` を開けないことも含め、実行パス周りの仕様を見たいときの入口になる。

## Read this when
- `run_codex_exec` の cwd や `--cd` の扱いを確認したい。
- 出力スキーマの保存先が worktree ではなく repo root 側になる条件を確認したい。
- 権限オーバーライドが `oracle` や `.cmoc/local` にどう効くか、`.agents` を開けない制約を確認したい。

## Do not read this when
- Codex 実行そのものの引数組み立てやプロンプト生成の詳細を見たいときは、より下位の実装を読む。
- ファイルアクセスルールの正本定義だけを確認したいときは、対応する oracle 側を先に読む。

## hash
- cbc9905852473ebc5dedf6cd82179034059f08384ffcb6f2117858b6f3afc1fa

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex 実行時の quota exceeded 後に、probe・resume・再実行・失敗停止の制御が外部挙動としてどう動くかを確かめる回帰テスト群。JSONL からの resume token 復元、quota probe の組み立て、`CODEX_HOME` と `cwd` の扱い、call log と subcommand log の記録もこの範囲に含める。
- 同じ retry 状態機械を前提にした fake Codex 呼び出し列やログ観測をまとめて追う必要があるときに読む。probe 共有、resume の有無、quota 待機の上限、並行実行時の代表 probe、probe 失敗時の即時エラーを確認したい場合の入口になる。

## Read this when
- Codex 実行が quota exceeded から回復する経路、または回復しない経路の外部挙動を変えたか確認したいとき。
- resume token の復元方法、quota probe の最小パラメータ、実行ログの残り方、`CODEX_HOME` と相対パスの解決を確認したいとき。
- quota 待機中の再試行回数、代表 probe の共有、並行呼び出し時の挙動を変える変更を入れるとき。

## Do not read this when
- quota retry 以外の Codex 実行経路だけを調べたいときは、より直接の実行テストへ進む。
- prompt 生成や一般的な ACP パラメータ変換だけを確認したいときは、この巨大な quota retry 回帰群ではなく、その責務のテストを読む。
- このファイルは Codex の出力品質そのものを評価する場所ではないので、LLM 品質や一般的な CLI 挙動の確認目的では読まない。

## hash
- 2dc5f969b51ae479362084efa15fa55d95d09cbcbdc6070e262369eeaac4b754

# `test_codex_runtime_retry.py`

## Summary
- `run_codex_exec` のリトライ挙動を検証するテスト群。構造化出力の再試行、JSONL エラーの扱い、capacity/quota の再試行条件、再試行後も差分や入力が維持されることを確認する。

## Read this when
- `commons.runtime_codex.run_codex_exec` の再試行条件や失敗時の判定を変更する。
- Codex CLI の出力解析、structured output の検証、capacity/quota 由来の再実行ロジックを変える。
- 呼び出しログやサブコマンドログに残す状態・エラー内容・再試行回数の扱いを確認したい。

## Do not read this when
- `run_codex_exec` 以外の CLI 起動経路や別サブコマンドのテストを探している。
- ファイルアクセスモードやプロンプト生成そのものの仕様を確認したい。
- Codex 実行以外の一般的な JSON パースやテスト補助関数の定義を探している。

## hash
- 005c0a658825567d1a2a502527dd8c2a4f9c40c2933c021074f364d5a4a8a9b4

# `test_codex_runtime_subprocess.py`

## Summary
- Codex CLI の subprocess 起動補助に対する外部挙動を確認するテスト群。専用 process group への記録と、継承された tracking 環境変数を通常起動で無視する挙動を扱う。

## Read this when
- run_codex_subprocess / run_tracked_codex_subprocess の process group 分離や apply process tracking の扱いを変更したいとき。
- tracking file の更新・復元・継承抑制が利用者向けの挙動として正しいか確認したいとき。

## Do not read this when
- Codex CLI 全体の起動前後の argv / sandbox / schema / error 判定を追いたいときは、subprocess 境界をまとめた別の runtime_codex_profile 側を読む。
- apply 停止や pid reuse、lock 待ちなど、tracking file そのものの停止制御を確認したいときは、停止ロジック側のテストを読む。

## hash
- 3e865634ac5bf2e461b525c349fdc27b94468e171380af38fee657e2410b0cf7

# `test_codex_runtime_tui.py`

## Summary
- `codex_runtime` の TUI 起動まわりを検証するテスト群。`run_codex_tui` の事前チェック、`codex` 呼び出し引数、許可領域の判定、成功・失敗時のログ記録とエラー表示を確認する。

## Read this when
- `run_codex_tui` の入出力や失敗時挙動を変えるとき。
- `codex` subprocess の起動条件、実行位置、`--cd` や出力スキーマの扱いを変えるとき。
- `extra_read_paths`、`memo`/`oracle` へのアクセス可否、呼び出しログやサブコマンドログの記録方法を変えるとき。

## Do not read this when
- `codex` 実行本体の実装を追いたいだけなら、テスト対象の実装側を読む。
- ファイルアクセス許可やリポジトリ境界の共通ロジックを確認したいだけなら、個別テストではなく関連する runtime/permission 実装を読む。
- TUI 以外のサブコマンドの挙動を調べたいだけなら、このファイルではなく該当サブコマンドのテストへ進む。

## hash
- e300386b3a1715845fd2808fea3f15f239bfc4789c9d8f5d8cac6c3d62d2e694

# `test_doctor_cli.py`

## Summary
- `doctor` サブコマンドの振る舞いを、CLI 経由の統合テストとして固定する。git 状態の修復、`.cmoc/config.json` の生成・同期、linked worktree での対象切り替え、managed ollama の準備、既存の staged 変更を壊さないことを確認する観点をまとめている。

## Read this when
- `doctor` のエンドツーエンド挙動を変えるとき。
- .gitignore`, `.agents/.gitkeep`, `.cmoc/config.json`, `.cmoc/local` の扱いを変えるとき。
- managed ollama のセットアップや再利用条件を変えるとき。
- linked worktree で `doctor` を実行したときの対象選択や修復範囲を変えるとき。
- staged 変更・rename・untracked/unstaged 差分の保持方針を変えるとき。

## Do not read this when
- `doctor` の内部 helper の分割や実装手順だけを変えるときは、まず実装側を読む。
- `doctor` 以外の CLI サブコマンドの振る舞いを変えるときは、各サブコマンドのテストを読む。
- config schema や managed ollama の正本仕様を確認したいだけなら、対応する oracle 側の文書を読む。

## hash
- 67fcb3c7f90ea764571ab2bdcecf209a3794371b546ac6999d4875f05f61e925

# `test_indexing_cli.py`

## Summary
- `INDEX.md` 生成・更新の CLI 回帰テスト。Codex による index entry 生成、未初期化時の preflight、linked worktree への適用、dirty worktree の拒否、既存 hash 再利用、commit 対象の絞り込み、INDEX.md conflict 解決までをまとめて確認する。

## Read this when
- `indexing` サブコマンドの外部挙動を変えるとき。
- INDEX.md の生成・更新条件、コミット条件、dirty 判定、linked worktree の扱いを確認したいとき。
- index entry のレンダリングや既存 hash の再利用、INDEX.md conflict 解決の挙動を確認したいとき。

## Do not read this when
- CLI 以外の indexing 内部 helper の細部だけを追いたいとき。
- 個別の schema 検証や `render_index_entry` の入力制約だけを見たいときは、該当する実装・テストを直接読むべきとき。
- 一般的な git 操作や worktree 管理だけを確認したいとき。

## hash
- e1cfc2810879a2f8762554fea3a29f8da9421252f7960a90d0d71481184b9d82

# `test_indexing_preflight.py`

## Summary
- `commons.runtime_codex_preflight` と `commons.indexing` の連携を検証する回帰テスト群。`run_codex_exec` / `run_codex_tui` の前に index 更新が挟まること、作業対象が root と cwd のどちらに解決されるか、repository lock 待ちの挙動、parameter で preflight を無効化したときのスキップ、file access violation 時に回復用 index 更新へ逸れないことを確認する。

## Read this when
- codex 実行や TUI 実行の前処理として indexing preflight を入れる・外す・待たせる挙動を変えるとき。
- root と cwd が別 worktree のときに、どちらへ index 更新をかけるかの境界を確認したいとき。
- repository lock による排他待ちや、preflight 無効化フラグ、file access violation 後の回復経路に触るとき。

## Do not read this when
- index 生成そのものの実装だけを変える場合は、`commons.indexing` 側の本文を先に読む。
- run_codex_exec / run_codex_tui の通常実行フローだけを変える場合は、より直接の実装ファイルを読む。
- lock 取得の共通処理や git 作業ツリー生成の詳細を見たいだけなら、このテストファイルではなく対応する支援モジュールを読む。

## hash
- e471c14f079e7924022b8ffb4a7a18ee48655f53549b253c3dc4d0d610bde671

# `test_packaged_import.py`

## Summary
- `packaged` 配置での import ルートと re-export の境界を検証するテスト群。`oracle/src/oracle` を site 配下に置いたときに、builder 側の参照が正本実装へ向くことと、config の公開名が余計なものを混ぜずに定義どおりに露出することを確認する。

## Read this when
- `oracle` ツリーを配布配置した前提で import が成立するか確認したいとき。
- `acp.builder` から参照される正本定義が、packaged layout でも同一オブジェクトとして再利用されるべきか確かめたいとき。
- `config.cmoc_config` の公開名が、設定定義だけに絞られているか確認したいとき。

## Do not read this when
- 通常の機能仕様や CLI 挙動を知りたいとき。
- `oracle` 配下の個別仕様や prompt 本文そのものを読みたいとき。
- packaging 以外の import 境界、依存解決、実行時動作を調べたいとき。

## hash
- 74dd7cd80b6e020389e9935b2d03db0716995c52119fee53c27eb0c207f521cb

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

# `test_review_oracle_cli.py`

## Summary
- review oracle の CLI 実行とレポート生成を end-to-end で検証するテスト群。対象 oracle の選択、scope 別の列挙、report の見出し・集計・評価結果・エラー報告を確認する入口。
- 所見の enumerate / validate / judge / merge のループ制御、再試行、失敗時挙動、review 作業中に作られる作業ツリーや commit の扱いを検証する。
- `<work-root>/oracle` 配下の対象判定や、`INDEX.md` / `AGENTS.md` 除外、tracked / ignored / symlink / memo 混在時の対象抽出など、レビュー対象探索の境界条件を確認する。

## Read this when
- review oracle の CLI 出力、report 生成、または所見評価ループの仕様を変えるとき。
- oracle 対象の列挙条件や、`session` / `full` scope の扱いを変えるとき。
- merge 失敗、judge 失敗、未コミット差分、INDEX 競合などの失敗系や復旧系を変更するとき。

## Do not read this when
- 通常の一般的な CLI 画面や他サブコマンドの仕様だけを追うとき。
- `oracle` 以外のレビュー対象抽出や、別の report 形式を探すとき。
- 実装本体のアルゴリズムを理解したいだけで、CLI 経由の統合検証は不要なとき。

## hash
- 7eb48fbdaa9bf3f758ceeb58e9a2c6526b468a3c0038e3387d5f1d4bae16bdc6

# `test_runtime_cli.py`

## Summary
- CLI の例外整形、標準出力への error report 出力、サブコマンドログ生成、work root / worktree preflight、shell completion の副作用回避を確認する統合テスト群。`runtime_cli`、`runtime_logging`、`cmoc_runtime`、`main` の CLI 境界を変えるときに読む。

## Read this when
- CLI 実行時の error 表示先や report 形式を変えるとき。
- サブコマンド実行前後の log 記録、preflight、work root 判定、`doctor` 系の前処理の境界を変えるとき。
- completion probe で初期化副作用を起こさない保証や、`ensure_cmoc_ignored` の `.gitignore` 更新方針を確認したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジックだけを変えるときは、各サブコマンド側のテストを読む。
- Markdown report の文言だけを追いたいときは、error 生成側の実装とそれを定義する oracle doc を先に読む。
- git 操作や worktree の一般仕様だけを見たいときは、この統合テストではなく該当 helper の実装を読む。

## hash
- 24a03a7ac7e3dd0d000cf0009d55bb2f63e6546f0f419d0206fa4ed1d0377ede

# `test_runtime_codex_conflicts.py`

## Summary
- session join の conflict 解消時に、Codex の追加書き込み許可がどの path を writable にするか、また拒否対象の名前・ランタイム領域をどう弾くかを検証するテスト群。
- `build_codex_override_args` とファイルアクセス規則の境界を変える作業、特に oracle 側の conflict 解消対象と realization 側の書き込み許可判定を調整する時に読む。

## Read this when
- session join の conflict 解消で、追加書き込み許可の root 判定や拒否条件を変更したい。
- oracle file とそれ以外の path の書き込み可否、`INDEX.md` や `AGENTS.md`、runtime 領域の扱いを確認したい。
- `build_codex_override_args` の追加書き込み許可ロジックや、その回帰テストを更新する必要がある。

## Do not read this when
- 通常の session join 処理や conflict 解消ロジックそのものだけを追う場合。
- Codex のファイルアクセス規則や追加書き込み許可 path を変えない変更をする場合。
- このテストの入力生成や pytest の共通補助だけを確認したい場合。

## hash
- 2c1f26fe02d301c0b5d236b7f3b3f8701d5cd85137aec075e24902953ca46c5f

# `test_runtime_codex_permissions.py`

## Summary
- `commons.runtime_codex_profile.build_codex_override_args` が、Codex のアクセスモード別に read/write 許可の root 集合と `extra_writable_paths` の扱いを正しく組み立てるかを検証するテスト。
- `READONLY` / `PURE_ORACLE_READ` では ignored gap だけを書けること、`REALIZATION_WRITE` では標準の realization 許可領域に加えて root 直下の追加 writable path を受け入れること、`REPO_WRITE` / `PURE_ORACLE_WRITE` では許可外 path を拒否することを確認する。
- アクセス許可の境界そのものを固定したいときの回帰テストであり、`file_access_rule.py` と `oracle_and_realization_basic.py` の定義を前提に、実運用の sandbox/permission profile への反映差分を見張る入口になる。

## Read this when
- Codex override の write 許可 root が、モードごとの正本仕様どおりか確認したいとき。
- `extra_writable_paths` が root 直下の補助ファイルだけを追加許可できるのか、あるいは許可外 path を拒否するのかを変えたいとき。
- `READONLY` / `PURE_ORACLE_READ` / `REALIZATION_WRITE` / `PURE_ORACLE_WRITE` / `REPO_WRITE` の許可境界を回帰確認したいとき。

## Do not read this when
- Codex のモデル選択、provider 切り替え、`CODEX_HOME` 検査など、権限以外の override 生成を見たいときは別の runtime_codex_profile テストを読む。
- `build_codex_override_args` の内部実装や permission profile の組み立て詳細だけを確認したいときは、この回帰テストではなく実装側を読む。
- `file_access_rule.py` や `oracle_and_realization_basic.py` の正本本文そのものを読みたいときは、対応する oracle 側を直接読む。

## hash
- d68af819997d5e1e26b2678c11d27f3d636a9c29d1fb978ca7ffd2e6f913f019

# `test_runtime_codex_profile.py`

## Summary
- `build_codex_override_args` が、`FileAccessMode` ごとの Codex 起動引数・権限境界・モデルプロバイダ選択をどう組み立てるかを検証するテスト群。`oracle/src/oracle/prompt_builder/parts/file_access_rule.py` と `oracle/doc/app_spec/codex_exec_rule.md`、`oracle/doc/app_spec/external_model_provider.md` に対応する実装や変更を読む入口にする。
- `make_repo`、`run_git`、`_codex_support` を使った境界条件の確認も含むため、`<work-root>` 配下の実行権限ルール、`oracle` と `realization` の読み書き境界、linked worktree 時の追加読取許可を直すときに参照する。

## Read this when
- Codex の sandbox 権限、`FileAccessMode` ごとの `--sandbox` / `permissions` / `writable_roots` の生成条件を変えるとき。
- `oracle` 配下・`src` 配下・`test` 配下・`.agents` / `.cmoc` / `.gitignore` まわりの可読・可書き境界を調整するとき。
- local SLM のモデルプロバイダ選択や `cmoc_managed_ollama` への切り替え条件を変えるとき。
- linked worktree 実行時の `extra_read_root` や repo 側 `cmoc/local` 読取許可の扱いを変えるとき。

## Do not read this when
- Codex 起動引数そのものではなく、別の実行経路や別コマンドの引数生成を確認したいだけのとき。
- `oracle` 文書の本文を更新する作業で、このテストの観点だけを見れば十分なときは、まず対応する oracle doc を読む。
- 一般的な repo 構成やパス規則ではなく、`test_runtime_codex_profile.py` の対象外のサブコマンドや別プロファイルを扱うとき。

## hash
- 47957ed5e85c47c47926963cad8fcf38659a3583e3bb670a05160c40b0827aa8

# `test_runtime_config.py`

## Summary
- `CmocConfig` の既定値、JSON 変換時の member 順序、入力検証、欠損時のエラー文言を検証するテスト。設定の振る舞いを固定したいときに読む。

## Read this when
- `CmocConfig` の既定値や配下設定の初期値を確認・追加するとき。
- 設定の JSON 変換で順序や値の保持を変えたくないとき。
- 不正な設定入力に対する `CmocError` の出し方や文言を変えるとき。
- 設定まわりの回帰テストを追加・整理するとき。

## Do not read this when
- 設定の実装や変換ロジックそのものを追うなら、対応する実装側を直接読む。
- 設定項目の意味や正本仕様を確認したいだけなら、oracle 側の設定定義とエラーハンドリング規則を読む。
- `cmoc` 全体のコマンド体系や他領域の仕様を知りたいだけなら、このテストではなく上位のルーティングを読む。

## hash
- 7a9b7e985de26b453b7462d375d1a5d649da297d220c67025aeaa2dd591a62b9

# `test_runtime_file_access.py`

## Summary
- `FileAccessMode` の永続化値、sandbox 変換、作業 root の扱い、binary 判定の読み取り範囲という、runtime 周辺の契約をまとめて検証するテスト。

## Read this when
- `FileAccessMode` の値変更が JSON 互換性や変換先に影響しないか確認したいとき。
- `file_access_to_sandbox_mode` の各アクセス種別が sandbox 権限へ欠落なく写るか確認したいとき。
- `file_access_to_codex_cwd` が work root を維持する互換性を壊していないか確認したいとき。
- `is_binary` が先頭 chunk だけを読む前提を壊していないか確認したいとき。

## Do not read this when
- runtime の実装詳細や enum 定義そのものを追いたいだけなら、対応する realization 側を直接読む。
- prompt 生成や file access ルールの文面仕様を確認したいだけなら、ここではなく根拠側の oracle file を読む。
- binary 判定以外の content 判定や file I/O 全般の挙動を探しているなら、別のテスト対象を読む。

## hash
- 6b4a9f40267b269b622e987b9d2e3b1b6b1810d94bafedca4bc2494a6e33dcf4

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
- `commons.runtime_state` の session/apply 状態 JSON の検証と、branch 名から session id を取り出す境界条件を扱う。state file の形状・nullable 項目・不正 branch の拒否を確認したいときに読む。

## Read this when
- session/apply state の読み書き形式を変える、または branch 名から session id を解釈する条件を変えるとき。
- state file の不正値や破損 branch を、どの入力でエラーにするか確認したいとき。

## Do not read this when
- merge 手順全体や conflict 解消の流れを追いたいときは、`cmoc session join` の仕様を見る。
- branch 操作の実行順や git 操作そのものを変えたいときは、state 解析ではなく該当コマンド側を見る。

## hash
- c1e45a52f5c411c578eb0dec0daac4d2beb9d279955dd2e96e4a628dda7e7256

# `test_session_cli.py`

## Summary
- `session fork/join/abandon` の CLI 挙動と session 状態遷移をまとめて確認する回帰テスト群。fork・join・abandon、linked worktree、state cleanup、dirty worktree 拒否、エラー時の表示先を横断して見るときに読む。
- session の branch/state fixture を共有しながら、状態ファイルや git 操作の観測点をまたいで検証するための入口。個別の 1 挙動だけを追うなら、より狭い session 関連テストへ進む方がよい。

## Read this when
- `session fork` / `session join` / `session abandon` の外部挙動を一括で確認したい。
- linked worktree 上での session 操作や、session state ファイルのライフサイクルを確認したい。
- dirty worktree 拒否、cleanup 失敗時の rollback、conflict 解消後の余差分拒否など、session 遷移に伴う境界条件を見たい。

## Do not read this when
- 単一の session サブコマンドだけの内部実装を追いたい。
- session 以外の CLI 挙動や、汎用的な git / preflight / runtime の個別テストを探している。
- state 生成や conflict 判定の細部だけを追いたい場合は、該当する session 実装や補助関数のテストを直接読む方が近い。

## hash
- 3a0d8c561956207ac18030cbb067cc3032084dd50940f4a48bb46fdb5d692b3e

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
