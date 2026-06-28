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
- cmoc の realization implementation を収める実装階層。公開 CLI 入口、利用者向けサブコマンド、共通 runtime helper、Codex exec/TUI 呼び出し境界、git・path・config・state・logging などの実行基盤、ACP 呼び出しパラメータ生成、正本側定義への互換 import 入口がここに配置されている。
- この階層は正本仕様断片ではなく、oracle file の意図を具体化する実装本文への入口である。CLI からどの処理へ委譲されるか、実行時副作用がどこで扱われるか、共有 helper と個別サブコマンドの境界を切り分けるために使う。
- 内容は、実処理を持つ runtime module・サブコマンド実装と、正本側または既存実体へ委譲する薄い互換層が混在している。具体挙動を読む場合は、CLI 構成、サブコマンド lifecycle、共通 runtime、ACP builder、basic/config 互換層のいずれが対象かをここから判断して下位へ進む。

## Read this when
- cmoc の実装を変更・調査するために、CLI 入口、サブコマンド実装、共通 runtime helper、ACP builder、互換 import 層のどこへ進むべきかを切り分けたいとき。
- 利用者が実行する cmoc コマンドの登録、option、サブコマンドグループ、引数解析エラー処理、console script 起動から実装関数への委譲関係を確認したいとき。
- session、apply、review、init、indexing、TUI 起動などの実行入口、事前条件、branch/worktree/state/report/log への副作用、成功時・失敗時の出力制御を追いたいとき。
- Codex exec/TUI 呼び出し、Structured Output 検証、profile/schema 準備、capacity/quota retry、call log、preflight indexing など、Codex subprocess 境界の実装を確認または変更したいとき。
- cmoc が共有する git 操作、path 解決、設定読み書き、session state 永続化、ログ、エラー表示、実行結果型、content hash、ignore 保証などの runtime 基盤を探したいとき。
- ACP に渡す prompt、model class、reasoning effort、file access mode、structured output schema path などの agent call parameter 生成箇所を、apply、indexing、review、session、TUI などの用途別に探したいとき。
- realization implementation 側で、path model、struct doc、config などの正本側定義が独自実装なのか再公開なのか、また互換 import path がどこで成立しているかを確認したいとき。

## Do not read this when
- 正本仕様断片そのもの、oracle file の要求、CLI 出力仕様の人間意図、path keyword の概念定義、oracle と realization の責務境界を確認したいとき。その場合は oracle 側の本文を読む。
- テスト観点、fixture、期待値、外部挙動の検証内容を調べたいとき。その場合は realization test 側を読む。
- README、開発者向け説明、補助ファイル、パッケージ設定、ビルド設定、管理対象外メモなど、実装本文以外の補助情報を探しているとき。
- 個々の正本側定義の詳細、たとえば path model の token 仕様、構造化ドキュメントの検証規則、設定項目の意味や制約を確認したいだけのとき。realization 側の薄い再公開入口ではなく、正本側の実体を直接読む。
- 特定サブコマンドの利用者向け仕様だけを確認したいとき。実装順序や副作用ではなく仕様意図が必要なら、対応する oracle doc を読む。
- INDEX.md エントリーの生成規則、ルーティング文書の標準、oracle/realization standard の方針そのものを確認したいとき。実装階層ではなく正本仕様側の規約本文を読む。

## hash
- 7f3dc690e31028633d71c8311203f40d91620ff591aabede3bb992f9dc7fc0b3

# `test`

## Summary
- cmoc の realization test 群を集約する階層で、CLI サブコマンド、Codex 実行ラッパー、runtime 基盤、prompt/ACP builder、indexing、review oracle、session/apply 系ワークフローの外部挙動と回帰条件を検証する。
- 共通補助関数により一時 Git リポジトリ、Codex home、fake Codex 実行、worktree/session/apply 状態の準備を共有し、個別テストは利用者から見える出力、終了コード、Git 副作用、状態ファイル、report、cleanup 境界を固定する入口になっている。
- realization test の階層であり、oracle の正本仕様そのものではなく、oracle file と既存実装から具体化された挙動が壊れていないかを確認するための読み先を選ぶ場所である。

## Read this when
- CLI の外部挙動、終了コード、stdout/stderr、report、状態ファイル、Git branch/worktree 副作用に関する回帰テストを探すとき。
- apply fork/join/abandon、session fork/join/abandon、init、TUI 起動前処理、indexing、review oracle のどの realization test を読むべきか切り分けたいとき。
- Codex CLI 呼び出しの profile 生成、CODEX_HOME 解決、sandbox/file access mode、retry、quota retry、process group 追跡など、runtime_codex 周辺の期待挙動をテストから確認したいとき。
- prompt part、AgentCallParameter builder、structured output schema、oracle source との整合、routing/file access rule の prompt 組み立て結果を検証するテストを探すとき。
- 基礎 runtime の path token、root/run/work root、linked worktree、設定検証、CmocError 表示、subcommand log、binary 判定、.cmoc ignore など、個別サブコマンドより下位の共通契約を確認したいとき。
- 新しい realization test を追加する前に、既存の同じ観点のテストや共通 fixture へ統合できるか確認したいとき。

## Do not read this when
- 正本仕様断片を確認・変更したい場合は、realization test ではなく oracle 側の本文を読む。
- 実装本体の関数、クラス、内部 helper、状態更新処理そのものを変更する場合は、期待される外部挙動を確認した後、対応する実装側を読む。
- 個別機能の挙動がすでに分かっており、単に実装箇所だけを探したい場合は、src 側の該当階層へ直接進む。
- Codex CLI や LLM の出力品質そのものを評価したい場合は、この階層を読む必要は薄い。多くのテストは fake/stub 実行で cmoc 側の制御と副作用を検証している。
- routing document のエントリー生成規則や oracle/realization の概念定義そのものを確認したいだけなら、該当する標準・oracle 文書を読む。

## hash
- d13ba28b0c2809e0b43f85819e7469bdafde81153e23248fe55038a97a01f36a
