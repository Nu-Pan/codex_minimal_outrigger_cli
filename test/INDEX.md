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
- apply join の CLI 挙動を、実際の git リポジトリと Typer runner を使って検証する realization test。apply worktree と apply branch の削除、session state の ready 復帰、oracle snapshot commit の記録、join report の生成を確認する。
- apply worktree 内から join した場合の作業ディレクトリ復帰、未コミット差分がある apply worktree での中断、ログ出力先、エラーメッセージの stdout/stderr 境界を検証する。
- apply 側の想定外差分、force-resolve による巻き戻し、許容される .gitignore 差分、通常ファイルの未解決 merge conflict、INDEX.md conflict の通常モード自動解決後の継続を扱う。

## Read this when
- apply join の終了後クリーンアップ、状態ファイル更新、report 生成、apply branch/worktree 削除の挙動を変更または確認したいとき。
- apply worktree から apply join を実行する経路、dirty worktree 検出、エラー表示先、sub_command log の保存先に関わる実装を触るとき。
- apply join の差分検査、想定外差分の検出、force-resolve、merge conflict レポート、INDEX.md conflict 処理の外部挙動を確認したいとき。

## Do not read this when
- apply fork や session fork の単独仕様を確認したいだけで、join 時の状態遷移や cleanup には触れないとき。
- Codex 実行結果の品質や LLM 出力内容そのものを検証したいとき。このテストは Codex 実行を fake に差し替え、join 制御ロジックを検証している。
- oracle file の正本仕様や INDEX.md 生成ルールを確認したいとき。ここは realization test であり、正本仕様の入口ではない。

## hash
- 0684dc6984286983dc9024be887edf2900caef81da2ef9228b93c6e7621f9230

# `test_basic_runtime.py`

## Summary
- cmoc の基本的な実行時挙動を横断的に検証する realization test。パス表記の解決、時間表示、Git worktree における root 判定、設定既定値、構造化エラー表示、CLI エラー出力、補完プローブ時の副作用抑止、.cmoc ignore 設定、file access mode と sandbox mode の対応、Codex profile の権限制御を扱う。
- 単一機能の詳細テストというより、runtime・CLI preflight・権限 profile・補助関数の基本契約が壊れていないかを確認する入口として位置づけられる。

## Read this when
- path token と実パスの相互解決、repo root と work root の判定、linked worktree 上の挙動を変更・確認したいとき。
- CmocConfig の既定値、model class、reasoning effort、file access mode、sandbox mode、Codex profile の permission profile を変更・確認したいとき。
- CmocError の markdown 表示、CLI 引数解析エラー、preflight エラー、stdout/stderr の出し分けを変更・確認したいとき。
- completion probe 実行時に cmoc preflight や .gitignore/.cmoc 生成などの副作用を避ける挙動を確認したいとき。
- ensure_cmoc_ignored による .gitignore 更新、既存 ignore pattern を尊重する挙動、git check-ignore との関係を確認したいとき。

## Do not read this when
- 個別サブコマンドの正常系ワークフローや永続状態の詳細を確認したいだけのときは、その機能に対応する CLI または runtime のより直接的なテストを読む。
- oracle file の正本仕様や文書方針を確認したいときは、実装テストではなく oracle 側の本文を読む。
- UI 表示、LLM 出力品質、または Codex CLI 自体の外部挙動を検証したいときは、このテストの対象外。
- 特定 helper の内部実装手順だけを調べたいときは、ここでは外部契約だけを確認し、必要に応じて対応する実装本文へ進む。

## hash
- e4e46f2e8d05f15bbbc375037b905b39a267ea5adb3bcf1bfbf8d9eae531d897

# `test_cli_init_tui.py`

## Summary
- CLI の初期化処理と対話型起動処理に対する realization test。既存の `.cmoc` 管理対象の untrack、`.gitignore` 更新、初期化 commit、既存 staged/unstaged 変更の保持、リンク worktree からの初期化、既定設定の生成と既存設定値の保持を検証する。
- 対話型起動では、エディタで作成された依頼文から不要な HTML コメントを除去し、パラメータ解決用 Codex 実行と TUI Codex 起動へ適切な parameter・cwd・root・ログ保存先を渡すことを検証する。
- Markdown prompt parser が fenced code block 内の見出し風テキストを見出し扱いしないこと、見出し前の本文を preamble として保持することも検証する。

## Read this when
- `init` サブコマンドの git 操作、副作用、`.cmoc` ignore、初期 commit、設定ファイル生成、既存変更の保護に関する挙動を確認・変更する時。
- リンク worktree 上で `init` または `tui` を実行した場合に、メイン worktree とリンク worktreeのどちらへ `.cmoc` 状態・ログ・schema・設定を書き込むかを確認する時。
- `tui` サブコマンドで、エディタ起動、依頼文の補完、コメント除去、パラメータ解決、Codex TUI 起動、ログファイル保存の流れを変更する時。
- Markdown 依頼文を章構造へ分解する parser の、fenced code block と見出し前本文の扱いを変更する時。

## Do not read this when
- CLI の `init`・`tui`・Markdown prompt parsing に関係しないサブコマンドや機能のテストを探している時。
- 正本仕様そのもの、実装本体、または helper の詳細な実装を読みたい時。この対象は挙動検証であり、仕様判断や実装変更の入口としては対応する oracle file や `src` 側の本文を優先する。
- Codex CLI や外部エディタの実物挙動を網羅的に確認したい時。この対象は fake executable と monkeypatch による制御ロジック検証に絞っている。

## hash
- d7dee94d4169a2e6503082451f449b9fba5530ef2f60979de74e4973a7dea9cc

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出しを包む runtime 層の realization test。exec 実行ではプロンプトを stdin で渡し、出力 schema・profile・CODEX_HOME・ログ・Structured Output の読み取りが期待どおりになることを検証する。
- worktree 上の cwd で exec した場合に、schema の保存先が実行 cwd 側の work root 配下になり、call log は repo root 側のログ領域に残ることを検証する。
- TUI 起動では exec サブコマンドを使わず、プロンプトをコマンド引数として渡し、capture しない subprocess 呼び出し、sandbox profile、call log、subcommand log、コンソール表示を検証する。
- repo 設定から Codex model と reasoning effort を読み込み、生成 profile に反映されることを検証する。

## Read this when
- Codex CLI の exec/TUI 呼び出し方法、引数構成、stdin と prompt 引数の使い分けを変更・確認するとき。
- Codex 呼び出し用 profile、CODEX_HOME、sandbox writable/read-only paths、repo 設定の反映を扱う runtime 実装を変更するとき。
- Codex 呼び出しログ、stdout/stderr ログ、subcommand log、コンソール表示、call result オブジェクトの挙動を変更・確認するとき。
- output schema のコピー先、worktree を cwd にした実行、Structured Output 読み取りの挙動を確認するとき。

## Do not read this when
- Codex CLI 呼び出しではなく、Git 操作、path model、INDEX 生成、oracle review など別領域の挙動だけを確認するとき。
- runtime 実装の外部挙動ではなく、テスト補助関数や fixture の定義そのものを調べたいときは、補助モジュールを直接読む。
- Codex や LLM の回答品質そのもの、プロンプト本文の内容設計、モデル選定方針の正本仕様を調べたいとき。

## hash
- 54ece639c73e67bed45444024eb270fe150d0625555e82d2972edac42103076f

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
- プロンプト部品とパラメータ生成のテスト群であり、レビュー基準、ルーティング規則、ファイルアクセス規則、INDEX エントリー基準などが構造化文書として期待語句を含んで描画されることを検証する。
- 完全なプロンプト生成が、指定された補助基準を含める条件、既定では省略する条件、Codex CLI 向けに禁止語を除去する条件、ルーティング規則を常に含む条件を満たすことを確認する。
- apply fork、TUI resolve、indexing、review oracle、session join などのパラメータビルダーが、想定するモデルクラス、推論量、ファイルアクセスモード、スキーマ、作業ツリー表記を使うことを検証する。

## Read this when
- プロンプト部品の文言、構造化文書のタイトル、Markdown 描画結果、または空行正規化の期待挙動を変更・確認したいとき。
- 完全なプロンプトに含める補助基準のオンオフ、Codex CLI 向け文言変換、ルーティング規則の常時挿入、ファイルアクセス規則のモード別出力を調べるとき。
- apply fork、TUI resolve、indexing、review oracle、session join の各パラメータ生成で、モデル種別、reasoning effort、file access mode、スキーマ、プロンプト本文への埋め込み内容が壊れていないか確認するとき。

## Do not read this when
- 個別のプロンプト部品やビルダーの実装を変更したいだけで、テストが期待する外部挙動や文言断片を確認する必要がないとき。
- CLI コマンド実行、永続状態、Git 操作、作業ツリー作成など、プロンプト生成以外の機能テストを探しているとき。
- INDEX エントリーの生成基準そのものの仕様を読みたいとき。ここでは基準文書の描画結果と完全プロンプトへの挿入だけを検証している。

## hash
- b638b246cff591c590e30db000e391bbad9e672e2504a46427ba76a82a3e5966

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
