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
- cmoc の realization implementation を置く領域で、CLI 入口、サブコマンド実装、共通 runtime helper、設定・基本型・ACP・oracle import の互換層を含む。
- 利用者向け command から、apply/review/session などの上位制御、複数サブコマンドで共有される runtime 支援、旧 import path を正本側実装へ中継する最小適応層へ進む入口になる。
- oracle src の正本定義を複製せずに再公開・委譲する互換 module と、realization 側で実際の CLI 挙動を担う実装 module の両方を収める。

## Read this when
- cmoc の実装側で、CLI entrypoint、subcommand、runtime helper、互換 import 層のどこを読むべきか判断したいとき。
- session、apply、review、init、doctor、indexing、tui などの利用者向けコマンド実装や上位制御の入口を探したいとき。
- 複数サブコマンドから共有される Codex 呼び出し、設定、profile、git、path、logging、state、error、INDEX 更新 preflight などの runtime helper を調べたいとき。
- 旧 `acp.*`、`basic.*`、設定参照経路、`oracle.*`、古い runtime import path など、realization 側に残る互換 import がどの正本側または実体 module へつながるか確認したいとき。
- oracle 側実装を正本に保ちながら realization 側で再公開、型変換、package path 接続、module alias をどう補っているか調べたいとき。

## Do not read this when
- oracle file に書かれた正本仕様、人間意図、prompt、出力条件、基本型、path placeholder、設定定義、構造化出力 schema を確認したいとき。oracle 側の該当文書や定義を読む。
- 生成済み INDEX.md の個別 entry 内容、実行済みログ、特定 directory のルーティング判断だけを確認したいとき。runtime helper や CLI 実装の変更を伴わないなら対象外。
- 特定のサブコマンド本体、共通 runtime helper、互換 module のどれを読むべきか既に分かっているとき。該当する下位対象へ直接進む。
- 新しい公開 API、設定項目、CLI option、状態ファイルを追加する設計だけが目的のとき。まず対応する oracle file で必要性を確認する。

## hash
- 5567b1d02db6ea9a7a69df9fa1ebc9a34de87e3309fd3dca2c549f35f685be38

# `test`

## Summary
- cmoc の realization test を収めるディレクトリ。CLI サブコマンド、Codex runtime、ACP builder、prompt 組み立て、packaged import、StructDoc rendering など、実装が外部挙動・状態遷移・import 境界を満たしているかを検証する入口になる。
- 共通テスト補助も含み、一時 Git リポジトリ、Codex home、fake external command、session/apply state などを使う統合寄りの回帰テストを探す起点になる。

## Read this when
- cmoc の realization implementation を変更し、その変更が既存の CLI 外部挙動、runtime 契約、状態遷移、ログ、git 操作、Codex 呼び出し、または import 境界に影響するか確認したいとき。
- apply、session、review oracle、indexing、init、tui、doctor などのサブコマンドについて、成功時・失敗時の出力、cleanup、commit、worktree、branch、state 更新の期待値を確認したいとき。
- Codex exec/TUI runtime の profile、sandbox、CODEX_HOME、retry、quota retry、post validation、subprocess tracking、ログ出力の回帰テストを探すとき。
- ACP builder、prompt parts、Structured Output schema 参照、packaged layout import、Markdown rendering など、CLI より下位の共通契約をテストから確認したいとき。
- 新しいテストを追加する前に、同じ観点を既存の realization test へ統合できるか確認したいとき。

## Do not read this when
- 正本仕様断片そのもの、oracle file の定義、標準文書、schema の正本文言を確認したいときは、oracle 側の対象を読む。
- 本番実装の処理を局所的に変更したいだけで、外部挙動や回帰テストの期待値をまだ確認する段階ではないときは、対応する implementation 側を先に読む。
- INDEX.md エントリー生成規則や routing 文書の一般標準だけを確認したいとき。
- Codex CLI や LLM の出力品質そのものを評価したいとき。このディレクトリのテストは外部ツールを stub し、cmoc 側の制御を検証する。

## hash
- a6642bc9c9743382932109b6e2a9f70ed3edf17b1bcd4a4465ae5ec7fca56171
