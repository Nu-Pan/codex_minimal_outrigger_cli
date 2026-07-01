# `_support.py`

## Summary
- CLI テストで使う共通補助関数群。最小構成の Git リポジトリ作成、ブランチ状態確認、Codex ホームのテスト用設定、Codex profile 生成の差し替え、偽の Python 実行ファイル作成、apply 用 worktree path 解決をまとめて提供する。
- 外部コマンドとしての Git と Codex 実行制御を伴うテストの前提準備を集約し、個別テストが fixture 作成や monkeypatch の詳細を重複して持たないための入口になる。

## Read this when
- CLI テストで一時 Git リポジトリ、初期 commit、oracle 配下の最小ファイル、追跡済みかつ ignore 対象の oracle ファイルを用意する方法を確認したいとき。
- Codex CLI 実行を伴うテストで、認証済みの最小 CODEX_HOME や profile 生成差し替えの仕組みを使う、または変更するとき。
- テスト内で現在の Git ブランチ名、Git コマンド実行結果、apply 状態から導かれる worktree path を検証する補助処理を探すとき。
- 外部コマンドの代替として実行可能な Python スクリプトをテスト中に生成する必要があるとき。

## Do not read this when
- 個別サブコマンドの期待挙動、CLI 出力、終了コード、状態ファイルの仕様を確認したいだけなら、該当するテスト本文または実装を直接読む。
- pytest の個別ケースやアサーション内容を探しているだけなら、この共通補助関数群ではなく対象機能のテストを読む。
- Codex profile 生成や apply worktree 解決の本体実装を変更する場合は、ここではなく実装側の該当モジュールを読む。
- oracle file や realization file の正本上の定義・標準を確認したい場合は、このテスト補助ではなく oracle 側の文書を読む。

## hash
- 54cf181de55105f9065ad7f515d614e2705529029548b38b874d2326362e0b59

# `test_acp_builder_parameters.py`

## Summary
- ACP builder が生成する AgentCallParameter の model/reasoning/file access mode、prompt へ埋め込まれる root 表記・標準文書・動的文字列、structured output schema 参照が oracle source と一致することを検証するテスト群。
- apply fork、TUI parameter 解決、indexing index entry、oracle review、session join conflict resolution、file access rule violation recovery の builder 挙動を横断的に扱う。

## Read this when
- ACP builder の parameter 生成結果、prompt 内容、structured_output_schema_path、または schema enum/required/additionalProperties の期待値を変更する。
- apply fork、TUI resolve parameter、indexing index entry、oracle review finding 系、session join conflict resolution、file access rule violation recovery の builder 実装を変更した後に、既存の外部挙動テストを確認する。
- oracle source 側の ACP builder schema を変更し、realization 側 builder が同じ schema を参照または生成しているか確認する。
- prompt 内の `<repo-root>`、`<work-root>`、`<oracle-root>`、`<oracle_root>` などの placeholder 表記や、動的入力文字列の保持挙動を変更する。

## Do not read this when
- 個別 builder の内部 helper 分割や import 整理だけを調べたい場合は、対象 builder 実装を先に読む。
- ACP builder 以外の CLI 挙動、永続状態、git 操作、一般的な path model を調べる場合は、それぞれの対象テストまたは実装を読む。
- oracle file の仕様本文や schema の正本内容を確認したい場合は、oracle 側の該当 doc/src を直接読む。

## hash
- 260bb17a591a3bfe649fa1f73ee13ca6ff6dff11505bfd4e13cc7742e3617f0a

# `test_apply_abandon_cli.py`

## Summary
- active apply run を CLI 経由で破棄する外部挙動を検証する realization test。worktree、branch、session state の cleanup、cleanup 対象欠落時の警告、running process 停止、実行位置判定、linked session worktree との境界条件を同じ abandon 操作の文脈で扱う。
- apply process identity の読み取り、child process group を含む停止順序、PID reuse や race 済み終了の扱いなど、abandon 前処理として必要な process 停止ロジックの制御境界も検証する。
- 16,000 文字を超えるが、active apply run の破棄という単一責務に閉じ、同じ state fixture と境界条件を共有するため、分割せず読み取り文脈を一箇所に保っている。

## Read this when
- apply abandon の CLI 挙動、出力、終了コード、state 遷移、apply worktree と apply branch の削除を変更または確認するとき。
- running apply を abandon する際の process identity 読み取り、tracked child process group の停止、PID reuse 防止、終了 race の扱いを変更または確認するとき。
- apply worktree 内、linked session worktree、linked apply worktree、stale apply branch など、abandon 実行位置ごとの許可・拒否条件を調べるとき。
- cleanup 対象がすでに存在しない場合の警告成功、または破損 state や process identity 欠落時に cleanup 前で拒否する挙動を確認するとき。

## Do not read this when
- apply abandon 以外の apply サブコマンドの通常フローや Codex 実行結果の品質を調べたいとき。
- session fork、init、git helper、runner などの共通 fixture や補助 API 自体の実装を確認したいとき。
- oracle file の正本仕様や実装標準を確認したいとき。
- active apply run の破棄に関係しない一般的な worktree、branch、session state の挙動を調べたいとき。

## hash
- ec0375e8de29f038d1dc8b4010eae864fadb5ba208f43ab7385d198d6ddc6158

# `test_apply_fork_cli.py`

## Summary
- `apply fork` CLI の realization test。Codex 実行を fake 化し、apply run の作成・完了、session state 更新、apply worktree 配置、linked worktree 起点の branch/HEAD、`.gitignore` 保持・編集、設定読み込み失敗時の非開始、apply 対象 path の正規化を検証する。

## Read this when
- `apply fork` の外部挙動、state 遷移、apply branch/worktree 作成、Codex 呼び出しループに関するテストを確認・変更する時。
- linked worktree 上で開始した session から apply run を作る挙動や、apply branch の開始 commit を確認する時。
- `apply fork` が session 側 `.gitignore` を汚さずに `.cmoc` ignore を確保する挙動、または apply branch 側で `.gitignore` を編集対象にできる挙動を確認する時。
- cmoc config の読み込み失敗時に apply run の branch/state/pid を作らないエラー処理を確認する時。
- apply 対象候補から root 直下の `memo`、管理 path、`INDEX.md`、`AGENTS.md` などを除外する正規化ルールの realization test を確認する時。

## Do not read this when
- `apply fork` の実装詳細だけを変更したく、外部挙動テストや期待 state を確認する必要がない時。
- apply 以外の session fork、init、設定ファイル処理、worktree helper の単体挙動を直接確認したい時。
- oracle file 側の正本仕様断片を確認・編集したい時。
- Codex CLI や LLM の実出力品質そのものを検証したい時。

## hash
- 118139392a3180ae63f3d170e94c0ff10a2e3d6df7ac0aabd694654e2e041b21

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 経由の制御を検証するテスト。所見列挙、所見適用、commit、変更要約、report 生成、session state 更新までの一連の挙動を扱う。
- apply fork report の収束、未収束、error、変更ファイル再調査、rolling fork の観測結果を、同じ loop と report schema に対する期待値としてまとめて確認する。
- apply fork 用 ACP builder の import 可能性、prompt 内容、oracle schema 参照も検証し、packaged layout や src のみの PYTHONPATH で動くことを確認する。

## Read this when
- apply fork の report 出力、exit code、収束・未収束・error の扱いを変更または確認したいとき。
- apply fork が所見適用後の変更ファイルを再調査する制御や、新規ディレクトリ配下の展開を確認したいとき。
- apply fork の commit 作成、変更要約、未追跡ファイルを含む差分要約、file access rule violation recovery の挙動を確認したいとき。
- rolling apply fork が前回 apply join 後の変更だけを対象にする session state 更新を確認したいとき。
- apply fork 用の change summary、file finding enumeration、finding application の ACP builder、prompt、structured output schema 参照を変更するとき。

## Do not read this when
- apply fork の内部実装だけを探している場合は、まず該当する実装モジュールを読む。
- apply join、session fork、init など apply fork の report loop 以外の CLI 挙動を確認したいだけなら、それぞれの専用テストを読む。
- Codex 実行基盤全般や ACP builder 全般の共通仕様を確認したい場合は、より直接その責務を持つ実装またはテストを読む。

## hash
- bc56550a489112289f5c1c97e0f3db300afbbff8dd00ab4ded38ee8d30310e4f

# `test_apply_join_cli.py`

## Summary
- apply run を session へ join する CLI 外部挙動を検証する realization test。join 成功時の merge、state 更新、report 生成、apply worktree・branch の cleanup と、dirty worktree、stale apply branch、想定外差分、merge conflict などの拒否・中止条件を同じ fixture と git 状態の文脈で扱う。
- 16,000 文字を超えるが、apply join の成功条件と拒否条件を一箇所で確認する凝集性を優先しているテスト群であり、worktree cleanup、branch cleanup、state 遷移、report、差分分類、conflict 処理を横断して読む入口になる。

## Read this when
- apply join の CLI 挙動、終了コード、標準出力、report 生成、state 更新、cleanup の期待値を確認・変更したいとき。
- apply worktree から join した場合、session worktree から join した場合、linked session worktree から join した場合の作業ディレクトリ別挙動を確認したいとき。
- dirty apply worktree、stale apply branch、想定外の apply 差分、削除パス、rename target、root memo、.gitignore 変更、merge conflict の扱いを検証するテストを探しているとき。
- apply join の差分分類 helper や conflict 解決後継続の制御が、CLI 経由の外部挙動としてどう期待されているかを確認したいとき。

## Do not read this when
- apply fork、session fork、init など join 以外のサブコマンド単体の挙動を確認したいだけのとき。
- apply join の実装内部構造、関数分割、git 操作 helper の実装詳細を直接変更したいときは、対応する実装側を先に読む。
- Codex 実行結果そのものや LLM 出力品質を検証したいとき。この対象では Codex 実行は fake に置き換え、join 後の外部副作用を検証している。
- 一般的な test fixture、repo 作成 helper、runner helper の仕様を確認したいだけのときは、共通 support 側を読む。

## hash
- db9c00e9643569b5c9ef444fa5ae130d8a8a2e52bb7e57173dee38a52227aa77

# `test_basic_runtime.py`

## Summary
- cmoc の基礎 runtime 契約を横断的に検証する realization test。root placeholder 解決、worktree 境界、config 既定値と検証、CmocError の Markdown 表示、CLI error の stdout 化、subcommand log、`.cmoc` ignore、FileAccessMode 変換、Codex sandbox profile、binary 判定、branch session state など、個別サブコマンドより下位の共通実行前提をまとめて扱う。

## Read this when
- runtime の共通契約や実行前提に関わる挙動を変更する。
- root 解決、repo root と work/run root、linked worktree、run worktree 作成・削除の安全条件を確認する。
- CmocConfig、config_from_dict、model class、reasoning effort、FileAccessMode の値や変換を変更する。
- CmocError、render_error、CLI parse error、stdout/stderr の error report 表示を変更する。
- Codex profile の sandbox mode、cwd、writable_roots、extra writable paths、session join conflict 用の書き込み許可を変更する。
- subcommand log、completion probe、preflight、副作用抑制、`.cmoc` ignore、binary 判定、branch session state の基本挙動を確認する。

## Do not read this when
- 特定サブコマンド固有の業務ロジックだけを調べる場合。
- runtime 境界に関係しない UI 文言、個別 prompt、個別 agent call の内容だけを変更する場合。
- oracle file の正本仕様そのものを確認・編集したい場合。
- 単一 helper の内部実装だけを調べれば足り、共通 runtime 契約の回帰確認が不要な場合。

## hash
- 2b7d1136ff001240378c1b28c9e114cef0afdabba1b236597a7fb1782d49d58c

# `test_cli_init_tui.py`

## Summary
- init と TUI 起動直前の CLI 前処理を外部挙動として検証するテスト。cmoc 初期化、.cmoc ignore、既存差分保護、設定既定値同期、linked worktree、Markdown prompt 整形、Codex TUI 起動 parameter 構築を同じ利用開始境界の回帰として扱う。

## Read this when
- `init` の git ignore 更新、.cmoc 配下の追跡解除、cleanup commit、既存 staged/unstaged 差分保護を変更・確認する。
- 初期設定ファイルの既定値生成、既存 human value を保持した設定同期、sub_command log の記録内容を変更・確認する。
- linked worktree での init/TUI の root/cwd、ignore、config/log/schema 保存先、git status への影響を確認する。
- TUI 起動前の editor 実行、HTML comment 除去、complete prompt 保存、resolve parameter の解釈、AgentCallParameter 構築を変更・確認する。

## Do not read this when
- 個別サブコマンドの本体処理や agent call 実行結果を確認したいだけで、init または TUI 起動前処理に関係しない。
- 設定値の定義元や prompt 構築仕様そのものを確認したい場合は、対応する oracle または実装側を直接読む。
- INDEX.md 生成規則や oracle/realization 標準の内容を確認したいだけで、この CLI 境界の回帰テストを見ない。

## hash
- b78e4d3a16f472b8ec6f743589c4e5f1fc8915248148f5d95c2f1a348d42db08

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI/TUI 呼び出しランタイムの実行制御を検証するテスト。Codex subprocess の process group 分離、apply tracking 環境変数の遮断、profile 生成、sandbox 設定、cwd 選択、schema 状態保存先、ファイルアクセス違反の扱い、extra read path の事前検査、非ゼロ終了や CLI 欠如時のエラー報告を扱う。
- `run_codex_exec` と `run_codex_tui` の外部プロセス起動まわりを、実 Codex CLI ではなく一時ディレクトリ上の stub 実行ファイルで検証する入口。

## Read this when
- Codex CLI/TUI 起動時の argv、cwd、stdin、profile、sandbox writable_roots、出力ファイル、call log の期待挙動を確認・変更するとき。
- `FileAccessMode` ごとの Codex 実行環境、特に `REPO_WRITE`、`REALIZATION_WRITE`、`PURE_ORACLE_READ` の差分を確認するとき。
- `.cmoc` worktree 配下で schema 状態や TUI prompt log をどこに置くか、linked worktree からの実行をどう扱うかを確認するとき。
- apply process tracking、process group、継承された tracking env の無効化など、Codex subprocess の低レベル実行制御を変更するとき。
- Codex 実行後の禁止領域 diff、extra read path、Codex CLI の非ゼロ終了・未インストール時の `CmocError` 表示を変更するとき。

## Do not read this when
- Codex runtime 以外の CLI コマンド仕様や oracle 文書生成のテストを探しているとき。
- 外部プロセス起動を伴わない pure path helper、設定 object 単体、git helper 単体の挙動だけを確認したいとき。
- 実 Codex CLI の出力品質や LLM 応答内容そのものを検証したいとき。
- テスト支援関数の実装詳細を確認したいだけなら、支援 module を直接読む方がよい。

## hash
- 1d70af1bb005d35891bef92b758d021cf6fd40404f02fb1337a40c510c714200

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行時の Codex home 解決と事前検証を扱う realization test。環境変数未設定時の既定値、相対値の解決基準、プロファイル配置、呼び出しログへの記録、Codex CLI 起動前に失敗すべき認証環境不備を検証する。

## Read this when
- Codex CLI 呼び出しに渡す CODEX_HOME、プロファイル、作業ディレクトリ、呼び出しログの挙動を変更または確認したいとき。
- Codex home が存在しない、ディレクトリではない、認証情報がない場合のエラー文言や失敗タイミングを変更または確認したいとき。
- file access mode によって Codex CLI の実行 cwd が変わるケースで、相対 CODEX_HOME の解決挙動を確認したいとき。

## Do not read this when
- Codex CLI の標準出力イベント処理、capacity wait、一般的な agent call 結果処理だけを確認したいとき。
- Codex home ではなく、repository path、oracle path、run root、work root の一般的なパスモデルを確認したいとき。
- CLI 利用者向けコマンド定義や設定ファイル全体の schema を確認したいとき。

## hash
- b92995fbdd0a93c847ae8a31d4ea6534df7c8b4185810379c129ee1b456241d7

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex quota exceeded 後に、quota availability probe、resume token、再実行、call log、subcommand log、CODEX_HOME/cwd が同じ retry 状態機械として期待どおり連動することを検証する realization test。
- quota 待機から復帰する Codex exec の外部挙動を、単一呼び出し、resume token あり/なし、probe 失敗、並列呼び出し時の代表 probe 共有まで含めて確認する。

## Read this when
- Codex exec が quota exceeded を返した後の polling、probe、resume、rerun の挙動を変更または調査するとき。
- quota retry 中に記録される call log、subcommand log、prompt/stdout/stderr/output の保存先や status/purpose の期待値を確認するとき。
- CODEX_HOME が相対パスの場合の cwd 解決、PURE_ORACLE_READ 時の実行ディレクトリ、または probe が使う profile/argv/stdin を確認するとき。
- 複数の Codex exec が同時に quota exceeded になった場合に、probe を代表 1 回に共有し、各呼び出しが復帰または失敗する制御を確認するとき。

## Do not read this when
- 通常の成功する Codex exec 呼び出しだけを調べたいとき。
- quota retry と無関係な CLI 引数生成、設定読み込み、リポジトリ作成 fixture の詳細を調べたいとき。
- Codex CLI や LLM の出力品質そのものを評価したいとき。
- oracle file の正本仕様を確認したいとき。

## hash
- 0a30f0b70db0ab7bf8389f4f98b8e15ac849abe651f620a206f7d85d4c7fec75

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーの retry 挙動を検証する pytest テスト。構造化出力の schema 不一致・JSON 解析失敗・capacity エラー時に再試行し、call log と subcommand log に期待する状態が記録されることを確認する。
- stdout JSONL 以外に出た capacity/quota 風の文字列を再試行条件として扱わず、通常の CLI 失敗として扱う境界も検証する。

## Read this when
- `run_codex_exec` の再試行条件、構造化出力検証、capacity/quota 判定、call log 記録、subcommand log の `codex_call` event を変更する時。
- Codex CLI の fake executable を使った retry 系テストの既存パターンを確認したい時。
- `AgentCallParameter`、`CmocConfig`、`SubcommandLogger` と `run_codex_exec` の結合テストを追加・修正する時。

## Do not read this when
- Codex CLI 呼び出しの通常成功系や引数組み立てだけを確認したい時は、より直接その挙動を扱う runtime テストを読む。
- repository fixture、Codex home setup、fake executable 作成 helper の実装を確認したい時は、テスト支援モジュールを直接読む。
- oracle file や INDEX.md の生成仕様を確認したい時は、該当する oracle doc または生成処理のテストを読む。

## hash
- 4756b71f801ab3d2753b1ac5ab73749a3bb338f0e6f7a177a3daa1c7451cab3b

# `test_indexing_cli.py`

## Summary
- indexing preflight と indexing subcommand が routing document を生成・更新・commit する CLI 境界の回帰テストをまとめる realization test。
- INDEX.md conflict 解決、未初期化・dirty worktree の拒否、linked worktree 対象化、repo config 利用、fresh hash による再生成スキップ、index path だけの commit を外部挙動として検証する。
- INDEX.md エントリーの schema 検証、 malformed entry の再生成、空ディレクトリ・memo 除外境界・symlink cycle・並列生成など、routing 更新ワークフローの観測点を扱う。

## Read this when
- indexing CLI の実行条件、失敗時メッセージ、commit 条件、linked worktree での対象 root 判定を変更・確認するとき。
- INDEX.md の生成・更新、hash 再利用、entry schema validation、malformed entry 再生成、空ディレクトリへの INDEX.md 配置を変更・確認するとき。
- indexing preflight が通常の indexing subcommand と異なり、既存の非 INDEX.md 差分を許容しつつ INDEX.md だけ commit する挙動を確認するとき。
- routing document 更新処理の並列化、memo ディレクトリの扱い、directory symlink cycle の除外を変更・確認するとき。
- apply 側の INDEX.md conflict 解決が conflict 中の INDEX.md を削除して merge commit を完了する挙動を確認するとき。

## Do not read this when
- 個別の indexing 実装 helper の内部アルゴリズムだけを調べたい場合は、実装モジュールを直接読む方が適切。
- Codex が生成する自然言語エントリーの品質や内容そのものを評価したい場合は、このテストではなく生成プロンプトや schema 側を確認する。
- indexing 以外の CLI subcommand、通常 apply workflow、設定ファイル全般の仕様を調べる場合は、該当する実装・テストへ進む方が適切。

## hash
- ba84ba2a5f8fac06dd16494e65b04728e1b72568d45ca51a5e25aa2604e2bf43

# `test_indexing_preflight.py`

## Summary
- Codex 実行前の indexing preflight が、exec/TUI 呼び出し前に INDEX.md 更新を実行し、必要な commit と worktree 選択を行うことを検証する realization test。
- repository lock 待機、index entry 生成や conflict resolution 用途で preflight を skip する条件も扱う。

## Read this when
- Codex 呼び出し前に indexing preflight が走る順序、commit、clean worktree を確認・変更する。
- cwd が別 worktree 配下にある場合、root ではなく cwd 側 worktree を index 更新対象にする挙動を確認・変更する。
- indexing lock の排他待機や、特定 purpose で preflight を skip する条件を確認・変更する。

## Do not read this when
- INDEX.md の本文生成ロジックやエントリー内容の仕様を確認したい場合。
- Codex 実行ラッパーではなく、個別の git helper や repository fixture の詳細を確認したい場合。
- oracle file の正本仕様や INDEX.md ルーティング規則そのものを確認したい場合。

## hash
- 5549e75d6493464e59f5f4cb68232c1fbd9fc7d03b85ee5f6cb6ea3ad4e04099

# `test_packaged_import.py`

## Summary
- packaged layout から review oracle enumerate builder を import できることと、packaging 設定が oracle package を期待した配置で公開していることを検証するテスト。
- 一時的な import 環境を組み立て、builder が schema path と prompt を正しく返せることをサブプロセスで確認する。

## Read this when
- packaged layout、setuptools package-dir、oracle package の import 境界を変更する。
- review oracle enumerate builder の依存関係、schema 参照、prompt 組み立てが配布後の import 環境で壊れていないか確認する。
- oracle src と realization src の配置分離に関わるテスト失敗を調査する。

## Do not read this when
- builder の prompt 本文や schema 内容そのものの詳細仕様を確認したい場合。
- 通常の CLI 動作、入出力、状態管理など packaged import 境界と無関係な挙動を調査する場合。
- 単体の helper ロジックを直接検証するテストを探している場合。

## hash
- cccc21d8925cdcc0798ceaddea1bf75e25fbadf671e8b6ee5e76317db75fb27f

# `test_prompt_parts.py`

## Summary
- 標準 prompt parts と complete prompt の組み立てに関する realization test。各標準文書ビルダーが主要な要求語句を markdown に含めること、complete prompt が指定された標準・file access rule・root token 表記を意図どおり含める／省くことを検証する。

## Read this when
- prompt builder の標準文書生成、complete prompt の構成、file access mode ごとの読み書きルール出力を変更する。
- oracle standard、realization standard、review oracle standard、apply review standard、index entry standard、routing rule の prompt への注入条件やレンダリング内容を確認する。
- `<work-root>` などの root token、補助 prompt、コードブロック内文字列が complete prompt で保持される挙動を検証する。

## Do not read this when
- 個別標準文書の正本内容そのものを確認したい場合は、対応する oracle 側の prompt part 定義を読む。
- prompt rendering の外部挙動ではなく、StructDoc や markdown renderer の低レベルな構造変換だけを調べる。
- CLI コマンド実行、git 操作、ファイル探索など prompt builder 以外の機能を変更する。

## hash
- 4ad1f3518e86aefeb906a6fa8b1a6537ec1ae2ca05cc46cf1e42c1fc75a1e104

# `test_review_oracle_cli.py`

## Summary
- review oracle コマンドの外部挙動を CLI 経由で検証する realization test。report の構成と集計、対象 oracle file の列挙条件、session/full scope、linked worktree、所見の列挙・検証・judge・merge、review 中に許される INDEX.md 変更と許されない差分、処理失敗時の error report を扱う。
- 所見評価 loop の fake Codex 応答と report 文脈を共有するため、oracle review run 全体の制御と出力を一箇所で確認する入口になる。

## Read this when
- review oracle コマンドの report 出力、終了コード、標準出力、集計値、section 順序、accepted/rejected finding の表示を変更・確認する。
- review oracle の対象 oracle file の選択条件を変更・確認する。特に AGENTS.md/INDEX.md の除外、git ignore された tracked file、未追跡 ignored file、symlink、memo 配下との境界を扱う。
- review oracle の session scope と full scope、短縮 option、対象 0 件時の挙動を変更・確認する。
- review oracle が linked worktree 上の session branch と oracle を扱う挙動、review 用 worktree、fork commit、join commit を変更・確認する。
- finding の enumerate loop、validate challenger/advocate、judge、merge operation の契約、loop 上限、対象別 prompt に渡す既存 finding 文脈を変更・確認する。
- review oracle 実行中に生成された INDEX.md 変更の取り込み、INDEX.md conflict 解決、INDEX.md 以外の差分拒否を変更・確認する。
- review oracle 処理途中の例外で error report を残す挙動を変更・確認する。

## Do not read this when
- oracle review 以外の review コマンドや一般的な CLI 初期化・session 操作だけを確認したい場合。
- report renderer や review loop の内部実装だけを局所的に読みたい場合で、対応する実装ファイルを直接読む方が早い場合。
- oracle file の正本仕様そのもの、prompt 文面、Structured Output schema の項目定義を確認したい場合。
- INDEX.md エントリー生成規則やルーティング文書の書き方だけを確認したい場合。

## hash
- 35b2d261f8fb5be8c89b1d133435957cf2ff500d9d0d0e5c5077625d5cab1597

# `test_session_cli.py`

## Summary
- session fork、join、abandon の CLI 回帰テストをまとめる realization test。session branch と session state のライフサイクル、linked worktree、state cleanup、dirty worktree 拒否、join 時の競合解決と branch 削除可否を外部挙動として検証する。

## Read this when
- session fork、join、abandon の CLI 挙動や出力、終了コード、branch/state 遷移を変更・確認する。
- session state file の生成、破損時エラー、cleanup 失敗時の rollback、abandoned/joined 状態の扱いを確認する。
- linked worktree 上での session 操作、home branch の保持、session branch の削除・未削除警告を変更・確認する。
- session join の競合解決、oracle conflict の書き込み profile、未解決 conflict marker 検出、delete conflict staging を確認する。
- dirty worktree 拒否や session join/abandon のエラー報告先が stdout/stderr のどちらかを確認する。

## Do not read this when
- session CLI 以外のサブコマンド挙動を確認したい。
- session の内部 helper 実装だけを局所的に確認したく、CLI 経由の branch/state ライフサイクル観測が不要である。
- oracle 正本仕様や INDEX.md ルーティング規則そのものを確認したい。
- 単体の git wrapper、config、runtime profile の一般挙動を確認したいだけで、session join の競合解決経路に関係しない。

## hash
- 217128b35d1efb878b56c76eb8363be96d3ec5ce84c980faf5f876c2b1861749

# `test_struct_doc_rendering.py`

## Summary
- StructDoc の Markdown renderer が本文中の連続空行を正規化する挙動を検証する単体テスト。通常テキストとコードブロックを対象に、過剰な空行が折りたたまれ、期待される Markdown 文字列になることを確認する。

## Read this when
- StructDoc の Markdown 出力で空行の扱いを変更・確認したいとき。
- 通常テキストまたはコードブロック内の連続空行がどのように描画されるべきかをテストから確認したいとき。
- render_as_markdown の整形挙動に関するテストを追加・修正したいとき。

## Do not read this when
- StructDoc のデータ構造そのものや renderer 全体の実装を確認したいときは、実装側を読む。
- Markdown renderer 以外の prompt builder 分割根拠や正本仕様を確認したいときは、対応する oracle 側の文書を読む。
- CLI 挙動、ファイル操作、永続状態など StructDoc の Markdown 整形と無関係な挙動を調べたいとき。

## hash
- 51580019f3a5f35c894b459980668eec4b098eecee22f1645f571c7c2084f811
