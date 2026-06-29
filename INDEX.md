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
- cmoc の realization implementation 全体を収める領域。最上位 CLI 入口、サブコマンド実行本体、複数機能で共有する runtime helper、Codex CLI/TUI 呼び出し境界、git・path・state・設定・ログ・INDEX.md maintenance、ACP builder 互換入口、oracle 側正本実装への薄い再公開 shim を扱う。
- 正本仕様断片そのものではなく、oracle file の人間意図を具体化する Python 実装層である。公開 CLI から実行時共通処理、session/apply/review/indexing/TUI の workflow、既存 import path の互換維持まで、実際に動作する realization code へ進むための入口になる。
- 下位領域は、公開 CLI 構成、サブコマンド orchestration、共通 runtime、ACP parameter builder の委譲・補正・互換再公開、基本型や設定の互換再公開、oracle package 解決 shim に分かれる。作業対象が特定済みなら、この領域全体ではなく該当責務の下位項目へ進む。

## Read this when
- cmoc の実装本体のうち、CLI 入口、サブコマンド本体、共通 runtime、ACP builder 互換層、oracle 側正本への shim のどこから調査すべきか切り分けたいとき。
- 公開 CLI のコマンド構成から、session、apply、review、indexing、TUI、初期化処理がどの実装層へ委譲されるかを追い始めるとき。
- Codex CLI/TUI 呼び出し、Structured Output 検証、quota/capacity retry、profile/schema/CODEX_HOME、call log、subcommand log、共通エラー表示など、複数 workflow にまたがる実行時境界を探したいとき。
- git branch/worktree 操作、session/apply state、report、設定 JSON、path 解決、`.cmoc` 配下の保存先、INDEX.md 更新 preflight など、実行時 helper とサブコマンド制御の接続を確認したいとき。
- oracle 側に正本がある型・設定・ACP builder・path model・構造化文書 API を、realization 側の既存 import path がどの互換入口で受けているか確認したいとき。
- realization implementation の変更で、既存実装の責務境界、互換コードの削除条件、下位領域の読み分けを把握してから編集先を選びたいとき。

## Do not read this when
- oracle file の正本仕様、人間意図、prompt 正本、設定定義、path model の仕様意図を確認したいとき。この領域は正本仕様ではないため、対応する oracle 側本文を読む。
- 実装ではなく自動テストの観点、fixture、期待挙動の検証方法を調べたいときは、realization test 側へ進む。
- 配布設定、依存定義、console script のパッケージ設定、補助 script、リポジトリ管理ファイルだけを確認したいときは、realization ancillary 側の該当対象を読む。
- 特定のサブコマンド、runtime helper、ACP builder、互換 shim のどれを読むべきか既に分かっているときは、この領域全体ではなく、その下位項目または個別 module へ直接進む。
- 生成済みログ、`.cmoc` 配下の実行結果、作業メモ、キャッシュ、pycache など、実装本文ではない生成物を調べたいだけのとき。
- INDEX.md エントリーの文面基準やルーティング文書の仕様そのものを確認したいときは、実装層ではなく対象本文とエントリー生成基準を読む。

## hash
- bc8017511adb4b80b7d5ec52ee73052b577bf6e3331006042dff2889201b66c3

# `test`

## Summary
- cmoc の realization test 群と CLI テスト用の共通補助を収める領域。session、apply、review、indexing、init/TUI、Codex runtime、prompt builder、基礎 runtime の外部挙動・制御ロジック・状態遷移・Git 副作用を pytest で検証する。
- 正本仕様そのものではなく、oracle file と実装から具体化された現在の期待挙動を固定する回帰テストの入口であり、CLI 出力、終了コード、状態ファイル、worktree/branch cleanup、Codex 呼び出し制御、INDEX 更新、report 生成などを確認する場所である。
- 一時 Git repository、Codex home、fake executable、profile 差し替えなど、外部コマンドを伴うテストの準備を共有する補助も含む。

## Read this when
- realization implementation の変更に対して、既存の外部挙動や回帰テストの期待値を確認したいとき。
- session、apply、review oracle、indexing、init/TUI、Codex runtime、prompt/ACP builder、path/config/error/profile/log/state などの挙動に関するテストを追加・更新・削除したいとき。
- CLI の終了コード、stdout/stderr、report、commit、branch、worktree、状態ファイル、cleanup、dirty worktree 拒否、conflict 解決など、ユーザーまたは Git から観測できる副作用を確認したいとき。
- Codex CLI 呼び出しを fake に差し替えたテスト、quota/capacity retry、schema validation、profile/sandbox/CODEX_HOME、prompt/schema 保存先などの runtime 制御を調べたいとき。
- INDEX.md 生成・更新、indexing preflight、routing entry schema validation、prompt standard のレンダリングなど、AI へ渡す文脈や構造化出力に関わる回帰を確認したいとき。
- テスト用 repository、Codex home、profile stub、fake Python executable、apply worktree path 解決など、複数テストで共有する fixture/helper の使い方や変更影響を確認したいとき。

## Do not read this when
- oracle file の正本仕様断片、利用者向け仕様、用語定義、routing 文書の原則を確認したいだけなら、oracle 側の本文を読む。
- 実装本体の責務分割、内部 helper の設計、データ構造、アルゴリズムを直接変更する場合は、まず対応する realization implementation を読む。
- 特定機能の現在のソースコード上の原因を追っており、すでに対象 module が分かっている場合は、その実装側へ直接進む。
- Codex CLI や LLM の実際の出力品質そのものを評価したい場合は、この領域を入口にしない。ここでは fake subprocess や固定応答で cmoc 側の制御を検証する。
- INDEX.md の既存 entry や生成済み routing 文書の内容を確認したいだけの場合は、テスト本文ではなく対象の routing 文書を読む。
- 単にファイル一覧や hash など機械的な情報だけを知りたい場合は、本文ではなくツールや Git の出力で確認する。

## hash
- 5e6619bc841388a09d53ab787e2c51f3d1f780a53cf0c5ab36c6b296f8a01808
