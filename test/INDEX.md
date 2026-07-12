# `_apply_support.py`

## Summary
- セッション状態スナップショットから apply 用の worktree を復元する小さなテスト補助関数を置く。branch 名を state から取り出して `commons.runtime_apply` の worktree 解決へ渡す責務に絞る。

## Read this when
- apply セッションの state から worktree パスを復元する経路を確認したいとき。
- 状態の `apply` 部分に含まれる branch 名が、どの worktree 解決処理に渡されるべきかを追いたいとき。

## Do not read this when
- apply worktree の作成・更新・削除の本体仕様を知りたいときは、補助関数ではなく `commons.runtime_apply` 側を読む。
- session state の保存形式全体や他の state 項目を知りたいときは、この補助関数ではなく state 定義側を読む。

## hash
- 3b712042f89265b83678a441ea1303b97064d27293e5813fea29dffd686fb17e

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
- `test/_codex_support.py` は、Codex 実行系テストで共通に使う補助関数をまとめた支援モジュール。最小限の認証済み `CODEX_HOME`、Codex 用の標準 `AgentCallParameter`、CLI 引数の単一値抽出、重複する `--config` の検証用統合、Codex override の固定化が必要なテストを読む入口にする。

## Read this when
- 複数の Codex 実行テストで共通の `CODEX_HOME` 初期化が必要なとき。
- Codex テストで使う既定の `AgentCallParameter` を揃えたいとき。
- Codex CLI 引数の値抽出や `--config` の重複マージを検証したいとき。
- Codex 実行系テストで override 引数を固定して subprocess 関連の観測を安定させたいとき。

## Do not read this when
- 個別の Codex 実行挙動やエラー処理だけを確認したいときは、対応するテスト本体を直接読む。
- Codex 以外の共通 fixture や Git・CLI まわりの補助を探しているときは、別の支援モジュールを読む。
- このモジュールの補助関数を追加・変更しないなら、読む必要はない。

## hash
- f8acf74d3b454096b26cf1785aaca7caeb8577cb2421fb9249df26b6f3090d08

# `_command_support.py`

## Summary
- `test` 配下のテストで、`PATH` に置くための偽コマンドを Python スクリプトとして生成し、実行可能にする共通補助を提供する。
- 個別のテストが外部コマンドの代役を必要とする場合に読む。スクリプトの中身や検証ロジックではなく、まず実行可能なスタブを作る入口として使う。

## Read this when
- 外部コマンドを差し替えるテストを追加・修正するとき。
- テスト用の実行可能ファイルを、現在の Python で起動する形で作りたいとき。
- `PATH` 上の偽コマンドを共通の方法で用意したいとき。

## Do not read this when
- 単に既存テストの期待値や制御フローを確認したいだけのとき。
- 偽コマンドの作成ではなく、個別のテスト対象の振る舞いを読みたいときは、呼び出し元のテスト本文を直接読む。
- シェルスクリプトや永続的な補助ファイルの設計を探しているとき。

## hash
- 9a0b5eff08e904d2840baa3c3609ea94406365c198072ce39a0030cb76d283a0

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
- `test` 配下の Ollama まわりのテストで使う隔離済み支援コードをまとめた補助モジュール。 fake `systemctl` と fake `ollama`、および deterministic な runtime 差し替えを提供し、cmoc managed ollama の doctor と provider 結合を本物のサービスに触れずに検証したいときに読む。

## Read this when
- cmoc managed ollama のテストを、実機の Ollama や user systemd に依存せず deterministic に走らせたいとき。
- doctor や provider 連携のテストで、fake `HOME`、fake `PATH`、fake `ollama` 実行ファイル、fake `systemctl`、runtime monkeypatch を使う必要があるとき。
- `test_doctor_cli.py` や Ollama provider 系テストの共通準備を確認・変更したいとき。

## Do not read this when
- Ollama 以外の CLI テストや一般的な test fixture を探しているときは、各対象テスト本体や別の共通ヘルパーを先に読む。
- `cmoc managed ollama` の仕様そのもの、配置先、利用可能性保証の正本を確認したいときは、`<work-root>/oracle/doc/app_spec/cmoc_managed_ollama.md` を読む。
- Real Codex CLI の意味的な成功や出力品質を確認したいときは、この支援モジュールではなく、該当する結合テスト本体を読む。

## hash
- a9d7d262b807af663e577d9bca277a2f3f8b10b0b48cf630e0fb91c7bd1d4150

# `test_acp_builder_parameters.py`

## Summary
- ACP builder が生成する AgentCallParameter のモデル種別、reasoning effort、file access mode、preflight 設定、prompt 埋め込み、structured output schema 参照、互換 module の公開名を検証する realization test。
- apply fork、TUI resolve parameter、indexing index entry、review oracle、session join conflict resolution の builder 群について、oracle src の schema や builder と realization 側の出力が一致するかを確認する。

## Read this when
- ACP builder の parameter 生成ロジック、prompt 内容、schema path、schema 内容、公開 API を変更する。
- apply fork、TUI resolve parameter、indexing index entry、review oracle、session join conflict resolution の builder 実装や compatibility module を変更した後、既存挙動の期待値を確認する。
- oracle src の structured output schema を realization 側 builder が正しく参照しているかを調べる。
- builder が使う `<repo-root>`、`<work-root>`、`<oracle-root>` の prompt 表記や動的文字列の保持を検証したい。

## Do not read this when
- ACP builder 以外の CLI 実行、永続状態、path model、index 生成本文などを調べたい場合。
- structured output schema の正本内容そのものを確認したい場合は、対応する oracle src の schema を直接読む。
- 個別 builder の実装方針を調べたい場合は、対象 builder の realization implementation を直接読む。

## hash
- e41e29054eb05095e6cb2dd467f62c95dc60cab965c04be787f521fc3b903fc2

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
- `apply fork` CLI の回帰テスト群。セッション作成後の apply 実行、Codex ループ完了後の state/worktree 更新、linked worktree からの開始、doctor 前処理、config 読み込み失敗、.gitignore への反映、target 正規化の境界をまとめて確認する。

## Read this when
- `apply fork` の外部挙動を追加・変更したとき。
- 対象の正規化、gitignore 判定、state 遷移、report 生成順、linked worktree 由来の実行元解決を確認したいとき。
- doctor preflight や config 失敗時の開始前ガードを確認したいとき。

## Do not read this when
- `apply` 以外の CLI や session 生成の仕様だけを見たいときは、より直接のテスト群を読む。
- `apply fork` の実装詳細や helper の内部分解だけを知りたいときは、この回帰テストではなく対応する実装を読む。
- 別の target 正規化ルールだけを調べたいときは、個別の正規化テストを優先して読む。

## hash
- 2221d43445a276a4fbd0f343f27f2f1038ef6cca18a7711ef130b50428280961

# `test_apply_fork_report_cli.py`

## Summary
- `apply fork` の report 生成と再検査制御を CLI 経由で検証するテスト群。所見列挙、適用、変更要約、未収束/エラー時の report、変更ファイル再調査、rolling apply の対象選定までをまとめて見る入口に向く。

## Read this when
- `apply fork` の report 文面、収束判定、変更要約、session state 更新の振る舞いを確認したいとき。
- 所見が残る場合と、適用後に差分が消えた場合や新規ファイルが増えた場合の再調査ロジックを追いたいとき。
- apply fork の関連 builder が、packaged layout と src-only import の両方で正しく動くかを確認したいとき。

## Do not read this when
- `apply fork` 本体の実装や report 生成ロジックそのものを追いたいときは、対応する realization code を直接読むべきで、このテストファイルは優先対象ではない。
- `apply` 以外のサブコマンドや、apply fork 以外の report 形式だけを見たいとき。
- ルーティング文書だけが必要で、CLI 振る舞いの詳細な期待値までは不要なとき。

## hash
- 67ddab5270bdb242c28431b893028c35d616a147b24cd3c01ce4fcfd394c0724

# `test_apply_join_cli.py`

## Summary
- `apply join` の CLI 振る舞いを検証するテスト群。apply worktree の後片付け、session state 更新、結果 report 生成、dirty worktree や想定外差分、merge conflict の扱いをまとめて扱う。

## Read this when
- `apply join` の成功条件と失敗条件を確認したいとき。
- apply worktree の削除・branch 消去・state 更新・report 保存のどれかが変わるとき。
- 想定外差分の判定、`--force-resolve` の挙動、dirty worktree や merge conflict の検証を追加・修正するとき。

## Do not read this when
- `apply fork` 自体の挙動だけを確認したいときは、fork 側のテストを読む。
- CLI の個別コマンド定義や引数パースだけを追いたいときは、join 以外のコマンド実装を読む。
- 純粋な git 補助関数や worktree 構築の詳細だけを見たいときは、このファイルではなく補助モジュールを読む。

## hash
- de29b403faf93bf183628ce6b8c960ff9042f8ba7812f3438dc57c008ce99b91

# `test_basic_runtime.py`

## Summary
- cmoc の基礎 runtime 契約を横断して守る回帰テスト群の入口。root/work root 解決、config 既定値と JSON 順序、CLI のエラー表示、subcommand log、worktree/state 操作、FileAccessMode ごとの Codex override、binary 判定までをまとめて確認する。
- 個別サブコマンドの業務ロジックではなく、起動前提と共通 runtime 境界が壊れていないかを見たいときに読む。共通 fixture と root 状態をまたぐため、関連テストを一箇所で追いたい場合の起点になる。

## Read this when
- work root / repo root / linked worktree の扱い、CLI preflight、エラー報告、runtime state、Codex override、sandbox 権限、ignore 反映のどこかを変えた。
- config 既定値、`CmocError` の表示形式、subcommand ログ、`FileAccessMode` の権限制御、binary 判定の契約を確認したい。
- basic runtime の回帰として、複数の共通前提が同時に崩れていないかを一通り確認したい。

## Do not read this when
- 個別サブコマンドの入出力や業務フローだけを確認したい。より直接のサブコマンド別テストを読む。
- 実装の内部 helper 分割や共通化方針だけを見たい。ここは外部契約の回帰が主目的で、内部構造の根拠にはしない。
- runtime 境界に触れない単独機能の細部だけを追いたい。

## hash
- f27a262999f19ad07deb7dfc2f1fe24b606dd7fff36cfdf5f1df68451d7d49be

# `test_cli_tui.py`

## Summary
- `tui` サブコマンドの起動直前に行う前処理の外部挙動を検証するテスト群。編集対象が `tui` の引数解決、プロンプト生成、Codex 起動、ログ保存、リンク済み worktree での保存先分岐ならここを読む。
- `file_access_mode` などの解決結果が `tui` 実行にどう反映されるか、元プロンプトと完成プロンプトがどのログへ残るか、実行時に参照する追加ファイルの渡し方を確認したいときに読む。
- worktree 直下とリンク済み worktree の両方で `.cmoc` 配下の扱いを変える必要がある変更なら、関連するログ配置と `.gitignore` 更新の検証意図をこのテストから追う。

## Read this when
- `tui` コマンドの前処理、Codex 実行前のパラメータ解決、起動後のログ保存の仕様を変えるとき。
- 完成プロンプトの組み立て方、追加で読むファイル、`repo_write` と `readonly` の切り替えに影響する変更をするとき。
- linked worktree での `.cmoc` 配下の保存先や参照先を変えるとき。

## Do not read this when
- `tui` 以外のサブコマンドだけを変更するとき。
- `run_codex_exec` や `run_codex_tui` の内部実装そのものを確認したいときは、まずそれぞれの実装側を読むべきで、このテストファイルは後回しでよい。
- 一般的な git helper、コマンド実行 helper、プロンプト部品の共通ロジックだけを追いたいときは、対応する実装や共通モジュールを直接読む方がよい。

## hash
- 221ccd1aebb345cdfde3f4191aca42c6d6a26d314178305c263184feae908adc

# `test_codex_runtime_errors.py`

## Summary
- Codex CLI 呼び出しの失敗処理を検証するテスト。`codex` 実行自体が見つからない場合に、`run_codex_exec` と `run_codex_tui` が同じ例外と監査ログを出すことを確認する。

## Read this when
- Codex 起動失敗時の例外メッセージや `codex_call` ログの記録内容を確認したいとき。
- `exec` と `tui` の両経路で、CLI 不在を同じように扱うべきかを確認したいとき。
- 外部 `codex` コマンドが起動できない異常系のテスト追加・修正をするとき。

## Do not read this when
- Codex の通常実行、引数組み立て、成功時の挙動を見たいとき。
- 別の失敗要因の扱いを確認したいときは、より直接のエラーテストを読むべきで、このテストは読まなくてよい。
- ログ形式全体やサブコマンド実行基盤の仕様を把握したいだけのとき。

## hash
- 688efb4449733c71d7cc6efba4f59ff9c4ce24947e6cbc607e708b37922e990c

# `test_codex_runtime_exec.py`

## Summary
- `run_codex_exec` とそれに関連する実行支援の挙動を確認する統合テスト群。Codex 実行時の引数注入、モデル/プロバイダの上書き、作業ディレクトリ、スキーマ保存先、managed Ollama 前提、`.agents` を開かない制約など、実行経路の外部挙動をまとめて検証したいときに読む。
- 個別の内部 helper ではなく、実際の `codex` 起動結果・ログ・生成物を使って「実行時に何が保証されるか」を見たいときに進む。純粋な `CmocConfig` の定義や Codex 仕様そのものを読む目的なら、より直接の定義元を当たる。

## Read this when
- `run_codex_exec` の CLI 引数や override config の組み立て結果を確認したいとき
- read-only / repo-write / pure oracle read の各モードで、`codex` 起動にどう反映されるかを確かめたいとき
- linked worktree での `cwd` や schema 保存先など、実行時のパス解決を確認したいとき
- managed Ollama 前提の実行や doctor 前処理との接続を追いたいとき

## Do not read this when
- `CmocConfig` や `CodexModelSpec` の定義そのものを知りたいだけのとき
- Codex CLI そのものの一般仕様やモデル仕様を読みたいだけのとき
- ファイルシステムや git 周りの実装詳細ではなく、別のサブコマンドや設定層の挙動を追いたいとき

## hash
- 462cb7e9f3e3531ceebcc73b5ecb4b5a0abb0d338e83129849f769384e114793

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行前の `CODEX_HOME` 解決と preflight 検証を扱うテスト群。未設定時の既定値、相対値の扱い、`auth.json` を含む失敗条件を確認したいときに読む。
- Codex 呼び出し前に失敗すべき境界だけを固定する。`CODEX_HOME` の環境変数をそのまま渡す条件と、実行時に解決した home を使う条件の両方を確認する。

## Read this when
- Codex home の既定値解決や、設定済み `CODEX_HOME` をどう扱うかを確認したいとき。
- `CODEX_HOME` が存在しない、ディレクトリでない、`auth.json` がない場合の事前失敗条件を確認したいとき。
- Codex 実行前に、環境変数値を保持したまま実行時解決だけ行う挙動を確認したいとき。

## Do not read this when
- Codex exec の再試行、quota 待機、Structured Output 検証を追いたいときは、exec 実行制御のテストへ進む。
- 一般的なエラーレポート整形や CLI 全体の例外処理を追いたいときは、別の error handling 系を読む。

## hash
- be07e773cef9149fff068e12507ace8b0c661f5706ee53baea1082f7ebb14a6d

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex quota 超過後の待機・再試行・resume 復帰を検証するテストで、単発失敗時の挙動だけでなく、probe の実行条件、resume token の復元、call log とサブコマンドログの記録、CODEX_HOME/CWD の扱いまで含めて確認する。
- 同じ retry 状態機械に関わる外部挙動を一箇所で追うための集約テストとして読む。quota 待機の分岐、probe 失敗、上限到達、並列実行時の代表 probe 制御までを確認したいときに進む。

## Read this when
- `run_codex_exec` の quota 超過後の制御フローを変える、またはその回帰を確認したいとき。
- probe 用の `AgentCallParameter` がどの制約で作られるか、resume token がどのログから復元されるかを確認したいとき。
- call log、stdout/output 生成物、サブコマンドログ、`CODEX_HOME` と `cwd` の対応をまとめて追いたいとき。
- quota 待機中の並列呼び出しが単一の代表 probe に収束するか、probe 失敗時に即失敗するかを確認したいとき。

## Do not read this when
- Codex の通常実行だけを確認したいときは、quota retry 以外の実行テストを読む方が直接的。
- probe パラメータ生成の定義そのものを見たいだけなら、対応する oracle 側の定義を先に読む方がよい。
- CLI の引数定義や一般的なログ形式だけを探しているなら、このファイルは粒度が細かすぎる。

## hash
- 0ce86c8afb3efbe485954bf033293d04311767034a7a2b63afa0b6a3849e852f

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
- `doctor` CLI と、その事前処理が Git 状態修復・`.cmoc` 設定生成・managed Ollama 起動をどう結び付けるかを確認するための統合テスト群。`run_doctor`/`run_doctor_preprocess` の外部挙動、作成されるファイル、Git の追跡・ステージ状態、worktree 切替時の扱いをまとめて見る入口。
- 既定設定の同期、既存の人間編集を上書きしないこと、`.cmoc/local` の未追跡化、`.agents/.gitkeep` の再生成、既存の staged change を壊さないことなど、doctor の境界条件を検証する。
- `doctor` の実装本体や config/ollama/git 支援関数の詳細を追う前に、まずこのテストで期待されるユーザー向け挙動を把握する位置づけ。

## Read this when
- `doctor`/`dector` コマンドの挙動を変える可能性があるとき。
- `.gitignore`、`.agents`、`.cmoc/config.json`、`.cmoc/local` の生成・修復・追跡状態を変えるとき。
- managed Ollama の起動やモデル選択の処理が、doctor の前処理からどう呼ばれるかを確認したいとき。
- linked worktree で doctor を実行した場合の参照先や作業対象を確認したいとき。

## Do not read this when
- CLI の引数定義やコマンド登録だけを確認したいときは、実装側の CLI 入口を先に読む。
- `doctor` 以外のサブコマンドの仕様を調べたいとき。
- `git` や `ollama` の単体ラッパーの細部だけが目的なら、それぞれの支援モジュールを直接読む。
- 設定スキーマ全体の定義を見たいだけなら、この統合テストではなく config 定義の本文を読む。

## hash
- 6f274f473e716490c64cc395049476b960f76cec7d5447c0d22b014c3f62630e

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

# `test_runtime_ollama.py`

## Summary
- `commons.runtime_ollama` の Ollama 起動・サービス維持・GPU 利用確認に関する振る舞いを検証するテスト群。サービス再修復の再起動条件、HTTP 到達確認の失敗扱い、リスナーが期待するサービスプロセスかの判定、モデル読み込み後の確認順序、GPU 推論可否の判定を扱う。

## Read this when
- Ollama の常駐サービスやモデルロードの判定条件を変えるとき。
- サービス再作成、再起動、接続確認、GPU 確認のどの失敗をエラーにするかを確認したいとき。
- `commons.runtime_ollama` の外部挙動に対する回帰テストを追加・修正したいとき。

## Do not read this when
- Ollama 以外の runtime 実装や別の service 管理ロジックを変更するとき。
- `runtime_ollama` の内部 helper の分割や実装手順だけを見直したいときは、まず該当する実装本体を読むべきとき。
- GPU 判定や HTTP 応答の詳細仕様ではなく、別のコマンドや別サービスのテストを探しているとき。

## hash
- 859258328f9114eeba1966d058499e06f871e8175c0599d7786aad71c76419b0

# `test_session_cli.py`

## Summary
- `session fork` / `join` / `abandon` の外部挙動回帰をまとめて確認する入口。session branch と session state の遷移、linked worktree、state cleanup、dirty worktree 拒否、conflict 解消の境界を扱うテスト群へ進むときに読む。
- 同じ session CLI でも、個別の内部 helper の単体確認や別サブコマンドの挙動確認が目的なら優先しない。ここは CLI 全体の状態遷移と副作用を観測する回帰テストに絞る。

## Read this when
- session CLI の `fork` / `join` / `abandon` の期待挙動を確認したい。
- session state ファイル、session branch、linked worktree、preprocess、cleanup の関係をまとめて追いたい。
- dirty worktree 拒否、state corruption、conflict resolution、branch deletion 可否の回帰を見たい。

## Do not read this when
- 個別の実装 helper の詳細を追いたいだけなら、対応する実装モジュールを直接読む。
- session 以外のサブコマンドや一般的な CLI 挙動を確認したいだけなら、このテスト群は読まない。
- このファイルは session CLI の統合回帰に限定されるので、状態遷移と関係しない単発のユーティリティ確認には使わない。

## hash
- 6284eb3df086367bf4390b7c46db8f3e9436a778fdfa39466397f22c736dd787

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
