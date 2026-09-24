# `AGENTS.md`

## Summary
- cmoc の自己開発で、仕様文・呼び出す agent への指示・現在の agent への指示を区別するための開発上の注意を示す。
- agent への指示を作成・確認する際に、指示の自己完結性と仕様文との分離を判断する入口となる。

## Read this when
- cmoc を使った自己開発で、同じ文面が異なる情報レイヤーに現れ、どの指示として扱うか判断するとき。
- agent に渡す指示を作成・確認し、単独で理解できることや仕様記述との分離を確認するとき。

## Do not read this when
- 個別の cmoc 機能要件や実装内容を確認するときは、該当する仕様文書または実装を直接読む。
- agent 指示のレイヤーや自己完結性が作業に関係しないとき。

## hash
- da4f29cd7f635f81ead991302bf0b25e687760e47096c1c5efe20318b8c9a8f2

# `LICENSE`

## Summary
- ソフトウェアと付属文書の利用・改変・配布に関する許諾条件、著作権表示の保持条件、保証否認と責任制限を示します。

## Read this when
- 利用、複製、改変、公開、配布などの許諾条件や、著作権表示・免責事項を確認するとき。

## Do not read this when
- 実装の動作、設計、開発手順を調べるときは、該当するソースコードや仕様文書を直接確認してください。

## hash
- a894f2547af0349f234986eb4661f0146f37b7d82f8b22a27a674d5c1236f08f

# `README.md`

## Summary
- Codex CLI を使った開発を補助する cmoc の概要と、初期セットアップの入口です。
- 基本ワークフローへの案内と、Ctrl+S によるターミナル停止を防ぐヒントを含みます。

## Read this when
- cmoc の役割を把握したいときや、導入後にコマンドを使えるよう設定したいとき。
- 基本ワークフローの参照先や、Ctrl+S でターミナルが停止する問題への対処を探すとき。

## Do not read this when
- AI に渡す詳細な作業規定を確認するときは、エージェント向けの指示文を直接読んでください。
- 基本ワークフローの具体的な手順を確認するときは、専用のワークフロー説明を直接読んでください。

## hash
- 6b9b1484c0f145d96180325067b4b8552f696e6ed12e84990ab90ed87d713cb6

# `bin`

## Summary
- コマンドの起動入口として、ローカルの仮想環境 Python を確認してからアプリケーション本体へ処理を引き継ぎます。起動前の環境エラーと補完プローブ時の起動経路も扱います。

## Read this when
- コマンド起動時の Python 検査、起動失敗の報告、または補完プローブ時の起動経路を調べる・変更する場合。

## Do not read this when
- コマンドやオプションの仕様、実際の処理や出力を調べる・変更する場合は、アプリケーション本体や仕様書を直接確認してください。
- 仮想環境の作成・インストール手順を調べる場合は、開発環境の説明を直接確認してください。

## hash
- 70422bb34b7732bfa99d94d395b5c91f9aba3302293f0edba8366c10e7645dfe

# `codex_minimal_outrigger_cli.code-workspace`

## Summary
- VS Code workspace 設定。開くフォルダー、Explorer で非表示にする項目、Python の interpreter と解析対象、Python と Markdown の編集設定を定めます。

## Read this when
- VS Code で開くフォルダーや Explorer の表示、Python の interpreter・解析対象、Python の保存時フォーマット、Markdown のインデント設定を変更するとき。

## Do not read this when
- アプリケーションの動作、Python の依存関係や環境構築、テスト・CI の方針を変更するとき。該当するソースやプロジェクト設定を確認してください。
- INDEX.md の内容やルーティング文を編集するとき。対象の INDEX.md とその生成規定を直接確認してください。

## hash
- 1938307f70f255710d75d39c07d860ecb381acbb031ca19b2f2b6e565ac41acb

# `oracle`

## Summary
- 人間が所有する cmoc の正本群をまとめ、要求・責務・判断基準を定める意味仕様、開発規則、利用 workflow、branch model、検討した代替案の記録へ進む入口。
- 意味仕様は要求の内容を定め、そこから委譲された正確な algorithm、選択値、prompt 構築、schema はプログラム上の定義が所有するため、変更する事項の責務に応じて参照先を選ぶ。

## Read this when
- cmoc の変更について、正本要求や開発上の制約、workload・branch の扱い、既存の設計判断を確認する必要がある。
- agent に渡す prompt や呼び出し設定など、文書仕様から委譲された正確な定義の所在を確認する必要がある。

## Do not read this when
- 対象となるコマンドや挙動の仕様が特定できている場合は、その責務を持つ個別仕様から確認を始める。
- 要求の変更を伴わない実装・テスト作業では、対応する実装・テストと適用される個別の正本仕様を確認する。

## hash
- 6461d17e820f91023eee9a668b5afdd3163fb37d2f428739d6461418c9ebc3a2

# `pyproject.toml`

## Summary
- Python 配布物のメタデータ、依存関係、CLI 起動点、setuptools のビルド・パッケージ設定を定める。
- pytest の実行設定と Ruff・mypy の静的検査設定をまとめる。

## Read this when
- 依存関係、インストール、配布、CLI の起動点を変更・確認するとき。
- Python のテスト実行条件や lint・型検査の設定を変更・確認するとき。

## Do not read this when
- コマンドの実際の動作や実装を調べるときは、該当する実装を直接読む。
- 製品の規範的な要求を確認するときは、該当する正本仕様を直接読む。

## hash
- 3a783c008041cc5d2791af2abb3cfe1c24d8231f77689b906b36f62158c77455

# `src`

## Summary
- cmoc の CLI command tree と、各コマンドの処理への受け渡しを定義する。
- 複数コマンドが使う runtime を担い、Codex 起動、設定、Git と state、ログとレポート、feedback、INDEX 更新などの共通処理をまとめる。
- コマンド固有の処理と ACP builder の adapter を含み、一部の旧 import 経路から oracle 側の正本実装や型を公開する。

## Read this when
- CLI の command 構成や、コマンド名から実処理へ至る経路を確認するとき。
- 変更が複数コマンドにまたがる、または Codex 起動・設定・Git と state・ログ・feedback・INDEX 更新などの共通処理に関わるとき。
- この領域の import 経路が oracle 側の正本実装や型をどう公開しているか調べるとき。

## Do not read this when
- 特定コマンドの処理だけを追う場合は、そのコマンド固有の処理領域から読む。
- 単一の共通 runtime 処理だけを変更・調査する場合は、その処理を担う領域から直接読む。
- oracle 側の正本仕様や実装自体を確認・変更する場合は、対応する oracle の文書やソースを直接読む。

## hash
- 1824cb2179c104e9b51340753f72ae42ed944cf5d795ea350bfd43b0aec32e2d

# `test`

## Summary
- 実装挙動の回帰テストをまとめ、CLI の各種操作、Git・worktree と session/run の状態管理、indexing、feedback report の処理を検証する。
- Codex の起動設定、出力処理、quota 待機・回復、中断時の subprocess 制御、TUI 通知といった runtime の契約も扱う。
- prompt と builder、構造化文書、設定、パッケージ import、wrapper を確認するテストに加え、実 CLI を独立プロセスや PTY から検証する受け入れテストがある。共有 helper と fixture は Git repository、外部コマンド、通知 transport などをテスト用に隔離する。

## Read this when
- CLI コマンドや report、indexing、feedback、session/run の挙動を変更し、回帰を確認する場所を探すとき。
- Codex runtime の設定・出力・回復・中断処理や prompt/builder の変更が、既存の契約に与える影響を調べるとき。
- 本番経路に近い独立プロセス・実 CLI・PTY の検証や、テスト環境の共有 fixture と隔離方法を確認するとき。

## Do not read this when
- 期待される仕様だけを確認したいときは、対応する正本仕様や schema を直接読む。
- 現在の処理実装を追うだけなら、対象機能の実装へ直接進む。
- 一つの限定された挙動の assertion を調べる場合は、その領域の個別テストへ進み、テスト群全体の責務を読む必要はない。

## hash
- b870f0c64965e0a8848270bdb6ca23372944797601b0e643b7f309e3f8aeeb64
