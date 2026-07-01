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
- apply fork コマンドの CLI 経由の実行、Codex 呼び出し、session state 更新、apply branch/worktree 作成、設定読み込み失敗時の中断、.gitignore の扱い、対象 path 正規化を検証する realization test。
- apply fork が session branch と現在の HEAD を基準に apply run を開始し、完了時に一時的な pid や旧 apply worktree 表現を残さないことを確認する。
- realization file 判定に関わる memo、oracle、管理ディレクトリ、INDEX/AGENTS、binary file、tracked ignored file の対象選別を確認する入口になる。

## Read this when
- apply fork の外部挙動、state 遷移、apply branch 名、apply worktree 配置、Codex loop 呼び出し順を変更する。
- linked worktree 上で apply fork を実行する挙動や、oracle snapshot commit と apply branch の起点を確認する。
- apply fork 実行時の .cmoc ignore 保証、session 側 .gitignore の非破壊性、apply branch 側での .gitignore 編集可否を変更または検証する。
- apply fork の設定ファイル読み込みエラー時に apply run を開始しない挙動、標準出力へのエラー表示、pid/state/branch の未生成を確認する。
- apply fork の対象正規化で、root 直下 memo、管理 path、INDEX/AGENTS、oracle path、binary file、tracked ignored file の扱いを確認する。

## Do not read this when
- apply fork 以外のサブコマンドの CLI 挙動だけを確認したい。
- Codex 実行器そのものの統合挙動や LLM 出力品質を確認したい場合で、apply fork 側の呼び出し・状態更新は関係しない。
- path model や realization/oracle file の定義そのものを確認したい場合は、正本仕様側を先に読む。

## hash
- 8132fa30a1ec010f5fecea77ff23e4bf3b34c02c05eaad6deab39af8f9353f9b

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 経由の挙動を、所見列挙から適用、commit、変更要約、report 生成、session state 更新までの一連の制御として検証するテスト群。
- builder の import 可能性、標準 prompt と schema の参照、変更ファイル再調査、収束・未収束・error report、未追跡 file や削除 file の変更要約、rolling 実行時の対象選定を扱う。
- 大きなテストファイルだが、apply fork report と再検査 loop の観測文脈を一箇所に保つため、関連する期待値がまとめられている。

## Read this when
- apply fork の CLI 実行結果、終了コード、report 内容、commit message、session state 更新を変更または調査するとき。
- 所見適用後の変更 file 再調査、収束判定、未収束判定、差分なし適用時の扱い、調査対象なしの場合の report 表示を確認するとき。
- apply fork 用 ACP builder の import 経路、prompt 内容、Structured Output schema 参照を変更するとき。
- report 用変更要約で、未追跡 file、削除済み tracked file、commit 前の working tree 差分をどう扱うか確認するとき。
- rolling apply fork が前回 apply join 後の変更だけを対象にする制御を確認するとき。

## Do not read this when
- apply fork 以外のサブコマンド、通常の session fork/join、または汎用的な git helper の単体挙動だけを調査するとき。
- report schema や prompt の正本仕様そのものを確認したいときは、対応する oracle file を読む。
- apply fork の内部実装だけを局所的に変更し、CLI report・再検査 loop・session state・変更要約の外部挙動に影響しないことが明らかなとき。

## hash
- a23d11397933b25dab37dff6a0bfb74ba9581ddcca7339bc68f5c4dd9091db0a

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
- cmoc の基礎 runtime 契約を横断的に検証する realization test。root placeholder 解決、worktree root 判定、config 既定値と検証、CmocError の表示、CLI preflight と error 出力、subcommand log、state branch 解析、FileAccessMode 変換、Codex sandbox profile、binary 判定など、個別サブコマンドより下位の共通実行前提をまとめて扱う。
- 単一責務は共通 runtime 回帰の維持であり、root 状態や共通 fixture を共有するため、個別機能の詳細テストではなく runtime 境界が一緒に崩れないことを確認する入口として位置づけられる。

## Read this when
- root placeholder、repo root、run root、work root、linked worktree、managed worktree の扱いを変更する。
- CmocError、CLI 引数解析 error、stdout/stderr への error report、call stack 表示、CLI preflight、completion probe、subcommand log の生成条件を変更する。
- config の既定値、codex model class、reasoning effort、config_from_dict の検証挙動を変更する。
- SessionState の branch 名解析、apply/session branch の形、branch からの state 読み込みを変更する。
- FileAccessMode、sandbox mode、Codex cwd、writable_roots、extra writable paths、session join conflict の書き込み許可範囲を変更する。
- binary 判定、duration 表示、`.cmoc` ignore pattern 追加のような共通 runtime helper の外部挙動を変更する。

## Do not read this when
- 特定サブコマンド固有の business logic、prompt 内容、indexing、session fork/join などの詳細挙動だけを確認したい場合は、そのサブコマンドや機能に対応するテストを先に読む。
- oracle file の正本仕様本文を確認したい場合は oracle 側の該当文書を読む。この対象は正本仕様ではなく realization test である。
- 単一 helper の内部実装だけを読みたい場合は、対応する実装モジュールを直接読む。ここは runtime 境界の回帰観点を確認するための入口である。

## hash
- 8b4fcd7566e0f09531dbabbb19791749068b68cb927bf76b6e7770d76198f47e

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
- Codex CLI 呼び出しランタイムのテスト群。exec/TUI 起動時の profile 生成、cwd と sandbox 設定、schema 配置、apply process tracking、ファイルアクセス違反の回復・拒否、追加 read path 検査、Codex CLI 不在や非ゼロ終了時のエラー報告を検証する。

## Read this when
- Codex CLI の exec/TUI 呼び出し処理、profile 設定、sandbox writable roots、作業ディレクトリ選択、schema 出力設定、または call log 周辺の挙動を変更する。
- FileAccessMode ごとの読み書き許可、oracle/memo/.agents/.cmoc へのアクセス制御、違反差分の検出・回復処理を確認または変更する。
- Codex subprocess の process group 管理、apply process tracking 環境変数の扱い、Codex CLI 不在・失敗時の CmocError と利用者向け出力を検証する。

## Do not read this when
- Codex CLI 呼び出しランタイムに関係しない通常の CLI コマンド処理、設定モデル定義、path model、INDEX 生成規則だけを調べる。
- oracle file の正本仕様本文やドキュメント構成だけを確認したい場合。
- 実際の Codex/LLM 出力品質やプロンプト内容そのものを評価したい場合。

## hash
- 54904239d7ac9fd67f23ce416a8393c45b82a0addb53f5738ef8c5aa64f8c1dc

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
- review oracle コマンドの CLI 経由の外部挙動を検証する realization test。対象 oracle file の列挙、report 生成、所見の列挙・検証・judge・merge、上限到達時や処理失敗時の report、review 用 worktree からの INDEX.md 変更の取り込み、非 INDEX.md 差分の拒否を扱う。

## Read this when
- review oracle の report 形式、件数、section 順、accepted/rejected finding の出力、error/no_targets/fatal/ok verdict を変更または確認したいとき。
- review oracle が full scope または session scope でどの oracle file を対象にするかを変更または確認したいとき。
- review oracle の所見 loop、challenger/advocate/judge/merge の制御、prompt に渡す既存所見の範囲、merge operation の契約を変更または確認したいとき。
- review oracle が linked worktree、session branch、review worktree、join commit、INDEX.md 変更の merge conflict をどう扱うかを変更または確認したいとき。
- review oracle 実行中に Codex が作成した差分のうち、INDEX.md だけを許し、それ以外を拒否して元 worktree を汚さない挙動を確認したいとき。

## Do not read this when
- review oracle 以外の review サブコマンドや通常の session 操作だけを扱うとき。
- 実装内部の helper 分割や型定義だけを確認したく、CLI 実行結果、report 内容、git/worktree 副作用を検証する必要がないとき。
- oracle file の正本仕様本文を確認したいとき。

## hash
- 1a8726db12b961d86532ae2594f48bb2d46607622497863717b193de359e1c47

# `test_session_cli.py`

## Summary
- session branch と session state のライフサイクルを、CLI 外部挙動としてまとめて検証する realization test。fork、join、abandon、linked worktree、state cleanup、dirty worktree 拒否、conflict resolution とエラー出力先を、同じ session 状態遷移の観測点として扱う。

## Read this when
- session fork が session branch と state file を作成する挙動、session-id collision、既存 state との衝突、linked worktree 上の開始 branch/head を確認したいとき。
- session abandon が home branch へ戻り、session branch を削除し、state を abandoned に更新する挙動や、home branch 不在・cleanup 失敗時の rollback を確認したいとき。
- session join が home branch へ取り込み、conflict resolution を Codex 実行へ委譲し、delete conflict の解決を stage し、session branch 削除可否を出力する挙動を確認したいとき。
- session completion 系が壊れた state file、dirty worktree、merge 後の予期しない conflict marker 残存をどう扱い、stdout/stderr のどちらへ報告するかを確認したいとき。

## Do not read this when
- session CLI の実装方針や helper の責務境界を調べたいだけなら、対応する session sub-command 実装を読む。
- session 以外の CLI コマンド、agent call 一般、設定読み込み、ログ基盤の挙動を調べたいだけなら、それぞれの対象テストや実装を読む。
- oracle file の正本仕様や realization standard 自体を確認したい場合は、oracle 配下の該当本文を読む。

## hash
- 5bd4a4c5a8c064008e49f02d663a1d9ed7792fe6487fc84e9104a99b33d4fe15

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
