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
- oracle 系サブコマンドをまとめる package。oracle edit、investigation、review の各サブコマンド実装と、review の対象列挙・パス解決・処理ループ・差分マージ・レポート生成を下位要素として提供する。

## Read this when
- oracle 系サブコマンドの package 構成や入口を確認するとき。
- oracle edit、oracle investigation、oracle review の実行フローや責務の入口を確認するとき。
- oracle review の対象列挙、パス解決、所見処理、INDEX.md のマージ、レポート生成を調査するとき。

## Do not read this when
- 個別サブコマンドの詳細実装だけを確認したいときは、該当する下位ファイルを直接読む。
- 調査指示テンプレートや正本仕様を確認したいときは、対応する oracle doc を直接読む。
- 共通 CLI runtime、TUI 起動、prompt 入力などの共通処理だけを確認したいときは、各共通モジュールを直接読む。

## hash
- 22b1cf882ab987ae56c677503357e4b5c934306ea35ba843b1f33085b526852d

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口と、apply・refactor の実行フローを案内するディレクトリ。サブコマンド全体の構成確認から、各下位パッケージの処理調査へ進む入口となる。

## Read this when
- realization workload サブコマンドの構成や実行フローを確認するとき。
- apply または refactor の realization 処理を調査・変更するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。
- apply fork の launch parameter、共通の run lifecycle・state・report 処理、file 単位の prompt や findings schemaだけを確認するときは、より直接の対象を読む。

## hash
- 54409f3f86561274aa137f7e5e35b2da2bc65cfc74512bcc3d5c440b6016dc60

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
- editing run の共通 lifecycle サブコマンドと基盤処理をまとめるパッケージ。abandon・join の実行、共通 lifecycle、レポート生成を確認する入口。

## Read this when
- editing run の開始・join・abandon、run worktree／branch の管理、state 更新、差分処理、cleanup、lifecycle report の生成を調査・変更するとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。
- 特定の lifecycle 実装やレポート形式だけを確認する場合は、配下の該当ファイルを直接読む。
- run state の永続化、process tracking、一般的な runtime 処理だけを確認する場合は、対応する runtime モジュールを直接読む。

## hash
- f6e735f4a033dee57428c327662e4a8473bc648a18290afce5d338683025d5d2

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
- `cmoc tui` の CLI 実行経路を担当する実装。プロンプト入力、実行パラメータ解決、TUI 用 AgentCallParameter の構築、Codex TUI 起動までを統合する。TUI のパラメータ解決や起動処理の流れを確認・変更するときの入口。

## Read this when
- `cmoc tui` の実行フロー、プロンプト編集入力、解決済みパラメータからの TUI 起動パラメータ構築を確認するとき
- TUI で許可するファイルアクセスモードや、設定された oracle・realization standard の反映を変更するとき
- TUI 起動前後の CLI runtime、ログ、作業ルートの扱いを確認するとき

## Do not read this when
- TUI の低レベルな起動パラメータ生成だけを変更する場合は、TUI builder の実装を直接確認する
- TUI 用パラメータ解決のプロンプトや許可モード定義だけを変更する場合は、resolve parameter 側を直接確認する
- プロンプト編集そのものの入力処理だけを変更する場合は、prompt editor input 側を直接確認する

## hash
- bc6c3be08640a1000dcead34a380e970ba103be1b1fd792bea3cc1579a1db2d3
