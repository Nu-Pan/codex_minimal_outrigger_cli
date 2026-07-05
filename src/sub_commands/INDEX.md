# `apply`

## Summary
- apply 系サブコマンドの実装をまとめるディレクトリ。apply fork・join・abandon の実行制御、apply run の状態遷移、branch/worktree/process id の扱い、fork report 生成への入口を持つ。
- apply run の開始、finding 適用、差分 commit、join merge、abandon cleanup、想定外差分や conflict の処理など、apply 操作単位の上位制御を読むための入口となる。

## Read this when
- apply fork・join・abandon のどの実装ファイルへ進むべきかを選びたいとき。
- apply run の lifecycle、session branch と apply branch、apply worktree、apply state、process id、report の関係をサブコマンド単位で確認したいとき。
- apply fork の対象 file 選定、Codex 呼び出し、再調査 loop、commit、report 出力に関する実装を探したいとき。
- apply join の merge、force-resolve、想定外差分、INDEX.md conflict 自動解決、cleanup に関する実装を探したいとき。
- apply abandon の未 join apply run 破棄、process 停止、worktree/branch/state cleanup に関する実装を探したいとき。

## Do not read this when
- apply 以外のサブコマンド、CLI 共通の実行ラッパー、エラー表示、git wrapper、state 読み書き、worktree 操作の汎用基盤だけを調べたいとき。
- apply fork report の Markdown 書式や差分要約だけを扱う場合を除き、report 生成詳細ではなく fork/join/abandon の制御対象が決まっているときは該当ファイルへ直接進めるとき。
- Codex に渡す prompt、Structured Output schema、parameter builder の詳細だけを変更したいとき。
- oracle file・realization file・INDEX.md 生成規則など、apply サブコマンド実装ではない仕様概念を確認したいとき。

## hash
- b250d5db42f8e8934e1accf90fcb3a95c789203262135b20b52b0f38b2d515b7

# `doctor.py`

## Summary
- CLI runtime の preprocess 経路を使って、初回 setup・config 同期入口と doctor preprocess の明示実行を提供するサブコマンド実装。
- repo root を cmoc 実行可能状態へ修復し、実行した command heading と repo root を CLI 出力する責務を持つ。

## Read this when
- init または doctor サブコマンドが、CLI runtime の preprocess をどのように呼び出すか確認したいとき。
- 初回 setup、config 同期入口、または .cmoc ignore の保証がどこで行われるかを追うとき。
- doctor preprocess を command wrapper 経由で実行する際の引数、preprocess 抑制、出力 heading を確認したいとき。

## Do not read this when
- CLI runtime 側の共通実行制御、repo root 解決、doctor preprocess 本体の修復内容を調べたいときは、runtime 実装を直接読む。
- 設定内容そのものや config 同期仕様の正本を確認したいときは、対応する oracle 側の config 定義を読む。
- init や doctor 以外のサブコマンド実装を調べたいときは、それぞれのサブコマンド実装へ進む。

## hash
- e2853624f970ea7d00a94f40e035fcd3dfa010ffb923459ccfa71a9e8a72e56e

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
- session 系サブコマンドの実装をまとめるディレクトリ。session branch の作成、home branch への join、merge せず破棄する abandon など、session の状態遷移と git 操作を CLI runtime 経由で実行する処理を収める。
- 個別サブコマンドの実行条件、branch/state 更新、clean worktree や active session の事前条件確認、失敗時の CmocError と利用者向け出力を調べる入口になる。
- join では merge conflict 解消を Codex CLI に依頼する制御、conflict 対象外差分や未解消状態の検出、merge commit までの監視も扱う。

## Read this when
- session 系サブコマンド全体の実装場所を探し、作成・join・破棄のどの処理へ進むべきか判断したいとき。
- session branch と home branch の関係、session state file の作成・更新、branch 削除、active session の有無確認に関わる CLI 挙動を調べたいとき。
- session join の merge conflict 解消フロー、対象外差分の拒否、未解消 marker や unmerged path の検出を調査または変更したいとき。
- session サブコマンドの利用者向け出力、失敗時 rollback、手動復旧メッセージ、CmocError の文脈情報を確認したいとき。

## Do not read this when
- session 系サブコマンドの正本仕様だけを確認したいときは、対応する oracle doc を読む。
- session state のデータ構造、永続化形式、path model、git wrapper、worktree 検証などの共通 helper の詳細だけを調べたいときは、runtime や state model 側へ進む。
- 共通 CLI ルーティング、サブコマンド登録、または session 以外のサブコマンド実装を調べたいときは、該当する上位または別サブコマンドの実装へ進む。
- join の conflict 解消で Codex CLI に渡す prompt や実行 parameter の内容だけを確認したいときは、builder 側の conflict resolution 定義を読む。

## hash
- ececbe728f46af93eb9db9769da311f7af8753d226e4c9901504798b8c21f0ac

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
