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
- cmoc の realization implementation 全体を置く領域であり、公開 CLI 入口、利用者向けサブコマンド実装、共通 runtime helper、設定・basic・ACP などの互換 import 入口を束ねる。
- CLI 登録から、session・apply・review・indexing・TUI・init の実行入口、Codex subprocess 境界、git/worktree/state/config/log/path/error などの横断処理へ進むための実装側の起点になる。
- 正本仕様断片そのものではなく、oracle 側の定義や builder 実装を再公開する薄い接続層と、cmoc の実処理を担う runtime module・サブコマンド module が混在するため、具体調査では下位の責務別対象へ進む。

## Read this when
- cmoc の実装側で、CLI コマンド構成、サブコマンドの実行入口、共通 runtime helper、または oracle 側実装への互換 import 経路のどこから読み始めるべきか切り分けたいとき。
- 利用者操作としての init、INDEX maintenance、TUI 起動、session lifecycle、apply lifecycle、review oracle のいずれかの実装入口を探したいとき。
- Codex exec/TUI 呼び出し、Structured Output 検証、preflight indexing、quota/capacity retry、ログ、設定、状態永続化、path 解決、git/worktree 操作、共通エラー表示など、複数機能にまたがる実行基盤を確認または変更したいとき。
- 正本側 basic・config・ACP builder 実装が realization implementation 側からどの公開名や import path で参照されるか確認したいとき。
- oracle file に書かれた意図が、実装側の CLI、runtime、サブコマンド制御、互換入口としてどのように具体化されているか追いたいとき。

## Do not read this when
- 正本仕様断片、用語定義、path keyword、oracle file と realization file の責務分担、サブコマンドの仕様意図そのものを確認したいとき。その場合は oracle 側の本文を読む。
- テストの期待値、fixture、外部挙動の検証内容、回帰確認の観点を調べたいとき。その場合は realization test 側へ進む。
- README、開発補助ファイル、パッケージ設定、gitignore など、実装ソース以外の補助的な repository 構成だけを調べたいとき。
- 個別 helper や個別サブコマンドの具体的な入出力、副作用、例外条件だけを調べたいときは、この領域全体ではなく、CLI 入口、共通 runtime、サブコマンド、互換 import 入口など責務が一致する下位対象へ直接進む。
- oracle 側実装の型、builder parameter、path model、struct doc、config 定義の実体を調べたいとき。この領域の一部は再公開入口なので、具体内容は再公開元の正本側実装を読む方が直接的である。

## hash
- 53a905bf28b5219229328cf9c59cd4d7340d6deb2727f674e4ae3c29806f4560

# `test`

## Summary
- test 配下の realization test と共通テスト補助の入口。CLI サブコマンド、Codex runtime、prompt 構築、indexing preflight、基礎 runtime の外部挙動を pytest で固定する。
- 個別テストは apply/session/review/init/indexing/runtime などの実行副作用、Git worktree・branch・state・report・ログ・Codex 呼び出し制御を検証し、共通補助は一時 Git repository や fake Codex 実行環境を組み立てる。
- cmoc の実装変更が既存の CLI 契約や runtime 境界を壊していないかを確認するため、対象機能ごとのテスト本文へ進む上位入口になる。

## Read this when
- cmoc の realization test 全体から、変更対象機能に対応する pytest ファイルを選びたいとき。
- CLI サブコマンド、Codex runtime、prompt/indexing preflight、基礎 runtime の外部挙動や回帰条件をテストで確認・変更したいとき。
- Git worktree、branch、session/apply state、report、ログ、fake Codex 実行などを伴う統合的なテストの配置を探すとき。
- 新しい realization test を追加する前に、既存テストへケース追加・統合できる場所や共通補助の入口を確認したいとき。

## Do not read this when
- 正本仕様断片を確認したい場合は、この realization test 群ではなく oracle 配下の本文を読む。
- 実装本体の責務分割、内部 helper、状態 schema、CLI 関数の処理詳細だけを変更したい場合は、対応する src 配下の実装を先に読む。
- 個別機能に対応するテストファイルが既に分かっている場合は、このディレクトリ入口ではなくそのテスト本文へ直接進む。
- Codex CLI や LLM の実出力品質を検証したい場合は読まない。ここでは fake/stub を使い、cmoc 側の制御と外部副作用を検証する。

## hash
- 116389f7bfe908d8ccc0e67106b0e25818267b5ab319b5a36f92cb3ea73617f8
