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
- cmoc の realization implementation 全体を収める領域。最上位 CLI の登録と起動、各サブコマンドの実行本体、共通 runtime helper、Codex subprocess 境界、git・state・config・logging・path・INDEX maintenance の実装、正本側実装へつなぐ互換 import 入口を扱う。
- 正本仕様そのものではなく、oracle file の意図を実行可能な Python 実装として具体化する場所であり、CLI から呼ばれる orchestration と複数機能で共有される runtime 境界への上位入口になる。
- ACP 型、path model、構造化文書、設定、ACP builder などは、この領域内で独自に正本を複製するのではなく、既存 import 経路を保つための薄い再公開や adapter を通じて正本側実装へ接続される。

## Read this when
- cmoc の CLI コマンド構成、サブコマンドから実装関数への委譲、または console script 起動後にどの実行本体へ進むかを調べたいとき。
- session、apply、review oracle、init、indexing、TUI などの利用者向け操作が、git worktree、branch、state、report、Codex exec/TUI 呼び出しをどう組み合わせて実行されるか追い始めるとき。
- 複数サブコマンドから共有される runtime helper、設定読み書き、エラー表示、ログ、path 解決、内容 hash、git wrapper、session state、Codex profile・schema・quota/capacity retry などの実装境界を確認または変更したいとき。
- 既存の公開 import 経路を壊さずに、ACP 型、path model、構造化文書、設定、oracle package、ACP builder を正本側実装へ接続している互換層や削除条件を確認したいとき。
- INDEX.md 更新の実行機構、対象抽出、hash による再生成判定、Structured Output 検証、Markdown 生成、更新 commit、Codex 実行前 preflight の実装を調べたいとき。
- oracle file で述べられた要求が realization implementation 上でどの関数、状態遷移、外部コマンド呼び出し、出力、永続ファイル操作として具体化されているか確認したいとき。

## Do not read this when
- 正本仕様断片、利用者向け要求、prompt 内容、file access rule、path placeholder の意味など、人間意図そのものを確認したいとき。その場合は oracle 側の本文を読む。
- 実装ではなく realization test の検証観点、fixture、期待挙動、回帰テストを確認または変更したいとき。その場合はテスト領域へ進む。
- 特定の下位責務が既に分かっており、CLI 登録、共通 runtime、サブコマンド本体、互換 import 入口、ACP builder adapter のいずれかへ直接進めるとき。この上位領域全体を広く読む必要はない。
- 生成済み INDEX.md の文面やルーティング内容だけを確認したいとき。この領域は目次生成・更新の機構を含むが、個別目次本文の正本ではない。
- README、パッケージ設定、補助スクリプト、またはリポジトリ外部の運用情報だけを調べたいとき。cmoc の Python 実装に関係しない対象は別領域を読む。

## hash
- f0f4103ac55b093ef56e1a4b9538113b35f399b1d778d06a2fa2bcf533c60be0

# `test`

## Summary
- cmoc の realization test 群への入口。session、apply、review oracle、indexing、init/TUI、Codex runtime、prompt 構築、共通 runtime など、CLI 外部挙動と制御ロジックの回帰観点を機能別のテスト本文へ振り分ける。
- 個別テストは正本仕様ではなく、oracle file で述べられた人間意図を realization implementation がどう具体化しているかを、git worktree、状態ファイル、Codex 呼び出し、レポート、ログ、終了コードなど観測可能な副作用で固定するための対象である。
- 共通補助関数、fake Codex executable、一時 Git repository、linked worktree、process cleanup、quota retry など、外部コマンドや状態遷移を伴うテストの前提と期待値を探す起点になる。

## Read this when
- realization implementation の変更により、CLI 出力、終了コード、git branch/worktree、状態ファイル、ログ、report、Codex 呼び出し引数など、利用者または外部から観測できる挙動が変わる可能性があるとき。
- session fork/join/abandon、apply fork/join/abandon、review oracle、indexing、init/TUI、Codex runtime、prompt builder、runtime 基盤のいずれかについて、既存の回帰観点や境界条件を確認してから実装を変更したいとき。
- Codex CLI 連携、quota/capacity retry、CODEX_HOME 検証、sandbox/profile/schema/prompt/log の扱い、外部 apply tracking や process group 制御など、Codex 実行 wrapper 周辺の外部契約を確認したいとき。
- INDEX.md 生成・更新、routing document preflight、fresh hash、malformed entry、merge conflict 解決、linked/apply worktree 上の indexing 挙動をテスト観点から確認したいとき。
- realization test を追加・変更する前に、既存テストへケース追加できるか、同じ観点の fixture や helper が既にあるか、どのテスト本文を読むべきかを絞り込みたいとき。

## Do not read this when
- oracle file の正本仕様断片、利用者向け仕様、概念定義そのものを確認したい場合は、ここではなく oracle 側の該当本文を読む。
- 実装本体の責務分割、内部 helper、データ構造、アルゴリズムを直接変更する場合は、期待される外部挙動の確認が必要な時だけこの領域を併読し、まず対応する実装側を読む。
- 個別機能に関係しない一般的な repository 構成、path model、INDEX routing 規約、oracle/realization の分類を知りたいだけなら、専用の正本仕様や基礎文書を読む。
- Codex CLI や LLM の応答品質そのものを評価したい場合は、この領域を読まなくてよい。ここで扱う多くのテストは fake executable や制御された出力で cmoc 側の制御ロジックだけを検証する。
- 単にテストを実行したいだけで、失敗箇所の意味や期待挙動を調べる必要がない場合は、対象本文を読む前にテスト runner の出力から該当ファイル・ケースを特定する。

## hash
- b796e20df73515c77e77acd342b7465bd71b2c0dc291b3f9adf32cabfe05b6b3
