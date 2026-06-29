# `AGENTS.md`

## Summary
- リポジトリ全体に適用される作業規則を示す文書。cmoc の略称、パス表記、ルーティング手順、閲覧・編集禁止対象、正本仕様断片と実装・テスト配置の基本方針を定める。
- 作業者がどの仕様断片を優先し、どこに実装や自動テストを書くべきかを判断するための入口になる。

## Read this when
- リポジトリ内で作業を開始し、全体に適用される前提ルール、用語、禁止事項を確認したいとき。
- パス表記として使われるルート系トークンの意味や、詳細定義をどこで確認するかを知りたいとき。
- 仕様断片、実装、自動テストの責務分担と配置先を確認したいとき。
- 閲覧・編集してはいけない領域や、編集してはいけない正本仕様・ルート文書を確認したいとき。
- 作業中にどの案内文書を起点にファイルを探すべきかを確認したいとき。

## Do not read this when
- 個別機能の詳細仕様、CLI の具体的な挙動、データ構造、テストケースの期待値を調べたいとき。この文書は全体規則だけを扱うため、該当する正本仕様断片や実装・テストを直接読む。
- 特定ディレクトリ内のファイル選択だけをしたいとき。全体規則を確認済みなら、その階層のルーティング情報へ進む。
- 実装コードや自動テストの具体的な修正箇所を探しているとき。配置先の基本方針を確認済みなら、対象の実装またはテストへ進む。

## hash
- c6f2df98ac0d979500fc13a35dd94143c5892db2faf71d604d2307c3c43fa94c

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
- cmoc の realization implementation を置く領域。最上位 CLI 入口、利用者向けサブコマンド本体、実行時共通基盤、ACP builder 周辺の互換入口、設定・基本型・oracle package への互換 shim など、実装側の公開面と orchestration を扱う。
- 正本仕様断片そのものではなく、oracle file で述べられた意図を具体化する実装領域であり、正本側へ集約された型・設定・builder を既存 import 経路から利用できるようにする薄い再公開領域も含む。
- CLI から各機能実装へ入る経路、サブコマンド固有の処理、共通 runtime helper、Codex 実行連携、git・path・state・logging・preflight indexing など、複数の実行機能を読むための上位入口になる。

## Read this when
- cmoc の realization implementation 全体から、CLI 入口、サブコマンド実装、共通 runtime、互換 import 入口のどこへ進むべきかを切り分けたいとき。
- 公開 CLI の command 構成、利用者向けサブコマンドの orchestration、Codex 実行連携、git/worktree/state 操作、INDEX maintenance、review/apply/session lifecycle など実装側の入口を探したいとき。
- 設定、ACP 型、path model、構造化文書 API、ACP builder などについて、realization 側に残る既存 import 経路が正本側実装へどう接続されているかを確認したいとき。
- 複数機能から共有される runtime helper、設定読み込み、エラー表示、ログ、path 解決、外部コマンド結果、session state、preflight indexing などの実装場所を探したいとき。
- oracle 側の正本実装や仕様断片ではなく、実際に CLI から動く realization 側コードの責務境界、委譲先、互換維持箇所を調べたいとき。

## Do not read this when
- 正本仕様断片としての要求、path model、INDEX.md 仕様、oracle/realization の方針、設定定義、prompt builder の正本を確認したいだけのとき。その場合は oracle 側の該当本文を読む。
- realization test の期待値、fixture、検証観点、テストケースの追加先だけを探しているとき。その場合は test 側へ進む。
- 既存 import 経路の互換維持ではなく、正本側の型・設定・builder・構造化文書 API の実体定義や仕様を変更したいとき。その場合は正本側実装を読む。
- 個別機能のさらに詳細な処理だけを確認したいときは、この上位領域で止まらず、該当するサブコマンド、共通 helper、builder、または互換入口の下位対象へ直接進む。
- README、開発方針、パッケージ設定、補助スクリプト、テスト以外の ancillary file を探しているとき。この領域は product behavior を実装する realization implementation を扱う。

## hash
- 2aef603d12af232280f6e656ce66c740e5314e1820f5d85e2308d8032bcea92c

# `test`

## Summary
- cmoc の realization test 群を置く領域。CLI サブコマンド、Codex runtime、indexing、prompt builder、session/apply/review 系の外部挙動と、共通 runtime 契約を pytest で固定している。
- 一時 Git repository、fake Codex CLI、linked worktree、state/report/log などを使い、oracle file の正本仕様断片を具体化した realization implementation が期待どおり動くかを確認する入口になる。
- 共通 fixture・補助関数も含み、個別テストが repository 初期化、Codex home、fake executable、branch/worktree 状態確認などの準備を重複して持たないよう支えている。

## Read this when
- cmoc の実装変更に対して、既存 realization test が固定している CLI 出力、終了コード、Git 副作用、状態ファイル、report/log、cleanup 条件を確認したいとき。
- apply fork/join/abandon、session fork/join/abandon、review oracle、indexing、init/TUI、Codex runtime のいずれかの外部挙動や回帰条件を調べる起点が必要なとき。
- Codex CLI 呼び出しの profile 生成、sandbox/file access mode、CODEX_HOME、retry/quota retry、process tracking、schema validation など、実 Codex ではなく fake 実行ファイルで観測される runtime 境界を確認したいとき。
- INDEX.md 生成・更新・preflight、routing document entry schema、hash 再利用、memo 除外、conflict 解決、並列生成など、indexing workflow の realization 側期待値を確認したいとき。
- prompt 構築、standard 文書の組み込み、ACP builder の model/reasoning/file access mode/schema path、structured output schema 参照の一致をテストから確認したいとき。
- テスト追加や既存テスト修正の前に、同じ観点を扱う既存ケースや共通 helper があるかを探したいとき。

## Do not read this when
- oracle file の正本仕様断片そのもの、用語定義、標準、path model、schema 本文を確認したい場合は、oracle 側の該当本文を読む。
- 実装 helper や CLI command 本体の内部アルゴリズムを直接修正する場合は、まず対応する実装領域を読む。
- Codex CLI や LLM の実際の応答品質、外部サービスの可用性、モデル選択そのものを評価したい場合は、この realization test 群は対象外。
- routing document の本文として読むべき対象を選ぶだけなら、個別テスト本文を総当たりで読む前に、より細かい階層や対象別のルーティング情報で候補を絞る。
- 共通 fixture の使い方だけ、または特定サブコマンドの挙動だけを確認したい場合は、テスト領域全体ではなく該当する補助ファイルまたは対象機能のテストへ直接進む。

## hash
- 1d9f7999a0a6092792ec59630d8ac9dbe3e5118d13a156e2c08525d709b7b23a
