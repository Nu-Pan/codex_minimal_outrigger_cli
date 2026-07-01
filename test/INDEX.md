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
- apply fork サブコマンドの realization test。Codex 実行を fake に差し替え、apply run の開始・完了、session state 更新、apply branch/worktree 作成、linked worktree 上の HEAD 起点、設定読み込み失敗時の中断、.gitignore の扱い、target 正規化を検証する。
- CLI 経由の統合的な挙動確認と、apply fork module の一部関数を直接呼ぶ境界条件確認の両方を含むため、apply fork の外部副作用や state/worktree/branch のライフサイクルを調べる入口になる。

## Read this when
- apply fork の実装変更により、session state の apply 状態、apply branch 名、apply worktree 配置、PID file 削除、完了判定が変わる可能性があるとき。
- linked worktree 上で apply fork を実行した場合の起点 commit、session branch、apply branch、worktree 配置の期待挙動を確認したいとき。
- apply fork 実行前の cmoc config 読み込み失敗時に、apply run を開始しないことやエラー出力先を確認したいとき。
- apply fork が .cmoc ignore を確保する処理、session 側の .gitignore を dirty にしない処理、または apply branch 側で .gitignore を編集対象にできる処理を変更するとき。
- apply fork の対象 path 正規化で、root 直下の memo 除外、入れ子の memo directory の保持、binary file の保持を確認したいとき。
- Codex 呼び出しを伴う apply fork loop の呼び出し目的、所見列挙、所見適用、変更要約の制御をテスト上で追いたいとき。

## Do not read this when
- apply fork 以外の apply 系サブコマンドや session fork 単体の仕様を調べたいだけのとき。
- Codex CLI や LLM 出力内容そのものの品質を検証したいとき。この対象は Codex 実行結果を fake にして制御フローと副作用を検証する。
- path model、oracle/realization の概念定義、INDEX routing の規約を確認したいとき。
- apply fork の内部 helper 実装そのものを読みたいとき。この対象は期待される外部挙動と重要な境界条件を示すテストであり、実装詳細の入口ではない。

## hash
- 299d8a600d3ab3b419a47ee298117556c499bfbbc77d3d80778aeade1dded333

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 経由の report 生成、再検査 loop、収束・未収束・error 判定、変更要約、commit、session state 更新を一体で検証する realization test。
- apply fork 用 ACP builder の import 可能性、prompt 内容、oracle schema 参照、変更ファイル再調査、未追跡 file を含む差分要約、rolling fork の対象選択も扱う。
- 対象は大きいが、apply fork report と同じ制御 loop から観測される期待値を一箇所に集めることで文脈を保っている。

## Read this when
- apply fork の CLI 挙動、終了 code、作業 report の内容、所見数推移、変更要約、commit message、session state 更新を変更または確認する時。
- apply fork が変更後 file を再検査する条件、INDEX.md を再検査対象から除外する条件、上限到達時の収束・未収束判定を確認する時。
- apply fork の error report、未 commit 差分、未追跡 file、fallback 変更要約、rolling fork の対象 commit 計算を変更する時。
- apply fork 用 ACP builder の packaging、PYTHONPATH、prompt に含める standard、structured output schema の参照先を変更する時。

## Do not read this when
- apply fork 以外の subcommand の CLI 挙動や report を確認したいだけの場合。
- apply fork の内部 helper 単体の詳細だけを確認したい場合で、より直接その実装または小さな単体 test が存在する場合。
- INDEX.md 生成や一般的な routing entry の規則だけを確認したい場合。
- Codex 実行結果の品質そのものや LLM 出力文面の妥当性を検証したい場合。

## hash
- f146c691c6ef55554c03b55114d50d8ade4f404c7d89f28876fa7a7e912a04a8

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
- cmoc の共通 runtime 契約を横断的に検証する realization test。root placeholder 解決、linked worktree と run/work root、config 既定値と不正値、CmocError の Markdown 表示、CLI error の stdout 出力、subcommand log、`.cmoc` ignore、FileAccessMode から Codex sandbox/profile への変換、binary 判定、branch session state の境界を扱う。
- 個別サブコマンドの仕様ではなく、複数機能の実行前提として同時に崩れやすい基礎 runtime 挙動を一箇所で確認する入口。

## Read this when
- runtime の root 解決、worktree 管理、path placeholder、config 読み込み、error report、subcommand log、FileAccessMode、Codex profile、binary 判定、session state の回帰を調べるとき。
- CLI 実行前 preflight や Click parse error が cmoc 形式の stdout report になる挙動を変更・確認するとき。
- Codex sandbox の writable roots、追加書き込み許可 path、oracle conflict 解決時の例外的な書き込み許可を確認するとき。
- 共通 runtime 契約に関わる実装変更で、個別サブコマンドより下の基礎挙動が壊れていないか確認するとき。

## Do not read this when
- 特定サブコマンド固有の入出力や業務ロジックだけを確認したいときは、そのサブコマンドのテストへ進む。
- oracle file の正本仕様内容そのものを確認したいときは、対応する oracle doc/src/test を読む。
- INDEX.md エントリー生成やルーティング文書の規則だけを確認したいときは、この runtime 回帰テストではなく INDEX 関連の仕様・テストを読む。

## hash
- 5cfb7b88b0ac9712755bbca8058e05328ef2fd4807db92a9f53005efbef28f7a

# `test_cli_init_tui.py`

## Summary
- init と TUI 起動直前の CLI 境界における外部挙動を検証するテスト。cmoc 初期化時の .cmoc ignore、既存 staged/unstaged 差分の保護、設定 default 同期、linked worktree 上の初期化、subcommand log、Markdown prompt 解析、TUI 用 AgentCallParameter 構築までを、利用開始直後の repository/runtime 準備として一体で扱う。

## Read this when
- init の挙動、生成される設定、.cmoc の ignore、初期化 commit、既存 git 差分の保護を変更または確認する時。
- TUI 起動前の editor 呼び出し、prompt 保存、resolve parameter、Codex TUI 起動 parameter、structured output schema、extra read path の扱いを変更または確認する時。
- linked worktree での init/TUI、repository root と作業 cwd の使い分け、root 側 .cmoc への log/config 保存、worktree 側 ignore の扱いを変更または確認する時。
- init/TUI 前処理の回帰テストを追加する時に、既存ケースへ統合できるか判断したい時。

## Do not read this when
- 個別 subcommand の処理本体や、init/TUI 前処理と無関係な CLI 挙動だけを確認する時。
- AgentCallParameter などの型定義そのもの、Codex 実行 wrapper の内部実装、runtime preflight の詳細を確認したい時。
- oracle 文書や INDEX.md 生成規則そのものを確認したい時。
- 単体 helper の細かな実装詳細だけを確認できれば足り、init/TUI の外部挙動や repository/runtime 準備の回帰に関係しない時。

## hash
- cb8700def91815f6c11e29f3f43dbb2adedcc09c99902c9ced35b3ccb657b85b

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI の exec/TUI 呼び出しを外部挙動として検証する realization test。専用プロセスグループでの apply 追跡、継承環境の無視、profile 生成、sandbox 設定、cwd 選択、schema state の配置、追加 read path の事前検査、失敗時エラー表示、Codex CLI 不在時のエラーを扱う。

## Read this when
- Codex CLI 呼び出しラッパーの引数、標準入力、作業ディレクトリ、profile 内容、出力取得、call log、失敗時エラー処理を変更する。
- FileAccessMode ごとの sandbox 設定、oracle 配下への書き込み許可、pure oracle read 時の cwd 制限を確認する。
- linked worktree 上での exec/TUI 実行、schema state の保存先、完全プロンプトの追加 read path 許可条件を確認する。
- apply process tracking のための subprocess 起動、プロセスグループ、追跡ファイル、継承環境変数の扱いを変更する。

## Do not read this when
- Codex CLI 呼び出しではなく、agent call parameter の値オブジェクト自体の定義や列挙値だけを確認したい。
- repository fixture、git helper、stub 実行ファイル生成などのテスト支援 API の実装を直接変更したい。
- oracle 文書の内容、INDEX.md 生成規則、または routing 仕様そのものを確認したい。

## hash
- d7b4501a02926a6ad6b8a2e311989e789a63a10736adadc63e285e7ad1626f90

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
- agent prompt の標準部品、routing、file access、structured output schema、各種 ACP builder の生成結果を横断的に検証する realization test。
- prompt の最終レンダリング、schema の oracle source との一致、builder の model・reasoning・file access mode、動的テキストや root token の保持を、同じ読み取り文脈でまとめて確認する。
- 16,000 文字を超えるが、prompt 構築回帰の期待値を一箇所に保つ意図と分割しない理由を本文冒頭に持つ。

## Read this when
- agent prompt の標準部品、complete prompt、routing rule、file access rule、oracle/realization/review/index entry standard のレンダリング挙動を変更・確認する。
- ACP builder が返す model class、reasoning effort、file access mode、structured output schema path、prompt 内容を変更・確認する。
- oracle source 側の schema や builder と realization 側 builder の一致性を確認する。
- root placeholder、動的 prompt、code block 内テキスト、既知所見テキストなどが prompt 生成で置換・破壊されないことを検証する。
- prompt 構築テストが大きい理由や、分割せず一箇所に保っている根拠を確認する。

## Do not read this when
- 個別 builder の実装そのものを変更する場合は、まず対応する実装側または oracle source 側の対象を読む。
- INDEX.md 用エントリー生成の規則だけを確認したい場合は、index entry standard の正本仕様を読む。
- prompt の期待値ではなく、CLI の実行フロー、永続状態、外部コマンド処理、UI 表示処理を調べる場合は、該当する実装・テストへ直接進む。
- jsonschema や subprocess などの一般的な依存利用を調べたいだけの場合は、このテスト全体を読む必要はない。

## hash
- 7a274f9bb1e5ce91654cd57a0bb4cc564bcd391387429035068d39a3228f7837

# `test_review_oracle_cli.py`

## Summary
- review oracle の CLI 実行を通じて、report 生成、所見の列挙・検証・judge・merge、scope ごとの対象選択、review 用 worktree と join commit、エラー時 report、許可されない差分の拒否を外部挙動として検証する realization test。
- 16,000 文字超の大きなテストだが、同じ review run の fake Codex 応答、report 文脈、所見 loop 状態を共有するため、oracle review の外部挙動確認を一箇所に集約している。

## Read this when
- review oracle command の出力 report 構成、metadata、accepted/rejected finding の表示順や件数集計を変更・確認する時。
- review oracle の full scope または session scope で、gitignored oracle、binary oracle、memo 形状の path、変更対象なしの場合の扱いを確認する時。
- 所見 loop における enumerate、validate challenger、validate advocate、judge、merge の呼び出し順、prompt に含める既存所見、merge operation の契約を変更・確認する時。
- review oracle が linked worktree 上の session branch を扱う挙動、review worktree の場所、review index 変更の merge、index conflict 解決を確認する時。
- review oracle 処理中の失敗時 report、標準出力への error 表示、review 側が生成した許可外差分の拒否と復元挙動を確認する時。

## Do not read this when
- oracle file の正本仕様そのものや、人間が管理する仕様文書の内容を確認したいだけの時。
- 通常の session fork、init、git helper、設定読み込みなど、review oracle の外部挙動に直接関係しない CLI 基盤を調べる時。
- report renderer や merge helper の実装詳細だけを局所的に確認したい時。ただし期待される外部出力や制御契約を確認する場合は読む。
- Codex CLI や LLM の品質評価そのものを調べる時。この対象は fake 応答を使い、cmoc 側の制御と出力を検証している。

## hash
- 4cba81a523f4670b96bf50c1a44aa9d4624cfa0be71338e3d3fbb14c2cb57cd5

# `test_session_cli.py`

## Summary
- session fork、join、abandon の CLI 外部挙動を、session branch と session state のライフサイクルとしてまとめて検証する回帰テスト。
- linked worktree 上での branch 操作、state cleanup、dirty worktree 拒否、session-id 衝突、壊れた state file、join 時の conflict 解決とエラー出力先を扱う。
- ファイルサイズが大きい理由として、同じ branch/state fixture を共有する session 状態遷移の観測点を一箇所に保つ判断を明記している。

## Read this when
- session fork、join、abandon の CLI 挙動を変更または調査する。
- session branch の作成・削除、home branch への復帰、session state file の作成・更新・cleanup を確認する。
- linked worktree から session 操作を行う場合の branch と state の扱いを確認する。
- session-id 衝突、壊れた session state file、必須 field 欠落などの異常系を確認する。
- session join の conflict 解決、oracle file conflict への writable profile、delete conflict の staging、conflict marker 検出を確認する。
- session join または abandon の失敗時に stdout と stderr のどちらへエラー報告されるかを確認する。
- この大きなテストファイルを分割すべきか判断するため、凝集性の根拠を確認する。

## Do not read this when
- session 以外のサブコマンドの CLI 挙動だけを確認したい。
- session 内部 helper の単体的な処理だけを調べれば足り、fork、join、abandon を通した外部挙動や state 遷移を確認しない。
- Codex agent call の一般的な profile 生成だけを調べたい場合で、session join conflict 解決時の writable profile には関心がない。
- git repository fixture や test runner の共通支援関数そのものを変更する場合。

## hash
- e0a237c3c2ea7a5280d26c2e314e2cece061625b8a601a038ca7b70b6836bab4
