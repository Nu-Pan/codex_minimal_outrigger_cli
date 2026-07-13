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
- `src` は realization implementation の公開入口で、CLI 本体・共通 runtime・互換 shim・サブコマンド実装の配置を見分けるために読む。正本仕様ではなく、既存の公開 import 面や起動経路をどこへ接続するかを判断する案内層として扱う。
- `acp` と `basic` は既存の import 経路を壊さずに正本側へつなぐ互換層なので、互換維持の要否や削除条件を確認したいときに読む。実装本体や新機能の定義場所としては使わない。
- `commons` は cmoc の実行時共通基盤の集約点で、設定・状態・ログ・path・Git・エラー処理・Codex 起動・共通結果型のような共有 helper を探すときに読む。個別 command の業務ロジックはここでは追わない。
- `config` と `oracle.py` は、それぞれ設定実装と oracle package の互換 import を受け止める入口なので、正本側定義への再公開や import 解決の仕組みを確認したいときに読む。
- `main.py` は Typer ベースの CLI 入口で、root command、subcommand 接続、引数解析エラー変換、completion 時の挙動を確認したいときに読む。
- `sub_commands` は各サブコマンド実装へのルーティング層で、どのコマンドがどの下位実装に対応するかを素早く特定したいときに読む。個別処理の詳細は下位 module を読む。

## Read this when
- `src` 配下で、どの領域が互換入口でどの領域が実装本体かを切り分けたいとき。
- `acp.*`、`basic.*`、`config.*`、`oracle.*` の既存参照を、壊さずに正本側または実体 module へ接続する変更をするとき。
- CLI 入口、共通 runtime、サブコマンドの責務境界を先に絞ってから、読むべき実装ファイルを選びたいとき。

## Do not read this when
- 実処理、生成ロジック、設定値の意味、状態管理の詳細を直接追いたいときは、この階層ではなく該当 module を読む。
- 新しい公開面や機能を追加する実装場所を探しているときは、互換層やルーティング層ではなく担当実装へ進む。
- すでに互換参照の削除が終わっていて、入口の維持要否を確認する必要がないとき。

## hash
- 8eb3b35e67a387e1ae4e152f722e0d0654414f54b0567e24b67239b4e466f6a6

# `test`

## Summary
- `test` 配下の共通サポートと回帰テストを束ねる入口です。`_*.py` は各種テストで再利用する補助だけを置き、個別の仕様や CLI 挙動は対応する `test_*.py` か oracle 側へ進むために使います。
- `test_*.py` は `acp_builder`、CLI、runtime、prompt、review、session、indexing などの外部挙動をそれぞれ固定する回帰群です。変更対象の機能に応じて、該当するサブコマンド名や runtime 名を含むものを読むのが入口です。

## Read this when
- `test` 配下で共通化された補助処理の責務や使い分けを確認したいとき。
- 特定サブコマンドの外部挙動や回帰条件を確認したいときに、対応する `test_*.py` を探したいとき。
- `oracle` 側の正本仕様断片に対応する realization test の入口を絞り込みたいとき。

## Do not read this when
- 個別機能の正本仕様そのものを確認したいときは、対応する `oracle` 側を読む。
- `test` 全体のルーティング方針や上位の案内を確認したいときは、ここではなく上位階層の案内を読む。
- テスト以外の実装本体や CLI ロジックを追いたいときは、各 `src` 側を読む。

## hash
- 5da52754ed7a23a0a9268e35ebbe8127611db143f9b7f1552c34875b01fbb82d
