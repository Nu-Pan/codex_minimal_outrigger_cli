# `AGENTS.md`

## Summary
- cmoc 開発時のリポジトリ共通ルールを定める。略称、パス表記、ルーティングの前提、閲覧・編集禁止領域、正本仕様断片と実装・テスト配置の基本方針を扱う。
- 作業開始時に正本仕様断片を起点として読み、必要に応じてルーティング情報をたどり、正本仕様断片と実装が乖離する場合は実装を合わせるという判断基準を示す。

## Read this when
- cmoc リポジトリで作業する前に、共通の作業規則、禁止領域、正本仕様断片と実装の関係を確認したいとき。
- パス表記の意味、ルーティング文書の使い方、正本仕様断片を読む順序を確認したいとき。
- 実装やテストをどこに置くべきか、正本仕様断片と実装のどちらを修正対象にすべきかを判断したいとき。

## Do not read this when
- 特定機能の詳細仕様、CLI の具体的な挙動、テストケースの期待値を確認したいときは、正本仕様断片または対象領域の本文へ進む。
- 特定ファイルの責務や読むべき下位対象を探したいだけなら、その階層のルーティング情報を読む。
- 実装内部の具体的な関数、クラス、制御フローを調べたいときは、実装またはテストの対象ファイルを読む。

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
- cmoc の正本仕様断片を集める領域。自然言語で書かれた仕様、正本実装、正本テストを通じて、人間意図、外部挙動、責務境界、AI agent call 入力契約、共通規範、パス表記、構造化文書モデルなどを確認する入口になる。
- 実装・テストへ反映すべき仕様根拠を探す際に、自然言語文書へ進むか、prompt・設定・schema・共有モデルなどの正本実装へ進むかを切り分けるための上位ルーティングを担う。

## Read this when
- cmoc の realization code を追加・変更する前に、根拠となる正本仕様断片を探すとき。
- 公開 CLI 挙動、状態・ログ・インデックス生成、agent call 境界、実行環境管理、branch/worktree モデル、開発作法など、人間意図として固定された仕様を確認したいとき。
- AI エージェント呼び出し時の prompt、Structured Output schema、モデル設定、ファイルアクセス権限、preflight、共通規範プロンプトなど、実装へ反映する入力契約や出力契約を確認したいとき。
- cmoc 全体で共有される設定値、パス表記、規範文書の構造化、Markdown rendering helper など、複数領域から参照される基礎仕様断片を探すとき。

## Do not read this when
- 正本仕様断片ではなく、realization implementation や realization test の具体的な関数構造、内部 helper、実行制御実装だけを調べたいとき。
- 設定ファイルの読み書き、JSON 変換、init 処理、バックエンド API への実リクエスト、agent CLI 実行処理など、実装側アルゴリズムだけを確認したいとき。
- oracle file と realization file の一般的な定義、責務境界、記述標準、INDEX.md エントリー作成規則だけを確認したいとき。
- パスキーワードやルート種別の定義そのものだけを確認したいとき。

## hash
- 46573c8d7a6258d7cb4fc8a05d19fe2b1810aea02b5e6ae48561822476f9a9cf

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
- cmoc の realization implementation 全体の入口。CLI 公開面、サブコマンド実行本体、共通 runtime helper、設定・基本型・ACP・oracle package への互換 import 層を含み、oracle 側の正本仕様断片を複製せず実装へ接続する領域。
- トップレベル CLI から各機能の orchestration、共通実行基盤、旧 import path の維持・移行条件までをたどるための上位ディレクトリであり、詳細確認では下位の責務別対象へ進む。

## Read this when
- cmoc の realization implementation で、CLI 入口、サブコマンド本体、共通 runtime helper、互換 import 層のどこへ進むべきか判断したいとき。
- トップレベルコマンドから apply、review、session、doctor、indexing、tui などの実行本体や共通処理への接続関係を確認したいとき。
- oracle 側実装を正本に保ったまま、realization 側で既存公開 import path、再公開、module alias、runtime path 接続をどう維持しているか調べたいとき。
- 旧来の公開参照や互換入口を canonical 実装へ移行する作業で、残存理由、影響範囲、削除条件を絞り込みたいとき。
- Codex 起動、config、git、path、state、logging、error、INDEX 更新 preflight、apply process 管理など、複数サブコマンドにまたがる実行基盤の読む先を探したいとき。

## Do not read this when
- oracle file にある正本仕様断片、prompt、出力条件、設定定義、path model、構造化出力 schema そのものを確認したいとき。対応する oracle 側の文書または実装を読む。
- 生成済み INDEX entry、実行済み log/report、特定 session の状態内容だけを確認したいとき。実装変更が目的でなければ対象の成果物や状態を直接確認する。
- 個別の低レベル helper、サブコマンド詳細、または互換 import 層だけを調べる対象が既に分かっているとき。該当する下位対象へ直接進む。
- 新しい公開 API、CLI 引数、設定項目、状態ファイルを追加する設計だけが目的で、既存実装・互換入口・共通基盤の残存理由を確認しないとき。

## hash
- 6022c666395b33cc972fd24d26eaec41c9b8cb8b5eb6fc914aa78c92b85f2b2c

# `test`

## Summary
- cmoc の realization test 群を置く領域。CLI サブコマンド、Codex 実行 runtime、ACP builder、prompt 組み立て、INDEX 更新、packaged import、構造化 Markdown rendering など、実装の外部挙動と共通 runtime 契約を検証する入口になる。
- 一時 Git repository、fake Codex/Ollama/systemctl、Codex home/profile、Typer runner、worktree/state 操作など、複数テストで共有される支援処理もこの領域に含まれる。

## Read this when
- cmoc の realization implementation を変更した後、その変更に対応する既存テストの期待値、fixture、外部挙動の境界を確認・更新したいとき。
- session、apply、review、indexing、doctor、TUI、Codex runtime などの CLI 経路について、終了コード、標準出力、report、state、branch/worktree cleanup、git 副作用を検証するテストを探すとき。
- Codex 呼び出し時の file access mode、sandbox、profile、schema、retry、quota retry、ログ、linked worktree、Codex home の扱いをテスト側から確認したいとき。
- ACP builder、prompt parts、structured output schema 参照、oracle src 参照方針、packaged import 境界など、実装と正本仕様断片の接続を realization test で確認したいとき。
- テスト用 repository、fake 外部コマンド、tracked ignored file、Codex profile、apply worktree path などの共有 fixture を再利用または変更したいとき。

## Do not read this when
- oracle file の正本仕様そのもの、oracle/realization file の定義、標準文書の本文を確認したいときは、対応する oracle 側の文書または実装を読む。
- 本番実装の制御ロジック、helper 分割、型定義、path model、永続状態処理を先に理解したいときは、対応する realization implementation を直接読む。
- 個別サブコマンドと無関係な一般的な設計方針や INDEX.md エントリー生成規則だけを確認したいとき。
- Codex CLI や LLM の出力品質そのものを評価したいとき。この領域のテストは fake 実行や制御ロジック検証を中心に扱う。

## hash
- f68f90312fd8c8fd82342a883a99b26b906139afba975994c7f4fbd0f91ac9f3
