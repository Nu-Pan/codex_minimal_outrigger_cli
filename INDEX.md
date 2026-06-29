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
- cmoc の正本仕様断片を収める領域。自然言語仕様と AI agent 呼び出し・共通基盤・プロンプト構築に関する正本実装断片への入口になる。
- CLI 外部挙動、状態・ログ・エラー処理、branch/worktree モデル、run 隔離、開発規則、不採用設計案、AI に渡す論理パラメータや出力契約など、人間が責任を持つ仕様判断を確認するための領域である。
- realization code の現在構造ではなく、人間意図を根拠に、公開面・制御境界・保存先・失敗時挙動・責務分担・agent call 契約を判断するために読む。

## Read this when
- cmoc の CLI 挙動、サブコマンド、利用手順、状態遷移、出力、ログ、エラー処理、run 隔離、agent call 境界など、利用者や外部連携に見える仕様を確認したいとき。
- session fork / join、session branch、run branch、linked worktree、cmoc-managed branch など、git branch・commit・worktree に関する cmoc 用語と責務を正本仕様から確認したいとき。
- realization code を追加・修正する前に、Python 実装、CLI 構成、共通処理の配置、開発環境、pytest 方針などの横断的な開発規則を確認したいとき。
- AI agent 呼び出し時の role、goal、prompt、file access profile、モデル設定、reasoning effort、Structured Output schema、出力契約を確認したいとき。
- 機能別の AI 呼び出し仕様、共有設定、パス表記、ファイルアクセス権限、規範文書表現、構造化 Markdown レンダリング、プロンプト構築順序や標準文書注入の扱いを探したいとき。
- AI 記憶、kaizen、自動注入、作業計画レビュー、apply 系 orchestration など、採用しなかった設計案の理由や non-goal を確認し、現行方針を変えるべきか判断したいとき。

## Do not read this when
- 具体的な関数、クラス、helper、テスト期待値、既存 realization code の現在構造を調べたいときは、実装またはテストを読む。
- AI agent 呼び出しの実行手順、プロセス起動、結果取得、エラー処理だけを確認したいときは、実行フロー本体を扱う実装へ進む。
- git 操作、branch 操作、fork 作成・適用、session join 通常処理、CLI 表示など、AI 呼び出し契約の外側にある処理本体を確認したいときは、該当する実装領域を読む。
- 個別の prompt builder や AgentCallParameter builder が生成する具体的な値、引数、profile 内容だけを確認したいときは、それらの正本となる実装側を読む。
- Codex CLI の外部仕様、利用可能モデル、最新のモデル情報を調べたいときは、この領域ではなく外部の公式情報を確認する。
- 対象が特定の文書領域や単一仕様に絞れているときは、この領域全体ではなく、下位の直接該当する対象へ進む。

## hash
- e6bacf18de32536c3e8f74bab6bf7d43021ecdd847fa854f148f4edecd5b09e8

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
- cmoc の realization implementation を収める実装ルートであり、最上位 CLI、サブコマンド実装、runtime 共通 helper、設定・basic・acp・oracle import 互換層などへの入口になる。
- この階層では、公開 CLI 入口から各サブコマンド本体、共有 runtime、正本側実装への互換再公開までを切り分け、実装本体を読むべき領域と移行用 shim を読むべき領域を選べる。
- oracle 側の正本仕様断片や正本実装そのものではなく、それらを具体化・参照・委譲する realization 側実装を探すための階層である。

## Read this when
- cmoc の実装を変更するために、CLI 入口、サブコマンド実装、runtime 共通 helper、互換 import 層のどこへ進むべきかを選びたいとき。
- `cmoc` console script から Typer app、各サブコマンド、共有 runtime、Codex subprocess、git、config、state、INDEX 更新などの実装領域へのつながりを確認したいとき。
- `acp.*`、`basic.*`、設定、`oracle.*`、旧 runtime module など、realization 側に残る互換 import path が正本側または実体 module へどう委譲されるかを調べたいとき。
- apply、review、session、indexing、init、TUI など、利用者が呼び出す操作の実装入口を探し、共通 helper と個別サブコマンド本体を切り分けたいとき。

## Do not read this when
- oracle file の正本仕様断片、正本 prompt、schema、型、path model、設定定義そのものを確認したいときは、対応する oracle 側を読む。
- テストの期待挙動や fixture を確認したいときは、realization test 側を読む。
- 特定の公開 CLI コマンド構成だけを確認したい場合は最上位 CLI 入口へ、特定サブコマンドの本体だけを確認したい場合は該当するサブコマンド領域へ直接進む。
- git、path、config、logging、Codex 起動などの低レベル共通処理だけを調べる場合は、この階層全体ではなく、対応する runtime helper 領域へ進む。

## hash
- 4946931e2edac663f6380bc9e8717c1bfda97d53506ccaf77b8fc7d3ceefa3ba

# `test`

## Summary
- cmoc の realization test 群を置くテスト領域。CLI サブコマンド、Codex runtime、indexing、prompt builder、file access profile、session/apply/review workflow など、実装の外部挙動と重要な制御境界を pytest で検証する。
- 共通 fixture・補助 profile と、機能別の CLI 回帰テストへの入口になる。

## Read this when
- cmoc の実装変更に対応する realization test を探し、どのテストファイルを読むべきか判断したいとき。
- apply、session、review oracle、indexing、init/TUI、Codex runtime、prompt builder、共通 runtime 契約のいずれかの外部挙動や回帰テストを確認・変更するとき。
- テストで使う共通 Git repository fixture、Codex home/profile 差し替え、file access profile の共有定義を確認したいとき。

## Do not read this when
- oracle file の正本仕様断片そのものを確認したいときは、oracle 配下の該当文書や source を読む。
- 実装 helper の内部構造だけを局所的に変更したい場合は、対応する src 側の実装モジュールを先に読む。
- Codex CLI や LLM の出力品質そのものを評価したいとき。この領域のテストは主に fake 応答や subprocess 制御により cmoc 側の外部挙動を検証する。

## hash
- 58bb7c95d5518e34d457c83be5fddbf93d1ce620f5274b9e95eab09109e6a880
