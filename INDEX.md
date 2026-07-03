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
- cmoc の正本仕様断片へ進むための入口。自然言語で書かれた仕様判断と、AI agent call・prompt・設定・パス表記・構造化文書モデルなどの正本実装断片を扱う領域を切り分ける。
- アプリケーション全体の外部挙動、branch / worktree モデル、不採用案、開発時の横断規則を探す場合と、agent call parameter、完全プロンプト、Structured Output schema、設定、パス解決、Markdown 整形 helper の正本断片を探す場合の起点になる。

## Read this when
- cmoc の利用者向け挙動、サブコマンド仕様、ログ、エラー処理、補完、Codex CLI 呼び出し、Structured Output、retry / resume、run 隔離、セッション状態、apply / fork / join などに関する正本仕様断片を探すとき。
- session branch、run branch、linked worktree、cmoc-managed branch、fork / join commit など、git branch・commit・worktree に関する cmoc 用語と責務を確認したいとき。
- 機能や workflow の追加時に、採用しなかった設計案とその理由、または Python 実装・CLI 構成・共通処理配置・開発環境・依存追加・pytest による決定論的テストなどの共通開発規則を確認したいとき。
- AI 呼び出しで使う role、summary、goal、prompt 断片、placeholder、モデル設定、reasoning effort、file access mode、出力契約を正本仕様断片から確認または変更したいとき。
- 完全プロンプトの構成順序、静的・動的 prompt 部品、file access rule、routing rule、各種 standard の prompt 注入責務を切り分けたいとき。
- cmoc の設定項目、既定値、永続化境界、リポジトリ別の挙動設定、ルート概念、プレースホルダ付きパス、絶対パス、git worktree との関係を確認したいとき。
- 規範文書を構造化して保持するモデルや、階層化された文章を Markdown として整形する helper を確認したいとき。

## Do not read this when
- oracle file と realization file の一般的な責務分担、編集権限、品質基準、INDEX.md エントリー作成基準そのものだけを確認したいとき。
- 実装モジュール、テスト、helper 分割、既存関数、現在のテスト期待値など、realization 側の具体的なコード構造だけを調べたいとき。
- CLI 引数解析、git 操作、branch 操作、作業レポート保存、結果集約、表示処理など、サブコマンド全体の実行フローを調べたいとき。
- agent call のプロセス起動、バックエンドが受理する具体的なモデル名への変換、結果処理、エラー処理を調べたいとき。
- 設定の読み書き処理、JSON 変換処理、初期化処理など、正本仕様断片ではなく realization 側の実装箇所を探しているとき。
- 特定サブコマンドや特定の仕様断片の読む先が既に分かっており、その本文から実装・テスト判断を行うだけのとき。
- 採用済み仕様ではなく実装都合だけを確認したいとき、または Codex CLI や LLM の実際の応答品質そのものを評価したいとき。

## hash
- e736f7ceac096827579e6ccadccce183c44810ac9642fb0870fc69a254c73d9a

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
- cmoc の realization implementation を収める実装ルート。CLI 公開入口、サブコマンド実行本体、共通 runtime helper、oracle src への互換 import 境界を扱う。
- 正本仕様断片そのものではなく、oracle 側 canonical 実装や oracle doc の意図を実行可能な CLI・runtime・互換層として具体化する領域。
- 内部は、利用者向け CLI routing、session・apply・review・index maintenance などの orchestration、複数サブコマンドから共有される helper、旧公開 import path の再公開層に分かれる。

## Read this when
- cmoc の実装本体を確認または変更したいとき。
- CLI コマンド構成、サブコマンドの実行フロー、共通 runtime 処理、git・state・logging・path・Codex 呼び出し周辺の実装入口を探したいとき。
- oracle src の定義を realization 側へ複製せず、既存公開 import path や package path をどう維持しているか確認したいとき。
- 個別機能の実装へ進む前に、CLI 入口、サブコマンド本体、共通 helper、互換層のどこを読むべきか切り分けたいとき。

## Do not read this when
- 正本仕様断片、人間意図、prompt・parameter・設定・path model・INDEX.md 生成規則などの仕様そのものを確認したいだけのときは、oracle 側の対応する doc または src を読む。
- 自動テストの期待挙動やテスト fixture を確認したいときは、test 側を読む。
- 実行ログ、生成済み成果物、管理用メタデータ、作業メモを探しているときは、この実装ルートではなく該当する管理領域を確認する。
- 旧 import path の互換維持と無関係に、新しい正本仕様や API 仕様を追加する場所を探しているときは、まず oracle 側の仕様断片を検討する。

## hash
- bc1c3618256ce933bb7bb72357c1e557cd01ef806f9eb2d513e7ac298ddd6933

# `test`

## Summary
- CLI 外部挙動と共通 runtime 境界を中心に、cmoc の realization test をまとめるディレクトリ。
- apply、session、init、TUI、Codex 実行、indexing、review oracle、prompt builder、packaging、StructDoc rendering など、ユーザー向け挙動や制御ロジックの回帰確認への入口になる。
- 一時 Git リポジトリ、fake Codex、fake profile、state fixture など、複数テストで共有される補助処理も含む。

## Read this when
- CLI サブコマンドの終了コード、標準出力、Git branch/worktree 操作、state 更新、report 生成などの外部挙動を確認・変更するとき。
- Codex CLI/TUI 呼び出し、CODEX_HOME、profile、sandbox/file access mode、retry、quota wait、file access violation recovery などの runtime 回帰を確認するとき。
- INDEX 生成・更新、indexing preflight、routing document 更新 workflow、review oracle、prompt parts、ACP builder parameter、packaged import のテストを探すとき。
- realization/oracle file 判定、tracked ignored file、memo、管理ディレクトリ、binary、INDEX/AGENTS の扱いが CLI 挙動にどう反映されるか確認するとき。
- テスト用 Git repository、fake executable、fake Codex home、session/apply state helper など、CLI テスト共通 fixture を確認・変更するとき。

## Do not read this when
- プロダクト実装の責務分割、内部 helper の詳細、設定や state の実装を直接変更したい場合は、対応する実装側へ進む。
- oracle file の正本仕様本文、schema、path model、file access rule、prompt 正本文言そのものを確認・変更したい場合は、oracle 側を読む。
- 個別の CLI サブコマンドや builder のテスト期待値だけを確認したい場合は、この階層全体ではなく該当するテスト本文へ直接進む。
- LLM 出力品質や外部ツールそのものの品質を検証したい場合は、この realization test 群の対象外。

## hash
- 9ff4c25f39b6e88c689c7baaa923ac42620c7c38868e05477d15a0e97cc293f3
