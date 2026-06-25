# `_support.py`

## Summary
- realization test で共有される補助コードであり、Git 操作、最小リポジトリ作成、CODEX_HOME の一時設定、apply 用 worktree 解決など、複数テストから再利用する setup/helper をまとめている。
- CLI runner、主要コマンド module、runtime helper、path model、設定型、ACP 型をテストから扱えるように import し、テスト本文側が共通準備処理を重複して持たないための入口になっている。

## Read this when
- テスト内で一時 Git リポジトリを作る、初期 commit 済みの fixture repo を用意する、現在 branch を確認するなど、Git 前提の共通 setup を使うまたは変更する場合。
- CODEX_HOME をテスト用に差し替える処理、auth.json を含む一時 Codex home の作成、monkeypatch による環境変数設定を確認する場合。
- apply 系テストで保存状態から apply branch の worktree path を導く補助処理を使うまたは変更する場合。
- テストで Typer CLI runner や cmoc runtime、主要 subcommand module、path token 解決、ACP/config 型を共通 import している前提を確認する場合。
- 複数のテストに同じ setup 処理を追加しようとしており、既存 helper に統合できるか判断する場合。

## Do not read this when
- 個別コマンドの期待挙動や assertion を確認したいだけの場合は、対象コマンドのテスト本文を読む。
- cmoc runtime や subcommand の実装仕様を確認したい場合は、実装側の該当 module を読む。
- path token の意味、repo/work root の仕様、sandbox mode 変換などの本体ロジックを調べる場合は、この共有 test helper ではなく実装側の定義を読む。
- INDEX 生成、oracle 仕様、またはルーティング文書の方針を調べる場合は、このテスト補助 module ではなく該当する仕様・実装・テストを読む。

## hash
- fd14d4042fff7ffe5c0d41d27c044e396963aa5a32afb82508bf9b28afe2cd43

# `test_apply_abandon_cli.py`

## Summary
- `apply abandon` コマンドの realization test。apply run 破棄時に apply worktree と apply branch を掃除し、状態を `ready` に戻す外部挙動を CLI 経由で検証する。
- cleanup 対象が既に消えている場合の warning、running 状態の process 停止、process id 不在時の拒否、apply worktree を導出できない状態の拒否、apply worktree 内からの実行、stale apply branch からの誤破棄拒否を扱う。

## Read this when
- `apply abandon` の CLI 挙動、出力文言、終了コード、session state の更新、apply worktree・apply branch の削除条件を変更または確認するとき。
- apply run の running/completed/ready 状態遷移、apply process id の扱い、cleanup 失敗や対象欠落時の warning/error 境界を確認するとき。
- 現在位置が apply worktree や stale apply branch の場合に、破棄対象をどう判定するかを調べるとき。

## Do not read this when
- `apply fork` の生成処理そのもの、Codex 実行結果の品質、review findings の内容を調べたいだけのとき。
- session fork、init、git worktree helper など、apply abandon 以外の CLI 基盤挙動を直接確認したいとき。
- oracle file の正本仕様を確認したいとき、または実装ファイル側の内部関数分割や helper 実装を読むべきとき。

## hash
- d9e1345db5eb3885badbb85781e46d4b37406d7a34cec2b8daeecf11b6b48904

# `test_apply_fork_cli.py`

## Summary
- apply fork の CLI 挙動を検証する realization test。Codex 呼び出しループ、apply 用 worktree/state/branch の更新、report 生成、dirty file 再検査、編集禁止対象の検出、rolling apply fork の対象選択など、apply fork の外部挙動と制御ロジックを扱う。

## Read this when
- apply fork の成功時に session state、apply branch、worktree、pid 管理がどう更新・削除されるべきかを確認したいとき。
- apply fork が Codex の所見列挙、所見適用、commit message 生成、変更要約生成をどの目的で呼び分けるかを検証したいとき。
- apply fork が既存の ignore 表現を session 側で書き換えないこと、または所見対象としての ignore file を apply branch 側で編集できることを確認したいとき。
- 設定読み込み失敗時に apply run を開始せず、ready state と branch 未作成を保つ挙動を確認したいとき。
- apply 対象の正規化で root 直下の private memo を除外し、入れ子の memo directory を対象に残す挙動を確認したいとき。
- 未収束・収束・error の apply report に、結果、終了理由、変更要約、commit message、return code がどう反映されるかを確認したいとき。
- apply 後の dirty file を再検査し、生成された routing document を再検査対象から外す制御を確認したいとき。
- 編集禁止対象への差分を検出した場合に、error state と report へ落とし込み、変更要約生成を行わない挙動を確認したいとき。
- rolling apply fork が前回 apply の oracle snapshot commit を基準に対象を選び、join 済み snapshot 情報を session state に反映する挙動を確認したいとき。

## Do not read this when
- apply fork 以外の apply/join/session/init コマンド全般の仕様や実装入口を探しているだけのとき。
- Codex 実行 wrapper や structured output schema の詳細実装を確認したいとき。
- report renderer、state model、path model、git helper などの個別実装を直接変更したいとき。
- oracle file や routing document の正本仕様を確認したいとき。
- 単体 helper の内部アルゴリズムだけを調べたい場合で、apply fork CLI の end-to-end な外部挙動や state/report 副作用を確認する必要がないとき。

## hash
- 8885974189de0d9ca5a841eb1c60cdf3bfc24cc1eef0dfce3aae8a71a23cf457

# `test_apply_join_cli.py`

## Summary
- `apply join` の CLI 挙動を検証する realization test。apply worktree の削除、apply branch の削除、session state の ready 復帰、oracle snapshot commit の記録、report 生成、作業ディレクトリ復帰、未コミット差分・想定外差分・merge conflict・INDEX.md conflict の扱いを、実際の git repository と CLI runner で確認する。

## Read this when
- `apply join` の外部挙動、終了コード、標準出力、report 内容、state 更新、worktree/branch cleanup を変更または確認する場合。
- apply worktree から `apply join` を実行したときの cwd 復帰、cleanliness check、ログ保存先を確認する場合。
- apply 側の oracle 変更、`.gitignore` 変更、通常 merge conflict、INDEX.md conflict、`--force-resolve` の扱いに関する回帰テストを確認する場合。

## Do not read this when
- `apply fork` の Codex 実行内容そのものや fork 作成処理だけを確認したい場合。
- session 作成、path model、state schema、git helper の単体仕様を調べたい場合。
- oracle file の正本仕様や自然言語仕様を確認したい場合。

## hash
- 151af6278fea5ccce789f55154a543387ee602c7adbd4164e8c56c660d66cb68

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
- CLI の初期化と TUI 起動フローの外部挙動を検証する realization test。初期化時の既存状態保護、`.cmoc` の無視設定、既定設定の生成と同期、sub command ログ、linked worktree での保存先、TUI が editor 入力からパラメータ解決と Codex 起動へ進む経路、Markdown prompt 解析の境界を扱う。

## Read this when
- `cmoc init` の git 操作、`.gitignore` 更新、`.cmoc` 配下の追跡解除、初期化 commit、既存 staged/unstaged 変更の保護を変更する。
- 既定 `config.json` の生成内容、既存設定への default 補完、人間が書いた設定値を上書きしない挙動を変更する。
- sub command ログ、TUI prompt ログ、linked worktree 実行時の root/cwd、schema や complete prompt の保存場所を変更する。
- TUI で editor が書いた依頼文を整形し、パラメータ解決用 Codex 実行と本体 Codex TUI 起動へ渡す制御を変更する。
- Markdown prompt parser の見出し抽出、fenced code block 内の見出し無視、見出し前本文の扱いを変更する。

## Do not read this when
- 対象が `init`、`tui`、Markdown prompt parser の外部挙動ではなく、別サブコマンド固有の CLI 挙動である。
- 設定 schema の定義そのものや model 名の正本仕様を確認したいだけで、初期化時にそれが書き込まれる挙動を検証しない。
- git helper、path model、Codex 実行 wrapper などの内部実装だけを局所的に読むべきで、ここで検証している外部副作用や制御フローに関係しない。
- TUI の見た目や対話 UI の詳細を調べたいだけで、editor 入力、prompt 保存、パラメータ解決、Codex 起動の結合挙動を扱わない。

## hash
- c020984aa7c0a50641148ddf9c370da58dfe96b64616db432f84bc8086663d75

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出しラッパーの実行時挙動を検証する realization test。exec 経路ではプロンプトを stdin 経由で渡すこと、構造化出力 schema とログ保存先、CODEX_HOME、profile 生成、subcommand log、console 表示を確認する。TUI 経路では prompt 引数、profile の sandbox 設定、call log、subcommand log、標準出力・標準エラーの扱いを確認する。
- worktree 上で exec を実行した場合に schema が cwd 側の work root 配下へ保存され、repo root 側へ不要な schema 状態を作らないことも扱う。repo の config.json が Codex profile の model と reasoning_effort に反映されることを検証する入口でもある。

## Read this when
- Codex CLI を起動する runtime ラッパー、特に exec/TUI の argv、stdin、cwd、env、profile、output schema、ログ出力の外部挙動を変更または調査するとき。
- AgentCallParameter の model class、reasoning effort、file access mode が Codex profile や起動引数へどう反映されるかをテスト側から確認したいとき。
- worktree 内の cwd で Codex exec を実行する場合の schema 保存場所や、repo root と work root の使い分けを確認するとき。
- Codex 呼び出しの subcommand log、call log、stdout/stderr log、console summary の期待値を更新する必要があるとき。
- repo の config.json から Codex 用 model 名や reasoning_effort が読み込まれる挙動を変更するとき。

## Do not read this when
- Codex CLI 呼び出しではなく、一般的な path model、oracle/realization 分類、INDEX.md 生成規則そのものを調べるとき。
- Git 操作、worktree 作成、Codex home setup、SubcommandLogger などの test fixture/helper の実装詳細だけを確認したいとき。
- 個別サブコマンドの業務ロジック、LLM 出力内容の品質、または Codex CLI 以外の外部コマンド実行を調査するとき。
- 実装ファイル側の責務分割や helper の内部設計だけを変更し、exec/TUI の公開的な起動引数・環境・保存ログ・schema 配置の期待値に影響しないとき。

## hash
- 87586292dfbc07fbd1d30b8dc9fc7a26338516225d73c433dddcbef9ce61395f

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行ラッパーが使用する Codex home の決定と事前検証を扱う realization test。環境変数未設定時は通常の home 配下を使うこと、環境変数設定時はその値を Codex CLI 呼び出し環境に保ちながら解決済みの保存先・ログへ反映することを検証する。
- Codex home が存在しない、ディレクトリではない、または認証情報を欠く場合に、Codex CLI を起動する前に利用者向けの CmocError として失敗する境界を検証する。

## Read this when
- Codex CLI 実行時の CODEX_HOME の扱い、既定の Codex home、相対パス指定、実行プロファイルの保存先、または呼び出しログに記録される Codex home を変更・調査する場合。
- Codex CLI 起動前に行う Codex home と認証情報の検証、またはその失敗時のエラー文言・next_actions を変更・調査する場合。
- run_codex_exec が fake Codex CLI に渡す環境変数や引数と、戻り値に含まれる codex_home・profile_path・call_log_path の関係を確認する場合。

## Do not read this when
- Codex home や CODEX_HOME に関係しない AgentCallParameter、モデル選択、reasoning effort、ファイルアクセスモードの仕様だけを確認したい場合。
- Codex CLI の実出力品質、LLM 応答内容、または実際の認証フローそのものを検証したい場合。
- リポジトリ作成 fixture やテスト支援 API の一般的な使い方を知りたいだけで、Codex home の実行時解決や事前検証に触れない場合。

## hash
- 4327dbfd51651c594d492426c94c5d67c607cbb145b3823973c827bd0b17f59c

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーの retry 制御を検証する realization test。schema validation 失敗後の再実行、capacity エラー時の再試行、quota 超過時の probe と resume/rerun、並列呼び出し時の代表 probe 共有、各試行の call log と subcommand log の記録を扱う。

## Read this when
- Codex CLI 呼び出しで、semantic output の schema validation 失敗後に再試行される挙動を確認・変更したいとき。
- capacity エラーや quota 超過を stdout JSONL の error event から検出し、再試行・待機・probe・resume を行う制御ロジックを確認・変更したいとき。
- Codex CLI 呼び出しごとの call log、stdout/stderr/output path、subcommand log event の status・purpose・returncode を検証したいとき。
- quota 超過後に thread id がある場合は resume し、ない場合は元 prompt で再実行する挙動を確認したいとき。
- 複数の Codex CLI 呼び出しが同時に quota 超過した場合に、availability probe を代表 1 回に抑える制御を確認したいとき。

## Do not read this when
- Codex CLI に渡す profile、sandbox、model、reasoning effort などの基本 argv 構築だけを確認したいとき。
- Codex CLI retry ではなく、通常成功時の出力取得や単純な失敗時エラー変換だけを確認したいとき。
- oracle file の正本仕様や routing 文書の記述方針を確認したいとき。
- 実際の Codex CLI や LLM の品質を評価したいとき。

## hash
- 42de0686524bd03c457bf927ed774826d01b851b710bbbbbfbb7a878ac0c9906

# `test_indexing_cli.py`

## Summary
- indexing コマンドと indexing preflight の realization test。INDEX.md 生成・更新・コミット、既存差分や未初期化 repository の扱い、linked worktree 対象化、fresh hash による再生成スキップ、INDEX.md conflict 解消、preflight lock 待機、Codex 呼び出し前の indexing 実行条件を検証する。

## Read this when
- indexing コマンドの CLI 挙動、INDEX.md の生成・更新・コミット条件、または dirty repository での失敗条件を確認・変更するとき。
- indexing preflight が Codex exec/TUI 呼び出し前に走る条件、skip される purpose、repository lock、linked worktree 選択を確認・変更するとき。
- 既存 INDEX.md の hash が fresh な場合の再生成スキップ、malformed entry の再生成、兄弟 entry の並列生成、memo directory の index 対象境界を確認・変更するとき。
- INDEX.md merge conflict の自動解消や、index path だけを commit して非 index 差分を残す制御を確認・変更するとき。

## Do not read this when
- indexing の実装詳細だけを追う場合は、対応する実装 module を先に読む。
- Codex 実行 parameter、runtime 呼び出し、git helper、test fixture の一般的な定義だけを確認したい場合は、共通 test support や対象 module を読む。
- INDEX.md エントリー本文の品質や routing 文書の一般規則だけを確認したい場合は、oracle の index entry 仕様を読む。

## hash
- 7b6f4d0473be3be54e2aadc0cadb8f3addfe8631d5f0f04d2bf05512eaadab35

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
- `cmoc review oracle` の CLI 挙動を検証する realization test。oracle レビューのレポート生成、scope 指定、gitignore 対象の除外、レビュー用 worktree で生成されたルーティング文書変更の取り込み、処理失敗時のエラーレポート、許可外差分の拒否を扱う。
- Codex 実行を fake に差し替え、実際の LLM 出力ではなく review oracle コマンドの制御フロー、出力レポート、git/worktree 副作用を確認するための入口になる。

## Read this when
- `cmoc review oracle` の外部挙動、レポート内容、終了コード、scope の扱いを変更または調査する場合。
- oracle file の列挙対象から gitignore 対象を除外する制御、session scope と full scope の対象数・no targets 判定を確認する場合。
- review oracle が Codex 実行用 worktree で生成した `INDEX.md` 変更だけを本体へ反映し、それ以外の差分を拒否する挙動を確認する場合。
- review oracle の処理途中失敗時に、未判定 finding を採用せずエラーレポートを出す挙動を確認する場合。

## Do not read this when
- oracle file や realization file の概念定義、正本仕様としての要求を確認したい場合は、仕様側の本文を読む。
- review oracle 以外の CLI サブコマンド、通常の session 操作、init 処理だけを調査する場合は、より直接対応するテストまたは実装を読む。
- Codex CLI や LLM の出力品質そのもの、finding の文章生成品質を調査する場合。この対象は Codex 実行を fake 化して制御ロジックだけを検証している。

## hash
- 337e9d9093302123e389539d0757df9c21ed3d1e7344e8bccc0739c7fb85e4cc

# `test_session_cli.py`

## Summary
- session サブコマンドの CLI 挙動を検証する realization test。session fork による session branch・状態ファイル作成、linked worktree 上での fork、session abandon の成功・失敗・cleanup 失敗時の復旧、session join の merge/conflict 解決・linked worktree・削除競合・branch 削除失敗警告を扱う。
- Git repository と worktree を実際に作成し、Typer runner、git コマンド、状態 JSON、Codex conflict resolution 呼び出しの monkeypatch を通して、利用者から見える branch 遷移・状態遷移・出力・作業ツリー内容を確認する入口。

## Read this when
- session fork / abandon / join の CLI 挙動、branch 操作、状態 JSON の更新、session home branch や session start commit の扱いを変更・調査するとき。
- linked worktree で session 操作を実行した場合に、root 側 branch を維持しつつ linked 側の current branch・commit・状態がどう扱われるかを確認するとき。
- session abandon の失敗時出力、home branch 不在時の非破壊性、cleanup 失敗時の state rollback と session branch 維持を検証するとき。
- session join の conflict resolution で Codex 実行が呼ばれる条件、file access mode、解決後の stage 状態、home branch への切り替え、session branch 削除失敗時の警告を確認するとき。

## Do not read this when
- session 以外の CLI サブコマンドや、init・apply・review など独立した機能の挙動だけを調べたいとき。
- CLI の外部挙動ではなく、内部 helper の単体ロジック、path model、runtime command wrapper などの実装詳細だけを確認したいとき。
- Codex CLI や LLM の出力品質そのものを検証したいとき。この対象は conflict resolution 呼び出しとその副作用を fake で確認するだけで、生成品質は扱わない。

## hash
- fa29ae5f52aef12140f003927bf2db689352b51ef2c8ef0cc84aa3458fdfdf31
