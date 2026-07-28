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
- oracle 系サブコマンドの実装をまとめるディレクトリ。編集・調査・レビューなどの個別サブコマンド実装への入口として機能する。

## Read this when
- oracle サブコマンド群の構成や、個別サブコマンド実装の所在を確認するとき
- oracle edit、investigation、review などの CLI 実行フローを調査するとき

## Do not read this when
- 特定サブコマンドの内部処理を詳しく確認するとき。対応する個別実装ファイルを直接読む
- TUI 起動パラメータ、レビュー判定、パス解決、レポート生成などの専用処理を調査するとき。対応する下位実装を直接読む

## hash
- b3f0861f35f4c3ea047e8e426c7f8d32f26e868b85796e0e54e6340baa892778

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口。apply workload と refactor workload の構成・実行フローを確認するための入口となる。

## Read this when
- realization workload サブコマンド全体の構成や、apply・refactor の実行フローを確認するとき。
- 対象選択、agent 実行、差分検証、状態更新、commit・rollback、report 保存などの workload 処理を調査・変更するとき。

## Do not read this when
- apply workload の prompt 構築や agent parameter の詳細だけを確認したいとき。
- refactor agent の入力 parameter や所見形式、change summary の Structured Output だけを確認したいとき。
- run の共通ライフサイクル、プロセス追跡、git 差分操作、report 出力の共通実装だけを確認したいとき。

## hash
- 8bf38c6a5f18d87b0b236b427f563c1eede0d3ac8f2b3b46146b614f5c1c479a

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
- editing run の共通 lifecycle サブコマンドと関連する互換 shim をまとめるパッケージ。run の abandon、join、共通 lifecycle、report writer の実装・参照先を確認する入口。

## Read this when
- editing run の開始後の停止・結合・cleanup・report 生成など、共通 lifecycle を調査・変更するとき。
- `cmoc run abandon` または `cmoc run join` の挙動を調査・変更するとき。
- 旧 import path の lifecycle helper や report writer の互換性を確認するとき。

## Do not read this when
- run lifecycle と無関係なサブコマンドや workload 固有の処理だけを変更するとき。
- canonical な共通 lifecycle・report 実装の詳細を確認するときは、再公開用 shim ではなく実体の実装を直接読む。

## hash
- f4ba538dabe3e83253590ef039e09d10c3d60527cddd26fb0d8931507b9f2f7a

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
