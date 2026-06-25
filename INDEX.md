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
- cmoc の正本仕様断片を集めた領域であり、人間が所有する oracle file の定義、realization file との責務分担、自然言語仕様、実装形式の仕様断片、テスト形式の仕様断片へ進む入口になる。
- 正本仕様断片として何を書くべきか、未定義部分をどう扱うか、用語・命名・矛盾・ベストプラクティスとの優先関係をどう判断するかなど、oracle 側の共通規範を扱う。
- realization file を追加・変更するときの最小化、品質、責務分割、抽象化、公開面・状態・依存・テスト肥大化の抑制など、AI が実装を具体化する際の共通制約を確認する入口になる。
- INDEX.md エントリーを、本文の代替ではなく読むべき対象へのルーティング情報として生成するための責務、根拠、境界、機械的情報の扱いを確認する入口になる。

## Read this when
- cmoc の正本仕様断片を探し、自然言語仕様、実装形式の仕様断片、テスト形式の仕様断片のどこへ進むべきか判断したいとき。
- oracle file と realization file の定義、正本性、編集主体、生成方向、下位概念の境界を確認したいとき。
- oracle file を追加・修正する提案を考える前に、人間の認知負荷、正本仕様断片の疎さ、未定義部分、総文字数、論理矛盾、用語統一、命名、non-goal の扱いを確認したいとき。
- realization implementation や realization test を追加・変更する前に、既存実装の整理、責務分割、抽象化、公開面、永続状態、依存、補助ファイル、テスト量をどう抑えるべきか確認したいとき。
- INDEX.md エントリーを生成・更新する際に、対象内容に根拠を持つルーティング条件、読むべき境界、読まなくてよい境界、機械的情報を混ぜない方針を確認したいとき。
- 一般的なベストプラクティスや既存実装からの推測より、cmoc の正本仕様断片を優先すべき場面かどうかを判断したいとき。

## Do not read this when
- 個別サブコマンドの CLI 引数、状態遷移、stdout、report、終了コードなどの利用者可視仕様を直接確認したいときは、自然言語仕様を扱う下位領域へ進む。
- AI agent 呼び出しパラメータ、Structured Output schema、root token 付きパス解決、設定 dataclass など、プログラミング言語・設定形式で表された正本値を確認したいときは、実装形式の仕様断片を扱う下位領域へ進む。
- realization implementation、realization test、helper、既存関数、現在のコード構造、テスト期待値だけを調べたいときは、oracle ではなく対象の実装またはテストへ直接進む。
- パスキーワードや root 種別の具体的な実装詳細だけを確認したいときは、パスモデルの仕様または実装へ直接進む。
- 既存のルーティング文書、生成キャッシュ、実行ログ、一時ファイル、ビルド成果物を確認したいだけのとき。
- pytest、PEP 8、git 操作、CLI 設計などの一般論を調べたいだけで、cmoc 固有の正本仕様断片との関係を確認する必要がないとき。

## hash
- 2acb616f721ecf468b7c9d89cb81df433cf8bbf06bd6c937eb10883456aa874c

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
- cmoc の realization implementation 全体を収める実装領域。最上位 CLI アプリの組み立て、各サブコマンドの実行フロー、Codex CLI/TUI 連携、INDEX.md maintenance、session/apply/review の状態遷移、git・worktree・config・log・report・runtime helper、エージェント呼び出しパラメータ、構造化プロンプト、パスモデル、規範文書レンダリングを扱う。
- 上位のコマンド登録から下位の共通 runtime、設定モデル、AI agent 向け prompt/schema builder、個別サブコマンド実装へ進むための入口である。cmoc の実行時挙動を実装側から追う場合は、この領域を起点に責務別の下位要素へ進む。
- 正本仕様断片ではなく、oracle file で述べられた意図を具体化する realization code の置き場である。利用者向けの公開面、永続状態、外部プロセス呼び出し、作業用 branch/worktree、Structured Output の消費、レポート生成など、実際に動く処理の責務境界を確認するための実装入口になる。

## Read this when
- cmoc の CLI コマンドがどのサブコマンド実装へ接続され、引数解析エラー、indexing preflight、Codex exec/tui 呼び出し前後の制御がどのように配線されているか確認または変更したいとき。
- init、tui、indexing、session、apply、review oracle の実行フロー、事前条件、clean worktree 要求、branch/worktree/state の作成・更新・削除、merge、cleanup、report 出力、利用者向け表示を実装側から追いたいとき。
- Codex CLI に渡す prompt、Structured Output schema、モデルクラス、reasoning effort、論理ファイルアクセスモード、標準プロンプト部品、補助文脈の組み立て方を確認または変更したいとき。
- Codex profile、sandbox/permission profile、CODEX_HOME、schema 配置、stdout/stderr/output/call log、resume token、capacity/quota retry、subprocess env など、外部 Codex 実行の runtime 連携を調べたいとき。
- cmoc config のデータ構造、既定値、JSON 変換・読み書き、モデル名・reasoning effort 名への対応、apply/review loop 回数上限を確認または変更したいとき。
- repo root、work root、cmoc root、run worktree、root token 付きパス表記、git common dir を含む root 解決、実パスと token path の相互変換を実装から確認したいとき。
- Git wrapper、managed branch 判定、worktree 作成削除、branch 削除、.cmoc ignore 検査、git ignored 判定、content hash、binary 判定、subcommand log、session/apply state の保存形式を扱いたいとき。
- INDEX.md の対象列挙、既存 entry の hash 判定、entry 生成用 Codex 呼び出し、深い階層からの再生成、INDEX.md 差分だけの commit、conflict marker 解消用 prompt など、目次 maintenance の実装を追いたいとき。
- 階層化された自然言語文書や standard を Markdown にレンダリングする構造、fenced code block、見出し階層、複数行文字列の整形など、prompt 文書生成の低レベル部品を確認したいとき。

## Do not read this when
- oracle file の正本仕様断片そのもの、oracle standard、realization standard、INDEX.md エントリー規則、path keyword の人間向け定義だけを確認したいとき。この領域はそれらを実装・プロンプト化する realization code であり、仕様本文の正本ではない。
- cmoc の利用方法、コマンドの使い方、開発者向け説明、パッケージ設定、依存関係宣言、エントリーポイント設定だけを確認したいとき。実行コードではなく利用者向け文書やプロジェクト設定を読む方が直接的である。
- テスト期待値、fixture、回帰観点、テストケース追加先を探しているとき。実装本文ではなく realization test 側を読む方が直接的である。
- 生成済み INDEX.md、過去の review/apply report、Codex call log、session state、config 実ファイルなど、実行によって作られた個別成果物の内容を確認したいだけのとき。
- 個別の正本仕様を変更すべきか判断したいとき。実装から仕様へ逆流させるのではなく、oracle file 側の本文を根拠にする必要がある。
- cmoc 以外の対象リポジトリのアプリケーション実装、業務コード、ユーザーが Codex TUI に渡す任意プロンプトの内容を調べたいとき。この領域は cmoc 自身の実装である。

## hash
- 4bd4a470219c8c9964c0e5875085c177a12c05873b6d5f0e0ab0240188099a38

# `test`

## Summary
- cmoc の realization test 群を収める領域で、CLI サブコマンド、Codex runtime、indexing、prompt 構築、review oracle、session/apply lifecycle、基本 runtime の外部挙動と制御ロジックを検証する入口になる。
- 一時 git リポジトリ、Codex home、Typer runner、apply worktree 復元などの共通 test support も含み、複数テストで共有される fixture と helper の所在を判断するための上位ルーティング対象である。
- 各テストは正本仕様そのものではなく、oracle file で述べられた人間意図を具体化した realization の回帰確認として、出力、状態ファイル、branch/worktree 操作、ログ生成、エラー境界などの観測可能な挙動を押さえる。

## Read this when
- cmoc の変更に対して、既存の realization test がどの外部挙動、状態遷移、ログ、エラー条件を固定しているかを調べたいとき。
- apply fork/join/abandon、session fork/join/abandon、init、tui、indexing、review oracle、Codex runtime など、CLI サブコマンド単位の回帰テストを探すとき。
- Codex CLI 呼び出しの argv、stdin、CODEX_HOME、profile、structured output schema、retry、quota、resume、ログ保存など、外部プロセス wrapper の期待挙動を確認するとき。
- path token、repo root と work root、file access mode、sandbox mode、既定設定、構造化エラー、preflight など、cmoc 全体にまたがる runtime 挙動のテスト入口を探すとき。
- INDEX entry 生成、indexing preflight、prompt 部品、review 基準、routing/file access ルールなど、Codex に渡す prompt や structured output 周辺の期待値を確認するとき。
- 新しい realization test を追加する前に、同じ観点を既存テストや共通 helper に統合できるか確認したいとき。

## Do not read this when
- oracle file の正本仕様断片を確認したいとき。この領域は正本ではなく realization test なので、対象となる oracle doc、oracle src、oracle test を読む。
- プロダクト実装の責務分割、内部 helper、CLI 定義、runtime 処理、path model、状態モデルそのものを変更したいだけで、テスト上の期待挙動を確認する段階ではないとき。
- 個別サブコマンドや機能の実装入口が既に分かっており、外部挙動や回帰条件ではなく実装本文だけを読むべきとき。
- Codex CLI や LLM の出力品質そのものを検証したいとき。この領域のテストは外部 Codex 呼び出しを fake 化し、cmoc 側の制御と副作用を検証する。
- git helper、fixture、runner などの共通支援処理ではなく、特定のテストシナリオの期待出力や状態遷移だけを確認したいときは、該当する個別テストへ直接進む。

## hash
- f53b080ca19d9744c978c814aa54ab42620756923d809b7a60d3f45ccc0979bd
