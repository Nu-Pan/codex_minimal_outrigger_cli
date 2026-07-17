# `apply`

## Summary
- apply サブコマンドの実装パッケージ。abandon、fork、fork_report、join の各処理を扱い、apply の実行制御、状態遷移、Git worktree・branch・process の管理、report 生成、cleanup を確認・変更する入口。

## Read this when
- apply サブコマンドの実装を確認または変更するとき。
- apply fork の orchestration、レビュー・修正ループ、commit、report、復旧処理を調査するとき。
- apply join の merge、force-resolve、conflict、状態更新、cleanup を調査するとき。
- apply abandon の run 検証、process 停止、worktree・branch 削除、state reset を調査するとき。
- apply fork のレポート形式や差分収集を変更するときは、レポート生成の実装を確認するとき。

## Do not read this when
- apply 以外のサブコマンドを扱うとき。
- apply の共通 runtime、lock、process 操作、session state、Git 操作の一般実装だけを調査するときは、対応する共通モジュールへ直接進む。
- レビュー・修正処理の Codex 呼び出しパラメータだけを調査するときは、file review/fix builder の実装へ直接進む。
- apply fork の report 内容だけを調査するときは、レポート実装へ直接進む。

## hash
- d78dd475c8107a9ac4ce6edb243e4e16d48a7ca04ee776713da29228f4dd783b

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
- `want` を書き出した oracle を、review oracle と同じ評価経路へ渡すための入口。評価対象の scope を受けて review 側の実行に委譲するので、oracle の評価フローを辿りたいときに読む。

## Read this when
- oracle の評価を review oracle と同じ経路で実行したいとき。
- scope を指定して、書き出した oracle を評価対象に乗せたいとき。

## Do not read this when
- oracle の実体を生成・修正したいだけのときは、直接その生成元や review 側の実装を読む。
- review の集約・レポート生成・対象列挙を知りたいだけなら、この薄い委譲層ではなく review 側の実装を読む。

## hash
- d2c72efffe412278a6207afbd665dfc79c3aba3444ba20b94bfddab2a5a70d70

# `indexing.py`

## Summary
- `cmoc indexing` サブコマンドの CLI 実行入口。worktree の安全条件を確認し、ロック下で INDEX.md の更新と差分 commit を実行する。

## Read this when
- `cmoc indexing` の実行フロー、worktree 前提条件、インデックス更新・commit 処理を変更または調査するとき。

## Do not read this when
- インデックス更新の具体的な処理や commit の実装自体を調査するときは、`commons.indexing` の実装を直接読む。
- 他のサブコマンドの CLI 実行フローだけを調査するとき。

## hash
- 648fe512e7039f2060fbe5969945f9992a0b8b3697e92d2cbbf949083d8804ce

# `review`

## Summary
- review 系サブコマンド群をまとめる Python package。review oracle の CLI 実行ライフサイクルと、所見検出・対象列挙・INDEX 統合・レポート生成へ進むための入口を提供する。

## Read this when
- review 系サブコマンド群の package 境界や構成を確認したいとき。
- review oracle の実行ライフサイクルを調べるときは oracle.py を読む。
- 所見検出、oracle 対象列挙、INDEX 統合、レポート生成の具体的な処理を調べるときは、この階層内の各担当モジュールを読む。

## Do not read this when
- review oracle の具体的な所見検出ループだけを調べるとき。
- oracle 対象ファイルの列挙規則だけを調べるとき。
- review report の表示形式やファイル書き込みだけを調べるとき。
- review branch の INDEX 変更の commit・merge・conflict 解決だけを調べるとき。

## hash
- d0b68039591eb520040c7a01c7dcb12b6d27b65a6108ca7bdf6becb9892758fd

# `review_index.py`

## Summary
- review oracle 用 worktree の INDEX.md 変更を検証・commitし、INDEX.md のみからなる review branch を session branch に merge するための Git 操作を扱う。変更 path の検査、競合解決、merge 後の commit 取得が下位処理への入口となる。

## Read this when
- review oracle の INDEX.md 変更を commit または merge する処理を確認するとき
- review branch に INDEX.md 以外の差分がないことの検証や、INDEX.md の merge conflict 解決を調べるとき

## Do not read this when
- 通常のアプリケーション機能や review oracle の内容自体を調べるとき
- INDEX.md 変更以外の Git 操作、または一般的な worktree 状態管理を直接確認したいとき

## hash
- ffbcec8958ff3f1466d4fe84e3f1be83be150a4ea79cd32761b2cf7dfbfc4673

# `review_loop.py`

## Summary
- review oracle の finding 列挙・マージ・妥当性検証・採否判定ループを実行する実装。中断時には確定済みの finding と評価済みファイルを保持して呼び出し元へ返す。
- Codex 実行結果を用いた finding 操作の検証、意味的マージの再試行、重複・削除・置換・統合操作の適用を担当する。

## Read this when
- review oracle のループ制御、中断時の進捗保持、step callback 通知を変更・調査するとき
- finding の列挙・マージ・検証・judge の呼び出し条件や反復処理を確認するとき
- merge operation の target_ids 検証、finding の削除・置換・統合処理を変更・調査するとき

## Do not read this when
- review oracle の個別 prompt や Structured Output 定義だけを確認したいときは、対応する oracle builder または oracle 仕様を直接読む
- review サブコマンドのパス解決や CLI 入出力を確認したいときは、review の呼び出し元やパス管理モジュールを直接読む

## hash
- 67c2950e4ce2eb16548da9ed66719586ad5908331c69fe60081a725f768d8696

# `review_paths.py`

## Summary
- oracle_path を解決して絶対パスへ変換する処理と、oracle file のパスを repository-relative key へ変換する処理を提供する。通常の repository root、oracle root alias、既知の managed worktree を扱い、対象外のパスは無視する。symlink を追跡しないパス正規化 helper も含む。

## Read this when
- review report や finding に含まれる oracle_path の解決・正規化・キー化を変更または調査するとき
- oracle root、worktree 境界、symlink の扱いに関係するパス処理を確認するとき

## Do not read this when
- review report の生成ロジックや oracle_path の入力仕様そのものを確認するときは、参照されている oracle 文書・実装を直接読む
- パス処理と無関係な sub-command の実装を変更するとき

## hash
- 2174112c8b159a6683cf0a66278af86d213bbef2c9b6e25917fb93d0e72299c6

# `review_report.py`

## Summary
- レビュー結果を Markdown レポートとして保存・描画するモジュール。frontmatter、レビュー判定、対象 oracle file 一覧、fatal/minor 所見の分類・順序付け、finding の Markdown 表示、パス表示を担当する。レビュー報告の出力形式や判定規則を確認・変更するときの入口。

## Read this when
- review oracle サブコマンドのレポート生成・保存処理を変更するとき
- レビュー結果の verdict、frontmatter、finding 表示順、対象ファイル一覧の出力を確認するとき
- Markdown レポートのパス表示や所見整形を調査するとき

## Do not read this when
- レビュー対象の探索・oracle path 判定そのものを変更するときは、review_paths の実装を先に読む
- レビュー仕様や出力契約を確認するだけの場合は、対応する oracle 文書を直接読む
- CLI コマンドの引数処理やレビュー実行制御を変更する場合は、コマンド実装を直接読む

## hash
- 5f4a38d52d7100ed102c0e28b394ded64b805217b67077066243d9fc80aadcfd

# `review_targets.py`

## Summary
- review oracle の scope に応じてレビュー対象の oracle file を列挙する。full scope では oracle ツリー全体を対象にし、session scope ではセッション開始コミットから review fork commit までに変更された oracle file に限定する。

## Read this when
- review oracle の対象ファイル列挙処理を変更・確認するとき
- full scope と session scope の対象範囲やコミット差分の扱いを確認するとき

## Do not read this when
- oracle file の内容やレビュー実行そのものを変更・確認するとき
- review 対象列挙と無関係なサブコマンドの処理を変更・確認するとき

## hash
- 5ec510cfdccdb608eb26afaabebb8e9075b417b1a87c3300026bf06703324b02

# `session`

## Summary
- session サブコマンドの実装パッケージ。session の各ライフサイクル処理を確認するための入口。
- abandon は active session の破棄、home branch への切替、state 更新、branch 削除、失敗時 rollback を扱う。
- fork は通常 branch と clean worktree を検証し、session branch/state の作成、衝突防止、失敗時 rollback を扱う。
- join は session branch の merge、状態更新、branch 削除、および merge conflict の検出・自動解消を扱う。

## Read this when
- session サブコマンドの実装構成やライフサイクル処理を確認・変更するとき。
- session の abandon、fork、join の個別動作や失敗時 rollback を調査するとき。
- session join の merge conflict 解消や Git の unmerged path 処理を確認するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- session の共通 state schema、Git 操作 helper、CLI runtime の一般仕様だけを調査するときは、それぞれの定義元を直接読む。

## hash
- 55c0997d6e359952976c795adc9259566d48dbe5d7f618561f47d0987d431e8e

# `tui.py`

## Summary
- `cmoc tui` サブコマンドの実行フローと補助処理を担う実装ファイル。利用者向けプロンプトの初期化・編集・読み込み、実行パラメータの解決、Codex TUI の起動、TUI 用ファイルアクセスモードの検証を扱う。TUI サブコマンドの挙動変更や関連するパラメータ構築・エディタ選択・ignore 保証を調べる際の入口。

## Read this when
- `cmoc tui` の起動処理、プロンプト編集、TUI 起動パラメータ、ファイルアクセスモード検証を変更または調査するとき
- TUI 実行前の `.cmoc` ignore 保証やエディタ選択・終了エラーの挙動を確認するとき

## Do not read this when
- TUI 以外のサブコマンドの実装を調べるとき
- 共通 CLI ランタイム、設定、ログ、パラメータビルダー自体の詳細を直接調べるときは、それらの定義元を読む

## hash
- 66edc6a24c58eeba12a447d3a68e8c7bdada3c440e6ff9fd788f8ae5daff1a84
