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
- oracle 系サブコマンドをまとめる package。oracle の編集・調査・レビューに関する CLI 実装と、それらを支える review 用の対象選定、ループ、パス、レポート、INDEX merge 処理への入口を提供する。

## Read this when
- oracle 系サブコマンドの構成や、各サブコマンド実装への入口を確認するとき。
- oracle review の lifecycle、対象選定、所見処理、レポート生成、INDEX 差分 merge の実装箇所を特定するとき。

## Do not read this when
- 特定の oracle サブコマンドの詳細な起動処理を確認する場合は、そのサブコマンド実装を直接読む。
- review の対象列挙、ループ、パス解決、レポート、INDEX 操作の個別仕様を確認する場合は、対応する実装ファイルを直接読む。
- oracle の正本仕様を確認する場合は、対応する oracle 文書を直接読む。

## hash
- d6eaa49c796a99bf83921c0827a42b43a0eae8cb1d6a595c2cb1491c29f5a39f

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口。apply と refactor の処理構成・CLI 実行フローを下位実装へ案内する。

## Read this when
- realization workload サブコマンドの構成や実装入口を確認するとき。
- realization apply または realization refactor の CLI 動作や処理フローを調査・変更するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。
- apply または refactor の具体的な処理詳細を確認する場合は、該当する下位パッケージを直接読むとき。

## hash
- 1a0b83f8736a7768a2d63071164a5f7a263e05689a37289ccf5904cf48024b8a

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
- session サブコマンドの実装パッケージ。session のライフサイクル操作に関する実装を確認する際の入口となる。
- session の abandon、fork、join を扱い、branch・state の作成、検証、更新、cleanup、失敗時のロールバックや merge conflict 解決を含む。

## Read this when
- session サブコマンドの実装構成やライフサイクル処理を確認・変更するとき。
- session branch と state の作成・更新・削除、cleanup、失敗時の復旧処理を調査するとき。
- session join の merge conflict 委譲、安全な差分制限、解決後の stage・commit 処理を確認・変更するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- session の共通 state データ構造、runtime、Git status 取得などの一般仕様だけを確認するときは、対応する共通実装・仕様を直接読む。
- conflict resolution 用 prompt の正本仕様や builder 実装そのものを確認するときは、対応する oracle または builder の対象を直接読む。

## hash
- 8a0dfef628903e21e7fae720cdfc2150168e3c41e5d0776d9d80ec9fd63a111d

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
