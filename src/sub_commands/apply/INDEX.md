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
- apply 実行時の worktree 特定、apply process pid file の保存・読取・削除、Codex subprocess 追跡環境の一時設定、running abandon 時の停止処理をまとめる runtime 補助実装。
- pid 再利用を避けるため process start time を含む識別子を扱い、pidfd と process group signal を使って apply 本体と配下の Codex subprocess を停止する責務を持つ。
- apply branch 名から managed worktree を復元する処理と、git linked worktree から branch checkout 先を探す処理もここに含まれる。

## Read this when
- apply branch と linked worktree の対応付け、または session branch の worktree 検出処理を確認・変更したいとき。
- apply 実行中に保存される pid file の path、形式、読取時の破損扱い、cleanup 後の削除を確認・変更したいとき。
- apply 実行中だけ Codex subprocess 追跡を有効化する環境変数・process-local tracking の扱いを確認・変更したいとき。
- apply abandon が実行中 apply process や Codex child process group を停止する条件、同一性確認、SIGTERM/SIGKILL の待機処理、権限・race 対応を確認・変更したいとき。

## Do not read this when
- apply サブコマンドの利用者向け CLI 引数、出力文言、全体フローだけを確認したいときは、呼び出し側の command 実装や仕様文書を先に読む。
- session state の schema や apply state 全体の保存内容を確認したいだけなら、状態定義や state 入出力を扱う対象を読む。
- Codex CLI 呼び出し内容そのもの、prompt、実作業の適用ロジックを確認したいだけなら、apply の実行本体を扱う対象を読む。
- 一般的な git 操作 helper や cmoc runtime 共通関数の挙動を確認したいだけなら、共通 runtime 側を読む。

## hash
- 4022eb4c2e409743d467cecee54f5a344fbd4546c5f7e85bfdb4eeb3e866fb06

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
- apply fork の実行結果または失敗結果を Markdown report として保存する処理を担う。
- fork 元からの変更差分を git diff と未追跡ファイル差分から集め、Codex による構造化変更要約を試み、失敗時は変更 path の機械的な要約へフォールバックする。
- report には session/apply の branch・commit・worktree、収束結果、所見数の推移、変更要約を frontmatter と本文として描画する。

## Read this when
- apply fork の report 生成先、保存タイミング、保存内容を確認・変更したいとき。
- apply fork の変更差分として、commit 差分、worktree 差分、staged 差分、未追跡ファイルをどう集めるか確認したいとき。
- apply fork の変更要約生成で Codex 実行結果を使う箇所、または要約生成失敗時・空差分時のフォールバック挙動を確認したいとき。
- apply fork report の result 表示、finding count 表示、change summary 表示、YAML frontmatter の構成に関わる変更を行うとき。

## Do not read this when
- apply fork のループ制御、所見検出、apply branch の作成・削除など、report 作成以外の実行フローを調べたいとき。
- Codex に渡す変更要約プロンプトや構造化出力の設計そのものを調べたいとき。
- reports directory や timestamp、git command 実行 helper の共通仕様を調べたいとき。
- apply fork 以外のサブコマンド report や、汎用的な report 表示仕様を調べたいとき。

## hash
- 910bff7f1c498e1843455a81c937f9793cf522a8cf47a71b6255132e74867ac3

# `join.py`

## Summary
- apply run の完了またはエラー状態から、apply branch を session branch へ join して apply state を初期化するサブコマンド実装を扱う。
- join 前の worktree 清潔性確認、想定外差分の検出と force-resolve による復元、merge conflict レポート作成、join 後の apply worktree・branch cleanup までを一連の責務として持つ。
- apply 側・session 側で許可される差分の分類、削除や rename の扱い、INDEX.md だけの conflict 自動解決など、join 固有の差分判定と復旧補助の入口になる。

## Read this when
- apply join の実行条件、session/apply branch 上での動作、apply state を ready 相当に戻す流れを確認・変更したいとき。
- apply branch の merge、merge conflict 検出、INDEX.md conflict の機械解決、join report の内容や生成条件を確認・変更したいとき。
- 想定外差分の分類、--force-resolve 時の session/apply 側差分の戻し方、apply worktree や apply branch の cleanup 条件を確認・変更したいとき。

## Do not read this when
- apply run の開始、作業ブランチ作成、または apply state を completed/error にする処理だけを調べたいとき。
- apply join に限らない CLI 共通実行ラッパー、git 実行、session state の低レベル読み書き、path model の定義を調べたいとき。
- INDEX.md エントリー生成やルーティング文書そのものの規約だけを確認したいとき。

## hash
- bdf6e03d8f2bf5d377ec2e86a06e0a7c979dc184aebe57e820d11a9beef541aa
