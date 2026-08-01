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
- oracle 系サブコマンドの実装をまとめるディレクトリ。編集、調査、レビューの各 CLI 入口と、レビュー対象列挙・ループ・パス解決・レポート・INDEX 差分処理への入口を提供する。

## Read this when
- oracle 系サブコマンドの構成や、各サブコマンド実装への入口を確認するとき。
- oracle review の実行ライフサイクル、対象選定、レビュー処理、レポート生成、INDEX 差分の統合処理を横断して調査するとき。

## Do not read this when
- 特定の oracle サブコマンドやレビュー処理の詳細だけを確認したいとき。対応する個別実装を直接読む方が適切。
- 共通 CLI runtime、設定読み込み、プロンプト入力など、oracle サブコマンド固有でない処理を調査するとき。

## hash
- 2b9f81cee3dbed523fa1f5ae690ef42d83c607248f011f5e611a5121a69c6bcf

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口。apply workload と realization refactor の実行構成へ進むための上位エントリー。

## Read this when
- realization workload サブコマンドの実装や構成を確認するとき。
- apply workload の実行フロー、fork のライフサイクル、差分検査、rollback、cleanup を調査するとき。
- realization refactor の fork 実行、対象選択、agent call、commit、state・report 管理を調査するとき。

## Do not read this when
- realization workload や realization refactor に関係しない処理を確認するとき。
- apply fork の launch parameter 構築だけを確認したいとき。
- state 同期、target 選択、共通 run lifecycle、report 表示などの共通実装だけを確認したいとき。

## hash
- 8902fe26739f5d4d3ac7367aa8bdd6c5f34bc96d1a21c9f205f27d9939a556ce

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
- session サブコマンドの実装パッケージ。session の各ライフサイクル操作に対応するサブコマンド実装への入口。

## Read this when
- session サブコマンドの構成や実装を確認・変更するとき
- session の fork、join、abandon のライフサイクル処理を扱うとき

## Do not read this when
- session 以外のサブコマンドを扱うとき
- Git 実行、state 管理、CLI ランタイムなど共通機能だけを確認するときは、対応する共通モジュールを直接読む

## hash
- 1b01f38b1306948237ab7a586e9027b86dfa7174512a360ba4f41377675838b6

# `tui.py`

## Summary
- `cmoc tui` サブコマンドの実行入口と本体処理を定義する。プロンプト編集、実行パラメータ解決、Codex TUI 起動を連携し、現在のリポジトリ状態から設定・作業ルートを取得して処理する。TUI 起動用パラメータの構築と、解決済み JSON の真偽値変換も担う。

## Read this when
- `cmoc tui` の CLI 実行フロー、プロンプト入力、パラメータ解決、Codex TUI 起動の連携を変更・調査するとき。
- TUI 起動用 `AgentCallParameter` の構築や、解決済みパラメータの解釈を変更・調査するとき。

## Do not read this when
- TUI のパラメータ解決規則そのものを確認したいときは、参照されているパラメータ構築側の仕様・実装を直接読む。
- プロンプトエディタの入力・無視設定の詳細や、共通ランタイム処理の仕様を確認したいときは、それぞれの共通モジュールを直接読む。

## hash
- 6d1d7abde773789d65402ae4e98d2edea2dde77c64a10e7c65ef77757604fb9b
