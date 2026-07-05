# `AGENTS.md`

## Summary
- cmoc リポジトリ全体で従う開発時の基本ルールを定める文書。パス表記、INDEX.md を使ったルーティング、閲覧・編集禁止対象、oracle と実装・テストの配置方針を確認する入口になる。

## Read this when
- このリポジトリで作業を始める前に、全体の作業規則や禁止対象を確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` などのパス表記の扱いを確認したいとき。
- oracle、実装、テストをどの領域に置くべきか、またどの領域を編集してはいけないかを確認したいとき。
- INDEX.md を使って読むべきファイルを探す作業手順を確認したいとき。

## Do not read this when
- 個別機能の正本仕様断片を確認したいだけなら、oracle 配下の該当文書へ進めばよい。
- 実装コードや自動テストの具体的な構造を確認したいだけなら、対象領域のルーティング情報から該当ファイルへ進めばよい。
- 禁止対象やリポジトリ全体の作業規則をすでに把握しており、特定ファイルの内容確認だけが目的のとき。

## hash
- be280f67baf8ea9e564641d6ae7327aff20fd9575bc114fa291f3c5de87833ac

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
- cmoc の正本仕様断片を置く領域で、自然言語の oracle doc と、AI エージェント呼び出しや共通基盤を定義する oracle src への入口になる。
- 利用者向け仕様、branch/worktree モデル、設計判断、開発作法は自然言語文書へ、prompt・Structured Output schema・モデル設定・パスモデル・共通規範プロンプトなどの正本実装断片は oracle src へ進む。

## Read this when
- cmoc の実装・テスト・レビューで、正本仕様断片の所在を oracle doc と oracle src から切り分けたいとき。
- CLI 挙動、共通処理、外部連携、状態、ログ、実行環境、branch/worktree モデル、開発作法、テスト方針に関する自然言語仕様を探したいとき。
- AI agent call の prompt、Structured Output schema、モデル設定、ファイルアクセス権限、preflight 設定、共通データ構造、規範プロンプトの正本実装断片を確認したいとき。

## Do not read this when
- realization code の現在の実装場所、関数シグネチャ、内部ロジック、テスト期待値だけを直接調べたいとき。
- oracle file と realization file の一般的な定義、編集責務、品質基準、INDEX.md エントリー作成規則だけを確認したいとき。
- path placeholder、work root、repo root、run root などの語彙定義そのものだけを確認したいとき。

## hash
- 3a7fbaba0658d335217373593cc427bb065d2478cace0551d056a64cc41b534c

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
- cmoc の realization implementation 全体への入口。最上位 CLI、サブコマンド実行本体、runtime 共通 helper、oracle 正本実装への package shim、旧公開 import 経路を維持する互換層を束ねる。
- この領域は、利用者向け command から共通 runtime、状態・git・path・logging・Codex 実行境界、INDEX maintenance、oracle 側正本定義の再公開まで、実装上の配置先を選ぶための上位ルーティング対象である。

## Read this when
- cmoc の realization implementation で、CLI 入口、サブコマンド本体、共通 runtime helper、互換 shim のどこを読むべきか選びたいとき。
- session、apply、review、indexing、TUI、doctor、init などの command が、どの実装関数や下位領域へ接続されるかを追いたいとき。
- Codex 実行、CLI 共通 runner、config、content hash、doctor preprocess、error、git、logging、path、result、state、apply process、INDEX 更新 preflight など、複数箇所で使う runtime 共通処理の入口を探しているとき。
- oracle 側の正本実装を複製せず realization 側の既存公開面から参照・再公開する互換層や、旧 import 経路の残存理由・削除条件を確認したいとき。
- src 起点の実行環境で oracle package を解決する仕組みや、runtime module 名の互換 alias を確認したいとき。

## Do not read this when
- oracle file にある正本仕様断片、prompt builder、path model、file access policy、INDEX 生成規則など、人間意図そのものを確認したいときは、対応する oracle 側を読む。
- 個別サブコマンドの詳細な業務処理だけを調べたい対象がすでに決まっているときは、この領域全体ではなく対応する下位実装へ直接進む。
- 特定 helper の細かな入出力や失敗時挙動がすでに分かっているときは、この領域全体ではなく該当する下位要素の本文を直接読む。
- ACP 型、path placeholder、構造化文書 API、設定値などの正本側定義そのものを確認したいときは、再公開入口ではなく oracle 側の定義元を読む。
- テスト期待値や外部挙動だけを確認したいときは、対応する realization test または仕様側の対象へ進む。

## hash
- 029d6995fedb3dc63e46e1c6e513a1ec86ff4a87f7dfdde5302aa17dde6026b0

# `test`

## Summary
- CLI と runtime の外部挙動を検証する realization test 群を置く領域。session/apply/doctor/indexing/TUI/Codex 実行、prompt/builder/import 境界、共通 runtime 契約など、利用者から観測できる状態遷移・出力・git 副作用・エラー処理の回帰確認への入口になる。
- 一時 Git リポジトリ、Codex home/profile、fake Codex/Ollama/systemctl、Typer 実行、apply worktree 解決など、複数テストで共有する pytest 支援コードも含む。

## Read this when
- CLI サブコマンドの終了コード、標準出力・標準エラー、report、state file、branch/worktree cleanup、commit、gitignore 反映など、外部挙動に影響する変更を行う。
- Codex exec/TUI 呼び出しの引数、profile、sandbox/file access、home 解決、retry、quota/capacity 待機、post validation、subprocess tracking、エラー変換を変更または確認する。
- apply、session、doctor/init、indexing、review oracle、TUI の既存回帰テストへ、同じ観点のケースを追加・統合できるか判断する。
- ACP builder、prompt parts、structured output schema 参照、packaged import 境界、Markdown renderer など、実装と oracle src/schema/prompt の接続を realization test から確認する。
- テスト用 repository、oracle file、Codex 設定、fake 外部コマンド、CLI runner などの共通 fixture/helper を使うまたは変更する。

## Do not read this when
- 正本仕様断片そのものを確認・編集したい場合は、oracle 側の doc/src/test を読む。
- 個別機能の内部実装責務、helper のアルゴリズム、データ構造定義だけを調べたい場合は、対応する implementation を直接読む。
- INDEX.md エントリー生成規則や routing standard の内容だけを確認したい場合は、この realization test 群ではなく対応する oracle standard または builder/schema を読む。
- LLM や Codex CLI 自体の応答品質を評価したい場合。この領域のテストは外部コマンドを fake 化し、cmoc 側の制御と副作用を検証する。

## hash
- 622c13ec8ada79fd9db6282934fa0bf5725f6cab018615c5439128bee9618363
