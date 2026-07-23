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
- oracle 系サブコマンドをまとめる package。oracle edit・investigation・review の CLI 入口と、review の対象列挙、パス解決、反復処理、INDEX 更新、レポート生成を扱う。各サブコマンドの詳細実装や補助モジュールへ進むための入口。

## Read this when
- oracle 系サブコマンドの package 構成や CLI 入口を確認するとき
- oracle edit、investigation、review の実行フローを調査・変更するとき
- oracle review の対象選定、パス解決、所見処理、INDEX 更新、レポート生成の担当箇所を特定するとき

## Do not read this when
- 個別サブコマンドの詳細実装だけを確認したいときは、該当するモジュールを直接読む
- oracle 編集・調査の正本仕様や instruction template を確認したいときは、対応する oracle doc を直接読む
- 共通 CLI runtime、TUI 起動、git 状態検証などの共通処理だけを確認したいときは、各共通モジュールを直接読む

## hash
- b3890e0aa774a45c53815adb55a25a19e04175fce4238458bb2fc1d89356c18a

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口。apply workload と refactor workload の実装への導線を提供する。

## Read this when
- realization workload サブコマンドの構成や実装入口を確認するとき。
- realization apply または realization refactor の処理を調査・変更するとき。

## Do not read this when
- realization workload に関係しない処理を確認するとき。
- apply や refactor の個別実装・共通 lifecycle・report 仕様を直接確認したいとき。

## hash
- 776b7b9132eafb0359eff3dbb307ccb8cc262558f70b31a16c251e73d3ed9942

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
- session サブコマンドの実装パッケージ。session の各操作に関する CLI 実装を確認する際の入口であり、作成・参加・中止などの個別処理へ進むためのルーティング対象。

## Read this when
- session サブコマンドの実装構成や、個別操作の処理箇所を確認・変更するとき。
- session fork、join、abandon の挙動を調査するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- Git 操作、session state、conflict resolution などの共通実装だけを直接調査するときは、それぞれの共通実装を読む場合。

## hash
- 1115a3058aeb212b7934ed6f2f72871a880d524ed048f390c151452c09bf960c

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
