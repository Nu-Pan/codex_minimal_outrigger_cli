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
- oracle 系サブコマンドの実装をまとめるパッケージ。編集・調査・レビューの CLI 起動処理、レビュー対象選定、レビュー実行ループ、パス解決、レポート生成、INDEX 差分の統合までの入口を提供する。各個別実装を確認する際の起点。

## Read this when
- oracle 系サブコマンドの構成や、目的のサブコマンド実装への入口を確認するとき。
- oracle review の対象選定、実行ライフサイクル、INDEX 差分統合、パス解決、レポート生成の責務分担を調べるとき。

## Do not read this when
- 特定サブコマンドの内部処理や prompt・TUI パラメータの詳細だけを確認するときは、該当する個別実装または import 先を直接読む。
- oracle の正本仕様や編集・レビュー契約を確認するときは、対応する oracle 文書を直接読む。

## hash
- 772c8d6f32c26d8eb74fe9db0f9343e0264ba2a8b1e3072e552816d10ddc0c74

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
- `cmoc tui` サブコマンドの実行入口と本体処理を担う。プロンプト編集用入力を準備・収集・確定し、固定パラメータで Codex TUI を起動する。

## Read this when
- `cmoc tui` の起動フロー、プロンプト編集、Codex TUI 起動処理を変更または調査するとき。
- TUI 実行前の indexing preflight、ログ前チェック、サブコマンド進捗管理の連携を確認するとき。

## Do not read this when
- TUI 起動パラメータの構築仕様だけを確認する場合は、パラメータ builder の実装を直接読む。
- プロンプト入力・保存・確定の詳細仕様だけを確認する場合は、prompt editor input 関連の実装または参照された正本仕様を直接読む。
- Codex TUI 自体の実行実装や共通 CLI ランタイムの挙動だけを確認する場合は、各ランタイム実装を直接読む。

## hash
- c544eb81e5f42cc514f3b4ffc390709325ed6cdb0cdd79ec833f4beff51e1ffa
