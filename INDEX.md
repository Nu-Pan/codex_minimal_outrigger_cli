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
- cmoc の正本仕様断片群への入口。自然言語文書で述べられた利用者向け挙動・開発規則・設計判断と、Python や JSON で述べられた agent 呼び出し・設定・基礎モデルなどの実装形式仕様を下位領域へ振り分ける。
- oracle file と realization file の関係、正本仕様断片としての扱い、仕様の隙間を AI 裁量で補う範囲、INDEX.md 生成やレビュー時に使う標準プロンプト断片など、実装・テストが従うべき上位仕様を探す起点になる。

## Read this when
- cmoc の実装やテストを変更する前に、根拠にすべき正本仕様断片が自然言語文書側か実装形式仕様側かを切り分けたいとき。
- CLI の外部挙動、サブコマンド、ログ、エラー処理、run 隔離、session 状態、Codex CLI 呼び出し、INDEX.md 生成、標準利用フローの仕様を確認したいとき。
- session branch、run branch、worktree、fork / join commit など、cmoc の git branch・commit・worktree モデルを確認したいとき。
- oracle file、realization file、oracle doc、oracle src、realization implementation、realization test などの基本分類や、正本仕様断片と実装成果物の責務境界を確認したいとき。
- AI agent 呼び出しの prompt、Structured Output schema、file access mode、model/reasoning 設定、path keyword、root token、構造化自然言語文書 helper など、実装形式で表された正本仕様を探したいとき。
- oracle や realization の標準、INDEX.md エントリー品質基準、作業計画レビューや memory などの不採用設計案の根拠を確認したいとき。

## Do not read this when
- 現在の realization implementation や realization test のコード構造、関数名、依存関係、既存テスト期待値だけを調べたいときは、実装・テスト側を直接読む。
- 特定の正本仕様断片がすでに分かっており、その詳細だけが必要なときは、この入口ではなく該当する本文へ直接進む。
- 生成済みルーティング文書の現在内容やハッシュだけを確認したいときは、対象の本文ではなく生成物確認の手順に従う。
- README、AGENTS、補助ファイル、または oracle 外の realization ancillary の現在内容を調べたいときは、それぞれの対象を直接読む。
- 実行ログ、一時ファイル、作業メモ、生成キャッシュなど、正本仕様断片ではないものを探しているとき。

## hash
- d1ca5ccbfff62854361230fc7528e8ddc123cb406c6fd7d98d8fbfaf62cead36

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
- cmoc の実装本体を収める realization implementation 領域で、CLI エントリーポイント、サブコマンド実行処理、共有 runtime helper、設定 dataclass、基礎型・パスモデル・構造化 Markdown helper、補助 AI 呼び出し用の parameter builder と標準プロンプト部品を扱う。
- session、apply、review、INDEX.md maintenance、初期化などの利用者向け操作が、git/worktree/state/config/Codex CLI 呼び出し/Structured Output/report 生成へどう接続されるかを追う入口になる。
- 正本仕様断片やテストではなく、oracle file の意図を具体化する Python 実装と、その実行時副作用・内部データ構造・補助 agent 呼び出し契約を確認するための上位入口である。

## Read this when
- cmoc の CLI コマンド、サブコマンドの実行フロー、git/worktree/state/config/log/report などの実装上の副作用を確認または変更したいとき。
- Codex CLI を subprocess として呼び出す処理、model/reasoning/file access mode の変換、quota/capacity retry、Structured Output schema 準備・検証、call log 保存を追いたいとき。
- session fork/join/abandon、apply fork/join/abandon、oracle review、INDEX.md maintenance、初期化の状態遷移や制御ロジックを調べたいとき。
- 補助 AI に渡す prompt、role、goal、読み書き制限、oracle/realization/review/apply/indexing 標準、応答 schema、AgentCallParameter の組み立てを確認したいとき。
- ルートトークン付きパス表記、共有設定構造、規範データ構造、構造化 Markdown 出力など、複数の実装領域から参照される基礎部品を確認したいとき。
- oracle file との不整合を直すために、現在の realization implementation がどのような責務境界と既存 helper で構成されているかを把握したいとき。

## Do not read this when
- 正本仕様断片そのもの、oracle file の定義・要求・標準本文だけを確認したいとき。その場合は oracle 側の本文を読む。
- 自動テスト、fixture、期待挙動の検証ケース、テスト追加先だけを探しているとき。その場合は test 側を読む。
- 利用者向け README、リポジトリ全体の説明、補助的な開発ファイル、生成済み metadata や cache だけを確認したいとき。
- 特定の下位領域や単一ファイルがすでに分かっており、CLI 層、共有 runtime、設定、基礎型、prompt builder の全体像を確認する必要がないとき。
- INDEX.md エントリー作成の根拠として既存 INDEX.md だけを読みたいとき。ここは本文実装を確認する入口であり、ルーティング文書そのものの代替ではない。
- 実装を変更せず、oracle file や realization file の編集可否、作業時のファイルアクセス規則、ルーティング規則だけを確認したいとき。

## hash
- e3028476f53c64a3dd8bee5fe9f80a89ff4f96c3c1b2d6ab4e5174fc3a2ca0b9

# `test`

## Summary
- cmoc の realization test 群への入口であり、主要 CLI コマンドと runtime 結合部の外部挙動、状態遷移、副作用、プロンプト部品生成の互換性境界を確認するためのテストを収める。
- 一時 Git リポジトリ、fake Codex CLI、monkeypatch を使う統合寄りの回帰確認と、標準文書を組み込むプロンプト生成の単体寄り確認の双方を扱う。
- 実装変更が利用者から見える終了コード、標準出力、エラーレポート、worktree・branch・状態ファイル・レポート生成、設定同期、quota 再開制御、Markdown プロンプト内容にどう影響するかを調べる入口になる。

## Read this when
- CLI サブコマンドの終了コード、標準出力、エラー描画、preflight、completion probe、初期化時の副作用を変更または検証するとき。
- session、apply、review、indexing の branch、worktree、状態 JSON、レポート、cleanup などの外部副作用や状態遷移を確認するとき。
- Codex CLI 呼び出しラッパーの stdin、profile/config 生成、structured output schema、ログ、認証環境検証、quota polling/resume、並列呼び出し制御を変更または検証するとき。
- INDEX.md 生成処理や indexing preflight が Codex 呼び出し前に走る条件、または特定目的で skip される条件を確認するとき。
- プロンプト部品生成関数の構造化文書型、Markdown レンダリング、標準文書セクションの含有条件、互換性境界となる主要語句を確認するとき。
- 実装変更に対して、既存の realization test がどの利用者向け挙動や制御ロジックを固定しているかを把握したいとき。

## Do not read this when
- oracle file の正本仕様そのものや、人間が管理する仕様断片の内容を確認したいとき。
- production code の責務、実装構造、個別 helper の詳細だけを直接調べたいとき。
- 構造化文書や Markdown レンダリングの汎用実装そのものを調べたいとき。
- CLI 実行、ファイルアクセス、パスモデル、永続状態などの挙動と無関係な、プロンプト本文生成ロジックだけを変更したいとき。
- INDEX.md エントリー生成規則やルーティング文書の書式だけを確認したいとき。

## hash
- cc621f0c23538f0759eb6c4704ab4ee55220047e49425e8448cf84c6489c61be
