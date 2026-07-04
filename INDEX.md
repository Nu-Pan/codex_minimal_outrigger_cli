# `AGENTS.md`

## Summary
- cmoc リポジトリで作業する AI agent 向けの最上位作業規約を定める。リポジトリの略称、パス表記、ルーティング文書の利用、アクセス禁止・編集禁止対象、正本仕様断片と実装・テスト配置の基本方針を扱う。
- 作業開始時に従うべき共通前提をまとめた入口であり、個別仕様や実装詳細へ進む前に、読む順序と触れてよい領域を判断するための基準を提供する。

## Read this when
- cmoc リポジトリで作業を始める前に、基本的な作業規約、読みに行くべき仕様領域、編集可能な領域を確認したいとき。
- パス表記の意味、正本仕様断片の位置づけ、実装とテストを置く場所、閲覧・編集してはいけない対象を確認したいとき。
- ルーティング文書をどのように使って必要なファイルを探すべきか、作業中のファイル探索方針を確認したいとき。

## Do not read this when
- 個別機能の詳細仕様、CLI の具体的な挙動、出力形式、テスト期待値を調べたいだけの場合。その場合は正本仕様断片や該当する実装・テストへ進む。
- 特定モジュールの実装構造や関数の挙動を確認したい場合。その場合は実装配置の下位対象へ直接進む。
- ルーティング文書そのもののエントリー内容や同階層の対象一覧を確認したい場合。その場合は同階層のルーティング文書を読む。

## hash
- be280f67baf8ea9e564641d6ae7327aff20fd9575bc114fa291f3c5de87833ac

# `LICENSE`

## Summary
- ソフトウェアの利用・複製・変更・配布・再許諾・販売を許可するライセンス条件と、著作権表示および許諾表示の同梱義務、無保証・免責を定める法的文書。

## Read this when
- このソフトウェアを配布、再配布、再許諾、販売、または派生物に組み込む際の許可範囲と義務を確認したいとき。
- 著作権表示や許諾表示を、コピーまたは実質的な部分に含める必要があるか確認したいとき。
- 保証の有無、作者または著作権者の責任範囲、損害賠償責任の扱いを確認したいとき。

## Do not read this when
- CLI の仕様、実装方針、テスト方針、ルーティング文書の作成規則を確認したいとき。
- ソースコード、テスト、設定、開発手順、パスモデルなど、プロダクトの挙動や構造を調べたいとき。
- 正本仕様断片と実装ファイルの関係、または INDEX.md エントリー生成の基準を確認したいとき。

## hash
- a894f2547af0349f234986eb4661f0146f37b7d82f8b22a27a674d5c1236f08f

# `README.md`

## Summary
- cmoc の概要、初期セットアップ手順、基本ワークフローへの参照、ターミナルロック回避の Tips をまとめた、プロジェクト利用開始時の入口となる案内文書。
- AI が作業規約の詳細へ進むための参照先と、利用者がローカル環境で cmoc コマンドを使い始めるための最小手順を示す。

## Read this when
- cmoc が何を補助するツールなのか、略称を含めた全体像を最初に確認したいとき。
- リポジトリを取得して Python 仮想環境を作り、開発用にインストールする初期セットアップ手順を確認したいとき。
- 任意でコマンドの実行パスを通す方法を確認したいとき。
- 基本ワークフローの詳しい説明へ進むための入口を探しているとき。
- Ctrl+S によるターミナル停止を避けるためのシェル設定例を確認したいとき。

## Do not read this when
- AI の作業規約、編集制限、ルーティング規則などの詳細を確認したいときは、作業者向け規約の本文へ直接進む。
- cmoc の基本ワークフローそのものの詳細を確認したいときは、ワークフロー仕様の本文へ直接進む。
- 実装やテストの具体的なコード構造、関数、挙動を調査したいときは、実装またはテストの対象領域へ直接進む。
- oracle file、realization file、パスモデルなどの正本仕様断片を確認したいときは、該当する仕様本文へ直接進む。

## hash
- c6c3f3c5798ecc63f8611a40982f7bc8100116d8a934616bbd2b2a5b5e0a1afc

# `bin`

## Summary
- CLI 起動のための薄いシェルラッパーを置く領域。リポジトリルート基準で仮想環境 Python を探し、通常起動や補完プローブを Python 実装へ委譲する入口を扱う。
- 仮想環境 Python が存在しない、または実行できない場合に、利用者向け Markdown エラー、セットアップ手順、表示用パス、簡易 call stack を出力して失敗させる起動前処理を扱う。

## Read this when
- コマンド起動時にどの Python 実装へ処理が委譲されるかを確認したいとき。
- 仮想環境が未作成または実行不能な場合の、起動失敗時の利用者向け出力や終了挙動を確認・変更したいとき。
- シェル補完プローブ時に通常起動と異なる分岐を取る理由や、補完時の失敗コードを確認したいとき。
- 起動前エラーの文面、セットアップ手順、表示用パス、call stack 行番号の組み立てを確認・変更したいとき。

## Do not read this when
- Python 側の CLI サブコマンド、引数解析、業務ロジック、実行後の出力内容を調べたいとき。
- 仮想環境の作成方法そのもの、依存パッケージ、プロジェクト設定を変更したいとき。
- oracle file、path model、または正本仕様断片の定義を確認したいとき。

## hash
- bcc444f615624a979df5ebba33008d88c68e9f32a99b58386f9f0158f7e98b02

# `codex_minimal_outrigger_cli.code-workspace`

## Summary
- VS Code ワークスペースの対象ルート、エディタ設定、Python 解析対象、Markdown 編集設定を定義する補助設定ファイル。
- 開発環境で除外表示する生成物やルーティング文書、Python の仮想環境・解析パス・整形設定を確認する入口となる。

## Read this when
- VS Code 上で cmoc のワークスペースを開く際の対象フォルダやエディタ挙動を確認したいとき。
- Python のデフォルトインタプリタ、解析対象パス、解析対象ディレクトリ、保存時整形設定を確認したいとき。
- エディタ上で非表示にされる生成物・補助文書の扱いを確認したいとき。
- Markdown 編集時のインデント幅やスペース利用設定を確認したいとき。

## Do not read this when
- cmoc の CLI 挙動、ドメイン仕様、出力互換性を確認したいとき。正本仕様断片または実装・テストを読む方が直接的である。
- Python 実装やテストの処理内容を調査・変更したいとき。対象は開発環境設定であり、実装ロジックは含まない。
- ルーティング文書そのものの内容や生成規則を確認したいとき。対象はエディタ上の表示除外対象として扱うだけで、ルーティング情報は含まない。
- パッケージ依存関係、テスト実行手順、ビルド手順を確認したいとき。対象はそれらの手順や依存定義を担わない。

## hash
- 1938307f70f255710d75d39c07d860ecb381acbb031ca19b2f2b6e565ac41acb

# `oracle`

## Summary
- cmoc の正本仕様断片全体への入口。自然言語仕様と実装形式の仕様に分かれ、外部挙動、branch/worktree モデル、agent call、プロンプト生成、共通モデルなど、人間意図と実装差を避けたい事項を確認するための領域。
- 実装・テストへ進む前に、自然言語で確認すべき仕様か、実装として書かれた仕様かを切り分けるためのルーティング対象。

## Read this when
- cmoc の実装やテストを変更する前に、根拠となる正本仕様断片を探し始めるとき。
- CLI 挙動、サブコマンド、Codex CLI 呼び出し、ログ、エラー処理、セッション状態、run 隔離、索引生成など、アプリケーション横断の外部仕様を確認したいとき。
- session fork/join、apply/review、managed branch、linked worktree など、cmoc の git branch・commit・worktree の扱いを確認したいとき。
- agent call に渡す role、prompt、権限、モデル方針、preflight 有無、Structured Output schema、プロンプト生成の正本値を探し始めるとき。
- リポジトリ設定、ルートパスプレースホルダ、規範文書モデル、構造化 Markdown レンダリングなど、複数領域から参照される共通概念を確認したいとき。
- 現行設計の変更を検討する際に、採用済み仕様や過去に不採用となった代替案との境界を確認したいとき。

## Do not read this when
- 実装ファイルやテストファイルの具体的な関数、クラス、内部 helper、既存コード構造だけを調べたいとき。
- CLI サブコマンドの実行制御、git 操作、状態ファイル、表示整形、対象ファイル探索など、プロダクト実行フローの実装を直接調べたいとき。
- バックエンド固有のモデル名変換、プロセス起動、結果処理、エラー処理など、AI 呼び出し実行基盤の詳細を追いたいとき。
- 採用済み仕様ではなく外部ツール自体の一般的な使い方だけを調べたいとき。
- 読むべき個別の正本仕様断片、実装、またはテストが既に分かっており、その本文へ直接進めるとき。

## hash
- 369e4dc088d4b39fd2a9a0abdb6e79063031fcc97ea785c097b5afb15aa49b5e

# `pyproject.toml`

## Summary
- Python プロジェクトの配布・ビルド・テスト実行に関わる設定をまとめる補助的な設定ファイル。パッケージ名、Python バージョン、実行時・開発時依存、CLI エントリーポイント、setuptools の収集対象、テスト時の import path を定義する。
- 実装本体や正本仕様ではなく、実装ファイルと oracle 側 Python パッケージをどのようにインストール・検出・テスト実行環境へ載せるかを確認する入口になる。

## Read this when
- 依存パッケージ、要求 Python バージョン、ビルドバックエンド、setuptools のパッケージ検出、package data の扱いを確認または変更したいとき。
- CLI コマンド名がどの Python callable に接続されるかを確認または変更したいとき。
- テスト実行時にどのソースツリーが import 対象へ追加されるかを確認したいとき。
- 実装側ソースと oracle 側ソースを同じ Python プロジェクト内でどう配置・配布しているかを確認したいとき。

## Do not read this when
- CLI の具体的な挙動、サブコマンド処理、実行時状態管理、出力内容を調べたいときは、実装ソースを直接読む。
- 正本仕様断片や用語定義、設計意図を確認したいときは、oracle 側の本文を読む。
- 個別テストケースの期待値や検証観点を確認したいときは、テストソースを読む。
- リポジトリ全体のルーティングや各ディレクトリの読む順序を判断したいだけのときは、該当階層のルーティング情報を読む。

## hash
- d01948ab1730e2747d529d49d8c8ca10b84bd6a86e19d7b2810ee87c95ccb904

# `src`

## Summary
- cmoc の realization implementation 全体を扱う実装入口。CLI entrypoint、サブコマンド orchestration、共通 runtime helper、互換 import 層、oracle src への委譲 shim など、利用者向け実行面と既存公開 import 面を構成する領域をまとめる。
- トップレベル CLI 配線、session・apply・review・init・indexing・tui の実行本体、Codex 呼び出しや git・state・path・log などの共通処理、ACP・basic・config 互換入口を切り分けて下位対象へ進むための入口になる。
- oracle src の正本実装を realization 側へ複製せず、既存 caller や公開 import path を維持するための再公開・委譲・shim の境界を確認する場所でもある。

## Read this when
- cmoc の実装側で、CLI 入口、サブコマンド本体、共通 runtime helper、互換 import 層のどこへ進むべきかを切り分けたいとき。
- Typer ベースのコマンド階層、サブコマンド実行フロー、preflight、Codex 実行、git/worktree/state 操作、report・stdout 出力、INDEX 更新などの realization implementation を確認または変更したいとき。
- ACP、basic、config、oracle package など、oracle src 側の正本実装を複製せずに既存 import 経路を成立させている互換境界を調べたいとき。
- 複数サブコマンドから共有される runtime helper、設定、path 解決、エラー表示、logging、session state、apply process 管理、hash・ignore 判定などの所在を探したいとき。

## Do not read this when
- oracle file の正本仕様断片、人間意図、prompt、Structured Output schema、path placeholder、file access rule などを確認したいときは、対応する oracle 側の文書または実装を読む。
- 個別の正本定義そのもの、たとえば ACP 型、設定定義、path model、構造化文書処理、用途別 builder 本文だけを確認したいときは、再公開入口ではなく定義元を読む。
- 生成済みログ、実行履歴、cache 的な出力内容の調査だけが目的で、実装や互換 import 境界を変更しないとき。
- 新しい公開 API、設定項目、import 経路、永続状態を追加する場所を探しているだけで、現行の実装入口や互換維持の確認が目的ではないときは、まず canonical な定義元や対応する設計対象を読む。

## hash
- f04e8691dc954b11e09e0f5d582b933357f5bd2ab4bd0a28c3a890f1bcde2b47

# `test`

## Summary
- cmoc の realization test 群を置くディレクトリ。CLI サブコマンド、Codex runtime、ACP builder、INDEX 更新、packaging、prompt rendering などの外部挙動と共通 runtime 契約を、用途別のテストファイルへ分けて検証する入口になる。
- 共通 fixture や test helper も同階層にあり、個別サブコマンドの回帰確認だけでなく、テスト用 Git repository、Codex home、fake executable、session/apply state 補助を探す起点にもなる。

## Read this when
- cmoc の実装変更に対して、どの realization test を読んで期待挙動や回帰範囲を確認すべきか選びたいとき。
- apply、session、review oracle、init/TUI、indexing、Codex runtime、ACP builder、prompt parts、packaged import、StructDoc rendering のテスト入口を探すとき。
- CLI 経由の外部挙動、state 遷移、worktree/branch cleanup、Codex subprocess 実行、file access violation、retry、quota retry、INDEX 更新 commit などの既存期待値を確認したいとき。
- テストで使う一時 Git repository、Codex home、profile stub、fake external command、apply worktree path 解決などの共通補助を探したいとき。

## Do not read this when
- oracle file の正本仕様断片そのものを確認したいときは、oracle 配下の対応する doc、src、test を読む。
- 本番実装の内部 helper やアルゴリズムだけを局所的に変更したい場合で、外部挙動や回帰テストの期待値確認が不要なときは、src 配下の該当実装を先に読む。
- INDEX.md エントリー生成規則や oracle/realization の一般標準だけを確認したいときは、該当する正本仕様断片を読む。
- Codex CLI や LLM の出力品質そのものを評価したいだけのとき。

## hash
- 51f920479100ec1351581b8202dd74990b96e6eca6cd527bb0765b59fed4b1c7
