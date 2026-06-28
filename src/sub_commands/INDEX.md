# `apply`

## Summary
- apply 系サブコマンドの実行本体をまとめる領域。run の開始、join、abandon、report 生成、実行時 process/worktree 管理まで、apply branch と apply worktree を使った隔離実行と session branch への取り込みに関する実装へ進む入口になる。
- 対象 worktree の解決、pid file と process tracking、実行中 process の停止、編集禁止対象の検出と復元、state 更新、cleanup、利用者向け report 出力など、apply run のライフサイクル全体に関わる処理が下位に分かれている。

## Read this when
- apply run の開始、破棄、join、report 生成、実行時補助のどれを読むべきかを選びたいとき。
- apply branch、apply worktree、session branch、apply state の関係や、apply run の状態遷移に関わる実装の入口を探しているとき。
- apply の実行中断、abandon、cleanup、process 停止、pid file 管理、worktree/branch 削除に関係する不具合を調査するとき。
- apply fork の対象列挙、Codex による finding 列挙と適用、変更の再キュー、commit/report/state 更新の流れを追いたいとき。
- apply join での merge、想定外差分検出、force-resolve、merge conflict、成功後 cleanup、report 出力を確認したいとき。
- apply fork report の保存内容、frontmatter、変更要約、差分収集、要約生成失敗時の fallback を調べたいとき。

## Do not read this when
- apply 以外のサブコマンド実装、共通 CLI dispatch、共通 runtime helper、git command wrapper、state file の一般的な読み書きだけを調べたいとき。
- 正本仕様、oracle の文書、path model、または実装全体の設計原則を確認したいとき。
- Codex に渡す prompt parameter や acp builder 側の詳細だけを調べたいとき。
- branch/worktree 操作の低レベル共通処理や report directory の共通 path 解決だけが目的で、apply 固有の制御に関心がないとき。
- テスト追加先や apply 挙動の外部仕様だけを探しており、実装本体へ進む前にテスト領域または oracle 領域を確認すべきとき。

## hash
- d35e1a8eece6bbffeeef4a13fb3b9f53a811a53d4932b5a34a9a2accf2dd5db5

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
- review oracle の実行結果を、人間が読む報告書として Markdown と YAML frontmatter に整形し、reports 配下へ書き出す処理を担う。
- レビュー対象 oracle の一覧、採用・不採用に分けた fatal/minor 所見、処理失敗や対象なしを含む最終 verdict、報告書内での oracle path 表示を組み立てる。

## Read this when
- review oracle report の保存先、生成タイミング、frontmatter、見出し、表、所見セクション、verdict 文言を変更したいとき。
- 採用所見と不採用所見、fatal と minor の分類が報告書にどう表示されるかを確認したいとき。
- oracle path を報告書上でどのように相対表示するか、または oracle ツリー外の path をどう表示するかを確認したいとき。
- review oracle の失敗時、対象 oracle なし、accepted fatal あり、accepted minor あり、問題なしの場合の report result と本文を調べるとき。

## Do not read this when
- review oracle が oracle file をどう収集・評価するか、所見をどう生成・判定するかを知りたいだけのとき。
- CLI の引数定義、サブコマンド登録、実行フローの入口を調べたいとき。
- reports directory や timestamp の共通仕様そのものを確認したいとき。
- INDEX.md 生成やルーティング文書の仕様を調べたいとき。

## hash
- 12c1a56a7dc4c31d006b2c3c0fd1b8962a519f80f003772c9f2c8c96ee20fa10

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
- session 系サブコマンドの実装をまとめるディレクトリ。session branch の作成、home branch への join、merge せず破棄する abandon など、session のライフサイクル操作に関する CLI 実行本体へ進む入口になる。
- 各サブコマンドは CLI runtime 経由で実行され、branch/state/worktree の事前条件確認、git 操作、session state 更新、利用者向け出力、失敗時の扱いなどをそれぞれの責務範囲で扱う。

## Read this when
- session 系サブコマンド全体の実装候補を探し、作成・合流・破棄のどの処理へ進むべきかを判断したいとき。
- session branch と home branch の関係、active session の状態遷移、session state file の更新、session branch の削除など、session 操作に関わる制御を調べたいとき。
- session fork、join、abandon の実行条件、失敗条件、git 操作順序、利用者向け出力のいずれかを確認・変更したいとき。
- merge conflict を Codex CLI に解消させる join 経路や、abandon 失敗時の state/branch rollback など、session 操作固有の復旧処理を調べたいとき。

## Do not read this when
- session 以外のサブコマンド実装、共通 CLI ルーティング、またはサブコマンド登録の仕組みを調べたいとき。
- git 実行 wrapper、CLI runtime、worktree clean 判定、branch 判定、path model、state file 読み書き helper などの共通 runtime 実装そのものを調べたいとき。
- session state schema や apply state schema の定義そのものを確認したいとき。
- Codex CLI に渡す conflict resolution parameter の具体的な組み立てや、INDEX.md 生成・indexing preflight の共通仕様を調べたいとき。

## hash
- c8787fb01d40933b2ced05ca16287fe12372650e2375d9becad599e8156e4c40

# `tui.py`

## Summary
- 利用者が入力した依頼文を編集させ、解決用 Agent 呼び出しで TUI 実行パラメータを決め、完全な prompt を保存して Codex TUI を起動するサブコマンド実装を扱う。
- TUI 実行前の indexing preflight、ログ領域の `.cmoc` ignore 保証、元 prompt と完全 prompt の保存、利用可能エディタ選択、Markdown 見出しの構造化、解決済み JSON からの AgentCallParameter 構築を一つの流れとして担う。

## Read this when
- 利用者編集用 prompt から Codex TUI 起動までの制御フローを確認または変更したいとき。
- TUI で許可する file access mode、resolve parameter の結果の読み取り、完全 prompt に含める oracle/review/indexing 系フラグの扱いを確認したいとき。
- TUI 用ログ領域への元 prompt・完全 prompt の保存先、保存名、`.cmoc` ignore の事前保証に関わる挙動を確認したいとき。
- TUI 起動前に使うエディタの選択順、エディタ異常終了時のエラー、prompt テンプレート中の HTML comment 除去を扱うとき。
- Markdown の見出し・本文・コードフェンスを StructDoc 階層へ変換する処理を確認または変更したいとき。

## Do not read this when
- TUI ではなく exec など別サブコマンドの CLI 制御や入出力を確認したいだけのとき。
- Codex 実行ランタイム、設定読み込み、repository/work root 判定、ログ実行基盤そのものの実装を確認したいとき。
- resolve parameter の prompt 生成内容や TUI で選べる file access mode の定義自体を確認したいとき。
- 完全 prompt の共通生成ロジックや StructDoc のレンダリング仕様そのものを確認したいとき。
- エディタ起動や Markdown 構造化ではなく、TUI セッション内で Codex が行う作業内容を調べたいとき。

## hash
- 374ac7e1a3e18a4b8a01c23ab501cd5769d6c0792add919a64687852a17d1984
