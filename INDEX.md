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
- 利用者が実行するコマンド入口のシェルラッパーを置く領域で、リポジトリルートと仮想環境内 Python を特定し、実体の Python エントリポイントへ制御を渡す起動経路を扱う。
- 仮想環境内 Python が存在しない、または実行できない場合の利用者向けエラー、初回セットアップ案内、表示用パス、行番号付きの簡易 call stack 出力を扱う。
- シェル補完プローブ時には通常の不足エラーを抑制し、仮想環境内 Python が使える場合だけ Python エントリポイントへ委譲する挙動を扱う。

## Read this when
- 利用者が実行するコマンドの起動経路、リポジトリルートの特定、仮想環境内 Python の検出、または Python エントリポイントへの委譲方法を確認・変更するとき。
- 仮想環境が未作成または壊れている場合のエラー出力、初回セットアップ案内、表示用パス、call stack 表示を確認・変更するとき。
- シェル補完時の挙動や、補完プローブで通常エラーを抑制する条件を確認・変更するとき。
- 利用者向けに表示されるスクリプト位置表記が、作業ツリー上の実パスではなく抽象パストークンに従っているか確認するとき。

## Do not read this when
- Python 側の CLI サブコマンド、引数解析、業務ロジック、または通常のコマンド出力内容を調べたいだけなら、委譲先の Python 実装を読む。
- 仮想環境の作成手順そのもの、依存関係定義、またはパッケージ設定を変更したいだけなら、セットアップやパッケージ管理を担う対象を読む。
- oracle file と realization file の概念、パストークンの定義、または正本仕様断片を確認したいだけなら、対応する oracle 側の文書や実装を読む。

## hash
- d95e290a70bec73f598a40b846824050bc085416d6211017dffdb386eb9c389f

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
- cmoc の realization implementation 全体の入口となる領域。最上位 CLI、サブコマンド実行フロー、共有 runtime helper、互換 import shim、正本側実装への薄い再公開入口を含む。
- 実装本体は、CLI 登録と委譲、操作別 orchestration、Codex CLI 実行境界、git・path・設定・state などの共通基盤、ACP builder や basic/config/oracle 互換経路に分かれており、下位領域へ進むための最初の切り分け点になる。
- この領域は realization implementation であり、正本仕様そのものではない。仕様意図や人間管理の要求は oracle 側を根拠にし、ここではそれを具体化した実装や移行用互換面を確認する。

## Read this when
- cmoc の実装変更で、最上位 CLI、サブコマンド、共有 runtime helper、互換 import 層のどこから調べ始めるべきかを切り分けたいとき。
- 公開 CLI コマンド構成、Typer app、session・apply・review・INDEX maintenance・TUI などの実行入口と委譲先を確認したいとき。
- Codex exec/TUI 起動、preflight、quota/capacity retry、設定、path、git、ログ、Structured Output 検証、session state、INDEX.md 更新共通処理など、複数の workflow が共有する runtime 基盤を探したいとき。
- 既存の `basic.*`、`config.*`、`oracle.*`、ACP builder 関連 import path が、正本側実装または下位実体へどう再公開・委譲されているかを確認したいとき。
- 実装上の変更対象がまだ特定できておらず、CLI 入口、操作別処理、共通 helper、互換 shim、正本側再公開のどれに進むべきか判断したいとき。

## Do not read this when
- cmoc の正本仕様断片、path model、設定仕様、状態仕様、INDEX.md エントリー仕様、prompt 本文、structured output schema など、人間が管理する仕様意図を確認したいとき。その場合は oracle 側の該当本文を読む。
- realization test の期待値、fixture、外部挙動の検証観点だけを調べたいとき。その場合は test 側を読む。
- 対象サブコマンドや責務がすでに特定できており、fork、join、abandon、review loop、report、target 列挙、INDEX merge、git 操作、設定 load などの詳細だけを調べたいとき。その場合は該当する下位実装を直接読む。
- ACP builder の正本仕様、prompt 構築、AgentCallParameter の値、path model や構造化文書処理の定義そのものを変更・確認したいとき。その場合は正本側実装または該当する個別 builder を読む。
- 互換 import path の維持や削除条件と無関係な一般的な仕様判断、ドキュメント整理、または oracle file の変更提案を行うとき。

## hash
- 551949011f19b3e0ae7333c53e352b2cb198dc6a0aab30893e9f00e154970dcb

# `test`

## Summary
- cmoc の realization test 群を収める領域。CLI サブコマンド、Codex 実行基盤、session/apply/review/indexing の workflow、prompt/ACP builder、共通 runtime 境界を、外部挙動・状態遷移・Git 副作用・ログ・report を中心に検証する。
- 一時 Git repository、fake Codex、profile 差し替え、process 制御などの共通補助も含み、実装変更が既存の user-visible behavior や制御ロジックへ与える影響を確認する入口になる。
- 個別ファイルは機能領域ごとに分かれており、apply/session/review/indexing/runtime/prompt など、変更対象のサブコマンドまたは共通基盤に対応するテストへ進むための上位ルーティング対象である。

## Read this when
- CLI サブコマンドの終了コード、標準出力・標準エラー、report、commit、branch、worktree、state file、cleanup など、外部から観測できる挙動の期待値を確認・変更したいとき。
- session fork/join/abandon、apply fork/join/abandon、review oracle、indexing、init、TUI 起動前処理など、複数の Git 状態や cmoc state を伴う workflow の回帰観点を探すとき。
- Codex CLI 呼び出し、CODEX_HOME、profile、sandbox file access mode、structured output、retry、quota probe、subcommand log など、Codex 実行基盤の契約を確認・変更するとき。
- prompt builder や AgentCallParameter builder が生成する prompt、schema path、file access rule、standard 文書の挿入条件を横断的に確認したいとき。
- realization implementation を変更する前後で、既存テストに同じ観点のケースを追加できるか、または削除・統合すべき古いテストがあるかを確認するとき。
- CLI テスト用の一時 repository、fake executable、認証済み Codex home、apply worktree path 解決など、テスト fixture や monkeypatch の共通入口を探すとき。

## Do not read this when
- oracle file の正本仕様断片そのものを確認・編集したいとき。この領域は realization test であり、正本仕様の代替ではない。
- 実装 helper の内部構造、関数分割、低レベル parser や renderer の詳細だけを局所的に確認したいときは、対応する realization implementation を先に読む。
- Codex CLI や LLM の出力品質そのものを評価したいとき。この領域のテストは fake subprocess や制御された応答で cmoc 側の呼び出し・副作用・制御境界を検証する。
- routing document の自然言語エントリー内容だけを作成する場合で、indexing workflow の生成・更新・commit・schema 検証の実装挙動を追う必要がないとき。
- 単一の設定値、path model、JSON schema、oracle/realization の概念定義など、テストではなく仕様または実装側に直接根拠がある事項だけを確認したいとき。

## hash
- 852b263d6d7768329dcf12e90410f1ec533ef05aac4a30a4287c628477ff73bb
