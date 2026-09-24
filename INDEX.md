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
- 人間が所有する正本仕様の入口。文書は要求、責務、判断基準、意味上の優先関係を定め、ソース側はそこから委譲された正確な指示文、構築方法、選択値、スキーマなどを担う。
- アプリケーションの動作やワークフロー、状態・分離・出力に関する仕様に加え、開発・テスト規約、ブランチの扱い、検討した代替案を収める。実装や仕様判断で cmoc の人間意図を確かめる入口となる。

## Read this when
- cmoc の要求や動作条件を確かめて実装・テストの変更方針を決めるとき、または仕様と実際の挙動の不整合を調べるとき。
- agent に渡す指示文や構築方法、構造化された入出力の正確な定義が必要なとき。文書が意味を定め、ソース側に詳細を委譲している場合があるため、両者の責務を確認する。
- 開発規約、ブランチ運用、検討済みの設計判断など、機能仕様とは異なる根拠を確認するとき。

## Do not read this when
- 意図する挙動が既に分かっており、実装の内部動作やテストだけを調べるときは、実装またはテストへ直接進み、仕様との適合性が論点になった場合に必要な正本を参照する。
- 確認したいコマンドや規約が特定済みで、他の仕様との関係や優先判断も不要なときは、該当する個別の説明から読む。

## hash
- 1ac05e9fcd954a5919cc90b3dff98aca3377d2f392ffab5bd788a9c30ac54ffa

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
- cmoc の CLI 起動口、サブコマンド処理、共通 runtime を実装するソース群です。
- Codex の起動、Git と session/run の状態管理、feedback、index 更新、報告などの共通処理を含みます。ACP builder や basic/config には、oracle 側の定義を公開する互換アダプターもあります。

## Read this when
- CLI のコマンド選択から処理の流れを追うとき、または複数のコマンドにまたがる挙動を調べるとき。
- Codex 実行、Git と worktree、session/run、feedback、index 更新など、共通 runtime の境界や連携を調べるとき。

## Do not read this when
- 作業が特定のコマンド群や共通処理の一領域に限られる場合は、その下位項目から確認するとき。
- oracle 側の正本仕様や builder 定義が対象の場合は、互換アダプターを含むこのソース群ではなく、該当する正本から確認するとき。

## hash
- cd10fda489523c68120ec4281369ad49419407a4b86e55a0dc08f303e90b691e

# `test`

## Summary
- cmoc の振る舞いを検査する pytest の単体・統合テストと、共有 fixture・補助コードをまとめる。CLI、runtime、Codex 呼び出し、prompt、indexing、feedback、session/run state、filesystem などの回帰確認に使う。
- 実装の外部挙動や境界条件を実行可能な形で確かめる入口。プロダクト実装は src、規範的な要件の根拠は oracle の該当箇所を参照する。

## Read this when
- CLI や runtime、Codex 呼び出し、prompt、indexing、feedback、session/run state など、ここで扱う振る舞いを変更・調査し、対応する回帰テストや共有 helper を探すとき。
- pytest の失敗を調べるとき、または既存のテスト構成に沿って対象の振る舞いを検証するとき。

## Do not read this when
- 規範的な要求や人間の意図を確認するときは、テストを正本として扱わず、関連する oracle の文書・実装・テストを読む。
- テストや回帰カバレッジが作業対象でなく、実装の詳細だけを追うときは、該当する src の対象へ進む。

## hash
- 2730679763eed478a570b47ccadc270f377ac15fe54347030381e51fb393e0f6
