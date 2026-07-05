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
- cmoc の realization implementation をまとめる領域。最上位 CLI、サブコマンド、共通 runtime helper、oracle package shim、正本側定義を複製しない互換 import 層など、実行時の具体化コードへ進む入口になる。
- CLI コマンド構成から個別 workflow、Codex 実行・設定・git・path・state・error・INDEX 更新などの横断基盤、旧 import 経路の互換維持まで、realization 側でどの責務へ進むべきかを切り分けるための階層。

## Read this when
- cmoc の実装側で、最上位 CLI、個別サブコマンド、共通 runtime helper、互換 import 層のどこを読むべきか判断したいとき。
- session、apply、review、indexing、TUI、初期化・修復などの workflow の実行入口、事前条件、状態遷移、出力、後片付けを確認または変更したいとき。
- Codex 実行、設定、git、path、logging、state、error、content hash、Structured Output schema、INDEX 更新 preflight など、複数機能から使われる runtime 基盤へ進みたいとき。
- oracle 側 canonical 実装や正本定義を複製せず、realization 側の公開 import 経路、package shim、互換 alias、再公開 wrapper がどう接続されるか確認したいとき。
- 旧 import 経路を canonical 実装へ移行する作業で、残すべき互換層、公開面に残る参照、削除条件を判断したいとき。

## Do not read this when
- oracle file にある正本仕様断片、prompt 本文、parameter 生成内容、path model、config 定義そのものを確認したいときは、oracle 側の該当対象を直接読む。
- realization test の期待値、外部挙動、fixture、テスト固有の制御を確認したいときは、対応する test 側を読む。
- ACP 型、path placeholder、構造化文書 API など共通基礎仕様だけを確認したいときは、再公開や互換入口ではなく正本側または共通定義を読む。
- 個別機能の担当領域がすでに分かっている場合は、この階層全体ではなく、該当する下位対象を直接読む。
- 新しい公開 API、設定項目、永続状態、import 経路を設計したいだけで、既存 realization 実装や互換維持の切り分けが不要なときは、先に正本仕様または新規機能の入口を確認する。

## hash
- 21ec12ca2e829b72355c64059ae53d7e11fd380ebc80ce8673483c7eb2f1fa9e

# `test`

## Summary
- cmoc の realization test 群を収めるディレクトリ。CLI サブコマンド、Codex 実行 runtime、ACP/prompt builder、INDEX.md 更新、packaged import、StructDoc rendering など、realization implementation の外部挙動と共通制御ロジックを検証する。
- 一時 Git repository、Codex home、fake 外部コマンド、fake Codex 応答、linked worktree、process tracking など、テスト間で共有される補助環境への入口も含む。

## Read this when
- realization implementation の変更に対応する既存テストの所在を探したいとき。
- session、apply、review oracle、doctor/init、TUI、indexing などの CLI 外部挙動、状態遷移、git 副作用、report 出力、cleanup 条件の回帰テストを確認・変更するとき。
- Codex exec/TUI runtime の起動引数、sandbox、Codex home、retry、quota retry、post validation、subprocess tracking、外部コマンド不在時の失敗変換を確認・変更するとき。
- ACP builder、prompt parts、structured output schema 参照、packaged import 境界、StructDoc Markdown rendering など、CLI 以外の realization code 契約をテスト観点から確認するとき。
- テスト支援用の一時 repository、fake Codex/Ollama/systemctl、AgentCallParameter、Codex profile、apply worktree 解決 helper の使い方を確認するとき。

## Do not read this when
- production 実装の責務・内部処理を直接変更したい場合は、対応する implementation 側を先に読む。
- oracle file の正本仕様、schema、標準 prompt、文書構成、ルーティング規則そのものを確認・編集したい場合は、oracle 配下の該当対象を読む。
- 個別機能の期待挙動がすでに分かっており、実装箇所だけを局所的に確認したい場合は、src 配下の対応箇所へ直接進む。
- Codex CLI や LLM の出力品質そのものを評価したい場合。このディレクトリのテストは fake 化や制御観測により cmoc 側の挙動を検証する。

## hash
- 8838c16b89a3ae37f95652949e237b1cfeb446ced202e66dec7b3e229aa27122
