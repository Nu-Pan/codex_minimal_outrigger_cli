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
- cmoc の realization implementation 全体の入口。CLI 最上位、サブコマンド実装、共通 runtime helper、agent call parameter builder、設定・basic・oracle 側実装への互換 shim など、実装側の主要領域を束ねる。
- 利用者が起動する CLI 制御、サブコマンド固有の orchestration、Codex 実行境界、git/state/path/config などの共有実行時基盤、既存 import path を維持する薄い互換層の読む先を切り分けるためのルーティング対象。

## Read this when
- cmoc の実装側で、CLI 入口、サブコマンド、共通 runtime helper、ACP builder、互換 import 層のどこへ進むべきかを最初に選びたいとき。
- 公開 CLI コマンド構成、サブコマンド実装、Codex 実行連携、INDEX.md 更新 preflight、git・state・path・config など横断的な runtime 処理の所在を探したいとき。
- 既存の `acp.*`、`basic.*`、設定、`oracle.*`、古い runtime import path などの互換入口が、正本側または実体 module へどう委譲されているか確認したいとき。
- realization 側の実装本体と、正本側実装を複製しないための薄い再公開・shim・互換層を見分けたいとき。

## Do not read this when
- 正本仕様断片、prompt の正本文面、oracle 側 builder・設定・path model・構造化文書 API の定義内容そのものを確認したいときは、対応する oracle 側本文へ進む。
- 個別サブコマンドの詳細な制御フロー、低レベル helper、個別 builder の型変換や prompt 補正など、読む対象がすでに分かっているときは該当する下位領域へ直接進む。
- realization implementation ではなく realization test、補助スクリプト、パッケージ設定、生成済みログや永続 state の実データを調べたいとき。
- Typer、Click、git、Codex CLI など外部ツールの一般的な使い方だけを調べたいとき。

## hash
- 7aee68764e374bb3ee2ed4432009b2cf79254709b2f179fe0c8ce43c9fe3e418

# `test`

## Summary
- CLI 外部挙動と runtime 契約を検証する realization test 群。apply、session、review oracle、indexing、init/TUI、Codex 実行、prompt 構築、共通 runtime など、利用者から観測できる出力・終了コード・状態遷移・git/worktree 副作用を中心に扱う。
- 一時 Git リポジトリや fake Codex 実行などの共通補助も含み、サブコマンド統合挙動、Codex subprocess 境界、routing document 更新、state cleanup、branch/worktree cleanup の期待値を確認する入口になる。

## Read this when
- CLI サブコマンドの外部挙動、終了コード、標準出力・標準エラー、report、state file、branch/worktree 副作用に関する既存テストを探すとき。
- apply fork/join/abandon、session fork/join/abandon、review oracle、indexing、init/TUI 起動前処理の回帰テストを確認または変更するとき。
- Codex CLI 実行 wrapper の subprocess 引数、CODEX_HOME、sandbox profile、quota/capacity retry、call log、process tracking、preflight との結合挙動を確認するとき。
- prompt 標準部品や AgentCallParameter builder の生成結果、structured output schema 参照、oracle 側の prompt/schema 断片との一致を realization test で確認するとき。
- テスト用 Git リポジトリ、Codex home、fake executable、profile 生成差し替えなど、複数の CLI テストで共有される fixture・補助関数を探すとき。

## Do not read this when
- oracle file の正本仕様断片、oracle/realization 標準、INDEX.md ルーティング規則そのものを確認したい場合は、oracle 側の該当文書を読む。
- 実装内部の関数分割、低レベル helper、データ構造定義だけを局所的に変更したい場合は、対象の realization implementation を直接読む。
- Codex CLI や LLM の出力品質そのものを評価したい場合は、このテスト群ではなく prompt や実行環境の目的に合う対象を確認する。
- 個別機能に関係しない一般的な Git 操作、設定 schema、path model の定義を確認したいだけなら、対応する実装または oracle src を読む。

## hash
- 3b41e1a7d888d211afb0bf829be989fdb1a52e393ec63d87085274ebefb7ca05
