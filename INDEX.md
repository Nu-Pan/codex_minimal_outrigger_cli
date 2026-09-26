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
- 人間が所有する cmoc の正本仕様をまとめる領域です。文書は要求や責務、判断基準、優先関係を定め、コードや設定は文書から委譲された正確なアルゴリズム、prompt の組み立て、schema などを定めます。
- 利用 workflow、CLI の挙動、session・run・branch の管理、ファイル分類、検索、ログ・エラー、feedback、agent 連携、開発規則、検討した代替案を扱います。Python の実装要素には、prompt や agent 呼び出しの組み立て、設定・パス・文書参照のモデル、検索、editor handoff も含まれます。

## Read this when
- cmoc の期待動作を変更・調査するときや、複数の仕様にまたがる責務と優先関係を判断するとき。
- 文書から委譲された prompt、agent 呼び出し、検索や handoff の具体的な構築方法を変更・確認するとき。
- cmoc の開発規則や branch・session・run の運用上の判断根拠を確認するとき。
- realization が人間の意図に適合しているかを確認するとき。

## Do not read this when
- 特定の CLI 機能の詳細だけを確認する場合は、その機能を扱う仕様項目へ直接進んでください。
- 実装の現在の挙動やテストだけを調べる場合は、該当する realization の実装・テストへ進み、必要な要求だけを対応する仕様項目で確認してください。
- 特定の prompt や agent 呼び出しの構築詳細だけを確認する場合は、該当する oracle source の実装へ直接進んでください。

## hash
- 64c1a6ff409020c59a045fb625ebad3bd320cfa06652e3d94803a486146a360a

# `pyproject.toml`

## Summary
- Python パッケージの配布設定、CLI コマンドの登録、依存関係、リソース同梱、および pytest・Ruff・mypy のプロジェクト設定をまとめた入口です。

## Read this when
- インストールや配布、利用可能なコマンド、依存関係、パッケージへのファイル同梱、テスト・静的解析の設定を確認または変更するとき。

## Do not read this when
- CLI の実際の処理や製品要件を調べるときは、該当する実装または oracle の仕様へ直接進んでください。

## hash
- 906a368dbc695aae9b6a59d73f66c0ac1d6bae72b2c6de7f5924b7aed93c9c13

# `src`

## Summary
- CLI の起動とコマンドツリーを定義し、各作業処理へ呼び出しを委譲するアプリケーション実装の入口。
- コマンド固有の処理と、Codex・Git・実行状態・設定・ログ・レポート・feedback・文書検索を支える共通 runtime を含む。
- 正本側の型や builder への互換 import 層と、文書検索用 Node worker の資材も含む。

## Read this when
- CLI の起動境界やコマンド登録、コマンド間の構成を確認・変更するとき。
- 複数の処理にまたがる共通 runtime の責務配置を把握し、調査の入口を決めるとき。

## Do not read this when
- 特定コマンドの処理や共通 runtime の一機能だけを調べるときは、その責務を扱う下位項目へ直接進む。
- 正本側の要求や型・builder の定義を確認するときは、互換 import 層ではなく対応する正本側の項目へ進む。

## hash
- eaa6355ab148cad41555f93d09a21404c287c73f236afbfffd7e126da2315792

# `test`

## Summary
- `pytest` による実装側の回帰テストと共有 fixture・helper をまとめ、実行時基盤、Codex 呼び出しと復旧、CLI および作業フローの挙動を検証する。
- 設定・state・worktree・ファイル分類、doctor・ログ・通知、prompt と editor handoff、session・run・oracle 操作、feedback observation の処理、oracle 文書検索などを対象とする。共有 fixture は一時 Git repository や Codex 環境を用意し、テスト中の toast 通知を隔離する。
- 実装のテスト入口であり、期待仕様の正本やコマンド・schema 定義の代わりではない。

## Read this when
- 変更や不具合に対応する回帰テストを探すとき。複数の機能層をまたぐ挙動や、テスト共通の環境設定を調べる場合にも参照する。
- 一時 repository、Codex の test double、editor handoff、通知隔離など、共有 fixture・helper の使い方を確認するとき。

## Do not read this when
- 要求や公開コマンド、schema の正本を確認するときは、該当する oracle の仕様・定義を直接読む。ここにあるテストは実装の振る舞いを検証するもので、正本仕様ではない。
- 変更や調査が単一の機能に限られる場合は、その機能に対応するテストと実装から始めればよく、テスト一式を通読する必要はない。

## hash
- 306c109784dc84914430facd67a6940b1e0d911e07d6c6a98d6e2392abd7c6ca
