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
- `oracle` 配下の正本仕様断片を読むための入口。`doc` で利用者向け仕様のまとまりを、`src` で ACP builder 周辺の実装・共通基盤・prompt 構成のまとまりを、それぞれどこから読むべきか判断するときに使う。
- 個別本文の代替ではなく、責務境界で読む先を絞る案内として位置づける。

## Read this when
- `cmoc` の CLI 挙動、サブコマンド、起動前処理、ログ、状態管理、補完、インデクシング、外部 model 連携のどの仕様断片へ進むべきか判断したいとき。
- 起動前の共通処理、エラー処理、run/session の隔離や状態更新、プロンプト受け渡しなど、複数機能にまたがる仕様の入口を探したいとき。
- 正本仕様断片の中で、利用者向け仕様と ACP builder 周辺の実装・基盤・prompt 構成を責務で切り分けて読みたいとき。

## Do not read this when
- oracle file と realization file の一般的な役割分担や編集規則だけを確認したいとき。
- 個別仕様がすでに分かっていて、その本文だけで判断できるとき。
- `cmoc` 以外の一般的な CLI 設計や、この配下に属さない別機能の仕様を探しているとき。

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
- `src` は cmoc の realization 実装全体の入口で、CLI 入口、共通 runtime、互換 shim、`acp` 系 builder 群、公開互換の `basic` / `config` / `oracle` 受け口をまとめて案内する階層。
- ここを読むと、旧 import 互換をどこで受け止めているか、CLI の配線がどこにあるか、共有基盤と各サブコマンド実装、そして oracle 側 builder へつながる具体的な実装群のどこへ進むべきかを切り分けられる。
- 新しい実装の本体や互換入口を探す起点には向くが、個別機能の詳細や正本仕様そのものを読む場所ではない。

## Read this when
- cmoc の realization 実装で、どの下位 module がどの責務を持つかをまず切り分けたいとき。
- `main.py` から各 subcommand へどう配線されるか、または `commons` / `sub_commands` / `acp` / `basic` / `config` / `oracle` のどこを読むべきか判断したいとき。
- 旧来の import 経路や互換 shim を維持・削除判断したいときに、その受け口が `src` 配下のどこにあるか確認したいとき。

## Do not read this when
- acp builder の正本仕様、prompt、生成内容、人間意図を確認したいときは oracle 側の builder を読む。
- 個別の CLI 挙動やサブコマンド実装の細部だけを調べたいときは、`sub_commands` や各下位 module を直接読む。
- 設定や path model、共通 runtime helper の詳細だけが目的なら、`commons` や対応する専用 module を直接読む。

## hash
- 48e33f5d891e74b3aa1d1a77111ad10586bcf6502412e2e3b40dcfd514625fd2

# `test`

## Summary
- cmoc の realization test 群をまとめる入口。CLI、runtime、prompt、indexing、session、doctor、review、apply などの外部挙動回帰を、関心領域ごとの個別テストへ振り分けるために読む。
- 共通 fixture や test 支援モジュールに触れる前に、まずどの挙動を固定したいかを決めるための案内点として使う。

## Read this when
- 実装変更の影響を受ける外部挙動を、どのテストから確認すべきか探したいとき。
- CLI 起動前処理、Codex runtime、prompt 組み立て、index 更新、session/doctor/review/apply のいずれかに関する回帰テストを探したいとき。
- 共有 fixture やテスト支援コードではなく、対象機能の境界と期待挙動をまず把握したいとき。

## Do not read this when
- 個別機能の期待値や失敗条件を確認したいだけなら、対応する個別テスト本文を直接読む。
- テスト支援関数、fixture、git repo 作成 helper の実装を追いたいなら、支援モジュール側を直接読む。
- oracle file の正本仕様や実装本体を確認したいなら、それぞれの oracle 側・src 側を直接読む。

## hash
- 52c2455a36118f65f2f9a7299008300e3d4fcfbd4a3ee14d039392bfd4aa682f
