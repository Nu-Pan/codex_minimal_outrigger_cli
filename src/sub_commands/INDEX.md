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
- doctor サブコマンドの実装。CLI runtime を介して doctor 用の preprocess 処理を明示的に実行する。

## Read this when
- doctor サブコマンドの動作や preprocess 呼び出しを確認・変更するとき。

## Do not read this when
- doctor 以外のサブコマンドを扱うとき。preprocess の共通実装自体を確認するときは、共通 runtime preprocess command の実装を直接読む。

## hash
- 9324a8b1f2f1bbd3a83adfb61690e64ff7e1f6502e165e208c84e2cefbd35980

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
- oracle 系サブコマンドをまとめる package。編集・調査・レビューの CLI 入口と、レビュー対象列挙、所見ループ、パス解決、レポート、INDEX 更新などの実装への入口を提供する。

## Read this when
- oracle 系サブコマンドの package 構成や CLI 入口を確認するとき。
- oracle review の実行フロー、対象列挙、レビュー処理、パス解決、レポート出力、INDEX 更新の責務分担を確認するとき。

## Do not read this when
- 個別サブコマンドの詳細実装を調査するときは、該当する実装ファイルを直接読む。
- TUI 起動パラメータの具体的な構築や oracle 編集処理の詳細を調査するときは、対応する下位実装を直接読む。
- oracle review の仕様そのものや、Codex TUI・共通 CLI runtime の詳細だけを調査するとき。

## hash
- 462ccec589780cdba5a5f1fe9925d7294d61a012c7d88cc9e0dada16897c638d

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口。apply と refactor の処理へ進む起点となる。

## Read this when
- realization workload サブコマンドの実装や構成を確認するとき。
- realization apply または realization refactor の処理を調査・変更するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。
- apply・refactor の共通 lifecycle や report 形式だけを確認するとき。

## hash
- a316111b16aa6e81a0498ea25d82d1d93fa0ab666836d183687f2c4a6b3d1d89

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
- editing run の共通 lifecycle サブコマンドと、関連する互換 shim をまとめるパッケージ。abandon・join の処理全体や、旧 import path の互換性を確認する入口であり、個別 helper の詳細は配下の該当ファイルを直接読む。

## Read this when
- editing run サブコマンドの共通 lifecycle、abandon、join、または旧 import path の互換 shim を調査・変更するとき
- run の process、worktree、branch、state、report の cleanup・同期・互換性を確認するとき

## Do not read this when
- editing run 以外のサブコマンドを扱うとき
- git 操作、state 操作、process tracking、report 出力などの共通 helper の実装詳細を確認するとき
- join や report の利用者向け仕様、state の正本定義、canonical な共通実装を確認するとき

## hash
- 086e4b17ca6db22c382c89b1b693a3fb9801bf5f3fc30950917566198730b370

# `session`

## Summary
- session サブコマンドの実装パッケージ。session 関連の実装を確認する際の入口。
- active session を検証し、home branch への切り替え後に session branch と state を abandoned として整理する処理。失敗時の rollback と cleanup error 表示を扱う。
- local branch から session branch と session state を作成する処理。active session 検査、clean worktree 要求、session-id 衝突回避、失敗時 rollback を扱う。
- session branch を home branch に merge する処理。conflict 解消依頼、merge 後の state 更新、branch 削除、安全性警告、結果表示を扱う。

## Read this when
- session サブコマンドの実装や構成を確認・変更するとき。
- session abandon の事前条件、branch/state の cleanup、失敗時復旧を変更・調査するとき。
- session fork の branch 作成、state 保存、session-id 生成、競合防止、rollback を変更・調査するとき。
- session join の merge、conflict 解消、merge 完了処理、branch 削除、結果表示を変更・調査するとき。
- session join における unmerged path・conflict marker 検出、NUL framing、Codex CLI 実行コンテキストを確認するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- session の開始・継続・完了など、abandon 以外の処理を調査するときは、対象サブコマンドの実装を直接読む。
- session join 以外の session サブコマンドだけを調査するとき。
- conflict resolution parameter の生成仕様だけを確認するときは、専用の conflict resolution 実装を直接読む。

## hash
- 3cab5ef887935a66c53bb4a5be54300c00e4f790b0353a568f334fd9253c94b1

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
