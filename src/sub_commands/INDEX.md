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
- review 系サブコマンドの Python package。package 初期化モジュールと、session branch の検証から隔離 worktree でのレビュー実行、finding のマージ、後始末、レポート出力までを統括する oracle review 実装を含む。個別の対象列挙・レビュー loop・レポート・INDEX 更新の詳細実装への入口でもある。

## Read this when
- review 系サブコマンド全体の package 境界や構成を確認したいとき。
- oracle review の起動条件、session branch 検証、隔離 worktree のライフサイクル、レビュー結果の統合を確認・変更するとき。
- review 系サブコマンドの具体的な処理へ進む入口を判断したいとき。

## Do not read this when
- 対象列挙、レビュー loop、finding 操作、レポート生成、INDEX 更新の個別実装だけを確認・変更したいときは、対応する下位実装を直接読む。
- package 初期化時の import、副作用、公開シンボルだけを調べたいとき。ただし初期化モジュールからはその責務は読み取れない。

## hash
- fc7e7aae9781f01c4e2ebd8ee4346cceb9e349fdf2441422539a790d7354bebd

# `review_index.py`

## Summary
- INDEX.md の変更だけを対象に、レビュー用 worktree の差分検証・commit・review branch の merge を行う処理をまとめたモジュール。INDEX.md 以外の差分拒否や、INDEX.md 限定の競合解決も扱う。

## Read this when
- oracle review による INDEX.md 更新の commit や review branch の merge 処理を変更・確認するとき。
- レビュー差分の対象制限、commit 判定、INDEX.md 限定の merge conflict 解決を確認するとき。

## Do not read this when
- 通常の INDEX.md 生成・内容解析を変更するとき。
- レビュー以外の git 操作や、INDEX.md 以外のファイルを扱う commit 処理を確認するとき。

## hash
- c7170abeb443d0c1825c25dae7baef0bd238c5e0205370db443e8f139878b029

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
- Oracle review の結果を timestamp 名の Markdown レポートとして保存・描画する実装。レポートの frontmatter、判定、評価対象一覧、severity・採否別の所見表示、パス表示を扱う。

## Read this when
- oracle review のレポート保存、Markdown/YAML frontmatter の形式、Verdict 判定、所見の分類・表示順を変更または確認するとき。

## Do not read this when
- oracle review の対象探索や finding の生成・判定ロジックを変更するとき。
- レビュー実行フローや session branch の操作を確認するときは、対応する実行・状態管理の実装を直接読む。

## hash
- d1b607f4227847c8dcbac22c7aee6cb0a9660b8a9447acafb684ae684d10ebff

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
