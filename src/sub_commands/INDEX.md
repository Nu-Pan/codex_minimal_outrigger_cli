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
- oracle 系サブコマンドの実装をまとめるパッケージ。編集・調査・レビューの各サブコマンドと、レビュー対象列挙、パス解決、結果報告、INDEX 差分統合などの下位実装への入口を提供する。

## Read this when
- oracle サブコマンド全体の構成や、個別実装・レビュー関連処理の入口を確認するとき。
- oracle edit、investigation、review の実行経路や、レビュー対象・パス・レポート・INDEX 統合の担当箇所を選ぶとき。

## Do not read this when
- 特定サブコマンドの詳細実装だけを確認したい場合は、該当する実装ファイルを直接読む。
- 共通の入力部品、TUI 起動パラメータ生成、Git 操作、レビュー判定、レポート生成の詳細だけを調査する場合は、対応する下位実装を直接読む。

## hash
- e5d49579d0eebf0a67acffe95ed980477a42ddc0bb1d2012bbb450ca32efc1b8

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口。apply と refactor の処理を束ね、各サブパッケージの実装へ進むための入口となる。

## Read this when
- realization workload サブコマンド全体の構成や、apply・refactor のどちらを調査すべきか確認するとき。
- realization apply または realization refactor の処理を調査・変更するとき。

## Do not read this when
- apply workload の詳細な実装や `cmoc realization apply fork` の実行処理だけを確認したいとき。
- refactor fork の実行フローだけを確認したいとき。
- run lifecycle、process tracking、report 出力などの共通処理だけを確認したいとき。

## hash
- 9339cd21879362b5f46cdf5073d0794a57afb8d37b6a2d3f075c545b24d6062e

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
- editing run の共通 lifecycle サブコマンドをまとめるパッケージ。run の開始後に行う abandon・join と、関連する lifecycle/report の互換 import path を扱う。配下の各実装・shimへ進むための入口。

## Read this when
- editing run の abandon または join の処理を調査・変更するとき
- editing run の lifecycle や report writer の旧 import path、共通実装との関係を確認するとき

## Do not read this when
- editing run 以外のサブコマンドを扱うとき
- 特定の run サブコマンドの詳細実装、共通 runtime、canonical な report writer を直接調査するときは、配下または共通実装の該当ファイルを読む

## hash
- 5d1d738900bd8f42793d64aa9151eca4d57ef58cdaa8e074f93aac9b04f349ce

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
