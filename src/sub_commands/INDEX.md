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
- oracle 系サブコマンドの実装をまとめる package。oracle edit・investigation・review の CLI 入口と、review に関する対象列挙、パス解決、ループ、INDEX 差分統合、レポート生成の各処理への入口を提供する。

## Read this when
- oracle サブコマンドの実装構成や、各サブコマンド・review 関連処理の入口を確認するとき
- oracle edit・investigation・review の実行フローや責務分担を調査するとき
- oracle review の対象列挙、パス解決、ループ、INDEX 統合、レポート生成の実装を調査するとき

## Do not read this when
- 個別サブコマンドの詳細実装だけを確認したいときは、該当するサブコマンド実装を直接読む
- oracle review の対象列挙、パス解決、処理ループ、INDEX 統合、レポート生成の詳細だけを確認したいときは、該当するモジュールを直接読む

## hash
- cff9bffee2a0446ce2e577968d8ac346978415b89cd353520fa01b25b940c960

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口。
- realization の apply 処理と refactor 処理を扱う下位モジュール群への入口。
- apply では `cmoc realization apply fork` の差分適用、agent 実行、検査、状態更新、report 保存までを扱う。
- refactor では fork の target 処理、調査・修正、unresolved 管理、完了検証、cleanup、summary/report 生成を扱う。

## Read this when
- realization workload サブコマンドの実装や構成を確認するとき。
- realization apply fork の実行フロー、失敗時処理、差分検証を調査・変更するとき。
- realization refactor fork のライフサイクル、target 処理、unresolved finding、完了判定を調査・変更するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。
- apply workload 以外の処理だけを扱うときは apply の下位モジュールへ直接進む。
- refactor の target 選択、state 同期、prompt 構築、共通 lifecycle・report・process tracking だけを扱うときは対応する専用実装へ直接進む。

## hash
- 5ec95214d78237dabc07f53dd3c97f4a1237218c4a2772d8a3090177aca2d3e9

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
- editing run の共通 lifecycle サブコマンドをまとめるパッケージの入口。abandon・join・lifecycle・report の各実装へ進む起点となる。

## Read this when
- editing run の共通 lifecycle、開始・状態遷移・cleanup、run report、または配下実装の責務を調査・変更するとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。特定処理の詳細を確認する場合は、配下の該当ファイルを直接読む。

## hash
- e259c3c33b8292f555320e71ac084412b88736a4fb8bd10a075d3b49880e3b0a

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
