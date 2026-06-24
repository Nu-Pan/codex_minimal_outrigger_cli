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
- cmoc の正本仕様断片全体への入口。人間が責任を持つ仕様として、利用者向け CLI 挙動、session / run / branch / worktree モデル、agent 呼び出し、設定、パス表記、構造化文書、ルーティング文書、開発・テスト規約、不採用設計判断などを扱う。
- 自然言語の仕様文書と、Python・JSON など実装形式で書かれた仕様断片の両方を含む。realization implementation や realization test を変更する前に、実装が従うべき根拠を目的別に探すための階層。
- 利用者が編集する仕様と AI が生成・修正する実装との境界を定め、oracle file を正本として realization file が追従するという cmoc の基本構造を確認する入口になる。

## Read this when
- cmoc の挙動や設計判断について、realization code より優先される正本仕様断片を探したいとき。
- CLI サブコマンド、stdout / stderr、終了コード、ログ、状態遷移、設定ファイル、補完、エラー処理など、利用者に見える cmoc の仕様を確認したいとき。
- session branch、run branch、home branch、fork / join commit、linked worktree、作業隔離など、git branch / commit / worktree モデルを確認したいとき。
- Codex CLI などの agent call、prompt、Structured Output、model class、reasoning effort、file access mode、並列実行、retry / resume など、外部 agent 制御の仕様を調べるとき。
- INDEX.md の生成・更新、hash、ルーティング文書の意味情報、インデクシング、自動コミットや排他制御の仕様を確認したいとき。
- cmoc の realization implementation や realization test を追加・修正する前に、Python 実装規約、設計規約、開発環境、テスト方針、共通データ構造、パスモデル、設定モデルの根拠を確認したいとき。
- memory、kaizen、作業計画レビュー、apply 挙動など、採用しなかった案や non-goal の背景を確認したいとき。

## Do not read this when
- 正本仕様ではなく、実際に編集する realization implementation や realization test のコード構造、既存関数、具体的な実装差分だけを調べたいとき。
- 対象のサブコマンド、agent call builder、パス helper、設定 helper など、読むべき下位領域がすでに特定できているときは、この階層全体ではなく該当する下位対象へ直接進む。
- 作業対象が生成物、一時ファイル、実行ログ、作業用 worktree 内の成果物などで、cmoc の正本仕様断片を確認する必要がないとき。
- 既に必要な正本仕様断片を読み終えており、次の作業が realization file の編集・テスト実行・既存実装の局所確認だけで足りるとき。
- リポジトリ外部の一般的な Git、Python、CLI、Codex のベストプラクティスだけを調べたいとき。cmoc で優先される判断根拠はこの階層の仕様だが、一般論そのものの参照先ではない。

## hash
- 30c6e7aa67d76cc5435fe906c93da95d389c87a5c851ee129db8605a27a39e07

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
- cmoc の realization implementation 全体への入口となる実装領域。利用者向け CLI の接続層、サブコマンドごとの実行制御、共有 runtime helper、設定データ構造、パス・AgentCallParameter・構造化文書などの基本モデル、AI 呼び出し用プロンプトと Structured Output schema の組み立てを含む。
- セッション作成・結合・破棄、apply fork/join/abandon、oracle review、INDEX.md maintenance、TUI 起動、Codex CLI 呼び出し、git worktree/branch/state/log/config/report 操作など、cmoc の実行時挙動がどの実装責務に分かれているかを辿る起点になる。
- 正本仕様断片そのものではなく、oracle file で述べられた意図を具体化する Python 実装と補助 schema のまとまり。仕様本文、テスト、生成済み run 成果物へ進む前に、プロダクト側の制御フローや共通部品の所在を選ぶための階層。

## Read this when
- cmoc の CLI コマンド、サブコマンド実行フロー、branch/worktree/state のライフサイクル、Codex CLI 実行、レポート生成、INDEX.md 更新など、実装側の挙動を確認または変更したいとき。
- 複数サブコマンドにまたがる git・filesystem・設定・ログ・schema・hash・binary 判定・Codex profile・retry・quota handling などの共有 runtime 処理の読む先を探しているとき。
- AgentCallParameter、ModelClass、ReasoningEffort、FileAccessMode、root token 付きパス、StructDoc、cmoc config など、上位処理から参照される基本データ構造や変換規則を調べたいとき。
- review、apply、indexing、session conflict resolution、TUI parameter resolution などで AI に渡す role、goal、補助文脈、共通 standard、Structured Output schema がどのように構築されるか確認したいとき。
- oracle review の finding 列挙・merge・validate・judge loop、apply fork の finding 列挙・refine・application loop、変更要約や commit message 生成など、AI 呼び出しを含む実装上の orchestration を追いたいとき。

## Do not read this when
- 正本仕様断片の内容、oracle file の要求、oracle standard、realization standard、INDEX.md entry standard そのものを確認したいとき。実装ではなく oracle 側の本文を読む方が適切。
- 実装が仕様を満たしているかを外部挙動として検証するテストケース、fixture、期待値、テスト追加先を探しているとき。テスト領域を直接読む方が適切。
- 過去または現在の run が生成した report、log、state、worktree、Codex 出力、INDEX.md などの成果物だけを確認したいとき。対象の生成物を直接読む方が適切。
- 利用者向けの概要説明、インストール手順、リポジトリ全体の案内だけを知りたいとき。実装本文まで読む必要はない。
- 対象とするサブコマンド、共通 helper、AI prompt builder、基本モデルのどれを読むべきかすでに分かっており、より直接の下位ファイルまたは下位領域へ進めるとき。

## hash
- 3fe66803cf5837f7bfd6a8bb9d08a635c73faf0986f66446cba6519347018543

# `test`

## Summary
- cmoc の realization test 群への入口であり、基本モデル・CLI 制御フロー・Git/worktree 操作・Codex CLI 呼び出し境界と、プロンプト部品・実行パラメータ生成の外部挙動を検証するテストを収める。
- 主要ユーザー操作、状態遷移、エラー表示、設定同期、quota retry、プロンプト断片のレンダリング、Structured Output schema 構造など、実装が正本仕様断片をどう具体化しているかを回帰検知するための対象である。
- 個別の正本仕様ではなく realization test の集合なので、仕様本文を読む前の代替ではなく、実装変更が既存外部挙動やプロンプト契約を壊さないか確認する入口として位置づけられる。

## Read this when
- 基本モデル、path token 変換、設定デフォルト、sandbox mode 変換、構造化エラー表示など、cmoc の基礎挙動を変更する。
- CLI の init、tui、session、apply、review、indexing まわりの外部出力、副作用、状態遷移、ブランチ・worktree 操作、merge conflict、dirty worktree、禁止差分の扱いを変更する。
- Codex CLI 呼び出しの stdin、profile、CODEX_HOME/auth.json 検証、ログ、schema validation retry、quota polling/resume など、外部プロセス境界の挙動を変更する。
- プロンプト builder、標準プロンプト断片、ファイルアクセス規則、レビュー基準、索引エントリー基準、review oracle 基準、TUI/indexing/review oracle 用の実行パラメータや schema 構造を変更する。
- 新しい realization test を追加する前に、既存の広い回帰テストへケース追加または統合できるか判断したい。

## Do not read this when
- oracle file の正本仕様そのものを確認したい場合。この対象は realization test であり、仕様本文の代替ではない。
- 特定の小さな helper や純粋関数の詳細だけを確認したい場合で、より局所的な実装やテストが存在する。
- CLI 外部挙動、状態遷移、Git/worktree 操作、Codex 呼び出し境界、プロンプト合成、実行パラメータ選定に影響しない内部整理や UI 文面だけを調べる。
- StructDoc や Markdown renderer の汎用実装詳細だけを変更し、このテスト群で固定している具体的なプロンプト文言やパラメータ契約には触れない。
- INDEX.md エントリー生成・描画の形式だけを確認したい場合は、indexing 専用の実装や schema を先に読む方が直接的。

## hash
- 2ae8665de6be7966b014db3db722b19d8e6238adee6627aaf23cad5c2bade714
