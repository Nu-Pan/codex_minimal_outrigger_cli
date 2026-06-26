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
- cmoc の正本仕様断片を置く領域で、自然言語で書かれた仕様断片、プログラミング言語や設定として書かれた仕様実装、テスト形式の仕様を下位に持つ。oracle file は人間が所有し、AI が編集する realization file の根拠になるものとして扱われる。
- CLI の公開挙動、AI エージェント呼び出しパラメータ、標準プロンプト部品、パス語彙、設定構造、構造化文書生成、開発・テスト規則など、cmoc の実装へ反映すべき正本仕様断片へ進む入口になる。
- oracle file と realization file の責務境界、正本仕様断片を小さく保つ方針、未定義部分を AI 裁量で補う原則、用語・命名・矛盾回避・INDEX.md ルーティング品質など、cmoc 全体の仕様記述と実装判断の前提を確認する場所でもある。

## Read this when
- cmoc の正本仕様断片を探し始めるとき、または自然言語仕様、仕様実装、テスト仕様のどこへ進むべきかを切り分けたいとき。
- oracle file を根拠に realization implementation や realization test を追加・修正する前に、人間意図として固定されている挙動や AI 裁量で補ってよい範囲を確認したいとき。
- CLI サブコマンド、session fork / join、apply fork / join / abandon、review oracle、init、tui、indexing、Codex CLI 呼び出し、Structured Output、ログ、エラー処理、run 隔離、session state、branch / worktree モデルなどの仕様断片へ進みたいとき。
- AI エージェント呼び出しの role、summary、goal、補助文脈、ファイルアクセス権限、モデル種別、reasoning effort、Structured Output schema、標準文面、リポジトリ設定などを確認したいとき。
- oracle / realization の基本概念、正本仕様断片としての記述方針、実装から仕様へ逆流させない原則、用語統一、命名、non-goal、INDEX.md エントリーの品質基準を確認したいとき。

## Do not read this when
- 特定の realization implementation や realization test の現在の関数、クラス、既存 helper、テスト期待値だけを調べたいとき。
- CLI 引数解析、プロセス制御、git 操作、永続状態の読み書き、端末 UI 描画など、実行フロー本体の実装コードだけを直接確認したいとき。
- 対象ファイルや差分そのものを読んで、個別の patch 内容、merge conflict、所見の妥当性、実装修正方針を判断したいとき。
- Codex CLI や LLM の一般的な使い方、実際の応答品質、生成結果の妥当性だけを評価したいとき。
- 既に読むべき下位の正本仕様断片が特定できており、この階層で oracle file の種類や責務境界を確認する必要がないとき。

## hash
- b61e5e15a1545f039bef99c512c1f7f4e1a07d69121ad857359ddc6aaae0699a

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
- `src` は cmoc の realization implementation を置く実装ルートで、CLI 入口、サブコマンド実行本体、共通 runtime helper、設定モデル、基礎データ型、AI agent 呼び出しパラメータ構築、互換 import 入口を配下に分けている。
- 利用者向けコマンドから下位 helper まで、cmoc の実行時挙動を実装側から追うための起点であり、具体的な責務は配下の領域ごとに分岐して読む。

## Read this when
- cmoc の実装コードを調査または変更するために、CLI 入口、サブコマンド本体、共通 runtime、設定、基礎モデル、AI agent prompt 構築のどこへ進むべきか切り分けたいとき。
- oracle file で述べられた正本仕様断片が、実際の realization implementation としてどの領域に具体化されているかを確認したいとき。
- CLI コマンドの公開構成から実行フロー、Codex 呼び出し、git・state・config・path・logging などの共通処理まで、実装側の入口を探したいとき。
- 実装変更の前に、既存 realization code の責務境界や近い実装がどの下位領域にあるかを把握したいとき。

## Do not read this when
- 正本仕様断片そのもの、oracle standard、path keyword の概念定義、INDEX.md 生成規則など、実装ではなく仕様文書を確認したいとき。
- テストコードだけを調査・変更したいとき。対応する realization test 側を読む方が直接的である。
- リポジトリ設定、ビルド設定、補助スクリプト、README など、実装ルート外の ancillary file を確認したいとき。
- すでに対象サブコマンド、共通 helper、設定モデル、基礎データ型、prompt builder などの具体的な下位領域が分かっているとき。

## hash
- 2f3da9ebd2b1bcf608ffff75d12fdc26646206ddbff45f6311f04df12d2d67ac

# `test`

## Summary
- cmoc の realization test 群をまとめる領域であり、CLI サブコマンド、Codex 実行 wrapper、INDEX 更新、prompt/schema builder、runtime/path/file access/state/git worktree 周辺の外部挙動と制御ロジックを検証する入口になる。
- 一時 Git リポジトリや fake Codex 実行ファイルなどの共有 test support を使い、oracle file で述べられた人間意図が src 側の実装としてどのように実現されているかを、利用者に見える出力・終了コード・永続状態・git 副作用・ログで確認する。
- 大きいテストファイルを複数含むが、apply fork/join/abandon、review oracle、prompt parts などは同じ fixture・状態・report 文脈で読む必要がある責務ごとに凝集されており、個別ファイルの入口は各エントリーで絞り込む。

## Read this when
- cmoc の CLI 外部挙動、終了コード、stdout/stderr、report、session/apply state、git branch/worktree cleanup、linked worktree 対応の回帰テストを探すとき。
- Codex CLI 呼び出し wrapper、CODEX_HOME、profile、retry/quota retry、call log、subcommand log、TUI 起動条件など、外部 Codex 実行を fake で観測するテストを確認したいとき。
- INDEX.md 生成・更新・preflight、root 直下 memo 除外、malformed entry、hash freshness、INDEX conflict 解決など、indexing 系の realization test を探すとき。
- prompt part、complete prompt、file access rule、structured output schema、各種 AgentCallParameter builder の期待値を横断的に確認したいとき。
- 新しい realization test を追加する前に、同じ観点を既存の apply/session/review/indexing/runtime/prompt 系テストへ統合できるか確認したいとき。

## Do not read this when
- 正本仕様断片そのものを確認したいとき。この領域は realization test であり、仕様判断の根拠は oracle 配下の該当本文を優先する。
- プロダクト本体の実装責務、内部 helper、状態管理、path model、Codex runtime の実装を先に理解したいときは、src 側の該当モジュールから読む方が直接的である。
- テスト fixture や helper の使い方ではなく、実装されるべき人間意図や oracle standard の境界を調べたいとき。
- Codex CLI や LLM 出力品質そのものを評価したいとき。ここでは多くのテストが fake 実行ファイルや monkeypatch を使い、cmoc 側の制御と副作用だけを検証している。
- INDEX.md の表示形式やルーティング文書の一般方針だけを知りたいときは、test 配下ではなく oracle の INDEX/indexing 関連文書または rendering 実装を読む方が適切である。

## hash
- 9c654e8780e26410d625740b0dfec57277056a98c61dda992dbd839356b1d9c0
