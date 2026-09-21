# `AGENTS.md`

## Summary
- cmoc 自己開発時に、仕様文・agent への指示文・現在の agent への指示文を区別するための注意事項と、agent 向け指示文を単独で理解可能かつ仕様定義を含まない形に保つための基準。

## Read this when
- cmoc 自身のリポジトリを cmoc で開発しており、同じ文面が異なる情報レイヤーに現れる場合の解釈を確認するとき。
- cmoc が呼び出す agent への指示文を作成・確認し、仕様への暗黙の依存や仕様定義の混入を避けるとき。

## Do not read this when
- cmoc の仕様そのものを調べる必要があるとき。
- 具体的な実装、設定、CLI 挙動を確認する必要があり、レイヤー区別や agent 向け指示文の独立性が関係しないとき。

## hash
- da4f29cd7f635f81ead991302bf0b25e687760e47096c1c5efe20318b8c9a8f2

# `LICENSE`

## Summary
- This file is the repository's license grant and warranty disclaimer. Read it when you need to confirm redistribution rights, attribution obligations, or liability terms for using the project in another codebase or release.
- It is the right place to consult for legal permission questions about copying, modifying, sublicensing, or distributing the software.

## Read this when
- You need to know whether the project can be reused, copied, modified, merged, published, sublicensed, or redistributed.
- You need to confirm whether attribution or the license notice must be preserved in derived or distributed copies.
- You need the warranty and liability terms that apply to use of the software.

## Do not read this when
- You are looking for implementation behavior, CLI usage, configuration, or development workflow.
- You need repository structure or routing guidance; a different `INDEX.md` is the better entry point.
- You need project-specific legal exceptions or additional terms, which would have to be stated in another file.

## hash
- a894f2547af0349f234986eb4661f0146f37b7d82f8b22a27a674d5c1236f08f

# `README.md`

## Summary
- Codex Minimal Outrigger CLI の概要、初期セットアップ、基本ワークフローへの入口、運用上の注意点を案内するプロジェクトの導入文書。リポジトリを初めて使う場合や開発環境を構築する場合の起点となる。

## Read this when
- プロジェクトの目的や略称を確認したいとき
- 初期セットアップ手順を確認したいとき
- 基本ワークフローの参照先を知りたいとき
- ターミナルロックなどの運用上の注意を確認したいとき

## Do not read this when
- 基本ワークフローの具体的な仕様や操作手順を確認したいときは、リンク先の仕様文書を直接読む
- 恒常的なリポジトリ開発ルールを確認したいときは、開発指示文書を直接読む

## hash
- 6b9b1484c0f145d96180325067b4b8552f696e6ed12e84990ab90ed87d713cb6

# `bin`

## Summary
- cmoc の CLI 起動用シェルラッパー。仮想環境 Python の存在・実行可能性を確認し、通常起動では不足時の標準エラー報告後に `src/main.py` を実行する。補完プローブ時は Python が利用可能な場合のみ転送する。CLI の起動経路、Python 検証、起動失敗時のエラー形式、補完時の挙動を確認・変更するときの入口。

## Read this when
- cmoc コマンドの起動処理や、仮想環境 Python の検証・エラー報告を調査するとき
- シェルラッパーから `src/main.py` への転送条件や、自動補完プローブ時の分岐を変更・確認するとき

## Do not read this when
- CLI の実際の引数処理やアプリケーション動作を調査するときは、直接 `src/main.py` または対応する仕様を読む
- エラー内容の正本仕様や初回セットアップ手順を確認するときは、参照されているエラー処理・開発環境の文書を直接読む

## hash
- 70422bb34b7732bfa99d94d395b5c91f9aba3302293f0edba8366c10e7645dfe

# `codex_minimal_outrigger_cli.code-workspace`

## Summary
- VS Code のワークスペース設定を確認・変更するときに読む。ここには、このリポジトリを開いたときの既定インタプリタ、Python の解析対象、エディタ既定設定、非表示対象の方針がまとまっている。
- 日常的な実装変更やテスト追加では通常読まない。そうした作業は各実装・テスト・関連 `INDEX.md` を優先し、このファイルはエディタ環境やワークスペース構成に関する判断が必要なときだけ参照する。

## Read this when
- このリポジトリを VS Code のワークスペースとして開くとき
- Python の実行環境や解析対象の既定を確認したいとき
- エディタ側でどのファイルを見せるか・隠すかの方針を変えたいとき

## Do not read this when
- アプリケーションの挙動や CLI の仕様を確認したいとき
- 実装やテストの変更先を探したいとき
- 既存の各領域の `INDEX.md` や本文を読むべき作業をしているとき

## hash
- 1938307f70f255710d75d39c07d860ecb381acbb031ca19b2f2b6e565ac41acb

# `oracle`

## Summary
- 人間が所有し責任を負う正本仕様を集約する領域です。自然言語の意味仕様、正確なアルゴリズム・prompt・schemaを担う正本実装、関連する検査用の正本テストを扱います。
- `oracle/doc` には cmoc の目的、運用規則、ファイル分類、フィードバック、実行方式、開発規則などの意味仕様が整理されています。
- `oracle/src` には oracle doc から委譲された prompt 構築、ポリシー、index entry生成、設定・パスモデルなどの実行可能な正本詳細があります。

## Read this when
- cmocの要求、責務、制約、goal・non-goalなどの意味仕様を確認するとき
- promptの正確な文面、構築順序、schema、選択値など、oracle docから委譲された詳細を確認するとき
- realization側の実装やテストが人間の正本仕様に適合しているか調査するとき

## Do not read this when
- 製品の実装挙動だけを確認・変更する場合は、対応する `src` を直接読むとき
- 製品のテストだけを確認・変更する場合は、対応する `test` を直接読むとき
- 正本仕様ではなく、生成済みpromptや現在の実装から仕様を推測したいとき
- リポジトリ全体の作業規定や目次生成規則だけを確認する場合は、対応する運用文書を直接読むとき

## hash
- 525c3fea5fe4110620201dd4e369dfec0faf94929f4e7c4c8a11e19a8d248ddb

# `pyproject.toml`

## Summary
- Pythonプロジェクトのパッケージ metadata、依存関係、CLIエントリーポイント、ビルド・配布設定、およびpytest・Ruff・mypyの開発ツール設定を定義する。

## Read this when
- Pythonのバージョン要件、実行時・開発時依存関係、`cmoc`コマンドのエントリーポイント、パッケージ探索や配布内容を確認するとき。
- pytest、Ruff、mypyの共通設定を確認・変更するとき。

## Do not read this when
- CLIの具体的な処理やランタイム挙動を確認するとき。
- 個別テストの内容やテスト実行手順を確認するとき。

## hash
- 3a783c008041cc5d2791af2abb3cfe1c24d8231f77689b906b36f62158c77455

# `src`

## Summary
- cmoc CLI の実装全体を格納するルートで、`main.py` が Typer/Click のコマンドツリーと起動境界を定義し、`sub_commands/` が各 CLI サブコマンドの入口、`commons/` が実行ライフサイクル・ログ・エラー・Git・設定などの共有 runtime、`basic/` と `config/` が基礎型と設定、`acp/` が agent 呼び出しや realization/oracle/feedback/indexing の構築処理を担う。
- `src` 全体の CLI 起動経路や複数サブコマンドにまたがる runtime 挙動を確認するときの入口であり、特定コマンドの処理は `sub_commands/`、共有実行基盤は `commons/`、agent 呼び出し構築は `acp/` の対応する下位要素へ進む。

## Read this when
- cmoc の CLI コマンド構成、起動時の Click/Typer 境界、サブコマンドの大分類を把握したいとき
- 複数のコマンドに共通する実行 lifecycle、診断ログ、エラー処理、feedback、Git 状態管理の実装位置を探すとき
- agent 呼び出し・oracle・realization・indexing 関連の実装入口を探すとき

## Do not read this when
- 特定のサブコマンドの詳細な挙動だけを調べるときは `src/sub_commands/` の該当モジュールを直接読む
- 共有 runtime の個別責務だけを調べるときは `src/commons/` の該当モジュールを直接読む
- 正本仕様やテストの内容を確認したいときは `src` 全体ではなく対応する `oracle/` または `test/` を読む

## hash
- c8fd21c4ac63f2324638d87568a44162d2df51c7d88d9c0116f80e23070f1419

# `test`

## Summary
- cmoc の CLI、ランタイム、Codex サブプロセス、設定、状態管理を検証するテストスイート。
- ACP ビルダー、プロンプト編集、エディタ引き渡し、パッケージ化レイアウトなどの補助機能と互換性を検証する。
- インデックス生成、ファイル分類、doctor、oracle 操作、feedback 観測・復旧、実運用 CLI の統合挙動を検証する。
- 各テストファイルが機能領域ごとの具体的な回帰検出を担い、共通 fixture・テストヘルパーは同階層の `_*.py` ファイルに集約されている。
- `_real_path_integration` は実パスを用いた個別の統合テスト領域への入口である。

## Read this when
- テストスイート全体の検証範囲や機能領域を把握したいとき。
- CLI、ランタイム、インデックス、feedback、ファイルインベントリなど複数コンポーネントにまたがる変更の回帰影響を調べるとき。
- 共通 fixture やテスト支援コードを含め、テスト実行環境の構成を確認したいとき。

## Do not read this when
- 特定の機能の期待値・失敗条件・fixture 実装を確認したいときは、対応する `test_*.py` または `_*.py` を直接読む。
- 実装の仕様や正本の意図を確認したいときは、`src` または `oracle` 配下を読む。
- 実パス統合テストの具体的な検証内容だけを確認したいときは、`_real_path_integration` 配下へ直接進む。

## hash
- f91239366c1220efc469d5423f49f623efa7ae8ee1e2bff6dc6c86ee5c11bda7
