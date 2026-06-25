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
- cmoc の最上位向け案内として、プロジェクトの略称と位置づけ、初期セットアップ手順、基本ワークフローの参照先、端末操作上の注意を短く示す。
- 詳細な開発ルールや AI 向け作業指示は別文書へ委ね、利用開始前にまず全体像と導入手順を確認する入口になる。

## Read this when
- cmoc が何をするための最小外部ツールなのか、略称が何を指すのかを最初に確認したいとき。
- リポジトリを clone した直後に、Python 仮想環境の作成、編集可能インストール、任意のコマンドパス設定を確認したいとき。
- 基本ワークフローの詳しい説明へ進む前に、どの正本仕様断片を読めばよいかを知りたいとき。
- 端末で Ctrl+S を誤入力した際のロック挙動や、それを無効化するためのシェル設定例を確認したいとき。

## Do not read this when
- AI が従うべき詳細な作業規則、ファイルアクセス規則、ルーティング規則を確認したいときは、本文が参照している AI 向け指示文書へ進む。
- cmoc の基本ワークフローや具体的な利用手順そのものを確認したいときは、本文が示す usage 系の正本仕様断片へ進む。
- 実装、テスト、内部のパスモデル、CLI 挙動の詳細を調査したいときは、この概要ではなく該当する仕様断片または実装領域を直接読む。
- すでにセットアップが済んでおり、プロジェクト概要や端末ロック対策を確認する必要がない作業では読む優先度は低い。

## hash
- e7f8b64d5a986f5bb2a696a71e2d6327bdc6d2cc72c909d0b6e2832c5c7df09a

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
- 開発環境向けのワークスペース設定で、リポジトリ全体を単一の作業フォルダとして開く前提を定義している。
- エディタ上で生成物やルーティング文書を非表示にする対象、Python と Markdown の編集設定、Python 解析対象と追加 import 探索パスをまとめて扱う。
- 実装・正本仕様断片・テストを同じワークスペース内で参照しながら作業するための補助設定であり、プロダクトの実行時仕様そのものではない。

## Read this when
- VS Code 系エディタでの作業対象、非表示ファイル、フォーマッタ、保存時整形、言語別インデント設定を確認したいとき。
- Python 解析がどのソースツリーやテストツリーを対象にし、どの追加探索パスを使うかを確認したいとき。
- エディタ上でルーティング文書やキャッシュ系生成物が表示されない理由を確認したいとき。

## Do not read this when
- CLI の外部挙動、コマンド仕様、出力形式、状態管理などのプロダクト仕様を確認したいとき。
- 実装コードやテストコードの責務、制御フロー、個別モジュールの変更点を調べたいとき。
- 正本仕様断片の内容や、実装が従うべき人間意図を確認したいとき。

## hash
- a486d130bc988b4be2adee6368d38bc0e0e7ac3825cc1fb472075109c8b5805a

# `oracle`

## Summary
- cmoc の人間所有の正本仕様断片を集める領域。自然言語で書かれた CLI 挙動・開発規則・設計判断と、プログラミング言語や schema で書かれた agent call parameter、prompt、基礎モデル、設定仕様などを扱う。
- realization file が従うべき人間意図、公開挙動、実装・テスト時の制約、AI に任せてよい未定義部分の境界を確認するための入口になる。

## Read this when
- cmoc の実装やテストを変更する前に、正本仕様断片として定められた要求、non-goal、用語、公開挙動、状態管理、開発規則を確認したいとき。
- CLI サブコマンド、run 隔離、branch / worktree モデル、session state、ログ、エラー処理、補完、インデクシング、Codex CLI 呼び出し境界など、利用者に見える挙動や永続状態をまたぐ仕様の読む先を選びたいとき。
- AI エージェント呼び出しパラメータ、prompt 構築、Structured Output schema、パス表記、設定値、構造化文書 helper など、実装形式で定義された正本仕様断片を根拠にしたいとき。
- oracle file と realization file の責務分担、人間と AI の編集権限、正本仕様断片の疎な書き方、INDEX.md エントリーの作り方など、cmoc 固有の仕様管理ルールを確認したいとき。
- 既存実装や一般的なベストプラクティスよりも、cmoc の正本仕様断片を優先すべき判断かどうかを確認したいとき。

## Do not read this when
- 現在の Python 実装、テスト、helper、CLI 配線、git 操作、プロセス起動、画面描画、ファイル保存など、realization implementation の具体的なコード構造だけを調べたいとき。
- 正本仕様ではなく、既存の realization test が現在どの挙動を検証しているかだけを確認したいとき。
- 対象の個別仕様、agent call parameter builder、設定モデル、パスモデル、サブコマンド仕様など、読むべき下位の正本仕様断片がすでに明確なとき。
- 生成済みキャッシュ、一時ファイル、実行ログ、ローカル作業メモのような正本仕様断片ではない情報を探しているとき。
- INDEX.md の既存内容やルーティング文書そのものの現状確認が目的で、本文仕様を根拠にした判断を行わないとき。

## hash
- c582b719b795fc877f704ef3ebb5ad374a077f2579e6f4abec441d2cf84b18db

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
- cmoc の realization implementation 全体を収める実装入口。最上位 CLI の組み立て、サブコマンド本体、共通 runtime helper、設定モデル、基礎データ構造、エージェント呼び出しパラメータ生成、互換 import 入口を扱う。
- CLI 表層から command orchestration、Codex CLI 呼び出し準備、Git/worktree/state/log/path などの共通処理、oracle/realization/INDEX.md 関連の prompt 生成まで、実装側の主要領域へ進むための起点になる。
- 下位要素は、CLI 入口、個別サブコマンド、共有 runtime、設定、基礎モデル、agent prompt/schema builder、互換 runtime import に分かれており、作業対象の責務に応じてより直接の下位ディレクトリまたはファイルへ進む。

## Read this when
- cmoc の実装ファイル全体から、どの領域に進むべきかを判断したいとき。
- CLI 起動入口、サブコマンド実行本体、共通 runtime helper、設定データ構造、基礎モデル、エージェント呼び出し契約のうち、調査対象の責務境界を切り分けたいとき。
- init、tui、indexing、session、apply、review などの利用者向け操作が、CLI 登録、サブコマンド orchestration、共通 helper、agent prompt builder のどこで扱われるかを確認したいとき。
- Codex CLI 呼び出し、Structured Output schema、file access mode、model/reasoning effort、sandbox/profile、runtime state、Git worktree、INDEX.md maintenance などの実装上の入口を探したいとき。
- oracle file を正本とする realization implementation の配置を確認し、実装変更前に読むべき下位領域を選びたいとき。

## Do not read this when
- 正本仕様断片そのもの、oracle file と realization file の概念定義、path keyword の正本的な説明、INDEX.md エントリー規則などを読みたいとき。その場合は oracle 側の仕様本文へ進む。
- 自動テスト、fixture、テストケース追加先を探しているとき。その場合は realization test 側へ進む。
- README、AGENTS、補助スクリプト、パッケージ設定、生成物、ログ、保存済み report など、実装ソース以外の補助ファイルを確認したいとき。
- すでに対象サブコマンド、共通 helper、設定モデル、agent prompt builder などが特定できているとき。その場合はこの階層で止まらず、該当する下位対象を直接読む。
- 特定の生成済み INDEX.md や過去の review/apply/session 状態の内容を確認したいだけのとき。

## hash
- aa57e6ea2b3148824aa4dc03207163f796cb7b6722001b69cbd00fc3844da7be

# `test`

## Summary
- cmoc の realization test 群を収める領域。CLI サブコマンド、Codex runtime、session/apply lifecycle、indexing/review、prompt builder、基本 runtime、共通 test support など、実装が外部挙動・状態更新・ログ生成・権限制御を満たしているかを確認する入口になる。
- 個別テストは実 Codex/LLM の品質ではなく、fake や fixture を使って cmoc 側の制御ロジック、git/worktree 副作用、永続状態、出力、エラー境界を検証する。共通 helper は一時 git repository、CODEX_HOME、runner、apply worktree 復元など、複数テストで使う前提環境を集約している。

## Read this when
- realization implementation の変更に対して、対応する CLI 外部挙動、状態遷移、git/worktree 副作用、ログ、エラー出力、権限 profile、preflight などの回帰テストを確認・追加・更新したいとき。
- apply、session、init、tui、indexing、review oracle、Codex runtime、prompt builder、基本 runtime のいずれかについて、仕様断片が実装上どう検証されているかを realization test 側から確認したいとき。
- 新しいテストを追加する前に、既存の同観点テストや共通 fixture へケース追加・集約できるかを確認したいとき。
- テスト用 repository、Codex home、fake Codex 呼び出し、CLI runner、apply worktree path など、複数テストで共有される setup や helper を探したいとき。

## Do not read this when
- oracle file の正本仕様断片そのものを確認したいときは、oracle 側の本文を読む。
- CLI command、runtime、path model、state 管理、Codex wrapper などの実装本体を変更する入口を探しているだけなら、対応する realization implementation を読む。
- Codex CLI や LLM の応答品質そのものを評価したいとき。この領域のテストは外部 Codex 呼び出しを fake 化し、cmoc 側の制御を検証する。
- 個別サブコマンドや機能のテスト対象が分かっている場合は、この領域全体ではなく該当する個別テストまたは共通 support に直接進む。

## hash
- 45d9625e41a055814d819be4abe8facdc770043748230d69fd6420d04e9c26ec
