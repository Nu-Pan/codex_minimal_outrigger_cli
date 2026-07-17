# `apply`

## Summary
- apply サブコマンドの実装パッケージ。abandon、fork、fork report、join の処理を扱い、apply run の開始からレビュー・修正、差分 commit、merge、report 保存、state 更新、process・worktree・branch cleanup までの実装入口となる。

## Read this when
- apply サブコマンドの実装を確認または変更するとき。
- apply run の lifecycle、state・process tracking、worktree・branch 操作、差分処理、report 生成、join・abandon の挙動を調査するとき。

## Do not read this when
- apply 以外のサブコマンドだけを扱うとき。
- 共通 runtime、Git、worktree、Codex 実行基盤の実装だけを変更・調査するときは、対応する共通実装を直接読む。
- apply fork 内のレビュー・修正プロンプト生成や report 内容だけを扱うときは、対応する下位実装を直接読む。

## hash
- 5f2275d9b011172ec29ff2fb2afa5fe73a6fa692c5de562481b35860e11e2fa4

# `doctor.py`

## Summary
- doctor サブコマンドの実装。CLI runtime を介して doctor 用の preprocess 処理を明示的に実行する。

## Read this when
- doctor サブコマンドの動作や preprocess 呼び出しを確認・変更するとき。

## Do not read this when
- doctor 以外のサブコマンドを扱うとき。preprocess の共通実装自体を確認するときは、共通 runtime preprocess command の実装を直接読む。

## hash
- 9324a8b1f2f1bbd3a83adfb61690e64ff7e1f6502e165e208c84e2cefbd35980

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
- review 系サブコマンド群の Python package。oracle 実行入口と、関連するレビュー処理モジュールへの入口を含む。

## Read this when
- review oracle の CLI 実行フロー、worktree・branch 管理、レビュー対象選定、割り込み・例外処理を調査するとき
- review 系サブコマンドの package 構成や関連モジュールへの入口を確認するとき

## Do not read this when
- 判定ループ、対象列挙、レポート形式、INDEX の commit・merge 処理など、個別機能だけを調査するときは対応する実装モジュールを直接読む
- package 初期化の import や公開シンボルだけを調査するときは、具体的な処理を持たない初期化モジュールを読む必要はない

## hash
- 261d8f5ae9ec1180763418a7bfa77e257cfbad56d74bc7b1a72d8903d6c04c43

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
- レビュー対象の oracle file 群に対して、finding の列挙・意味的マージ・反証/擁護による検証・採否判定を反復実行する review oracle loop の実装。
- 中断時には確定済み finding と評価済みファイルを専用例外で呼び出し元へ返し、merge operation の形式・対象 ID・重複を検証して不正な Structured Output を再試行する。

## Read this when
- review oracle の実行フロー、進捗保持、KeyboardInterrupt 時の部分結果、finding の検証・判定を変更または調査するとき
- finding の merge operation 契約や、列挙・マージ・反証・擁護・judge の Codex 呼び出し連携を確認するとき

## Do not read this when
- review コマンド全体の CLI 入出力やパス定義だけを確認したいときは、対応する review command/path の実装を直接読む
- review oracle の各 agent prompt の内容だけを変更・確認するときは、各 build parameter の実装を直接読む

## hash
- a818d7636b9973397e8b7b34f401427387d1d7a45e6d767a29bb182175c210fb

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
- review oracle の結果を Markdown レポートとして生成・保存する実装。レポートの保存先、YAML frontmatter、Verdict、対象 oracle 一覧、Fatal/Minor 所見の分類・順序、エラーや中断時の結果判定、finding と path の描画を扱う。review oracle レポート出力の実装を変更・調査する際の入口。

## Read this when
- review oracle サブコマンドのレポート形式、保存処理、Verdict 判定、finding の表示順を変更・検証するとき
- レビュー結果の frontmatter や Markdown セクション構成が期待どおりか調査するとき
- 所見の severity・verdict 分類、oracle path 表示、エラー・中断・対象なしの扱いを確認するとき

## Do not read this when
- レビュー処理そのものの対象探索、oracle 内容の評価、git branch 操作を調査するときは、対応するレビュー実行・探索処理を直接読む
- 一般的なレポート生成や他サブコマンドの出力を調査するとき

## hash
- 05e364b8ace32c3e484f56c08353323b1de9befbf8a066acd22af1d43106b742

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
- session サブコマンドの実装パッケージ。fork、join、abandon の各 session 操作に関する CLI 実装を確認する入口。

## Read this when
- session サブコマンドの実装や構成を確認・変更するとき。
- session branch、session state、cleanup、merge、rollback など session 操作の挙動を調査するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- 共通の git 操作、state 操作、Codex 実行規則、session データモデル自体を直接確認するとき。

## hash
- fd4b0da87a48090397a866c729c2b89e9e18e7a38833e92107be89c7220385bd

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
