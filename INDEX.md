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
- cmoc の正本仕様断片を置く領域であり、自然言語の仕様文書と、実装・テスト・設定として書かれた正本断片への入口になる。
- アプリケーション仕様、branch/worktree モデル、設計判断、開発規則に加えて、agent call parameter、prompt 構築、設定、パス表記、規範文書モデルなど、realization code が従うべき人間意図を確認する起点になる。

## Read this when
- cmoc の正本仕様断片から、実装・テスト・補助ファイルが従うべき要求を確認したいとき。
- CLI 挙動、サブコマンド仕様、Codex CLI 呼び出し、ログ、エラー、セッション状態、INDEX.md 自動生成、run 隔離などのアプリケーション仕様文書へ進む入口を探すとき。
- session fork / join、cmoc-managed branch、run branch、linked worktree、fork / join commit などの git branch / worktree モデルを確認したいとき。
- 採用されなかった設計案の背景や、不採用理由を確認して、自然に見える代替案を再導入してよいか判断したいとき。
- Python 実装、CLI 構成、開発環境、pytest 方針など、realization code を追加・変更する前の横断的な開発規則を確認したいとき。
- AI エージェントへ渡す prompt、role、goal、モデル設定、reasoning effort、ファイルアクセス方針、Structured Output schema の正本仕様断片を探すとき。
- 完全な agent call prompt が、標準プロンプト、補助プロンプト、ファイルアクセス規則、ルーティング規則、プレースホルダ定義からどう組み立てられるかを確認したいとき。
- 設定項目、既定値、リポジトリ別挙動設定、設定ファイルの永続化境界を確認したいとき。
- ルート概念、プレースホルダ付きパス、絶対パス、git worktree との関係を確認したいとき。
- 規範文書を構造化して保持するモデルや、階層化された文章を Markdown へ整形する helper の正本実装断片を確認したいとき。

## Do not read this when
- oracle file と realization file の一般的な責務分担、編集権限、品質基準、INDEX.md エントリー生成基準そのものを確認したいだけのとき。
- 現在の実装ファイル、テストファイル、既存関数、内部 helper、依存関係など realization code の具体構造を調べたいとき。
- CLI 引数解析、git 操作、branch 操作、実行フロー、保存処理、結果集約、表示処理など、正本実装断片を利用する realization implementation 側の制御を調べたいとき。
- 設定の読み書き処理、JSON 変換処理、状態ファイル操作、レビュー所見の生成・検証ロジック自体を探しているとき。
- 生成済みプロンプトをどこで agent call へ渡すか、または realization implementation や realization test の現在構造を追いたいとき。
- 既に読むべき個別の正本仕様文書、正本実装断片、または下位領域が特定できており、その本文を直接読む方が早いとき。

## hash
- 09e4d929f6bb5a3c1874f45c4d5c98661778adc1d6f923cc52f796c68957c9a9

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
- cmoc の realization implementation を収める領域。最上位 CLI 入口、サブコマンド実行制御、共通 runtime helper、設定・basic・ACP builder・oracle import 互換層など、利用者向け CLI の実体と既存 import 経路の維持を扱う。
- oracle 側の正本実装や正本仕様断片を複製せず参照・委譲する互換入口と、CLI サブコマンドが共通処理を組み合わせて外部挙動を作る実装領域へ進むための上位入口になる。

## Read this when
- cmoc の公開 CLI 構成、サブコマンド入口、引数から実装関数への委譲、console script 起動経路を確認または変更したいとき。
- init、indexing、tui、apply、session、review など、利用者向けサブコマンドの実行順序、preflight、git 操作、state 更新、Codex 連携、レポート生成を追いたいとき。
- Codex 呼び出し、INDEX 更新 preflight、設定、内容 hash、エラー表示、Git 操作、ログ、パス解決、外部コマンド結果、session state など、サブコマンド横断の共通 runtime helper を探したいとき。
- oracle 側の basic、config、ACP builder、oracle package などを realization 側へ複製せず、既存 import path や公開名を維持する互換入口、委譲先、削除条件を確認したいとき。
- CLI 実装、共通 runtime、互換 shim のどの下位領域へ進むべきかを絞りたいとき。

## Do not read this when
- oracle file の正本仕様断片、prompt 文面、出力条件、判定仕様、file access rule、path placeholder の概念定義を確認したいときは、対応する oracle 側を読む。
- ACP builder、basic API、設定定義などの正本実装本文を直接確認したいときは、互換入口ではなく正本側または実体 module を読む。
- 個別の低レベル helper、特定サブコマンド、特定 runtime API の所在がすでに分かっているときは、この領域全体ではなく該当する下位対象へ直接進む。
- 新しい仕様や API の正本を追加する場所を探しているとき。ここに含まれる互換層は既存参照維持のための入口であり、機能追加の正本ではない。
- Typer、Click、Git、Codex CLI など外部ツール一般の使い方を調べたいだけのとき。

## hash
- 88ed462a8f4d6ac68dc08907c54228fa14273f0a75452823c7d55988c1c56788

# `test`

## Summary
- cmoc の realization test 群を置くディレクトリ。CLI サブコマンド、Codex 実行 runtime、agent call parameter builder、prompt 組み立て、INDEX.md 更新、packaged import、共通 rendering など、実装が正本仕様断片から導かれる外部挙動を検証する入口になる。
- 一時 Git リポジトリや偽 Codex/Python 実行ファイルなどを使う共通テスト補助も含み、個別テストが Git 状態、Codex home、profile 差し替え、worktree path 解決の準備を重複して持たないための支援領域でもある。

## Read this when
- cmoc の実装変更後に、対応する CLI 外部挙動、終了コード、標準出力、状態ファイル、Git/worktree 副作用、report 内容の既存期待値を探すとき。
- apply、session、review oracle、indexing、init/TUI、Codex runtime、ACP builder、prompt parts、packaged import、Markdown rendering の回帰テストを確認または変更するとき。
- realization implementation の変更に合わせて realization test を追加・整理し、同じ観点の既存テストへケース追加できるか確認したいとき。
- テストで使う一時リポジトリ、Codex home、fake executable、branch/state 確認などの共通補助処理を探すとき。

## Do not read this when
- oracle file の正本仕様本文、標準、schema 定義そのものを確認したい場合は、oracle 側の文書または source を読む。
- 実装内部の helper 分割、型定義、低レベル git/runtime 処理だけを変更したい場合は、まず対応する realization implementation を読む。
- INDEX.md エントリーの自然言語内容だけを生成・更新したい場合で、CLI 境界やテスト期待値の確認が不要なら対象本文または routing 仕様を読む。
- Codex CLI や LLM の出力品質そのものを評価したい場合。このディレクトリのテストは主に fake executable や構造化された外部副作用で runtime 制御を検証する。

## hash
- 5fdbb9934490bb0d98ce2620569557fe936d74f97ce16b526e5b825f2f097104
