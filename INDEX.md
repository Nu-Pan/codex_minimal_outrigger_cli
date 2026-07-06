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
- cmoc の realization implementation を置く実装入口階層。CLI 入口、サブコマンド orchestration、共通 runtime helper、oracle package shim、旧 import 互換層を束ね、利用者向け command から正本側定義や下位実装へ接続する。
- apply、review、session、tui、indexing、doctor、init、eval oracle などの実行入口と、Codex 実行、path 解決、設定、git、状態管理、INDEX 更新 preflight などの横断基盤を探す起点になる。
- oracle src 側の正本定義を複製せず参照・再公開するための acp、basic、config などの互換入口や、runtime・oracle package の移行 shim も扱う。

## Read this when
- cmoc の realization implementation 全体から、CLI 入口、個別サブコマンド、共通 runtime helper、互換 import 層のどこへ進むべきか判断したいとき。
- コマンド名、CLI option、console script 起動、サブコマンド実行フロー、preflight、branch/worktree/state 操作、report 出力、Codex 呼び出しへの接続点を確認・変更したいとき。
- Codex exec/TUI 起動、quota/capacity retry、Structured Output 検証、call log、config JSON、git worktree、oracle file 判定、path 解決など、複数サブコマンドにまたがる基盤処理を調べたいとき。
- oracle 側 canonical 実装や正本定義を realization 側の既存 import 経路から参照・再公開している acp、basic、config、oracle package shim、runtime shim の維持理由や削除条件を確認したいとき。

## Do not read this when
- oracle file の正本仕様断片、自然言語プロンプト、Structured Output schema、path keyword の概念定義、agent call parameter の構築仕様そのものを確認したいときは、対応する oracle 側を読む。
- 特定の共通 runtime API、サブコマンド下位処理、builder、report 描画、INDEX 統合、git wrapper など読むべき対象がすでに分かっているときは、この階層全体ではなく該当する下位対象へ直接進む。
- CLI や runtime の利用者向け仕様だけを確認したいときは、対応する oracle doc または個別コマンドの正本仕様へ進む。
- 旧 acp、basic、config、runtime などの互換 import 経路がすでに不要で、互換 shim の削除判断や移行経緯を確認する必要がないとき。

## hash
- 66f1a76c57441c7b7c33cca8d4c70099989c76f0ab31f5f83b43a92022224d6e

# `test`

## Summary
- cmoc の realization test 群を収めるディレクトリ。CLI サブコマンド、Codex runtime、indexing、prompt rendering、packaged import、共通 test support など、src 実装の外部挙動と制御ロジックを回帰確認する入口になる。
- apply/session/review/indexing/doctor/TUI/Codex 実行系の統合的な CLI 挙動は個別テストに分かれ、共通 fixture や fake 外部コマンド環境はテスト支援モジュールに集約されている。

## Read this when
- realization implementation の変更に対して、対応する外部挙動・状態遷移・git 副作用・runtime 境界の既存テストを探すとき。
- apply fork/join/abandon、session fork/join/abandon、review oracle、indexing、doctor/init、TUI、Codex exec/TUI runtime の CLI 回帰テストを確認・変更するとき。
- Codex home/profile/sandbox、quota/capacity retry、post validation、process tracking、prompt parts、packaged import など、複数実装モジュールにまたがる runtime 契約をテスト観点から確認するとき。
- 新しいテストを追加する前に、既存の fixture、parametrized case、同じ責務のテストファイルへ統合できるか判断するとき。

## Do not read this when
- 本番実装の責務、内部 helper、データ構造、path 分類、CLI 処理本体を変更したい場合は、まず src 側の該当 implementation を読む。
- oracle file の正本仕様、標準文書、Structured Output schema、開発ルールそのものを確認・編集したい場合は、oracle 配下の該当文書や定義を読む。
- 個別コマンドや runtime 領域が既に分かっており、対応するテストファイルへ直接進める場合は、この階層全体を広く読む必要はない。
- Codex CLI や LLM の出力品質そのものを評価したい場合は対象外であり、ここでは cmoc 側の呼び出し制御と観測可能な副作用を扱う。

## hash
- c114115e3682d49300912095080e16948cf83360f6706cda3f9fcecf6ab2c6ed
