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
- cmoc の正本仕様断片を置く領域であり、自然言語の仕様文書と、AI 呼び出し・prompt・設定・パス・構造化文書モデルなどの正本実装断片への入口を束ねる。
- アプリケーション仕様、branch/worktree モデル、設計判断、開発規則を扱う文書領域と、agent call parameter や完全プロンプト構築などを扱う実装断片領域へ進むためのルーティングを担う。

## Read this when
- cmoc の正本仕様断片を起点に、自然言語仕様または正本実装断片のどちらを読むべきか判断したいとき。
- CLI 挙動、サブコマンド仕様、Codex CLI 呼び出し、ログ、エラー、セッション状態、INDEX.md 自動生成、run 隔離などの仕様文書へ進む入口を探すとき。
- session fork / join、cmoc-managed branch、run branch、linked worktree、fork / join commit などの branch/worktree モデルを確認したいとき。
- 採用されなかった設計案の背景や、代替案を再導入してよいか判断するための正本仕様文書を探すとき。
- AI 呼び出しの role、summary、goal、prompt 断片、placeholder、モデル設定、reasoning effort、file access mode、出力契約を確認または変更したいとき。
- 完全プロンプトの構成順序、file access rule、routing rule、各種 standard の prompt 注入責務、設定、パス表記、構造化文書モデルを確認したいとき。

## Do not read this when
- oracle file と realization file の一般的な責務分担、編集権限、品質基準、INDEX.md エントリー生成基準そのものだけを確認したいとき。
- 現在の realization code の具体構造、既存関数、内部 helper、依存関係、テスト配置など、実装変更箇所を探したいだけのとき。
- CLI 引数解析、git 操作、branch 操作、作業レポート保存、結果集約、表示処理など、サブコマンド全体の実行フローを実装から調べたいとき。
- agent call のプロセス起動、具体的なモデル名への変換、結果処理、エラー処理など、正本仕様断片ではなく実装箇所を探しているとき。
- 既に読むべき個別の正本仕様文書や下位領域が特定できており、その本文を直接読む方が早いとき。

## hash
- ad4c594278b0c454604f82e85942de55725b05ae172be8391426a6909cc0442f

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
- cmoc の realization implementation 全体への入口。CLI 登録、サブコマンド実装、共通 runtime helper、互換 import 層、正本側実装への参照境界、ACP builder 関連入口を含む。
- 利用者向け CLI 挙動、実行時共通基盤、設定・basic・oracle 側実装の再公開、旧来 import path 維持など、realization 側で具体化された実装対象へ進むための上位ルーティング対象。
- この階層自体は正本仕様ではなく、oracle file の意図を実装へ落とし込んだ領域と、正本側実装を複製しないための薄い互換層を切り分ける入口である。

## Read this when
- cmoc の realization implementation のどこへ進むべきかを、CLI 入口、サブコマンド、共通 runtime、ACP builder、設定・basic・oracle 互換層の観点で選びたいとき。
- 公開 CLI コマンド構成、サブコマンド実行フロー、共通実行基盤、状態・Git・ログ・パス・エラー処理、INDEX.md maintenance などの実装入口を探しているとき。
- oracle 側の正本実装を realization 側へ複製せず、既存 import 経路や公開名を維持している境界、移行理由、削除条件を確認したいとき。
- Codex 呼び出しや AgentCallParameter 生成、quota availability probe、apply・review・session・TUI・indexing などの実装領域へ進む前に入口を切り分けたいとき。

## Do not read this when
- oracle file の正本仕様断片、正本文面、出力条件、path model、設定定義、ACP builder の定義内容そのものを確認したいときは、対応する oracle 側の本文を読む。
- 個別サブコマンド、特定 runtime helper、特定 builder など読む対象がすでに決まっているときは、この階層ではなく該当する下位対象を直接読む。
- AgentCallParameter 型、model、reasoning effort、file access mode などの基礎定義そのものを確認したいときは、基礎定義側を読む。
- 互換 import 経路の維持や realization 側実装と関係しない正本仕様の編集判断、画面仕様、状態仕様、利用者向け新機能の検討だけを行うときは、より直接その責務を持つ対象へ進む。

## hash
- e4431d001cab6761620ce1dd61ecc27a3c823ec72ee9771bea0404442861e62d

# `test`

## Summary
- cmoc の realization test 群を収める領域。CLI 外部挙動、Codex runtime、apply/session/indexing/review oracle、prompt、packaging、基礎 runtime の回帰観点を、機能ごとのテスト入口として整理している。
- 共通テスト補助も含み、一時 Git リポジトリ、Codex home、fake executable、branch/state/worktree 検証など、外部コマンドや agent call を伴うテスト前提を共有する。

## Read this when
- cmoc の実装変更後に、対応する realization test の確認先を機能別に探したいとき。
- CLI サブコマンドの出力、終了コード、state 遷移、worktree/branch cleanup、git 副作用などの外部挙動をテストから確認したいとき。
- Codex CLI 実行、TUI 起動、CODEX_HOME、retry、quota、file access violation recovery、call log など runtime 境界の回帰テストを探すとき。
- apply、session、indexing、review oracle、init/TUI、ACP builder、prompt parts、packaged import、StructDoc rendering の既存テスト観点を把握したいとき。
- 新しいテストを追加する前に、既存の共通補助や同じ観点のテストへ統合できるか確認したいとき。

## Do not read this when
- oracle file の正本仕様、oracle/realization の概念定義、INDEX.md エントリー生成規則そのものを確認したい場合は、oracle 側の文書を読む。
- 実装内部の責務分割、helper の本体、設定値や schema の定義元を直接変更したい場合は、対応する implementation または oracle src を先に読む。
- 個別機能に関係しない一般的なリポジトリ構成やパスモデルだけを確認したい場合は、より直接の routing entry から対象領域へ進む。
- Codex CLI や LLM の出力品質そのものを評価したい場合は、このテスト群ではなく実行制御や外部副作用の検証範囲として読む。

## hash
- b285826bef38279d334784c022d3d43961d3f98cfee14ec120edf90140e61279
