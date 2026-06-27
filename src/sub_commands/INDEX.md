# `apply`

## Summary
- 実行結果を別 worktree で作成し、必要に応じて破棄または session 側へ取り込む一連のサブコマンド実装を扱う領域。
- 実行開始時の対象選定、process 追跡、branch/worktree 管理、差分検証、report 生成、cleanup、状態遷移の入口になる。
- 実行中の process 停止や pid 管理、fork 結果 report、join 時の想定外差分分類や merge conflict 処理など、apply 系操作固有の実行時責務を下位要素に分けて持つ。

## Read this when
- apply 系サブコマンドの開始、破棄、取り込み、report 生成、process 管理のどこを読むべきかを選びたいとき。
- session branch や apply branch を前提に、isolated worktree を作成・削除しながら apply run の状態を進める流れを調べたいとき。
- apply run の成果を session 側へ merge する条件、想定外差分の検出、force resolve、merge conflict 時の扱い、cleanup の責務境界を確認したいとき。
- 未 join の実行を破棄して ready 状態へ戻す操作、実行中 process の停止、apply worktree や branch の削除に関わる実装へ進みたいとき。
- apply fork の対象ファイル選定、finding 列挙・適用、禁止対象差分のロールバック、commit 作成、converged/unconverged/error 判定を追いたいとき。
- apply fork や join の利用者向け report に含まれる結果、warning、変更要約、保存先を確認・変更したいとき。

## Do not read this when
- CLI 全体のサブコマンド登録、dispatch、共通引数処理だけを調べたいとき。
- repo root、work root、git command 実行、状態ファイル読み書き、report root など、複数サブコマンドにまたがる runtime primitive の詳細だけが必要なとき。
- session state schema、session の作成・終了、branch 名規則そのものを調べたいとき。
- Codex に渡す prompt や parameter の詳細だけを変更・確認したいとき。
- oracle file、realization file、INDEX.md エントリー生成などの一般ルールを確認したいだけで、apply 系操作の実行時挙動に関心がないとき。
- 具体的な apply 系処理ではなく、パッケージ import 時の副作用や再 export の有無だけを確認したいとき。

## hash
- d2cc97b9294c96440affb0699a62fff04cbeb3f3280f49ff27a892411887dc84

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
- `cmoc init` サブコマンドの実行本体を扱う。CLI runtime 経由で初期化処理を起動し、work root の `.cmoc` ignore 保証、設定同期、初期化コミット作成、利用者が事前に持っていた staged 差分と `.gitignore` 状態の復元をまとめて担う。
- 初期化成功時に stdout へ出す Markdown 形式の結果文もここで組み立てる。

## Read this when
- `cmoc init` の実行順序、初期化コミット、設定同期、または `.cmoc` を `.gitignore` に含める処理を確認・変更したいとき。
- 初期化前から存在する `.gitignore` の worktree/index/HEAD 状態や、利用者が事前に staged していた差分を `cmoc init` 後にどう戻すかを調べるとき。
- `cmoc init` のログ作成前に行う ignore 保証と、その副作用を後続の復元処理から区別する仕組みを確認したいとき。
- `cmoc init` 成功時の利用者向け Markdown 出力を変更・検証したいとき。

## Do not read this when
- 個別の git コマンド実行 wrapper、runtime 共通処理、repo/work root 解決、設定同期、または ignore パターン生成そのものの実装を調べたいだけのときは、それらを定義する共通 runtime 側を読む。
- 他のサブコマンドの CLI 挙動、出力、状態復元を調べたいときは、対象サブコマンドの実装へ進む。
- `cmoc init` の外部挙動をテスト観点から確認したいだけのときは、対応するテストを読む。

## hash
- a7f12d58923b83b9f3941a0e829e20e9ed445db35c3a5fc9c20b6112c3620faf

# `review`

## Summary
- review 系サブコマンドを収める Python package で、現内容では package 境界と review oracle サブコマンドの実行入口を扱う。
- 主な責務は、active session branch 上での実行前提確認、scope 検証、clean worktree 要求、review 用 worktree と一時 branch の準備、対象列挙・review loop・INDEX 反映・report 出力・後始末の順序付けである。
- 対象列挙、finding 生成、review loop、INDEX 変更の commit・merge・conflict 関連処理、report rendering などの詳細処理は下位モジュールへ委譲し、この階層自体は CLI runtime 上のオーケストレーションを中心に読む。

## Read this when
- review 系サブコマンド群が Python package として扱われる境界を確認したいとき。
- review oracle サブコマンドの実行可能条件、active session branch 判定、scope validation、clean worktree 要求、cmoc ignore 確保の流れを確認したいとき。
- review 用 worktree と一時 branch の作成から、review loop 実行、INDEX 変更の commit と session branch への merge、worktree・branch 後始末、成功・失敗 report 出力までの大きな制御順序を追いたいとき。
- CLI から review oracle を起動する際の command name、command argv、Codex exec callback、preflight の受け渡し位置を確認したいとき。
- review oracle 実行中に対象列挙、findings 生成、report 書き出し、merge conflict 関連処理へどこから入るかをたどりたいとき。

## Do not read this when
- review 系サブコマンド群の package 境界だけでなく、package 初期化時の import、副作用、公開シンボルを調べたいとき。現内容からはそのような責務は読み取れない。
- oracle file の列挙条件や scope ごとの対象選択ロジックそのものだけを調べたいとき。対象列挙を担う下位モジュールを直接読む方が適切である。
- Codex による review loop の prompt、finding の生成・統合、merge operation 適用の詳細だけを調べたいとき。review loop を担う下位モジュールを直接読む方が適切である。
- report の本文構成、finding section の描画、report ファイルへの書き出し形式だけを調べたいとき。report を担う下位モジュールを直接読む方が適切である。
- review 用 INDEX 変更の status 判定、commit、merge、conflict 解決の詳細だけを調べたいとき。INDEX 反映を担う下位モジュールを直接読む方が適切である。

## hash
- 083601eeadc4297e6e80477998dbca65d18259c365ba9273e1ccf1655dbb7c65

# `review_index.py`

## Summary
- review 用 worktree に作られた変更を INDEX.md 差分だけに限定して commit し、その review branch を session branch へ merge するための処理を持つ。
- review worktree の git status から変更パスを取り出し、INDEX.md 以外の差分をエラーにし、INDEX.md のみを stage/commit する制御を扱う。
- merge 失敗時に未解決 conflict が INDEX.md だけであれば ours 側採用または削除で自動解決し、merge commit 後の HEAD を返す処理への入口になる。

## Read this when
- review oracle が生成した INDEX.md 変更だけを commit する流れを確認・変更したいとき。
- review branch を session branch へ merge する処理や、merge 後 HEAD の取得に関わる挙動を確認したいとき。
- INDEX.md conflict だけを自動解決する条件、ours stage の有無による checkout/rm の分岐、非 INDEX.md conflict を手動解決へ回す境界を確認したいとき。
- review worktree の porcelain status から rename/copy を含む変更パスを抽出するロジックを確認したいとき。

## Do not read this when
- 通常のサブコマンド引数定義、CLI 表示、ユーザー入力解析を確認したいだけのとき。
- INDEX.md 本文の生成内容やルーティング文書の文章品質を調べたいとき。
- oracle file と realization file の仕様関係や、INDEX.md エントリー作成基準そのものを確認したいとき。
- 一般的な git helper の実装や CmocError の定義を確認したいときは、それらを定義している共通 runtime 側を直接読む。

## hash
- fd46086c773e71294be6c9b8ed3da758d0729bfa1dc795d5f35336f661efd447

# `review_loop.py`

## Summary
- review oracle による finding の列挙、統合、検証、判定を一連のループとして実行する処理を担う。Codex 呼び出しの結果を finding 一覧へ反映し、finding_id や検証理由、判定結果の既定値を補いながら最終結果を返す。
- finding の oracle_path を実パスへ解決して対象 oracle file ごとの既存 finding を絞り込む補助処理と、merge finding の edit operation を検証して finding 一覧へ適用する処理を含む。

## Read this when
- review oracle の enumerate、merge、validate、judge の実行順序や反復条件を確認・変更したいとき。
- review oracle が Codex 実行へ渡す builder parameter、root、cwd、config、purpose の扱いを確認したいとき。
- finding の採番、既定フィールド、advocate_reasons、challenger_reasons、verdict、judge_reason の更新ロジックを確認したいとき。
- finding の oracle_path と worktree、絶対パス、パストークン表記の対応付けを確認したいとき。
- merge finding operation の delete、replace、merge の妥当性検証や、target_ids の重複・未知 ID エラーを扱う実装を確認したいとき。

## Do not read this when
- review oracle に渡すプロンプトや Structured Output parameter の詳細を確認したいだけなら、builder 側の各 review oracle parameter 生成処理を読む。
- CmocConfig の review_oracle 設定値そのものの定義や読み込みを確認したいだけなら、設定モデル側を読む。
- パストークンの一般的な定義や resolve_real_path の仕様を確認したいだけなら、path model 側を読む。
- 通常のサブコマンド登録、CLI 引数、コマンド dispatch の構造を確認したいだけなら、このループ処理ではなくサブコマンド入口や CLI 構成を読む。

## hash
- 86cde0b2e0151ed2d36309831353b40d7525abae13ac516f2e8f44bbd517cffb

# `review_report.py`

## Summary
- oracle レビュー結果を Markdown レポートとして永続化・描画する実装。評価対象の oracle、採用/不採用と fatal/minor の所見集計、実行ブランチやコミット情報、エラー時や対象なしの場合の判定文をレポートへまとめる。
- レポート本文の章構成、YAML frontmatter の値、所見セクションの表示、oracle パスの表示用正規化を扱う。

## Read this when
- review oracle サブコマンドの最終レポート内容、判定結果、所見の分類表示、件数集計を変更・確認したいとき。
- レビュー処理でエラー、対象 oracle なし、採用 fatal、採用 minor、問題なしの各ケースがレポート上でどう表現されるかを確認したいとき。
- oracle file のパスをレポート上でどのように相対表示するか、または oracle ツリー外のパス表示がどう扱われるかを確認したいとき。
- review oracle レポートの保存先ディレクトリ作成やタイムスタンプ付きファイル生成の呼び出し境界を確認したいとき。

## Do not read this when
- review oracle の所見検出ロジック、レビュー実行フロー、AI 呼び出し、または finding の生成方法を調べたいとき。
- review oracle 以外のサブコマンドのレポート形式や保存処理を調べたいとき。
- oracle file の正本仕様そのもの、oracle の探索条件、または対象 oracle の選定規則を確認したいとき。
- 単にランタイム状態、レポート保存先、タイムスタンプ生成などの共通 helper の仕様を調べたいとき。

## hash
- 7ebb6b472e6187ab56b144d4468a975d2ce397b4e4af3355c4983363560af38b

# `review_targets.py`

## Summary
- review oracle が検査対象にする oracle file を列挙する処理を担う。scope が full の場合は全対象を返し、それ以外では session_start_commit から HEAD までに oracle 配下で変更された対象だけを返す。
- oracle file 候補の列挙では oracle ツリーを再帰走査し、通常ファイルのうち INDEX.md、root memo、git ignore 対象を除外して並び順を安定させる。

## Read this when
- review oracle の対象ファイル集合が scope によってどう変わるかを確認・変更したいとき。
- session_start_commit を基準にした差分対象の判定や、git diff の対象範囲を確認・変更したいとき。
- oracle file 候補から INDEX.md、root memo、git ignore 対象を除外する条件を確認・変更したいとき。
- review oracle が参照する oracle file の列挙順やフィルタ条件に関する不具合を調査するとき。

## Do not read this when
- review oracle の結果表示、診断内容、プロンプト、出力形式を確認したいだけのとき。
- oracle file や realization file の概念定義そのものを確認したいとき。
- oracle 以外の realization file や test file の列挙条件を確認したいとき。
- root memo 判定、git ignore 判定、git コマンド実行 helper の詳細を確認したいとき。

## hash
- 8757d7467f9e0f50ab5b0c8b0f40fda477f0e603870376d607db08c28669e79e

# `session`

## Summary
- session 系サブコマンドの実装群をまとめる領域。session branch の作成、home branch への取り込み、merge せず破棄する処理を中心に、CLI runtime 経由の実行、事前条件検証、branch 遷移、state 更新、cleanup と失敗時 rollback の入口になる。
- 各実装は個別の利用者操作ごとに責務が分かれており、session state、apply state、clean worktree、managed branch 判定、home branch 存在確認、session branch 削除、merge conflict 解消など、session 操作に伴う制御を扱う。

## Read this when
- session 系サブコマンドのどの実装へ進むべきかを判断したいとき。
- 新しい session branch を現在の local branch から開始する処理、session-id 生成、active session の重複検出、branch/state file の衝突回避を調べたいとき。
- active session branch を home branch に取り込み、merge、conflict 解消依頼、状態更新、session branch 削除、成功時出力までの流れを調べたいとき。
- active session branch を home branch へ merge せず破棄し、state を abandoned に更新し、session branch を削除する流れや rollback を調べたいとき。
- session 操作に共通して現れる事前条件違反、clean worktree 要求、home branch への切り替え、利用者向けエラーや出力の境界を把握したいとき。

## Do not read this when
- session 以外のサブコマンド実装、共通 CLI ルーティング、サブコマンド登録だけを調べたいとき。
- git 実行 wrapper、CLI runtime、worktree root、branch 判定、clean worktree 判定、state file 読み書きなどの共通 helper 自体の実装を調べたいとき。
- session state schema、apply state schema、path model など、状態やパスのデータ構造定義そのものを確認したいとき。
- merge conflict 解消依頼用の Codex CLI parameter 構築だけを確認したいとき。
- session 系パッケージに初期化処理があるかだけを確認したいときは、パッケージ初期化の最小モジュールを直接読めばよい。

## hash
- 225d0765a07a101fee4e56b031ae231881a4499e5bb8fcbfc8aabb1164bf8c66

# `tui.py`

## Summary
- 利用者が対話的に依頼文を編集して Codex TUI を起動するサブコマンド本体を扱う。元 prompt の作成、エディタ起動、実行パラメータ解決、完全 prompt の保存、TUI 用 AgentCallParameter 構築までの一連の制御がまとまっている。
- TUI で許可する file access mode の検証、Markdown 見出しを StructDoc 階層へ変換する処理、解決済み JSON から `{value: ...}` 形式の値や真偽値を取り出す補助処理も含む。
- TUI ログ領域へ prompt ファイルを書き出すため、TUI 実行前に `.cmoc` ignore を保証する処理と、利用可能なエディタを PATH から選ぶ処理への入口でもある。

## Read this when
- 対話的な `tui` サブコマンドの起動順序、prompt 編集、パラメータ解決、Codex TUI 呼び出しの制御を確認・変更したいとき。
- TUI で使用できる file access mode の扱い、解決済みパラメータから AgentCallParameter を作る処理、完全 prompt の組み立て条件を確認したいとき。
- 利用者が編集する元 prompt や解決後の完全 prompt をどこへ保存するか、TUI 実行時にどの root の `.cmoc` ignore を保証するかを調べたいとき。
- TUI 用 prompt の Markdown 見出しを構造化文書へ変換する挙動、またはコードフェンス内の見出しを無視する解析処理を確認したいとき。
- `cmoc tui` が使うエディタ選択順、エディタ終了失敗時のエラー、HTML comment を除去した prompt 読み取りを確認したいとき。

## Do not read this when
- 通常の CLI サブコマンド共通実行基盤、設定読み込み、repo root や work root の算出そのものを調べたいだけなら、runtime 側の対象を読む。
- TUI パラメータ解決用に Codex exec へ渡す schema やプロンプト定義そのものを調べたいだけなら、TUI resolve parameter builder 側を読む。
- 完全 prompt の汎用的な構築ルールや StructDoc の Markdown レンダリング仕様を調べたいだけなら、prompt_parts や struct_doc 側を読む。
- TUI 以外のサブコマンドの挙動、ログ保存、review や indexing などの各機能を調べたい場合は、それぞれのサブコマンドまたは共通モジュールへ進む。
- エディタや subprocess の一般的な使い方だけを確認したい場合、または Codex TUI 実行後の対話内容を調べたい場合は、この対象を読む必要はない。

## hash
- 3ae76b0057081bf6c6c1b52da9770d39cee78fb9ace94eff6132b444abd4862a
