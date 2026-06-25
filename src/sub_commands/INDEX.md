# `apply`

## Summary
- apply 系サブコマンドの実行、破棄、join、report 生成と、それらを支える worktree・branch・process id 操作をまとめる実装ディレクトリ。
- apply run の開始から isolated worktree での finding 適用、変更 commit、状態更新、失敗時 report、完了後の session branch への merge、不要になった apply branch/worktree の cleanup までを扱う入口になる。
- apply 専用の低レベル runtime、abandon・fork・join の各利用者向け処理、fork report 生成に責務が分かれているため、apply のどの段階を調べるかに応じて下位対象へ進むための案内として読む。

## Read this when
- apply サブコマンド群のどの実装を読むべきか、実行開始、破棄、join、report、worktree/process 補助処理の観点で切り分けたいとき。
- apply run の状態遷移、apply branch/worktree のライフサイクル、process id の保存・削除、cleanup の全体像から調査先を選びたいとき。
- apply fork 中の finding 列挙・適用・commit・report 生成と、join 時の merge・conflict・想定外差分処理の関係を把握したいとき。
- active apply run の破棄、実行中 process 停止、apply state の ready への復帰、orphan warning など abandon 系処理の入口を探したいとき。

## Do not read this when
- apply 以外のサブコマンドの CLI 定義、実行処理、状態遷移を調べたいとき。
- git 実行 wrapper、repo root、worktrees root、state model、report directory、timestamp、CmocError など共通 runtime API そのものを調べたいとき。
- session state schema、session_id の生成・管理、apply.apply_branch の状態モデル上の意味を調べたいとき。
- INDEX.md エントリー生成の一般仕様、oracle file と realization file の基本概念、または oracle 側の正本仕様断片を確認したいとき。

## hash
- 721301312312178689c686acbd0fdcf8b5de42e633f28a4ef796fc5b83c06068

# `indexing.py`

## Summary
- 現在の work root に対して INDEX.md の保守を実行する indexing サブコマンド実装。clean worktree 確認、排他ロック、対象ディレクトリと子要素の列挙、既存エントリーの hash 検証、Codex CLI による不足エントリー生成、INDEX.md 書き戻し、更新分だけの git commit までを扱う。
- INDEX.md の対象外判定として、git ignore、binary file、dot directory、root 直下の memo 配下を除外するルールを実装している。
- Structured Output から INDEX.md entry Markdown を描画する処理と、既存 entry の必須セクションおよび hash 形式を検証して再利用可否を判定する処理の入口になる。

## Read this when
- cmoc indexing の実行フロー、preflight での index 更新、または INDEX.md 更新を commit する挙動を確認・変更するとき。
- INDEX.md の再生成対象になる directory/file の選別、memo や git ignored path や binary file の除外条件を確認・変更するとき。
- 既存 INDEX.md entry の parse、hash 抽出、鮮度判定、Codex CLI への entry 生成依頼、Structured Output から Markdown への変換を扱うとき。
- indexing 処理の排他制御や、git path 上の lock file を使った同時実行防止を確認・変更するとき。

## Do not read this when
- 個別サブコマンドの通常 CLI 登録や Typer app 全体の配線だけを確認したいとき。
- INDEX.md entry の内容を生成する prompt や AgentCallParameter の詳細を確認したいときは、entry 生成パラメータを組み立てる acp/builder 側を直接読む。
- work root の定義、git wrapper、hash 計算、config 読み込み、clean worktree 判定などの共通 runtime helper の詳細だけを確認したいとき。
- 生成済み INDEX.md の各エントリー内容を読むべきか判断したいだけのときは、対象階層の INDEX.md を読む。

## hash
- 4b30b315415bcf463bcf923b56e4604d4bc793ed405072d5d0e131fa6f893dc7

# `init.py`

## Summary
- リポジトリを cmoc が扱える初期状態へ同期する init サブコマンドの実装。ログ作成前の .cmoc ignore 保証、init commit 作成、利用者が実行前から持っていた .gitignore と staged 差分の退避・復元、成功結果の Markdown 出力を扱う。

## Read this when
- cmoc init の実行内容、init commit の作成条件、stdout に出す成功結果を確認または変更したいとき。
- init 実行時に .gitignore へ /.cmoc/ を追加する処理や、ログ作成前にその ignore を保証する処理を確認または変更したいとき。
- init 実行前から存在した staged 差分や .gitignore の worktree/index/head 状態を、init 後にどう復元するか確認または変更したいとき。

## Do not read this when
- init 以外のサブコマンドの CLI 挙動や出力を調べたいとき。
- repo root 判定、git コマンド実行、設定同期、.cmoc ignore の基本処理そのものを調べたいとき。
- init の外部挙動を検証するテストケースだけを探しているとき。

## hash
- 2d2315a5f424230c542ae2b1532a4dd9a9c31d25ff641f9fa0bfdf275980e15f

# `review.py`

## Summary
- active な session branch 上で oracle review を実行するサブコマンド統括フローを定義している。
- session 状態確認、clean worktree 確認、review 用一時 branch/worktree のライフサイクル、対象列挙・finding loop・INDEX 取り込み・レポート生成 helper の呼び出し順序を扱う入口になる。

## Read this when
- oracle をレビューするサブコマンドの実行条件、作業ツリーの清潔性確認、一時 worktree/branch のライフサイクル、または active session branch 制約を確認したいとき。
- review oracle 全体の呼び出し順序、失敗時にも report を書く制御、または下位 helper の接続を確認・変更したいとき。

## Do not read this when
- 通常の CLI アプリ登録、Typer の command wiring、または他サブコマンドの引数定義だけを調べたいとき。
- review 対象となる oracle file の列挙条件、session scope と full scope の違い、INDEX.md と binary file を除外する対象選定だけを調べるときは、`review_targets.py` を読む。
- finding を列挙・統合・反証/擁護検証・判定するループ制御、Structured Output の finding list への適用、finding id や verdict の扱いを変更するときは、`review_loop.py` を読む。
- review worktree で生成された INDEX.md 差分だけを commit/merge する制御、INDEX.md 以外の差分検出、merge conflict を session 側採用で解消する挙動を確認するときは、`review_index.py` を読む。
- review 結果レポートの frontmatter、判定区分、対象 oracle file 一覧、fatal/minor finding 表示、path 表示の整形を変更するときは、`review_report.py` を読む。
- oracle review 用 prompt parameter の具体的な文面や Structured Output schema の定義を確認したいときは、builder 側の該当実装を読む。
- git command 実行、worktree 操作、branch 操作、設定読み込み、session state 読み込み、report directory 解決などの共通 runtime helper 自体を調べたいときは、runtime 側の実装を読む。
- oracle file の正本仕様内容そのものや、INDEX.md エントリーとして何を書くべきかの規則を確認したいときは、oracle 側の仕様断片を読む。
- 生成済みレポートの個別内容や過去実行結果を確認したいだけのときは、レポート出力先の生成物を読む。

## hash
- da34890c9d586595154820a8b028253f100cb4b390c3742335e67d7621ffc2b5

# `review_index.py`

## Summary
- oracle review 用 worktree で生成された INDEX.md 差分の commit と、review branch から session branch への merge を扱う。
- INDEX.md 以外の差分検出、porcelain status の path 抽出、INDEX.md だけが conflict した場合に session 側採用で解決する処理をまとめている。

## Read this when
- review worktree の INDEX.md 変更だけを commit する条件、INDEX.md 以外の差分をエラーにする制御、または status parsing を確認・変更したいとき。
- review branch merge の失敗時に INDEX.md conflict だけを自動解決する挙動、merge 後 commit の取得、手動解決へ回す条件を調べたいとき。

## Do not read this when
- review oracle 全体の一時 worktree 作成・削除順序や active session 制約を確認したいときは、`review.py` を読む。
- oracle file の対象列挙、finding loop、または report rendering を確認したいときは、それぞれ `review_targets.py`、`review_loop.py`、`review_report.py` を読む。
- git command 実行 wrapper や worktree 操作 helper 自体の実装を調べたいときは、runtime 側を読む。

## hash
- 42f2f7a768474b5b07e47ec55750ce65ea6bba3439c7cd667355dc5c6ca6efa9

# `review_loop.py`

## Summary
- oracle review の finding enumerate/merge/validate/judge loop を実行する実装。
- Codex に渡す review oracle 用 AgentCallParameter builder を呼び分け、finding id、advocate/challenger reasons、verdict、judge reason を Structured Output から更新する。

## Read this when
- finding の列挙、統合、反証/擁護検証、判定のループ回数や停止条件を確認・変更したいとき。
- merge finding operation の delete/replace/merge 適用、finding id の採番、finding list の更新規則を調べたいとき。
- review oracle 用 Codex 呼び出し purpose、作業 cwd、既存 finding JSON の渡し方を変更したいとき。

## Do not read this when
- oracle review の active session 制約、一時 worktree 作成、INDEX.md commit/merge、report rendering を確認したいときは、それぞれ該当する review 系 module を読む。
- prompt parameter の文面や Structured Output schema の定義そのものを確認したいときは、acp.builder.review.oracle 側を読む。

## hash
- 56a9c39c86337277ad4be649704deccd9415f64ce48f6e2194b06b95ca3d9fd5

# `review_report.py`

## Summary
- oracle review 結果を Markdown + YAML frontmatter の report として描画し、report directory へ書き出す処理を扱う。
- verdict 判定、frontmatter fields、評価対象 oracle file の表、fatal/minor finding section、path 表示整形をまとめている。

## Read this when
- review report の出力 path、frontmatter 項目、result/verdict の判定条件、または fatal/minor finding の表示形式を確認・変更したいとき。
- oracle path の表示整形、finding section の Markdown 文面、エラー時 report の描画を調べたいとき。

## Do not read this when
- review oracle の実行順序、一時 branch/worktree、対象 oracle file の列挙、finding loop、INDEX.md merge を確認したいときは、それぞれ該当する review 系 module を読む。
- 生成済み report の個別内容だけを読みたいときは、report 出力先の生成物を直接読む。

## hash
- 5a4bc1bc25bc2c3390133302a704cfab266f75d5d961859b561a4a82777866ee

# `review_targets.py`

## Summary
- oracle review の対象 oracle file を scope 別に列挙する処理を扱う。
- full scope では全 oracle file、session scope では session 開始 commit から変更された oracle file のうち、INDEX.md、git ignored、binary file を除外した対象を返す。

## Read this when
- review 対象となる oracle file の列挙条件、session scope と full scope の違い、または INDEX.md・binary・git ignored file の除外条件を確認・変更したいとき。
- session 開始 commit から oracle 配下の変更 path を取得し、列挙済み oracle file と照合する処理を調べたいとき。

## Do not read this when
- review oracle 全体の実行順序、一時 worktree、finding loop、INDEX.md merge、report rendering を確認したいときは、それぞれ該当する review 系 module を読む。
- binary 判定、git ignored 判定、git diff wrapper 自体の実装を調べたいときは、runtime 側を読む。

## hash
- f42029951fa3338498710cca446b7ee6dbf8f87039fc10726d2cecc385a0c05c

# `session`

## Summary
- session 系サブコマンドの実装をまとめるディレクトリ。active session の作成、home branch への取り込み、破棄など、session branch と session state を操作する各 subcommand 実装への入口になる。
- 各実装は、現在 branch、worktree cleanliness、cmoc ignore、apply/session state、home branch などの事前条件を確認し、Git 操作・状態更新・利用者向け出力・失敗時のエラー報告を扱う。

## Read this when
- session 系 subcommand のどの実装を読むべきかを選びたいとき。
- session branch の作成、取り込み、破棄に関する実行条件、状態遷移、副作用、エラー処理の入口を探したいとき。
- session 操作が branch 切り替え、branch 削除、state file 更新、clean worktree 要求、cmoc ignore 確認とどう関わるかを調べ始めるとき。

## Do not read this when
- session 以外の subcommand、共通 CLI ルーティング、Typer 登録全体を調べたいとき。
- Git wrapper、branch 判定、worktree 検査、state file schema、path model などの共通 helper の詳細だけを調べたいとき。
- 個別の session 操作がすでに決まっているとき。その場合は作成、取り込み、破棄など該当する実装へ直接進む。

## hash
- af7779bdd3151ca37e91ef8170a3139762d0692fa00838305739f08a6405a43c

# `tui.py`

## Summary
- 対話型実行フローを実装するサブコマンド本体。ユーザー用プロンプトの初期ファイル作成、エディタ起動、入力プロンプトからの実行パラメータ解決、完全プロンプト保存、TUI 用 Codex 呼び出しまでをつなぐ。
- TUI で許可するファイルアクセスモードの検証、Markdown 入力を構造化プロンプト部品へ分解する処理、解決済みパラメータ辞書から値を取り出す小さな補助処理を含む。

## Read this when
- 対話型サブコマンドの実行順序、生成されるプロンプトログ、エディタ選択、TUI 起動時に Codex へ渡す AgentCallParameter の組み立てを確認・変更したいとき。
- ユーザーが入力した Markdown プロンプトの見出し・本文・コードフェンスの扱い、またはコメント除去後の入力読み取り挙動を確認したいとき。
- TUI で利用可能なファイルアクセスモード、oracle/realization/review/index entry 系フラグを complete prompt に反映する経路を調べたいとき。

## Do not read this when
- 通常の非対話型サブコマンド、設定ファイルの定義そのもの、Codex 実行ラッパーの低レベル実装だけを調べたいとき。
- TUI パラメータ解決用プロンプトの生成内容そのものを変更したい場合は、その解決パラメータを組み立てるモジュールを直接読む方が適切。
- complete prompt の各セクション内容やレンダリング規則そのものを変更したい場合は、完全プロンプト生成や構造化ドキュメントの担当箇所を直接読む方が適切。

## hash
- e274745becf0d7dd19c1f830062a93a54eae26eeb1220a8112a19d2e096833c4
