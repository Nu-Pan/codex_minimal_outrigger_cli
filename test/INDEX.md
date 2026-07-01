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
- apply fork の CLI 経由の制御を検証する realization test。所見列挙、所見適用、commit、変更要約、report 生成、session state 更新までの一連の挙動を、収束・未収束・error・変更ファイル再調査・rolling fork の観測結果として扱う。
- apply fork 用 AgentCallParameter builder の import 可能性、prompt 内容、Structured Output schema 参照も検証し、packaged layout や src のみの PYTHONPATH で成立するかを確認する。
- report 用の変更差分・変更 path・fallback 要約が未追跡ファイルや未 commit 差分を含めて扱えることを検証する。

## Read this when
- apply fork の report 内容、終了コード、収束判定、未収束判定、error report、変更要約、commit message、session state 更新の CLI 挙動を確認・変更したいとき。
- apply fork が所見適用後に変更ファイルや新規ディレクトリ配下を再調査する制御、または所見適用で差分が出ない場合の扱いを確認したいとき。
- apply fork が file access rule violation recovery を挟んで許可差分を commit する挙動を確認したいとき。
- apply join 後の rolling apply fork が、前回 apply join の oracle snapshot 以降の変更を対象にするか確認したいとき。
- apply fork の change summary builder、file finding enumeration builder、finding application builder の import、prompt 構成、schema path 参照を確認したいとき。

## Do not read this when
- apply fork の内部 helper 単体の小さな仕様だけを確認したい場合で、該当する実装ファイルやより局所的なテストを直接読めるとき。
- apply fork 以外の subcommand、session fork/join 自体、init、または通常の Git 操作 wrapper の挙動を調べたいとき。
- oracle file の正本仕様を確認したいとき。この対象は realization test であり、正本仕様ではない。

## hash
- 688028dac5e7ac9eb0ac5bee8cabbcf9652385e2c82bd08243c7b3800e587da5

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
- cmoc の基礎 runtime 契約を横断して検証する realization test。root placeholder 解決、repo/run/work root 判定、config 既定値と検証、CmocError の表示、CLI preflight と parse error、subcommand log、worktree 作成・削除ガード、FileAccessMode 変換、Codex profile の sandbox 許可範囲、binary 判定など、サブコマンド共通の実行前提をまとめて扱う。

## Read this when
- runtime 全体の共通契約、root 解決、worktree 管理、CLI error 表示、config 読み込み、FileAccessMode、Codex sandbox profile、状態 branch 名、binary 判定の回帰テストを確認・変更する時。
- 個別サブコマンドではなく、複数機能の実行前提として共有される cmoc runtime 挙動が壊れていないかを調べる時。
- sandbox 書き込み許可範囲や追加 writable path の拒否・許可条件に関するテストを確認する時。

## Do not read this when
- 特定サブコマンド固有の入出力、分岐、永続状態だけを調べたい時は、そのサブコマンドの実装・テストを直接読む。
- oracle file の正本仕様そのものを確認したい時は、対応する oracle doc または oracle src を読む。
- runtime 共通契約に関係しない UI、prompt 文面、個別生成物、補助スクリプトの詳細だけを調べたい時。

## hash
- 1eb9475eca578153a8e895613e4fba2f48c6e93259df3c015984dfd0ffcb7488

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
- Codex CLI 実行・TUI 呼び出しの runtime 境界を検証する pytest 群。プロセスグループ追跡、継承された追跡環境変数の無視、profile 生成、sandbox と writable_roots、作業ディレクトリ、schema 保存先、追加 read path 検査、非ゼロ終了、CLI 不在時エラーを扱う。
- `run_codex_exec` と `run_codex_tui` が、file access mode と worktree に応じて Codex subprocess をどの引数・cwd・profile・許可領域で起動するかを確認する入口。

## Read this when
- Codex CLI 呼び出し時の subprocess 起動引数、stdin、`--cd`、`--profile`、`--output-schema`、`--output-last-message` の外部挙動を変更・確認するとき。
- Codex runtime の sandbox mode、writable_roots、pure oracle read、repo write、realization write、linked worktree での cwd や許可領域の扱いを調べるとき。
- Codex subprocess の apply process tracking、process group、追跡環境変数の扱い、file access violation からの再試行挙動を変更するとき。
- TUI 呼び出し前の extra read path 検査、complete prompt の許可条件、TUI 失敗時の console 表示・call log、Codex CLI 不在時の `CmocError` を検証するとき。

## Do not read this when
- Codex runtime の実装詳細だけを読みたい場合は、対応する runtime 実装モジュールを直接読む。
- Codex profile の低レベルな TOML 生成規則だけを確認したい場合は、profile 生成側の実装またはその単体テストを読む。
- agent call parameter、file access mode、model class などの基本データ構造の定義を確認したい場合は、それらの定義元を読む。
- Git repository fixture、stub executable、Codex home setup などテスト支援関数の実装を調べたい場合は、テスト support 側を読む。

## hash
- 6b7ee1fbdbb5044992214adcf591df6b2354e8e39c21d5843e05eba8b180b328

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

# `test_prompt_parts.py`

## Summary
- agent prompt の各標準部品と ACP builder の生成結果を、最終 prompt 上で組み合わさった外部挙動として横断検証する realization test。
- routing、file access、oracle/realization/review/index 系 standard、TUI parameter 選定、review/apply/session 系 builder の prompt・実行パラメータ・structured output schema 参照が、正本仕様断片とずれないことを確認する入口。
- 単一ファイルとしては大きいが、prompt 構築の回帰観点を同じ render/schema 期待値で読む必要があるため、関連する prompt 構築テストを一箇所に集約している。

## Read this when
- prompt 標準部品の markdown render 結果、空行処理、root token の保持、または最終 prompt への標準文書注入条件を変更する。
- ACP builder が返す model class、reasoning effort、file access mode、prompt 本文、または structured output schema 参照の挙動を変更する。
- oracle 配下の schema や prompt builder 正本仕様断片を変更し、realization 側の生成結果との一致を確認したい。
- TUI parameter 選定、review oracle、apply fork、session join など、複数 builder にまたがる prompt/schema 回帰を調べる。

## Do not read this when
- 個別 builder の内部実装だけを読みたい場合は、対象 builder の implementation を先に読む。
- oracle file 側の正本仕様断片そのものを確認・検討したい場合は、oracle 配下の該当本文を読む。
- prompt 構築と関係しない CLI 実行、永続状態、git 操作、または一般的な補助処理のテストを探している。
- 単一の小さな helper の実装詳細だけを確認したい場合は、その helper の実装またはより局所的なテストを読む。

## hash
- c0e7ff3c7ac7d2eca4ba7d7719d98093e9121fb7c58c40643d2e6a75eea51df5

# `test_review_oracle_cli.py`

## Summary
- review oracle を CLI 経由で実行したときの外部挙動を検証するテスト群。report の生成内容、scope 別の対象選択、所見の列挙・検証・judge・merge、エラー時 report、review 用 worktree と join commit、INDEX.md 差分の取り込み・競合解決を扱う。
- 所見評価 loop の制御と report 文脈を共有するため、複数の観点を単一の review run の統合テストとしてまとめている。

## Read this when
- review oracle コマンドの CLI 挙動、終了結果、標準出力、生成 report の構成やメタデータを変更・確認するとき。
- review oracle の対象 oracle file 列挙、full scope と session scope、git ignored だが tracked な oracle file、AGENTS.md や INDEX.md の除外条件を確認するとき。
- review oracle の所見 loop で、列挙結果の次 round への渡し方、challenger と advocate の理由、judge 結果、merge operation の契約や不正操作拒否を変更するとき。
- review oracle 実行中の一時 worktree、linked worktree 上の session branch、review が生成した INDEX.md の取り込み、join commit、INDEX.md 競合解決を扱うとき。
- review oracle が途中失敗した場合の error report、または review が INDEX.md 以外の差分を作った場合の拒否と原状維持を確認するとき。

## Do not read this when
- oracle review の prompt 文面や structured output schema だけを確認したいとき。
- review oracle 以外の review サブコマンド、または一般的な session fork/init の単体挙動だけを確認したいとき。
- report rendering の細部ではなく、対象ファイル列挙 helper の最小単位の実装だけを確認したいとき。
- CLI を経由しない低レベルな git helper や設定モデルの構造だけを確認したいとき。

## hash
- 963813a19eb75c2c5dc4742e2613e94860da6869f4800b819c0a0920b98d6cbf

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
