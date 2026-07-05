# `apply`

## Summary
- apply 系サブコマンドの実行制御をまとめるディレクトリ。run の開始、破棄、取り込み、結果レポート生成に関する上位処理へ進む入口になる。
- apply state、apply branch、apply worktree、process id、session branch との関係を扱う処理が集まっており、apply run の外部挙動や状態遷移を調べるときの起点になる。

## Read this when
- apply run の開始、破棄、取り込み、レポート生成のどの実装へ進むべきかを選びたいとき。
- apply branch、apply worktree、apply process id、session state の扱いを伴う apply 系サブコマンドの挙動を確認または変更したいとき。
- apply run の成功時・失敗時・未収束時の状態遷移、出力、cleanup、report 連携を調べたいとき。
- apply 対象 file の列挙、finding 列挙と適用、差分 commit、join merge、abandon cleanup の流れをサブコマンド単位で追いたいとき。

## Do not read this when
- apply 以外のサブコマンド実行基盤、共通 runtime、設定読み込み、git wrapper、state 型そのものを調べたいとき。
- branch、worktree、state file、process id を操作する低レベル helper の汎用実装だけを確認したいとき。
- Codex に渡す prompt、parameter builder、Structured Output schema の詳細だけを確認したいとき。
- oracle file や realization file の一般定義、INDEX.md 生成規則、ルーティング規則そのものを調べたいとき。

## hash
- 614529c6a7ab4147e599d32d7fa6c38cbb3a39b3193b78f1e0e21708f11e0609

# `doctor.py`

## Summary
- doctor サブコマンドの実行本体を定義し、CLI runtime 経由で doctor preprocess を明示的に起動する。
- 現在の repo root を取得し、cmoc 実行可能状態への修復処理を走らせたうえで、doctor の実行結果として repo root を表示する。

## Read this when
- doctor サブコマンドの挙動、実行入口、または表示内容を確認・変更したいとき。
- doctor preprocess を通常の CLI preprocess とは別に明示実行する経路を確認したいとき。
- repo root を取得して修復処理へ渡す doctor 固有の制御を確認したいとき。

## Do not read this when
- doctor preprocess の具体的な修復内容を確認したいだけなら、runtime 側の preprocess 実装を読む。
- repo root の探索規則そのものを確認したいだけなら、repo root を定義する runtime 側を読む。
- doctor 以外のサブコマンドの CLI 挙動を確認したいときは、そのサブコマンドの実装を読む。

## hash
- 8381189b496dd020a8b46e16e2d13b3f03f58b372c085a3849ae81db685728ea

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
- review oracle の指摘抽出、重複整理、検証、判定を codex 実行で順に回すループ処理を担う。
- finding の採番、関連 oracle path による絞り込み、merge operation の検証と適用、advocate/challenger/judge の結果反映を扱う。

## Read this when
- review oracle 実行時に finding がどの順序で列挙、merge、validate、judge されるかを確認したいとき。
- merge finding Structured Output の delete、replace、merge operation がどの条件で受理または拒否されるかを確認したいとき。
- finding_id、advocate_reasons、challenger_reasons、verdict、judge_reason の初期化や更新タイミングを調べたいとき。
- oracle path ごとに既存 finding を渡す条件や、dirty 状態の進み方を変更したいとき。

## Do not read this when
- review oracle 用 prompt parameter の内容や Structured Output schema 自体を確認したいときは、builder 側の該当対象を読む。
- finding から oracle path を解決する規則だけを確認したいときは、review path 解決を担う対象を読む。
- 設定値そのものや loop 回数の定義を確認したいときは、config 側の対象を読む。
- review oracle 以外の review loop や CLI entrypoint の挙動を確認したいときは、その責務を持つ対象を読む。

## hash
- 6d2050cdbc25b2851d391f49e9b895d0632b0ea9489de6552196593d56188ebf

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
- review oracle の実行結果を、Markdown 本文と YAML frontmatter を持つレポートとして生成する処理を扱う。
- 評価対象 oracle file 一覧、accept/reject された finding の重大度別集計、コマンド実行メタデータ、結果 verdict をレポートに整形する。
- finding の表示、oracle path の表示名変換、エラー時・対象なし・fatal/minor/ok の結果判定を確認する入口になる。

## Read this when
- review oracle のレポート出力内容、frontmatter 項目、見出し構成、finding の並びや表示形式を変更したいとき。
- review oracle の結果判定が error、no_targets、fatal、minor、ok のどれになるかを確認したいとき。
- oracle file のパスをレポート上でどのように相対表示するか、または oracle ツリー外の path 表示を調べたいとき。
- accepted/rejected finding や fatal/minor finding の件数がレポートにどう反映されるかを確認したいとき。

## Do not read this when
- review oracle がどの oracle file を対象に選ぶか、または finding をどう検出・判定するかを調べたいとき。
- レポート保存先ディレクトリ、timestamp、session state などの共通 runtime 処理そのものを調べたいとき。
- review oracle 以外のサブコマンドの出力やレポート生成を変更したいとき。

## hash
- 343a451b0583fb9e3ab827733b2dad6c371ed1689c01dbdda7c419ba5d8f3baf

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
- session 系サブコマンドの実行本体をまとめる実装領域。session の開始、取り込み、破棄に関する branch/state 操作、事前条件確認、失敗時処理、利用者向け出力の具体化を扱う。
- パッケージ自体は初期化処理や公開 API を持たず、個別の session サブコマンド実装へ進むための入口として位置づく。

## Read this when
- session 系サブコマンドの実装を調べ、どの処理本体へ進むべきかを判断したいとき。
- session の開始、home branch への merge、session branch の破棄、state 更新、branch switch/delete、clean worktree 確認などの実装を確認または変更したいとき。
- session 操作中の git 操作失敗、rollback、conflict 解消委譲、conflict marker/unmerged path 検査、利用者向けエラー出力の扱いを調べたいとき。
- session 配下のパッケージ境界を確認し、パッケージ自体に初期化処理があるかを見たいとき。

## Do not read this when
- session サブコマンドの正本仕様を確認したいときは、対応する oracle doc を読む。
- session state のデータ構造、state file schema、path model、git wrapper、CLI runtime、branch 判定などの共通機構そのものを調べたいときは、それぞれの定義または共通実装へ進む。
- session 以外のサブコマンド実装、共通 CLI ルーティング、サブコマンド登録を調べたいとき。
- INDEX.md 用エントリーの生成規則やルーティング文書の書き方だけを確認したいときは、規則本文を読む。

## hash
- 3f5d8784a365ddc733c78060bd96b6dcd807e5310d92e72cc43195ec711c5a8c

# `tui.py`

## Summary
- TUI サブコマンドの実行本体を扱う。利用者が編集する元プロンプトの作成、エディタ起動、プロンプト本文の読み取り、実行パラメータ解決、Codex TUI 起動までの一連の制御を担う。
- TUI 用のファイルアクセスモード検証、起動パラメータの既定値補完、TUI ログ領域への prompt ファイル作成、TUI 実行前の `.cmoc` ignore 保証を扱う入口である。

## Read this when
- TUI サブコマンドの起動フロー、エディタ選択、prompt テンプレート、prompt 読み取り、または Codex TUI へ渡すパラメータ生成を確認・変更するとき。
- TUI 実行時に許可するファイルアクセスモード、resolve parameter の JSON からの値取り出し、または TUI 起動前の ignore 設定保証に関する挙動を調べるとき。
- TUI サブコマンドのテストで、外部実行関数を差し替えながら本体処理の制御順序や例外条件を検証したいとき。

## Do not read this when
- CLI runtime 全体の共通実行・ログ・設定読み込み・Codex 呼び出しの低レベル処理だけを調べる場合は、それらを提供する runtime 側を読む。
- TUI 用 prompt の文面構築や AgentCallParameter の詳細な構造そのものを調べる場合は、TUI builder 側を読む。
- indexing preflight の仕様や実装だけを調べる場合は、indexing 側を読む。

## hash
- 1624cda85856bef68561ea9c9090f7e56efc69184746b9dcf344337499083636
