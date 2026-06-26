# `_support.py`

## Summary
- realization test 群で共通利用するテスト補助モジュール。Typer の CLI runner、git 操作、最小リポジトリ作成、Codex home 準備、Python 実行ファイル生成、apply 用 worktree 解決など、CLI テストの前提環境を組み立てる小さな helper をまとめている。
- 実装本体や個別サブコマンドの仕様を直接検証する本文ではなく、複数のテストが同じセットアップや状態確認を共有するための入口として位置づけられる。

## Read this when
- CLI テストで一時 git repository、初期 commit、user 設定、oracle ディレクトリ、ignored な oracle file などの共通 fixture を作る helper を確認・再利用したいとき。
- テスト内で CODEX_HOME、auth.json、実行可能な Python スクリプト、Typer CliRunner、現在 branch 名、apply branch に対応する worktree path を準備・取得する既存 helper を探すとき。
- テスト失敗の原因が共通セットアップ、git command 呼び出し、テスト用 repository の初期状態、または shared import の差し替え対象にありそうなとき。

## Do not read this when
- 個別サブコマンドの期待動作、入出力、永続状態、エラー条件を確認したいだけのときは、対象サブコマンドの実装または個別テストを読む。
- path token、sandbox mode、preflight、TUI prompt parsing などの本体ロジックを理解・変更したいときは、対応する implementation module を直接読む。
- テストケース固有の assertion や scenario を探しているときは、この共通 helper ではなく該当する test module を読む。

## hash
- f6f7fe7881a530da660ffebd31555224dfde6ff5aee8d86792527e253c949bad

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
- 基本的なランタイム挙動を横断的に確認する realization test。パス表記、時間表示、worktree 判定、設定既定値、構造化エラー表示、CLI エラー出力、補完プローブ時の副作用抑止、`.cmoc` ignore 処理、ファイルアクセスモード、Codex profile の権限設定を検証する。
- 個別機能の詳細な仕様書ではなく、cmoc の基礎部品が期待する外部挙動と制御ロジックをまとめて押さえるための入口となる。

## Read this when
- パス token 解決、repo root と work root の区別、linked worktree 上の実行判定に関わる変更を確認したいとき。
- `CmocConfig` の既定値、model class、reasoning effort、file access mode の値や sandbox mode 変換を変更するとき。
- `CmocError` の markdown 表示、空の next actions 補完、CLI 引数解析エラーや実行時エラーを stdout に出す挙動を変更するとき。
- `init` や `session fork` の preflight、current directory が work root であることの要求、shell completion probe で副作用を起こさない制御を確認するとき。
- `.cmoc` を `.gitignore` に追加する処理、既存 ignore pattern を尊重する処理、Codex profile の read/write/deny/read_only permission 構成を変更するとき。

## Do not read this when
- 特定サブコマンドの正常系フローや永続状態の詳細だけを調べたいときは、そのサブコマンドや状態管理を直接検証する対象を読む。
- oracle の正本仕様断片そのものを確認したいときは、対応する oracle doc または oracle src を読む。
- 単一 helper の内部実装だけを変更し、このテストが検証する外部挙動や制御ロジックに影響しないことが明確なときは、対象 helper の実装を直接読む。
- Codex CLI や LLM の出力品質そのものを評価したいときは、この対象は読まなくてよい。

## hash
- 194cf3aecd22facacecd521489ff755fd98432647a96bbb8bdd1585e048800f8

# `test_cli_init_tui.py`

## Summary
- CLI の初期化と対話起動まわりの外部挙動を検証する realization test。初期化時の `.cmoc` 管理対象外化、`.gitignore` 更新、既存 staged/unstaged 変更の保全、linked worktree での root/cwd/state/log の扱い、既定設定ファイルの生成と既存設定値の保持、サブコマンドログ、対話起動時のプロンプト編集・パラメータ解決・Codex 起動条件を扱う。
- Markdown プロンプト解析について、 fenced code block 内の見出し記法を見出し扱いしないこと、見出し前の本文を本文セクションとして保持することも検証する。

## Read this when
- `init` コマンドの git 操作、`.cmoc` の ignore/untrack、初期コミット、`.gitignore` への追記、既存 index/worktree 変更を壊さない挙動を変更または確認するとき。
- 初期設定ファイルの既定値、既存設定との同期、既存の人間設定値を上書きしない挙動を変更または確認するとき。
- linked worktree 上での `init` や対話起動が、main worktree 側と linked worktree 側のどちらに config・log・state・schema・complete prompt を置くかを確認するとき。
- 対話起動でエディタを開き、コメント除去済みの依頼文から実行パラメータを解決し、その結果に応じて Codex TUI を起動する流れを変更または確認するとき。
- サブコマンド起動ログの event、command、argv など、起動した CLI コマンドを識別するログ挙動を確認するとき。
- Markdown プロンプトを見出し単位に分解する処理で、コードブロック内の `#` や見出し前本文の扱いを確認するとき。

## Do not read this when
- 個別の `init` 実装内部 helper の責務やアルゴリズムだけを調べたい場合は、対応する実装ファイルを直接読む方がよい。
- 設定 schema の全項目や正本仕様上の既定値そのものを確認したい場合は、設定定義や oracle 側の該当文書を読む方がよい。
- 対話起動後の Codex/LLM の出力品質や実際の対話 UI 表示を検証したい場合は、この対象は制御ロジックのテストであり直接の入口ではない。
- Markdown 一般仕様や parser 全体の網羅的な挙動を調べたい場合は、ここで扱うのは見出し分解の限定的なケースだけなので、parser 実装またはより直接のテストを読む方がよい。

## hash
- e6b4d44cacfedc87208e49827c66651cfb7cdbeb8976627d0aa935b87643e165

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出しを包む runtime 層のテストで、exec 実行と TUI 実行が生成する引数、標準入力、環境変数、プロファイル、schema 保存先、ログ、コンソール表示を検証する。
- fake の codex コマンドや monkeypatch を使い、外部 Codex 自体ではなく cmoc 側の起動制御、記録、設定反映、作業ディレクトリ別の状態保存を確認する。

## Read this when
- run_codex_exec または run_codex_tui の挙動を変更する時。
- Codex CLI へ渡すプロンプト、引数、CODEX_HOME、profile、output schema、cwd の扱いを確認したい時。
- Codex 呼び出しログ、stdout/stderr ログ、SubcommandLogger の codex_call イベント、コンソール表示の仕様をテストで確認したい時。
- repo config の codex model や reasoning_effort が生成 profile に反映される挙動を変更または調査する時。

## Do not read this when
- Codex CLI 実行以外のサブコマンド、git 操作、path model、oracle 文書処理のテストを探している時。
- 実際の Codex CLI や LLM の出力品質、対話内容そのものを検証したい時。
- runtime 層の実装詳細を先に読みたい場合は、対応する実装ファイルを直接読む方がよい。

## hash
- 601b59c25b65ba1977e77d29c378ac64039b201e02ab969eeb5b66d9875c018c

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行ラッパーが使用する Codex home の解決と事前検証を扱う realization test。環境変数が未設定の場合は通常の home 配下を使うこと、環境変数で指定された値を CLI 呼び出し環境には保持しつつ内部では root 基準で解決すること、存在しない・ディレクトリでない・認証情報がない Codex home を Codex CLI 起動前に CmocError として失敗させることを検証する。

## Read this when
- Codex CLI 呼び出し時の CODEX_HOME の既定値、相対パス解決、子プロセスへ渡す環境変数、実行結果に記録される codex_home や profile_path の挙動を確認・変更する時。
- Codex home や auth.json の事前検証、またはそれらが不正な場合の CmocError の summary・detail・next_actions を変更する時。
- run_codex_exec が Codex CLI を呼ぶ前に認証環境を検査する制御をテストしたい時。

## Do not read this when
- Codex CLI の出力イベント解析、容量待ち、プロンプト作成、モデルや reasoning effort の選択など、Codex home の解決・検証と無関係な run_codex_exec の挙動を調べる時。
- cmoc 全体の oracle/realization 境界、INDEX.md 生成規則、またはルーティング文書の仕様を確認したい時。
- 実際の Codex CLI や LLM の出力品質そのものを検証したい時。

## hash
- 0b5e6b71990de6210a442b8915b2bf18394492d336d14f0bd7ec248f7f8736de

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーのリトライ制御を検証する realization test。構造化出力の schema validation 失敗後の再試行、capacity エラー時の再試行、quota 超過時の probe と resume/rerun、並列呼び出し時の quota probe 集約、各呼び出しログと subcommand event の記録を扱う。
- 偽の Codex 実行ファイルを一時 PATH に置き、出力 JSONL、終了コード、標準出力・標準エラー、last message ファイル、呼び出し回数を制御して、外部 Codex CLI に依存せず retry と logging の外部挙動を確認する。

## Read this when
- Codex CLI 呼び出しの retry 条件、retry 後の最終結果、または call log/subcommand log の記録内容を変更・調査する場合。
- schema validation retry、capacity retry、quota polling、quota availability probe、thread resume、resume token がない場合の rerun の挙動を確認したい場合。
- quota 超過検出を JSONL の error event に限定する境界や、stderr・通常 stdout に出た同じ文言を直接失敗として扱う挙動を確認したい場合。
- 複数の同時 Codex 呼び出しが quota 超過したとき、代表 probe を 1 回だけ実行し各呼び出しが復帰する制御を変更・検証する場合。

## Do not read this when
- Codex CLI 呼び出しの retry や quota/capacity/schema validation と無関係なサブコマンド、path 処理、oracle/realization 分類、通常の CLI 引数解析だけを調べる場合。
- 実際の retry 実装やログ出力処理そのものを読みたい場合は、先に実装側の Codex runtime を読む方が直接的である。
- Codex CLI や LLM の品質、実モデルの応答内容、ネットワーク越しの実サービス挙動を検証したい場合。この対象は偽実行ファイルで制御ロジックを検証する。

## hash
- e6c82b09811e6c3fa97a95d467f4eb4b9d09e49ed9ecc511defeb025a0ffd5e1

# `test_indexing_cli.py`

## Summary
- indexing コマンドと indexing preflight の realization test。INDEX.md 生成・再生成、fresh hash による Codex 呼び出し省略、index entry builder の structured output 利用、index path だけを commit する制御、既存の非 index 差分の保持、merge conflict 解消時の index 削除、linked worktree と cwd worktree の選択、repository lock 待機、Codex exec/TUI 呼び出し前の preflight 実行・スキップ条件を検証する。

## Read this when
- indexing コマンドの外部挙動、commit 対象、未初期化 repo での失敗、既存差分を残す挙動を変更・確認する。
- INDEX.md の entry 生成、hash freshness 判定、malformed entry の再生成、 sibling entry の並列生成、root の memo 除外と nested memo indexing の扱いを変更・確認する。
- Codex exec/TUI 実行前に indexing preflight が走る条件、index entry 生成や conflict resolution で preflight をスキップする条件、worktree 選択、repository lock 待機を変更・確認する。
- indexing が git commit、worktree、merge conflict、status clean/dirty 状態へ与える副作用の regression test を探す。

## Do not read this when
- indexing の実装詳細や helper の実装を直接変更したいだけで、期待される外部挙動や回帰条件を確認する必要がない。
- Codex runtime、path model、git wrapper、CLI framework そのものの責務を調べたい場合。
- INDEX.md 以外の機能テスト、または apply/review/session など indexing preflight と関係しないコマンド挙動を確認する場合。

## hash
- 990fe9155576e38efbd6bce4b7f47265d6c1865605145dd990955cc7ef311377

# `test_prompt_parts.py`

## Summary
- プロンプト部品と実行パラメータ生成のテスト群。レビュー基準、ルーティング規則、ファイルアクセス規則、保守基準、エントリー基準などの文書レンダリング内容と、完全プロンプトへの注入・用語書き換え・コードブロック保護を検証する。
- apply fork、indexing、review oracle、session join、TUI resolve parameter など、各 builder が期待するモデルクラス、推論努力、ファイルアクセスモード、schema、プロンプト断片を持つことを確認する入口になる。

## Read this when
- プロンプト部品の文言、見出し、Markdown レンダリング、標準文書の注入条件を変更する。
- 完全プロンプト生成で、標準文書や依頼本文の用語書き換え、コードブロック内文字列の保持、ルーティング規則の常時包含を確認したい。
- ファイルアクセスモードごとの禁止・許可文言や、各 builder が返す実行パラメータのモデル種別・推論努力・読み書きモードを変更または検証する。
- TUI の実行パラメータ選定 schema、論理 enum、必須項目、各フラグの boolean 構造に関わる変更を行う。

## Do not read this when
- 個別サブコマンドの実処理、ファイル操作、Git 操作などの実装挙動だけを調べたい場合。
- 正本仕様断片そのものの記述方針を確認したい場合。テスト期待値ではなく仕様文書側を読む方が直接的である。
- 特定の prompt part や builder の実装詳細を修正するだけで、期待される外部挙動や回帰テストを確認する必要がまだない場合。

## hash
- 42d8c30786067c047e75f73fc40b727a8b55278cf61b81a47744002934f96ff8

# `test_review_oracle_cli.py`

## Summary
- `review oracle` の CLI 挙動を検証する realization test。レビュー対象 oracle の選定、レポート出力、Codex 呼び出し制御、レビュー用 worktree からの `INDEX.md` 反映、失敗時レポート、`INDEX.md` 以外の差分拒否を扱う。

## Read this when
- `review oracle` コマンドの外部挙動、終了コード、標準出力、生成レポート内容を変更・確認するとき。
- レビュー範囲の既定値、`full` 指定、短い scope option、session scope で対象がない場合の扱いを確認するとき。
- gitignored な oracle file を full scope や session scope のレビュー対象から除外する制御を変更するとき。
- oracle ごとの発見事項列挙ループで、別 oracle の発見事項をプロンプトへ混ぜない制御を確認するとき。
- レビュー用 worktree で生成された `INDEX.md` だけを元 worktree に反映し、その他の差分を拒否する処理を変更するとき。
- レビュー処理中の例外で error report を残し、未判定 finding を通常の却下結果として扱わない挙動を確認するとき。

## Do not read this when
- `review oracle` 以外の CLI コマンド、session 作成、init 処理そのものの仕様を調べたいとき。
- oracle 本文の正本仕様や、oracle file と realization file の定義を確認したいとき。
- Codex 実行 wrapper の低レベルな引数組み立て、外部プロセス実行、設定読み込みの実装だけを調べたいとき。
- レビュー finding の判定基準や LLM 出力品質そのものを確認したいとき。

## hash
- cdfbee61f9eb8ba6aef5748350f8b40b1a426e6836a8d9eb2bf9acf872581815

# `test_session_cli.py`

## Summary
- session サブコマンドの CLI 挙動を検証する realization test。session fork による session branch と状態ファイル作成、linked worktree 上の fork/join、session abandon の正常系・失敗時ロールバック、session join の conflict 解決・削除 conflict・session branch 削除失敗時の出力を扱う。
- Git 操作、状態 JSON、Typer runner、Codex 実行の monkeypatch を組み合わせ、session lifecycle が branch・worktree・永続状態・利用者向け出力へ与える影響を確認する入口。

## Read this when
- session fork、session abandon、session join の外部挙動や回帰テストを確認・変更したいとき。
- session branch 名、session home branch、session start commit、active/joined/abandoned などの session 状態更新が期待どおりか確認したいとき。
- linked worktree 上で session 操作した場合に、元 worktree と linked worktree の branch がどう保たれるか確認したいとき。
- session join の merge conflict 解決で Codex 実行に渡す file access mode や writable paths、解決後の staging 状態を確認したいとき。
- session abandon や session join の cleanup 失敗時に、branch・状態ファイル・CLI 出力がどう扱われるかを確認したいとき。

## Do not read this when
- session 機能以外の CLI サブコマンドや一般的な init 処理だけを調べたいとき。
- session の正本仕様断片を確認したいとき。実装やテストではなく oracle 側の該当文書を読む方が適切。
- session 操作の内部実装、状態ファイル schema の定義、Git helper、Codex 実行 wrapper の実装詳細を直接変更したいとき。
- INDEX.md 生成規則やルーティング文書の形式そのものを調べたいとき。

## hash
- 57ee23478d5674d43603726d688fea5594fab2e5dcc4e6b44946b8b92698fda7
