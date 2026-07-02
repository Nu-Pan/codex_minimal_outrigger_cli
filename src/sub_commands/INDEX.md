# `apply`

## Summary
- apply 系サブコマンドの実行制御をまとめる実装ディレクトリ。fork による apply run 開始、abandon による破棄、join による session への取り込み、実行中 process 管理、worktree・branch・state・report の扱いを入口として持つ。
- apply run のライフサイクル全体を読むための入口であり、具体的な処理は開始、破棄、取り込み、runtime helper、report 生成の責務ごとに分かれている。

## Read this when
- apply run の開始から終了、破棄、取り込みまでの状態遷移や cleanup の責務分担を確認したいとき。
- apply branch、apply worktree、session branch、process id file、Codex subprocess、report が apply 系サブコマンド間でどう扱われるかを調べたいとき。
- apply fork、apply abandon、apply join のどの実装へ進むべきかを判断したいとき。
- apply 実行中 process の停止、pid reuse 対策、worktree 探索、apply branch 復元など、apply 専用 runtime helper を探したいとき。
- apply fork の結果 report や失敗 report、変更要約、未収束時表示を確認・変更したいとき。

## Do not read this when
- apply 以外のサブコマンド実装、共通 CLI 配線、Typer option 登録だけを調べたいとき。
- git コマンド実行 wrapper、state 永続化、report 保存先、clean worktree 検証など、apply に限らない低レベル共通処理を変更したいとき。
- Codex に渡す prompt や parameter の組み立て内容そのものを確認したいとき。
- パッケージ説明や import 副作用の有無だけを確認すればよく、具体的な apply 制御ロジックを読む必要がないとき。

## hash
- 052d7cb7b9ffe916d7f3bf92c634d12c3c601961cbdb66ef0067b1312b9264b9

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
- `cmoc init` の実行本体を担い、CLI runtime 経由で初期化処理を起動する。work root の `.cmoc` ignore 保証、設定同期、`.agents` の追跡用 placeholder 作成、初期化 commit、実行前の staged 差分や `.gitignore` 状態の復元を扱う。
- init 実行前にログ出力先が git 管理へ混入しないよう ignore 状態を整え、実行後には Markdown 形式の成功結果を組み立てる。

## Read this when
- `cmoc init` の外部挙動、初期化時の git 操作、`.gitignore` や exclude の扱いを確認・変更したいとき。
- init が既存の staged 差分や利用者の `.gitignore` 作業ツリー状態をどう退避・復元するかを調べたいとき。
- `.agents` が空の場合に追跡対象の placeholder を作る処理、または init commit に含める対象を確認したいとき。
- `cmoc init` の stdout 文面を変更したいとき。

## Do not read this when
- init 以外のサブコマンド実装を調べたいとき。
- CLI runtime 共通の実行制御、git コマンド wrapper、work root や repo root の解決、設定同期 helper 自体の仕様を調べたいとき。
- oracle 側の init 仕様や ignore 仕様そのものを確認したいとき。

## hash
- c54e629b998aecdefbd2cba613d73532e598c4a29248a962d643403f76950293

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
- session 系サブコマンドの実装をまとめるディレクトリ。
- session の開始、home branch への統合、merge しない破棄など、session branch と session state を操作する各サブコマンド実装への入口になる。
- 各実装は CLI runtime 経由の実行、事前条件検証、git branch 操作、状態更新、成功時出力、失敗時の利用者向けエラーや rollback を扱う。

## Read this when
- session 系サブコマンドの実装全体から、目的の操作に対応する読む先を選びたいとき。
- session branch の作成、home branch への merge、merge しない破棄など、session lifecycle に関わる CLI 挙動を調べたいとき。
- session 操作の事前条件、状態遷移、branch 削除、clean worktree 要求、merge conflict 対応のどれがどの実装に属するかを切り分けたいとき。

## Do not read this when
- CLI 全体のコマンド登録、Typer アプリ構成、共通 runtime、git 実行 wrapper、path model など、session 個別操作ではない共通基盤を調べたいとき。
- session state の schema、永続化形式、branch 判定 helper、worktree clean 判定そのものの実装を直接確認したいとき。
- oracle 側の正本仕様断片や、session 以外のサブコマンド実装を調べたいとき。

## hash
- 119ad92e34ce996052054e3d9c5130fa60339eab184386f4b007909fe876d20f

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
