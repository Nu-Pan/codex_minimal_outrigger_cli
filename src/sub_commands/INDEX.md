# `apply`

## Summary
- apply 系サブコマンドの実行制御をまとめる実装パッケージ。run の開始、破棄、取り込み、結果 report 生成を扱い、branch・worktree・state・process id・Codex 呼び出し・変更要約の連携を確認する入口になる。
- apply run の lifecycle に沿って、対象ファイル選定、finding 列挙と適用、収束判定、失敗時処理、merge と conflict 処理、後片付けまでの上位 orchestration を担う。

## Read this when
- apply 系サブコマンドの外部挙動、事前条件、状態遷移、出力内容、失敗条件、report 生成のどこを読むべきか判断したいとき。
- apply run が branch、worktree、process id、session state、report をどのタイミングで作成・更新・削除するかを追いたいとき。
- finding 列挙対象の決定、変更後の再キュー、apply branch の session branch への取り込み、想定外差分や conflict の扱いを調べたいとき。
- apply fork の report 本文や変更要約、apply join の結果 report など、apply run の利用者向け結果生成を確認または変更したいとき。

## Do not read this when
- apply 以外のサブコマンドの CLI 定義、状態遷移、入出力を調べたいとき。
- git command wrapper、state 読み書き、worktree 探索、Codex exec runtime、report directory 生成など、複数機能で使われる低レベル helper の基本挙動だけを確認したいとき。
- oracle file、realization file、INDEX.md 生成規則、path model など、apply run 固有ではない仕様概念を確認したいとき。
- パッケージ説明や import 時副作用の有無だけを確認したい場合を除き、具体的な制御ロジックが不要なとき。

## hash
- 06b00bc96e45831f9e65695d05464eaa91aa3129ccd9e9a9aea7232cd216cb37

# `indexing.py`

## Summary
- cmoc の indexing サブコマンド実行入口を定義し、CLI runtime 経由で現在の work root に対する INDEX.md maintenance を起動する実装を扱う。
- indexing 実行前の preflight、安全条件の検査、index 更新の排他実行、更新結果の commit、CLI 向けの更新件数出力までを結びつける薄い orchestration 層である。
- INDEX.md の生成・更新ロジックそのものではなく、既存の indexing 共通処理をサブコマンドとして呼び出すための接続点として読む。

## Read this when
- cmoc indexing サブコマンドの実行フロー、CLI runtime への渡し方、command 名や argv、work root runtime の指定を確認・変更したいとき。
- indexing 実行前に clean worktree や cmoc ignore 条件をどこで検査しているかを確認したいとき。
- INDEX.md maintenance がどの root に対して lock 付きで実行され、更新後にどのように commit と件数出力へ進むかを追いたいとき。
- indexing サブコマンドが Codex exec 実行関数や indexing 共通処理へどのように依存しているかを確認したいとき。

## Do not read this when
- INDEX.md の内容生成、差分検出、更新対象探索、commit 処理、lock 実装などの詳細ロジックを調べたいときは、ここではなく indexing 共通処理側を読む。
- work root の定義、CLI runtime の一般的な実行規約、clean worktree 判定、cmoc ignore 判定の詳細を調べたいときは、それぞれの runtime helper 側を読む。
- Typer app へのサブコマンド登録やトップレベル CLI 配線を確認したいだけなら、CLI entrypoint や subcommand 登録側を読む。
- oracle 上の indexing サブコマンド仕様そのものを確認したいときは、実装ではなく対応する oracle doc を読む。

## hash
- 300dd7538efb7a60cb06753149ee3b7f779bd687acbf6cc8a567083f8e6fa0a8

# `init.py`

## Summary
- `cmoc init` の実行本体を担う実装。runtime 経由で init サブコマンドを起動し、work root の `.cmoc` ignore、`.agents` 追跡 placeholder、設定同期、init commit、実行結果 Markdown 出力を処理する。
- init 実行前から存在した `.gitignore` と staged 差分を退避・復元し、init が作る管理用変更と利用者の作業中差分を混ぜないための復元処理も含む。

## Read this when
- `cmoc init` の実行順序、git 操作、commit 作成条件、stdout 出力を確認・変更したいとき。
- init が `.gitignore`、`.cmoc`、`.agents`、git index、staged 差分をどう扱うかを調べるとき。
- ログ作成前に `.cmoc` ignore を保証する処理や、work root と repo root が異なる場合の exclude 更新を確認したいとき。

## Do not read this when
- init 以外のサブコマンド実装を探しているとき。
- cmoc runtime 共通処理、git wrapper、root 解決、設定同期、ignore pattern 生成そのものを変更したいときは、それらを定義する runtime 側を読む。
- 正本仕様として init の要求を確認したいだけのときは、対応する oracle doc を読む。

## hash
- 74f27bc5512015dfdb5a1abc0cf9dcba26060cbdf8daccdc82c252cc1c6d5f36

# `review`

## Summary
- review 系サブコマンド群の package 境界と、oracle review を CLI 実行単位として接続する orchestration 層を含む。
- この階層は、review oracle の実行入口を中心に、preflight、session/state 検証、worktree 操作、対象列挙、review loop、INDEX 変更反映、後片付け、report 出力へ処理をつなぐ入口になる。
- 具体的な対象列挙、review loop、report 描画、INDEX 統合処理は下位 module が担い、この階層の入口はそれらを review oracle サブコマンドとして束ねる。

## Read this when
- review 系サブコマンド群の Python package 境界を確認したいとき。
- review oracle サブコマンドの実行順序、session branch 制約、clean worktree 要件、run worktree の作成・削除、review branch の merge 条件、失敗時 report 出力の扱いを確認または変更したいとき。
- review oracle が対象列挙、findings 生成、INDEX 変更反映、report 書き込みをどの helper module で接続しているかを追いたいとき。
- review oracle 実行時の公開入口や、review 関連 API の集約点を確認したいとき。

## Do not read this when
- review oracle の対象列挙条件や scope ごとの対象選定だけを変更したいときは、対象列挙を担う下位 module を読む。
- review loop 内で Codex に渡す prompt、finding の merge 操作、反復制御だけを扱うときは、review loop を担う下位 module を読む。
- report の本文構成、finding section の描画、report path の決定だけを扱うときは、report 生成を担う下位 module を読む。
- INDEX 変更の commit、review branch merge、conflict 解決、status path 取得だけを扱うときは、INDEX 統合処理を担う下位 module を読む。
- package 初期化時の import、副作用、公開シンボルを調べたいとき。ただし現在内容からはそのような責務は読み取れない。

## hash
- 7ea1740b338b184b4fba2974299d880e5575af5a23ebd4d13d2e6373496024e8

# `review_index.py`

## Summary
- review 用 worktree と review branch に含まれる差分が INDEX.md のみであることを検査し、INDEX.md 変更だけを commit して session branch へ merge する処理を扱う。
- review branch の merge 失敗時に、競合対象が INDEX.md だけなら ours 側または削除で自動解決し、解決不能な差分や競合は CmocError として扱う。
- git status、diff、merge、checkout、rm、commit、ls-files を使った review oracle indexing 周辺の git 制御ロジックへの入口である。

## Read this when
- review oracle が生成した INDEX.md 変更だけを commit する処理を確認・変更したいとき。
- review branch に INDEX.md 以外の commit 済み差分が混入していないか検査する挙動を確認・変更したいとき。
- review branch を session branch へ merge する処理、または INDEX.md だけの merge conflict 自動解決を扱うとき。
- review worktree の git status porcelain 出力から変更 path を抽出する処理を確認したいとき。

## Do not read this when
- 通常の sub command 引数解析、CLI 出力、または review command 全体の制御フローを確認したいだけのとき。
- INDEX.md エントリーの生成内容や oracle 文書のルーティング規則そのものを確認したいとき。
- review 以外の sub command の git 操作や worktree 操作を扱うとき。
- 一般的な git 実行ラッパー、HEAD 取得、CmocError の定義を確認したいとき。

## hash
- bd938a309c570ac01ae74652549b60ad737ca35824a7dc2043b471f2db2d8464

# `review_loop.py`

## Summary
- review oracle の finding を列挙し、重複整理し、検証者と擁護者の往復評価を行い、最終判定まで進めるループ処理を担う。
- oracle path 表記を実ファイル path に解決し、finding と対象 oracle file の関連付けを行う。
- merge finding の Structured Output edit operation を検証し、delete・replace・merge を finding list に適用する。

## Read this when
- review oracle の finding enumerate、merge、validate、judge の実行順序や反復条件を確認したいとき。
- finding の dirty 管理、finding_id 採番、advocate/challenger/judge フィールドの初期化や更新を調べたいとき。
- oracle_path の絶対 path、相対 path、プレースホルダ表記、oracle root alias の解決挙動を確認したいとき。
- merge finding operation の入力検証、target_ids の重複・未知 ID 検出、delete・replace・merge の適用規則を変更またはテストしたいとき。

## Do not read this when
- review oracle 用 prompt や codex 実行 parameter の文面を確認したいだけなら、builder 側の対象を読む。
- cmoc 全体の path placeholder 定義や実 path 解決の一般仕様を確認したいだけなら、path model 側の対象を読む。
- review oracle の反復回数など設定値の定義を確認したいだけなら、設定モデル側の対象を読む。
- oracle file の内容そのものをレビューしたいだけで、finding ループ制御や merge operation 適用には関心がないとき。

## hash
- 72935ec2e446bd58d0781ad2ecd853617501102084f80999f492fd638c188ece

# `review_report.py`

## Summary
- review oracle の実行結果を Markdown レポートとして保存・描画する実装。YAML frontmatter、判定文、評価対象 oracle 一覧、severity/verdict 別の finding 集計と詳細表示、oracle path の表示用整形を扱う。

## Read this when
- review oracle のレポート出力内容、見出し順、frontmatter 項目、判定 result の決まり方を確認・変更したいとき。
- review oracle の findings を accepted/rejected や fatal/minor に分類して表示する処理を追うとき。
- oracle file のパスをレポート上でどのように相対表示するかを確認・変更したいとき。

## Do not read this when
- review oracle の対象 oracle file を収集・選択する処理を探しているとき。
- review oracle の finding を生成・判定するレビュー本体のロジックを調べたいとき。
- review oracle 以外のコマンドのレポート出力を確認したいとき。

## hash
- 78249bbed205387b3ea6da3190592d887dc393325f6dac73ba150217fb94c000

# `review_targets.py`

## Summary
- review oracle の対象候補を列挙する処理を扱う。oracle ツリー配下から対象外名・memo・git ignore 対象を除外し、scope が full でない場合は session 開始 commit から HEAD までに変更された oracle file だけへ絞り込む。

## Read this when
- review oracle が対象にする oracle file の列挙条件を確認・変更したいとき。
- review oracle の full scope と変更分 scope の違いを確認したいとき。
- session 開始 commit がない場合の review oracle 対象の扱いを確認したいとき。
- oracle file 対象から INDEX.md、AGENTS.md、memo、git ignore 対象を除外する制御を確認したいとき。

## Do not read this when
- review oracle の実際の検査内容や診断ルールを確認したいとき。
- review oracle 以外のサブコマンドの対象列挙を確認したいとき。
- git コマンド実行、SessionState、memo 判定、git ignore 判定の共通実装そのものを確認したいとき。

## hash
- 00f712ea56b7dacdfbe5d7a0faf2bd9c9f3629aa7f0ce1a36ffa2280b37e3eb9

# `session`

## Summary
- session 系サブコマンドの実装群を収める領域。active session の作成、home branch への合流、破棄など、session branch と session state を操作する各サブコマンドへの入口になる。
- 配下には、パッケージ初期化だけを担う最小モジュールと、fork、join、abandon の実行本体があり、各コマンドの事前条件、git 操作、状態更新、失敗時処理を確認する起点になる。

## Read this when
- session 系サブコマンドのどの実装へ進むべきかを判断したいとき。
- session branch の作成、home branch への merge、merge せず破棄する処理の入口を探したいとき。
- session state の更新、branch switch/delete、clean worktree 確認、既存 active session 判定などが、どの session 操作に属するかを切り分けたいとき。

## Do not read this when
- session 以外のサブコマンド、共通 CLI ルーティング、git 実行 wrapper、runtime、path model、state model の汎用実装を調べたいとき。
- 個別コマンドの正本仕様そのものを確認したいとき。その場合は対応する oracle doc を読む。
- Codex CLI に渡す conflict 解消 prompt やパラメータ構築だけを調べたいときは、conflict resolution parameter builder を直接読む。

## hash
- de61c6979e3e3ba27721b704545bb23c7478091b32aa0e7f0fa3287c2291e605

# `tui.py`

## Summary
- `cmoc tui` の実行本体を担い、依頼文テンプレートの作成、エディタ起動、入力 prompt の読み込み、Codex Exec による TUI 起動パラメータ解決、Codex TUI 起動までの流れを扱う。
- TUI 実行前の indexing preflight、`.cmoc` ignore 保証、実行時 context からの root/config 解決、TUI 用 file access mode の検証と `AgentCallParameter` 構築をまとめる。
- TUI parameter JSON の `{value: ...}` 形式から文字列値・真偽値を取り出す小さな補助処理も含む。

## Read this when
- `cmoc tui` の起動フロー、依頼文編集、TUI log 領域への prompt ファイル作成、完成 prompt の参照渡しを確認・変更したいとき。
- TUI で許可する file access mode、resolved parameter の default 値、role/summary/goal や各 standard flag の TUI prompt への反映を確認・変更したいとき。
- TUI 実行前に `.cmoc` を ignore へ入れる処理、repository root と work root の扱い、config 読み込みを確認したいとき。
- 利用可能なエディタの選択順、エディタ異常終了時のエラー、元 prompt から HTML comment テンプレートを除去する処理を確認・変更したいとき。

## Do not read this when
- TUI prompt の具体的な組み立て形式や launch parameter の詳細だけを確認したい場合は、TUI launch parameter builder を直接読む。
- TUI parameter を Codex Exec で解決するための schema や resolve prompt の詳細だけを確認したい場合は、TUI resolve parameter builder を直接読む。
- CLI 共通の subcommand 実行、Codex Exec/TUI 実行、設定読み込み、root 判定、timestamp、`.cmoc` ignore の汎用挙動だけを確認したい場合は、runtime 側を直接読む。
- indexing preflight の仕様や実装だけを確認したい場合は、indexing preflight 側を直接読む。

## hash
- 5fd4f89ffaa5bd36df37c3140cac01b525bd4d460c1d94bdea8dd4925d644cd2
