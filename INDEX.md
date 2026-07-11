# `LICENSE`

## Summary
- ソフトウェアの利用・複製・変更・配布・再許諾・販売を許可し、著作権表示と許諾表示の同梱条件、無保証および責任制限を定めるライセンス本文。

## Read this when
- 配布物に含めるべき著作権表示・許諾表示・免責条項を確認したいとき。
- 利用、改変、再配布、販売、再許諾が許される範囲を確認したいとき。
- ライセンス条件や保証・責任制限に関する質問へ答える必要があるとき。

## Do not read this when
- CLI の機能仕様、実装構造、テスト方針を調べたいとき。
- リポジトリ内の作業対象ファイルを探すためのルーティング情報が必要なとき。
- 開発手順、依存関係、コマンド実行方法を確認したいとき。

## hash
- a894f2547af0349f234986eb4661f0146f37b7d82f8b22a27a674d5c1236f08f

# `README.md`

## Summary
- cmoc の概要、初期セットアップ手順、基本ワークフローの参照先、ターミナル操作上の注意を案内する入口文書。
- 開発を始める前に、cmoc が何を補助するツールか、環境をどう用意するか、利用手順をどこから読むかを把握するための導入情報を扱う。

## Read this when
- cmoc の目的や略称を最初に確認したいとき。
- clone 後の Python 仮想環境作成や editable install など、初期セットアップ手順を確認したいとき。
- 基本ワークフローの詳しい仕様を読むための入口を探しているとき。
- ターミナルで Ctrl+S による停止を避けるための設定例を確認したいとき。

## Do not read this when
- 実装やテストの詳細、内部構造、仕様断片そのものを確認したいとき。
- コマンドの具体的な利用仕様や基本ワークフロー本文を確認したいとき。
- リポジトリ内での agent 向け作業規則や編集規則を確認したいとき。

## hash
- c6c3f3c5798ecc63f8611a40982f7bc8100116d8a934616bbd2b2a5b5e0a1afc

# `bin`

## Summary
- cmoc 起動用の薄いシェルラッパーを扱うディレクトリ。リポジトリルート基準で仮想環境 Python を探し、通常起動や補完プローブを Python 実装へ委譲する入口を担う。
- 仮想環境 Python が存在しない、または実行できない場合の利用者向け Markdown エラー、セットアップ手順、簡易 call stack の表示挙動を扱う。

## Read this when
- cmoc コマンド起動時に、どの Python 実装へ委譲されるかを確認したいとき。
- 仮想環境 Python がない場合、または実行不能な場合の起動失敗挙動を確認・変更したいとき。
- シェル補完プローブ時に通常起動と異なる分岐を取る理由や、補完時の失敗コードを確認したいとき。
- 起動前に利用者へ表示されるエラー文面、セットアップ手順、表示用パス、call stack 行番号の組み立てを確認・変更したいとき。

## Do not read this when
- Python 側の CLI サブコマンド、引数解析、業務ロジック、実行後の出力内容を調べたいとき。
- 仮想環境の作成方法そのものやパッケージ設定を変更したいとき。
- oracle file や path model の正本仕様を確認したいとき。

## hash
- bcc444f615624a979df5ebba33008d88c68e9f32a99b58386f9f0158f7e98b02

# `codex_minimal_outrigger_cli.code-workspace`

## Summary
- VS Code workspace configuration for this repository, defining the workspace root, editor exclusions, Python formatting/interpreter settings, analysis search paths, and Markdown indentation behavior.

## Read this when
- Configuring or troubleshooting VS Code behavior for this workspace, including hidden files, Python formatter selection, virtualenv interpreter path, analysis include paths, or Markdown editor indentation.
- Checking how the editor is expected to discover both implementation code and oracle source during Python analysis.

## Do not read this when
- Investigating cmoc runtime behavior, CLI command semantics, tests, or oracle specifications; read the relevant source, test, or oracle document instead.
- Looking for repository routing guidance; use the appropriate directory routing document rather than editor workspace settings.

## hash
- 1938307f70f255710d75d39c07d860ecb381acbb031ca19b2f2b6e565ac41acb

# `oracle`

## Summary
- `oracle` は cmoc の正本仕様断片を集める最上位の入口で、まずこの配下に人間が責任を持つ仕様を置き、実装やテストの前に読むべき領域を切り分けるときに使う。
- 配下の `doc` は実行仕様の横断把握、`src` は builder 系などの正本仕様断片の確認に進む入口で、どちらを読むべきかを先に判断するための案内役になる。

## Read this when
- cmoc の正本仕様断片をどの配下から読むべきか判断したいとき。
- oracle 側の仕様を起点に、実装へ進む前の読む範囲を絞りたいとき。
- 配下の `doc` と `src` のどちらを先に読むべきか迷うときの入口として使うとき。

## Do not read this when
- すでに読むべき下位領域が分かっているなら、この入口を経由せず直接その配下を読む。
- oracle と realization の役割分担や編集規則だけを確認したいとき。
- この配下以外の仕様や実装を調べたいとき。

## hash
- 2b279bab62fb859f5577120fce645f80fe2cd1bb02b932e9210997ece7afd976

# `pyproject.toml`

## Summary
- Python パッケージとしての cmoc のプロジェクトメタデータ、実行コマンド、依存関係、ビルド設定、setuptools の探索範囲、pytest の import path を定義する設定ファイル。
- CLI エントリーポイントは `cmoc` コマンドから実装の `main` 関数へ接続され、実装コードと oracle src の両方をパッケージ探索・テスト import の対象にする。

## Read this when
- Python バージョン要件、配布パッケージ名、依存パッケージ、ビルド backend など、プロジェクト全体の packaging 設定を確認・変更したいとき。
- `cmoc` コマンドがどのモジュール関数へ接続されるかを確認・変更したいとき。
- setuptools がどのディレクトリからモジュールやパッケージを収集するか、また JSON などの package data が含まれるかを確認したいとき。
- pytest 実行時の import path を確認し、実装コードや oracle src の import 解決に関する問題を調べたいとき。

## Do not read this when
- 個別サブコマンドの処理内容、CLI 入出力仕様、実行時ワークフローの実装詳細を調べたいとき。
- テストケース自体の期待値や fixture の内容を確認したいとき。
- oracle file の正本仕様断片の本文を確認したいとき。
- リポジトリ内の各ディレクトリやファイルへ進むためのルーティング情報を探しているとき。

## hash
- d01948ab1730e2747d529d49d8c8ca10b84bd6a86e19d7b2810ee87c95ccb904

# `src`

## Summary
- `src` 配下の realization 実装をまとめて読むための入口。CLI 本体や共通基盤の薄い再公開ではなく、実際の挙動を担う実装側の module を辿るときに使う。
- この階層は、`basic`・`commons`・`config`・`sub_commands` のような公開面や入口から、実処理の実体へ進みたいときに読む。互換 shim や正本側の定義そのものを探す用途には向かない。
- `oracle.py` は正本側 `oracle` package を起動時に解決するための shim だが、`src` 全体の案内としては、そこから先の実体実装を追う必要があるときに読む。

## Read this when
- CLI の実処理本体、共通 runtime、状態管理、path や git の扱いなど、入口の先にある realization implementation を確認したいとき。
- `basic`・`commons`・`config`・`sub_commands` などの公開面から、実体 module へどうつながるかを辿りたいとき。
- `oracle` package の解決 shim を起点に、正本側 module を参照する経路を確認したいとき。

## Do not read this when
- 互換 import の維持可否や旧公開名の扱いだけを確認したいときは、より直接の互換層を読む。
- 正本仕様断片や oracle file の文面を確認したいときは、`oracle` ツリー側を読む。
- CLI の登録、サブコマンドの接続、設定や共通 helper の入口だけを確認したいときは、それぞれの下位ディレクトリへ直接進む。

## hash
- adc4c1e47fdb45a4b0c972a3b84964ba50dfc4148d1ce2f5e1ec88ae9a86ca93

# `test`

## Summary
- テスト群の入口。共有テスト補助と各機能の回帰テストが集まっており、CLI 振る舞い・実行時契約・prompt 生成・状態遷移・Markdown レンダリングのどれを追うかで、読む先を切り分けるための案内に使う。
- 共通補助は、外部コマンドの差し替え、git/worktree の最小 fixture、Codex 実行環境の固定、Ollama の隔離、CLI 実行支援など、複数テストで再利用される前提準備をまとめる。
- 個別テストは、apply/session/indexing/review/doctor/tui/Codex runtime/prompt parts/StructDoc rendering などの外部挙動を確認する回帰検証であり、実装本体ではなく仕様上意味のある境界を固定する。

## Read this when
- 共通 fixture やテスト支援の使い分けを確認したいとき。
- CLI の外部挙動、状態ファイル遷移、worktree との整合、Codex 起動前後の前提条件、prompt 生成、Markdown レンダリングのどれかを変更したとき。
- 特定機能の回帰テストを探していて、まずどのテスト群を見るべきかを判断したいとき。

## Do not read this when
- 実装本体のアルゴリズムや内部 helper の分割だけを知りたいときは、対応する実装側を読む。
- 仕様の正本や設計意図そのものを確認したいときは、テストではなく oracle 側の文書や定義を読む。
- テスト支援ではなく CLI 定義、設定定義、runtime 実装、prompt 正本を探しているときは、この領域ではなく該当する実装領域を読む。

## hash
- 130b0fb829fc41e8b27071105befd01f3658b5369a7f01027ca1f29bff98b2cd
