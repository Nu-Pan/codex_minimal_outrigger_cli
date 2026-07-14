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
- `src` は realization 側の実体コードの根で、`acp`、`basic`、`commons`、`config`、`sub_commands` などの公開 import 面と実装本体をまとめて受ける入口である。ここでは個別機能の仕様そのものではなく、どの下位領域へ進むべきかを切り分ける。
- `oracle.py` は正本側 `oracle` package へ到達するための import shim であり、`src` 起点の実行環境で正本仕様断片を参照する必要があるときだけ読む。
- `main.py` と `sub_commands` は CLI 入口と各サブコマンドの配線・実行入口なので、コマンド追加や実行フロー確認では先にここを読む。
- `basic`、`config`、`cmoc_runtime.py` は主に互換 import 面や runtime 共通基盤をまとめる領域で、正本定義の複製ではなく再公開・委譲の境界を確認するときに使う。

## Read this when
- `src` 配下でどの実体モジュールから読み始めるべきかを決めたいとき。
- `acp.*`、`basic.*`、`config.*`、`oracle.*` の互換 import 面と、その委譲先を確認したいとき。
- CLI 入口、サブコマンド登録、runtime 共通処理、設定系の公開面がどこにあるかを切り分けたいとき。
- 正本側の仕様断片を参照する必要があり、`src` 側の shim から到達経路を確認したいとき。

## Do not read this when
- 個別機能の処理内容、引数の詳細、エラー条件などの本文仕様を知りたいときは、対応する下位モジュールを直接読む。
- 正本仕様断片そのものを確認したいときは、`src` ではなく `oracle` 側を読む。
- 単にルーティング情報だけが欲しいときに、互換 shim の実装本体やサブコマンド内部まで追わない。
- 新しい正本仕様や新しい公開 API を追加する場所を探しているだけなら、まず該当領域の下位モジュールへ進む。

## hash
- 36ec313aab36ccee78d050ba749ed5ce6a61f56f9bb078674390b80ad1054314

# `test`

## Summary
- `test` 配下にあるテスト用の共通補助をまとめた案内です。`acp_builder` の正本 schema や各種 runtime/CLI の実装を直接読む前に、テストがどの共通 helper を使うか、またどの境界をこの層で支えるかを判断するときの入口になります。
- 個別の機能本体ではなく、`CliRunner`、git fixture、`CODEX_HOME` 初期化、fake 外部コマンド、Ollama 共有前提、path 解決、権限判定、preflight/ subprocess 補助など、複数テストで共通利用される支援対象を読むためのルーティングです。

## Read this when
- テストで共通に使う補助の責務や境界を確認したいとき。
- 同じ初期化や path 解決、権限判定、外部コマンド差し替えを複数テストで再利用したいとき。
- `acp_builder` の正本 schema 参照や、apply / session / codex / indexing / review / tui / doctor まわりのテスト補助を探しているとき。

## Do not read this when
- 個別サブコマンドの実装や正本仕様そのものを確認したいとき。
- テスト補助ではなく CLI 本体、runtime 本体、oracle 側の本文を見たいとき。
- 共通支援ではなく、特定テストケース固有の期待値だけを追いたいとき。

## hash
- d2948feabd6106855126765efa443b8048b94a9bac0a8a51914fc6975b3a8cb7
