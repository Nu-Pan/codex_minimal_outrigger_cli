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
- cmoc の realization implementation を置く最上位領域で、CLI 入口、サブコマンド実装、共通 runtime 基盤、互換 import 層へ進むための起点。
- Typer の公開 CLI 面、各 workflow の制御層、Codex 実行・git・state・INDEX 更新などの共通処理、oracle src を複製しない再公開境界を扱う。
- 実処理は下位のサブコマンド領域や共通 runtime 領域に分かれ、正本仕様・prompt・基本型などは必要に応じて oracle 側の対応箇所を読む。

## Read this when
- cmoc の実装変更で、CLI 入口、サブコマンド実装、共通 runtime helper、互換 import 層のどこから読むべきか判断したいとき。
- 公開 CLI コマンド、option、Typer/Click エラー変換、console script 起動経路を確認または変更したいとき。
- apply、review、session、tui、indexing、doctor/init などのサブコマンド実行フローや下位処理への委譲先を探したいとき。
- Codex CLI 起動、git 操作、state、config、path、logging、error、content hash、INDEX 更新 preflight など複数サブコマンドから使われる runtime 基盤を扱うとき。
- oracle 側の正本実装を realization 側へ複製せず、既存の acp、basic、config、oracle、runtime 系 import 経路をどう維持しているか確認したいとき。

## Do not read this when
- oracle file の正本仕様、prompt 本文、parameter 生成内容、基本型、path model、設定定義そのものを確認したいだけなら、oracle 側の対応箇所を読む。
- 生成済み INDEX.md の個別 entry 内容や特定 directory のルーティング判断だけを確認したい場合は、その directory の INDEX.md または対象本文を読む。
- ログ、設定、state、schema、call log、report など生成済みファイルの内容調査が目的で、実装を変更しないとき。
- 対象が既に特定のサブコマンド、runtime helper、互換 wrapper、builder 実体に絞れている場合は、この階層全体ではなく該当する下位対象を直接読む。

## hash
- 8d125a55b888137347ff4912873917123a649acdee0b5c687db5e742cf5cb26d

# `test`

## Summary
- cmoc の realization test 群を置くディレクトリ。CLI サブコマンド、Codex runtime、ACP builder、prompt rendering、packaged import、session/apply/review/indexing/doctor などの外部挙動と回帰観点を、共有テスト支援部品と各機能別テストに分けて扱う。
- 本番実装や oracle file の正本仕様ではなく、realization 側の挙動が現行仕様と既存制御に沿っているかを確認する入口となる。

## Read this when
- cmoc のテスト全体から、変更対象に対応する realization test や共有テスト helper を探したいとき。
- CLI の終了コード、stdout/stderr、report、state 更新、git worktree/branch 副作用、Codex 呼び出し、INDEX 更新、doctor 修復などの回帰テストを確認・変更したいとき。
- apply、session、review oracle、indexing、doctor、tui、Codex runtime、ACP builder、prompt parts、packaging import のどのテストへ進むべきかを判断したいとき。

## Do not read this when
- 本番実装の責務分割、低レベル helper、設定型、Git 操作、Codex 実行 wrapper そのものを確認したい場合は、対応する src 側を読む。
- oracle file の正本仕様、oracle/realization の概念定義、INDEX.md 生成規則、path model の根拠を確認したい場合は、oracle 側の該当文書または実装を読む。
- 個別テストファイルが既に特定できており、その期待値だけを確認したい場合は、このディレクトリ入口ではなく該当テストを直接読む。

## hash
- 4a6f38a44e875c15738c05c8bd11f07161c50e4e1cc5cf9a812620729936a7b0
