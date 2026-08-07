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

# `feedback`

## Summary
- feedback サブコマンドの実装をまとめるディレクトリ。入力 observation の処理、issue への統合、状態復旧、report 公開までの feedback report 処理を扱う。配下の各実装へ進むための入口。

## Read this when
- feedback サブコマンド全体の実行フローや責務分担を確認・変更するとき。
- feedback report における observation の正規化、issue 統合、checkpoint・receipt・state の復旧、表示内容の生成を調べるとき。
- feedback 関連の処理中断、部分失敗、再実行、corruption 検出の扱いを確認するとき。

## Do not read this when
- feedback observation の入力 schema、state record のデータモデル、共通 persistence API の詳細だけを調べるとき。
- normalization agent の parameter や Structured Output schema だけを調べるとき。
- feedback 以外のサブコマンド、または共通 CLI runtime・ログ・path・result validation だけを調べるとき。

## hash
- 89bcf4d5416cefb4ddd2a31d82471273bdc7caa5b425970f0df996d761fda786

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
- oracle 系サブコマンドの実装パッケージです。編集・調査・レビューの CLI ワークロードと、レビュー対象列挙、進捗ループ、パス解決、レポート生成、INDEX 差分の commit/merge を担う補助処理を含みます。oracle サブコマンド群の実装へ進む入口です。

## Read this when
- oracle 系サブコマンドの実装構成や、編集・調査・レビューの実行フローを確認するとき。
- oracle review の対象列挙、レビュー進捗、finding の処理、レポート生成、隔離 run の lifecycle を調べるとき。
- レビュー結果の oracle path 解決や INDEX 差分の commit・merge 処理を調査するとき。

## Do not read this when
- 特定サブコマンドの詳細だけを確認する場合は、対応する個別実装へ直接進んでください。
- TUI 起動パラメータ、共通入力エディタ、git 状態確認などの共通処理だけを調べる場合は、対応する共通モジュールへ直接進んでください。
- oracle review の正本仕様や編集プロンプトの内容を確認する場合は、参照されている oracle 文書へ進んでください。

## hash
- a410d8e4e8bdd436ce9dec0f620ec85133ada016bbaed55f1b44f7d7e6c13669

# `realization`

## Summary
- realization workload のサブコマンド群を束ねるパッケージ。workload の入口、apply、refactor の実行オーケストレーションと関連する状態遷移・差分検査・report 処理への入口を提供する。

## Read this when
- realization workload サブコマンド全体の構成や、apply・refactor の処理へ進む入口を確認するとき。
- realization apply または refactor の実行順序、状態管理、差分・commit 検証、report 処理を調査するとき。

## Do not read this when
- realization workload に関係しない CLI サブコマンドを扱うとき。
- apply agent 固有の prompt や、run lifecycle・process tracking・git 差分操作など共通処理の仕様だけを確認したいとき。

## hash
- be75104a33adab32d91f2931c63f6211a43bd71e0da0b23e82882e075df2372b

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
- editing run の abandon・join など、実行ライフサイクルに関する CLI サブコマンドと共通互換 shim をまとめた領域。run の停止・統合・レポート・ライフサイクル処理を調査する際の入口。

## Read this when
- editing run の作成後 lifecycle、abandon、join、cleanup、状態遷移、レポート生成を調査・変更するとき。
- run サブコマンド間で共有される lifecycle helper や旧 import path の互換性を確認するとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。
- 特定の run サブコマンドの詳細実装や canonical な共通 runtime/report 実装だけを確認したいときは、配下または commons 側の該当ファイルを直接読む。

## hash
- 8013fa5a8c188e86f32a2d4238e189a3214e25d6b28cc5dfa392076666666a43

# `session`

## Summary
- session サブコマンドの実装パッケージ。session の各ライフサイクル処理を確認する際の入口となる。
- session の abandon、fork、join における branch 操作、state 更新、競合解消、失敗時の復旧を扱う。

## Read this when
- session サブコマンドの実装や構成を確認・変更するとき。
- session の作成、離脱、統合、branch・state のライフサイクルを調査するとき。
- session join の merge conflict 解消や検証処理を確認するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- session の共通 state データ構造、runtime Git 処理、Codex 実行規則だけを確認したいときは、それぞれの共通実装や定義を直接読む。

## hash
- 8a0dfef628903e21e7fae720cdfc2150168e3c41e5d0776d9d80ec9fd63a111d

# `tui.py`

## Summary
- 対象は `cmoc tui` の CLI 実行入口です。インデックスからは、TUI 起動フローやプロンプト編集入力、起動パラメータの組み立てを調べる必要がある場合に進みます。

## Read this when
- `cmoc tui` サブコマンドの実行開始処理を確認するとき
- オリジナルプロンプトの編集から Codex TUI 起動までの連携を追うとき
- TUI 起動時の固定設定や現在のリポジトリ・作業ルートの受け渡しを確認するとき

## Do not read this when
- TUI 起動パラメータの詳細仕様だけを確認したいときは、パラメータ生成元の実装または TUI サブコマンド仕様を直接読む
- プロンプト編集入力の仕様だけを確認したいときは、入力収集処理の実装または対応する仕様書を直接読む
- CLI 共通の実行ラッパーや設定ロードの挙動だけを確認したいときは、それぞれの共通実装を直接読む

## hash
- 50927cde072036223c209ad43e0f4a9fc55ac3c827fdb77489488047831d25f5
