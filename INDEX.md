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
- cmoc の正本仕様断片を置く領域。自然言語仕様、agent call の入力契約・プロンプト・設定・パスなど、realization file が従う人間意図の確認入口になる。
- 外部仕様や横断仕様を自然言語文書から探す場合と、AI agent call や共通規範プロンプトなどの基礎概念を実装形式の正本仕様断片から探す場合の分岐点になる。

## Read this when
- cmoc の実装・テストを始める前に、正本仕様断片から読むべき領域を選びたいとき。
- CLI 挙動、サブコマンド、状態遷移、ログ、エラー処理、Codex CLI 連携などの外部仕様や横断仕様を確認したいとき。
- session fork/join、run worktree、managed branch など、cmoc の git branch・commit・worktree モデルを確認したいとき。
- Python 実装、CLI 構成、開発環境、pytest を中心としたテスト規約など、realization code や realization test の書き方に関わる正本仕様断片を確認したいとき。
- AI agent call のパラメータ、Structured Output schema、モデル設定、ファイルアクセス権限、preflight、共通規範プロンプト、リポジトリ別設定、パスプレースホルダなどの基礎概念を確認したいとき。

## Do not read this when
- 正本仕様断片ではなく、現在の realization implementation や realization test の具体的なコード本文だけを調べたいとき。
- oracle file と realization file の一般的な責務境界、編集責任、INDEX.md エントリー作成規則だけを確認したいとき。
- パスキーワードの定義そのものだけを確認したいとき。
- 採用済み仕様ではなく、実装上の関数、クラス、内部 helper、テスト構造を直接調べたいとき。

## hash
- d6bca67183766fdd91f227ce006e85a31474238beb83b6c7482690c59e49b7aa

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
- 正本側の実装を複製せず利用する互換層、CLI 入口、共通 runtime helper、利用者向けサブコマンド実装を束ねる realization implementation 領域。
- 旧来の公開 import 経路を canonical 実装へ委譲する薄い入口と、コマンド実行を共通処理やサブコマンド単位の orchestration へ接続する入口を探すための上位ルーティング対象。
- 設定、基本型、agent call parameter、実行時支援、エラー表示、状態管理、indexing、apply、review、session、TUI などの実装側責務へ進む起点になる。

## Read this when
- realization 側の実装入口を選び、互換 import、CLI 起動、共通 runtime、サブコマンド実行のどこへ進むべきか判断したいとき。
- 正本側実装を複製せず再公開している import 経路、公開名維持、移行理由、削除条件を調べたいとき。
- CLI コマンド構成、引数解析エラー変換、console script から各実行本体への委譲関係を確認したいとき。
- 複数のコマンドから使われる Codex 呼び出し、preflight、config、hash、doctor、error、git、logging、path、result、session state、process 管理などの共通 runtime 挙動を確認または変更したいとき。
- 利用者向けサブコマンドの上位制御、状態遷移、出力、失敗時処理、cleanup、report 生成の実装先を探したいとき。

## Do not read this when
- oracle file に書かれた正本仕様、人間意図、prompt、出力条件、型定義、設定構造そのものを確認したいとき。対応する oracle 側本文を読む。
- 個別の共通定義や helper の詳細だけを確認したい対象が既に分かっているとき。該当する定義元または実体 module へ直接進む。
- 生成済みルーティング文書の個別 entry 内容や、特定対象を読むべきかだけを判断したいとき。対象階層のルーティング情報または本文を読む。
- 新しい公開 API、設定項目、サブコマンド、状態ファイルを設計する入口を探しているだけで、既存 realization 実装の互換維持や実行制御が論点ではないとき。
- 実装ではなく repository 全体の方針、oracle と realization の責務境界、INDEX entry 作成規則を確認したいとき。該当する正本仕様断片を読む。

## hash
- 60d8da97e70cc4e8307a546bda52deabddb48b948b44f058157be22de62168a8

# `test`

## Summary
- CLI と runtime の realization test 群をまとめるテスト領域。apply/session/review/indexing/doctor/TUI/Codex 実行などの外部挙動、共通 runtime 契約、prompt・ACP builder・packaging 境界、テスト補助関数への入口になる。
- 多くのテストはサブコマンド単位または runtime 境界単位に分かれており、CLI 出力、状態遷移、Git worktree/branch、Codex 呼び出し、INDEX 更新、schema 参照などを実装変更時に確認するための回帰検証を担う。

## Read this when
- CLI サブコマンドや Codex 実行基盤、runtime 共通契約、indexing、prompt、ACP builder、packaging 境界の外部挙動を変更し、対応する realization test の入口を選びたいとき。
- apply fork/join/abandon、session fork/join/abandon、review oracle、doctor、TUI、Codex retry/quota/home/exec、INDEX 更新の成功・失敗条件や state/worktree/branch の期待を確認したいとき。
- テスト用 Git リポジトリ、Codex home、fake executable、doctor 実行、apply worktree 解決など、CLI テストで共有される fixture や補助関数を探したいとき。
- 実装変更に対して、どの外部挙動テストや回帰テストを読むべきかを同階層のテスト群から絞り込みたいとき。

## Do not read this when
- oracle file の正本仕様や oracle standard の根拠を確認したい場合は、oracle 配下の該当文書または oracle src を読む方がよい。
- 個別実装 helper の内部構造だけを調べたい場合で、外部 CLI 挙動や回帰期待を確認する必要がないなら、対応する実装ファイルを直接読む方がよい。
- Codex CLI や LLM の出力品質そのものを評価したい場合は、このテスト領域の主目的ではない。
- INDEX.md エントリー生成規則や routing document の自然言語内容だけを調整したい場合は、indexing の仕様文書や該当実装を読む方がよい。

## hash
- f80b416acac77f71ae4ff6c97bad70f22c6abd0e3b43bba7997a8838149dd876
