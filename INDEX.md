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
- cmoc の正本仕様断片全体への入口。人間が所有する自然言語仕様、AI agent 呼び出し契約や標準プロンプトを定義する実装形式の仕様断片、正本性・実現物との関係を確認するための領域である。
- 利用者向け CLI 挙動、run/session/branch/worktree モデル、開発規則、non-goal、AI 呼び出しパラメータ、Structured Output schema、標準文書生成、共有データ構造など、realization file を正本仕様断片に沿わせるための根拠を探す起点になる。
- 下位には、自然言語で仕様判断を読む領域と、プロンプト・schema・設定・共有モデルを実装形式で読む領域があり、作業内容が公開挙動や設計判断なのか、AI 呼び出し契約や生成形式なのかで読む先を切り分ける。

## Read this when
- cmoc の仕様根拠を oracle file から確認し、realization implementation や realization test をどの意図に合わせるべきか判断したいとき。
- CLI の外部挙動、状態・ログ・出力、run 隔離、agent call 境界、session fork / join、branch / worktree 用語、開発規則、採用しない設計案の理由を確認したいとき。
- AI agent に渡す role、summary、goal、標準プロンプト、権限、モデル品質区分、reasoning effort、Structured Output schema、設定、パス表記、規範データ構造の正本仕様断片を確認したいとき。
- oracle file と realization file の関係、正本仕様断片として守るべき公開面・保存先・失敗時挙動・責務分担、または標準文書やルーティング規則がどうプロンプト化されるかを確認したいとき。

## Do not read this when
- 既存実装の具体的な関数、クラス、helper、git 操作、状態ファイル処理、外部プロセス起動、テスト期待値だけを調べたいときは、realization implementation または realization test を読む。
- 対象が自然言語仕様または実装形式の AI 呼び出し契約のどちらかに絞れているときは、この領域全体ではなく該当する下位領域へ直接進む。
- 個別の prompt builder、AgentCallParameter builder、schema、設定モデル、パスモデル、規範モデルなど、読むべき下位対象がすでに分かっているときは、その対象を読む。
- INDEX.md エントリー生成の一般基準、oracle file の正本性、realization file の編集責務など、提示済みの共通標準だけで判断でき、対象本文の仕様断片を追加で確認する必要がないとき。

## hash
- 4841c324d9619d505ed501af9f1d5ed78c83063821303c3727e251e92d9dee76

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
- cmoc の realization implementation 全体を置く領域。最上位 CLI の Typer entrypoint、利用者向けサブコマンド本体、サブコマンド間で共有される runtime helper、Codex CLI/TUI 実行、git・path・state・logging・INDEX maintenance などの実装基盤を扱う。
- 正本側にある ACP builder、基本型、設定、path model、構造化文書 API、oracle package へ到達するための互換 shim や再公開層も含み、旧来 import path を保ちながら実体を oracle 側または下位実装へ委譲する公開境界として機能する。
- cmoc の実行挙動を実装側から追うための入口であり、上位では CLI 構成・互換境界・共通 runtime・サブコマンド orchestration のどこへ進むべきかを切り分け、詳細は各下位領域または正本側実装へ進む。

## Read this when
- cmoc の CLI コマンド構成、サブコマンド登録、option の受け口、console script 起動、または CLI 引数解析エラーの cmoc 形式表示を確認・変更したいとき。
- init、indexing、tui、session、apply、review など、利用者向けサブコマンドが実行時にどの実装へ入り、git/worktree/state/Codex 実行/利用者向け出力へどうつながるかを追いたいとき。
- Codex CLI exec や TUI 起動、profile・sandbox・CODEX_HOME・cwd・call log・stdout/stderr・quota/capacity retry・Structured Output 検証など、サブコマンド共通の実行基盤を確認したいとき。
- INDEX.md の maintenance 実装について、更新対象探索、既存エントリー再利用、hash 鮮度判定、Codex へのエントリー生成依頼、commit までの realization 側制御を調べたいとき。
- git wrapper、path 解決、設定同期、content hash、runtime state 永続化、cmoc 共通例外、logger、外部コマンド結果など、複数の実行経路から共有される helper を探したいとき。
- realization 側に残る ACP builder、基本型、設定、oracle package への互換 import path や再公開境界を確認し、削除条件や移行先を判断したいとき。

## Do not read this when
- 正本仕様断片そのもの、app spec、path model の概念定義、oracle standard、prompt builder の正本実装、設定定義の正本を確認したいときは、oracle 側の該当本文を読む。
- 実装に対する期待値、fixture、テスト観点、回帰検証を確認・変更したいときは、realization test 側を読む。
- ACP 型、構造化文書、設定、path model、AgentCallParameter builder の実体定義や仕様意図だけを確認したいときは、互換再公開層ではなく正本側または該当 builder 本体へ進む。
- README、AGENTS、bin、pyproject など、実装本体ではない利用者向け説明、作業規則、起動スクリプト、パッケージ設定だけを確認したいときは、この領域ではなく該当する補助ファイルを読む。
- 特定サブコマンドの利用者向け workflow だけを知りたい段階で、共通 runtime や互換 shim の詳細まで読む必要はない。まずサブコマンド入口または oracle 側仕様から読む先を絞る。

## hash
- ab007a7d47527d4fe135ce2d479e540d1c9bf3af0fd00f8049f70eb5b2189a2b

# `test`

## Summary
- cmoc の realization test 群を収める領域。CLI サブコマンド、Codex runtime、indexing、prompt builder、session/apply/review の外部挙動と重要な制御ロジックを pytest で固定している。
- 一時 Git repository、fake Codex executable、Codex home、linked/apply worktree、state/report/log などを使い、正本仕様断片を具体化した実装が利用者から観測される副作用・終了コード・出力・永続状態を満たすかを検証する入口になる。
- 共通 fixture と補助関数も含み、個別テストが repository 初期化、Codex 実行差し替え、branch/worktree 状態確認、profile 生成差し替えなどを重複して持たないための支援層を提供する。

## Read this when
- realization implementation の変更に対して、CLI から観測される終了コード、stdout/stderr、report、commit、state file、worktree/branch cleanup、log などの回帰確認先を探すとき。
- apply fork/join/abandon、session fork/join/abandon、review oracle、indexing、init/TUI、Codex runtime、prompt builder のどの外部挙動が既存テストで固定されているかを把握したいとき。
- Codex CLI 呼び出しを fake executable で置き換え、profile、sandbox、CODEX_HOME、cwd、structured output、retry、quota wait、process tracking などの runtime 境界を検証する方法を確認したいとき。
- Git worktree、linked worktree、apply worktree、dirty state、merge conflict、branch cleanup、repository lock など、Git 状態を伴う cmoc の統合的な挙動をテストで確認または変更したいとき。
- routing document 生成・更新・commit、preflight indexing、hash 再利用、malformed entry 再生成、memo 除外、symlink cycle 除外など、索引更新ワークフローの realization 側の期待値を調べるとき。
- prompt 構築、standard 文書の組み込み、file access rule、structured output schema 参照、ACP builder parameter の期待値が realization test でどう固定されているかを確認したいとき。
- 新しい realization test を追加する前に、既存テストへ case 追加・fixture 再利用・責務統合できるかを判断したいとき。

## Do not read this when
- 正本仕様断片そのもの、oracle file の文言、schema の正本、path model の定義を確認したい場合は、oracle 側の本文を直接読む。
- CLI や runtime の実装本体、helper の内部アルゴリズム、report renderer、prompt builder、Git wrapper などを修正する段階では、該当する実装側を読む。
- Codex CLI や LLM の実際の応答品質、モデル選択、認証フローそのものを評価したい場合は、この realization test 群の目的外である。
- 個別サブコマンドや runtime 境界に関係しない repository の補助ファイル、開発設定、配布設定だけを確認したい場合は、より直接の対象へ進む。
- routing document の書き方や INDEX.md エントリー生成規則だけを確認したい場合は、索引更新のテストではなく該当する正本仕様や生成規則を読む。

## hash
- f22ca6d9823951ca407df7810062c2663b7c87b9444d953b6e5d73e7de71f8a5
