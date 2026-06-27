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
- cmoc の正本仕様断片を束ねる領域。人間が所有する oracle file と、AI が具体化する realization file の責務境界、正本仕様断片としての一般原則、実装・テスト・補助ファイルの肥大化抑制、ルーティング文書エントリーの作成基準を扱う。
- 下位には、自然言語で書かれた利用者向け挙動・git/session/run モデル・設計判断・開発規則の仕様断片と、Python 実装や設定形式で書かれた path model・設定モデル・AI 呼び出し境界などの仕様断片がある。
- 実装やテストを変更する前に、正本仕様として読むべき領域を、自然言語仕様、プログラム形式の仕様、oracle/realization の基本原則、INDEX.md エントリー基準のどれとして探すかを切り分ける入口になる。

## Read this when
- cmoc の正本仕様断片全体から、読むべき自然言語仕様またはプログラム形式の仕様を探したいとき。
- oracle file と realization file の定義、責務分担、編集主体、正本仕様から実装へ流れる関係を確認したいとき。
- oracle file をどの程度書くべきか、未定義部分をどう扱うか、用語・命名・矛盾・ベストプラクティスとの優先関係など、正本仕様断片の一般基準を確認したいとき。
- realization file の実装・テスト・補助ファイルについて、最小化、品質、分割、抽象化、公開面、依存、削除・統合余地の共通基準を確認したいとき。
- INDEX.md エントリーに何を書くべきか、対象本文との根拠関係、読む条件と読まなくてよい条件の境界、機械的情報を混ぜない基準を確認したいとき。
- CLI 挙動、実行時状態、git branch / commit / worktree モデル、Codex CLI 呼び出し、ログ、エラー処理、インデクシング、run 隔離、開発環境などの自然言語仕様へ進む入口を探したいとき。
- path キーワード、設定値、基礎型、Markdown レンダリング、AI 呼び出しパラメータ、Structured Output 契約など、プログラム形式の正本仕様断片へ進む入口を探したいとき。

## Do not read this when
- 既存 realization code の具体的な関数、クラス、CLI 実装、git 操作、永続状態更新、TUI 描画、テスト期待値だけを調べたいとき。
- 読むべき個別の正本仕様断片がすでに特定できており、その本文だけを確認すればよいとき。
- 自然言語仕様だけを確認したいことが明確で、下位の自然言語仕様領域へ直接進めるとき。
- path model、設定モデル、AgentCallParameter builder、Structured Output schema など、プログラム形式の仕様だけを確認したいことが明確で、下位の実装形式仕様領域へ直接進めるとき。
- 正本仕様断片やルーティング基準ではなく、生成物、実行ログ、一時ファイル、または作業メモを探しているとき。

## hash
- a6ee75fc12fb3905d402e6217213d05db2e4d2b275370043873941ccf78842de

# `pyproject.toml`

## Summary
- Python パッケージとしての配布設定、実行コマンドのエントリーポイント、対応 Python バージョン、実行時・開発時依存、パッケージ探索、テスト実行時の import 経路を定義するプロジェクト設定。
- CLI 名から実装上の main 関数へ接続する公開実行面と、setuptools によるビルド・モジュール配置・パッケージデータ同梱の前提を確認する入口。

## Read this when
- 依存パッケージ、対応 Python バージョン、ビルド backend、配布対象モジュール、パッケージデータ、CLI エントリーポイントを確認・変更する必要があるとき。
- テスト実行時に実装側または正本仕様側の Python モジュールが import される経路を確認する必要があるとき。
- 新しい実行時依存、テスト依存、公開コマンド、配布対象モジュール、同梱データを追加・削除する変更を検討するとき。

## Do not read this when
- 個別の CLI 挙動、コマンド処理、ランタイム処理、設定ファイル生成ロジックの実装詳細を調べたいとき。
- 正本仕様断片の内容や、実装が満たすべき仕様上の要求を確認したいとき。
- 個別テストケースの期待値、fixture、テスト対象の制御ロジックを調べたいとき。

## hash
- a1df0d9e48d52552fd4d13591133e0405f6a99fe2cdafa91a6470bcd1986bfb7

# `src`

## Summary
- cmoc の realization implementation を収める実装領域。公開 CLI 入口、サブコマンド本体、session/apply/review/indexing/tui/init の制御フロー、共通 runtime helper、設定モデル、基礎データ構造、AI agent 呼び出しパラメータと標準プロンプト片の構築を扱う。
- 利用者が実行する操作を、Git worktree/branch/state、Codex exec/TUI 呼び出し、設定読み書き、レポート生成、INDEX.md maintenance などの具体的な実装へ接続する中心的な入口である。
- 下位には、CLI コマンド登録と委譲、サブコマンド別 workflow、横断的 runtime 基盤、リポジトリ設定、path token や Structured Output schema を含む基礎モデル、用途別 AI 依頼プロンプト生成の各領域がある。

## Read this when
- cmoc の CLI コマンド構成、option、サブコマンド実装への委譲先、引数解析エラーの扱いを確認または変更したいとき。
- session の開始・取り込み・破棄、apply run の開始・取り込み・破棄、oracle review、INDEX.md maintenance、初期化、TUI 起動など、利用者操作としての実行順序・事前条件・状態遷移・出力・cleanup を追いたいとき。
- Git branch/worktree 操作、cmoc 管理 branch、session/apply state、run worktree、merge conflict、想定外差分、report 生成など、サブコマンドの具体的な runtime 挙動を確認または変更したいとき。
- Codex CLI の exec/TUI 起動、profile や sandbox 設定、schema 配置、resume token、quota/capacity handling、call log、preflight indexing など、AI agent 呼び出しの実行基盤を調べたいとき。
- AI agent に渡す AgentCallParameter、model class、reasoning effort、file access mode、Structured Output schema、完全プロンプト、標準プロンプト片、用途別プロンプト builder を確認または変更したいとき。
- リポジトリごとの cmoc 設定、既定値、設定 JSON との変換、Codex 向けモデル名・reasoning effort 名の対応、apply/review の処理上限を調べたいとき。
- root token 付き path 表記、repo/work/run/cmoc root 解決、規範文書モデル、構造化文書から Markdown への変換など、複数実装から参照される基礎型・変換処理を確認したいとき。
- INDEX.md 更新の対象列挙、鮮度判定、entry 生成、lock、自動 commit、既存 entry 解析など、ルーティング文書 maintenance の実装を追いたいとき。

## Do not read this when
- cmoc の正本仕様断片そのもの、oracle file の要求、app spec、path model の仕様文、review oracle の規範など、人間が所有する仕様本文を読みたいとき。
- 実装の外部挙動をテスト観点で確認または変更したいだけのとき。対応する realization test を読む方が直接的である。
- README、パッケージ設定、補助スクリプト、配布設定、リポジトリ管理用ファイルなど、実装ソース以外のプロジェクト補助情報を確認したいとき。
- 生成済みバイトコード、キャッシュ、実行ログ、一時生成物、保存済み report の内容を確認したいとき。この領域の本文ではなく生成先や runtime 出力を直接見る。
- oracle file と realization file の関係、oracle standard、realization standard、index entry standard の本文だけを確認したいとき。実装側の標準プロンプト生成ではなく、仕様または提示された標準本文を読む方が直接的である。
- 個別サブコマンドの利用方法だけを知りたいとき。内部実装の読解ではなく、CLI help や利用者向け出力を確認する方が十分である。

## hash
- 7bb8ea4521a5a5a0d6b6251cd75b71c0d3a5d960294ef5ab8de5c2a775ac69de

# `test`

## Summary
- cmoc の realization test 全体を収める領域。CLI サブコマンド、Codex 実行 wrapper、indexing、prompt 構築、path/runtime 契約、session/apply/review の外部挙動を、実際の Git 操作や fake Codex 実行を組み合わせて検証する。
- 共通 fixture 的な補助処理と、個別コマンド・runtime 制御・report/schema・状態遷移の回帰テストへの入口として位置づく。実装詳細ではなく、現行仕様上意味のある外部挙動や制御境界を確認するために読む。
- 一部の大きなテストは 16,000 文字を超えるが、同じ run 状態、fake 応答、report 文脈、cleanup 境界条件を一箇所で扱うため、関連する外部挙動をまとめて追うための凝集した realization test として置かれている。

## Read this when
- cmoc の CLI 操作について、終了コード、stdout/stderr、report、状態ファイル、Git branch/worktree、cleanup、rollback などの観測可能な挙動を確認・変更したいとき。
- session、apply、review、indexing、init、TUI、Codex runtime wrapper のいずれかに関する regression test や既存期待値を探すとき。
- Codex CLI 呼び出しを fake executable で置き換えたテスト、CODEX_HOME/profile/log/schema/sandbox、retry や quota retry、preflight indexing の制御を確認したいとき。
- path token、run/work root、linked worktree、file access mode、branch 名からの状態解釈、binary 判定、config 既定値など、複数 module にまたがる runtime 契約の外部挙動を確認したいとき。
- prompt 構築、標準文書、structured output schema 参照、oracle source との一致、markdown rendering の回帰観点をテスト側から確認したいとき。
- テスト用 repository、tracked かつ ignore された oracle file、CLI runner、Git wrapper、偽 Python/Codex 実行ファイルなど、複数テストで再利用される準備処理を確認したいとき。

## Do not read this when
- cmoc の正本仕様断片を確認したいとき。realization test は仕様判断の起点ではないため、対応する oracle file を先に読む。
- CLI 実装、runtime helper、状態管理、path model、Codex wrapper、indexing 実装などの内部制御フローそのものを変更するために、まず実装本体を読むべきとき。
- 特定の細かい helper 関数や低レベル構造体の実装責務だけを確認したいとき。テスト期待値ではなく、対応する実装 module へ直接進む方が適切。
- Codex CLI や LLM の実出力品質、推論内容、自然文生成の良し悪しを検証したいとき。この領域の多くは fake 応答で cmoc 側の制御と観測結果を検証している。
- INDEX.md の本文生成規則、oracle 文書構成、routing 文書作成ルールそのものを調べたいとき。文書系の正本仕様または indexing 関連のより直接的な対象を読む。
- pytest の一般的な使い方や、プロジェクト全体の開発手順だけを知りたいとき。

## hash
- e88837902cc4ea0f0089e951329a7332788584e48b65f47536b753b461dff066
