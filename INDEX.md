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
- cmoc の realization implementation を収める領域。CLI 入口、サブコマンド実装、共通 runtime helper、oracle src への互換 import 境界、既存公開 import path の再公開層を扱う。
- 正本仕様断片そのものではなく、oracle 側の意図を具体化する実装と、旧 import 経路を正本側または実体側へ接続する互換層へ進むための入口。
- 個別サブコマンドの実行制御、共通処理、設定・基本型・ACP builder などの互換公開面、top-level CLI 登録の読む先を切り分けるための階層。

## Read this when
- cmoc の実装本体を調べる起点を探しているとき。
- CLI の公開コマンド構成、サブコマンド登録、引数解析エラーの扱い、console script からの起動入口を確認または変更したいとき。
- init、indexing、tui、apply、review、session などのサブコマンド実行順序、状態遷移、git 操作、Codex 呼び出し、report 生成へ進む入口を探したいとき。
- 複数サブコマンドで共有される runtime helper、共通データ型、logging、path 解決、config/state 永続化、git 境界、agent call 周辺の共通実行制御を確認または変更したいとき。
- oracle src の正本実装を realization 側へ複製せず、既存公開 import path、再 export、module alias、package path 接続、公開型への最小変換で互換性を保つ境界を確認したいとき。
- 設定、基本型、path model、構造化文書 API、ACP builder などについて、正本側または実体側への委譲経路と互換層の削除条件を調べたいとき。

## Do not read this when
- oracle file、path model、INDEX.md 生成規則、prompt builder、設定定義などの正本仕様断片や人間意図を確認したいだけなら、対応する oracle 側の文書または実装を読む。
- テストの期待挙動、fixture、外部挙動の検証観点を確認したいだけなら、realization test 側を読む。
- 生成済みログ、実行履歴、作業メモ、git 内部状態の内容確認が目的で、実装を変更しないとき。
- 特定の責務別 helper や個別サブコマンドの場所がすでに分かっているなら、この階層全体ではなく該当する下位対象を直接読む。
- 新しい正本仕様や API 仕様を追加する場所を探しているとき。この領域は realization implementation と互換接続境界であり、正本仕様の追加場所ではない。

## hash
- e350a91f94bc8d6ceb3adf45f76865c33d810cee4243635a740dd799fdc1191e

# `test`

## Summary
- CLI 外部挙動と runtime 境界を検証する realization test 群。init/TUI、session、apply、review oracle、indexing、Codex runtime、prompt 構築、packaged import、StructDoc rendering などの回帰観点へ進む入口になる。
- 共通支援コードも含み、一時 Git リポジトリ、fake Codex/CODEX_HOME、session/apply state、linked worktree などを使った統合的なテスト文脈を扱う。

## Read this when
- CLI サブコマンドの終了コード、stdout/stderr、Git branch/worktree/state、report、cleanup、拒否条件など、利用者から見える挙動のテストを探すとき。
- Codex CLI/TUI 実行 wrapper、file access rule、quota/capacity retry、CODEX_HOME、sandbox profile、call log など runtime 境界の回帰テストを確認・変更するとき。
- apply fork/join/abandon、session fork/join/abandon、review oracle、indexing preflight/update など、複数ファイル・Git 状態・agent call が絡むワークフローの期待値を確認するとき。
- prompt parts、ACP builder parameter、packaged import、StructDoc Markdown rendering のような、実装モジュールの公開契約や出力整形に対応する realization test を探すとき。
- テスト用の Git fixture、fake executable、fake Codex profile、session state から worktree を解決する補助関数を確認・変更するとき。

## Do not read this when
- 正本仕様断片そのものを確認・変更したい場合は、oracle 側の対象本文を読む。
- プロダクト実装の責務分割、低レベル helper、状態管理、Git 操作、Codex 実行処理の実装詳細だけを調べたい場合は、対応する implementation を直接読む。
- 個別テストの assertion や fixture ではなく、ルーティング文書の記述規則や INDEX.md entry の自然言語内容だけを設計したい場合は、関連する oracle 文書や indexing 実装を読む。
- CLI や runtime の外部挙動に影響しない局所的な内部整理だけが目的で、既存の小さい単体テストや対象実装を直接読める場合。

## hash
- fabc8cf82eb71fb564a22fe5927e3246f4014c0315c61a1b41a68b8da4a94f63
