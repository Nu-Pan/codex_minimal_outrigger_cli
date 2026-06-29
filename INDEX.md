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
- cmoc の realization implementation 全体への入口。公開 CLI、サブコマンド orchestration、共通 runtime helper、Codex CLI 実行連携、git/worktree 操作、状態管理、INDEX.md 更新、TUI 起動、review/apply/session lifecycle、設定・基本型・ACP builder の互換 import 境界を扱う。
- 正本仕様そのものではなく、oracle file で述べられた意図を実行可能な Python 実装として具体化する領域。下位には、CLI entrypoint、互換 shim、共通 runtime、サブコマンド本体、agent call parameter builder 周辺の再公開層が分かれている。

## Read this when
- cmoc の CLI 挙動、サブコマンド実行、Codex subprocess/TUI 連携、git branch/worktree 操作、状態ファイル更新、利用者向け report やエラー表示など、実装本体の所在を探したいとき。
- oracle file の正本仕様断片や既存テストを根拠に、実際の runtime 処理、公開 import path、互換 shim、共通 helper、サブコマンド orchestration を確認または変更したいとき。
- 初期化、INDEX maintenance、session fork/join/abandon、apply fork/join/abandon、review oracle、TUI 起動のどの実装領域へ進むべきかを切り分けたいとき。
- 設定・ACP 型・path model・構造化文書・ACP builder などが、realization 側の既存 import path から oracle 側正本実装または下位実装へどう橋渡しされているか確認したいとき。
- 複数サブコマンドで共有される runtime path、設定読み書き、content hash、Codex profile/sandbox、quota/capacity retry、Structured Output 検証、call log、session/apply state、git wrapper、INDEX preflight の実装入口を探したいとき。

## Do not read this when
- 人間が所有する正本仕様断片、path token の概念定義、oracle/realization の分類、INDEX.md 仕様、各サブコマンドの意図や出力互換性の根拠を確認したいだけのときは、oracle 側の文書や実装を読む。
- テスト観点、期待される外部挙動の検証、fixture、回帰条件を確認または変更したいときは、realization test 側を読む。
- 配布設定、補助スクリプト、gitignore など、実装コードではない補助ファイルの責務を調べたいときは、それぞれの ancillary 領域へ進む。
- 特定サブコマンドの利用者向け option 名や委譲先だけを確認したい場合は CLI entrypoint へ、個別処理の詳細を追う場合は該当サブコマンドや共通 runtime の下位本文へ直接進む。
- ACP builder の正本 prompt や parameter 仕様そのものを確認したいときは、互換再公開層ではなく oracle 側または該当 builder 本体を読む。

## hash
- 765f426654d4ef2aed24d587aeea6bdf63ed62bfa501564e1fb7e6bac9852a70

# `test`

## Summary
- cmoc の realization test 群を収める領域。CLI サブコマンド、Codex runtime、indexing preflight、prompt/ACP builder、session/apply/review の外部挙動を、Git worktree・状態ファイル・report・ログ・Codex 呼び出し stub などの観測点から検証する。
- 共通 test helper も含み、一時 Git repository、Codex home/profile、fake executable、branch/worktree 状態確認など、外部コマンドや Git 副作用を伴うテストの前提準備への入口になる。
- テストは正本仕様そのものではなく、oracle file で述べられた意図を具体化した realization code の回帰確認であるため、仕様判断の根拠が必要な場合は oracle 側を先に確認する。

## Read this when
- cmoc の実装変更に対して、既存の realization test が固定している CLI 出力、終了コード、Git 副作用、状態遷移、report 生成、ログ記録、Codex 呼び出し制御の期待値を確認したいとき。
- apply fork/join/abandon、session fork/join/abandon、review oracle、init/TUI、indexing、Codex exec/TUI runtime、quota/capacity retry、prompt builder などの外部挙動に関する回帰テストを探すとき。
- 新しい realization test を追加する前に、同じ観点を既存テストへ統合できるか、既存 fixture や helper を再利用できるかを確認したいとき。
- Git worktree、branch、dirty 状態、merge conflict、linked worktree、CODEX_HOME、sandbox/profile、structured output schema、subcommand log などを伴うテストの既存パターンを確認したいとき。
- INDEX.md 生成・更新、entry schema、routing document conflict 解決、memo 除外、symlink cycle、preflight commit など indexing 周辺の realization 挙動を検証するテストを探すとき。

## Do not read this when
- oracle file の正本仕様断片、用語定義、標準、JSON schema の正本内容を確認したい場合は、ここではなく oracle 側の本文を読む。
- 実装本体の責務分割、内部 helper のアルゴリズム、公開 API の設計を直接変更する場合は、まず対応する implementation 側を読む。
- Codex CLI や LLM の実際の応答品質、モデル選択、認証フローそのものを評価したい場合は、この領域のテストは主に fake subprocess と stub 応答で制御フローを検証するため入口ではない。
- 単に repository 全体の構成やルーティング文書の生成規則を知りたいだけの場合は、より上位または oracle 側の routing/indexing 仕様を読む。
- 個別サブコマンドや runtime 領域に関係しない補助ファイル、ドキュメント、設定の意味を調べる場合は、対象の同階層エントリーや実装本文へ直接進む。

## hash
- f595f01b83d1f836130ff4b9ac6ddbf54cf20d73b33d128bba44a8364cebb33c
