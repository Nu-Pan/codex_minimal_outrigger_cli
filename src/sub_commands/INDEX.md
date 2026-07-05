# `apply`

## Summary
- apply サブコマンド群の実行本体をまとめるディレクトリ。apply run の開始、破棄、join、fork report 生成など、apply 固有の branch/worktree/state/report 制御への入口になる。
- apply fork の orchestration、apply join の merge・cleanup、apply abandon の破棄処理、fork report の Markdown 生成を、同階層の各実装へ振り分けるための対象。

## Read this when
- apply サブコマンドのうち、fork、join、abandon、report 生成のどの実装を読むべきかを判断したいとき。
- apply run の branch/worktree/state/process/report に関する処理が、開始・破棄・join・report 生成のどこに属するかを切り分けたいとき。
- apply 固有の実行条件、状態遷移、差分分類、cleanup、CLI 表示を調べる入口を探しているとき。

## Do not read this when
- apply 以外のサブコマンド、共通 CLI runtime、git wrapper、session state 型、report directory 共通処理だけを調べたいとき。
- oracle file、realization file、path model、INDEX.md 生成規則などの正本仕様そのものを確認したいとき。
- Codex に渡す prompt、Structured Output schema、低レベルの state 読み書きや worktree 操作だけを直接確認したいとき。

## hash
- d0d181d31aa7bc845aa0211e4f0df788f337282cf5b442156a857664f7d95ff9

# `doctor.py`

## Summary
- doctor サブコマンドの実処理として、CLI runtime の preprocess 実行経路へ処理を委譲する薄い入口。doctor 固有の処理内容はここでは持たず、明示的に doctor preprocess を起動する責務だけを持つ。

## Read this when
- doctor サブコマンドが呼ばれた時に、どの runtime preprocess 名へ委譲されるかを確認したいとき。
- doctor サブコマンドの実装入口と、runtime preprocess 実行処理との接続を変更または確認したいとき。

## Do not read this when
- preprocess command の実行方法、失敗時挙動、runtime 側の制御を調べたいときは、preprocess 実行を担う commons 側の実装を読む。
- doctor preprocess の中身や診断項目を調べたいときは、その preprocess 本体を読む。

## hash
- 13b0493ce99287b1643522676065d9b8d003da0fc0cc55a3423864c0541091a8

# `eval_oracle.py`

## Summary
- want を書き出した oracle 評価を、review oracle と同じ実装経路へ委譲する薄い入口。eval oracle 側に独自の評価処理を持たせず、評価本体は review oracle 実装に集約する。

## Read this when
- eval oracle サブコマンドがどの評価実装へ接続されるかを確認したいとき。
- want を書き出した oracle の評価経路と review oracle の評価経路が同一であることを確認したいとき。
- eval oracle 用の入口関数や委譲先を変更する必要があるとき。

## Do not read this when
- review oracle の評価処理本体、出力、検査内容を確認したいときは、委譲先の review oracle 実装を読む。
- oracle 評価の根拠となる正本仕様や working plan review の意図を確認したいときは、対応する oracle doc を読む。
- CLI の引数定義やサブコマンド登録を確認したいだけのときは、CLI 構成側の実装を読む。

## hash
- aa69d5ae36aec1c3d31050a5ce5880c23ecaa6c7edd6a3d605751ccaf75a2501

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
- CLI の init サブコマンド実装を扱う。実処理は CLI runtime の preprocess command に委譲し、このファイルは init 用の入口だけを持つ。

## Read this when
- init サブコマンドがどの runtime preprocess command を呼ぶか確認したいとき。
- init サブコマンドの入口関数名や委譲先を変更したいとき。

## Do not read this when
- init の具体的な setup 内容や config 同期処理を確認したいとき。委譲先の runtime preprocess command 実装を読む。
- CLI runtime の preprocess command 共通挙動を変更したいとき。共通実装側を読む。

## hash
- 1c31245c4d543ed7f9025e974fb32ba8e42ae10a6075fed57af40989bba4c425

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
- review oracle コマンドの実行結果を、Markdown 本文と YAML frontmatter を持つレポートとして生成する処理を定義する。
- 評価対象 oracle file 一覧、accepted/rejected と fatal/minor に分類された finding、処理失敗時の verdict、関連ブランチ・コミット・件数メタデータをレポートへ描画する。
- finding の対象 oracle path を表示用に正規化し、レポート上の finding 件数集計と finding セクション本文のレンダリングを担う。

## Read this when
- review oracle のレポート出力形式、frontmatter 項目、verdict 文言、finding の分類表示を確認または変更したいとき。
- review oracle の結果が error、no_targets、fatal、minor、ok のどれになるかを確認したいとき。
- oracle file ごとの finding 件数表示や、oracle path の表示形式を調べたいとき。
- review oracle の永続レポートファイルの作成先やファイル名生成を確認したいとき。

## Do not read this when
- review oracle の対象 oracle file の収集、finding の検出、または finding の accept/reject 判定ロジックを調べたいだけのとき。
- review oracle 以外のサブコマンドのレポート形式や実行制御を調べたいとき。
- oracle file 自体の仕様内容や、oracle path の正本上の定義を確認したいとき。

## hash
- 459effd196adadf54bac5ce229e6694167c7fa345683ea2663ef2a9374a476f5

# `review_targets.py`

## Summary
- review oracle の対象となる oracle file を列挙する実装。scope が full の場合は全 oracle file、差分 scope の場合は session start commit から HEAD までに変更された oracle 配下の対象だけを返す。

## Read this when
- review oracle が検査対象にする oracle file の列挙条件を確認したいとき。
- scope と session state に応じて full review と差分 review の対象がどう変わるかを確認したいとき。
- oracle 配下から git 追跡対象外・INDEX.md・AGENTS.md などを除外する判定が対象列挙にどう使われるかを追いたいとき。

## Do not read this when
- oracle file かどうかの判定条件そのものを確認したいときは、runtime 側の path 判定を読む。
- review の実行内容、診断観点、出力形式を確認したいときは、対象列挙ではなく review 本体の実装を読む。
- oracle 以外の review 対象や一般的なファイル探索処理を確認したいとき。

## hash
- 76df8a9304aa0f5e4a6801534aeb25108d711ef343aabc725a20f8549b02c5ef

# `session`

## Summary
- session 系サブコマンドの実装をまとめるディレクトリ。session の作成、取り込み、破棄など、session branch と session state を扱う個別コマンド実装への入口になる。
- 各コマンド実装は、clean worktree、active session、home branch、state file、branch 切り替え・削除などの事前条件と状態遷移を扱い、失敗時には利用者向けの復旧情報を返す。
- merge conflict 解消や session-id 衝突回避など、特定コマンド固有の安全境界もこの配下の該当実装に分かれている。

## Read this when
- session 系サブコマンドのどの実装へ進むべきかを選びたいとき。
- session branch の作成、home branch への取り込み、破棄、状態更新、branch 削除条件など、session 操作の実行本体を調べたいとき。
- session 操作の事前条件、失敗時 rollback、cleanup、manual resolution、利用者向けエラーや出力の扱いを確認したいとき。

## Do not read this when
- CLI 全体の dispatch、共通 runtime、git wrapper、path model、state schema そのものを調べたいとき。その場合は共通基盤側を読む。
- apply workflow や session 以外のサブコマンド実装を調べたいとき。
- session の正本仕様断片そのものを確認したいとき。その場合は oracle 側の該当文書を読む。

## hash
- ebca94b04c4964aacd9c7206a1c632dcd214cb6372dc3629f2533963058f98cc

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
