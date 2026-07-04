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
- cmoc の正本仕様断片を束ねる領域。自然言語の仕様文書と、AI エージェント呼び出し・prompt・Structured Output schema・横断モデルなどの oracle src へ進む入口になる。
- 利用者向け挙動、git branch/worktree、過去に不採用となった設計案、開発規約、パス・設定・規範文書モデルなど、人間が責任を持つ仕様断片の読む先を切り分ける対象。

## Read this when
- cmoc の正本仕様断片を起点に、外部挙動、状態、ログ、branch/worktree、agent call、prompt、Structured Output schema、開発規約の読む先を探すとき。
- CLI 挙動、サブコマンド、共通前処理、エラー処理、索引生成、セッション状態、run 隔離、Codex CLI 呼び出し、プロンプト受け渡し、ローカル SLM 利用に関する仕様文書を探すとき。
- agent call parameter、機能別 builder、完全プロンプトの構築順序、共通規範プロンプト、ファイルアクセス制限やルーティング規則の注入位置を確認したいとき。
- 設定値、ルートパスプレースホルダ、パス解決、規範文書の構造化、仕様文生成用 Markdown helper など、複数領域から参照される基礎概念の正本仕様断片を確認したいとき。

## Do not read this when
- realization code 側の実装詳細、外部コマンド起動、表示整形、diff 取得、レポート保存、対象ファイル探索、既存関数のシグネチャ、テスト期待値だけを調べたいとき。
- oracle file と realization file の一般的な定義、責務境界、編集権限、追跡対象判定、INDEX.md エントリー作成規則、品質基準だけを確認したいとき。
- Codex CLI 本体、git ignore、permission profile など、cmoc の正本仕様断片ではなく外部機能の一般仕様を調べたいとき。
- 読むべき個別仕様文書または oracle src がすでに分かっており、その本文へ直接進めばよいとき。

## hash
- 2980a42f8cc7d1b98f2fa597f06822e9973af16e720320d4004abfc8ff13421f

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
- cmoc の realization implementation を収める領域。Typer ベースの CLI 入口、利用者向けサブコマンド実装、共有 runtime helper、旧 import path を維持する互換層から構成される。
- サブコマンド固有の orchestration、共通 runtime 基盤、oracle src を複製しない再公開・委譲境界、既存公開参照の移行や削除条件を下位対象へ振り分ける入口になる。

## Read this when
- realization 側で CLI コマンド階層、サブコマンド実行本体、共通 runtime helper、設定・基本型・ACP・oracle package の互換 import 境界のどこを読むべきか判断したいとき。
- init、indexing、TUI、session、apply、review などの利用者向け CLI 挙動や、各サブコマンドから git、state、Codex 実行、INDEX.md maintenance、report 出力などの共通処理へどう接続しているかを追いたいとき。
- 複数 command から共有される runtime 処理、Codex 呼び出し、profile/config/content、error、git、logging、path、result、state、preflight、apply 補助などの実装所在を探したいとき。
- oracle src 側の正本実装を realization 側へ複製せず、旧来の公開 import path や module alias を維持している互換層の理由、接続先、移行範囲、削除条件を確認したいとき。

## Do not read this when
- oracle file に書かれた正本仕様、prompt 文面、agent call parameter の生成内容、path model、設定定義、構造化出力 schema そのものを確認したいとき。その場合は oracle 側の該当本文を読む。
- 特定の実行本体、共通 helper、互換入口など読むべき下位対象がすでに分かっているとき。この階層ではなく該当する下位対象へ直接進む。
- 生成済み INDEX.md の entry 内容や特定 directory のルーティング判断だけを確認したいとき。その場合は対象 directory の INDEX.md または対象本文を読む。
- 新しい API 仕様や正本仕様断片を追加する場所を探しているとき。realization implementation は正本仕様を述べる場所ではなく、既存仕様を具体化する実装領域である。

## hash
- e87b4025802d8bed83f63ed170ff7e997f9488cd6da30b84fa46e4c77b87915b

# `test`

## Summary
- CLI サブコマンド、Codex 実行ラッパー、ACP builder、prompt 組み立て、INDEX 更新、packaged import、StructDoc rendering など、cmoc の realization test を集めた領域。
- 一時 Git リポジトリや stub executable を使った外部挙動テストが中心で、session/apply/review/indexing/runtime の状態遷移、出力、失敗時挙動、import 境界を確認する入口になる。

## Read this when
- cmoc の realization implementation を変更し、対応する CLI 外部挙動や runtime 契約の回帰テストを探すとき。
- session fork/join/abandon、apply fork/join/abandon、review oracle、indexing、init、TUI、Codex runtime のテスト期待値を確認するとき。
- ACP builder、prompt parts、packaged layout import、StructDoc Markdown rendering の realization test を確認または修正するとき。
- テスト用の一時 Git リポジトリ、Codex home、fake external command、session/apply state helper などの共通テスト補助を探すとき。

## Do not read this when
- 本番実装の処理を変更したいだけで、外部挙動やテスト期待値を確認する必要がないときは、対応する implementation 側を読む。
- oracle file の正本仕様、oracle standard、realization standard、path placeholder の概念定義を確認したいときは、対応する oracle 側を読む。
- INDEX.md エントリーの自然言語生成規則やルーティング文書の正本仕様だけを確認したいときは、oracle 側の文書を読む。
- Codex CLI や LLM 自体の品質・出力内容を検証したいとき。この領域のテストは外部ツールを stub し、cmoc 側の制御を検証する。

## hash
- a59c8f9b01934b75e4990769554a7e0d2ca46ae513adda89a7a86cece14b89b7
