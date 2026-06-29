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
- cmoc の realization implementation 全体への入口。公開 CLI、サブコマンド実行本体、複数 workflow で共有される runtime helper、既存 import path を保つ互換 shim・再公開層を含む。
- 正本仕様や正本実装を複製する領域ではなく、oracle file で述べられた意図を CLI 実行、状態操作、git 操作、Codex 呼び出し、INDEX.md maintenance、互換 import 境界として具体化する実装側の上位階層である。
- 下位要素へ進む際は、CLI 定義、個別サブコマンド、共有 runtime 基盤、ACP・basic・config・oracle 関連の互換入口のどれを調べるべきかを切り分ける起点になる。

## Read this when
- cmoc の realization implementation を変更・調査する作業で、最上位 CLI、サブコマンド本体、共有 runtime helper、互換 import 層のどこへ進むべきかを判断したいとき。
- 公開 CLI のコマンド構成、各コマンドから実装関数への委譲、引数解析エラー表示、console script 起動境界を確認したいとき。
- 初期化、INDEX maintenance、TUI、session、apply、review oracle などのサブコマンド実行フロー、preflight、state 遷移、branch/worktree 操作、report 出力への接続点を追い始めるとき。
- Codex CLI 呼び出し、設定、runtime path、git wrapper、ログ、状態、エラー表示、内容 hash、CLI 実行ライフサイクルなど、複数機能から共有される実行時基盤の所在を探したいとき。
- realization 側に残る ACP、basic、config、oracle、runtime などの旧 import path や互換再公開が、正本側実装または実体 module へどう接続されているかを確認したいとき。

## Do not read this when
- 正本仕様断片、設計意図、prompt、structured output schema、path model の概念定義、設定定義の正本を確認したいとき。その場合は oracle 側の本文へ進む。
- テスト期待値、fixture、検証観点だけを調べたいとき。その場合は realization test 側を読む。
- 補助スクリプト、配布設定、gitignore など、実装ソースではない realization ancillary を確認したいとき。
- 個別の対象がすでに特定できているとき。CLI 定義、特定サブコマンド、共有 helper、互換 shim、正本側実装など、より直接の下位対象へ進む。
- ACP builder の prompt 本体、設定項目の内容、path 解決の定義、構造化文書処理、indexing の実体処理など、互換入口ではなく正本側または責務別実装を読むべき作業のとき。

## hash
- 41a87ddbbbc28d857e0f59d2c6d76eec9fcd24eb7f78d47edc91a1835e2bb805

# `test`

## Summary
- cmoc の realization test 群への入口。CLI サブコマンド、Codex runtime、prompt/schema 構築、INDEX 更新、session/apply/review の外部挙動と制御ロジックを、共通テスト補助とともに扱う。
- 正本仕様そのものではなく、oracle file の人間意図を具体化した既存実装の観測可能な挙動、状態ファイル・Git worktree/branch・ログ・レポート・エラー表示などの回帰境界を確認するための領域である。
- 個別機能のテストは対象サブコマンドや runtime 責務ごとに分かれており、共通 fixture、fake Codex 実行、最小 Git repository、Codex home/profile 差し替えなどの準備処理も同じ領域にまとまっている。

## Read this when
- cmoc の実装変更に対して、CLI から観測される出力、終了コード、Git branch/worktree 副作用、状態ファイル更新、ログ、レポート生成の既存期待値を確認したいとき。
- session の fork/join/abandon、apply の fork/join/abandon、review oracle、init/TUI、indexing など、利用者向けサブコマンドの回帰テストや境界条件を探すとき。
- Codex CLI 呼び出し wrapper の subprocess 起動、profile/sandbox/cwd/schema/log、CODEX_HOME 検証、retry、quota probe/resume、異常終了時のエラー報告を確認・変更するとき。
- prompt builder、ACP builder、structured output schema、routing rule、file access rule、root token の扱いが最終 prompt や schema 参照にどう反映されるかを横断的に検証したいとき。
- INDEX 更新や indexing preflight の生成・再生成判定、hash freshness、malformed entry、conflict 解決、commit 条件、worktree 選択、Codex 呼び出し条件を確認するとき。
- CLI テスト用の一時 Git repository、最小 oracle 構成、fake Codex/Python executable、Codex home、profile 生成差し替え、branch/worktree 検証 helper を使う、または変更するとき。
- 新しい realization test を追加する前に、既存テストへ同じ観点のケースを統合できるか、既存 fixture や helper を使えるかを確認するとき。

## Do not read this when
- oracle file の正本仕様断片、用語定義、設計意図、標準文書そのものを確認・変更したいときは、oracle 側の本文を読む。
- 実装本体の関数分割、内部 helper、データ構造、アルゴリズムを直接修正したいだけで、外部挙動や回帰期待値を確認する必要がないときは、対応する realization implementation を先に読む。
- Codex CLI や LLM の実出力品質、モデル選択の妥当性、生成内容の品質そのものを評価したいとき。この領域は fake 実行や構造化された観測結果で cmoc 側の制御を検証する。
- 特定サブコマンドや runtime 責務と無関係な一般的な repository 構造、path model、oracle/realization 概念、INDEX ルーティング規約だけを知りたいときは、該当する仕様文書や実装入口へ進む。
- pytest の個別アサーションではなく利用者向け仕様を決めたいとき。この領域の内容は realization test であり、正本仕様の代替として扱わない。

## hash
- 15729214ea0dd88ca201b2a9a9b4010e17f50c5c720eb07f3c1b18ceb4734308
