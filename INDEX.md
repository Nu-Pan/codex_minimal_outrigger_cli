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
- cmoc の realization implementation 全体の入口。公開 CLI、サブコマンド実装、実行時共通 helper、Codex 呼び出し境界、git・path・state・logging・INDEX 更新支援、ACP/basic/config/oracle 互換 import 境界など、実装本体と移行用公開面を束ねる。
- 利用者向け操作の入口は CLI 定義とサブコマンド領域へ、横断的な実行基盤は共通 helper 領域へ、正本側実装を再公開する旧 import 経路は互換領域へ分岐する階層である。

## Read this when
- cmoc の realization implementation のどこを読むべきか、CLI 入口、サブコマンド、共通 runtime、互換 import 境界の単位で最初に切り分けたいとき。
- 公開 CLI の command 構成、Typer app、console script 起動、または `session`・`apply`・`review` などのサブコマンド実装への委譲を確認したいとき。
- Codex exec/TUI 呼び出し、設定、runtime path、git 操作、session state、logging、quota retry、Structured Output、INDEX.md 自動更新 preflight など、複数機能から使われる共通実行基盤を探しているとき。
- ACP builder、基本型、設定、oracle package、runtime module 名などについて、正本側実装や既存実体 module を再公開する互換 import 経路の有無と削除条件を確認したいとき。
- init、indexing、TUI、apply、session、review oracle など、利用者操作単位の大きな orchestration から読む先を選びたいとき。

## Do not read this when
- oracle file による正本仕様断片、prompt 文面、path model の抽象定義、設定定義そのものを確認したいときは、実装領域ではなく oracle 側の該当本文を読む。
- realization test、fixture、README、補助スクリプト、生成物、実行ログなど、実装本体ではない対象を探しているときは、それぞれの領域へ進む。
- 特定の下位 package や module が読むべき対象だと既に分かっているときは、この階層で止まらず、該当下位領域または個別実装を直接読む。
- 既存互換 import path の維持と無関係に、新しい正本仕様や公開 API を設計したいだけのときは、互換入口ではなく対応する oracle file や実体実装を確認する。

## hash
- 7318b02556e65506f1d295df6f3c5043a81c3868e99918ddd5a2876d631a4053

# `test`

## Summary
- cmoc の realization test 群をまとめる領域。CLI サブコマンド、Codex 実行 runtime、prompt 構築、indexing、session/apply/review の外部挙動と制御境界を、実リポジトリや fake Codex 実行を使って検証する。
- 共通 fixture・補助関数と、機能別の realization test への入口になる。テストは正本仕様そのものではなく、oracle file と実装から導かれた外部挙動、状態遷移、ログ、終了コード、Git 副作用、report 生成、retry/cleanup 境界の回帰確認を担う。
- 大きなテストは、apply/session/review/runtime など同じ状態 fixture や制御 loop を共有する単一責務に凝集しており、該当機能の期待挙動を横断して確認するための読み取り単位として配置されている。

## Read this when
- realization implementation の変更が CLI の終了コード、stdout/stderr、状態ファイル、Git branch/worktree、report、commit、cleanup、ログ出力に影響する可能性があり、対応する外部挙動の期待値を確認したいとき。
- apply fork/join/abandon、session fork/join/abandon、review oracle、init/TUI、indexing、Codex runtime、prompt builder のいずれかについて、既存テストの観測点や境界条件を探すとき。
- Codex CLI 呼び出しを fake にした subprocess 制御、CODEX_HOME/profile/sandbox/cwd/schema path、quota/capacity retry、structured output validation retry の回帰観点を確認したいとき。
- 一時 Git repository、linked worktree、初期 commit、oracle 最小構成、fake executable、Codex home、apply worktree path など、CLI realization test の共通準備方法を探すとき。
- 新しい realization test を追加する前に、既存テストへケース追加できるか、同じ外部挙動や制御境界を検証するテストがすでにあるかを確認したいとき。
- prompt 部品、routing rule、file access rule、structured output schema、ACP builder parameter が最終 prompt や Codex 呼び出し条件へどう反映されるかを、realization 側の回帰テストとして確認したいとき。

## Do not read this when
- oracle file の正本仕様、用語定義、path model、標準文書、prompt 文言や schema の正本を確認したい場合は、oracle 側の本文を読む。
- 実装内部の関数分割、helper のアルゴリズム、状態 model、Git 操作 wrapper、report renderer、prompt rendering の詳細を直接変更する場合は、対応する implementation を先に読む。
- Codex CLI 本体や LLM 応答の品質、実際の認証フロー、外部サービスの挙動を評価したい場合は読まなくてよい。この領域は fake 実行や制御副作用を中心に検証している。
- 個別サブコマンドに関係しない一般論、設計方針、oracle と realization の関係だけを知りたい場合は、標準文書や該当する oracle doc を読む。
- 単にディレクトリ内の対象を機械的に列挙したい、または hash やファイル識別子だけを確認したい場合は、このエントリーの意味情報ではなくファイル一覧や生成済み routing 情報を使う。

## hash
- 50bd4ed3c0364f758166ff43734db79b0cb353c7c572c3d68e2574ef81df1bef
