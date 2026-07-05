# `apply`

## Summary
- apply 系サブコマンドの実行本体をまとめる領域。apply run の開始、破棄、join、report 生成に関する CLI 制御、状態遷移、branch/worktree 操作、Codex 呼び出し、結果表示への入口になる。
- apply fork では対象 file の選定、finding 列挙・適用、差分 commit、収束判定、state 更新を扱い、apply join/abandon では apply run の取り込みや破棄、cleanup、失敗条件を扱う。

## Read this when
- apply fork、join、abandon の実行条件、状態遷移、return code、削除対象、merge や cleanup、CLI 表示を確認または変更したいとき。
- apply run に紐づく apply branch、apply worktree、process id、session state、oracle snapshot commit、前回 join 済み apply merge commit の関係を調べたいとき。
- apply fork がどの file を対象にするか、scope ごとの差分、oracle 除外、git ignore・管理外領域・AGENTS/INDEX 除外、再調査キューや収束判定を確認したいとき。
- apply fork の report 生成、失敗時 report、Markdown 構成、frontmatter、変更差分収集、Codex 要約や fallback 要約を確認または変更したいとき。
- apply join 時に許可される差分範囲、想定外差分、force-resolve、INDEX.md conflict の自動解決、root memo や oracle file の扱いを確認したいとき。

## Do not read this when
- apply 以外のサブコマンド実行基盤、CLI 共通ラッパー、設定読み込み、git wrapper、state 型、worktree 探索、report directory の共通処理だけを調べたいとき。
- Codex に渡す prompt、Structured Output schema、parameter builder の詳細だけを変更したいとき。
- worktree 削除、branch 削除、process 停止、state 読み書きなどの低レベル helper の汎用実装そのものを確認したいとき。
- oracle file や realization file の一般定義、ファイルアクセス規則、仕様文書上の分類を確認したいとき。
- パッケージ説明や import 副作用の有無だけを確認したい場合を除き、具体的な apply サブコマンドと無関係な調査をしているとき。

## hash
- 09d2209b9249bd86daac8668d21433834b3b639ef7e5010f5e7d4917f0949c99

# `doctor.py`

## Summary
- CLI の init/doctor サブコマンド実装で、runtime の共通実行経路を使って doctor preprocess を明示実行する入口を定義する。
- init では preprocess 後に config 同期も行い、doctor では修復処理のみを行う差分を持つ。
- repo root の検出、doctor preprocess、必要時の config 同期、実行結果表示の流れを確認するための入口である。

## Read this when
- init または doctor サブコマンドの挙動を変更・確認したいとき。
- doctor preprocess の CLI からの呼び出し方、command heading、command argv、runtime wrapper との接続を確認したいとき。
- init 実行時だけ config 同期を行う理由や、その同期入口を変更する必要があるとき。
- CLI 実行後に表示される repo root 出力の生成箇所を確認したいとき。

## Do not read this when
- doctor preprocess 自体の修復内容や repo root 判定の詳細を知りたいだけなら、runtime 側の実装を読む。
- config の正本内容や同期対象の定義を確認したいだけなら、対応する oracle 側の config 定義を読む。
- Typer app へのサブコマンド登録や CLI 全体のルーティングを確認したいだけなら、上位の CLI 定義を読む。

## hash
- b9218f70377e66d6cad3aa19e1dd8fd6a7bc1184744c81c74615b30c74ab8f06

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
- review 用 worktree/branch に生じた差分を INDEX.md のみに制限し、必要な INDEX.md 変更だけを commit する処理を扱う。
- review branch を session branch へ merge し、競合が INDEX.md だけの場合に ours 側採用または削除で自動解決して merge commit を完了させる処理を扱う。
- git status、diff、merge、checkout、rm、commit を通じて review oracle indexing の差分検査・確定・取り込みを行う入口である。

## Read this when
- review oracle が作った差分に INDEX.md 以外が混ざった場合のエラー条件や確認方法を調べるとき。
- review worktree 上の INDEX.md 変更を commit する条件、commit しない条件、戻り値を確認するとき。
- base commit 以降の review branch 差分が INDEX.md だけであることを検査する処理を確認するとき。
- review branch の merge 失敗時に、INDEX.md 競合だけを自動解決する挙動を変更・確認するとき。
- review oracle indexing と review branch merge の git コマンド呼び出し順や失敗時の CmocError を追うとき。

## Do not read this when
- INDEX.md エントリー本文の生成規則や preflight indexing 全体の仕様を確認したいだけの場合は、対応する oracle doc を読む。
- git コマンド実行ラッパー、HEAD commit 取得、status path 収集の共通処理そのものを変更したい場合は、それらの runtime/helper 側を読む。
- review oracle のプロンプト、分離 worktree の作成、または subcommand 全体の制御フローを調べたい場合は、上位の review command 実装を読む。
- INDEX.md 以外の通常ファイル差分を merge・解決する汎用的な仕組みを探している場合は、この対象ではない。

## hash
- 500e71a4ff36cb5a35cbc12a4bb56b76f82c137800554580654c20e984e4fc66

# `review_loop.py`

## Summary
- review oracle の finding 抽出、統合、検証、判定を Codex 呼び出しで反復実行する制御ロジックを扱う。
- finding list に対する merge/delete/replace 操作の検証と適用、および semantic retry 失敗時のエラー化を担う。

## Read this when
- review oracle の finding enumerate/merge/validate/judge の実行順序、反復条件、dirty 管理を確認・変更したいとき。
- finding merge の Structured Output operation の許容条件、finding_id の採番、重複・未知 ID・不正 kind の扱いを確認・変更したいとき。
- review oracle loop が Codex 実行パラメータ builder、設定値、log root、worktree、oracle path とどう連携するかを追いたいとき。

## Do not read this when
- review 対象の oracle file 一覧作成や finding から oracle path を取り出す処理だけを確認したいときは、より直接その責務の対象を読む。
- Codex 実行パラメータのプロンプト内容や Structured Output schema 自体を確認したいときは、各 builder 側を読む。
- review oracle 以外の review workflow、CLI 引数、設定定義を確認したいだけのときは、それぞれの責務を持つ対象を読む。

## hash
- e905f9cf7705c92dbd8fbbdd55db0080f23e60a8bc26b5a4ca8987880fc5b237

# `review_paths.py`

## Summary
- review finding の `oracle_path` 値を、実在パスまたは解決済みパスへ変換する補助処理を扱う。
- 空値・非文字列・不正なプレースホルダを `None` にし、絶対パス、`<oracle-root>` alias、その他のパスプレースホルダ、worktree 相対パスを分岐して解決する。

## Read this when
- review finding に含まれる oracle 参照パスの解決方法を確認または変更したいとき。
- `<oracle-root>` alias、`<...>` 形式のパスプレースホルダ、worktree 相対パスの扱いを調べたいとき。
- finding に oracle path が無い場合や不正な場合の戻り値を確認したいとき。

## Do not read this when
- review finding の列挙 prompt や oracle path の出力仕様そのものを確認したいとき。
- 汎用的なパスプレースホルダ解決規則や path model 全体を調べたいとき。
- review サブコマンド全体の制御フロー、表示、終了コードを確認したいとき。

## hash
- 030dc150f751305de30cf8f55a7b22f925529de6c4aa2b2b36480935057e02ae

# `review_report.py`

## Summary
- review oracle の実行結果を Markdown レポートとして保存・描画する処理を担う。
- YAML frontmatter、判定文、評価対象一覧、accepted/rejected と fatal/minor に分けた finding セクション、oracle path の表示形式を組み立てる。
- finding の内容を判定する処理ではなく、既に得られた finding とレビュー実行メタデータを利用者向けレポートへ整形する出口に位置づく。

## Read this when
- review oracle のレポート出力内容、見出し順、frontmatter 項目、result/verdict 文言を確認または変更したいとき。
- finding の accepted/rejected や fatal/minor の集計、表示順、表示文言を確認または変更したいとき。
- 評価対象 oracle file の一覧表や、finding 数の集計表示、oracle path の相対表示ルールを確認したいとき。
- review oracle 実行中のエラー、対象 0 件、fatal/minor/ok の最終レポート判定ロジックを確認したいとき。

## Do not read this when
- review oracle の対象となる oracle file の探索・選定ロジックを確認したいだけのとき。
- finding の生成、検出、判定、または oracle path 抽出の詳細を確認したいとき。
- レポート保存先ディレクトリや timestamp の共通仕様だけを確認したいとき。
- review oracle 以外のサブコマンドの出力形式やレポート形式を確認したいとき。

## hash
- ace91ceb7f0700c17fc2c761b9aed86e91736c2638b8467a4d31b27d6ca69c96

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
- session 系サブコマンド実装をまとめるディレクトリ。session fork、join、abandon と、パッケージ境界を示す初期化モジュールを含む。
- session branch の作成、home branch への join、merge せず破棄する abandon など、session の lifecycle 操作に関する CLI 実装へ進む入口となる。

## Read this when
- session 系サブコマンドの実装場所を選びたいとき。
- session fork、join、abandon の実行条件、状態遷移、branch 操作、利用者向け出力の実装を調べたいとき。
- session join の merge conflict 解消制御、または session abandon の rollback/cleanup failure handling を調べたいとき。
- session branch と home branch の関係、active session state file の作成・更新・削除に関わるサブコマンド実装を確認したいとき。

## Do not read this when
- session 系サブコマンドの正本仕様だけを確認したいときは、対応する oracle doc を読む。
- CLI 全体の dispatch、共通 runtime、git wrapper、worktree 検証、state schema、path model の詳細を調べたいときは、それぞれの共通実装へ進む。
- session 以外のサブコマンド、apply workflow、または共通 indexing 処理を調べたいとき。

## hash
- 6808f64c3c792e174df9f8e8c533af5b52df67831d9f56984a39f0e333744e09

# `tui.py`

## Summary
- 対話的な依頼文編集から実行パラメータ解決、Codex TUI 起動までをつなぐ `cmoc tui` の実装を担う。
- TUI 用ログ領域への元 prompt 作成、利用可能なエディタ選択、HTML コメント除去、解決済み JSON からの起動パラメータ構築、TUI で許可される file access mode の検証を扱う。
- CLI runtime から現在の repository/context を取得して TUI 本体処理へ渡し、ログ作成前に必要な `.cmoc` ignore を保証する入口でもある。

## Read this when
- `cmoc tui` の実行フロー、エディタ起動、prompt ファイル作成、TUI 起動前の parameter 解決を変更したいとき。
- TUI サブコマンドで利用する file access mode、role・summary・goal・各標準フラグの既定値や resolved JSON の読み取り方を確認したいとき。
- TUI 実行時のログ保存先、元 prompt と完成 prompt の扱い、`.cmoc` ignore 保証の挙動を調べたいとき。
- TUI 起動前の Codex exec 呼び出しと TUI 起動呼び出しの引数、cwd、purpose、config の渡し方を確認したいとき。

## Do not read this when
- TUI 用 prompt の標準文面や agent call parameter の最終的な本文構築そのものを確認したいだけなら、TUI 起動パラメータを組み立てる builder 側を読む。
- resolved JSON を生成するためのプロンプトや schema、TUI で指定可能な解決項目を確認したいだけなら、parameter resolve の builder 側を読む。
- CLI runtime 共通の subcommand 実行、config 読み込み、log path、repository root 判定、Codex 実行 wrapper の詳細を調べたいだけなら、runtime 共通処理を読む。
- TUI 以外のサブコマンドの挙動や CLI 全体の command routing を調べたい場合は、そのサブコマンドまたは CLI entrypoint を読む。

## hash
- ec33c67348f84c67cb37c97936f7d21ff0b8f53fe546f3169c70732bb149c750
