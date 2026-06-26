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
- cmoc の人間所有の正本仕様断片を集約する領域。自然言語で書かれた利用者向け挙動・git/session/run モデル・設計判断・開発規則と、プログラムや設定として書かれた AI 呼び出しパラメータ、標準プロンプト部品、共通型、パス語彙、設定構造などへの入口になる。
- 実装やテストの変更前に、正本仕様として確認すべき内容が、自然言語仕様なのか、AI 呼び出しや共通値を定義する仕様実装なのかを切り分けるために読む対象である。

## Read this when
- cmoc の実装・テスト・利用手順・CLI 挙動について、正本仕様断片を根拠に作業判断を始めたいとき。
- サブコマンド、実行時状態、ログ、エラー処理、Codex CLI 呼び出し、プロンプト、インデクシング、run 隔離、利用ワークフローなどの仕様確認先を探したいとき。
- session、run、apply、review に関わる branch、commit、linked worktree、隔離境界、merge 先などの用語やモデルを確認したいとき。
- AI エージェントへ渡す role、summary、goal、補助文脈、ファイルアクセス権限、モデル種別、reasoning effort、Structured Output schema の仕様を確認したいとき。
- 正本仕様断片と realization の責務分担、開発時に守るべき oracle standard・realization standard・index entry standard の考え方を踏まえて作業したいとき。

## Do not read this when
- 既存 realization code の具体的な関数、クラス、現在の内部ロジック、テスト期待値だけを調べたいとき。
- CLI 引数解析、プロセス制御、git 操作、永続状態の読み書き、端末 UI 描画など、実行フロー本体の実装箇所がすでに目的になっているとき。
- 個別の正本仕様断片がすでに特定できており、その本文だけを直接読めばよいとき。
- 対象ファイルの差分や本文そのものを読んで、patch 内容、merge conflict、所見の妥当性、具体的な修正方針を判断する段階に入っているとき。
- 生成物、実行ログ、一時ファイル、または正本仕様ではない補助的な実体を探しているとき。

## hash
- 42bb304b18d106c861bf60896e86c3c9f527503ac9fedc4878e4f3d6f76bfb35

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
- cmoc の realization implementation 全体を置く実装領域。Typer による CLI 入口、init・tui・indexing・review・session・apply のサブコマンド本体、Codex 呼び出しや Git・設定・ログ・状態管理を支える共通 runtime、リポジトリ別設定 dataclass、root token 付き path や AgentCallParameter などの基礎モデル、AI agent に渡す prompt と Structured Output parameter の組み立てを扱う。
- 正本仕様本文ではなく、oracle file で述べられた意図を具体化する実装コードへの入口である。利用者向け CLI 挙動、実行時の状態遷移、外部コマンド連携、AI 呼び出し条件、共有モデルのどこを読むべきかを切り分ける起点になる。

## Read this when
- cmoc の実装本体を調査または変更したいとき。特に CLI command から実行本体、共有 runtime、設定値、基礎データ型、AI agent 呼び出しパラメータ生成のどこへ進むべきかを判断したいとき。
- 利用者が実行する init、tui、indexing、review oracle、session fork/join/abandon、apply fork/join/abandon の処理フロー、事前条件、git・worktree・state・report・出力との接続を追いたいとき。
- Codex exec/TUI 呼び出し、Structured Output 検証、設定ファイル入出力、共通エラー表示、JSON Lines ログ、hash 付き保存、Git wrapper、root/path 解決、session state など、複数機能で共有される runtime 実装を確認したいとき。
- AgentCallParameter、FileAccessMode、ModelClass、ReasoningEffort、root token、規範文書構造、階層化 Markdown 生成など、上位処理から参照される共有モデルや小さな変換処理を確認したいとき。
- AI agent に渡す role、goal、補助 prompt、ファイルアクセス制約、標準文書部品、Structured Output schema、用途別 parameter builder を確認または変更したいとき。
- oracle file の仕様意図を realization code としてどのように具体化しているか、または実装とテストの対応を追うために実装側の入口を探したいとき。

## Do not read this when
- oracle file の正本仕様断片そのもの、oracle standard、realization standard、INDEX.md 生成規則など、人間が所有する仕様本文を確認したいだけのとき。仕様本文を読む必要がある場合は oracle 側へ進む。
- realization test のテストケース、fixture、期待される外部挙動の検証観点だけを調べたいとき。実装ではなくテスト本文へ直接進む方が適切である。
- README、AGENTS、補助スクリプト、gitignore など、実装本体ではない ancillary file の内容を確認したいとき。
- 既に調査対象が特定のサブコマンド、runtime helper、prompt builder、基礎モデル、設定モデルに絞れているとき。全体入口ではなく該当する下位ファイルまたは下位ディレクトリを直接読む方がよい。
- 生成済みまたは既存の INDEX.md の内容を評価したいだけのとき。ここは INDEX.md 本文ではなく、INDEX.md が案内する realization implementation の本文領域である。

## hash
- 173ee4598b308b6bd5138683667631c72e35ddea4b7e5740f541385eaaab1e7e

# `test`

## Summary
- cmoc の realization test 群を収める領域で、CLI サブコマンド、Codex 実行ラッパー、INDEX 更新、prompt/schema builder、runtime 基本契約などの外部挙動と制御ロジックを検証する。
- 一時 Git リポジトリや fake external command を使う共有 fixture も含み、実装変更後にどの利用者向け挙動・副作用・状態更新を確認すべきかを探す入口になる。
- 正本仕様そのものではなく、oracle file から具体化された realization code の回帰確認として読む対象である。

## Read this when
- CLI サブコマンドの終了コード、標準出力・標準エラー、Git branch/worktree 操作、状態ファイル更新、cleanup、report 生成など、利用者から見える挙動を変更または検証するとき。
- Codex CLI 呼び出し、TUI 起動、CODEX_HOME、profile 生成、sandbox/file access、ログ保存、quota/capacity/schema retry など、外部 Codex 実行ラッパーの挙動を確認するとき。
- INDEX.md 生成・更新・preflight・conflict 解決・hash freshness・root 直下 memo 除外など、indexing 系の実装変更に対する回帰観点を探すとき。
- prompt part、structured output schema、builder parameter、file access rule、各種標準文書を含む最終 prompt の期待値を確認するとき。
- session/apply/review oracle/init/tui など複数機能にまたがる realization test の配置を把握し、より具体的なテストファイルへ進む入口が必要なとき。
- テスト用の一時リポジトリ、認証済み Codex home、fake executable、Git helper、worktree path 解決など、共有 fixture や helper を使う・変更するとき。

## Do not read this when
- oracle file に書かれた正本仕様断片そのものを確認したいとき。仕様判断の根拠は oracle 配下の本文を優先する。
- プロダクト本体の実装責務、内部 helper の設計、状態管理や path model の実装詳細を先に理解したいときは、実装側の対象へ直接進む。
- 特定サブコマンドや機能のテスト期待値が既に分かっており、対応する個別テストへ直接進めるとき。
- Codex CLI や LLM の実出力品質そのものを評価したいとき。この領域の多くは fake 応答や monkeypatch により cmoc 側の制御と副作用を検証する。
- 一般的な pytest/Typer runner の使い方だけを調べたいとき。cmoc 固有の外部挙動や fixture に関係しないなら対象外である。

## hash
- aa5265eb4d2d3db252077149f9965ddbc458c447df4062ca81c691f023e6e549
