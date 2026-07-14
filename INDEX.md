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
- realization 側の公開 import 面と CLI 入口を束ねる実装ルート。`basic`、`config`、`oracle`、`cmoc_runtime.py` の互換 shim と、`commons`、`sub_commands`、`main.py` の実体を見分けて、どの責務へ進むかを切り分ける起点になる。
- 正本側定義を複製せずに再公開する領域と、実処理を持つ領域が同居するため、互換維持の判断は shim 群、CLI 挙動は `main.py`、共通基盤は `commons`、個別実行フローは `sub_commands` を読む前提で使う。

## Read this when
- realization 側の公開 import 経路や互換 shim の残存理由を確認したいとき。
- cmoc の CLI 入口、共通 runtime、個別サブコマンド実装のどれを読むべきか判断したいとき。
- 正本側の定義を参照しているだけの領域と、実装本体を持つ領域を切り分けたいとき。

## Do not read this when
- 個別 helper の入力・出力・失敗時挙動を知りたいときは、対応する下位モジュールを直接読む。
- oracle 側の正本仕様断片そのものを確認したいときは、この実装ルートではなく oracle 側を読む。
- 公開面や共通基盤ではなく、特定サブコマンドの業務ロジックだけを追いたいときは `sub_commands` 配下へ直接進む。

## hash
- df62cb647f33180a676ea2d0b2911102a3d4f987944d0a5edfa1a220c6f82635

# `test`

## Summary
- `test` 配下の回帰テスト群を、CLI・runtime・Codex 実行・indexing・review・apply・session・prompt・struct doc・共通テスト補助の関心別に案内する入口。各テストは個別の機能契約や境界条件を検証するため、まずこの階層で対象の責務を絞ってから該当ファイルへ進む。
- 共通補助は `_cli_support.py`、`_git_support.py`、`_codex_support.py`、`_command_support.py`、`_ollama_support.py`、`_apply_support.py`、`_acp_builder_support.py` に分かれており、テスト本文の重複を避けるための足場だけを置く。実装本体や正本仕様はここでは追わない。
- `acp.builder` 系の契約確認は `test_acp_builder_*` 群、`apply` / `session` / `review` / `indexing` / `codex` / `doctor` / `runtime` はそれぞれ対応するテスト群に分かれている。変更対象のサブコマンドや runtime 境界が分かっているなら、この階層から該当グループへ進む。

## Read this when
- テスト対象が CLI、runtime、Codex 実行、indexing、review、apply、session、prompt、StructDoc のどれかに当たり、まず読むべきテスト群を絞りたいとき。
- 共通テスト補助の責務や、どの補助がどの種類のテストを支えているかを確認したいとき。
- `acp.builder` の parameter 生成や正本 schema 参照に関わる回帰を追いたいとき。
- `apply` / `session` / `review` / `indexing` / `runtime` の境界条件や外部挙動を、個別テストの入口からたどりたいとき。

## Do not read this when
- 正本仕様そのものを確認したいときは、この階層ではなく対応する `oracle` 側の本文を読む。
- CLI や runtime の実装本体を追いたいときは、このテスト群ではなく対応する `src` 側を読む。
- 個別テストの細部ではなく、共通の routing 方針や上位の案内を確認したいときは、この階層ではなく上位の `INDEX.md` を読む。

## hash
- 4a52612d817e5d54f585eb42345fb0e1b8da2c0e09cb726000457a511bddc82b
