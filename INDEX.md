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
- realization 側の主要実装ルート。`acp` 系の互換入口、`basic` 系の再公開、`commons` の実行時共通処理、CLI 入口、各サブコマンド実装を束ねており、正本仕様を直接書く場所ではなく、既存 import 面と実行入口を維持するための案内役として読む。
- この階層では、どの名前空間が互換 shim で、どれが実体の実装かを見分ける。個別機能の中身より、目的の責務を持つ下位モジュールへ進むための分岐点として使う。

## Read this when
- `acp.*`、`basic.*`、`config.*`、`oracle.*` のような既存 import 経路を残す必要があるかを確認したいとき。
- CLI 入口から各サブコマンド実装へどう接続されているか、また共通 runtime helper がどこにまとまっているかを確認したいとき。
- 互換 namespace を維持するべきか、それとも正本側・実体側へ寄せてよいかを判断したいとき。

## Do not read this when
- 個別の生成ロジック、CLI 挙動、状態管理、Git 操作、review/apply/session の実装詳細を知りたいとき。そうした内容は対応する下位モジュールを直接読む。
- 新しい機能や公開 API を追加する実装場所を探しているとき。この階層は入口の整理が役割で、機能追加の主戦場ではない。
- 互換入口の維持可否がすでに確定しており、詳細なルーティング確認が不要なとき。

## hash
- 1c4f8f83061a7b5eeb7edeaa11acd7887eeff1f720c8264bd2a7ac3a101b729c

# `test`

## Summary
- `test` 配下の共通補助群を案内するルーティングで、`acp_builder` 正本 schema 参照、CLI 実行補助、git/worktree 補助、Codex/Ollama 補助、INDEX 生成補助、StructDoc などのテスト支援を目的別に分けている。個別機能の正本仕様ではなく、どの共通 helper を読むべきかを絞る入口として使う。
- `test_acp_builder_*` は `acp.builder` 系の parameter 生成と公開面を検証するテスト群で、apply fork・indexing・review oracle・session join conflict resolution・tui の各 builder が正本 schema や prompt とどう整合するかを確認するための入口になっている。
- `test_apply_*` は apply fork / join / abandon の CLI 挙動と target 正規化、report 生成、state/worktree/branch cleanup を追うための入口で、対象別に lifecycle・report・正規化・終了コードの観点を分けている。
- `test_basic_runtime`、`test_runtime_*`、`test_codex_runtime_*` は path/root 解決、設定、file access、process 停止、Ollama、Codex exec の argv・権限・retry・quota・TUI など runtime 周辺の外部挙動を扱う。実行経路ごとに責務を分けており、正本仕様そのものではなく runtime 契約の回帰確認に使う。
- `test_indexing_*`、`test_review_oracle_*`、`test_session_cli`、`test_cli_tui`、`test_doctor_cli` は各サブコマンドの外部挙動と lifecycle を検証する入口で、INDEX 生成、review 対象選定、session lifecycle、TUI 起動、doctor preprocess のように、実装詳細よりもコマンド境界の確認に向いている。
- `test_prompt_parts` と `test_struct_doc_rendering` は prompt 文面の組み立てと StructDoc の Markdown 変換を検証する。前者は標準文書・file access rule・root token を含む prompt 構成、後者は空行圧縮の挙動を確認するための入口になっている。

## Read this when
- 共通テスト補助で `CliRunner`、git fixture、fake command、Ollama 呼び出し補助、Codex 実行補助のどれを使うべきか確認したいとき。
- `acp.builder` 系の builder 出力、公開面、structured output schema、prompt 注入条件を変更・確認したいとき。
- apply 系の CLI、target 正規化、report、cleanup、state/worktree/branch の更新条件を確認したいとき。
- runtime の root/path 解決、設定、file access、Codex 実行、Ollama、process tracking、retry/quota、TUI 起動のどれかを変えるとき。
- indexing、review oracle、session CLI、doctor、TUI の各コマンドの外部挙動や lifecycle を確認したいとき。
- prompt parts の文面、root token、file access rule、StructDoc の Markdown 整形を変更・確認したいとき。

## Do not read this when
- 個別のコマンド仕様や正本仕様本文を確認したいだけなら、この共通補助群ではなく対応する oracle 側や実装側を読むべきとき。
- `acp_builder` 以外の CLI や runtime の挙動を見たいだけで、builder の契約に触れないとき。
- apply 以外のサブコマンドや低レベルの git / process helper だけを確認したいとき。
- prompt 文面や runtime の一般論ではなく、別の領域のテストや実装を直接見たほうが近いとき。
- INDEX 生成規則、review 対象選定、session lifecycle、doctor preprocess などの各コマンド本体を追う必要があるとき。
- StructDoc 以外の prompt builder、CLI、runtime、oracle 正本の内容そのものを確認したいとき。

## hash
- cdf7e0e21cca2320feb2c075c670fb09080c3b93c858ca7de9c4b42433c9a206
