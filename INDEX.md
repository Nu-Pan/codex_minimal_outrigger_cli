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
- cmoc の realization implementation 全体を収める領域。最上位 CLI、個別サブコマンド本体、共通 runtime helper、Codex CLI 呼び出し境界、git・path・設定・状態・ログ処理、INDEX.md 更新処理、ACP builder 関連の互換入口と一部補正処理を含む。
- 正本仕様断片そのものではなく、oracle file の人間意図を実行可能な Python 実装へ具体化する場所である。下位領域は、CLI 公開面、サブコマンド実行フロー、横断的 runtime 支援、旧 import path を維持する薄い再公開層、AgentCallParameter 構築入口へ読み進めるための起点になる。

## Read this when
- cmoc の CLI 実装、サブコマンド実行本体、共通 runtime、ACP builder 互換入口のうち、どの実装領域へ進むべきかを最初に判断したいとき。
- 公開 CLI コマンド構成、Typer から各実装関数への委譲、CLI 引数解析エラーの扱い、console script 起動入口を確認または変更したいとき。
- init、indexing、tui、session、apply、review oracle の実行条件、状態遷移、git branch・worktree 操作、Codex exec/TUI 呼び出し、利用者向け出力や report 生成の実装先を探したいとき。
- 設定の読み書き、runtime path 解決、ログ、エラー表示、git wrapper、state file、content hash、Codex profile、quota/capacity retry、Structured Output 検証、INDEX.md 更新など、複数機能で共有される runtime helper を調べたいとき。
- 既存の `acp.*`、`basic.*`、`config.*`、`oracle.*`、`cmoc_runtime` などの import 経路が、正本側実装または実体 runtime module へどう橋渡しされているかを確認したいとき。
- AgentCallParameter builder の realization 側入口、正本側 builder への委譲、prompt や schema の最小補正、TUI・apply・review・session・indexing 向け builder の公開面を調べたいとき。

## Do not read this when
- 正本仕様断片、利用者向け仕様、path model の概念定義、INDEX.md エントリー生成標準など、人間意図そのものを確認したいとき。その場合は oracle file を読む。
- テスト期待値、fixture、外部挙動の検証観点だけを確認したいとき。その場合は realization test 側を読む。
- すでに個別サブコマンド、runtime helper、builder、互換 shim の対象が特定できており、その下位対象を直接読めば足りるとき。
- 実行ログ、state file、report、Codex 出力、キャッシュ、一時ファイルなど生成済み runtime artifact の内容を調査したいだけのとき。
- 正本側の ACP 型、設定定義、path model、構造化文書 API、prompt builder 本体を確認または変更したいとき。この領域には再公開や補正入口が含まれるが、正本定義そのものは別領域にある。

## hash
- bb9468201629d0f63c414875f403fad12ec943774151e5ca46b0cf27960f4eca

# `test`

## Summary
- cmoc の realization test を集約するディレクトリ。CLI サブコマンド、Codex 実行基盤、索引更新、prompt/schema 構築、runtime 共通契約など、oracle file から具体化された外部挙動と制御ロジックの回帰を検証する。
- 共通テスト補助から個別機能の統合テストまでを含み、session、apply、review、init/TUI、indexing、Codex runtime などの期待挙動を、Git worktree・branch・状態ファイル・ログ・report・sandbox profile といった副作用込みで確認する入口になる。
- 正本仕様ではなく realization test の集合であり、実装変更が既存の利用者向け挙動や重要な内部制御境界を壊していないかを確認するための読み先である。

## Read this when
- CLI サブコマンドの終了コード、標準出力・標準エラー、report、commit、branch、worktree、状態ファイル、cleanup など、外部から観測できる挙動の期待値を確認・変更したいとき。
- session や apply の lifecycle、linked worktree 上の動作、dirty worktree 拒否、merge conflict、stale branch、abandon/join cleanup など、Git 状態と cmoc 状態が結合する回帰を調べたいとき。
- Codex CLI 呼び出しの sandbox profile、CODEX_HOME、cwd、schema 出力、retry、quota probe、process tracking、TUI 起動引数など、実行基盤の制御境界を変更・確認するとき。
- INDEX.md 更新、indexing preflight、prompt builder、structured output schema、標準 prompt 断片など、AI 呼び出し前後の文書生成・routing・schema 関連の実現挙動を確認するとき。
- 実装変更に対して、どの既存 realization test にケース追加すべきか、または既存回帰がどの責務境界を守っているかを探すとき。
- テスト用の一時 Git repository、fake Codex executable、認証済み CODEX_HOME、profile 生成差し替え、apply worktree path 解決などの共通補助を利用・変更したいとき。

## Do not read this when
- oracle file に書かれた正本仕様断片や設計意図そのものを確認したいときは、ここではなく oracle 側の本文を読む。
- 実装 module の内部構造、helper の責務分割、関数単位の処理詳細だけを変更したい場合で、外部挙動や回帰期待値をまだ確認する必要がないときは、対応する実装側を先に読む。
- Codex CLI や LLM の出力品質そのものを評価したいとき。この領域のテストは fake や stub を使い、cmoc 側の呼び出し制御と副作用を検証する。
- 特定サブコマンドや runtime 領域に関係しない補助ファイル、依存関係、開発手順、文書作成方針だけを調べたいとき。
- INDEX.md エントリーの形式やルーティング文書の正本規則だけを確認したいときは、この realization test 群ではなく該当する oracle 側の規則を読む。

## hash
- 5157d5b1fa47d5032692f56ce15f03156b0ced5a85ffbcdf412c4a5b8cb6d9c3
