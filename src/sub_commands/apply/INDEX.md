# `__init__.py`

## Summary
- サブコマンド実装パッケージの入口として、パッケージの役割を短い docstring で示すだけの対象。
- 具体的な処理、公開 API、import 副作用、設定値は持たないため、実装詳細への入口ではなく、パッケージ単位の責務確認に限って使う。

## Read this when
- サブコマンド実装パッケージそのものに、パッケージ説明や初期化時の処理があるかを確認したいとき。
- パッケージ import 時に実行される処理や再 export が存在しないことを本文で確認したいとき。

## Do not read this when
- 具体的なサブコマンドの引数定義、実行処理、入出力、エラー処理を調べたいとき。
- 実装変更やテスト追加のために、実際の制御ロジックを読む必要があるとき。
- パッケージ説明の文言確認以外が目的で、同階層または下位の具体的な実装対象へ直接進めるとき。

## hash
- e5354bb58c94a87f51093db4681c6f341202c07abf4b77772fb37b788f40b7b1

# `_runtime.py`

## Summary
- apply 実行時に使う linked worktree 解決、apply 用 worktree path 復元、apply process pid file の保存・読取・削除、Codex subprocess 追跡環境の一時設定、apply abandon での process / process group 停止を扱う実行時補助モジュール。
- pid 再利用を避けるため process start time と pidfd を使い、停止対象の同一性確認、SIGTERM から SIGKILL への段階的停止、停止済み・stale pid の警告化、権限不足や安全確認不能時の cmoc error 化を担う。

## Read this when
- session branch や apply branch から対象 worktree を特定する処理を確認・変更したいとき。
- apply 実行中の pid file の形式、生成条件、読取時の破損扱い、cleanup 後の削除を確認・変更したいとき。
- apply abandon が実行中 apply process や Codex subprocess group をどの順序・条件・signal で停止するかを確認・変更したいとき。
- Codex subprocess 追跡用の環境変数と process-local tracking path の復元挙動を確認・変更したいとき。
- Linux pidfd、process start time、/proc の process group 検査に関わる停止安全性や race 回避の挙動を調査するとき。

## Do not read this when
- apply subcommand の CLI 引数定義、ユーザー向け出力、または上位の command flow だけを確認したいとき。
- session state 全体の schema、apply branch の生成規則、または state file の読み書き全般を確認したいとき。
- Codex CLI の起動方法や通常の apply 作業内容を確認したいだけで、abandon 用の process 追跡・停止処理に触れないとき。
- git worktree の一般的な作成・削除処理を確認したいだけで、既存 branch から linked worktree を逆引きする処理に触れないとき。

## hash
- 282aaad7fa4d99a38607c0be1de675d6675914fe0dbd75fc568912c6fde691be

# `abandon.py`

## Summary
- 未 join の apply run を破棄し、apply state を ready に戻す CLI 処理を実装する。実行場所が session branch または対象 apply branch であることを検証し、必要なら実行中 apply process を停止したうえで、apply worktree・apply branch・process id file を片付け、状態ファイルを書き戻す。
- 破棄処理の結果として、対象 apply branch、apply worktree、破棄前後の状態、残存物や既欠落などの warning を利用者向けに出力する。

## Read this when
- 未 join の apply run を利用者操作で破棄して ready 状態へ戻す挙動を確認・変更したいとき。
- apply branch または session branch 上からの実行制約、active apply run が存在しない場合のエラー、対象 apply branch の整合性チェックを調べたいとき。
- running 状態の apply process 停止、apply worktree 削除、apply branch 強制削除、apply process id file 削除、apply state 初期化の一連の cleanup を追いたいとき。
- apply abandon の標準出力に含まれる before/after、warnings、削除対象情報を確認したいとき。

## Do not read this when
- apply run の開始、join、完了処理、または通常の ready 状態からの遷移を調べたいだけのとき。
- apply process の停止方法、process id file の保存場所、apply worktree path の算出規則そのものを調べたいときは、apply runtime helper 側を直接読む。
- branch 操作、worktree 削除、state file の読み書き、clean worktree 検証の低レベル実装を調べたいときは、CLI runtime 側の共通処理を直接読む。
- 破棄ではなく、apply run の成果を session branch へ取り込む処理を確認したいとき。

## hash
- 8cf68cbbea7c3a9377b922b36715768d1c71aea6dc037c1b20400f7f5834da66

# `fork.py`

## Summary
- apply fork の実行本体として、session branch 上の事前条件確認、isolated worktree と apply branch の作成、apply state の running/completed/error 更新、Codex による所見列挙と適用、変更ファイルの再キュー、commit、report 出力までの一連の orchestration を担う。
- apply scope から調査対象 file を列挙する処理、変更 path の正規化、直近 join 済み apply merge commit の探索、所見適用後の commit subject 生成など、apply run の loop 継続条件と失敗時復旧条件に密接に結び付く helper も同じ場所にまとまっている。
- 16,000 文字を超えるが、branch/worktree/state/report/requeue/commit が同じ apply fork loop の文脈を共有するため、分割よりも apply fork orchestration として一箇所で読む対象として位置付けられている。

## Read this when
- apply fork の CLI 実行フロー、事前条件、apply branch/worktree 作成、process id 管理、state 遷移、成功時・失敗時の report 出力を確認または変更したいとき。
- apply scope ごとの調査対象列挙、oracle や ignored file や INDEX.md の除外、変更済み realization file の再キュー、重複 target 除去の挙動を確認したいとき。
- Codex に渡す apply finding 列挙・所見適用の呼び出し境界、Codex profile と file access prompt に委ねる責務、apply fork 中の commit message 生成を確認したいとき。
- rolling scope で前回 join 済み apply merge commit から差分範囲を決める処理や、session_start_commit への fallback 条件を追いたいとき。

## Do not read this when
- apply fork が生成する report の本文構造や書き込み形式だけを確認したいときは、report writer 側を読む方が直接的。
- Codex exec に渡す prompt parameter の具体的な構築内容だけを確認したいときは、apply fork 用 ACP builder 側を読む方が直接的。
- apply process id の保存先や tracking の低レベルな実装だけを確認したいときは、apply runtime 側を読む方が直接的。
- CLI 共通 runtime、git wrapper、worktree 作成、state file の永続化、config load の共通挙動だけを確認したいときは、runtime 側を読む方が直接的。
- apply fork の正本仕様や公開仕様そのものを確認したいときは、oracle doc を読むべきであり、この実装だけを仕様根拠にしない。

## hash
- b060adca981f865b67eed797f481b2ca325aa767d51e1fd01448c83363c98c82

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を Markdown report として保存する処理を扱う。
- apply fork worktree の fork commit 以降の変更差分を集め、Codex による構造化要約または変更 path の fallback 要約へ変換する。
- report の frontmatter、作業結果、所見数推移、変更内容要約の組み立てを担う。

## Read this when
- apply fork 完了時・失敗時に生成される report の内容、保存先、生成タイミングを確認したいとき。
- apply fork の変更要約がどの差分を対象にし、未追跡ファイルをどう扱うかを確認または変更したいとき。
- 変更要約生成に失敗した場合や空要約だった場合の fallback 表示を確認または変更したいとき。
- report に出力される result label、所見数推移、branch・commit・worktree 情報の扱いを確認したいとき。

## Do not read this when
- apply fork のループ制御、所見列挙、収束判定そのものを調べたいとき。
- apply fork の変更要約プロンプトや構造化出力 schema の詳細を調べたいとき。
- git コマンド実行 helper、report directory 解決、timestamp 生成、session state 定義の共通実装を調べたいとき。
- apply 以外の sub command の report 生成や通常ログ出力を調べたいとき。

## hash
- 186ef04236529c1d7562192dcb8b72c304f536d3faa14511b89b4366a768f69c

# `join.py`

## Summary
- apply run の join 実行を担う実装。session branch または apply branch 上で実行され、対象 apply branch を session branch へ merge し、apply state を初期化して ready 相当に戻し、結果レポートを保存する。
- join 前の worktree 清潔性確認、cmoc ignore 確保、active session と completed/error apply run の検証、oracle snapshot commit と apply branch の特定、merge 後の apply worktree・apply branch の掃除を扱う。
- apply/session branch 上の想定外差分を分類し、通常時はレポート付きで中止し、force-resolve 時は基準 commit へ戻して commit する処理を含む。INDEX.md だけの merge conflict は削除 commit で機械解決し、それ以外の conflict はレポートして手動解決へ回す。

## Read this when
- apply join の実行条件、成功時の state 更新、apply branch の merge、apply worktree や branch の削除条件を確認したいとき。
- apply join で想定外差分がどのように検出・分類され、--force-resolve でどの branch 側の変更がどの基準 commit へ戻されるかを調べるとき。
- apply join 結果レポートの記録内容、merge conflict 時の中止条件、INDEX.md conflict の自動解決挙動を変更または検証するとき。
- session branch 上と apply branch 上の許可差分の境界、root memo・oracle・.agents・git ignored path の扱いを追うとき。

## Do not read this when
- apply run の開始、apply branch や worktree の作成、session state への apply 情報の書き込みを調べたいだけのとき。
- apply join 以外の apply サブコマンドの CLI option 定義や Typer command 登録だけを確認したいとき。
- git 実行、state 読み書き、reports directory、worktree 探索などの共通 runtime helper の低レベル実装を調べたいとき。
- oracle file の正本仕様そのもの、または apply join の仕様文書を確認したいとき。

## hash
- fff7ab6917b17a245a6a01863838ed827e5fe02fffaba951e76fddb05210aabf
