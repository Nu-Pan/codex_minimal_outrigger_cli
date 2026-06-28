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
- apply abandon を CLI 経由で実行したときの active apply run 破棄の外部挙動を検証する realization test。
- completed/running apply run の worktree・branch・session state cleanup、cleanup 対象欠落時の警告、running process と記録済み child process の停止順、PID reuse や raced exit の扱いを固定する。
- repo root、apply worktree、linked session/apply worktree、stale apply branch など実行位置ごとの abandon 境界条件を扱う。

## Read this when
- apply abandon の成功時に apply worktree・apply branch・state・process id 記録がどう削除または ready 化されるかを確認したいとき。
- running apply process の停止、child process group の停止順、pidfd signal、PID reuse、終了済み process の許容に関する制御ロジックを変更するとき。
- apply abandon をどの worktree から実行できるか、linked session の state をどう正として扱うか、stale apply branch をどう拒否するかを確認するとき。
- cleanup 対象が先に消えている場合の warning 出力や、破損 state・process identity 欠落・dirty linked session worktree の拒否条件を変更するとき。

## Do not read this when
- apply fork の生成処理そのもの、Codex 実行結果の解釈、findings の扱いを調べたいだけのとき。
- apply abandon 以外の session fork、init、merge などの CLI 挙動を確認したいとき。
- oracle の正本仕様断片を確認したいとき。この対象は realization test であり、正本仕様ではない。
- process 停止や worktree cleanup を伴わない単純な path model、INDEX 生成、補助 fixture の責務を調べたいとき。

## hash
- f7e3591b4969ab79a729de5928c6ee1e9d8461e0eacdbfe6f0afb89f877c50a7

# `test_apply_fork_cli.py`

## Summary
- apply fork の CLI 経路と内部 body が、Codex 実行ループ、apply run の branch/state/worktree 更新、linked worktree 起点、設定読み込み失敗時の中断、.cmoc ignore 処理、.gitignore 編集対象化、target 正規化を期待どおり扱うことを検証する realization test。
- session fork 後に apply fork を実行したとき、apply state が completed になり、apply branch と run_id 別 worktree が作られ、旧 apply_worktree/apply_process_id/pid が残らず、所見列挙が呼ばれることを確認する。
- linked worktree 上で開始した session branch と HEAD commit を apply run の起点にし、apply worktree は linked worktree 配下ではなく cmoc 管理 worktree 配下へ作ることを確認する。
- apply fork が session 側の既存 .gitignore 表現を書き換えないこと、未 ignore の .cmoc は git info exclude で clean にすること、所見対象としての .gitignore は apply branch 側で編集できることを確認する。
- target 正規化について、root 直下 memo は除外しつつ入れ子の memo directory は残し、binary file も file 種別だけでは除外しないことを確認する。

## Read this when
- apply fork の外部挙動、state 遷移、apply branch 名、apply worktree 配置、apply_process pid の後始末に関するテスト期待値を確認したいとき。
- linked worktree から apply fork を走らせる場合の oracle snapshot commit、apply branch の開始 commit、worktree 配置の期待値を確認したいとき。
- apply fork 実行時の .cmoc ignore 処理、session 側 .gitignore の保持、git info exclude への追加、.gitignore 自体を所見対象として編集する挙動を確認したいとき。
- cmoc config が壊れている、または存在しない場合に、apply run の branch/state/pid を開始せず stdout にエラーを出す挙動を確認したいとき。
- apply fork の target 正規化で root 直下 memo、入れ子の memo directory、binary file、oracle 配下 file の扱いを確認したいとき。
- Codex 実行を fake に差し替えて apply fork の制御フローや副作用をテストする既存パターンを参照したいとき。

## Do not read this when
- apply fork の実装本体、永続 state の読み書き helper、git worktree 作成処理、Codex 呼び出し処理を変更したいだけで、テスト期待値ではなく実装詳細を確認したいとき。
- session fork、init、git helper、runner fixture など apply fork 以外の CLI テスト基盤そのものを調べたいとき。
- apply fork 以外の apply サブコマンド、review、oracle、path model などの仕様やテストを探しているとき。
- Codex CLI や LLM 出力品質そのものの検証方針を知りたいとき。この対象は Codex 実行結果を fake 化し、apply fork 側の制御と副作用だけを検証する。

## hash
- afa9543f71fb61a087b92aa30f464282ad3d4815a4d75b7a289e83836f07ff5d

# `test_apply_fork_report_cli.py`

## Summary
- apply fork を CLI から実行したときの report 生成、収束判定、再検査対象の制御、error report、session state 更新をまとめて検証する realization test。所見列挙、所見適用、commit message、変更要約、report schema の観測が同じ制御 loop に閉じるため、apply fork report 周辺の期待値を一箇所で読む入口になる。
- 未追跡 file を含む fork 後差分の抽出、fallback 変更要約、編集禁止対象差分の error 化、rolling apply fork が前回 apply join 後の変更だけを対象にすることも、この report 制御の一部として扱う。

## Read this when
- apply fork の CLI 実行結果、exit code、stdout に出る report path、report 本文の result や Finding Count、変更要約表示を確認したいとき。
- apply fork が所見適用後に変更 file を再調査する条件、INDEX.md を再調査対象から外す条件、上限到達時の converged/unconverged 判定を変更・検証するとき。
- apply fork の所見適用が差分を作らない場合、commit message 生成を行わないことや apply branch が進まないことを確認したいとき。
- apply fork 中に編集禁止対象の差分が発生した場合の stderr、error state、error report、未 commit 差分を含む変更要約を扱うとき。
- apply fork report 用の fork 後差分検出が未追跡 file を含むか、変更 path fallback summary がどう作られるかを確認したいとき。
- rolling apply fork の調査対象が前回 apply join 後の変更に限定されることや、session state の apply join snapshot 更新との関係を確認したいとき。

## Do not read this when
- apply fork の内部実装だけを局所的に変更したく、CLI 経由の report・session state・git commit まで含む外部挙動を確認する必要がないとき。
- apply join、session fork、init などの個別 command 自体の仕様や挙動を調べたいだけで、apply fork report 制御との結合を扱わないとき。
- Codex 実行 wrapper、AgentCallParameter、structured output schema の一般的な仕組みを調べたいだけで、この test が fake している apply fork 用応答の期待値に関心がないとき。
- INDEX.md 生成やルーティング文書そのものの挙動を調べたいとき。ただし apply fork の再調査対象から INDEX.md を除外する挙動を扱う場合は読む。

## hash
- 3d2195a4f9374476ac5893c8dae8c254ce0881d062e97b288c12587a508518fc

# `test_apply_join_cli.py`

## Summary
- apply run を session へ join する CLI 外部挙動を検証する realization test。成功時の apply worktree と branch の後片付け、session state 更新、report 生成、linked session worktree への merge 先、join 実行位置の扱いを確認する。
- dirty な apply worktree、同一 session の stale apply branch、想定外差分、merge conflict、force resolve、削除パスや rename target の分類、memo と .gitignore の変更分類など、apply join の受理・拒否境界を一箇所で扱う。

## Read this when
- apply join の CLI 挙動、後片付け、state 遷移、report 出力、または join 実行元 worktree の違いに関するテストを確認・変更する時。
- apply join が dirty worktree、stale apply branch、想定外の oracle 差分、merge conflict をどのように拒否または解決するかを確認する時。
- apply join の変更パス分類、削除パス除外、rename target 採用、memo や .gitignore の expected change 判定に関する回帰テストを探す時。

## Do not read this when
- apply fork 単体、session fork 単体、または join を伴わない通常の session 操作だけを確認したい時。
- CLI 経由の apply join 外部挙動ではなく、内部 helper の実装詳細だけを調べたい時は、対応する実装モジュールを先に読む。
- oracle file の正本仕様や文書上の要求を確認したい時は、test 配下の realization test ではなく oracle 配下の該当本文を読む。

## hash
- 2f5012fcfe4825679d269a9326f2725db6c44ea11ea1a2d5100efc94a786b9df

# `test_basic_runtime.py`

## Summary
- cmoc の基本 runtime 挙動を横断的に固定する realization test。path token 解決、run/work/repo root 判定、設定既定値と不正値検証、CmocError の Markdown report、CLI preflight と parse error の stdout 出力、`.cmoc` ignore 更新、file access mode から sandbox/Codex profile への変換、binary 判定など、基盤機能の外部挙動と制御境界を検証する。
- session/apply branch 名から session state を扱う経路、起動 wrapper の call stack 表示、shell completion probe の副作用抑止など、複数 module にまたがる runtime 契約の回帰確認入口になる。

## Read this when
- cmoc の runtime 基盤、CLI error report、preflight、root/path token 解決、`.cmoc` ignore、file access mode、Codex sandbox profile、session/apply branch state の挙動を変更または調査するとき。
- `cmoc_runtime`、`basic.path_model`、`commons.runtime_*`、`config.cmoc_config`、CLI entrypoint 周辺の変更で、利用者に見える出力・副作用・例外条件が変わり得るとき。
- 基本機能の回帰テストがどの外部挙動を固定しているかを確認し、既存テストへの case 追加で足りるか判断したいとき。

## Do not read this when
- 特定サブコマンド固有の成功フロー、Codex 呼び出し orchestration、oracle 文書生成など、このファイルが扱う runtime 基盤契約に関係しない機能を調べるとき。
- 実装詳細だけを局所的に変更し、path/root 判定、CLI error report、設定、状態 branch、sandbox profile、`.gitignore` 副作用、binary 判定の外部挙動に影響しないことが明確なとき。
- oracle file の正本仕様を確認したいとき。この対象は realization test であり、仕様本文の代替にはならない。

## hash
- 4b7edf73dd74f3ec4fecf6f409504f97dc3c7367280574ab972a536f53c50208

# `test_cli_init_tui.py`

## Summary
- CLI の初期化処理と対話起動処理に関する realization test。初期化時の .cmoc 管理除外、.gitignore 更新、既存 staged/unstaged 変更の保護、設定ファイルの既定値同期、サブコマンドログ記録、linked worktree での保存先・ignore・commit 挙動を検証する。
- 対話起動について、エディタで作られた依頼文からコメントを除去してパラメータ解決を行い、解決結果から Codex 呼び出し用パラメータを組み立て、完了プロンプトをログへ保存する制御を検証する。
- Markdown プロンプト解析について、fenced code block 内の見出し風文字列を無視し、見出し前本文と見出し階層を保持する挙動を検証する。

## Read this when
- 初期化コマンドが .cmoc を Git 管理から外し、ignore 設定を追加し、cleanup commit を作る挙動を変更・確認したいとき。
- 初期化コマンドが利用者の既存 staged 変更や .gitignore の staged/unstaged 変更を壊さないことを確認したいとき。
- linked worktree 上で初期化または対話起動を実行した場合の、repo root と worktree root の使い分け、ログ保存先、schema 保存先、ignore 設定、commit 対象を確認したいとき。
- 設定ファイルの初回生成、既定値、既存の人間設定を保持したまま不足キーを補う挙動を変更・確認したいとき。
- 対話起動でエディタ編集後のプロンプトを整形し、パラメータ解決用 Codex 実行と TUI 用 Codex 起動へ渡す値を確認したいとき。
- Markdown プロンプト parser の見出し検出、見出し前本文の扱い、階層構造の保持を変更・確認したいとき。

## Do not read this when
- 初期化、対話起動、Markdown プロンプト解析に関係しないサブコマンドの挙動だけを調べたいとき。
- Codex 実行ラッパーそのもののプロセス起動仕様や外部 CLI の詳細を調べたいときは、実装側の呼び出し処理を直接読む方がよい。
- 設定項目の正本仕様やパス概念そのものを確認したいときは、oracle 側の該当仕様を読む方がよい。
- テスト支援関数や temporary repository fixture の実装詳細だけを調べたいときは、支援モジュールを直接読む方がよい。

## hash
- 935565fd5bbe27dc1fab1611fcff207f94f87f7a4019c82d91bc157aa38fdba8

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出しまわりの realization test。tracked subprocess の process group 分離、exec/tui 起動時の profile・cwd・sandbox 設定、呼び出しログ、禁止領域変更の検出、extra read path 検証、非ゼロ終了、CLI 欠落時エラーを検証する。
- 実際の Codex CLI ではなく一時ディレクトリ上のスタブ実行ファイルと pytest の monkeypatch を使い、外部プロセス起動の引数・標準入力・生成 profile・ログ副作用・例外メッセージを確認する。

## Read this when
- Codex exec/tui の起動引数、作業ディレクトリ、sandbox profile、CODEX_HOME profile 生成、出力最終メッセージの扱いを変更する。
- FileAccessMode ごとの Codex 実行制限、特に repo write と pure oracle read の cwd・sandbox 挙動を確認または変更する。
- Codex subprocess の process group、tracked pid 記録、呼び出しログ、subcommand logger、失敗時コンソール出力に関わる実装を変更する。
- `.agents` 配下変更の拒否、`memo` など許可領域外 extra read path の事前拒否、Codex CLI 欠落や非ゼロ終了時の CmocError を扱う。

## Do not read this when
- Codex 呼び出し制御ではなく、通常の CLI サブコマンド解析、oracle 文書生成、path model、設定ファイル読み込みだけを調べたい。
- テスト支援 helper の一般的な使い方だけを知りたい場合は、fixture や support helper の定義を直接読む方が適切である。
- Codex CLI や LLM の出力品質そのものを評価したい場合。この対象は cmoc 側の起動制御・権限設定・失敗処理を検証するものである。

## hash
- a5c50f5f2b987c017ef264cb8dd6012f8503aca7c9ec3dc72fa8c10179ef2971

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行時の Codex home 解決と事前検証を対象にした realization test。環境変数が未設定の場合の既定 home、環境変数で指定された home の保持、Codex 実行 cwd に対する相対 home の解決、home や認証情報が不正な場合に Codex CLI 起動前に失敗することを検証する。

## Read this when
- Codex CLI 呼び出しで使用する CODEX_HOME の決定、相対パス解決、実行結果へ記録される codex_home や profile_path の挙動を確認・変更するとき。
- Codex home が存在しない、ディレクトリではない、auth.json がない場合の CmocError の summary・detail・next_actions を確認・変更するとき。
- ファイルアクセスモードによって Codex CLI の作業ディレクトリが変わる状況で、相対 CODEX_HOME がどこから解決されるかを検証するとき。

## Do not read this when
- Codex CLI の容量待機、標準出力イベント処理、プロンプト生成など、Codex home の解決や検証に直接関係しない実行制御を調べるとき。
- 実際の Codex CLI や LLM の出力品質を検証したいとき。ここでは fake executable を使い、home 解決と事前検証の制御ロジックだけを扱う。
- oracle file 側の正本仕様を確認・変更したいとき。この対象は realization test であり、正本仕様そのものではない。

## hash
- f113426a3f92145e9b5bff3bfd809dd949834c6dbb9c2471815903cec09de7fe

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex 実行が quota exceeded で失敗した後、quota availability probe を挟んで resume または再実行する制御を検証する realization test。
- quota 待機中・probe・resume の各 Codex 呼び出しについて、引数、標準入力、CODEX_HOME、作業ディレクトリ、出力 JSON、call log、subcommand log、コンソール表示が期待どおり残ることを確認する。
- 並列実行時に代表 probe が 1 回だけ使われ、各実行が成功結果へ復帰することも扱う。

## Read this when
- Codex 実行の quota exceeded 検出、quota availability probe、resume token を使った再開、resume token がない場合の再実行を変更・調査するとき。
- Codex 呼び出しログ、subcommand logger の codex_call イベント、stdout・stderr・prompt・output の保存先、quota_waiting や failed などの状態記録を確認するとき。
- CODEX_HOME が相対パスの場合の基準ディレクトリ、PURE_ORACLE_READ での Codex 作業ディレクトリ、または quota probe が .agents を変更した場合の拒否処理を扱うとき。
- 複数スレッドから同時に quota exceeded になった場合の probe 共有と各呼び出しの復帰動作を検証・変更するとき。

## Do not read this when
- 通常の Codex 実行成功経路だけを確認したいとき。quota exceeded 後の probe・resume・再実行に関係しないなら、より直接の実行系テストを読む。
- CLI の引数解析、設定ファイル読み込み、リポジトリ作成 fixture そのものを調べたいとき。ここではそれらを quota retry 検証の前提として使うだけで、主対象ではない。
- Codex CLI や LLM の出力品質そのものを評価したいとき。この対象は外部コマンドを stub し、quota retry 制御とログ副作用を検証する。

## hash
- f7fc97f0c355d4ab8079b39fb4242e76eed97d9468b674a18c38f2de43b09b2d

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーの retry 制御を検証する realization test。schema validation 失敗時の再実行、capacity エラー時の再実行、stdout JSONL 外に出た capacity/quota 文字列を retry 判定に使わないことを、偽の codex 実行ファイルとログ出力で確認する。
- 実行結果の JSON、呼び出し回数、call log、prompt/stdout log path、subcommand log の codex_call status・returncode・error detail を観測し、retry の外部挙動とログ記録の境界を確認する入口になる。

## Read this when
- Codex CLI 呼び出しの retry 条件、retry 後の成功扱い、または CmocError への失敗変換を変更する。
- schema validation retry、capacity retry、quota/capacity marker の判定元、または stdout JSONL の解釈を変更する。
- codex call log、prompt log、stdout log、subcommand log の記録内容や、retry ごとの log path の扱いを変更する。
- run_codex_exec の外部コマンド呼び出しをテスト上で置き換える fixture や helper の使われ方を確認したい。

## Do not read this when
- Codex CLI 実行と無関係な CLI サブコマンド、設定読み込み、path model、oracle/realization 分類の仕様を調べたい。
- retry ではない通常成功・通常失敗の基本挙動だけを確認したい場合で、より直接その観点を扱うテストがある。
- Codex CLI や LLM の出力品質そのものを評価したい。ここではラッパーの制御ロジックとログ副作用だけを検証している。

## hash
- ee15da0887d4878f996c9352e878cabccda604558cc4e7f34ecaae2df5879d20

# `test_indexing_cli.py`

## Summary
- indexing コマンドと indexing preflight の実現テスト。INDEX.md 生成、Codex によるエントリー生成、fresh hash による再生成スキップ、 malformed entry の再生成、index commit の範囲、worktree 上での実行対象、dirty worktree の拒否、apply worktree での repo config 利用、root 直下 memo 除外と nested memo 対象化を検証する。
- apply 側の INDEX.md merge conflict 解消処理について、競合した INDEX.md を削除して merge commit を成立させる挙動も検証する。

## Read this when
- indexing コマンド、run_indexing_preflight、update_indexes、render_index_entry、commit_index_updates の外部挙動や回帰テストを確認・変更する。
- INDEX.md の生成・再生成・hash freshness・malformed entry 判定・semantic fields の validation に関するテスト観点を確認する。
- cmoc indexing が clean/dirty な通常 worktree・linked worktree・apply worktree でどの root/cwd/config を使い、何を commit するかを確認する。
- INDEX.md の merge conflict を apply 側でどう処理するか、または memo ディレクトリを indexing 対象からどう扱うかのテストを探す。

## Do not read this when
- CLI 全体のコマンド定義、設定モデル、path model、Codex 実行 wrapper の実装詳細だけを確認したい場合は、対応する実装ファイルを直接読む。
- oracle file の正本仕様を確認したい場合は、この realization test ではなく oracle 配下の該当本文を読む。
- indexing 以外のサブコマンドや、INDEX.md 生成と無関係な git 操作の挙動を調べたい場合は、より直接のテストまたは実装へ進む。

## hash
- 5116be4af0a7ffa3f454bb5ebcfc8b31571db6b4d1c6a4f43ecc57b9d47514e8

# `test_indexing_preflight.py`

## Summary
- Codex 呼び出し前に索引更新を走らせる preflight 制御の realization test。exec/TUI 経由の実行順、更新後コミット、作業ツリー選択、リポジトリロック待機、特定 purpose での索引更新スキップを検証する。

## Read this when
- Codex 実行ラッパーが索引更新を先に行うか、更新後に専用コミットを作って作業ツリーを clean に戻すかを確認・変更したいとき。
- root と cwd が異なる場合に、どの worktree を索引更新対象にするかを確認・変更したいとき。
- 索引更新の排他ロック取得待ち、または索引エントリー生成・衝突解決の purpose で preflight をスキップする条件を扱うとき。

## Do not read this when
- 索引本文の生成内容、ディレクトリ走査、エントリー構造化出力そのものを確認したいだけのとき。
- Codex 実行パラメータの定義や runtime 実行関数の通常動作だけを調べたいとき。
- Git worktree やロックを伴わない一般的なテスト補助関数だけを探しているとき。

## hash
- 5549e75d6493464e59f5f4cb68232c1fbd9fc7d03b85ee5f6cb6ea3ad4e04099

# `test_prompt_parts.py`

## Summary
- prompt 部品と AgentCallParameter builder が生成する prompt、file access rule、routing rule、各種 standard、structured output schema、model/reasoning/file access 設定を横断的に検証する realization test。
- 標準 prompt の組み立て、markdown rendering、apply fork・review oracle・session join・TUI resolve・indexing builder の期待値が、実装および oracle 側 schema と一致することを確認する入口。
- 16,000 文字を超えるが、agent prompt と structured output schema の構築結果を同じ読み取り文脈で検証するため、共通の render/schema 期待値を一箇所に集約している。

## Read this when
- prompt 構築に含まれる routing rule、file access rule、各種 standard の出力内容や既定の含有有無を変更・確認したいとき。
- AgentCallParameter builder の model class、reasoning effort、file access mode、prompt 本文、structured output schema path の期待値を確認したいとき。
- apply fork、review oracle、session join、TUI resolve、indexing index entry など複数 builder にまたがる schema 同期や prompt 回帰を調べるとき。
- StructDoc や StructCodeBlock の markdown rendering、とくに連続空行や code block 内空行の扱いを確認したいとき。

## Do not read this when
- 個別 builder の実装詳細、prompt 文面の生成ロジック、schema ファイル本体を確認したいだけなら、対応する実装または oracle 側 schema を直接読む。
- 単一機能の外部挙動や CLI 実行結果だけを調べたい場合は、その機能を直接扱う実装・テストを優先する。
- INDEX.md エントリー生成の出力規則そのものを確認したい場合は、index entry standard を生成・検証する対象や関連 standard を読む。

## hash
- 2641417fa6a7330408ae9a33d871bd3c51c795b01ffeed07856171e56e2b4562

# `test_review_oracle_cli.py`

## Summary
- review oracle の CLI 経由の report 生成、所見列挙・検証・judge・merge の loop 制御、対象 oracle 選択、review worktree での実行と INDEX.md 変更の取り込み、失敗時 report、想定外差分の拒否をまとめて検証する realization test。
- 16,000 文字を超えるが、同じ review run の状態、fake Codex 応答、report 文脈を共有する外部挙動群を一箇所で扱うため、oracle review の読み取り文脈を保つ凝集したテスト群として位置づけられている。

## Read this when
- review oracle の report に含める verdict、評価対象、accepted/rejected findings、件数、no_targets、error 表示などの外部出力仕様を確認・変更する。
- review oracle の対象選択で full/session scope、短縮 option、gitignored oracle、binary、memo 形状の path、linked worktree 上の oracle をどう扱うかを確認・変更する。
- 所見評価 loop で enumerate の再実行文脈、challenger/advocate reason の受け渡し、judge 結果、merge operation の契約と不正 operation 拒否を確認・変更する。
- review oracle 実行用 worktree、review が生成した INDEX.md の merge、INDEX.md 削除 conflict 解決、INDEX.md 以外の想定外差分の拒否を扱う実装を変更する。
- review oracle の途中失敗時に error report を残し、CLI がどこへ何を出力するかを確認・変更する。

## Do not read this when
- review oracle 以外のサブコマンド、session 管理、設定読み込み、git helper の一般挙動だけを調べたい場合。
- oracle file や realization file の概念定義、正本仕様断片そのもの、または人間が編集する oracle 文書の内容を確認したい場合。
- review oracle の内部 helper の細かな実装だけを局所的に読む必要があり、外部挙動や CLI report との対応を確認しない場合。
- 通常の INDEX.md ルーティング文書の生成規則や schema だけを確認したい場合。

## hash
- fb1bcbdd95446c0d256449bfb602a0ddb48d543d23892e05de28e4c8fc41cc3a

# `test_session_cli.py`

## Summary
- session サブコマンドの CLI 挙動を検証する realization test。session fork / abandon / join について、branch 作成・切替・削除、session state の生成・更新、linked worktree 上の挙動、衝突解決、cleanup 失敗、エラー出力先を実リポジトリ操作と CLI 実行結果で確認する。
- session state JSON、git branch/worktree、未コミット差分、oracle conflict resolution 用の Codex 実行呼び出し、stdout/stderr の失敗報告など、session ライフサイクルの外部挙動を横断的に扱うテスト群である。

## Read this when
- session fork / abandon / join の CLI 外部挙動、状態遷移、git branch 操作、または linked worktree 対応を変更・調査するとき。
- session state file の必須 field、破損 state、session-id collision、abandoned / active / joined への更新条件を確認するとき。
- session join の merge conflict 解決、conflict marker 検出、削除 conflict の staging、Codex 実行時の file access mode や writable path を変更・調査するとき。
- session サブコマンドの成功時・失敗時レポート、stdout/stderr の出力先、cleanup 失敗時の rollback や再実行案内を確認するとき。

## Do not read this when
- session サブコマンド以外の CLI コマンド、または session ライフサイクルに関係しない実装・テストを調べるとき。
- session の内部 helper の細部だけを確認したい場合で、対象 module の単体実装を直接読む方が早いとき。
- oracle file の正本仕様そのものを確認したいとき。このテストは realization test であり、仕様判断の根拠としては対応する oracle file を優先する。

## hash
- 54f593b6c669227406abe4f8afa58d3167cd2a39e1155717f9d003f6ef1237fd
