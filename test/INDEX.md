# `_support.py`

## Summary
- テスト内で共通利用する補助関数群をまとめた realization test の支援モジュール。git リポジトリ作成、テスト用 CODEX_HOME 設定、ブランチ取得、apply 用 worktree 解決など、CLI テストの前提環境を小さく構築する入口になる。
- Typer のテスト runner や主要な cmoc 実装モジュールを同じ場所から参照できるようにし、複数テストで共有される setup と状態参照を集約している。

## Read this when
- CLI テストで一時 git リポジトリ、初期 commit、oracle 配下の fixture、または追跡済み ignore 対象ファイルを用意する helper を確認・追加したいとき。
- テスト中に CODEX_HOME を一時ディレクトリへ向ける処理や、認証ファイルを含む最小の Codex home fixture を再利用したいとき。
- apply 系テストで保存状態から apply branch の worktree path を復元する共通処理を確認したいとき。
- 複数のテストファイルにまたがって同じ subprocess git 操作や CLI runner setup が重複しそうなとき。

## Do not read this when
- 個別サブコマンドの期待出力、エラー条件、状態遷移を確認したいだけなら、該当するテスト本文を直接読む。
- プロダクト実装の CLI 定義、runtime 処理、path token 解決、sandbox mode 変換の挙動を変更したいときは、対応する実装側の本文を読む。
- oracle file の正本仕様断片や仕様文書を確認したいときは、このテスト支援モジュールではなく oracle 側の本文を読む。

## hash
- 177bd3430c87ab5f9b7100c81bd29747aefe79b9e5248eaa456c01e737e6345d

# `test_apply_abandon_cli.py`

## Summary
- apply run の破棄コマンドに関する realization test。apply worktree と apply branch の削除、状態の ready への戻し、警告出力、実行中 process 停止、破棄対象を特定できない場合や stale branch からの実行拒否を、CLI の外部挙動と永続状態の変化で検証する。

## Read this when
- apply run を破棄する CLI の挙動、出力、終了コード、永続状態更新を変更・確認したいとき。
- apply worktree や apply branch の cleanup、既に存在しない cleanup 対象の warning、apply_process_id の扱いを確認したいとき。
- 実行中 apply の停止順序、process id が無い running 状態の拒否、破棄対象ではない apply branch からの実行拒否を検証したいとき。
- apply worktree 内から破棄コマンドを実行した場合に、元 repo へ戻って cleanup される挙動を確認したいとき。

## Do not read this when
- apply run の生成、review、merge など、破棄以外のサブコマンド挙動だけを調べたいとき。
- CLI 経由ではなく内部 helper の単体仕様や path model の定義だけを確認したいとき。
- Codex 実行結果の内容や LLM 出力品質そのものを検証したいとき。
- oracle の正本仕様断片を確認したいとき。

## hash
- 26427038c4cf686d4d47d6f63da1bc304c403298ac812e3cce145351156cae87

# `test_apply_fork_cli.py`

## Summary
- apply fork 系 CLI の realization test。session fork 後の apply fork 実行が Codex ループ、apply branch/worktree、session state、report、commit message、change summary、再検査、rolling target をどう扱うかを外部挙動として検証する。
- 設定読み込み失敗、編集禁止対象の差分、root 直下 memo の除外、.gitignore の扱いなど、apply fork 実行時に開始・変更・状態更新してはいけない境界も確認する。

## Read this when
- apply fork の成功時・未収束時・エラー時の終了コード、出力、report 生成、state 更新、apply branch/worktree 作成の挙動を変更または調査するとき。
- apply fork が Codex exec を呼ぶ目的名、所見列挙、所見適用、commit message 生成、change summary 生成の制御フローを検証したいとき。
- apply fork の対象 path 正規化、root 直下 memo 除外、nested memo 許可、dirty file の再検査、INDEX.md の再検査除外を扱うとき。
- apply fork が .gitignore を勝手に書き換えないこと、ただし所見対象としては .gitignore を編集できることを確認するとき。
- apply join 後の rolling apply fork が前回 apply の oracle snapshot commit と現在差分から対象を選ぶ挙動を確認するとき。
- 編集禁止対象に差分が出た場合の error state、report 内容、change summary を呼ばない制御を確認するとき。

## Do not read this when
- apply fork ではなく apply join、session fork、init など個別コマンド単体の基本仕様や実装入口だけを知りたいとき。
- Codex exec の実プロセス起動、プロンプト内容、構造化出力 schema そのものを調べたいとき。
- path keyword、oracle file、realization file などリポジトリ全体の概念定義を調べたいとき。
- apply fork 以外の CLI や、テスト支援 fixture の一般的な使い方を調べたいとき。

## hash
- 2169b31f834e790817e27d8c9c16e6700d7ffb05a21a8fccbba514819c53681f

# `test_apply_join_cli.py`

## Summary
- apply join の CLI 挙動を検証する realization test。apply 用 worktree と branch の後片付け、session 状態の ready への復帰、join report の生成、apply oracle snapshot commit の記録を確認する。
- apply worktree 内から join した場合の作業ディレクトリ復帰、未コミット差分がある場合の中断、ログ保存先、stdout/stderr の扱いを確認する。
- 想定外の apply 差分、force resolve、許容される .gitignore 差分、通常ファイルの merge conflict、INDEX.md conflict 解決後の継続といった apply join の失敗・復旧経路を扱う。

## Read this when
- apply join の成功時に apply worktree と apply branch が削除され、session state と last joined snapshot が更新されるかを確認・変更したいとき。
- apply join を session worktree または apply worktree のどちらから実行してもよい挙動、特に apply worktree からの実行後に root へ戻る挙動を調べるとき。
- apply worktree に未コミット差分がある場合に join を拒否し、apply state を completed のまま保ち、apply worktree と apply branch を残す挙動を確認するとき。
- apply join の report 出力、想定外差分の検出、force resolve による破棄、merge conflict の報告・中断・継続条件を変更するとき。
- apply join で .gitignore 変更を通常の apply diff として許容する境界や、INDEX.md conflict を通常モードで解決して処理を続ける境界を確認したいとき。

## Do not read this when
- apply fork の起動条件、Codex 実行パラメータ、apply worktree 作成そのものだけを調べたいとき。
- session fork、init、repository fixture、git helper など、join 前提を作る共通テスト基盤の詳細だけを確認したいとき。
- oracle file や INDEX.md の正本仕様を確認したいとき。この対象は realization test であり、正本仕様ではない。
- apply join 以外の CLI サブコマンドの正常系・異常系を調べたいとき。

## hash
- b11a14f6cba6f5a1d8f404c6cb28d0539cf1010f0efc6a8de68e83fc65d6363b

# `test_basic_runtime.py`

## Summary
- cmoc の基本的な実行時挙動を横断的に検証する realization test。パス token 解決、時間表示、repo root と work root の判定、設定既定値、エラー markdown、CLI エラー出力、補完 probe、`.cmoc` ignore 設定、file access mode と Codex profile の権限生成を扱う。
- 個別機能の細部テストというより、ランタイム基盤・CLI 前処理・権限 profile 生成が現行の外部挙動を満たすかを確認する入口として位置づく。

## Read this when
- パス表記や `<cmoc-root>` token 解決、linked worktree における repo root と work root の区別を確認・変更したいとき。
- 実行時間表示、設定既定値、model class や reasoning effort の既定 mapping を変更する影響を確認したいとき。
- `CmocError` の markdown 表示、CLI 引数解析失敗、detached HEAD、work root 外実行などのエラーが stdout に出る挙動を確認・変更したいとき。
- shell completion probe 時に cmoc preflight や `.gitignore`・`.cmoc` 作成などの副作用を避ける挙動を確認したいとき。
- `.cmoc` を `.gitignore` に追加する処理、既存 ignore pattern を尊重する処理を確認・変更したいとき。
- file access mode の文字列表現、sandbox mode 変換、Codex profile 内の read/write/deny_read/read_only/writable_roots の生成を確認・変更したいとき。

## Do not read this when
- 特定サブコマンドの通常成功フローや domain logic だけを調べたいときは、そのサブコマンドや対象機能の実装・専用テストを先に読む。
- oracle file の正本仕様そのものを確認したいときは、この realization test ではなく対応する oracle doc または oracle src/test を読む。
- LLM や Codex CLI の出力品質そのもの、または外部ツールの一般的な挙動を検証したいときは対象外。
- 個別 helper の内部実装手順だけを変更する場合で、ここに現れる外部挙動や制御ロジックに影響しないなら、直接その helper の実装・近接テストを読む。

## hash
- e2a9c702735fb2b3e209b419ff7e7cc558d2c4161951d3bb4262319072940066

# `test_cli_init_tui.py`

## Summary
- CLI の初期化処理、対話起動処理、Markdown プロンプト解析の外部挙動を検証する realization test。
- 初期化では既存の管理ディレクトリ追跡解除、ignore 設定、既存 staged/unstaged 変更の保全、linked worktree での保存先、デフォルト設定生成と既存設定値の維持を扱う。
- 対話起動ではエディタで作成された依頼文の整形、パラメータ解決、Codex 起動時の引数・追加 read path・ログ保存先を扱う。
- Markdown プロンプト解析では fenced code block 内の見出し無視と、見出し前本文の保持を扱う。

## Read this when
- 初期化コマンドが管理ディレクトリや ignore 設定、設定ファイル、サブコマンドログ、git commit・index・worktree 状態へ与える副作用を変更または確認する時。
- 既存の staged 変更や unstaged 変更を初期化処理が壊さないことを確認したい時。
- linked worktree 上で初期化または対話起動した場合の、実リポジトリ側と作業ツリー側の保存先・cwd・root の扱いを確認する時。
- 対話起動がエディタ内容から完全版プロンプトを作り、不要な HTML コメントを除去し、パラメータ解決結果を Codex 起動設定へ反映する挙動を変更または確認する時。
- Markdown 依頼文を見出し単位に分解する処理で、コードブロック内の見出し風行や見出し前の本文をどう扱うか確認する時。

## Do not read this when
- CLI の初期化・対話起動・Markdown プロンプト解析以外のサブコマンド挙動を調べたい時。
- 設定値の schema や既定値の定義そのものを確認したい時は、実装または仕様の定義元を読む方が直接的。
- Codex 実行ラッパーや外部コマンド実行の内部実装を変更したいだけで、対話起動から呼ばれる引数・副作用を確認する必要がない時。
- Markdown 全般の構文解析仕様を網羅的に確認したい時。この対象は依頼文分割で検証されている境界だけを扱う。

## hash
- 3876e04d7b822b40ba6d714085c6a89446d1ee0f53e067eae2e29288cccdfdce

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI を呼び出す runtime 層の realization test。exec 経路で prompt を標準入力に渡すこと、schema 配置、profile 生成、ログ記録、repo config の反映を検証する。TUI 経路で prompt を引数に渡すこと、workspace write sandbox 設定、call log と subcommand log の記録を検証する。

## Read this when
- Codex CLI 呼び出しの exec 経路について、引数構成、標準入力、output schema、output last message、生成 profile、CODEX_HOME、作業ディレクトリ、ログ出力の期待挙動を確認・変更する時。
- Codex CLI 呼び出しの TUI 経路について、prompt の渡し方、subprocess.run の呼び出し条件、sandbox_workspace_write の writable/read-only path、call log、console 表示を確認・変更する時。
- repo 側 config.json の codex model や reasoning_effort が生成 profile に反映される挙動を確認・変更する時。
- Codex 呼び出し runtime のテストを追加・整理する前に、既存の外部挙動検証観点と重複していないか確認する時。

## Do not read this when
- Codex CLI 呼び出し runtime 以外のサブコマンド仕様、UI 表示、path model、git worktree 管理だけを調べたい時。
- LLM 出力品質そのものや Codex 本体の内部挙動を検証したい時。ここで検証しているのは cmoc が Codex CLI をどう起動し、結果とログをどう扱うかに限られる。
- 実装の詳細な関数分割や設定ロード処理そのものを変更したいだけで、まず実装側の runtime module を読む方が直接的な時。

## hash
- a89550feed0daa416f3ba339ebe12988df1a9aedd060e16a786fb05443b92689

# `test_codex_runtime_home.py`

## Summary
- Codex runtime wrapper の CODEX_HOME default、既存 CODEX_HOME 維持、missing home、file home、missing auth.json の事前失敗を検証する realization test。

## Read this when
- Codex CLI 呼び出し前の CODEX_HOME 解決、環境変数引き継ぎ、auth.json validation、事前エラー文面を変更する。

## Do not read this when
- subprocess stdin/log/schema 保存や quota retry/resume の挙動を確認したい。

## hash
- edede0989727c4367d407b9fa2be3dfac723e7f2300fb9f5fda3bd51396503f4

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 呼び出しの retry 制御を検証する realization test。schema 検証失敗後の再実行、capacity 検出時の再試行、quota 検出時の availability probe と resume/rerun、並列呼び出し時の代表 probe 共有、各 call log と subcommand log の記録内容を扱う。

## Read this when
- Codex CLI 実行ラッパーの retry 条件、retry 後の成功結果、または失敗時の扱いを変更・調査するとき。
- stdout JSONL 上の capacity/quota error marker の解釈、stderr や通常出力に出た marker を retry 対象外にする境界を確認するとき。
- quota 待機後の availability probe、thread id を使った resume、resume token が無い場合の prompt 再実行、並列実行時に probe を 1 回に集約する制御を確認するとき。
- Codex call log、stdout/stderr/output path、subcommand logger の codex_call event、console 表示に記録される retry 状態や purpose を検証するとき。

## Do not read this when
- Codex CLI の通常成功パスだけを確認したいときは、retry ではない実行結果や基本ログを扱うテストを先に読む。
- 作業対象が path model、oracle/realization 分類、INDEX.md 生成規則など Codex CLI 実行 retry と無関係な仕様・ルーティングであるとき。
- Codex CLI 本体の引数組み立てや profile 設定だけを調べたい場合で、capacity/quota/schema retry や call log の retry 状態に触れないとき。

## hash
- e51aeba28342f8ed0a8dbfc509a105f56e89207aea20648b71adf155b0149a40

# `test_indexing_cli.py`

## Summary
- cmoc の indexing 機能と indexing preflight の realization test。INDEX.md 生成・更新・commit、fresh hash 時の再生成省略、壊れた既存エントリーの再生成、兄弟エントリーの並列生成、root 直下 memo の除外と入れ子 memo の対象化、git worktree 選択、Codex 呼び出し前の indexing 実行・省略条件、repository lock 待機、INDEX.md merge conflict 解消を検証する。

## Read this when
- indexing コマンド、indexing preflight、INDEX.md の生成・更新・commit、または indexing lock の挙動を変更する。
- Codex exec/TUI 呼び出し前に indexing を走らせる制御、index entry 生成時や conflict resolution 時に preflight を省略する制御を確認する。
- worktree 上での indexing 対象選択、未初期化 repository、未コミット差分、INDEX.md 以外の差分を含む repository 状態への挙動を検証する。
- INDEX.md 既存エントリーの hash freshness 判定、malformed entry の再生成、memo directory の indexing 対象境界、または sibling entry の並列処理を確認する。

## Do not read this when
- indexing 以外の CLI サブコマンドや workflow のテストだけを確認したい。
- INDEX.md エントリーの文章構造や schema そのものを調べたいだけで、生成・更新・commit・preflight の制御には触れない。
- oracle file の正本仕様や path keyword の定義を確認したいだけで、realization test の期待挙動は不要である。

## hash
- 80a020fbfa4b09b4f2139df23e82a21bcc486ce5db51253acbd75f19ac074b52

# `test_prompt_parts.py`

## Summary
- プロンプト部品とパラメータビルダーのテスト群。標準文書・ルーティング規則・ファイルアクセス規則・完全プロンプトへの補助標準注入、TUI パラメータ解決、各種ビルダーのモデル種別やファイルアクセスモードが期待通りに構成されることを検証する。
- 構造化文書の Markdown レンダリング、標準文書の主要文言、プロンプト生成時の用語書き換え、リポジトリルート解決、スキーマ内容の整合性など、プロンプト生成系の外部挙動を横断的に確認する入口になる。

## Read this when
- プロンプト生成、標準文書の組み込み、ルーティング規則、INDEX エントリー基準、レビュー基準、実装保守基準、ファイルアクセス規則の出力内容を変更する。
- 完全プロンプトに含める補助標準の有無、タイトル、禁止語の書き換え、Markdown 出力の整形規則を確認したい。
- TUI の実行パラメータ選定用プロンプト、構造化出力スキーマ、モデルクラス、推論 effort、ファイルアクセスモードの期待値を変更または確認する。
- apply fork、indexing、review oracle、session join などのビルダーが生成するパラメータの基本属性やプロンプト断片の回帰を調べる。

## Do not read this when
- 個別 CLI コマンドの実行フロー、Git 操作、ワークツリー作成、永続状態管理など、プロンプト部品生成以外の実装挙動を調べたい。
- 標準文書やプロンプトの本文仕様そのものを確認したい場合は、テストではなく該当するプロンプト部品または標準文書ビルダーの実装を直接読む方がよい。
- 特定のビルダー内部の組み立てロジックを修正する作業で、期待される回帰観点ではなく実装詳細だけを追いたい。

## hash
- 4d99e1511a5e1bcc87323f885c06ae7f3e4808c6e78d04d717f310d4a60d3aa2

# `test_review_oracle_cli.py`

## Summary
- `review oracle` コマンドの realization test。レポート生成、scope 指定、gitignored な oracle の除外、対象なし時の扱い、レビュー用 worktree で生成された索引変更の取り込み、処理失敗時のエラーレポート、INDEX.md 以外の差分拒否を、CLI の外部挙動として検証する。
- Codex 実行部分は monkeypatch で偽装し、実際の LLM 出力品質ではなく、schema ごとの制御分岐、レポート内容、git/worktree 副作用、異常時の復元境界を確認する入口になる。

## Read this when
- `review oracle` の CLI 挙動、scope の既定値や短縮オプション、生成されるレポート内容を変更・確認したいとき。
- oracle file の列挙条件、とくに gitignore 対象の oracle を full/session scope から除外する制御を確認したいとき。
- レビュー処理が作る一時 worktree、INDEX.md 変更の取り込み、INDEX.md 以外の差分拒否、失敗時レポートの挙動を変更・検証したいとき。
- Codex exec の structured output schema ごとの呼び出し順や、finding の列挙・検証・判定が CLI レポートへ反映される経路をテスト側から追いたいとき。

## Do not read this when
- oracle 正本仕様そのものの内容や編集方針を確認したいだけのとき。
- `review oracle` 以外の CLI サブコマンド、または oracle review と無関係な session/init の一般挙動を調べたいとき。
- LLM の出力品質、プロンプト本文、structured output schema の定義そのものを確認したいとき。
- テスト支援 fixture や一時リポジトリ作成 helper の実装詳細だけを調べたいとき。

## hash
- 01ece7fdd0c949051055b1a19fa264a30cb7aaded22db4187e1961d8c6ad2911

# `test_session_cli.py`

## Summary
- セッション系 CLI の fork、abandon、join の外部挙動を検証する realization test。Git branch/worktree、セッション状態 JSON、CLI 出力、Codex による join conflict resolution 呼び出し、session branch 削除失敗時の警告など、セッション操作がリポジトリ状態へ与える影響を確認する。

## Read this when
- セッションの fork が session branch と状態ファイルを作成し、home branch や開始 commit を正しく記録するかを確認したいとき。
- リンク済み worktree 上での session fork/join が、元 worktree の branch を汚さず現在の worktree の branch と HEAD を基準に動くかを調べたいとき。
- session abandon の成功時の branch 切替、session branch 削除、状態更新、利用者向け出力を変更または確認するとき。
- session abandon の失敗時、特に home branch 不在や cleanup 失敗で、branch と状態が壊れず再実行可能な形で残るかを確認したいとき。
- session join の merge/conflict 解決、Codex 実行時の file access mode、削除競合の staging、join 後の状態更新や session branch 削除警告を扱うとき。

## Do not read this when
- セッション以外の CLI コマンド、初期化処理、oracle 適用、レビュー、設定読み書きなどの挙動だけを調べるとき。
- セッション機能の実装詳細や helper の責務を確認したいだけで、テストが固定している外部挙動を確認する必要がないとき。
- Codex CLI や LLM の出力品質そのものを検証したいとき。この対象は Codex 実行を模擬し、cmoc 側の制御と副作用を検証する。

## hash
- 16c3f5afc8753d334157924e33e5c5e25050f981a4af853af339a33a740e38b7
