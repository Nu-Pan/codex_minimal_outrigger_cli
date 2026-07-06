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
- cmoc の realization implementation を収める階層で、CLI 入口、利用者向けサブコマンド、共有 runtime helper、oracle 正本実装への import shim、旧公開 import 経路の互換層を扱う。
- サブコマンド実行フロー、Codex 呼び出し境界、設定・path・git・state・logging などの共通処理、oracle 側定義の再公開や中継を通じて、正本仕様断片を実行可能な実装へ接続する入口になる。

## Read this when
- cmoc の realization implementation 全体から、CLI 配線、サブコマンド実装、共有 runtime 処理、互換 import 層のどこへ進むべきか判断したいとき。
- 利用者向け command 面、session・apply・review・indexing・doctor などの実行制御、またはそれらが共通 helper や oracle 側実装へどう委譲されるかを調べたいとき。
- oracle src の定義を複製せず realization 側の既存公開面や旧 import 経路から参照・再公開している箇所を確認したいとき。
- Codex subprocess、profile、preflight、quota/capacity retry、call log、Structured Output 検証など、実行基盤に関わる実装の入口を探したいとき。

## Do not read this when
- oracle file にある正本仕様断片、prompt、schema、人間意図そのものを確認したいときは、対応する oracle 側を読む。
- テスト期待値や外部挙動の検証だけを確認したいときは、対象の realization test または仕様に対応する本文を読む。
- 設定値、ACP 型、path model、構造化文書 API などの正本定義そのものを確認したいときは、再公開層ではなく正本側の該当対象を読む。
- 具体的に読むべき下位の command 実装、共通 helper、互換 shim が既に決まっているときは、この階層全体ではなくその対象へ直接進む。

## hash
- 2afa2fb1dcf1013d02c69e8a3539e12e864f316fbc7c16a0ffb73a7372534841

# `test`

## Summary
- CLI、runtime、apply/session/review/indexing、prompt、packaged import などの realization test を集めたディレクトリ。共有 pytest helper と、各サブコマンドや Codex 実行 wrapper の外部挙動・状態遷移・エラー境界を検証するテストへの入口になる。
- テスト対象は主に `<work-root>/src` の実装であり、oracle src/schema/prompt との参照関係、worktree・branch・session state・Codex home・fake 外部コマンドなどを使った統合的な回帰確認を扱う。

## Read this when
- realization implementation を変更した後、対応する CLI 外部挙動、runtime 契約、状態ファイル更新、Codex 実行 wrapper、prompt 組み立て、INDEX.md 更新、review/apply/session workflow の回帰テストを探すとき。
- 使い捨て git repository、Codex home、fake Codex/Ollama/systemctl、AgentCallParameter、apply worktree など、テスト用 fixture や共有 helper の前提を確認・変更するとき。
- apply fork/join/abandon、session fork/join/abandon、doctor、indexing、review oracle、TUI、Codex exec/TUI/subprocess/retry/quota retry などのサブコマンド境界を CLI 経由で検証する期待値を確認するとき。
- oracle src の schema や builder と realization 側の builder/output が一致しているか、または packaged layout から必要な import が成立するかをテスト側から確認するとき。

## Do not read this when
- 本番実装の責務分割、内部 helper、設定定義、path model、Git 操作、Codex 実行処理そのものを調べたい場合は、まず対応する realization implementation を読む。
- oracle file の正本仕様断片、schema 本体、prompt 正本文、oracle 側のテスト規則を確認したい場合は、対応する oracle 配下の文書または src/test を読む。
- INDEX.md エントリー本文の自然言語表現や routing 文書の生成規則だけを確認したい場合は、対象の routing 情報または oracle 側の標準を読む。
- 個別サブコマンドと無関係な汎用 pytest の使い方や、外部サービスそのものの仕様を調べたいだけの場合。

## hash
- b0328d7aeb251e9a558555380befd2814c796003a832b6a0188ae09e21b87a91
