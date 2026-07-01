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
- cmoc の realization implementation 全体への入口。最上位 CLI、サブコマンド実装、共通 runtime helper、agent call parameter builder、設定・基礎定義・正本側実装への互換 import 境界を含む。
- 利用者向けコマンドから実処理、共通基盤、互換層、正本側参照へ進むための上位ルーティング対象であり、個別責務の下位領域を選ぶために読む。

## Read this when
- cmoc の実装側で、CLI 入口、サブコマンド、共通 runtime、builder、設定・基礎 API の互換層のどこへ進むべきかを選びたいとき。
- 公開 CLI の command 構成、利用者操作の実行フロー、Codex 実行、Git・状態・ログ・設定・path・INDEX.md 更新などの共通基盤の所在を調べたいとき。
- 既存 import path を維持する互換入口、正本側実装への委譲、再公開範囲、削除条件を確認したいとき。
- agent call parameter の生成処理が、正本側への薄い再公開なのか、実装側で parameter を組み立てる処理なのかを見分けたいとき。

## Do not read this when
- 正本仕様断片、正本文書、正本側 builder、設定定義、path model などを確認したいときは、oracle 側の本文へ進む。
- 個別の低レベル処理や特定サブコマンドの詳細が分かっているときは、この階層全体ではなく、対応する下位領域へ直接進む。
- テストの期待挙動や検証観点を確認したいときは、実装側ではなくテスト側へ進む。
- 既存互換 import path や実装側公開面に関係しない仕様検討だけを行うときは、対応する正本仕様断片を読む。

## hash
- f100a4851fdad510a1ad26c629a12e95572232b4b1f287c8c19d746d300c0f6f

# `test`

## Summary
- CLI 外部挙動と共通 runtime 契約を検証する realization test 群。session/apply/review/indexing/init/TUI/Codex runtime/prompt/packaging など、利用者から観測できる終了コード、標準出力、state、git 副作用、report、preflight、process 制御を扱う。
- 共通 fixture と補助関数も含み、一時 Git リポジトリ、Codex home、fake executable、branch/worktree 状態など、外部コマンドや Codex 呼び出しを伴うテストの前提準備への入口になる。

## Read this when
- CLI サブコマンドの外部挙動、終了コード、標準出力、report、state 遷移、branch/worktree cleanup、dirty worktree 拒否、merge conflict 処理などを変更または確認するとき。
- Codex CLI/TUI 実行ラッパー、profile、sandbox、CODEX_HOME、retry、quota wait、process group、file access violation、preflight など、Codex 呼び出し runtime の回帰テストを探すとき。
- INDEX.md 生成・更新、indexing preflight、routing document commit、malformed entry 再生成、conflict 解決など、indexing workflow の外部挙動を確認するとき。
- ACP builder、prompt parts、Structured Output schema 参照、packaged import 境界、oracle source と realization 側 builder の接続を検証するテストを探すとき。
- テスト用の最小 repository、oracle/realization file fixture、Codex home、fake Python executable、branch 名取得、apply worktree path 解決など、共通テスト支援を使うまたは変更するとき。

## Do not read this when
- 正本仕様断片、oracle file の標準、prompt や schema の正本内容を確認したい場合は、oracle 側の該当文書や source を読む。
- 個別 helper の内部実装、関数分割、git wrapper、report renderer、path model などを局所的に変更するだけなら、対応する実装側を先に読む。
- Codex CLI や LLM の出力品質そのものを評価したい場合は読まなくてよい。ここでは fake executable や stub 応答を使い、cmoc 側の制御と副作用を検証している。
- 特定サブコマンドに関係しない一般的な設計方針や README 的な概要を探しているだけなら、このテスト群ではなく上位の routing から目的の文書へ進む。

## hash
- 18a8a541c91371a110fb0280b0a7aa920935f20eef3742bbdbe6412cda2afe66
