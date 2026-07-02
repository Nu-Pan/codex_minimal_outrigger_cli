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
- cmoc の realization implementation を収める実装ルート。CLI 最上位入口、サブコマンド実行制御、共通 runtime helper、互換 import 層、oracle 側正本実装への橋渡しが並ぶ。
- 公開 CLI の構成を確認する入口、個別サブコマンドへ進む入口、複数経路で共有される runtime 実装へ進む入口、旧 import path 互換層の残置理由や削除条件を切り分ける階層。

## Read this when
- cmoc の実装領域で、CLI 入口、サブコマンド、共通 runtime、互換 import 層のどこへ進むべきかを選びたいとき。
- 公開 CLI コマンド構成、Typer app、console script 起動、引数解析エラー表示、サブコマンド委譲先を確認または変更したいとき。
- init、indexing、tui、apply、session、review など、利用者向けサブコマンドの実行順序、preflight、状態更新、git 操作、Codex 連携、出力処理を追いたいとき。
- Codex 実行、設定、Git、ログ、パス、状態、INDEX.md 更新など、複数サブコマンドから使われる共通 runtime 処理の所在を探したいとき。
- acp.*、basic.*、config、oracle.*、古い runtime module などの互換 import 経路が、正本側実装または実体 module へどう委譲されているかを確認したいとき。

## Do not read this when
- oracle file にある正本仕様断片、prompt 正本文面、path model、設定定義、INDEX.md エントリー標準などの人間所有仕様を確認したいときは、対応する oracle doc または oracle src を読む。
- 対象の下位領域がすでに決まっている場合は、この階層ではなく該当する実装ファイルまたは下位ディレクトリへ直接進む。
- 生成済みログ、状態ファイル、設定ファイルなどの実データを調査したいだけのとき。この階層はそれらを扱う実装への入口である。
- 互換 import 経路や CLI/runtime 実装に関係しない新しい仕様判断だけをしたいときは、正本仕様側または該当する設計対象を読む。

## hash
- 5cc6fdd4513e8dd11d58697c2feae17c57961b5d0b05e33fefdbee7be0510477

# `test`

## Summary
- cmoc の realization test をまとめるディレクトリ。CLI サブコマンド、Codex runtime、prompt builder、ACP builder、packaged import、StructDoc rendering など、実装の外部挙動と共通実行前提を検証する入口になる。
- apply/session/indexing/review oracle/init/TUI/Codex 実行層などの機能別テストと、テスト用 Git repo・Codex home・fake executable などの共通補助関数を同階層に置き、変更対象に応じて該当テストへ進むための上位ルーティングを担う。

## Read this when
- cmoc の実装変更後に、どの realization test が外部挙動・状態遷移・git 副作用・prompt/schema 契約を検証しているかを探すとき。
- apply fork/join/abandon、session fork/join/abandon、indexing、review oracle、init/TUI、Codex runtime の CLI 境界テストへ進む入口を探すとき。
- ACP builder、prompt parts、packaged import、StructDoc markdown rendering など、CLI 本体より下位の builder/import/rendering 契約を検証するテストを探すとき。
- 一時 Git リポジトリ、Codex home、fake Codex/Python executable、apply worktree path など、CLI テスト共通 fixture や helper の置き場を確認したいとき。

## Do not read this when
- oracle file の正本仕様、oracle/realization 標準、routing 規則そのものを確認したい場合は、oracle 側の文書を読む。
- 実装内部の関数分割、型定義、低レベル helper の詳細を変更したいだけなら、対象の実装モジュールを先に読む。
- 特定サブコマンドの仕様本文ではなくテスト観点が不要な場合は、このディレクトリではなく該当する oracle doc または implementation を読む。
- Codex CLI や LLM の出力品質そのものを評価したい場合は、この realization test 群ではなく、呼び出し制御や外部副作用を検証する範囲に限定して読む。

## hash
- 359dae77d7c8fe362ec87c1d249000dc017a4bd4df213abafe4b80d5c911382d
