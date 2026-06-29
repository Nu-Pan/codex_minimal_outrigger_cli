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
- cmoc の realization implementation 全体の入口。公開 CLI の Typer 構成、サブコマンド本体、共通 runtime helper、Codex exec/TUI 実行境界、git・path・state・log・config・error 処理、ACP builder 入口、正本側実装を再公開する互換 shim を含む。
- 正本仕様を直接述べる領域ではなく、oracle file で述べられた意図を実行可能な CLI・runtime・互換公開面として具体化する実装層である。
- 下位領域は、CLI 登録と委譲、サブコマンド orchestration、複数機能から共有される runtime、用途別 AgentCallParameter 構築、正本側型・設定・path model の互換再公開に分かれる。

## Read this when
- cmoc の実装変更を行う前に、CLI 入口、サブコマンド本体、共通 runtime、ACP builder、互換 shim のどの領域へ進むべきか切り分けたいとき。
- 利用者が実行するコマンドから、branch/worktree 操作、state 更新、Codex 呼び出し、report 生成、INDEX.md 更新などの実装へどう接続されるかを追い始めるとき。
- 複数サブコマンドで共有される runtime 機能、設定読み書き、path 解決、git wrapper、エラー表示、ログ、Codex profile/schema/preflight などの実装所在を探したいとき。
- 既存 import path を維持するための再公開・委譲・package shim と、正本側実装または責務別 runtime module との境界を確認したいとき。
- AgentCallParameter builder の用途別入口や、正本側 builder への委譲・adapter・局所補正を確認したいとき。

## Do not read this when
- 正本仕様断片、利用者向け要求、prompt の仕様意図、path model や設定定義の正本を確認したいとき。その場合は oracle 側の該当本文を読む。
- 自動テストの期待値、fixture、検証観点を確認・変更したいとき。その場合は realization test 側へ進む。
- パッケージ設定、補助スクリプト、README、リポジトリ運用ファイルなど、実装ソース以外の ancillary file が対象のとき。
- 対象が特定のサブコマンド、runtime helper、builder、互換再公開 module に既に絞れているとき。この上位領域ではなく、対応する下位本文へ直接進む。
- 生成済みログ、`.cmoc` 配下の状態・report・worktree、または memo 配下の内容を調べる作業で、実装本文の責務判断が不要なとき。

## hash
- 771fcdf0334a8ebfeffc0d9b2c6ed0346a1f70b3fa918426529d09e854bf420e

# `test`

## Summary
- cmoc の realization test 群を収める領域で、CLI サブコマンド、Codex 実行連携、runtime 共通契約、prompt 構築、INDEX 更新、review/apply/session workflow などの外部挙動と重要な制御境界を検証する入口になる。
- 共通補助関数により一時 Git repository、Codex home、fake executable、branch/worktree/state の前提を揃え、各テストは正本仕様そのものではなく実装が満たすべき観測可能な挙動と回帰条件を固定する。
- 複数の大きなテストは、同じ fixture・state・Git worktree・Codex 呼び出し列に強く結び付く一連の挙動をまとめて確認するために置かれており、対象 workflow の成功条件・拒否条件・cleanup・report・log を同じ文脈で追うための階層である。

## Read this when
- CLI サブコマンドの終了コード、標準出力、標準エラー、report、commit、branch/worktree/state の副作用など、利用者または外部から観測される挙動を変更・確認したいとき。
- session fork/join/abandon、apply fork/join/abandon、review oracle、init/TUI、indexing など、複数の Git 状態や cmoc state をまたぐ workflow の回帰条件を探すとき。
- Codex CLI 実行 wrapper の profile、sandbox、CODEX_HOME、retry、quota retry、schema validation、call log、subcommand log、process group、preflight indexing の期待挙動を確認・変更するとき。
- root/worktree/path model、config、CmocError 表示、file access mode、binary 判定、.cmoc ignore、state 解決など、個別 workflow の前提になる runtime 契約のテスト上の固定点を確認したいとき。
- prompt builder、structured output schema path、routing/file access rule の render、各 ACP builder の model・reasoning・file access mode 選択が期待どおりかを横断的に確認したいとき。
- 新しい realization test を追加する前に、既存の同じ観点のテストへ case 追加または fixture 共有できるかを確認したいとき。

## Do not read this when
- oracle file の正本仕様断片、用語定義、routing document の設計意図、利用者向け仕様そのものを確認したい場合は、oracle 側の本文を読む。
- 実装 helper、CLI command 本体、prompt builder、diff/report 生成、state 読み書き、Codex runtime などの内部実装を直接修正する場合は、対応する実装側を先に読む。
- 特定の狭い helper や fixture の使い方だけを知りたい場合は、共通補助関数または対象機能のより直接のテストへ進む。
- Codex CLI や LLM の出力品質そのものを評価したい場合は、この領域を読む必要は薄い。ここでは多くの場合 fake 実行結果により cmoc 側の制御ロジックと副作用を検証している。
- INDEX.md エントリーの形式、生成規則、hash freshness などの routing 文書更新仕様だけを調べたい場合は、indexing 関連の対象に絞って読む。

## hash
- c9ce90dbdef47b59d97c7c2cb717c17bf8050b62064fa1d50daff98ca3f9ee33
