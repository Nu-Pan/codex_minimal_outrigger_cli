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
- `acp.builder.session.join.conflict_resolution` の公開 API と、セッション join の conflict resolution 用パラメータ生成が正本どおりかを確認する回帰テスト。公開された builder だけを残し、内部依存を外へ漏らさないことと、生成時に repo write 権限・高い推論設定・索引事前処理なしで conflict 対象ファイルを prompt に反映することを扱う。

## Read this when
- セッション join の conflict resolution builder の契約変更を確認したいとき。
- 公開モジュールの export 境界や、生成される agent call parameter の権限・モデル設定・prompt 反映を検証したいとき。

## Do not read this when
- session join の他の builder や join 処理全体の挙動を追いたいときは、より直接の実装・テストを読む。
- 公開 API ではなく内部ヘルパーの分割や実装手順だけを確認したいときは、ここではなく対応する実装側を読む。

## hash
- 0e1cfedb64251290b7dab4e8a69db9fa29c5c44c0d8f10dc2783621c24cd0637

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
- `cmoc apply fork` の作業レポートと再検査ループを CLI 経由で検証する回帰テスト群。収束・未収束・error の判定、変更要約の反映、未追跡ファイルや削除済みファイルを含む差分集計、rolling apply の対象切り替えを確認したいときに読む。

## Read this when
- `cmoc apply fork` の report 出力、終了判定、再検査の繰り返し条件を変えたいとき。
- 変更要約の生成結果が report にどう反映されるか、また commit 前後や未追跡ファイルを差分としてどう扱うか確認したいとき。
- rolling apply で前回の apply join 後の変更だけを再調査対象にする挙動を確認したいとき。

## Do not read this when
- 変更要約や file 単位所見の prompt / schema そのものを確認したいときは、`acp_builder` 側の正本仕様を読む。
- `apply fork` の内部実装分割だけを追いたいときは、この CLI テストではなく対応する realization implementation を読む。
- `cmoc apply fork` 以外のサブコマンドの report や状態遷移を確認したいとき。

## hash
- 3b12e69c7edde1c04db6870c1ac26d6ed57e50b0f393cff0c221868d9287b903

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
- `apply join` の CLI 挙動を検証するテスト群。成功時の後片付け、state 更新、report 生成に加え、dirty worktree、想定外差分、merge conflict、rename/delete、symlink、tracked ignored file などの境界条件を含むため、`apply join` の外部挙動や異常系を変更するときに読む。
- 同じ `apply join` でも内部 helper の分割や処理順の細部を確認したいだけなら、ここは入口ではなく、対象実装と関連する support/helper 側を直接読む。

## Read this when
- `apply join` の完了条件、拒否条件、force resolve の扱い、cleanup と state 遷移を変えるとき.
- `apply` 側の差分分類や merge conflict 検出の外部挙動を確認したいとき.
- `apply join` のレポート内容や、どの差分を想定外として扱うかを見直すとき.

## Do not read this when
- `session fork` や `apply fork` の生成ロジックだけを追いたいとき.
- `apply join` 以外のサブコマンドの CLI 挙動を調べたいとき.
- 内部実装の関数分割や git 操作の細部だけを見たいとき。

## hash
- a4904d51642c5e6941447c5fa7bedaef92190c8de41fb49c0163d6c1d80e01b1

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
- Codex runtime の失敗系を扱うテスト群への入口。Codex CLI が起動できない場合に、例外と失敗ログの両方が期待どおりになるかを確認したいときに読む。
- CLI 呼び出しのエラー処理とサブコマンドログの記録仕様を押さえるためのファイルで、正常系や他の runtime エラーの詳細はここでは追わない。

## Read this when
- Codex CLI の不在や起動失敗を契機に `CmocError` になる経路を確認したい。
- `codex_call` ログの失敗記録に、returncode や error 文言がどう残るべきかを確認したい。
- CLI 呼び出し失敗時の振る舞いを検証するテストを追加・修正したい。

## Do not read this when
- Codex の正常系実行や引数整形だけを追いたいときは、より直接の runtime 呼び出し側を読む。
- ログ出力全般の形式や他イベント種別を確認したいときは、ログ定義側や別のログ関連テストを読む。
- このファイルが参照する正本仕様の本文を確認したいだけなら、コメントにある正本側を直接読む。

## hash
- 7187451342221a1b90bed9f51f448c8edc06dcba845caabb4c37ab8d1c91a7a8

# `test_codex_runtime_exec.py`

## Summary
- `codex exec` 呼び出しの実行経路を、`cmoc managed ollama`・`CODEX_HOME`・プロンプト/スキーマ/ログ保存まで含めて検証する回帰テスト群。Real Codex CLI を使う結合動作と、Fake ではなく実 CLI を呼ぶ前提の挙動確認が主目的。

## Read this when
- `run_codex_exec` や `prepare_codex_override_args` の変更で、Codex CLI への引数注入・プロンプト渡し・出力保存・schema 指定・`CODEX_HOME` 扱い・`cmoc managed ollama` provider 切り替えの仕様を確認したいとき。
- Real Codex CLI を使う経路で、`cmoc managed ollama` の preflight や `model_provider="cmoc_managed_ollama"` の注入が正しいかを見たいとき。
- `codex exec` 呼び出しの回帰を、実行結果だけでなく argv・stdin・保存ファイル・override config まで含めて確かめたいとき。

## Do not read this when
- Codex CLI 以外の実行経路や、`cmoc managed ollama` を使わない機能を確認したいだけのとき。
- LLM の応答品質や外部 provider 自体の正しさを検証したいとき。
- `codex exec` の内部実装ではなく、別のサブコマンドや一般的なテスト方針だけを追いたいとき。

## hash
- fc45122df2860fdbf2dcd333bae33464fe6f8f955545e7c4fcf0df07975f2263

# `test_codex_runtime_home.py`

## Summary
- `run_codex_exec` の実行前に、`CODEX_HOME` の解決結果と preflight 失敗時の遮断を検証するテスト群。`codex exec` を起動せずに失敗する条件や、相対/既定の home の扱いを確認したいときに読む。

## Read this when
- `CODEX_HOME` が未設定・相対パス・不正な型のときの `run_codex_exec` の挙動を確認したい。
- `auth.json` の有無やディレクトリ種別を理由に、`codex` subprocess を起動する前に失敗するかを確認したい。
- `run_codex_exec` が実際に子プロセスへ渡す home 値と、`call_log` に残る解決済み path の一致を確認したい。

## Do not read this when
- `codex exec` の再試行、Structured Output 検証、quota 復帰は別の runtime_codex 系テストを見る。
- `CODEX_HOME` 以外の codex 実行引数やファイルアクセス制御の確認は、対応する builder や subprocess テストを見る。

## hash
- 36143b5ce50111592664082e59e00925e96b6294be2e74248d02ee22ad33d474

# `test_codex_runtime_paths.py`

## Summary
- `run_codex_exec` の実行時パス処理を検証するテスト群。`cwd` の決定、出力 schema の保存先、権限 profile への反映、リンク済み worktree や追加 read path の扱いを確認したいときの入口。

## Read this when
- `commons.runtime_codex.run_codex_exec` の `cwd` や `--cd` の決め方を変えるとき。
- 出力 schema をどこに保存するか、repo root 配下に置くかを確認したいとき。
- `FileAccessMode` から Codex の filesystem 権限 override を組み立てる境界を確認したいとき。
- リンク済み worktree から実行したときのパス解決や、追加 read path の許可範囲を確認したいとき。

## Do not read this when
- 再試行、容量 retry、JSONL エラー、KeyboardInterrupt などの実行制御を見たいときは、別の `run_codex_exec` テスト群を読む。
- prompt 生成や `FileAccessMode` の定義そのものを確認したいときは、`oracle/src/oracle/prompt_builder/parts/file_access_rule.py` 側を読む。
- session/apply など上位 CLI の引数解決やサブコマンド分岐を確認したいときは、このファイルではなく該当する CLI テストや実装を読む。

## hash
- 962990fb7916c430d53376f096d2df6bebd94de53140f9d33951e73917f2b954

# `test_codex_runtime_quota_retry.py`

## Summary
- `Codex` 実行が `quota exceeded` 後にどう待機・再試行・再開するかを外部挙動として検証するテスト群。`resume token` の復元、quota probe の組み立て、再実行時の `CODEX_HOME`/`cwd`、呼び出しログとサブコマンドログまで含めて確認する入口。
- 並行実行時に代表 probe だけを使う制御や、probe 失敗・poll 上限・KeyboardInterrupt などの失敗経路もここで扱う。quota retry の状態機械や観測点を変える作業で読む。

## Read this when
- `quota exceeded` 後の `probe`/`resume`/再実行フローを変えるとき。
- resume token の抽出元、quota probe パラメータ、`CODEX_HOME` や `cwd` の引き回しを変えるとき。
- 呼び出しログ、サブコマンドログ、並行実行時の代表 probe 選択や失敗時挙動を確認するとき。

## Do not read this when
- quota retry と無関係な通常の `Codex exec` 挙動だけを変えるときは、まず通常経路のテストを読む。
- quota 制御以外のサブコマンド、別の runtime helper、一般的なテスト基盤の変更だけを追うとき。

## hash
- c64cd4c8efcddd5ce0f60d72c17165979faa1d2922884fc930606a53bfa34794

# `test_codex_runtime_retry.py`

## Summary
- `run_codex_exec` の再試行まわりを検証するテスト群。構造化出力の再試行、容量再試行、JSONL エラー処理、KeyboardInterrupt の記録、再試行後も差分が保持されること、stdout 以外のエラーマーカーを無視することを扱う。

## Read this when
- `commons.runtime_codex.run_codex_exec` の再試行条件や失敗時の記録方法を変えるとき。
- Codex CLI の出力検証、`call_log`/サブコマンドログの内容、再試行時のプロンプトや出力ファイルの扱いを確認したいとき。
- 容量・構造化出力・JSONL エラー・中断のいずれかが、現行の失敗判定やログ仕様に影響するかを見たいとき。

## Do not read this when
- `run_codex_exec` 以外の Codex 実行経路を確認したいときは、実装側の `commons.runtime_codex` 本体や関連する上位テストを先に読む。
- CLI 引数の組み立てや設定値の定義だけを確認したいときは、このテストではなく `basic.acp` や `config.cmoc_config` 側を読む。
- 再試行以外の一般的なテスト配置や共通 fixture の定義を探したいだけなら、ここではなく共通補助ファイルを探す。

## hash
- bae14eb77d298c8e1295c0019b1ca348d646ac5dc568b47cb944580e3e2400ea

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
- `codex tui` 実行時の制御と観測可能挙動を検証するテスト群。起動前の読み取り許可判定、プロンプト読み込み、linked worktree での実行、成功・失敗・割り込み時のログ出力とエラー報告を確認したいときに読む。

## Read this when
- `commons.runtime_codex.run_codex_tui` の振る舞いを変更したとき
- Codex subprocess の起動条件、出力、失敗時ログ、割り込み時の扱いを確認したいとき
- `FileAccessMode` ごとの許可判定や、`extra_read_paths` の扱いを見たいとき

## Do not read this when
- CLI 引数定義や設定モデルの全体を追いたいときは、より上位の実装や設定側を読む
- `codex tui` 以外のサブコマンドの仕様を確認したいとき
- 個別の補助関数の実装詳細だけを追いたいとき

## hash
- c972e0ca03002ac4f071319d0310335d543701bc370c42473134d349118dc270

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
- `indexing` CLI の回帰テスト群。`INDEX.md` の生成・再生成・衝突解決・コミット条件・linked worktree での対象決定・既存 hash 再利用・空ディレクトリやメモ配下の扱いを、外部挙動として確認する。

## Read this when
- `indexing` の実行で `INDEX.md` が作られるか、更新されるか、コミットされるかを確認したいとき。
- linked worktree や dirty 状態で `indexing` の対象がどこになるか、また処理を止める条件を確認したいとき。
- INDEX.md conflict 解決や hash 再利用、空ディレクトリ、memo 配下、symlink cycle などの境界条件を確認したいとき。

## Do not read this when
- `indexing` の実装そのものや git 操作の共通処理を追いたいときは、対応する実装側を読む。
- `INDEX.md` の個別テンプレートや生成ロジックの詳細を確認したいときは、このテストより先に indexing 関連の実装と正本仕様を読む。
- 別サブコマンドの回帰だけを見たいときは、このファイルは読まない。

## hash
- 64ee342f862e6fe7808f6a6c5d79aa2e5e40f95f86167d7d201a01479899692d

# `test_indexing_preflight.py`

## Summary
- `commons.runtime_codex_preflight` と `commons.indexing` の連携を検証するテスト群。Codex 実行前に INDEX 更新 preflight が走ること、TUI/exec 両経路で同じ前提が保たれること、索引更新がリポジトリロックに従って直列化されることを確認する。

## Read this when
- Codex 呼び出しの前に index 更新が入るかを確認したいとき。
- `cwd` が worktree 側にある場合に、root ではなくその worktree を索引更新の起点にする挙動を確認したいとき。
- 索引更新の排他ロック待ちや、`run_indexing_preflight` の待機順序を検証したいとき。
- preflight 無効化フラグや、file access violation 時に recovery 用の再 indexing が走らない条件を確認したいとき。

## Do not read this when
- INDEX 生成ロジックそのものの仕様を確認したいときは、`commons.indexing` 側のテストや実装を読む。
- Codex 入出力パラメータの組み立てを確認したいときは、ACP builder 系のテストを読む。
- session join や review/apply の個別機能の仕様を確認したいときは、それぞれのサブコマンドや oracle 側の文書を読む。
- index 更新の実際の entry 生成内容ではなく、呼び出し前後の制御だけを見たいときに読む。

## hash
- 074c05eda316a1630f6ec80d19eb4f28629daf8ae6c76e7da073b195e6dfa39a

# `test_packaged_import.py`

## Summary
- パッケージ配置での import 境界を確認するテスト群。`oracle` 側の正本定義が、配布形態でも `acp.builder` と `config.cmoc_config` から正しく参照・再公開されること、そしてレビュー用の oracle 生成処理が packaged layout でも期待どおりの参照先と出力スキーマを持つことを検証する。

## Read this when
- `oracle` 配下の実装を配布用レイアウトから import できるかを確認したいとき。
- `acp.builder` の公開 API が canonical 定義を再公開していることを確認したいとき。
- レビュー用 oracle のパラメータ生成が、正本仕様ファイルを入力に受け取り、生成物と prompt の契約を満たすかを確認したいとき。

## Do not read this when
- 通常のビジネスロジックや CLI 挙動を確認したいだけのとき。
- `oracle` の正本内容そのものの編集方針を知りたいときは、このテストではなく対応する `oracle` 側の定義を読むべき。
- packaged layout ではない通常の開発環境での import 解決だけを見たいときは、より直接のモジュール実装や公開定義を読むべき。

## hash
- 3678aacc11be328efaffe58f8f497cb99edf2a97ea9fb17b6040f973943ba350

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
- `review oracle` の反復実行で、finding の列挙・検証・マージが期待どおりに結び付くかを確認するテスト群。`sub_commands.review.oracle` の loop 全体と、finding merge の適用規則の境界を読む入口。
- 同じラウンドの challenger 理由が advocate に引き継がれるか、既存の challenger 理由が保持されるか、merge operation の再試行や失敗時の打ち切り条件がどう扱われるかを確認したいときに読む。

## Read this when
- `review oracle` の loop に関する振る舞い、finding の生成・統合・判定の流れ、または merge operation の妥当性検証を変更するとき。
- finding の target 共有、同一ラウンド内の reason の引き継ぎ、merge 失敗後の再試行回数やエラー条件を確認したいとき。

## Do not read this when
- `review oracle` のプロンプト文面や schema 定義そのものを変えたいときは、対応する実装側を先に読む。
- finding 以外の review フロー全般や別サブコマンドの挙動を追いたいときは、このテストではなく該当する上位の review 入口を読む。

## hash
- 2a19ab413b7f601aff51a07428afa466f23a03728b6a3b7f3a0192532fb61c23

# `test_review_oracle_report.py`

## Summary
- `review oracle` 系の回帰テスト群。`eval-oracle` から `review oracle` 実装へ委譲されること、レポートの Markdown 構成、集計結果、エラー時レポート出力を確認する。

## Read this when
- `review oracle` の CLI 出力、レポート生成、findings の採否・集計・並び順を変える。
- `eval-oracle` と `review oracle` の接続や、scope 引数の受け渡しを変える。
- 処理失敗時に error report を出す挙動を変える。

## Do not read this when
- `review oracle` の内部検出ロジックそのものを追うなら、実装側の `sub_commands/review/oracle` を先に読む。
- セッション作成や doctor の準備挙動だけを変えるなら、各サブコマンドの別テストを読む。
- `review oracle` 以外の review サブコマンドの仕様だけを確認したい場合は、このファイルは読まない。

## hash
- 405024b6366a9702605c60db7d900bb152d20e7e4a3b5c6dff07a05ecac2eb93

# `test_review_oracle_targets.py`

## Summary
- `review oracle` の対象解決と列挙ルールを検証するテスト群。`oracle_path` の `<work-root>` / `<oracle-root>` 解決、`full` / `session` スコープでの oracle 対象選定、ignored や symlink を含む oracle file の扱い、`AGENTS.md` / `INDEX.md` を除外する境界を確かめる。

## Read this when
- `review oracle` の対象ファイル選定やパス解決を変更する。
- oracle 配下の symlink, ignored file, tracked ignored file, `AGENTS.md`, `INDEX.md` の扱いを変える。
- session scope と full scope の対象数や評価数の差が変わる可能性がある。

## Do not read this when
- review 実行の見た目だけを変える。
- finding 本文の評価ロジックや report の文面だけを変える。
- oracle 以外のサブコマンドの対象列挙を直す。

## hash
- ae482ffa010320a92be4a6c65a7633c5a2efe074181a12b161d07b55b81928d9

# `test_review_oracle_worktree.py`

## Summary
- `review oracle` が worktree 選択、INDEX 統合、差分検査、競合解決をどう扱うかを検証するテスト群。
- セッション fork 後の review 実行で、linked worktree や preflight 由来の INDEX.md をどう反映するか、また未コミット差分や不要な worktree 生成をどう拒否するかを確認する。

## Read this when
- `review oracle` の CLI 挙動、worktree の選択条件、INDEX.md のマージや競合解決を変えるとき。
- review 実行前後の git 差分チェックや、linked worktree / session branch の扱いを確認したいとき。
- review で生成される report や worktree 配置が期待どおりかを確認したいとき。

## Do not read this when
- `review oracle` 以外の review ルートの一般的な実装を追いたいときは、対応する実装側を読む。
- INDEX 統合の具体処理だけを追いたいときは、このテストより `commons.indexing` 側を読む。
- セッション fork 自体の挙動だけを確認したいときは、このファイルではなく session 関連のテストを読む。

## hash
- d4a9017f429505064cc1704b3c60d331bcee268fe15119594e7b471e5b1bbc85

# `test_runtime_cli.py`

## Summary
- CLI の実行前後で発生する error 表示、ログ出力、preflight、shell completion の境界をまとめて検証するテスト群の入口。`runtime_cli` と `runtime_logging` の実行制御、`CmocError` の整形、`cmoc` 起動時の副作用有無を確認したいときに読む。

## Read this when
- CLI の失敗が stdout/stderr のどちらに出るべきかを確認したいとき。
- サブコマンドログの生成条件や、pre-log check / doctor preprocess の実行順を確認したいとき。
- work root 判定、detached HEAD の拒否、completion probe で副作用を起こさない条件を確認したいとき。
- `CmocError` の Markdown report 形式や duration 表示の仕様を確認したいとき。

## Do not read this when
- サブコマンド本体の業務ロジックを確認したいときは、各サブコマンド側のテストや実装を読む。
- git ignore の生成規則だけを追いたいときは、ignore 専用の実装・テストを読む。
- CLI 以外のログ形式や一般的なファイル管理の仕様を確認したいときは、別の対象を読む。

## hash
- 8d0de04a29fc2b06f1251abe217641042e438bb3a42d22b8f77ff91ced6c2d1b

# `test_runtime_codex_conflicts.py`

## Summary
- Codex の追加書き込み許可が、セッション join の conflict 解決で選ばれた対象に対してどの範囲まで有効になるかを検証するテスト群。 oracle 側の conflict resolution と file access rule に由来する境界を確認したいときに読む。

## Read this when
- session join の conflict 対象に対する write 可否、拒否条件、許可される境界を変える変更をする。
- 追加書き込み許可の判定が、oracle 配下・INDEX/AGENTS・実行時保護領域・通常の作業対象でどう振る舞うかを確認したい。
- Codex のオーバーライド引数生成や、session join conflict resolution に関する回帰をこの観点で追加・修正したい。

## Do not read this when
- session join の通常の参加パラメータだけを変更する場合は、より直接の session join パラメータ系テストを読む。
- write policy ではなく、indexing・review・apply の別経路の引数生成や CLI 挙動を調べたい場合はこのテスト群は読まない。
- oracle file 自体の仕様文を確認したいだけなら、このテストではなく根拠となる oracle 側の文書を読む。

## hash
- 059405185d07ce2025bb7804412cfbf6c8d7672a36a398f6b89dfe23b9d6d7c1

# `test_runtime_codex_permissions.py`

## Summary
- `build_codex_override_args` が生成する Codex のファイルアクセス制御を検証するテスト群。読み取り専用・oracle 寄り・realization write・repo write の各モードで、許可される書き込み先、拒否される領域、追加 writable path の扱いを確認する入口として読む。
- `memo` と `AGENTS.md` / `INDEX.md` 系の保護、`realization write` のトップレベル許可範囲、モード別の追加 writable path 拒否をまとめて扱うため、許可領域ルールを見直すときにこのファイルを読む。

## Read this when
- Codex の read/write 許可領域の判定条件を変えるとき。
- 追加 writable path の受理・拒否条件を確認したいとき。
- `memo` やルーティング系ファイルの保護範囲を検証したいとき。

## Do not read this when
- `build_codex_override_args` の内部実装を追いたいだけなら、まず `oracle/src/oracle/prompt_builder/parts/file_access_rule.py` 側の正本仕様を読む。
- Git の ignore 判定や repo 作成の補助実装を知りたいだけなら、このテストではなく補助関数側を読む。
- Codex のアクセス制御とは関係ない一般的な CLI 挙動を探しているなら、このファイルは読まなくてよい。

## hash
- c33add86a06d13258920e198e0f2d1e62881aaa46200ee39711c8f81763511f5

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
- `session fork`・`session join`・`session abandon` の外部挙動を、session 状態ファイル、branch 切り替え、linked worktree、preflight、cleanup、conflict 解消の観点でまとめて確認する回帰テスト群。
- session の生成・参加・放棄に加えて、dirty worktree 拒否、状態破損、session-id 衝突、削除失敗時の巻き戻し、join 後の残差検出や stdout/stderr の出し分けを読むときの入口。
- 関連する個別の session 実装や補助関数ではなく、CLI を通した end-to-end の期待結果を確認したい場合に読む。

## Read this when
- `session` サブコマンドのユーザー向け挙動を変える変更をしたとき。
- session state の生成・更新・破棄、branch 遷移、linked worktree 対応、dirty / corrupt 状態の拒否条件を確認したいとき。
- join の conflict 解消判定、残差検出、エラー出力先、cleanup 失敗時の復旧をまとめて追いたいとき。

## Do not read this when
- `session` 実装の内部分割や helper の責務だけを確認したいときは、対応する `src/sub_commands/session/*` を直接読む。
- 個別の state schema や preflight ルールの正本を確認したいだけなら、対応する oracle 側の文書や実装を読む。
- CLI 全体の共通テストや別サブコマンドの挙動を探したいだけなら、このファイルは範囲外。

## hash
- 876bc3bbff5180805f51e75f514a66e231624f06174194dd35369718de8b54b6

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
