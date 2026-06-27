# `apply`

## Summary
- apply 系サブコマンドの実行制御をまとめる実装領域。apply run の開始、破棄、取り込み、実行結果 report 生成、実行中 process 管理までを扱う。
- session branch と apply branch、linked worktree、apply state、pid file、git diff/merge/commit、Codex CLI 呼び出しが関係する apply 固有の処理へ進む入口になる。
- 上位の CLI runtime や state schema そのものではなく、apply 操作としてそれらをどう組み合わせるかを確認するための対象。

## Read this when
- apply run を開始して isolated worktree 上で所見適用、差分 commit、report 生成、状態更新を行う流れを確認・変更したいとき。
- 未 join の apply run を破棄して ready 状態へ戻す cleanup、または実行中 apply process の停止と pid file 管理を追いたいとき。
- apply 実行結果を session branch へ取り込む join 条件、想定外差分の検出、force-resolve、merge conflict 処理、後片付けを調べたいとき。
- apply branch や session branch から linked worktree を特定する処理、apply worktree path、process 同一性確認、Linux 依存の process 停止処理を扱うとき。
- apply fork や join が生成する利用者向け report の内容、保存先、変更要約、warning 表示を確認・変更したいとき。
- apply 固有の CLI 挙動、標準出力、終了コード、状態遷移、作業ツリーや branch の cleanup をサブコマンド単位で調べたいとき。

## Do not read this when
- apply 以外の session 作成・終了、review、indexing など別サブコマンド固有の挙動を調べたいとき。
- git command 実行 wrapper、state file の基本 schema、path model、config schema、timestamp や report root など共有 runtime の詳細だけが必要なとき。
- Codex に渡す prompt parameter の本文や structured output parameter の詳細だけを調べたいとき。
- apply に関係しない oracle/realization の一般ルール、INDEX.md 生成規則、indexing preflight の仕様を確認したいとき。
- パッケージ説明や import 時副作用の有無だけを確認したい場合を除き、具体的な実行処理を読まずに済ませたいとき。

## hash
- 9b3f4b44a2cbf2347fa903080a1c8658ab9455316152a5da2c17842ea2e09af5

# `indexing.py`

## Summary
- indexing サブコマンドの実行入口を定義し、CLI runtime 経由で INDEX.md maintenance を起動する実装。
- 実行前に indexing 用 preflight を有効化し、worktree の安全条件を検査したうえで、現在の work root に対する index 更新・commit・更新件数表示までを統括する。
- 実際の index 更新処理、lock、commit、Codex exec 型は共通 indexing 実装へ委譲し、この対象はサブコマンドとしての接続と実行順序を担う。

## Read this when
- indexing サブコマンドの CLI 実行経路、runtime wrapper への渡し方、command 名や argv の扱いを確認したいとき。
- INDEX.md maintenance 実行時に、work root の lock、index 更新、commit、更新件数出力がどの順序で呼ばれるかを確認したいとき。
- indexing 実行前に clean worktree や cmoc ignored 条件を要求する precondition の接続先を確認したいとき。
- run_codex_exec を CodexExec として index 更新へ渡す流れや、テストなどで codex_exec を差し替える入口を確認したいとき。

## Do not read this when
- INDEX.md の内容生成、差分検出、個別ファイル走査、lock 実装、index 更新結果の commit 実装そのものを調べたいときは、共通 indexing 実装を直接読む。
- work root の決定方法、CLI runtime の共通実行制御、Codex exec の実行方法を調べたいときは、runtime 側の実装を直接読む。
- 他サブコマンドの CLI 接続や出力形式を調べたいときは、そのサブコマンドの実装を読む。
- indexing の高水準な正本仕様や oracle と realization の関係を確認したいだけなら、対応する oracle 文書を読む。

## hash
- cc7f1d7ba65fd8dd216ba1c42b817d8af6f63eecceef84fabbc96b7793ac1a37

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
- review oracle の実行結果を、人間が読む Markdown レポートとして保存・描画する実装。
- レビュー対象 oracle の件数、判定済み finding の severity/verdict 別集計、対象 oracle ごとの finding 数、実行中エラー、関連 branch/commit 情報をレポート本文と frontmatter にまとめる。
- oracle 配下の path 表示を、repo root からの相対表記または path 中の oracle 起点表記へ整える補助処理も担う。

## Read this when
- review oracle のレポート生成、保存先、frontmatter、Verdict 文言、finding セクション、対象 oracle 一覧の出力内容を確認・変更したいとき。
- review oracle の結果判定が error、no_targets、fatal、minor、ok のどれになるかを確認・変更したいとき。
- finding の accept/reject や fatal/minor の集計、または oracle path の表示形式がレポートにどう反映されるかを調べたいとき。

## Do not read this when
- review oracle が oracle file をどのように収集・検査するか、finding をどう生成するかを調べたいだけのとき。
- review oracle 以外のサブコマンドのレポート、CLI 引数、状態管理、git 操作を確認したいとき。
- Markdown レポートの出力内容ではなく、oracle file や realization file の正本仕様そのものを確認したいとき。

## hash
- c735d523554a1f2fc90ccdc9d92499da36540150b1ce2795cb72602f2930bc62

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
- 利用者が編集する依頼文を作成し、解決用の Codex 実行で TUI 起動パラメータを決め、完全 prompt を保存して Codex TUI を起動する一連の処理を担う。
- TUI 実行前の ignore 設定保証、元 prompt と完全 prompt のログ保存、利用可能なエディタ選択、エディタ実行失敗時のエラー化、Markdown 見出しの構造化、解決済み JSON からの AgentCallParameter 構築を扱う。

## Read this when
- 対話的な依頼文編集から Codex TUI 起動までの実行フローを確認・変更したいとき。
- TUI で許可する file access mode、reasoning effort、model class、structured output schema path、完全 prompt の組み立て方を確認したいとき。
- 利用者が編集する元 prompt のテンプレート、HTML comment 除去、Markdown 見出しの StructDoc 変換、完全 prompt の保存場所に関わる挙動を変更したいとき。
- TUI 起動前に `.cmoc` を ignore 対象へ入れる処理や、root と work root の両方を扱う条件を確認したいとき。
- `code`, `nano`, `vim`, `vi` からエディタを選ぶ順序、エディタ起動コマンド、エディタ異常終了時の利用者向けエラーを変更したいとき。
- TUI parameter 解決結果の `{value: ...}` 形式を読む helper や、未指定時の既定値の扱いを確認したいとき。

## Do not read this when
- 通常の非対話 CLI 実行、Codex exec の低レベル実行、または TUI 以外のサブコマンド処理だけを調べたいとき。
- TUI parameter を解決するための prompt 定義や schema そのものを変更したいときは、解決パラメータ構築側を直接読む。
- 完全 prompt の共通構築ルールや prompt part 全般を変更したいときは、prompt 構築の共通実装を直接読む。
- CLI runtime の共通的なログ、設定読み込み、root 解決、Codex 実行 wrapper の挙動だけを確認したいときは、runtime 側を直接読む。
- INDEX 生成や preflight の詳細だけを調べたいときは、preflight 実装を直接読む。

## hash
- 034a10d810f3d7817287889468a6df514a4b69570a46b9315aec8e257c9d98d1
