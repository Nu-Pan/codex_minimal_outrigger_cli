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
- cmoc の正本仕様断片へ進むための入口。自然言語で書かれた仕様判断と、AI agent call・prompt・設定・パス表記・構造化文書モデルなどの正本実装断片を扱う領域を切り分ける。
- アプリケーション全体の外部挙動、branch / worktree モデル、不採用案、開発時の横断規則を探す場合と、agent call parameter、完全プロンプト、Structured Output schema、設定、パス解決、Markdown 整形 helper の正本断片を探す場合の起点になる。

## Read this when
- cmoc の利用者向け挙動、サブコマンド仕様、ログ、エラー処理、補完、Codex CLI 呼び出し、Structured Output、retry / resume、run 隔離、セッション状態、apply / fork / join などに関する正本仕様断片を探すとき。
- session branch、run branch、linked worktree、cmoc-managed branch、fork / join commit など、git branch・commit・worktree に関する cmoc 用語と責務を確認したいとき。
- 機能や workflow の追加時に、採用しなかった設計案とその理由、または Python 実装・CLI 構成・共通処理配置・開発環境・依存追加・pytest による決定論的テストなどの共通開発規則を確認したいとき。
- AI 呼び出しで使う role、summary、goal、prompt 断片、placeholder、モデル設定、reasoning effort、file access mode、出力契約を正本仕様断片から確認または変更したいとき。
- 完全プロンプトの構成順序、静的・動的 prompt 部品、file access rule、routing rule、各種 standard の prompt 注入責務を切り分けたいとき。
- cmoc の設定項目、既定値、永続化境界、リポジトリ別の挙動設定、ルート概念、プレースホルダ付きパス、絶対パス、git worktree との関係を確認したいとき。
- 規範文書を構造化して保持するモデルや、階層化された文章を Markdown として整形する helper を確認したいとき。

## Do not read this when
- oracle file と realization file の一般的な責務分担、編集権限、品質基準、INDEX.md エントリー作成基準そのものだけを確認したいとき。
- 実装モジュール、テスト、helper 分割、既存関数、現在のテスト期待値など、realization 側の具体的なコード構造だけを調べたいとき。
- CLI 引数解析、git 操作、branch 操作、作業レポート保存、結果集約、表示処理など、サブコマンド全体の実行フローを調べたいとき。
- agent call のプロセス起動、バックエンドが受理する具体的なモデル名への変換、結果処理、エラー処理を調べたいとき。
- 設定の読み書き処理、JSON 変換処理、初期化処理など、正本仕様断片ではなく realization 側の実装箇所を探しているとき。
- 特定サブコマンドや特定の仕様断片の読む先が既に分かっており、その本文から実装・テスト判断を行うだけのとき。
- 採用済み仕様ではなく実装都合だけを確認したいとき、または Codex CLI や LLM の実際の応答品質そのものを評価したいとき。

## hash
- e736f7ceac096827579e6ccadccce183c44810ac9642fb0870fc69a254c73d9a

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
- cmoc の realization implementation 全体への入口であり、CLI 入口、サブコマンド実装、runtime 共通部品、互換 import 層をまとめて扱う。
- サブコマンドの公開面と実行フロー、複数 workflow から使われる共通 runtime、正本側実装を複製しないための再公開・互換境界へ進むための分岐点になる。
- 正本仕様断片そのものではなく、oracle 側の定義や canonical 実装を realization 側の既存公開面・既存 import 経路・実行時処理へ接続する実装領域として位置づけられる。

## Read this when
- cmoc の実装を調べる起点として、CLI 登録、サブコマンド実装、runtime 共通部品、互換 import 層のどこへ進むべきか判断したいとき。
- 利用者向け CLI のコマンド階層、引数解析エラー処理、各サブコマンドの orchestration、git/worktree/state 操作、Codex 呼び出し、report 出力の実装入口を探したいとき。
- 複数サブコマンドで共有される config、path、git、ログ、session state、apply process、INDEX 更新、Codex 実行制御などの runtime 支援を確認または変更したいとき。
- oracle src 側の ACP builder、basic API、設定、oracle package などを realization 側へ複製せず、旧 import 経路や公開名として維持する互換層の理由・境界・削除条件を確認したいとき。

## Do not read this when
- oracle file にある正本仕様断片、prompt、structured output、path placeholder、file access rule、設定定義などの人間意図を確認したいだけのとき。
- 特定の実装対象がすでに分かっており、より直接の下位領域や実体 module を読めるとき。
- 生成済みログや実行履歴の内容確認だけが目的で、runtime logging、Codex 呼び出し、サブコマンド実装を変更しないとき。
- realization 側の旧 import 互換や公開面維持に関係しない正本側実装の本文、個別 builder の生成内容、共通型そのものの定義を確認したいとき。

## hash
- 19f324281a775bdc49a5dd78283c6444e033f470b20708f1d7b777a557276a08

# `test`

## Summary
- CLI 経由の外部挙動、Codex 実行 wrapper、ACP builder、prompt rendering、INDEX 更新、session/apply/review の状態遷移を検証する realization test 群。
- 共通 support で一時 Git repository、fake Codex/Codex home、session/apply state fixture を用意し、実装が正本仕様断片から導かれる公開契約を保っているかを確認する入口。
- 個別 command の成功・失敗・cleanup・report・file access rule・linked worktree・packaged import など、利用者から観測できる挙動の回帰確認を担う。

## Read this when
- CLI command の外部挙動、終了コード、標準出力、report、Git branch/worktree cleanup、永続 state 更新を変更または確認したいとき。
- Codex CLI/TUI 呼び出し、retry、quota wait、file access rule recovery、Codex home/profile、sandbox profile、call log など runtime 境界を変更または調査するとき。
- ACP builder、prompt parts、structured output schema 参照、packaged layout での import/re-export 境界を変更または確認したいとき。
- INDEX 更新 workflow、indexing preflight、routing document conflict 解決、空 directory・symlink・memo 除外など routing 文書生成の回帰を確認したいとき。
- session/apply/review oracle の統合フローで、dirty worktree、conflict、stale branch、linked worktree、process cleanup、state 破損などの境界条件を確認したいとき。
- テスト支援 fixture、fake executable、最小 repository、tracked ignored file、apply worktree 解決など、複数テストで共有される補助処理を変更したいとき。

## Do not read this when
- 正本仕様断片そのもの、oracle source の schema 内容、path model や file 分類の定義を確認したい場合は、oracle 側の対象本文を読む。
- プロダクト実装の内部 helper、Git 操作、prompt builder、Codex runtime、state 管理の局所的な実装だけを変更したい場合は、対応する implementation を先に読む。
- Codex や LLM の出力品質そのものを評価したいだけで、cmoc 側の呼び出し契約や回帰観点に触れない。
- 個別テストの assertion や fixture ではなく、ルーティング文書の記述規則や INDEX.md entry の自然言語品質だけを確認したい場合は、仕様文書側を読む。

## hash
- 7c58b6c274696462800613826aa649f63e53852d17a5c6e598316ab897085a7b
