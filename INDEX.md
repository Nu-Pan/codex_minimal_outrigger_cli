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
- cmoc の正本仕様断片を集める領域であり、人間が責任を持つ oracle file の定義、realization file との関係、正本から実装へ流れる責務境界を確認する入口。自然言語仕様、プログラム・設定形式の仕様断片、テスト形式の仕様断片へ進む上位階層として機能する。
- oracle file を小さく矛盾なく保ち、人間の認知負荷を節約しながら、実装差を避けたい事項だけを正本仕様断片として明示するための標準を扱う。未定義部分を AI 裁量で補ってよい範囲、用語・命名、non-goal、ベストプラクティスより正本を優先する判断基準も含む。
- realization file の品質・規模・責務分割・公開面・依存関係・テスト肥大化を抑える実装側標準と、INDEX.md エントリーを本文へのルーティング情報として作るための基準を含む。下位には、自然言語 Markdown の仕様文書群と、AI 呼び出しパラメータや共通値を定義するプログラム形式の仕様断片がある。

## Read this when
- oracle file と realization file の定義、所有者、編集責任、正本仕様断片と実装成果物の関係を確認したいとき。
- oracle を正本として realization を実装・修正・テストする前に、人間が明示すべき仕様と AI 裁量で補ってよい未定義部分の境界を確認したいとき。
- oracle file を追加・修正・レビューする際に、人間の認知負荷、仕様断片の疎さ、矛盾禁止、用語統一、命名、non-goal 記述、実装から仕様への逆流禁止といった正本側の標準を確認したいとき。
- realization file を追加・変更・整理する際に、コード量最小化、責務分割、既存実装との統合、抽象化の根拠、公開面や永続状態の増加抑制、テストや依存関係の肥大化抑制を確認したいとき。
- INDEX.md エントリーを生成・評価する際に、対象を読むべき条件、読まなくてよい境界、機械的識別情報を混ぜない方針など、ルーティング文書としての品質基準を確認したいとき。
- cmoc の正本仕様全体から、自然言語仕様文書、プログラム・設定形式の仕様断片、テスト形式の仕様断片のどこへ進むべきかを判断したいとき。

## Do not read this when
- 特定の CLI サブコマンド、session/run の branch・worktree モデル、ログ、エラー処理、状態、インデクシング、不採用設計案などの自然言語仕様本文が読みたいだけなら、下位の自然言語仕様文書群へ直接進む。
- AI エージェント呼び出しパラメータ、標準プロンプト部品、Structured Output schema、パス語彙、設定構造など、プログラム・設定形式の正本断片だけを確認したいなら、下位の該当領域へ直接進む。
- CLI 引数解析、git 操作、状態ファイルの読み書き、端末 UI、実装関数、テスト fixture など realization 側の現在の内部ロジックを調べたいときは、正本仕様ではなく実装・テスト側の該当箇所を読む。
- 対象ファイルや対象サブディレクトリが既に明確で、その本文を読む判断が済んでいるときは、この上位入口ではなく対象本文へ直接進む。
- 生成済みの INDEX.md に書かれている現在のルーティング記述そのものを確認したい場合。ただし INDEX.md エントリーの作成基準や評価基準を確認する場合は読む。

## hash
- 5e7d2d271f01bd9a8a74a8e23588e230e5602510d8336715026ce26ba2b76ff0

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
- cmoc の realization implementation を収める実装領域。CLI 入口、サブコマンド本体、共通 runtime、設定モデル、AI agent 呼び出しパラメータ構築、パス・構造化文書・標準規範などの基礎部品を扱う。
- 利用者向けコマンドの公開面から、Git/worktree/state/config/Codex CLI 実行などの共通処理、さらに review・apply・session・indexing・tui の業務フローまで、cmoc の実行挙動を追うための主要な入口になる。

## Read this when
- cmoc の実装本体、CLI サブコマンド、実行時制御、AI agent 呼び出し、設定値、状態管理、Git 操作、INDEX 更新、review/apply/session/tui の処理を確認または変更したいとき。
- 正本仕様断片に対して、実際の realization implementation がどのように具体化されているかをコードから追いたいとき。
- CLI で公開されるコマンド階層、引数、エラー表示、stdout/report 生成、終了時の状態更新など、利用者から見える挙動の実装入口を探したいとき。
- Codex CLI の exec/TUI 呼び出し、prompt・Structured Output schema・file access mode・model/reasoning 設定の組み立てや実行境界を調べたいとき。
- work root/repo root/path keyword 解決、設定ファイル、session/apply state、実行ログ、report、worktree、branch、git status など、複数機能で共有される runtime helper の所在を切り分けたいとき。

## Do not read this when
- 人間が所有する正本仕様断片そのもの、oracle file の記述方針、概念定義、仕様上の要求を確認したいとき。その場合は oracle 側の本文を読む。
- テスト期待値、fixture、外部挙動の検証観点、回帰テスト追加先を確認したいとき。その場合は test 側を読む。
- プロジェクト全体の導入説明、利用者向け README、パッケージ設定、依存関係定義、補助スクリプトだけを確認したいとき。
- 生成済みルーティング文書の内容や、INDEX.md エントリー自体の現在値だけを確認したいとき。
- 実装変更ではなく、正本仕様断片の修正提案や人間判断が必要な仕様整理を行うとき。

## hash
- 18f9d452250ba6ace7b04a6467b21cac3d3ab8ff632145ff02e82d30629cccfd

# `test`

## Summary
- cmoc の realization test 群を収める領域。CLI サブコマンド、Codex runtime、indexing、prompt 生成、path・権限・設定などの外部挙動と制御ロジックを、実際の一時 git repository や fake Codex 実行環境を使って検証する。
- 共通 fixture/helper によるテスト環境構築を入口に、apply、session、init/TUI、review oracle、INDEX 更新、Codex 呼び出し retry/home/exec、基本 runtime など、src 側実装の realization が正本仕様断片と矛盾しないことを確認するためのテスト群として位置づけられる。

## Read this when
- cmoc の実装変更に対して、どの外部挙動・永続状態・git 副作用・CLI 出力・終了コードが既存テストで固定されているかを確認したいとき。
- apply fork/join/abandon、session fork/join/abandon、init、対話起動、review oracle、indexing などの CLI コマンドについて、実 repository 上での状態遷移や cleanup、report、branch/worktree 操作の期待値を調べるとき。
- Codex CLI 呼び出しラッパーの引数、環境変数、CODEX_HOME、profile、schema validation retry、capacity/quota retry、ログ記録、TUI/exec 起動制御をテスト観点から確認するとき。
- INDEX.md 生成・更新・preflight、fresh hash、malformed entry 再生成、merge conflict 解決、root 直下 memo 除外など、routing document 周辺の回帰テストを探すとき。
- path token、repo root/work root、file access mode、sandbox mode、Codex profile permission、設定 default、エラー markdown、CLI preflight など、cmoc の基礎 runtime 挙動のテスト入口を探すとき。
- プロンプト部品、standard 文書の Markdown 描画、complete prompt 注入、builder ごとの model class・reasoning effort・file access mode・schema 選択を確認したいとき。
- 新しい realization test を追加する前に、既存の共通 helper、fixture、または同じ観点のテストへケース追加できるかを確認したいとき。

## Do not read this when
- 正本仕様断片そのもの、oracle file の意図、自然言語仕様、path keyword の定義、INDEX.md エントリー設計方針を確認したいときは、oracle 側の該当本文を読む。
- 実装内部の責務分割、helper のアルゴリズム、状態 model、git helper、prompt builder、Codex runtime の実装を直接変更したいだけのときは、src 側の該当 module を読む。
- Codex CLI や LLM の実際の出力品質、外部サービスの挙動、対話 UI の表示品質そのものを検証したいとき。この領域の多くは fake 実行環境や制御ロジックの確認であり、実サービス評価の入口ではない。
- 個別サブコマンドや runtime 領域と無関係な補助ファイル、開発手順、生成物、プロジェクト概要を調べたいときは、同階層外のより直接の対象へ進む。
- テスト支援 fixture や共通セットアップだけを探している場合は、個別 scenario 群を読む前に共通 helper へ進む。

## hash
- 9d6aa563a86e0867ffd81e2b3a33e9327da41ab884b04e4749c0ef4e62bec8e7
