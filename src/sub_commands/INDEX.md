# `apply`

## Summary
- apply run の開始、進行、破棄、取り込み、実行時状態管理、実行結果 report 生成を扱うサブコマンド実装群への入口。
- session branch と apply branch/worktree をまたぐ状態検証、isolated worktree 上での Codex CLI 実行、process id 管理、成果の merge、後片付け、警告・report 出力など、apply 系操作の制御フローを調べる起点になる。
- 個別の責務は、破棄、fork 実行、fork report、join、process/worktree runtime helper に分かれており、apply の利用者向け挙動と低レベル実行時状態の両方へ分岐する階層。

## Read this when
- apply 系サブコマンド全体のどの実装へ進むべきかを選びたいとき。
- apply run の開始から join または abandon までの状態遷移、branch/worktree 操作、process id 管理、report 出力の関係を把握したいとき。
- apply branch/worktree の作成・探索・削除、session state の更新、clean worktree 検証、merge conflict、warning 出力など、apply 操作の副作用を調べたいとき。
- apply fork の反復制御、finding 適用、禁止対象差分の rollback、commit 作成、converged 判定、通常・エラー report の生成経路を確認したいとき。
- running 状態の apply process を停止する処理、pid file、pidfd、process start time、stale pid の扱いなど、apply 実行時状態の低レベル処理へ進みたいとき。

## Do not read this when
- apply 以外のサブコマンド、session 管理、config schema、git wrapper の一般挙動だけを調べたいとき。
- oracle file、realization file、INDEX.md 生成規則など、仕様文書やルーティング文書の方針そのものを確認したいとき。
- Codex CLI に渡す prompt や parameter 構築だけを調べたいときは、それを組み立てる実装へ直接進む。
- 共通 runtime の branch 操作、state 読み書き、report 保存先、git command 実行など、apply 固有でない helper の詳細だけを確認したいときは共通実装へ直接進む。
- 特定の apply 操作に読む対象がすでに決まっており、破棄、fork、join、report、process 管理のいずれかの本文へ直接進めるとき。

## hash
- 24780d44ae972d7a71c690bc14fd580e3fc7af0149192836ce6395259484cda7

# `indexing.py`

## Summary
- 現在の work root に対するルーティング目次の更新を実行するサブコマンド実装。実行前条件の確認、排他ロック、対象ディレクトリ走査、既存エントリーの再利用、Codex による不足エントリー生成、更新差分のコミットまでをまとめて扱う。
- 目次生成対象から除外する条件、対象内容の取り出し、鮮度判定用ハッシュ、Structured Output から Markdown エントリーへ変換する処理の入口になる。

## Read this when
- 目次更新サブコマンドの実行フロー、preflight 連携、排他制御、更新後コミットの挙動を確認または変更したいとき。
- 目次生成対象に含めるファイル・ディレクトリ、除外条件、既存エントリー再利用条件、深い階層から再生成する順序を調べたいとき。
- Codex 呼び出しで目次エントリーを生成する経路、生成 prompt に渡す対象内容、Structured Output の検証と Markdown 描画を追いたいとき。
- 目次エントリーのハッシュ検証、必須セクション判定、古いエントリーを再生成する条件に関わる不具合を調査するとき。

## Do not read this when
- 個別サブコマンドの業務ロジックや利用者向け機能を調べたいだけで、目次更新処理に関係しないとき。
- Codex 実行ラッパー、git コマンド実行、設定読み込み、ignore 判定などの共通 runtime 実装そのものを変更したいとき。
- 生成される目次エントリーの内容方針や prompt パラメータの仕様だけを確認したいときは、その構築元を直接読む。
- 正本仕様やルーティング文書の記述方針を確認したいだけで、実装上の走査・生成・コミット処理を追う必要がないとき。

## hash
- b861a2700ec18e93a2f924e78d4298110459a99188cc9fb4e01cdb656da25187

# `init.py`

## Summary
- 作業ツリーを cmoc が扱える初期状態へ同期するサブコマンド実装を扱う。実行前の利用者差分を init commit に混ぜないよう staged 差分と .gitignore 状態を退避・復元し、cmoc 用 ignore と設定同期、必要な初期化 commit、成功時の Markdown 出力をまとめて担う。

## Read this when
- 初期化サブコマンドの実行順序、ログ作成前の ignore 保証、設定同期、初期化 commit の条件を確認・変更したいとき。
- 利用者の既存 staged 差分や .gitignore の作業ツリー・index・HEAD 状態を、初期化処理後にどう復元するかを調べたいとき。
- 初期化成功時に標準出力へ出す Markdown 形式の結果表示を確認・変更したいとき。

## Do not read this when
- 初期化以外のサブコマンドの CLI 制御や出力を調べたいとき。
- cmoc 用 ignore の具体的な追記規則そのものや、設定同期処理の中身を調べたいとき。
- git 実行ラッパー、work root・repo root の解決、共通のサブコマンド実行基盤を調べたいとき。

## hash
- d458d8f2867e4dcf14fa58d8f2b16b6ca84c25b5cadf47172131cd16b9070d32

# `review.py`

## Summary
- active session branch 上の oracle を isolated review worktree でレビューするサブコマンド実装の入口を扱う。
- scope 検証、session branch と worktree 状態の前提確認、review 用 branch/worktree の作成と後始末、対象 oracle file の列挙、Codex 実行ループ、INDEX 変更の commit/merge、review report 出力までの orchestration を担う。
- レビュー対象の列挙、レビュー実行ループ、report 描画、merge conflict 解決などの詳細処理は下位 helper module に委譲し、この対象はそれらを CLI コマンドとして接続する位置づけにある。

## Read this when
- oracle review サブコマンドの実行順序、前提条件、失敗時 report 出力、または一時 review worktree と一時 branch のライフサイクルを確認したいとき。
- review scope の受け付け条件や、active session branch・clean worktree・cmoc ignore 確保などの preflight がどこで行われるかを追うとき。
- oracle review の処理全体で、対象列挙、Codex review loop、INDEX 変更 commit、review branch merge、report 書き込みがどの順でつながるかを把握したいとき。
- CLI 層から review 関連 helper へ渡される主要な値、特に session state、config、review worktree、review branch、fork/join commit、findings の流れを確認したいとき。

## Do not read this when
- oracle file の列挙条件や scope ごとの対象選択の詳細だけを確認したい場合は、対象列挙を担当する helper を読む。
- Codex に渡す review prompt、review loop の反復制御、finding の merge operation 適用の詳細だけを確認したい場合は、review loop 側の helper を読む。
- review report の表示形式、finding section の描画、report file の書き込み内容だけを変更したい場合は、report 生成を担当する helper を読む。
- review branch の merge、INDEX 変更 commit、conflict 解決、worktree status path の扱いだけを調べたい場合は、review index 操作を担当する helper を読む。
- 通常の indexing preflight の中身や、Codex 実行・git worktree 作成・branch 削除など runtime 共通処理の実装詳細を確認したい場合は、それぞれの共通 helper を直接読む。

## hash
- 683f45afe7813f49a04b82cb6d1ba48c5faf9f4a588193292002d1d82a68fc2d

# `review_index.py`

## Summary
- oracle review 用 worktree で生成された INDEX.md 差分の commit と、review branch から session branch への merge を扱う。
- INDEX.md 以外の差分検出、porcelain status の path 抽出、INDEX.md だけが conflict した場合に session 側採用で解決する処理をまとめている。

## Read this when
- review worktree の INDEX.md 変更だけを commit する条件、INDEX.md 以外の差分をエラーにする制御、または status parsing を確認・変更したいとき。
- review branch merge の失敗時に INDEX.md conflict だけを自動解決する挙動、merge 後 commit の取得、手動解決へ回す条件を調べたいとき。

## Do not read this when
- review oracle 全体の一時 worktree 作成・削除順序や active session 制約を確認したいときは、`review.py` を読む。
- oracle file の対象列挙、finding loop、または report rendering を確認したいときは、それぞれ `review_targets.py`、`review_loop.py`、`review_report.py` を読む。
- git command 実行 wrapper や worktree 操作 helper 自体の実装を調べたいときは、runtime 側を読む。

## hash
- 42f2f7a768474b5b07e47ec55750ce65ea6bba3439c7cd667355dc5c6ca6efa9

# `review_loop.py`

## Summary
- review oracle による finding の列挙、統合、検証、判定を Codex 実行ループとして制御する実装。oracle ごとの dirty 管理、finding_id や検証理由・判定結果の初期値付与、merge 操作の適用と妥当性検証、finding の oracle_path 解決を扱う。

## Read this when
- review oracle の finding enumerate/merge/validate/judge の実行順序、反復回数、dirty 条件、Codex 呼び出しパラメータ生成との接続を確認したいとき。
- finding の merge 操作で delete/replace/merge がどの条件で受理され、既存 finding がどう削除・追加されるかを確認したいとき。
- finding に含まれる oracle_path を実パスへ解決し、特定 oracle に関連する finding を絞り込む挙動を確認したいとき。
- review oracle が finding_id、advocate_reasons、challenger_reasons、verdict、judge_reason をどの段階で補完・更新するかを確認したいとき。

## Do not read this when
- 個々の Codex プロンプトや Structured Output parameter の本文を確認したいだけの場合は、review oracle 用 parameter builder を直接読む。
- CLI サブコマンドの引数定義、設定読み込み、ログルートや worktree の準備を確認したい場合は、呼び出し元のサブコマンド実装を読む。
- review oracle の反復回数など設定値の定義やデフォルトを確認したい場合は、設定モデルを読む。
- oracle file の正本仕様そのものや review 観点を確認したい場合は、対象の oracle 文書を読む。

## hash
- d116a58b5c91dcc0446b89b792e5dd64c675efd7a66b3858cb3fbbfd92e54581

# `review_report.py`

## Summary
- oracle review 結果を Markdown + YAML frontmatter の report として描画し、report directory へ書き出す処理を扱う。
- verdict 判定、frontmatter fields、評価対象 oracle file の表、fatal/minor finding section、path 表示整形をまとめている。

## Read this when
- review report の出力 path、frontmatter 項目、result/verdict の判定条件、または fatal/minor finding の表示形式を確認・変更したいとき。
- oracle path の表示整形、finding section の Markdown 文面、エラー時 report の描画を調べたいとき。

## Do not read this when
- review oracle の実行順序、一時 branch/worktree、対象 oracle file の列挙、finding loop、INDEX.md merge を確認したいときは、それぞれ該当する review 系 module を読む。
- 生成済み report の個別内容だけを読みたいときは、report 出力先の生成物を直接読む。

## hash
- 5a4bc1bc25bc2c3390133302a704cfab266f75d5d961859b561a4a82777866ee

# `review_targets.py`

## Summary
- oracle review の対象 oracle file を scope 別に列挙する処理を扱う。
- full scope では全 oracle file、session scope では session 開始 commit から変更された oracle file のうち、INDEX.md、git ignored、binary file を除外した対象を返す。

## Read this when
- review 対象となる oracle file の列挙条件、session scope と full scope の違い、または INDEX.md・binary・git ignored file の除外条件を確認・変更したいとき。
- session 開始 commit から oracle 配下の変更 path を取得し、列挙済み oracle file と照合する処理を調べたいとき。

## Do not read this when
- review oracle 全体の実行順序、一時 worktree、finding loop、INDEX.md merge、report rendering を確認したいときは、それぞれ該当する review 系 module を読む。
- binary 判定、git ignored 判定、git diff wrapper 自体の実装を調べたいときは、runtime 側を読む。

## hash
- f42029951fa3338498710cca446b7ee6dbf8f87039fc10726d2cecc385a0c05c

# `session`

## Summary
- session 系サブコマンドの実装をまとめる領域。通常 branch から session branch を作成する処理、active session branch を home branch へ取り込む処理、merge せず破棄する処理を扱う。
- 各サブコマンドは実行前条件、worktree の clean 確認、cmoc ignore の保証、branch 切り替え、session state 更新、利用者向け出力、共通 CLI 実行 wrapper への接続を担う。
- join では merge conflict 発生時に Codex CLI へ解消を依頼し、残存 conflict marker や unmerged path の検査から merge commit まで進める補助処理も含む。

## Read this when
- session fork、session join、session abandon の実行条件、状態遷移、branch 操作、利用者向け出力を確認または変更したいとき。
- 通常 branch から session branch を作成する流れ、active session を home branch へ merge する流れ、または merge せず破棄する流れの実装入口を探すとき。
- session 系サブコマンドが共通 CLI 実行 wrapper、indexing preflight、git 実行 helper、session state 読み書き helper をどの順序で呼び出すかを追いたいとき。
- session join の conflict 解消依頼、解消後の検査、merge commit までの制御を確認したいとき。

## Do not read this when
- session 以外のサブコマンド、CLI 全体のコマンド登録、Typer app 構成を調べたいとき。
- session state の schema、state file path 算出、branch 判定、worktree clean 判定、git 実行、timestamp 生成など共通 runtime helper の内部実装を知りたいだけのとき。
- apply、review、indexing など session 操作以外の業務処理を調べたいとき。
- Codex CLI に渡す conflict 解消依頼パラメータの構築仕様そのものを確認したいとき。

## hash
- 466ff6de3251f18b083d7100e33214824fbab69ca3268efc0094e57e67b94cac

# `tui.py`

## Summary
- 利用者が編集した依頼文を起点に、TUI 用の実行パラメータ解決、完全 prompt の生成・保存、Codex TUI 起動までをつなぐサブコマンド実装。
- 依頼文テンプレートの作成、エディタ選択・起動、HTML コメント除去、解決済み JSON からの AgentCallParameter 構築、Markdown 見出しの StructDoc 変換を扱う。

## Read this when
- 対話的に依頼文を編集して Codex TUI を起動する処理の流れを確認・変更したいとき。
- TUI 起動時の file access mode、model class、reasoning effort、完全 prompt 生成、structured output schema の扱いを確認したいとき。
- 利用可能なエディタの選択順、エディタ異常終了時のエラー、依頼文テンプレートや保存先 log 領域の扱いを変更したいとき。
- TUI 向けパラメータ解決結果の JSON から値や真偽値を取り出す規則、または Markdown 見出しを構造化 prompt に変換する規則を確認したいとき。

## Do not read this when
- 通常の非対話 CLI 実行、Codex exec の低レベル実行、または TUI 以外のサブコマンド起動処理だけを調べたいとき。
- TUI パラメータ解決用 prompt の具体的な schema や選択肢定義そのものを調べたいときは、その解決パラメータを構築する側を読む。
- 完全 prompt の共通フォーマットや StructDoc の markdown レンダリング仕様を調べたいときは、prompt 構築・構造化文書レンダリング側を読む。
- INDEX 生成の preflight 処理そのものを調べたいときは、indexing の preflight 実装を読む。

## hash
- da24e922e6a1930a64a5667c2c3867e90de41524c59de1c97005abece970b630
