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
- cmoc の CLI 起動・コマンド別処理・共有 runtime を担う実装コードです。
- 一部の設定、基本型、ACP builder は正本側の実装を既存の import 経路で公開する互換層で、oracle package を解決する shim も含みます。

## Read this when
- CLI の起動、コマンド登録や引数処理から、個別処理の実行までをたどるとき。
- Git、worktree、session、run、Codex process、ログ、feedback、indexing など、複数コマンドで共有する実行基盤を調べるとき。
- 既存の import 経路が正本側の builder や設定・基本型へどう接続されるか確認するとき。

## Do not read this when
- 仕様上の挙動や agent に渡す指示の正本を確認するときは、oracle の仕様文書を直接読んでください。
- 特定コマンドの実行順序やエラー処理だけを調べるときは、そのコマンドの workload 実装へ直接進んでください。
- ACP builder の正本の内容や設定定義そのものを確認するときは、互換層を広く読むより正本側の実装を直接確認してください。
- テストの期待値や fixture を確認するときは、対応するテスト実装へ直接進んでください。

## hash
- 39a5c9e34ab974c701131e3dc223519a46304f00e1087d9e55708d09d022b762

# `test`

## Summary
- pytest による realization test 群。CLI サブコマンド、Codex 呼び出し、セッション状態、ファイル判定、indexing、feedback、editor handoff などの制御と、外部から確認できる結果を検証する。
- 共有 fixture や補助関数を備え、実 Codex CLI と実推論を使う本番経路の統合テストも含む。

## Read this when
- 制御ロジックの回帰テストを追加・修正するときや、関連するテスト領域を探すとき。
- 複数のテストで使う fixture や補助関数、本番経路の統合検証を変更するとき。

## Do not read this when
- 正本の要求や実装の詳細を確認・変更するときは、該当する仕様または実装を直接読む。
- 特定の振る舞いに対応するテストだけを追うときは、その領域のテストへ直接進む。
- テストの実行方法、選択、完了判定や報告の規則を確認するときは、専用の実行手順を参照する。

## hash
- fb2fbd4a22fa7f39d140d0deeaa1a236d42b7357c3f0aeed40821e29adf21118
