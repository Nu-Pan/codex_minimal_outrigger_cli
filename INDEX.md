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
- cmoc の正本仕様断片を収める領域。自然言語ドキュメントによる仕様断片と、プロンプト・schema・設定・パスモデルなどの正本実装断片へ進む入口になる。
- アプリケーション挙動や開発規則を文書として確認する領域と、AI Agent 呼び出しや標準文書パーツを Python/設定として確認する領域を切り分けるために読む。

## Read this when
- cmoc の CLI 挙動、run/session、git branch/worktree、Codex CLI 呼び出し、状態、ログ、エラー、インデクシングなどの正本仕様断片を探すとき。
- realization code を変更する前に、Python 実装・テスト・CLI 構成・開発環境などへ適用される開発規則を確認したいとき。
- AI Agent 呼び出しの parameter、Structured Output schema、完全プロンプト、標準文書パーツ、設定、パス表記、構造化文書モデルの正本実装断片を確認したいとき。
- 対象の仕様断片が自然言語ドキュメント、正本実装断片、開発規則、不採用案のどれに属するかを切り分けたいとき。

## Do not read this when
- oracle file と realization file の一般的な責務分担、編集権限、品質基準、INDEX.md エントリー生成基準だけを確認したいとき。
- realization implementation や realization test の具体的な既存コード、内部 helper、現在のテスト期待値を調べたいとき。
- CLI 引数解析、サブコマンド制御、設定ファイルの読み書き、JSON 変換、Codex CLI へ渡す実際のコマンド列など、realization implementation 側の実行フローを追いたいとき。
- 特定の作業ディレクトリで読むべきファイルや生成済み INDEX.md の内容だけを知りたいとき。

## hash
- 78fc60b045851e616de9359fa1f7fcbe8cd2bde2a61f972eab797d61ee45a4f9

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
- cmoc の realization implementation 全体への入口。公開 CLI、サブコマンド実装、共通 runtime helper、互換 import shim、正本側実装への薄い再公開層、agent call parameter builder 領域へ進むためのルーティング対象。
- CLI の起動面と実行面、複数サブコマンドで共有される補助処理、旧来 import path を維持する互換層、正本側を複製せず参照する境界を見分けるための上位ディレクトリ。

## Read this when
- realization 側の実装入口から、CLI 定義、サブコマンド実行、共通 runtime、設定・基礎型・ACP builder の互換入口のどこへ進むべきか選びたいとき。
- cmoc の公開コマンド構成、各サブコマンドの orchestration、Codex 実行境界、git・path・logging・session state・INDEX 更新支援など、実装側の責務配置を確認したいとき。
- oracle src を realization 側へ複製せず参照するための import 境界や、旧来の公開参照経路を残す互換層の位置づけを調べたいとき。
- agent call parameter builder が、正本側への薄い再公開なのか、実装側で parameter を組み立てる処理なのかを切り分けたいとき。

## Do not read this when
- 正本仕様断片、oracle 側の prompt 文面、path model、設定定義、ACP 基本型、builder 本体の正本内容を確認したいときは、対応する oracle 側の本文へ進む。
- 個別サブコマンドの詳細な制御フローや状態遷移、特定 helper の失敗時挙動や副作用など、読む対象がすでに分かっているときは、その下位領域を直接読む。
- テスト、fixture、実行ログ、生成済み report、memo、git 管理情報など、実装本体以外を探しているときは、それぞれの対象領域へ進む。
- 新しい仕様判断や公開面追加の是非だけを検討しており、既存 realization implementation の配置や互換入口を確認する必要がないとき。

## hash
- e156e8233fba00b31192d32018c48b829774c97c57e1dbdabf66be6830f8ed3a

# `test`

## Summary
- cmoc の realization test を集約するディレクトリ。CLI サブコマンド、Codex runtime、prompt 構築、indexing、session/apply/review workflow、共通 runtime 境界、テスト補助関数の外部挙動を検証する入口になる。
- 個別機能のテストだけでなく、Git worktree、branch/state cleanup、Codex subprocess、quota/capacity retry、INDEX.md 更新、正本仕様断片と prompt/schema 生成結果の一致など、複数モジュールをまたぐ回帰観点を扱う。

## Read this when
- CLI の外部挙動、終了コード、標準出力、report、state 遷移、worktree/branch cleanup などを変更または確認したいとき。
- Codex CLI 呼び出し、CODEX_HOME、sandbox/profile、process tracking、retry、quota recovery、TUI 起動前処理など runtime 境界の既存期待値を調べるとき。
- apply、session、review、indexing の workflow が Git 状態、linked worktree、dirty worktree、conflict、ignore 対象、cleanup とどう連動するかをテストから確認したいとき。
- prompt builder、Structured Output schema 参照、oracle 由来の標準部品、routing document 生成が realization 側でどう回帰検証されているかを探すとき。
- 新しいテストを追加する前に、既存の共通 fixture、fake Codex 実行、Git repository setup、parametrized case へ統合できるか確認したいとき。

## Do not read this when
- 正本仕様断片そのもの、oracle file の定義、oracle/realization 標準、INDEX.md エントリー生成規則を確認したい場合は、oracle 側の文書を読む。
- 実装内部の関数分割、helper の責務、低レベルな制御フローだけを変更する場合は、対応する realization implementation を先に読む。
- Codex CLI や LLM の出力品質そのものを評価したい場合は、このディレクトリのテストではなく、対象の prompt や schema の責務を確認する。
- 特定サブコマンドと無関係な一般的な Git 操作、設定定義、path model、profile 生成規則だけを知りたい場合は、より直接の実装または oracle src へ進む。

## hash
- 88fba703bd9e9f02d28fd15ab4c7001b0cce5ef0084b0048fdb68acdfbe63573
