# `apply`

## Summary
- apply サブコマンド実装をまとめる階層で、fork・join・abandon の各実行本体、apply 実行時 process/worktree 管理、fork report 生成を扱う。
- apply run の開始、完了後の join、未 join run の破棄、実行中 pid 管理、作業レポート生成など、apply 関連の上位 orchestration と cleanup の入口になる。

## Read this when
- apply サブコマンド群のうち、fork・join・abandon・runtime 管理・fork report 生成のどこを読むべきか切り分けたいとき。
- apply run の branch/worktree 作成、state 遷移、Codex 適用 loop、join/abandon cleanup、process 停止、report 出力に関係する実装を探すとき。
- apply branch と session branch の関係、linked worktree 探索、apply process pid file、merge conflict 処理、force-resolve、作業レポートの生成範囲を確認したいとき。

## Do not read this when
- apply 以外のサブコマンド実装を探しているとき。
- session state のデータ構造、git wrapper、report directory、timestamp などの共通 runtime 処理そのものを確認したいとき。
- Codex に渡す prompt、Structured Output、subprocess 起動方法など、apply orchestration から呼ばれる下位処理の詳細だけを確認したいとき。

## hash
- 2b1a84a98dbbdc88e97353089ed87f45f592b7622c91c4477aa13c214c4f9a4b

# `indexing.py`

## Summary
- CLI runtime 経由で INDEX.md maintenance を実行する indexing subcommand の入口を定義する。
- indexing preflight を有効化し、現在の work root を対象に lock、index 更新、更新 commit、更新数の出力までをまとめる。
- 実行前条件として cmoc 管理対象の ignore 状態と clean worktree を要求し、current worktree を使う runtime 設定にしている。

## Read this when
- indexing subcommand の CLI 実行フロー、preflight、runtime 設定を確認したいとき。
- INDEX.md maintenance がどの work root を対象にし、lock、更新、commit、出力へ進むかを追いたいとき。
- indexing 実行前の安全条件として、ignore 状態や clean worktree の検査がどこで行われるかを確認したいとき。

## Do not read this when
- INDEX.md の生成・更新ロジックそのものを調べたいときは、index 更新を担う共通処理を読む。
- Codex 実行や CLI subcommand runtime の汎用挙動を調べたいときは、runtime 側の共通処理を読む。
- 他の subcommand の仕様や実行フローを調べたいときは、その subcommand の実装を読む。

## hash
- 300dd7538efb7a60cb06753149ee3b7f779bd687acbf6cc8a567083f8e6fa0a8

# `init.py`

## Summary
- 初期化サブコマンドの実行本体を扱う。runtime 経由で初期化処理を走らせ、ログ作成前に必要な ignore 設定を保証し、設定同期と初期化 commit を行ったうえで結果表示を組み立てる。
- 利用者が実行前から持っていた staged 差分や作業ツリー上の ignore 設定を初期化 commit に混ぜないよう、一時退避と復元を行う責務を持つ。

## Read this when
- 初期化サブコマンドの実行順序、commit 対象、stdout の成功表示を確認・変更したいとき。
- 初期化時に `.cmoc` を ignore する処理や、ログ作成前の ignore 保証がどこで行われるかを調べたいとき。
- 初期化処理が利用者の staged 差分や作業ツリー上の ignore 設定をどう保護・復元するかを確認したいとき。
- work root と設定側 root が異なる場合の ignore 設定や設定同期の挙動を追いたいとき。

## Do not read this when
- 初期化サブコマンド以外の CLI コマンド挙動を調べたいとき。
- ignore パターンを追加する低レベル処理そのものや git 実行 wrapper の実装を確認したいとき。
- 設定同期の内部仕様や保存形式を調べたいとき。
- ビルド成果物ではなく正本の実装ソースを変更する必要があるとき。

## hash
- f8b5eb0008695af8fb9f118551e0687e29e4af4f0bc257bc241dd7c6a435f237

# `review`

## Summary
- review 系サブコマンドの package 境界と、review oracle ワークフローの入口を含む領域。package 自体の所属確認は初期化ファイルで足り、review oracle の実行順序、前提確認、review worktree・branch、対象列挙からレポート・後始末までの統括はコマンド本体へ進む。

## Read this when
- review 系サブコマンドが属する package 領域を確認したいとき。
- review oracle コマンド全体の入口、実行順序、事前条件、scope、review worktree・review branch、レポート出力、後始末の流れを確認したいとき。
- review oracle 関連 helper の集約・再公開関係や、下位モジュールがコマンド本体から呼ばれる順序を追いたいとき。

## Do not read this when
- review 以外のサブコマンド領域を調べたいとき。
- 個別の oracle file 列挙条件、review loop 内の Codex 実行結果処理、finding から merge 操作への変換、レポート本文の描画や出力先パスだけを確認したいとき。その場合は該当責務を持つ下位モジュールを直接読む。
- 具体的な処理内容が不要で、review 系サブコマンドの package 境界だけ分かればよいときは、初期化ファイルだけを読む。

## hash
- be788e4e3373869a8515ab1e8bcd95ed6eb56b1d18390f937b29189ebc9b7cc7

# `review_index.py`

## Summary
- review 用 worktree で生成された差分を INDEX.md だけに限定して commit し、review branch を session branch へ merge するための処理を扱う。
- review oracle による INDEX.md 以外の変更を検出してエラーにし、INDEX.md だけの merge conflict は session branch 側を優先して自動解決する。

## Read this when
- review oracle が生成した INDEX.md 差分の commit 条件や、INDEX.md 以外の差分を拒否する挙動を確認したいとき。
- review branch の merge 失敗時に、INDEX.md conflict だけを自動解決する制御を確認したいとき。
- git status、cached diff、unmerged stage を使った review index 更新の git 操作を変更したいとき。

## Do not read this when
- 通常の CLI 引数定義やサブコマンドの入口を確認したいだけのとき。
- INDEX.md の本文生成ロジックやエントリー内容の仕様を確認したいとき。
- review branch 以外の branch 作成、worktree 作成、session 管理の処理を確認したいとき。

## hash
- fd46086c773e71294be6c9b8ed3da758d0729bfa1dc795d5f35336f661efd447

# `review_loop.py`

## Summary
- review oracle の finding 収集、merge、validate、judge を設定された反復回数で実行し、finding list を更新して返す制御ロジックを扱う。
- oracle path と finding の対応付け、merge operation の検証と適用、finding_id や検証理由・判定結果の初期化を含む。

## Read this when
- review oracle の enumerate/merge/validate/judge の実行順序、反復条件、dirty 管理を確認・変更したいとき。
- finding の merge operation の delete/replace/merge の制約、未知 ID や重複 ID の扱いを確認・変更したいとき。
- finding 内の oracle_path を実パスへ解決する処理や、特定 oracle file に関連する finding の抽出条件を確認したいとき。
- codex_exec に渡す review oracle 用 builder parameter、purpose、root/cwd/config の接続箇所を追うとき。

## Do not read this when
- review oracle 用 prompt や Structured Output parameter の内容そのものを確認したいだけなら、builder 側の対象へ進む。
- cmoc の path placeholder 全般や resolve_real_path の仕様を確認したいだけなら、path model 側の対象へ進む。
- review oracle 以外のサブコマンド処理、CLI 引数定義、設定ファイル読み込みを確認したいだけなら、それぞれの実装対象へ進む。
- 個別 oracle file の仕様内容や review 対象文書そのものを確認したいだけなら、oracle 側の対象へ進む。

## hash
- b19cd10eb6d96e1d94ba9b04991f574bba4c0ba9898fd7f44625b5cdb29ecc0b

# `review_report.py`

## Summary
- review oracle の実行結果を Markdown レポートとして書き出す処理を扱う。レポート保存先の作成、YAML frontmatter、判定文、評価対象 oracle file 一覧、accepted/rejected finding の集計と描画を担う。
- finding の severity/verdict による分類、エラー・対象なし・fatal/minor/ok の最終判定、oracle 配下を基準にした表示用パス整形の挙動を確認する入口になる。

## Read this when
- review oracle レポートの出力内容、見出し順、frontmatter 項目、判定結果、finding 集計数を変更または確認したいとき。
- review oracle の結果ファイルがどこに作られ、どのような Markdown 本文として描画されるかを追いたいとき。
- oracle file の表示パスや、finding が評価対象一覧の件数にどう対応づけられるかを確認したいとき。
- review oracle のエラー時、対象 0 件時、fatal/minor finding 検出時、問題なし時の表示文を確認したいとき。

## Do not read this when
- review oracle がどの oracle file を収集するか、どのレビュー処理を実行するか、finding をどう生成するかを調べたいだけのとき。
- 汎用的なセッション状態、レポートディレクトリ、タイムスタンプ生成の定義を確認したいとき。
- oracle file の正本仕様そのものや、review oracle コマンドの上位仕様を読みたいとき。
- レポート描画ではなく CLI 引数解析、git branch 操作、作業ツリー操作の実装を確認したいとき。

## hash
- e39d2f34db4295c4bb34632d44f1497bc943c37042808e9be704d149e29ae234

# `review_targets.py`

## Summary
- review oracle の対象ファイル列挙を担う実装。scope が full の場合は oracle file 全件を返し、それ以外では session_start_commit から HEAD までに変更された oracle 配下の対象だけを返す。
- oracle file の候補から AGENTS.md、INDEX.md、root memo、git ignore された未追跡ファイルを除外する判定境界を持つ。

## Read this when
- review oracle の対象範囲が full と差分指定でどう切り替わるかを確認したいとき。
- session_start_commit がない場合の review oracle 対象列挙の挙動を確認したいとき。
- oracle 配下から review 対象候補に含めるファイルと除外するファイルの実装条件を確認したいとき。

## Do not read this when
- oracle file の概念定義や正本仕様上の責務を確認したいだけのとき。
- review 結果の出力形式、診断内容、表示文言を確認したいとき。
- oracle 以外の realization file や memo の列挙条件を確認したいとき。

## hash
- 00f712ea56b7dacdfbe5d7a0faf2bd9c9f3629aa7f0ce1a36ffa2280b37e3eb9

# `session`

## Summary
- session サブコマンドの build 配下 Python package。管理対象 session branch を作る処理、home branch へ merge する処理、session を abandoned にして branch を消す処理の実行実装を収める。
- 各サブコマンドの runtime 呼び出し、事前条件検証、git 操作、session state 更新、失敗時 rollback や警告、利用者向け出力へ進む入口になる。

## Read this when
- 生成済み build 配下で session サブコマンド群の実装候補を絞り込みたいとき。
- session の fork、join、abandon のどの実装を読むべきか判断したいとき。
- session branch の作成、merge、削除、state 更新、worktree clean 確認、merge conflict 解消フローに関係する実装を探したいとき。
- session package 自体に初期化処理や公開 API があるかを確認したいとき。

## Do not read this when
- 編集対象の実装を変更したいとき。生成済み build 配下ではなく source 配下の対応実装を読む。
- session サブコマンドの正本仕様を確認したいだけのとき。対応する oracle doc を読む。
- session state のデータ構造、state file path、CLI runtime、git wrapper、worktree 判定などの共通 helper そのものを調べたいとき。定義元へ直接進む。
- session 以外の CLI サブコマンドを調べたいとき。

## hash
- 01dd3ef44caf349820720b35861c1c06d86767ee5cb4dc4dd99e627a36d7d0d7

# `tui.py`

## Summary
- TUI サブコマンドの実行入口と本体処理を扱う。依頼文テンプレートの作成、エディタ起動、解決用 Codex exec 呼び出し、起動用パラメータ構築、Codex TUI 起動までの流れをまとめている。
- TUI で許可する file access mode の検証、TUI 用プロンプト生成パラメータの既定値、`.cmoc` ignore 保証、TUI parameter JSON からの値取り出しもここで扱う。

## Read this when
- TUI サブコマンドの起動フロー、依頼文編集、ログ領域への prompt 作成、Codex TUI 起動に関する挙動を確認または変更したいとき。
- TUI 用の file access mode 制限、resolve parameter の JSON から AgentCallParameter を組み立てる処理、role・summary・goal・各 standard フラグの既定値を確認したいとき。
- TUI 実行前に `.cmoc` を ignore する処理、または利用可能なエディタ選択とエディタ異常終了時のエラー処理を確認したいとき。

## Do not read this when
- CLI runtime 全体の共通実行、設定読み込み、Codex exec/TUI の低レベル実行方法を知りたいだけなら、それらを提供する runtime 側を読む。
- TUI の resolve parameter や launch parameter の schema・prompt 構築そのものを変更したい場合は、それぞれの builder 側を直接読む。
- 通常の CLI サブコマンド追加や、TUI 以外のサブコマンド実装を探している場合は、該当するサブコマンド実装へ進む。

## hash
- 5fd4f89ffaa5bd36df37c3140cac01b525bd4d460c1d94bdea8dd4925d644cd2
