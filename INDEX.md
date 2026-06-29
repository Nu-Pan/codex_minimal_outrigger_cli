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
- cmoc の realization implementation を置く実装ツリー。公開 CLI 入口、サブコマンド本体、共有 runtime helper、Codex CLI/TUI 呼び出し基盤、git・設定・状態・ログ・path・INDEX 更新処理、ACP builder 互換入口、正本側型や設定への再公開 shim を含む。
- 正本仕様断片そのものではなく、oracle 側の型・設定・prompt builder を参照または再公開しながら、利用者向け CLI 操作と実際の実行時挙動を具体化する領域。
- 上位から実装側へ入るときに、CLI 登録、サブコマンド制御、共通 runtime、互換 import 境界、ACP parameter 構築入口のどれを読むべきかを切り分ける起点になる。

## Read this when
- cmoc の CLI コマンドがどの実装へ委譲され、init、indexing、TUI、session、apply、review などの利用者向け操作がどの実行処理へ接続されるか確認したいとき。
- サブコマンド共通の実行ライフサイクル、cmoc 形式のエラー表示、設定読み書き、git 操作、path 解決、ログ、永続 state、外部コマンド結果、Codex exec/TUI 呼び出し、sandbox/profile、quota/capacity retry、Structured Output 検証を実装側から追いたいとき。
- INDEX.md の自動更新、対象探索、hash 判定、既存エントリー再利用、Codex へのエントリー生成依頼、Markdown 描画など、INDEX maintenance の実装を確認または変更したいとき。
- oracle 側に正本がある ACP 型、path model、構造化文書、設定定義、ACP builder を realization 側の既存 import path からどう再公開・委譲しているか確認したいとき。
- apply fork/join/abandon、session fork/join/abandon、oracle review、TUI 起動など、branch/worktree、状態更新、Codex 呼び出し、report 生成を伴う実処理の入口を探したいとき。

## Do not read this when
- 正本仕様断片、仕様意図、path model の概念定義、prompt standard、subcommand の外部仕様などを確認したいだけのときは、実装ではなく oracle 側の本文を読む。
- realization test の期待値、fixture、検証観点を変更したいときは、実装ツリーではなく対応するテスト領域を読む。
- README、配布メタデータ、補助スクリプト、gitignore など、実装ソース以外の ancillary file を確認したいだけのときは、それぞれの配置先を読む。
- 個別の下位領域や単一機能の読む先がすでに特定できているときは、この上位入口に留まらず、該当するサブコマンド、共有 runtime helper、互換再公開層、または ACP builder 領域へ直接進む。
- oracle 側に正本がある型・設定・prompt builder の内容そのものを変更したいときは、realization 側の互換 shim ではなく正本側の実装または仕様本文を読む。

## hash
- 20a99cb314467ff15577021aa370d87bb8de0563fdabaaafd769a4fe88c5187d

# `test`

## Summary
- realization test 全体の入口。CLI サブコマンド、Codex runtime、prompt 構築、indexing preflight、session/apply/review など、oracle file から具体化された外部挙動と制御ロジックの回帰を検証するテスト群を収める。
- 共通補助関数も含み、一時 Git repository、Codex home、stub executable、linked worktree、apply worktree など、外部コマンドや状態ファイルを伴うテストの準備・観測を支える。
- 各テストは実装詳細そのものよりも、CLI 出力、終了コード、git/worktree/state/report/log への副作用、Codex 呼び出し境界、エラー時の保持・cleanup といった realization file として意味のある挙動を固定する役割を持つ。

## Read this when
- CLI から観測される cmoc の挙動を変更する前に、既存の終了コード、標準出力・標準エラー、report、commit、state、worktree、branch、log への副作用を確認したいとき。
- apply fork/join/abandon、session fork/join/abandon、init/TUI、indexing、review oracle、Codex runtime など、複数の repository 状態や外部プロセスをまたぐ回帰テストの読む先を選びたいとき。
- Codex CLI 呼び出しの profile、sandbox、CODEX_HOME、retry、quota wait、structured output schema、process tracking、file access mode の扱いをテスト上で確認したいとき。
- prompt builder、routing rule、file access rule、structured output schema 参照、standard prompt 断片が complete prompt や ACP builder にどう反映されるかを検証したいとき。
- realization test を追加・変更する際に、既存テストへケース追加できるか、共通 fixture や helper を使えるか、同じ観点の重複テストがないかを確認したいとき。
- git worktree、branch、dirty 状態、merge conflict、INDEX 更新、memo 除外、binary file、ignore 対象など、repository 境界を伴う挙動の既存期待値を探したいとき。

## Do not read this when
- oracle file の正本仕様断片や標準そのものを確認したい場合は、ここではなく oracle 側の本文を読む。
- 実装 helper、CLI command、path model、prompt builder、Codex runtime、diff/report 生成などの内部設計を直接修正する場合は、まず対応する実装側を読む。
- Codex CLI や LLM の実際の応答品質、モデル選択、プロンプト内容の良し悪しを評価したいだけの場合は、この realization test 群を読む必要はない。
- routing document の意味品質や INDEX.md エントリー生成規則そのものを確認したいだけの場合は、正本仕様や対象本文を読む。
- 個別サブコマンドの一点だけを調べる作業で読む先がすでに分かっている場合は、全体入口ではなく該当テスト本文へ直接進む。

## hash
- 4222d066831aba73fa8b3d5636e4dd8a1ceeebea1ac7c6fc2add4333a121466f
