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
- cmoc の正本仕様断片を集約する階層への入口。人間が所有する oracle file と、AI が生成・編集する realization file の関係、oracle file を正本として realization file を追従させる片方向の責務境界を確認する起点になる。
- 自然言語 Markdown の仕様文書群と、プログラミング言語・設定ファイルで書かれた正本仕様断片へ分かれており、CLI 外部挙動、session/run の git モデル、AI 呼び出しパラメータ、パス語彙、設定構造などの仕様判断へ進むための上位ルーティングを担う。
- oracle file の規模を小さく保つこと、未定義部分を AI 裁量として許容すること、用語・命名・論理整合性を保つこと、realization file の肥大化や公開面・依存関係・テストの増加を抑制することなど、cmoc 開発全体の判断基準を読む入口でもある。

## Read this when
- cmoc の正本仕様断片を読み始める必要があり、自然言語仕様、実装形式の oracle、設定・パス・AI 呼び出し仕様のどこへ進むべきかを判断したいとき。
- oracle file と realization file の定義、所有者、編集責任、正本仕様から実装への片方向関係、oracle doc・oracle src・oracle test と realization 側の下位概念を確認したいとき。
- 実装やテストを変更する前に、oracle file の未定義部分をどう扱うか、既存実装から仕様へ逆流させてよいか、ベストプラクティスと oracle 要求が競合した場合に何を優先するかを確認したいとき。
- cmoc の実装・テスト・補助ファイルを増減させる作業で、文字数最小化、責務境界、抽象化、公開面、永続状態、依存関係、fixture、不要コード削除に関する共通判断基準を確認したいとき。
- INDEX.md エントリーを作成・更新する作業で、対象を読むべき条件、対象内容への根拠、対象外へ進ませない境界、機械的情報を混ぜない方針を確認したいとき。

## Do not read this when
- 特定の CLI サブコマンド、ログ、エラー処理、branch/worktree モデル、開発規則、不採用案など、自然言語で書かれた個別仕様範囲がすでに明確なときは、下位の自然言語仕様文書群へ直接進む。
- AI 呼び出しパラメータ、root token と実パスの変換、構造化文書モデル、永続設定など、実装形式で書かれた正本仕様断片だけを確認したいときは、下位の実装・設定形式の oracle へ直接進む。
- cmoc の現在の Python 実装、関数、クラス、CLI 処理、git 操作、永続状態読み書き、自動テストの実体を調べたいときは、正本仕様断片ではなく realization 側の該当実装またはテストを読む。
- oracle file 本文を読む必要がなく、既に根拠となる仕様断片と対象 realization file が特定できている小さな修正だけを行うとき。
- 生成物、実行ログ、一時ファイル、補助スクリプト、具体的な fixture 内容など、正本仕様ではない realization ancillary の現状確認だけが目的のとき。

## hash
- d94617e27965f1c10fabfc2f81a67fcfe447007e1444431c92580cf7bb0e1e2a

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
- cmoc の realization implementation 全体を収める実装領域。AI agent 呼び出し契約、基礎データ構造、runtime helper、リポジトリ別設定、CLI 起動入口、各サブコマンド本体に分かれている。
- 正本仕様断片を具体化するプロダクト実装の入口であり、利用者が実行する CLI 表層から、Codex 呼び出し、Git 操作、設定・状態管理、INDEX.md maintenance、session/apply/review の業務フローまでをたどるための上位階層。
- 仕様そのものではなく、oracle file の意図を実行可能なコード・設定として実現する側を調べるときに、共通 helper、AI 委譲境界、コマンド固有処理のどこへ進むべきかを切り分けるためのまとまり。

## Read this when
- cmoc の実装変更や不具合調査を始めるにあたり、CLI 入口、サブコマンド本体、runtime helper、設定モデル、AI agent 呼び出し契約、基礎型のどこへ進むべきか判断したいとき。
- init、tui、indexing、session、apply、review などのコマンド実行時に、引数解析から共通 runtime、Git/worktree 操作、Codex 呼び出し、状態更新、利用者向け出力へどうつながるかを追いたいとき。
- AI agent に渡す prompt、Structured Output schema、model class、reasoning effort、ファイルアクセス権限など、cmoc が別 agent へ処理を委譲する境界を実装側から確認したいとき。
- 複数機能で共有される path 解決、設定読み書き、content hash、エラー表示、実行ログ、Codex CLI 呼び出し、session/apply 状態、Git helper などの runtime 支援を調べたいとき。
- リポジトリ別設定値、CLI command 登録、互換 import 入口、基本データ構造、Markdown 文書生成など、上位機能から参照される実装部品の責務を切り分けたいとき。
- realization implementation に新しい機能や変更を入れる前に、既存の責務境界、共通化済み処理、コマンド固有処理、テスト追加先の手がかりを得たいとき。

## Do not read this when
- oracle file の正本仕様断片、path keyword の概念定義、oracle standard、realization standard、review standard、INDEX.md エントリー標準そのものを検討したいとき。仕様判断の正本は oracle 側を読む。
- cmoc の自動テスト、fixture、期待挙動、回帰テスト追加先を直接確認したいとき。テスト領域へ進む方が直接的。
- README、AGENTS、補助スクリプト、Git 管理設定、生成物や開発補助ファイルなど、実装ソース以外の realization ancillary を確認したいとき。
- 個別の下位領域で読むべき対象がすでに分かっており、特定サブコマンド本体、共通 runtime helper、AI 委譲 prompt、設定モデル、基本型だけを直接調べれば足りるとき。
- 実装から仕様を逆算して oracle file を変更したいとき。実装側の内容は調査材料にはなり得るが、正本仕様として扱うべきではない。

## hash
- dc3c310d9806516a5f7723db063f341b8d0dd9ab00fd0da5852a19d86b8f33cf

# `test`

## Summary
- cmoc の realization test 群を収める領域。CLI サブコマンド、Codex runtime、indexing、prompt 構築、path/root 判定、file access mode、session/apply/review の外部挙動と制御ロジックを、テスト用 git repository や fake Codex 実行を使って検証する。
- 実装側の詳細責務ではなく、oracle file を具体化した実行結果、状態ファイル、branch/worktree 副作用、ログ、report、エラー出力、preflight などの回帰確認へ進む入口になる。
- 共通 fixture と helper も含み、一時 repository、CODEX_HOME、CLI runner、apply worktree 解決など、複数の realization test で共有するテスト環境構築の確認先でもある。

## Read this when
- cmoc の CLI 外部挙動を変更した後に、対応する realization test の期待値、回帰観点、状態遷移、stdout/stderr、report、ログ、git 副作用を確認したいとき。
- init、tui、session、apply、review oracle、indexing などのサブコマンドについて、実装ではなく利用者から見える結果や制御境界をテスト観点で調べたいとき。
- Codex CLI 呼び出し wrapper の argv、stdin、CODEX_HOME、profile、schema 保存、call log、retry、quota/capacity handling、TUI/exec 差分を確認したいとき。
- path token、repo root/work root、linked worktree、sandbox mode、file access mode、Codex profile 権限など、複数機能にまたがる runtime 前提を検証するテストを探しているとき。
- INDEX entry 生成、indexing preflight、INDEX conflict 解決、prompt parts、review criteria、routing/file access/index entry standards のプロンプト反映をテスト側から確認したいとき。
- 新しい realization test を追加する前に、既存テストへケース追加できるか、共通 helper を使えるか、重複した観点がないかを確認したいとき。

## Do not read this when
- cmoc の正本仕様断片を確認したいときは、oracle file を読む。この領域は realization test であり、正本仕様の代替ではない。
- プロダクト実装の責務分割、内部 helper、CLI command 本体、runtime 本体、path model 本体を直接変更したいときは、まず実装側の対象を読む。
- Codex CLI や LLM の出力品質そのものを評価したいときは対象外である。ここでは fake 実行や monkeypatch により cmoc 側の制御と副作用を検証している。
- 個別機能に関係しない一般的な pytest fixture、git helper の低レベル実装、またはテスト基盤以外の補助ファイルを探しているときは、より直接の実装・補助領域へ進む。
- INDEX.md のルーティング文書としての正本仕様や entry 文面基準だけを確認したいときは、仕様断片や prompt/schema 側を読む。

## hash
- 23f206dd520b5a66d363cbb5593012b80f2c150d8ec1ddb41f253ae1a54dd99d
