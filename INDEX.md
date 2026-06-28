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
- cmoc の正本仕様断片全体への入口。人間が所有する自然言語仕様、AI agent 呼び出し契約や標準プロンプトを定義する実装形式の仕様断片、正本性・実現物との関係を確認するための領域である。
- 利用者向け CLI 挙動、run/session/branch/worktree モデル、開発規則、non-goal、AI 呼び出しパラメータ、Structured Output schema、標準文書生成、共有データ構造など、realization file を正本仕様断片に沿わせるための根拠を探す起点になる。
- 下位には、自然言語で仕様判断を読む領域と、プロンプト・schema・設定・共有モデルを実装形式で読む領域があり、作業内容が公開挙動や設計判断なのか、AI 呼び出し契約や生成形式なのかで読む先を切り分ける。

## Read this when
- cmoc の仕様根拠を oracle file から確認し、realization implementation や realization test をどの意図に合わせるべきか判断したいとき。
- CLI の外部挙動、状態・ログ・出力、run 隔離、agent call 境界、session fork / join、branch / worktree 用語、開発規則、採用しない設計案の理由を確認したいとき。
- AI agent に渡す role、summary、goal、標準プロンプト、権限、モデル品質区分、reasoning effort、Structured Output schema、設定、パス表記、規範データ構造の正本仕様断片を確認したいとき。
- oracle file と realization file の関係、正本仕様断片として守るべき公開面・保存先・失敗時挙動・責務分担、または標準文書やルーティング規則がどうプロンプト化されるかを確認したいとき。

## Do not read this when
- 既存実装の具体的な関数、クラス、helper、git 操作、状態ファイル処理、外部プロセス起動、テスト期待値だけを調べたいときは、realization implementation または realization test を読む。
- 対象が自然言語仕様または実装形式の AI 呼び出し契約のどちらかに絞れているときは、この領域全体ではなく該当する下位領域へ直接進む。
- 個別の prompt builder、AgentCallParameter builder、schema、設定モデル、パスモデル、規範モデルなど、読むべき下位対象がすでに分かっているときは、その対象を読む。
- INDEX.md エントリー生成の一般基準、oracle file の正本性、realization file の編集責務など、提示済みの共通標準だけで判断でき、対象本文の仕様断片を追加で確認する必要がないとき。

## hash
- 4841c324d9619d505ed501af9f1d5ed78c83063821303c3727e251e92d9dee76

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
- `src` は cmoc の realization implementation を収める実装ルートであり、console script から起動される CLI 定義、利用者向けサブコマンドの orchestration、複数コマンドで共有される runtime helper、互換 import path の入口をまとめる。
- この階層は、CLI の公開面から実装本体へ入る起点であり、上位の仕様断片やテストではなく、実際に動作するコマンド配線・状態操作・Codex 呼び出し・git/worktree 操作・INDEX.md 更新処理の実装先を選ぶための入口になる。

## Read this when
- cmoc の実装本体を調べ、CLI コマンド定義、サブコマンド実行フロー、共有 runtime helper、または互換 import path のどこへ進むべきかを判断したいとき。
- 公開 CLI のコマンド構成、Typer app から各実装関数への委譲、通常の引数解析エラー表示、console script 起動の入口を確認または変更したいとき。
- 初期化、indexing、TUI、session、apply、review oracle など、利用者が実行するサブコマンドの orchestration、状態遷移、branch/worktree 操作、Codex 呼び出し、利用者向け出力への接続を追いたいとき。
- 設定読み込み、path 解決、git wrapper、session state、ログ、結果型、エラー表示、Codex exec/TUI profile、preflight indexing、内容 hash、INDEX.md 更新のような複数コマンドで共有される実行時基盤を探したいとき。
- 古い公開 import path がどの実体 runtime module に委譲されるか、互換入口を残す理由や削除条件を確認したいとき。

## Do not read this when
- oracle file が述べる正本仕様断片、path keyword の概念定義、oracle/realization の所有関係、または CLI 外部仕様の人間意図そのものを確認したいとき。実装ではなく oracle 側の本文を読む。
- realization test の期待値、fixture、テスト観点だけを確認したいとき。実装入口ではなくテスト領域へ進む。
- 個別コマンドや特定 runtime helper の対象がすでに分かっているとき。この階層全体ではなく、該当する下位モジュールまたは下位ディレクトリへ直接進む。
- 生成済みログ、レポート、作業中の session/apply 状態、または実行結果ファイルの内容を調べたいとき。ここはそれらを生成・操作する実装であり、生成物そのものの置き場ではない。
- Codex CLI 自体、外部 LLM の出力品質、Typer/Click/git/jsonschema など外部ライブラリ一般の仕様を知りたいだけのとき。ここは cmoc からそれらを使う境界実装を扱う。

## hash
- f72ef21c2746e9203d6fef59b203fe3f4e0e1ad471de42e1a03dcf4e3a89ad3a

# `test`

## Summary
- realization test 全体の入口。CLI サブコマンド、Codex 実行 wrapper、runtime 基盤、prompt 構築、indexing、review、session/apply の外部挙動と制御ロジックを pytest で固定する領域である。
- 共通補助関数は fixture、Git repository 構築、Codex home/profile 差し替え、fake executable、worktree path 解決を集約し、個別テストは各機能の状態遷移、標準出力、終了コード、report、永続 state、worktree/branch cleanup、保護領域検査などの観測結果を扱う。
- 大きなテストファイルの一部は、同じ CLI 境界や run 状態、fake Codex 応答、Git 状態、report 文脈を一箇所に保つために凝集されており、実装詳細よりも現行仕様上意味のある外部挙動と回帰観点を読むための階層である。

## Read this when
- realization implementation を変更する前後に、対応する CLI 外部挙動、runtime 契約、prompt 生成、Codex 呼び出し制御、Git/worktree/state 副作用の既存期待値を確認したいとき。
- apply、session、review、indexing、init/TUI、Codex runtime、basic runtime などのサブシステムについて、成功条件、拒否条件、error report、stdout/stderr、commit、cleanup、retry、保護領域検査の回帰テストを探すとき。
- Codex 実行を fake に差し替えたテスト、最小 Git repository fixture、認証済み Codex home、profile 生成差し替え、branch/state/worktree 準備など、CLI テストの既存パターンを確認したいとき。
- routing document 更新、INDEX 生成 preflight、hash freshness、semantic field validation、root 直下 memo 除外と nested memo 対象化など、indexing workflow の観測点を確認したいとき。
- prompt part、standard 文書注入、structured output schema、AgentCallParameter builder、file access mode、model/reasoning 設定がどのように組み合わさるかをテスト側から確認したいとき。

## Do not read this when
- oracle file の正本仕様断片そのものを確認したいとき。この階層は realization test であり、仕様の正本ではない。
- 実装 helper、state persistence、Git 操作、Codex subprocess wrapper、path model、profile 生成などの本体コードを局所的に変更したいだけなら、対応する実装領域を直接読む方がよい。
- 個別サブコマンドのテスト期待値ではなく、CLI コマンド定義や API の一般構造だけを把握したいとき。
- Codex CLI や LLM の出力品質そのものを検証したいとき。この階層の多くは fake executable や fake response を使い、cmoc 側の制御と副作用を固定する。
- テスト共通 fixture の使い方ではなく、特定機能のアサーションだけを確認したい場合は、共通補助ではなく該当機能のテスト本文へ直接進む方がよい。

## hash
- 2daf900dd7f11bdc8d279d83ecb3c38b14eed26358914df0954165d8672caeb1
