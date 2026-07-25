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
- oracle 系サブコマンドをまとめる package。oracle の edit・investigation・review と、review の対象列挙、反復処理、パス解決、レポート生成、INDEX 統合を担う下位実装への入口。

## Read this when
- oracle 系サブコマンドの package 構成や、各サブコマンド・review 専用モジュールへの入口を確認するとき。
- oracle edit／investigation／review の実行経路、または review の対象管理・処理ループ・パス解決・レポート・INDEX 統合の担当箇所を探すとき。

## Do not read this when
- 個別サブコマンドの詳細実装を確認したい場合は、該当する下位モジュールを直接読む。
- Codex TUI や共通 CLI runtime の実装詳細を確認したい場合は、それらの実装先を直接読む。

## hash
- d411a552877e22fbc584498de86994f6591a36fbe07b9b10a87fee2c8d574b04

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口。apply workload と refactor workload の実装へのルーティングを提供する。
- apply workload は `cmoc realization apply fork` の実行ライフサイクル、agent 実行、差分検証、commit、状態遷移、report 保存、失敗時 rollback を扱う。
- refactor workload はリファクタリング関連 CLI の入口と、対象ファイルの調査・修正、差分検証、commit、所見管理、完了・中断・エラー処理、report 生成を扱う。

## Read this when
- realization workload サブコマンドの実装や構成を確認するとき。
- `cmoc realization apply fork` の実行フロー、状態遷移、agent 実行、差分検証、commit、report、rollback を調査・変更するとき。
- realization のリファクタリング機能や refactor fork のライフサイクル、調査・修正、完了判定、report 生成を調査・変更するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。
- apply workload や refactor workload の個別 agent、run 状態管理、差分取得、commit、INDEX 更新、report 生成など、より限定された共通処理だけを確認するとき。
- `cmoc realization apply fork` 以外のサブコマンドの CLI 本体だけを確認するとき。

## hash
- 4959038c5bf90e20e28f2c2c62228774dd99289c691b51ce23551377c93b1b17

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
- editing run サブコマンドの共通 lifecycle 処理をまとめるパッケージ入口。abandon・join の run lifecycle 実装と、旧 import path を維持する lifecycle/report 互換 shim への導線を提供する。

## Read this when
- editing run の共通 lifecycle や配下のサブコマンド実装を調査・変更するとき
- run の停止・統合・cleanup・state 同期・report 出力の処理を確認するとき
- 旧 import path の互換 shim や canonical helper への移行を確認するとき

## Do not read this when
- editing run 以外のサブコマンドを扱うとき
- 共通 helper の実装詳細や正本仕様を確認するときは、配下の該当ファイルまたは commons 側の実装・oracle doc を直接読む

## hash
- 6b46c14a1d9f3a78c4ace8ed4f06ed4150ca809512ab6b1528a7676940e9578f

# `session`

## Summary
- session サブコマンドの実装パッケージ。session 関連の各サブコマンド実装を確認する際の入口となる。
- session の abandon、fork、join における branch 操作、state 管理、事前条件検証、失敗時の復旧、結果表示を扱う。

## Read this when
- session サブコマンドの実装構成を確認・変更するとき
- session の abandon、fork、join の処理や相互の責務分担を調査するとき

## Do not read this when
- session 以外のサブコマンドを扱うとき
- session state の schema やライフサイクル仕様そのものを確認するとき
- Git 操作、CLI 共通基盤、conflict resolution の専用実装を直接調査するときは、それぞれの実装を直接読む

## hash
- 23efdccb94ae350083302d248278150d52c81e762e8bff022e8cf1edd7853d8a

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
