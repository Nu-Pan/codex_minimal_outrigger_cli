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
- cmoc の realization implementation を収める階層。CLI 入口、サブコマンド実装、runtime 共通 helper、互換 import shim、oracle 側正本実装への参照・再公開境界を扱う。
- 利用者向け command 面から workflow 制御、Codex 実行基盤、git/worktree/state/path/logging/error/indexing などの共通処理へ進むための入口になる。
- oracle 側の正本仕様・正本実装を複製せず参照する互換層も含み、旧 import 経路の維持・削除判断や公開名の移行状況を確認する場所になる。

## Read this when
- cmoc の実装本体を調査・変更するために、CLI 入口、サブコマンド、runtime 共通 helper、互換 shim のどこへ進むべきか判断したいとき。
- apply、session、review、indexing、tui、doctor、eval oracle などのサブコマンド workflow や、それらを CLI から呼び出す経路を確認したいとき。
- Codex 実行、設定読み込み、path 解決、git 操作、logging、error report、state、doctor、INDEX.md maintenance など、複数処理から共有される runtime 基盤を探したいとき。
- oracle 側正本実装への参照・再公開によって既存 import 互換を保っている箇所や、その削除条件を確認したいとき。
- runtime package shim、公開 module alias、console script 起動、引数解析エラー変換など、実装入口と公開 import 経路の薄い配線を調べたいとき。

## Do not read this when
- oracle file の正本仕様、人間意図、prompt、Structured Output schema、path keyword の概念定義を確認したいときは、oracle 側の該当対象を読む。
- 実装ではなくテスト固有の期待値、fixture、外部挙動の検証観点を確認したいときは、test 側の該当対象を読む。
- 個別のサブコマンド処理や共通 helper の所在がすでに分かっているときは、この階層全体ではなく該当する下位対象へ直接進む。
- oracle 側定義を複製せず再公開しているだけの互換層について、再公開先の仕様や実装詳細そのものを知りたいときは正本側または実体 module を読む。

## hash
- 4363fe098eb67267d1e495a6cb2f7a5f95b53823fe5cc562f8dfaf65e9d842d6

# `test`

## Summary
- CLI、runtime、Codex 実行、apply/session/review/indexing/doctor、prompt、packaging、Ollama、Markdown rendering などの realization test 群をまとめるテスト領域。
- 共有 fixture による一時 Git リポジトリや fake 外部コマンドを入口に、サブコマンドの外部挙動、状態遷移、ログ、profile、権限、report、preflight、cleanup、retry 境界を回帰確認する。
- 個別の実装詳細よりも、利用者から観測できる CLI 結果、git/state 副作用、Codex/Ollama 起動境界、structured output schema 参照の互換性を確認する入口になる。

## Read this when
- CLI サブコマンドの終了コード、標準出力、report、commit、worktree/branch/state cleanup、dirty worktree や conflict 時の拒否条件など、外部挙動の期待値を確認・変更するとき。
- Codex exec/TUI 実行 wrapper、profile 生成、file access mode、CODEX_HOME、call log、subcommand log、quota/capacity retry、subprocess tracking など runtime 境界の回帰テストを探すとき。
- apply fork/join/abandon、session fork/join/abandon、review oracle、indexing、doctor の統合的な状態遷移や git 副作用を検証するテストを探すとき。
- oracle src の schema や prompt builder を realization 側 builder がどう参照し、packaged layout や compatibility module で公開されるかを確認するとき。
- テスト用の一時 repository、Codex home、fake executable、fake managed Ollama、Typer runner、apply worktree 解決など、共通テスト支援を使うまたは変更するとき。
- Ollama サービス検証、Markdown rendering、prompt parts、基礎 runtime 契約など、複数機能の前提になる小さな共通挙動の回帰テストを確認するとき。

## Do not read this when
- 正本仕様断片そのもの、oracle file・realization file・path keyword・INDEX エントリー規約などの定義を確認したいだけなら、oracle 側の該当文書を読む。
- 個別サブコマンドや runtime helper の内部実装方針だけを確認したい場合で、CLI 経由の外部挙動や git/state 副作用の期待値が不要なら、対応する実装モジュールを直接読む。
- Codex CLI や LLM の回答品質、prompt 文面の良し悪しそのものを検証したい場合。ここでは cmoc が管理する起動条件、成果物、schema、ログ、状態を検証対象にしている。
- 本番の Codex profile 生成、Ollama 管理、runtime apply 実装の詳細だけを変更する場合で、fake 外部コマンドを使ったテスト境界を確認する必要がないとき。
- INDEX.md 更新内容の自然言語表現だけを確認したい場合や、routing document の本文生成規則だけを扱う場合。

## hash
- e02e60e22f1acd0818db9b31c9aecf9dc7672d60d53fdae3c5eb52ccfc0c198a
