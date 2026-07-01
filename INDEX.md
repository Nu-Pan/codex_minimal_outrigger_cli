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
- cmoc の正本仕様断片を置く領域への入口。自然言語仕様を扱う文書群と、AI 呼び出し・共通概念・構造化出力契約などを扱う oracle src へ分岐する。
- CLI 挙動、branch/worktree モデル、agent call parameter、prompt 構築、Structured Output schema、パス概念、開発規則など、実装差を避けたい人間意図を確認する起点になる。

## Read this when
- cmoc の正本仕様断片から、利用者向け挙動、状態管理、作業隔離、ログ・出力、ルーティング文書生成、開発規則などの読むべき領域を選びたいとき。
- AI コーディングエージェント呼び出しに渡す入力、制約、モデル・reasoning effort、ファイルアクセス条件、応答契約などの正本仕様断片を探すとき。
- session fork / join、run branch、linked worktree、cmoc-managed branch、root path やプレースホルダ付きパスなど、cmoc 全体の共通概念を確認したいとき。
- 機能追加や workflow 変更の前に、自然言語仕様と oracle src のどちらを読むべきか判断したいとき。

## Do not read this when
- 実装ファイルやテストファイルの具体的なコード構造、既存関数、helper 分割、現在のテスト期待値だけを直接調べたいとき。
- 実際の CLI 引数解析、サブコマンド実行制御、git 操作、状態管理、ファイル書き込み、結果集約、表示処理など realization implementation 側の流れだけを確認したいとき。
- oracle file と realization file の一般的な責務分担、編集権限、標準本文そのものだけを確認したいとき。
- 既に読むべき個別の正本仕様文書または oracle src が分かっており、その本文へ直接進む方が適切なとき。

## hash
- b988bf458504b7aac703b6bab0fb1ef27bd30a4afd058fbd3e699cd819a1c580

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
- cmoc の realization implementation を収める最上位領域で、公開 CLI 入口、サブコマンド実装、runtime 共通基盤、設定・basic・ACP・oracle import 互換層などへ進むための入口。
- 実装本体と、正本側実装を複製せず既存 import 経路を維持する薄い互換入口が混在するため、CLI 制御、共通 helper、正本側への委譲、互換 import path の削除可否を切り分ける階層。
- 利用者が起動する操作の実装、複数機能から共有される runtime helper、oracle 側正本実装への橋渡し、既存公開参照の維持に関する下位領域を選ぶために読む。

## Read this when
- cmoc の realization implementation の配置を確認し、CLI 入口、サブコマンド、runtime 共通基盤、互換 import 層のどこへ進むべきか判断したいとき。
- 公開 CLI コマンド構成、利用者が起動するサブコマンド処理、またはサブコマンドから runtime・git・state・builder などへ委譲される大枠を追いたいとき。
- Codex 実行、INDEX 更新、設定、git、path、logging、state、外部コマンド結果など、複数の上位機能から使われる runtime helper の実装場所を探したいとき。
- 正本側の ACP builder、basic API、設定定義、oracle package を realization 側へ複製せず、既存 import 経路として再公開または接続している境界を確認したいとき。
- 古い公開 import path、薄い wrapper、互換 shim、再公開 module を残す理由、移行状況、削除条件を調べたいとき。

## Do not read this when
- oracle file にある正本仕様断片、正本側 builder、設定定義、path model、構造化文書 API の本文を確認したいときは、対応する oracle 側本文を読む。
- 実装ではなく realization test、fixture、テスト観点、テスト用補助コードを確認したいときは、テスト領域へ進む。
- 個別ファイルや下位領域の責務がすでに分かっており、具体的な生成ロジック、CLI 処理、runtime helper、互換 shim の本文を直接確認したいときは、その対象へ進む。
- 生成済みログ、保存済み state、report、キャッシュ、一時ファイルなど、実装ソース以外の成果物や実行結果を調べたいとき。
- 新しい正本仕様断片や oracle 側の内容を編集・設計したいとき。この領域は正本仕様ではなく、正本仕様を具体化する realization implementation と互換入口を扱う。

## hash
- 7d5b6ec19b9199f5a759453468c32ec6749a80333eb65e07092a8361c2078e7f

# `test`

## Summary
- CLI と runtime の realization test 群を収める領域。session、apply、indexing、review、init/TUI、Codex 実行ラッパー、prompt 構築、共通 test support など、利用者から観測できる外部挙動と重要な制御境界を検証する。
- 個別サブコマンドや共通 runtime の変更時に、期待される終了コード、出力、Git 状態、state 更新、worktree/branch cleanup、Codex 呼び出し制御がどのテストで固定されているかを探す入口になる。

## Read this when
- CLI サブコマンド、Codex 実行 runtime、prompt 構築、indexing preflight、review/apply/session の状態遷移を変更し、既存の外部挙動テストや追加先を探すとき。
- Git repository fixture、Codex home、fake executable、branch 状態確認、apply worktree path 解決など、CLI テスト共通の補助関数を使う、または変更するとき。
- worktree、branch、state file、report、commit、cleanup、error 表示先、retry、quota wait、sandbox/profile などの回帰観点がどのテストにあるかを切り分けたいとき。
- 新しい realization test を追加する前に、同じ観点の既存テストへ統合できるか判断したいとき。

## Do not read this when
- 正本仕様断片、oracle file や realization file の定義、routing entry standard、path model の意味を確認したい場合は、oracle 側の該当文書を読む。
- 実装内部の関数分割、helper の処理手順、型定義、設定読み込み本体などを直接変更する場合は、対応する実装側を先に読む。
- Codex CLI や LLM の出力品質そのものを評価したい場合は、このテスト領域ではなく、prompt や schema の正本仕様・生成処理を確認する。
- 個別機能の期待挙動をすでに特定できている場合は、このディレクトリ全体ではなく、対象機能のテスト本文へ直接進む。

## hash
- 3309eb3af3fa7f6ad0b0537813395fe114857ec96d4fda5c5f87357159ec15f3
