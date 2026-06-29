# `apply`

## Summary
- apply サブコマンド群の実装を収める領域で、apply run の開始、join、abandon と、それらを支える runtime 補助や report 生成を扱う。
- session branch と apply branch/worktree の関係、apply state の遷移、Codex 実行、成果取り込み、破棄、process 追跡・停止の入口になる。

## Read this when
- apply fork、join、abandon のいずれかの CLI 実行フロー、状態遷移、branch/worktree cleanup、利用者向け出力を確認・変更したいとき。
- apply branch と session branch/worktree の対応、apply process id file、Codex subprocess tracking、running apply の停止処理を確認・変更したいとき。
- apply fork の report 保存、変更要約、所見数推移、成功・失敗時の記録内容を確認・変更したいとき。
- apply scope の対象列挙、変更 file の再キュー、直近 join 済み merge commit からの差分範囲、apply 成果の commit や session branch への merge を追いたいとき。

## Do not read this when
- apply 以外のサブコマンド、CLI 共通 runtime、git wrapper、設定 load、state file 入出力の共通処理だけを調べたいとき。
- apply の正本仕様や公開仕様そのものを確認したいときは、oracle doc を読む方が適切なとき。
- Codex CLI 全般の挙動、prompt profile、または apply fork 用 prompt parameter の詳細だけを調べたいとき。
- 実装を読む必要がなく、パッケージ説明や import 副作用の有無だけを確認したいときは、入口ファイルだけで足りるとき。

## hash
- e1c4a72101bde94aae63bc56b8518e55926996fe42a679a0641967c36f6e2367

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
- CLI runtime 経由で初期化処理を実行し、work root を cmoc が扱える状態へ同期するサブコマンド実装。
- .cmoc ignore の保証、設定同期、初期化コミット作成、実行前に staged だった利用者差分と .gitignore 状態の復元、成功時の Markdown 出力生成を扱う。
- 初期化ログ作成前に必要な ignore 状態を整える入口と、git index・worktree 状態を壊さないための復元 helper 群を含む。

## Read this when
- 初期化サブコマンドの実行順序、run_cli_subcommand への渡し方、pre-log 処理、または use_work_root_runtime の使い方を確認・変更したいとき。
- .cmoc を .gitignore または repository exclude へ入れる初期化時の副作用、ログ作成前の ignore 保証、repo root と work root が異なる場合の扱いを確認したいとき。
- 初期化中に利用者の staged 差分、.gitignore の HEAD・index・worktree 状態を退避・復元する挙動を調査・修正したいとき。
- 初期化が作成する commit、git add・diff・restore・apply・update-index など git 操作の流れを追いたいとき。
- 初期化成功時に標準出力へ表示する Markdown の内容を変更・確認したいとき。

## Do not read this when
- 初期化以外のサブコマンドの CLI 挙動、引数定義、または出力を調べたいとき。
- cmoc runtime の共通処理、path 解決、git 実行 wrapper、設定同期、ignore pattern 生成そのものの実装を調べたいとき。
- 初期化コマンドの外部仕様や利用者向け要求を確認したいだけで、実装上の git 状態復元や副作用制御を追う必要がないとき。
- テストケース、fixture、または oracle 側の正本仕様断片を探しているとき。

## hash
- f8b5eb0008695af8fb9f118551e0687e29e4af4f0bc257bc241dd7c6a435f237

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
- review oracle の finding 収集から統合、検証、判定までの反復制御を担う実装。
- oracle file ごとに既存 finding との関連を渡して列挙を行い、merge operation を検証して finding list に適用し、advocate/challenger の検証理由を蓄積したうえで最終 verdict と judge reason を設定する。
- finding 内の oracle_path を絶対 path、worktree 相対 path、または path token 付き表記から解決し、対象 oracle file に紐づく finding を絞り込む処理も含む。

## Read this when
- review oracle の enumerate、merge、validate、judge の実行順序や反復停止条件を確認したいとき。
- review oracle が生成・更新する finding の初期値、finding_id の採番、advocate_reasons/challenger_reasons/verdict/judge_reason の扱いを変更または確認したいとき。
- merge finding の delete、replace、merge operation の検証条件、target_ids の重複・未知 ID の扱い、置換後 finding の作り方を調べたいとき。
- finding の oracle_path がどのように実 path に解決され、特定の oracle file に関連する finding と判定されるかを確認したいとき。
- Codex 実行関数へ渡す review oracle 用 builder parameter、cwd、root、purpose の組み立てを追いたいとき。

## Do not read this when
- 個々の review oracle prompt や Structured Output parameter の内容を確認したいだけなら、builder 側の該当実装を読む。
- review_oracle のループ回数など設定値の定義や読み込みを確認したいだけなら、設定モデル側を読む。
- path token の仕様や resolve_real_path の詳細な解決規則を確認したいだけなら、path model 側を読む。
- CLI サブコマンドとして review oracle loop がどこから呼ばれるか、引数や利用者向け入出力を確認したいだけなら、呼び出し元の sub command 実装を読む。
- finding の内容品質や LLM 判定結果そのものを調べたい場合は、この制御実装ではなく実行ログや生成結果を確認する。

## hash
- b19cd10eb6d96e1d94ba9b04991f574bba4c0ba9898fd7f44625b5cdb29ecc0b

# `review_report.py`

## Summary
- review oracle 実行結果のレポート本文を生成し、reports 配下へ Markdown と YAML frontmatter 付きで保存する処理を担う。
- レビュー対象数、評価済み oracle、採用・不採用の所見件数、エラー有無から結果判定を作り、fatal/minor と accepted/rejected に分けた所見一覧を描画する。
- oracle パスの表示正規化や frontmatter 値の描画など、review oracle レポート固有の小さな整形 helper も含む。

## Read this when
- review oracle のレポート保存先、ファイル生成、Markdown 構成、frontmatter 項目、結果判定文言を確認または変更したいとき。
- accepted/rejected や fatal/minor の所見分類が、レポート上でどの順序・見出し・件数として表示されるかを確認したいとき。
- oracle file のパスがレポート内でどのように相対表示または oracle 起点表示へ整形されるかを調べたいとき。
- review oracle 処理の失敗、対象 0 件、fatal 所見あり、minor 所見あり、問題なしの場合のレポート上の verdict を確認したいとき。

## Do not read this when
- review oracle の対象 oracle 探索、所見検出、所見採否判定、git branch 操作そのものを調べたいとき。
- review oracle 以外のサブコマンドのレポート形式や出力処理を確認したいとき。
- reports ディレクトリや timestamp の汎用的な定義・生成規則を調べたいとき。
- oracle file の正本仕様内容や review oracle コマンドの利用者向け仕様そのものを確認したいとき。

## hash
- 3037be4342dfe983940c1941048f9fc8dda8a2a3d6b09819bc09e381fd478a77

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
- session 系サブコマンドの実装群で、session branch の作成、home branch への join、merge せず破棄する abandon など、session のライフサイクル操作を扱う。
- CLI runtime から呼ばれる各操作の事前条件確認、git branch 操作、session state file 更新、利用者向け出力、失敗時の復旧処理へ進むための入口となる。
- merge conflict 解決を Codex CLI に依頼する join 固有の制御や、timestamp による session-id 生成、cleanup 失敗時 rollback など、個別操作ごとの詳細は下位モジュールに分かれている。

## Read this when
- session 系サブコマンドのうち、どの操作の実装を読むべきかを選びたいとき。
- active session の作成、join、破棄に関する実行条件、状態遷移、branch 操作、state file 更新、利用者向け出力の実装箇所を探したいとき。
- session branch と home branch の関係、clean worktree 要求、managed branch 禁止、既存 active session 検出、session-id 衝突回避など、session 操作に共通または近接する制御を調べ始めるとき。
- join 時の merge conflict 解決、abandon 時の cleanup 失敗 rollback、fork 時の state file 作成など、session ライフサイクル上の個別ケースへ読む先を振り分けたいとき。

## Do not read this when
- CLI 全体のサブコマンド登録、Typer アプリ構成、共通 runtime の仕組みだけを調べたいとき。
- session state のデータ構造、永続化形式、path model、git 実行 wrapper、worktree clean 判定、branch 判定 helper の実装そのものを調べたいとき。
- session 以外のサブコマンドや、apply state など別領域の状態操作を調べたいとき。
- 個別の session 操作が既に特定できており、その処理詳細だけを読むべきときは、対応する実装モジュールへ直接進む。

## hash
- 54af30b1ac4fd33d09edf5f94335851f9563968f677a02534c40f54facc9bff3

# `tui.py`

## Summary
- `cmoc tui` の実行本体を担う realization implementation。利用者が編集する元 prompt の作成、エディタ起動、prompt からの TUI 起動パラメータ解決、Codex TUI 起動までの一連の制御を扱う。
- TUI 実行前に `.cmoc` ignore を保証し、TUI で許可される file access mode の検証、解決済み JSON から `AgentCallParameter` への変換、ネストされた `{value: ...}` 形式の値取得を行う。

## Read this when
- `cmoc tui` の起動フロー、prompt 編集から Codex TUI 起動までの制御順序を確認・変更したいとき。
- TUI 用の元 prompt テンプレート、保存先、HTML comment 除去、エディタ選択、エディタ異常終了時の扱いを確認したいとき。
- TUI の file access mode 制限、解決済みパラメータの既定値、`role`・`summary`・`goal`・各 standard flag から TUI 起動用パラメータを組み立てる処理を確認したいとき。
- TUI 実行時に `.cmoc` ignore をどの root に対して保証するか、repository root と work root の扱いを確認したいとき。

## Do not read this when
- TUI 向け prompt からパラメータを推定する LLM 呼び出し用入力の schema や builder 自体を確認したいだけなら、resolve parameter 側を読む。
- Codex TUI 起動用 prompt 全体の文面・構成・標準指示の内容を確認したいだけなら、launch TUI parameter builder 側を読む。
- CLI runtime 全般、repository root や work root の解決、Codex 実行 wrapper、設定読み込みの共通挙動を確認したいだけなら runtime 側を読む。
- TUI 以外の sub command の実行フローや引数処理を確認したい場合は、対象 sub command の実装を読む。

## hash
- 5fd4f89ffaa5bd36df37c3140cac01b525bd4d460c1d94bdea8dd4925d644cd2
