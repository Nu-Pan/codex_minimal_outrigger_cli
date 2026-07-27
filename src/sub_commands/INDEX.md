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
- oracle 系サブコマンドの実装をまとめるパッケージ。edit・investigation・review の CLI 入口と、review の対象列挙、パス解決、ループ処理、レポート生成、INDEX 変更の統合処理への入口を提供する。

## Read this when
- oracle サブコマンドの構成、CLI 入口、または各サブコマンドの実行経路を確認するとき。
- oracle review の対象列挙、パス解決、レビュー制御、レポート、INDEX 変更統合の実装先を特定するとき。

## Do not read this when
- 個別サブコマンドの詳細実装を確認する場合は、該当する実装ファイルを直接読む。
- 共通 TUI 起動処理や oracle 文書の仕様を確認する場合は、それぞれの対応する実装・oracle 文書を直接読む。

## hash
- da285b5b1b980ccb2f75a83a8b07ea646691dbf624f8e45eaaadd76167a9da0a

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口。apply と refactor の workload、および各 fork 実行フローへの入口を扱う。

## Read this when
- realization workload サブコマンドの構成や入口を確認するとき。
- realization apply の workload、fork 実行制御、agent 実行、差分検証、commit・rollback、run 状態、report 保存を調査・変更するとき。
- realization refactor の fork 実行フロー、対象選択、state 遷移、commit、未解決所見、cleanup、完了判定、report 出力を調査・変更するとき。

## Do not read this when
- realization workload に関係しない処理を確認するとき。
- 共通の editing run lifecycle、process tracking、report 生成、対象選択、state 同期だけを調査するとき。
- apply agent の prompt 構築、通常の realization apply、単一ファイルの review・修正、変更概要生成だけを確認するとき。

## hash
- 96d040aaa9d23ba8140853f063c08ca8998a93713d66f07b18f392658447e6c7

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
- editing run の共通 lifecycle サブコマンドと互換 shim をまとめるパッケージ。abandon・join の実行フロー、共通 lifecycle/report 実装への入口、旧 import path の互換層を扱う。

## Read this when
- editing run の abandon、join、共通 lifecycle、report writer、cleanup、state 同期を調査・変更するとき。
- run サブコマンドから参照される lifecycle・report 関連モジュールの配置と入口を確認するとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。
- 特定サブコマンドや共通 runtime の具体的な実装詳細を確認する場合は、配下または commons 側の該当ファイルを直接読むとき。

## hash
- b9a071b2953bdcfa3c487bfe1c088b7865cd62d659fb05350fb3aad2767088b2

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
