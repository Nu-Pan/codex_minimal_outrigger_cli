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
- oracle 系サブコマンドをまとめる package。oracle の edit、investigation、review と、review の対象列挙・loop・path 解決・report・INDEX merge を担う実装への入口。

## Read this when
- oracle 系サブコマンドの package 構成や入口を確認するとき。
- oracle edit、investigation、review の実行経路を調査・変更するとき。
- oracle review の対象列挙、評価 loop、path 解決、report、INDEX 差分 merge のいずれかを調査・変更するとき。

## Do not read this when
- 個別サブコマンドや review 機能の詳細だけを確認する場合は、該当する実装ファイルを直接読む。
- oracle の正本仕様を確認する場合は、対応する oracle 文書を直接読む。

## hash
- 69f4a777ca3159ddf6a0bacf46b478271aed4523b93bb7282cf7e1312594263e

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口。
- apply workload と refactor 処理の実装へ進むための階層入口であり、apply では実行ライフサイクルや差分・状態・report、refactor では fork 実行全体や完了判定・report 保存を扱う。

## Read this when
- realization workload サブコマンドの実装構成を確認するとき。
- realization apply workload の CLI 動作、run lifecycle、差分検査、commit、状態遷移、fork report を調査または変更するとき。
- realization refactor の fork 実行フロー、対象選択、差分・commit・INDEX 検証、所見管理、state 更新、report 生成を確認するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。
- apply agent の launch parameter、run 共通の join・abandon 処理、または realization apply の正本仕様だけを確認するとき。
- 個別 refactor agent の Structured Output や prompt builder、refactor state のデータ形式・対象選択ロジック、共通 lifecycle・report・process tracking・INDEX 更新の仕様だけを確認するとき。

## hash
- 6692789f64731f8e38015a17e85a88e921b58653e364c247ea4d541ce7f3e522

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
- session サブコマンドの実装パッケージ。session の各ライフサイクル処理を確認する入口で、開始・参加・中断などの個別サブコマンド実装を含む。

## Read this when
- session サブコマンドの実装構成や、fork・join・abandon の処理を確認・変更するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- session のデータ構造や共通 runtime、設定・仕様のみを確認するときは、対応する直接の実装・仕様ファイルを読む。

## hash
- ab4130d63f8a101c3dcea6098fe955537fe6e185866cf8cb9e83dd99578b8e4c

# `tui.py`

## Summary
- `cmoc tui` サブコマンドの実行入口と本体処理を定義する。インデックス事前処理、オリジナルプロンプトの編集入力、TUI 起動パラメータの構築、Codex TUI の起動を担当する。

## Read this when
- `cmoc tui` の実行フロー、プロンプト入力、TUI 起動処理を変更または調査するとき。
- TUI 起動時のリポジトリルート、作業ルート、設定値の受け渡しを確認するとき。

## Do not read this when
- TUI 起動パラメータの詳細仕様だけを確認したいときは、パラメータ構築側の実装や対応する仕様を直接読む。
- プロンプトエディタの入力・ignore 処理だけを変更または調査するときは、入力処理側の実装や対応する仕様を直接読む。

## hash
- aa6f03a8d2a0cd859192f29279ebe32b845bd7c380a0ce0620b2b1a54dd3483e
