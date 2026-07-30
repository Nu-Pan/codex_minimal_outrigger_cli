# `apply`

## Summary
- 現在、apply サブコマンドの実装ファイルはありません。

## Read this when
- apply サブコマンドの実装が追加された後、その内容を確認するとき。

## Do not read this when
- apply 以外のサブコマンドを扱うとき。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `doctor.py`

## Summary
- `cmoc doctor` サブコマンドの実装。CLI ランタイム経由で doctor preprocess を 1 ステップ実行し、完了後に repo_root を表示する。doctor コマンドの実行経路と preprocess 呼び出しの入口として扱う。

## Read this when
- doctor サブコマンドの実装や実行手順を変更・調査するとき
- doctor preprocess の呼び出し位置、実行ステップ、表示内容を確認するとき

## Do not read this when
- doctor preprocess 自体の仕様や処理内容を確認したいときは、参照される oracle/doc/app_spec/doctor_preprocess.md を直接読む
- CLI ランタイム共通処理の仕様や実装だけを確認したいとき

## hash
- 48cc149773f0620f64d4650bed55bdb7b42dada088e55d312892186978176836

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

# `oracle`

## Summary
- oracle 系サブコマンドをまとめる package。oracle の編集・調査・レビュー機能への入口であり、レビュー実行、対象列挙、パス解決、レポート生成、INDEX 差分の commit／merge などの実装へ案内する。
- 編集・調査・レビューそれぞれの個別 CLI フローと、review loop・対象選定・パス解決・レポート・Git 操作の詳細実装を含む。

## Read this when
- oracle 系サブコマンドの package 構成や入口を確認するとき。
- oracle edit、oracle investigation、oracle review の CLI 実行フローを変更・調査するとき。
- oracle review の対象列挙、finding 処理、パス解決、レポート出力、INDEX.md の commit／merge 処理を確認するとき。

## Do not read this when
- 個別サブコマンドの入力部品や TUI 起動パラメータ構築など、より具体的な下位実装だけを確認したいとき。
- oracle review の finding 判定、対象列挙、パス解決、レポート生成など単一責務の詳細だけを調査するときは、対応する下位実装を直接読む。
- 他のサブコマンドや一般的な CLI runtime、Codex TUI 自体の実装を調査するとき。

## hash
- 89d3539c4eb91ebc7e7ddafd50267ec3c6441498f5618b938b2852539afd3a67

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口。apply workload と refactor workload、およびそれぞれの CLI 実行・ライフサイクル関連処理への入口を提供する。
- apply は realization apply fork の実行、例外処理、run state、fork report、差分検査、commit 処理を扱う。
- refactor はリファクタリング fork の初期化から対象調査・修正、差分・commit 検証、unresolved 所見追跡、完了判定、cleanup、report 保存までを扱う。

## Read this when
- realization workload サブコマンドの実装構成やパッケージ入口を確認するとき。
- realization apply workload または `cmoc realization apply fork` の動作を調査・変更するとき。
- realization のリファクタリング fork の実行順序、対象選択、commit、完了条件、report 保存を調査・変更するとき。
- apply または refactor における fork の状態管理、検証、エラー処理、cleanup を確認するとき。

## Do not read this when
- realization apply workload や refactor workload に関係しない処理を確認するとき。
- Codex builder の launch parameter、agent parameter、state データ構造、対象同期処理だけを確認したいとき。
- run lifecycle の共通仕様や process tracking、isolation、report 処理だけを確認したいとき。
- realization apply または realization refactor の利用者向け仕様だけを確認したいとき。

## hash
- 6983835b09b08dee1a99df472c2b5ed99ce9bcaefd79739bd4ce72c21ceeace8

# `review`

## Summary
- review サブコマンドの realization 実装を配置するディレクトリ。現在は実装本文がなく、レビュー処理の具体的な入口として参照できる下位要素はない。

## Read this when
- review サブコマンドの実装ファイルを追加・変更する場所を確認するとき。

## Do not read this when
- oracle review の処理内容や仕様を調べるときは、対応する oracle 実装・仕様文書を直接読む。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `run`

## Summary
- editing run の共通 lifecycle サブコマンドをまとめるパッケージ。abandon・join の実装と、共通 lifecycle/report 実装への互換 shim を下位要素として案内する入口。

## Read this when
- editing run の abandon、join、ライフサイクル、report 連携を調査・変更するとき。
- run worktree・branch・state・process tracking・rollback・cleanup・report の処理経路を追うとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。
- 特定の処理の実装詳細を確認する場合は、この入口ではなく配下の該当ファイルを直接読むとき。
- 共通 lifecycle や report の canonical 実装そのものを確認する場合は、commons 側の実装を読むとき。

## hash
- 487cfc797f092144b6fb5980fa1a2c7f5200bee0e5d3f21250e7429a4fc84f01

# `session`

## Summary
- session サブコマンドの実装パッケージ。session の各ライフサイクル操作を確認する際の入口となる。
- session の abandon・fork・join サブコマンド実装を含む。

## Read this when
- session サブコマンドの実装構成やライフサイクル処理を確認・変更するとき。
- session の branch 操作、state 管理、merge、cleanup、失敗時復旧の挙動を横断的に調査するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- 特定の session サブコマンドだけを調査・変更する場合は、該当する実装ファイルを直接読む。

## hash
- a12b38f37341e0ada494e5c0d04aea1042f7528583228f05e396368a56d18652

# `tui.py`

## Summary
- `cmoc tui` サブコマンドの実行フローを担う実装。プロンプト編集、実行パラメータ解決、Codex TUI 起動を、リポジトリおよび作業ルートのコンテキストで統合する。TUI 起動用パラメータの構築と、解決済み JSON の真偽値抽出も提供する。

## Read this when
- `cmoc tui` の起動処理、プロンプト入力、実行パラメータ解決、Codex TUI 呼び出しを変更・調査するとき
- TUI 用 `AgentCallParameter` の構築や解決済み設定値の扱いを確認するとき

## Do not read this when
- TUI の起動パラメータ定義そのものを確認したいときは、TUI builder の実装を直接読む
- プロンプト編集の入力仕様を確認したいときは、prompt editor input の実装または参照される oracle 文書を直接読む
- CLI 共通実行処理や設定読み込みの仕様だけを確認したいときは、cmoc runtime の実装を直接読む

## hash
- a257bd9698b2b21e78a3eaf80056c7cb90787bb53c494cc35b490e8e2710a60f
