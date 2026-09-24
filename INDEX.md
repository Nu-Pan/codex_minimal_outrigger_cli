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
- 人間が所有する正本仕様をまとめる入口です。製品の意味仕様、開発・テスト規則、検討した代替案の記録に加え、意味仕様から委譲されたアルゴリズムや agent 向け文面・schema の定義を扱います。
- 文書は要求や判断基準を、ソースは委譲された正確な処理や文面を所有します。どちらを根拠にするかは、対象事項の責務に応じて判断します。

## Read this when
- 仕様の正本や、文書とソースの責務・優先関係を確認したいとき。
- 横断的な製品仕様、開発・テスト規則、session と run のブランチ運用、または検討済みの代替案を探すとき。
- agent に渡す正確な文面や schema、仕様から委譲された処理の定義を探すとき。

## Do not read this when
- 対象機能やサブコマンドが特定できており、横断的な責務・優先関係の確認が不要なら、その機能の仕様へ直接進むとき。
- realization の実装やテストだけを調べる場合は、該当する realization の対象へ直接進むとき。

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
- cmoc の CLI command tree と各 command の Python 処理をつなぎ、共有 runtime を含む実装の中心。
- Codex・ACP の呼び出し処理や、正本側の定義を再公開する互換 import 入口も含む。

## Read this when
- CLI の command 登録と処理のつながりや、複数 command にまたがる runtime の動作を実装から追うとき。
- ACP 呼び出しや互換 import が、実行処理からどう使われるかを調べるとき。

## Do not read this when
- 調査・変更対象が特定の command、runtime helper、builder、互換 import に絞れているときは、対応する下位項目から読む。
- 正本の要求や定義を確認するときは正本側を、テストの期待値や fixture を確認するときはテスト側を読む。

## hash
- 39a5c9e34ab974c701131e3dc223519a46304f00e1087d9e55708d09d022b762

# `test`

## Summary
- pytest の単体・統合テストを集め、CLI と runtime の外部挙動、Git/worktree 操作、状態遷移、ログや報告の契約を検証する。これらの実装変更に対する回帰確認の入口となる。
- Codex の exec/TUI 起動、prompt とアクセス境界、プロセス管理、再試行・回復、および editor input、handoff、通知の連携を検証する。
- indexing、ファイル列挙、feedback の判定・処理・公開や、各種 builder の契約を検証する。正本に基づく振る舞いと CLI 経路の適合性を調べる場所である。
- 本番経路を使う統合テストも含み、実行後の終了状態や報告、Git と state の変化を確認する。外部推論の回答品質を評価する場所ではない。

## Read this when
- CLI、runtime、Git/worktree、state、ログまたは報告の挙動を変更し、既存の回帰検証範囲を調べるとき。
- Codex 呼び出し、prompt、プロセス管理、editor input/handoff、通知の境界や連携を変更するとき。
- indexing、ファイル分類、feedback、または builder の契約を変更し、CLI からの統合動作も確認するとき。

## Do not read this when
- 要件の正本を確認・改訂するときは、テストの期待値ではなく oracle の仕様本文を読む。
- 単一の機能の実装や不具合の原因を調べるときは、まず該当する実装と正本仕様を確認し、この配下全体を読む必要がない場合。
- 利用者向けの CLI の使い方や運用手順を調べるとき。ここは主に回帰検証とテスト用共有処理を扱う。

## hash
- fb2fbd4a22fa7f39d140d0deeaa1a236d42b7357c3f0aeed40821e29adf21118
