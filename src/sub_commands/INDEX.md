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
- oracle 系サブコマンドの実装群を含むディレクトリ。編集、調査、レビューの CLI 実行入口と、レビュー対象列挙・パス解決・ループ・INDEX 差分処理・レポート生成などの下位実装への入口を提供する。

## Read this when
- oracle サブコマンドの一覧、実装配置、個別サブコマンドやレビュー関連処理の入口を確認するとき。
- oracle edit・investigation・review の CLI 実行経路を調査するとき。
- oracle review の対象列挙、パス解決、レビュー判定、INDEX 差分処理、レポート生成の担当ファイルを特定するとき。

## Do not read this when
- 特定サブコマンドの詳細実装を確認する場合は、このディレクトリの該当ファイルを直接読む。
- レビュー判定、対象列挙、パス解決、INDEX 差分処理、レポート生成の詳細だけを調べる場合は、それぞれの担当ファイルを直接読む。
- Codex TUI 自体や、oracle サブコマンド以外の共通 CLI runtime を調査する場合。

## hash
- e69b213ffadfe4b7465b316a3e47603b93a79dbc26ab9fda12b879498544d2d6

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口。apply workload と refactor workload を束ね、各処理の下位実装への入口となる。

## Read this when
- realization workload サブコマンドの構成や、apply・refactor のどちらを調査すべきか確認するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。

## hash
- 7b264537f54597e8a7b16ce8d24a975b3a9faf3eb80d76d77cfd93f9f526e82b

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
- `cmoc tui` の CLI 実行フローを担当する実装。入力プロンプトの収集、実行パラメータの解決、Codex TUI 用パラメータの構築、対象 worktree での TUI 起動を一連の runtime 処理として実装している。

## Read this when
- `cmoc tui` の起動処理、プロンプト入力、実行パラメータ解決、Codex TUI 起動の流れを変更または調査するとき。
- 解決済みパラメータから `AgentCallParameter` を構築する処理や、TUI 実行時の repository/worktree コンテキストを確認するとき。

## Do not read this when
- TUI 用の個別パラメータ定義やプロンプト内容の正本仕様を確認したいときは、参照コメントに示された oracle doc を直接読む。
- 共通 CLI runtime、設定読み込み、プロンプト入力収集の共通処理だけを変更または調査するときは、それぞれの共通モジュールを直接読む。

## hash
- fbdd08269efbbff2e6a6820d30b8bc62602ddb51e91183451fe1b430eb68fc66
