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
- oracle 系サブコマンドをまとめる package。各サブコマンドの CLI 入口に加え、oracle review の対象列挙・パス解決・ループ・差分統合・レポート生成を下位モジュールへの入口として提供する。

## Read this when
- oracle 系サブコマンドの構成や package の入口を確認するとき。
- oracle review の実行フロー、対象選定、finding 処理、INDEX.md 統合、レポート生成の担当モジュールを特定するとき。

## Do not read this when
- 個別サブコマンドや review の詳細実装を調査するときは、該当する下位モジュールを直接読む。
- Codex TUI や共通 CLI runtime の詳細だけを調べるとき。

## hash
- 70c0eeb423abba2065aa653c708573da3c9cd047c868cf19621135805eac4b67

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口。apply と refactor の実行処理への導線を提供する。

## Read this when
- realization workload サブコマンドの実装や構成を確認するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。

## hash
- 36caddb4ff81b39a1fbd53dba51ab268ecaf247153f35f7753f78d4c8e33d8d6

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
- editing run の共通 lifecycle サブコマンドをまとめるパッケージ。run の開始・参加・放棄、共通 lifecycle 処理、merge・cleanup、report 保存を確認する入口。
- 個別コマンドの実装に加え、active run の解決、state 更新、Git 差分検査、worktree・branch 操作、INDEX.md conflict 処理、ライフサイクルレポート生成を扱う。

## Read this when
- editing run の開始・join・abandon の動作や、共通 lifecycle の変更・調査を行うとき
- run の state 遷移、worktree・branch・process tracking の cleanup、merge、rollback、report 保存を確認するとき
- run lifecycle と doctor preprocess、refactor state 同期、INDEX.md 更新の連携を確認するとき

## Do not read this when
- editing run 以外のサブコマンドを扱うとき
- state データ構造や永続化形式そのものを確認するときは runtime_state と対応する oracle を読む
- Git・path・INDEX 更新の低レベル utility、または report 保存先の規則だけを確認するときは各専用 module を直接読む

## hash
- 4fe0a4f49f2675ca3252c2e652da0c2b82bf2041f8e866d0f65cb428dafff9fd

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
