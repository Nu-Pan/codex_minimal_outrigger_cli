# `apply`

## Summary
- apply 系サブコマンド群の実行時ロジックをまとめる実装ディレクトリ。apply run の開始、実行中状態の補助管理、破棄、成果取り込み、実行結果 report 生成までを扱う。
- apply branch/worktree、apply process id、session state、差分反映、merge、後片付けなど、apply の lifecycle に関わる具体処理への入口になる。

## Read this when
- apply run の開始から終了、破棄、join までの全体像や、apply state がどの操作で遷移・初期化されるかを追いたいとき。
- apply branch や apply worktree の作成・特定・削除、session branch との関係、実行可能 branch の検証を確認・変更したいとき。
- apply process id の保存・削除、実行中 process の停止、abandon 時の TERM/KILL 待機など、apply 実行プロセス管理を調べたいとき。
- apply fork による finding 列挙、変更適用、編集禁止対象の差分検出と rollback、commit 作成、report 出力を確認・変更したいとき。
- apply join による apply branch の成果 merge、想定外差分や conflict の扱い、force-resolve、apply worktree と branch の後片付けを確認・変更したいとき。
- apply fork または join の report 内容、変更要約、失敗時 report の保存内容を確認・変更したいとき。

## Do not read this when
- apply 以外のサブコマンドの CLI 定義、dispatch、共通 Typer 配線だけを確認したいとき。
- session state の schema、session_id の生成・管理、apply.apply_branch のデータ構造そのものを確認したいときは、状態モデルや session 管理側へ進む。
- git command wrapper、worktree root、state 読み書き、clean worktree 判定、CmocError の表示形式など、複数サブコマンドで使う共通 runtime の詳細だけを調べたいとき。
- apply fork で Codex に渡す prompt、AgentCallParameter、structured output の構成だけを確認したいときは、それらを組み立てる専用実装へ進む。
- oracle file、realization file、INDEX.md 生成規則など、apply 処理が参照・保護する対象概念の仕様自体を調べたいとき。

## hash
- fe3df4dd9232765d81636083f223e67c48ce065137c6d16f98ff4830e7f48da1

# `indexing.py`

## Summary
- 現在の作業ツリーに対するルーティング文書の更新処理を実装するサブコマンド本体。対象ディレクトリと子要素の列挙、既存エントリーの再利用判定、Codex 呼び出しによるエントリー生成、Markdown への描画、更新差分の git commit、並列生成、排他 lock をまとめて扱う。
- Codex 実行前 preflight から同じ更新処理を呼べるようにし、CLI 実行時には cmoc 管理対象チェックを経由して更新件数を表示する入口も持つ。
- ルーティング文書の鮮度判定に使う hash、対象内容の取り出し、root 直下の memo や git ignored/binary 対象の除外といった、indexing 全体の制御ロジックを読む入口になる。

## Read this when
- ルーティング文書を生成・更新するサブコマンドの挙動、実行順序、commit 条件、排他制御を確認または変更したいとき。
- どのファイルやディレクトリがルーティング文書の対象になるか、memo・git ignored・binary・隠し要素の除外条件を確認または変更したいとき。
- 既存エントリーを再利用する条件、hash の計算方法、エントリー形式の検証、Structured Output から Markdown へ変換する処理を調べたいとき。
- Codex CLI に個別エントリー生成を依頼する引数、対象本文の渡し方、生成結果が不正な場合のエラー経路を確認したいとき。
- indexing preflight と通常サブコマンド実行で共有される更新処理の関係を追いたいとき。

## Do not read this when
- ルーティング文書に書くエントリー本文のプロンプトや Structured Output パラメータの詳細だけを確認したい場合は、builder 側のエントリー生成パラメータを読む方が直接的。
- cmoc の path 概念、git 実行 wrapper、config 読み込み、hash 計算、binary 判定、git ignore 判定の実装詳細だけを調べたい場合は、runtime や path/model 系の定義を読む方が直接的。
- 特定ディレクトリのルーティング文書の内容や、個別ファイルの読むべき条件を確認したいだけなら、対象階層のルーティング文書または対象本文を読む方が適切。
- CLI 全体のコマンド登録や Typer app 構成を調べたい場合は、サブコマンドを束ねる上位の CLI 定義を読む方がよい。

## hash
- 5caec3c108af017e4f099f3725503817a9313d74c0bfd0de22795909a98b29d8

# `init.py`

## Summary
- work root を cmoc 利用可能な初期状態へ同期する init サブコマンドの実装。実行前から staged だった利用者差分を init commit に混ぜないよう退避・復元しつつ、.cmoc の ignore 保証、設定同期、必要な初期 commit、成功結果の Markdown 出力を扱う。
- init だけがログ作成前に必要とする .cmoc ignore 保証と、その副作用を利用者の .gitignore 状態へ戻すための一時状態管理・復元 helper を含む。

## Read this when
- init サブコマンドの実行フロー、出力文言、初期 commit の作成条件、または work root 初期化時の git 操作を確認・変更したいとき。
- init 実行前に staged だった利用者差分や .gitignore の worktree/index/HEAD 状態が、init 後にどう復元されるかを確認したいとき。
- .cmoc を .gitignore に追加する処理が、ログ作成前の pre_log_check と通常の init 処理でどう扱われるかを追いたいとき。

## Do not read this when
- init 以外のサブコマンドの通常処理、CLI 全体のコマンド登録、または共通 runtime の挙動を確認したいだけのとき。
- work root の解決、git コマンド実行ラッパー、設定同期、.cmoc ignore 追加そのものの共通実装を変更したいときは、それらを定義する共通 runtime 側を直接読む方がよい。
- init の外部仕様ではなく、oracle file と realization file の定義や INDEX.md 生成方針を確認したいとき。

## hash
- 40c8a1439f1e36929bf9fd0e25dc79c5c54a820fe6578bff3ea04bf81445060f

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
