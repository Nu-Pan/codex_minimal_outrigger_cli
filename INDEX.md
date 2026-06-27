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
- cmoc の realization implementation 全体を置く領域。公開 CLI 入口、サブコマンドの上位 orchestration、AI エージェント呼び出し用パラメータと標準プロンプト、共通 runtime helper、リポジトリ単位設定、基礎モデルや文書変換 helper など、実際に動作する実装本体を扱う。
- 下位要素は、利用者が実行する CLI command から各処理本体へ進む入口、session・apply・review・indexing・TUI・init の実行制御、Codex CLI 呼び出しとログ・状態・git・path・config の共有処理、Structured Output 付きの agent prompt 構築、互換 import 面などに分かれる。
- 正本仕様断片やテストではなく、oracle file で述べられた意図を具体化する realization code の入口であり、cmoc の挙動を実装側から確認・変更するための起点になる。

## Read this when
- cmoc の CLI コマンド構成、実行入口、サブコマンドから実装関数への委譲、または引数解析エラーの扱いを確認・変更したいとき。
- init、TUI、INDEX.md 更新、review oracle、apply run、session fork/join/abandon など、利用者が実行する機能の制御フロー、前提条件、git 操作、状態遷移、後片付け、利用者向け出力を追いたいとき。
- Codex CLI の exec/TUI 呼び出し、profile・sandbox・schema・ログ・quota/capacity retry・resume・preflight indexing など、AI エージェント実行基盤の実装を確認または変更したいとき。
- AI エージェントへ渡す role、summary、goal、補助文脈、file access rule、標準規範、Structured Output schema など、機能別の呼び出しパラメータ構築を調べたいとき。
- cmoc の共通 runtime helper として、設定ファイル入出力、エラー描画、git wrapper、実行結果モデル、session state、内容 hash、runtime path、subcommand log などの実装を探したいとき。
- モデルクラス、reasoning effort、ファイルアクセスモード、root token 付き path 解決、規範文書モデル、構造化 Markdown 生成など、複数機能で共有される基礎的な実装モデルを確認したいとき。
- cmoc の realization implementation を追加・整理・削除する変更で、既存の責務境界や下位領域の読む先をまず切り分けたいとき。

## Do not read this when
- 正本仕様断片そのもの、oracle file の自然言語仕様、path keyword の正本定義、oracle/realization の概念規範、INDEX.md エントリー規範などを確認したいときは、仕様側の本文を読む。
- cmoc の自動テスト、fixture、外部挙動の期待値、回帰検証観点を確認・変更したいだけのときは、テスト側へ進む。
- パッケージ設定、console script 配布設定、開発補助スクリプト、gitignore など、実装本体ではない補助ファイルを調べたいときは、それぞれの補助領域を読む。
- 生成済みの INDEX.md エントリー、レビュー report、Codex call log、subcommand log、session state などの成果物や実行時データを確認したいだけのときは、実装ではなく該当する保存先を見る。
- 特定の下位責務がすでに分かっている場合は、この領域全体を広く読むのではなく、CLI orchestration、共通 runtime、agent prompt 構築、基礎モデル、設定など該当する下位領域へ直接進む。
- cmoc の利用方法や人間向け概要だけを知りたい場合は、実装本体ではなく利用者向け文書やコマンドヘルプを確認する。

## hash
- 1d6745d43a84924b187a46948c25d7442d4fbc6d0fc6d052d21c176a2059de50

# `test`

## Summary
- cmoc の realization test 群を収める領域で、CLI サブコマンド、Codex runtime、prompt/schema、INDEX 生成、session/apply/review oracle などの外部挙動と制御ロジックを検証する入口になる。
- テスト用の最小 Git リポジトリ、Codex home、fake executable、Git helper などの共有補助も含み、個別テストは実 Codex ではなく fake 応答や monkeypatch を使って cmoc 側の副作用、出力、状態遷移、ログ、Git 操作を観測する。
- 大きい realization test は、同じ loop、report、schema、prompt などの読み取り文脈を一箇所に保つ意図を持ち、仕様本文の代替ではなく既存 realization の外部契約を確認するための根拠として位置づけられる。

## Read this when
- CLI の init、tui、session、apply、indexing、review oracle などのサブコマンドについて、終了コード、標準出力・標準エラー、Git branch/worktree 操作、状態ファイル更新、report 生成、cleanup、拒否条件を確認または変更したいとき。
- Codex CLI 呼び出しランタイムについて、argv/env/cwd、標準入力、profile、Codex home、ログ、structured output schema、retry、quota retry、TUI 起動、禁止領域変更検出などの外部挙動をテストで確認したいとき。
- prompt parts、standard 文書の注入、routing/file access rule、ACP builder の model・reasoning・file access mode、structured output schema の required・enum・validation 制約の回帰観点を調べたいとき。
- INDEX 生成、entry 検証、fresh hash 判定、INDEX だけを commit する制御、preflight、競合解決、root 直下 memo 除外とネストした memo の扱いを realization test から確認したいとき。
- apply fork/join/abandon や review oracle のように、fake Codex 応答を使った複数段 loop、report schema、dirty file 再検査、merge/conflict、rolling 対象選定などを同じ外部観測文脈で追いたいとき。
- 新しい realization test を追加する前に、既存の同じ観点のテストや共有 fixture へケース追加できるか、または不要になった旧テストを削除・統合できるかを確認したいとき。

## Do not read this when
- oracle file の正本仕様断片や自然言語仕様そのものを確認したいとき。仕様判断の根拠が必要なら oracle 側を読む方が直接的である。
- プロダクト本体の実装責務、内部 helper、状態モデル、path model、設定 loader、prompt builder、subcommand 実装を局所的に変更したいだけで、外部挙動や回帰テストの期待値をまだ確認する必要がないとき。
- Codex CLI や LLM の実出力品質、生成内容の妥当性、外部サービスとしての挙動を評価したいとき。この領域は主に fake executable や monkeypatch により cmoc 側の制御と副作用を検証する。
- 共有 fixture や Git helper の使い方ではなく、個別サブコマンドの実装フローや正本仕様の要求だけを調べたいとき。
- INDEX.md ルーティング文書の記述方針や schema 定義だけを確認したいときは、テスト群ではなく対応する standard、schema、または builder の本文を読む方が適切である。

## hash
- 3de208af0a526853e2a15ea8acb5bb50549e1ac0e15a80367cfc04bbdb34b0cb
