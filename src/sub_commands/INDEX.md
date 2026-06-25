# `apply`

## Summary
- apply 系サブコマンドの実装群で、apply run の開始、実行結果の取り込み、破棄、report 生成、worktree・branch・process 状態の補助処理を扱う入口。
- session branch と apply branch/worktree の関係、apply state の ready/running/done 遷移、Codex による finding 適用、join/abandon 時の cleanup や warning 出力を追うための実装がまとまっている。
- apply 実行中の編集禁止対象差分の検出・ロールバック、想定外差分や merge conflict の扱い、process id の保存・停止確認など、apply run のライフサイクル全体に関わる制御へ進む起点になる。

## Read this when
- apply run を開始して isolated worktree 上で finding を適用し、差分 commit と report 作成まで進める全体フローを確認・変更したいとき。
- 完了した apply run を session branch へ取り込む join 処理、merge conflict、想定外差分、force-resolve、cleanup の挙動を確認・変更したいとき。
- 未 join の active apply run を破棄し、process 停止、apply worktree/branch 削除、state 初期化を行う abandon 処理を確認・変更したいとき。
- apply branch や session branch から対象 worktree を特定する規則、apply branch 名からの期待 path 導出、process id 状態ファイルの読み書きや削除を確認・変更したいとき。
- apply fork や join/abandon の利用者向け report 内容、結果ラベル、frontmatter、変更要約、失敗時フォールバックを確認・変更したいとき。
- apply 実行中または join 時に、編集禁止対象の差分、想定外差分、INDEX.md だけの conflict 自動解決など、apply 固有の差分制御を調べたいとき。

## Do not read this when
- apply 以外のサブコマンドの CLI 登録、dispatch、引数定義を調べたいとき。
- session state の型定義、永続化形式、session_id の生成・管理、apply.apply_branch の schema そのものを調べたいとき。
- git command wrapper、worktree root、branch 操作、clean worktree 判定、timestamp、report directory、config 読み込みなどの共通 runtime 基盤だけを調べたいとき。
- Codex 呼び出し用 prompt や structured output builder の詳細だけを調べたいとき。
- oracle file の正本仕様、INDEX.md 生成規則、編集禁止領域の原則そのものを調べたいとき。
- apply package に import 時処理や再 export があるかだけを確認したい場合を除き、パッケージ説明だけを読む目的のとき。

## hash
- f911a56f1c0739f0c4c0544fe220f796d3c75297958c2780ae20d7950bffa663

# `indexing.py`

## Summary
- 現在の work root 全体に対する INDEX.md maintenance の実行手順を実装するサブコマンド領域の中核コード。clean worktree 確認、repository 単位の排他 lock、indexable 対象の列挙、鮮度 hash による既存 entry 再利用、Codex 呼び出しによる不足 entry 生成、INDEX.md 更新差分の commit までを扱う。
- INDEX.md entry の Markdown 形式を検証・抽出・描画する処理と、対象本文の取り出し、binary・git ignored・root memo 除外、directory hash の再帰計算をまとめて確認する入口になる。

## Read this when
- INDEX.md maintenance の実行順序、排他制御、clean worktree 前提、更新後 commit の条件を確認または変更したいとき。
- indexable な directory や child の判定、root memo・git ignored・binary file の除外条件、directory traversal の挙動を確認または変更したいとき。
- 既存 INDEX.md entry の再利用条件、必須 section と hash の検証、対象 hash の計算方式、entry の Markdown rendering を確認または変更したいとき。
- Codex CLI に INDEX.md entry 生成を依頼する入力内容、並列生成数、codex_exec が未指定の場合のエラー処理を確認または変更したいとき。

## Do not read this when
- 個別サブコマンドの CLI 登録や Typer app 全体の構成だけを確認したいとき。
- INDEX.md entry 生成 prompt の具体的な AgentCallParameter 構築内容だけを確認したいとき。
- git 実行 wrapper、config 読み込み、hash 計算、binary 判定、work root 解決などの共通 runtime helper 自体を確認したいとき。
- 生成された INDEX.md の個別 entry 内容やルーティング文書の文章品質だけを確認したいとき。

## hash
- e9d9c48b2422dc3b9603c8c9211952730e6ea8312162c7bda63ade6ca37cadf4

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
- 利用者が入力した依頼文を編集させ、依頼内容から TUI 実行パラメータを解決し、完全な prompt を保存して Codex TUI を起動する一連の処理を担う。
- TUI 用の元 prompt テンプレート作成、エディタ選択と実行、HTML comment 除去、解決済み JSON からの AgentCallParameter 構築、Markdown 見出しの StructDoc 化を扱う。

## Read this when
- `cmoc tui` の起動処理、利用者 prompt の作成・編集・読み込み、または TUI 実行時に Codex へ渡すパラメータの組み立てを確認・変更したいとき。
- TUI で許可する file access mode、parameter 解決結果の読み取り、完全 prompt の保存先、または Codex TUI 呼び出し時の引数を追う必要があるとき。
- 利用者が書いた Markdown prompt を構造化された詳細指示へ変換する処理や、コードフェンス内の見出しを無視する解析挙動を確認したいとき。
- `cmoc tui` 実行時にエディタ未検出、エディタ異常終了、TUI 非対応の file access mode で発生するエラーを調査するとき。

## Do not read this when
- TUI 以外のサブコマンド本体、CLI 引数定義、設定ファイル形式、または Codex 実行基盤そのものを調べたいだけのとき。
- TUI パラメータ解決用 prompt の中身や schema 定義を調べたいときは、解決パラメータを構築する別モジュールを直接読む方がよい。
- 完全 prompt の一般的な構成規則や render 処理そのものを調べたいときは、prompt 構築や構造化 markdown の共通処理を直接読む方がよい。

## hash
- 0be11b2c52c4c301f4207952ae677296c80919fb5408d827ce8e7fc28f87a634
