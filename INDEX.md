# `AGENTS.md`

## Summary
- cmoc リポジトリで作業する AI agent 向けの最上位作業規約を定める。リポジトリの略称、パス表記、ルーティング文書の利用、アクセス禁止・編集禁止対象、正本仕様断片と実装・テスト配置の基本方針を扱う。
- 作業開始時に従うべき共通前提をまとめた入口であり、個別仕様や実装詳細へ進む前に、読む順序と触れてよい領域を判断するための基準を提供する。

## Read this when
- cmoc リポジトリで作業を始める前に、基本的な作業規約、読みに行くべき仕様領域、編集可能な領域を確認したいとき。
- パス表記の意味、正本仕様断片の位置づけ、実装とテストを置く場所、閲覧・編集してはいけない対象を確認したいとき。
- ルーティング文書をどのように使って必要なファイルを探すべきか、作業中のファイル探索方針を確認したいとき。

## Do not read this when
- 個別機能の詳細仕様、CLI の具体的な挙動、出力形式、テスト期待値を調べたいだけの場合。その場合は正本仕様断片や該当する実装・テストへ進む。
- 特定モジュールの実装構造や関数の挙動を確認したい場合。その場合は実装配置の下位対象へ直接進む。
- ルーティング文書そのもののエントリー内容や同階層の対象一覧を確認したい場合。その場合は同階層のルーティング文書を読む。

## hash
- be280f67baf8ea9e564641d6ae7327aff20fd9575bc114fa291f3c5de87833ac

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
- CLI 起動のための薄いシェルラッパーを置く領域。リポジトリルート基準で仮想環境 Python を探し、通常起動や補完プローブを Python 実装へ委譲する入口を扱う。
- 仮想環境 Python が存在しない、または実行できない場合に、利用者向け Markdown エラー、セットアップ手順、表示用パス、簡易 call stack を出力して失敗させる起動前処理を扱う。

## Read this when
- コマンド起動時にどの Python 実装へ処理が委譲されるかを確認したいとき。
- 仮想環境が未作成または実行不能な場合の、起動失敗時の利用者向け出力や終了挙動を確認・変更したいとき。
- シェル補完プローブ時に通常起動と異なる分岐を取る理由や、補完時の失敗コードを確認したいとき。
- 起動前エラーの文面、セットアップ手順、表示用パス、call stack 行番号の組み立てを確認・変更したいとき。

## Do not read this when
- Python 側の CLI サブコマンド、引数解析、業務ロジック、実行後の出力内容を調べたいとき。
- 仮想環境の作成方法そのもの、依存パッケージ、プロジェクト設定を変更したいとき。
- oracle file、path model、または正本仕様断片の定義を確認したいとき。

## hash
- bcc444f615624a979df5ebba33008d88c68e9f32a99b58386f9f0158f7e98b02

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
- cmoc の正本仕様断片を置く領域であり、自然言語の oracle doc と実装形式の oracle src への入口になる。
- アプリケーション仕様、branch/worktree モデル、採用しなかった代替案、開発規則、AI agent 呼び出しパラメータ、prompt、設定、パス表記、規範文書などを下位領域に分けて扱う。

## Read this when
- cmoc の正本仕様断片を確認したいとき。
- 自然言語で書かれた仕様、設計判断、開発規則へ進む入口を探すとき。
- oracle src に定義された agent call、Structured Output schema、prompt 構築、設定、パス表記、規範注入の正本仕様断片を確認したいとき。
- CLI 挙動、サブコマンド仕様、Codex CLI 呼び出し、ログ、エラー、セッション状態、INDEX.md 自動生成、run 隔離、branch/worktree モデルに関する正本仕様文書を探すとき。
- apply fork、review oracle、indexing、tui、session join、ファイルアクセス規則違反リカバリなど、別 agent call に渡す prompt と呼び出し条件の正本を探すとき。

## Do not read this when
- 現在の実装ファイル、テストファイル、既存関数、内部 helper、依存関係、プロセス起動、git 操作、状態ファイル更新、結果表示など realization code の具体構造を調べたいとき。
- realization test、realization implementation、補助スクリプト、生成物、または実際の差分適用箇所を探しているとき。
- oracle file と realization file の一般的な責務分担、編集権限、品質基準、INDEX.md エントリー生成基準そのものだけを確認したいとき。
- パスキーワードやルートディレクトリ概念そのものの定義だけを確認したいとき。
- 既に読むべき個別の正本仕様文書、oracle src、または下位領域が特定できており、その本文を直接読む方が早いとき。

## hash
- 2af6656d2a7793b20a12c9e87767e41e076ee853dde36ff69367abca5417344a

# `pyproject.toml`

## Summary
- Python プロジェクトの配布・ビルド・テスト実行に関わる設定をまとめる補助的な設定ファイル。パッケージ名、Python バージョン、実行時・開発時依存、CLI エントリーポイント、setuptools の収集対象、テスト時の import path を定義する。
- 実装本体や正本仕様ではなく、実装ファイルと oracle 側 Python パッケージをどのようにインストール・検出・テスト実行環境へ載せるかを確認する入口になる。

## Read this when
- 依存パッケージ、要求 Python バージョン、ビルドバックエンド、setuptools のパッケージ検出、package data の扱いを確認または変更したいとき。
- CLI コマンド名がどの Python callable に接続されるかを確認または変更したいとき。
- テスト実行時にどのソースツリーが import 対象へ追加されるかを確認したいとき。
- 実装側ソースと oracle 側ソースを同じ Python プロジェクト内でどう配置・配布しているかを確認したいとき。

## Do not read this when
- CLI の具体的な挙動、サブコマンド処理、実行時状態管理、出力内容を調べたいときは、実装ソースを直接読む。
- 正本仕様断片や用語定義、設計意図を確認したいときは、oracle 側の本文を読む。
- 個別テストケースの期待値や検証観点を確認したいときは、テストソースを読む。
- リポジトリ全体のルーティングや各ディレクトリの読む順序を判断したいだけのときは、該当階層のルーティング情報を読む。

## hash
- d01948ab1730e2747d529d49d8c8ca10b84bd6a86e19d7b2810ee87c95ccb904

# `src`

## Summary
- cmoc の realization implementation を収める領域で、CLI 入口、サブコマンド実行制御、共通 runtime helper、互換 import 層を扱う。
- 公開 CLI から各サブコマンド実装への委譲、Codex 呼び出しや INDEX 更新などの共通処理、oracle 側正本実装を複製しないための再公開・shim の入口になる。
- 下位対象へ進む前に、個別コマンドの制御フロー、共通 runtime 処理、旧 import 経路の互換維持、oracle 側実装への接続境界のどれが主対象かを切り分けるために読む。

## Read this when
- cmoc の CLI コマンド構成、サブコマンドへの委譲、起動時の import 境界、または利用者向け実行入口を確認・変更したいとき。
- init、indexing、tui、apply、session、review などのサブコマンド単位の実行順序、preflight、git 操作、state 更新、Codex subprocess 連携、失敗時処理を追いたいとき。
- Codex exec/TUI 呼び出し、INDEX 更新 preflight、設定、内容 hash、Git、ログ、runtime path、session state など、複数サブコマンドから共有される runtime helper の読む先を選びたいとき。
- oracle 側の basic、config、ACP builder、runtime 実装を realization 側へ複製せず、既存の公開 import 経路や旧 import path をどの互換入口で維持しているか確認したいとき。
- 互換 wrapper、再公開 module、shim の残置理由、委譲先、公開名、移行状況、削除条件を判断したいとき。

## Do not read this when
- oracle file の正本仕様断片、prompt 文面、出力条件、file access rule、path model、ACP 基本型、設定定義そのものを確認したいときは、対応する oracle 側を読む。
- 個別 helper、個別サブコマンド、互換入口のどれを読むべきか既に決まっているときは、この階層ではなく該当する下位対象へ直接進む。
- 実装本体ではなく正本仕様の変更判断、新しい API 仕様や設定項目の追加判断だけをしたいときは、この realization implementation 領域を起点にしない。
- Typer、Click、Git、Codex CLI など外部ツールの一般的な使い方を調べたいだけのときは、この対象を読む優先度は低い。
- 生成ロジック、repo root 解決、型変換、prompt 補正、状態ファイル schema などの詳細を直接確認したいときは、該当する下位実装または正本側実装へ進む。

## hash
- d643c6e946ed7355eb900a934e8ef7a59c9b42b30f31b5178b609f78fb990485

# `test`

## Summary
- cmoc の realization test 群を置く領域。CLI サブコマンド、Codex runtime、ACP builder、prompt rendering、packaged import、INDEX.md 更新など、realization implementation の外部挙動と制御ロジックを pytest で検証する。
- 共通 fixture と helper はテスト補助対象に集約され、個別テストは session/apply/review/indexing/init/runtime などの変更時に期待される終了コード、出力、git/worktree 副作用、state 遷移、prompt/schema 連携を確認する入口になる。

## Read this when
- realization implementation を変更した後、その変更が CLI 外部挙動、Codex 呼び出し、state 更新、git/worktree 操作、prompt/schema 生成に与える期待値を確認したいとき。
- session fork/join/abandon、apply fork/join/abandon、review oracle、indexing、init、TUI 起動前処理、Codex runtime など、サブコマンドや runtime 境界の回帰テストを探すとき。
- oracle source や prompt/schema 定義との連携が、realization 側 builder、packaged layout、structured output schema path、complete prompt で壊れていないか確認するとき。
- CLI テスト用の一時 Git repository、Codex home、fake executable、branch/state 検証など、テスト前提を作る共通補助処理を確認または変更するとき。

## Do not read this when
- oracle file の正本仕様本文、oracle/realization file の定義、実装標準、INDEX.md エントリー規則そのものを確認したい場合は、oracle 側の文書を読む。
- 個別 helper や production code の内部構造、関数分割、低レベルな git/path/config 実装だけを変更する場合は、まず対応する implementation 側を読む。
- Codex CLI や LLM の出力品質そのものを評価したい場合は、このテスト領域ではなく対象外として扱う。
- INDEX.md エントリーの自然言語内容だけを作成・編集したい場合で、CLI 更新ワークフローや生成処理の外部挙動を確認する必要がないとき。

## hash
- 1094e669ae444681299cebe5aca5ee857885def39dcf7e7f6e37a5107a3e2b3d
