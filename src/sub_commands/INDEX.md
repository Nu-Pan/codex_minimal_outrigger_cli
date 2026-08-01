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
- oracle 系サブコマンドの実装をまとめる package。編集・調査・レビューの各サブコマンドと、レビュー処理を構成する対象列挙、パス解決、差分統合、レポート生成などの下位実装への入口を提供する。

## Read this when
- oracle サブコマンドの構成や実行入口を確認するとき
- oracle review の実行経路、対象選定、finding 処理、INDEX 差分統合、パス解決、レポート生成の実装箇所を特定するとき

## Do not read this when
- 個別サブコマンドの詳細な処理を確認する場合は、対応する実装ファイルを直接読む
- 共通 CLI runtime や git・session 管理など、oracle package 外の共通処理だけを調査する場合

## hash
- ff9dfe07b5fd461acee9fbc1693175e4d9ca1422f804a78bf9787199ea1c248e

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
- `cmoc tui` サブコマンドの実行フローを担当する実装。プロンプト編集、実行パラメータ解決、Codex TUI 起動を、CLI ランタイムと現在の worktree コンテキストに接続する。TUI の起動処理、解決済みパラメータからの `AgentCallParameter` 構築、ネストされた真偽値の読み取りを確認したい場合の入口。

## Read this when
- `cmoc tui` の CLI 実行フローを変更・調査するとき
- オリジナルプロンプトの収集から Codex TUI 起動までの連携を確認するとき
- TUI 起動パラメータや実行時の root、worktree、設定の受け渡しを確認するとき

## Do not read this when
- TUI 用の個別パラメータ生成ロジック自体を変更・調査する場合は、参照先の builder 実装を直接読むとよい
- `cmoc tui` 以外のサブコマンドの実行フローや共通ランタイムの仕様だけを調べる場合

## hash
- a2beb411104f9d6157b6de05b641d0fa5d32f4103ed5ee895fdb872293522a99
