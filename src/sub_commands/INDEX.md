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
- feedback サブコマンドの実装群を扱うディレクトリ。feedback の CLI 入口と、`cmoc feedback report` の中断可能な transaction、observation の normalization・issue 統合・Markdown report 生成を確認するための入口。

## Read this when
- feedback サブコマンドの挙動や実装を確認・変更するとき。
- `cmoc feedback report` の実行順序、checkpoint 復旧、state 整合性、issue 集計、report 生成を確認するとき。

## Do not read this when
- feedback 以外のサブコマンドを扱うとき。
- feedback observation の保存・列挙や issue state の共通 schema を直接確認したいときは、それぞれの専用実装へ進む。
- normalization agent の prompt や Structured Output schema だけを確認したいときは、対応する normalize issue parameter の実装へ進む。

## hash
- 453d36b046dcadee04cde82f6d9091b476fafb11fb90eb758996179d05acc747

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
- realization workload サブコマンドのパッケージ入口。apply と refactor の処理構成や実行フローを確認する際の起点となる。
- apply workload の入口と、realization apply fork における実行オーケストレーションを扱う下位要素へ進める。
- realization のリファクタリング処理、CLI 実行、refactor fork の実行フローを扱う下位要素へ進める。

## Read this when
- realization workload サブコマンドの実装や構成を確認するとき。
- realization apply workload または realization refactor の実行フロー、状態管理、差分・commit・cleanup・report 処理を調査・変更するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。
- apply agent 固有の prompt や差分適用規則だけを調べるとき。
- 共通の run lifecycle、process tracking、git 差分操作の一般仕様だけを調べるとき。
- 単一ファイルの refactor prompt や Structured Output 契約、正常完了時の変更概要生成だけを確認するとき。

## hash
- 07915510e6a8f6c0ead70596b6950aee914463aa3f7e95e7f55738f1c9b236a3

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
- `cmoc tui` サブコマンドの実行入口と本体処理を定義する。インデックス事前処理、オリジナルプロンプトの編集入力、TUI 起動パラメータの構築、Codex TUI の起動を担当する。

## Read this when
- `cmoc tui` の実行フロー、プロンプト入力、TUI 起動処理を変更または調査するとき。
- TUI 起動時のリポジトリルート、作業ルート、設定値の受け渡しを確認するとき。

## Do not read this when
- TUI 起動パラメータの詳細仕様だけを確認したいときは、パラメータ構築側の実装や対応する仕様を直接読む。
- プロンプトエディタの入力・ignore 処理だけを変更または調査するときは、入力処理側の実装や対応する仕様を直接読む。

## hash
- aa6f03a8d2a0cd859192f29279ebe32b845bd7c380a0ce0620b2b1a54dd3483e
