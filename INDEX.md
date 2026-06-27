# `AGENTS.md`

## Summary
- cmoc リポジトリ全体で作業する AI 向けの基本指示をまとめる入口。プロジェクト名と略称、パス表記、INDEX.md を使ったルーティング、閲覧・編集禁止領域、oracle と実装・テスト配置の大枠を定める。
- 特に、正本仕様断片を oracle 配下に置き、実装を src、テストを test に置くという作業境界と、作業開始時に oracle 側のルーティング情報を確認する運用を示す。

## Read this when
- cmoc リポジトリで作業を始める前に、全体の作業規則・禁止事項・正本仕様と実装の関係を確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` などのパス表記が出てきて、リポジトリ内での意味や参照先を把握したいとき。
- oracle 配下を正本仕様断片として扱うべきか、src や test に実装・テストを書くべきかなど、作業対象の配置と責務境界を確認したいとき。
- 閲覧禁止・編集禁止の対象を確認し、作業で触れてよい領域と触れてはいけない領域を切り分けたいとき。

## Do not read this when
- 個別機能の詳細仕様、CLI の出力形式、パスモデルの厳密な定義などを確認したい場合は、ここではなく oracle 配下の該当する正本仕様断片へ進む。
- 既に全体作業規則を把握しており、特定の実装やテストの修正箇所を探しているだけなら、src や test 側のより直接の対象へ進む。
- INDEX.md エントリー生成やルーティング文書そのものの詳細基準を確認したい場合は、この全体指示ではなく、エントリー生成規則や関連する正本仕様断片を根拠にする。

## hash
- 3a1ea63ae7c7c50f65474c7a2c0f0e6884ad15e82af35e63fbd80fbee958f7d3

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
- 実行環境内の Python へ処理を渡すためのシェル製エントリーポイントを置く補助ディレクトリ。呼び出し位置からリポジトリルートと仮想環境 Python を決定し、通常実行時は仮想環境の存在と実行権限を確認してから本体へ委譲する。
- 仮想環境 Python が使えない場合に Markdown 形式のエラー、復旧手順、必要な実行ファイル、簡易的な call stack を出して失敗する起動ラッパーの挙動を扱う。補完プローブ時は本体へ渡せる場合だけ委譲し、仮想環境が使えない場合は詳細エラーを抑制して失敗する。

## Read this when
- CLI 起動直後にどの Python と本体スクリプトへ処理が渡るかを確認したいとき。
- 仮想環境が存在しない、実行権限がない、または初回セットアップ未完了のときに表示されるエラー文面や終了経路を確認したいとき。
- シェル補完の問い合わせ時だけ通常の missing venv エラーを抑制する挙動を確認したいとき。
- 起動ラッパー内で出力される call stack の行番号計算や、自己参照による行番号取得の仕組みを確認したいとき。

## Do not read this when
- Python 側の CLI 引数解析、サブコマンド実装、業務ロジック、または実行後の主要な処理内容を調べたいとき。
- 仮想環境の作成手順そのものやパッケージ設定の正本を調べたいとき。
- テストコード、oracle 由来の仕様断片、またはルーティング文書の生成規則を確認したいとき。
- リポジトリ内のパス概念全体や `<cmoc-root>` などの用語定義を調べたいとき。

## hash
- 06c5f5f4145b6aa6d3f881761b05f09b4fdf00336454e1336db384b724d37e98

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
- cmoc の realization implementation を置く Python 実装ルート。公開 CLI 入口、利用者向けサブコマンドの実行フロー、AI agent 呼び出し parameter と prompt 構築、共通 runtime helper、リポジトリ設定、基礎モデル・文書変換・パス解決など、oracle file の意図を実際の挙動へ接続するコードを扱う。
- 下位は、最上位 CLI 定義、サブコマンド orchestration、Codex 実行・設定・状態・Git・ログなどの横断基盤、agent prompt 部品と用途別 builder、設定 dataclass、AgentCallParameter や root token path などの基礎型へ分かれており、実装変更時に読む先を選ぶための入口になる。

## Read this when
- cmoc の実装コードを調査・変更し、CLI 入口、サブコマンド本体、共通 runtime、設定、AI agent 呼び出し構成、基礎モデルのどこへ進むべきか切り分けたいとき。
- init、tui、indexing、review oracle、apply、session など、利用者が実行する操作の command 定義、委譲先、実行順序、状態更新、worktree・branch・Git 操作、report 生成を追いたいとき。
- Codex exec/TUI 呼び出し、Structured Output 検証、profile/schema 準備、preflight、call log、サブコマンドログ、設定 JSON、session state、runtime path、利用者向けエラー表示など、複数機能から共有される runtime 処理を確認または変更したいとき。
- AI agent に渡す role、summary、goal、補助文脈、file access rule、routing rule、standard、model class、reasoning effort、Structured Output schema などの組み立てを確認または変更したいとき。
- AgentCallParameter、FileAccessMode、ModelClass、ReasoningEffort、RootToken、StructDoc、Standard など、実装全体で参照される基礎的な型・文書変換・パス解決の実装を確認したいとき。
- 新しい realization implementation を追加する前に、既存の責務境界、共有 helper、サブコマンド配置、公開 CLI 面、設定面、状態管理との重複や接続先を確認したいとき。

## Do not read this when
- oracle file の正本仕様断片そのもの、仕様文書、仕様上の用語定義、または人間が編集するべき要求内容を確認したいとき。実装ではなく oracle 側を読む。
- realization test の期待挙動やテスト fixture だけを確認したいとき。実装変更の入口ではなく、対応するテスト領域へ直接進む。
- README、AGENTS、補助スクリプト、プロジェクト設定、生成物、ログ、キャッシュなど、Python 実装ルート外の ancillary file だけを調べたいとき。
- 既に対象の下位ディレクトリまたは個別モジュールが特定できており、その責務だけを読めば足りるとき。
- 生成済みの INDEX.md や report の内容を読むだけで、生成・保存・commit・merge・agent 呼び出しの実装を調べないとき。

## hash
- e3302131d8b43287d3a5b0164ded1d3c6cba4fbed42c1e6f96645dc709bdaeb5

# `test`

## Summary
- cmoc の realization test 群を置く領域で、CLI サブコマンド、Codex 実行ラッパー、session/apply/review/indexing、prompt/schema、runtime 共通契約などの外部挙動と制御ロジックを検証する入口である。
- テスト補助 fixture も含み、一時 Git リポジトリ、fake Codex 実行、Codex home、linked worktree、state/report/log などを使って、oracle file 由来の意図が realization implementation で満たされているかを確認する。
- 大きなテストは個別機能の成功条件・拒否条件・cleanup・report・状態遷移を同じ文脈で読むために凝集しており、実装変更時の回帰確認先を選ぶためのルーティング階層として位置づけられる。

## Read this when
- cmoc の実装変更に対して、どの realization test が外部挙動、Git 副作用、状態更新、ログ、report、終了コード、出力内容を検証しているかを探すとき。
- session、apply、review oracle、indexing、init、tui、Codex runtime、prompt/schema、path model、file access、sandbox profile など、利用者から見える挙動や制御境界の期待値を確認・更新するとき。
- 新しいテストを追加する前に、既存の realization test へケース追加できるか、同じ観点のテストがすでに存在するかを確認するとき。
- fake external command、一時 Git リポジトリ、Codex home、linked worktree、session/apply state、report/log などの fixture や helper を使ったテストの書き方を確認するとき。
- oracle file ではなく、現在の realization implementation が満たすべき観測可能な挙動や回帰テスト上の契約を入口として把握したいとき。

## Do not read this when
- 正本仕様断片そのものを確認・変更したいとき。この領域は realization test であり、仕様判断の根拠は oracle file を優先する。
- プロダクト本体の実装、内部 helper、状態管理、path model、prompt builder、Codex runtime などの処理内容を直接修正したいだけで、既存テストの期待挙動をまだ確認する必要がないとき。
- 特定のサブコマンドや runtime 部品の挙動がすでに分かっており、対応する実装ファイルを読む方が直接的なとき。
- ルーティング文書、INDEX エントリー生成規則、oracle/realization の概念定義、または標準文書の本文を確認したいとき。
- 実際の Codex CLI や LLM の出力品質そのものを評価したいとき。この領域の多くは fake 実行や monkeypatch により cmoc 側の制御と副作用を検証している。

## hash
- 5ee2a3ffb20cc7cf9f550f64428d5deb0d7bc2e8d9896eec9a11ab974fb6baa3
