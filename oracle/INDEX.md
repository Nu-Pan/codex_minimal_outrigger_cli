# `doc`

## Summary
- cmoc の正本文書を領域別に参照するための入口。アプリケーション仕様、branch・commit・worktree、採用しなかった代替案、開発ルールを扱い、各領域の下位文書へ案内する。

## Read this when
- cmoc の挙動仕様・共通契約・サブコマンド仕様の入口を選ぶとき
- session fork、run の隔離、branch・commit・worktree の関係を調査・変更するとき
- 現行設計で不採用となった方式や仕様案と、その理由を確認するとき
- Python 実装、CLI 配置、開発環境、テスト要件・実行手順を確認するとき

## Do not read this when
- 対象の個別仕様や専用ルールが既に特定できており、下位文書を直接読む方が適切なとき
- 具体的な実装コード・テストコードの詳細だけを調査するとき
- INDEX.md の自動生成処理そのものを調査するとき

## hash
- ec096959e4eb52e19ebc398225c3d1ecfe16a9729c5ca403ab4f1eb62b539d10

# `src`

## Summary
- cmocのAIエージェント呼び出しを支える実装領域で、モデル・設定・パス解決・構造化文書・プロンプト構築・用途別の起動定義を扱う。共通呼び出し契約やquota probeはacp_builder、設定・パス・Markdown構造化ヘルパーはother、完全なpromptと各種policyはprompt_builder、およびoracle・realization・feedback・indexing・session・TUIなど用途別処理は下位ディレクトリへの入口となる。

## Read this when
- AIエージェント呼び出し全体の構成、共通パラメータ、プロンプト、設定、パスコンテキストの関係を確認するとき
- 複数のoracle実装領域にまたがる呼び出し契約やprompt構築経路を調査・変更するとき
- 用途別agent call定義や、acp_builder・other・prompt_builderの参照先を判断するとき

## Do not read this when
- 特定のagent callの詳細な起動パラメータや用途別処理だけを確認したいとき
- Codex CLIバックエンド固有のモデル解決だけを確認したいとき
- oracle・realizationの正本仕様や具体的な実装、個別policy、設定・パス・構造化文書ヘルパーの詳細を直接確認したいとき

## hash
- 5aca12ce788a76339c6a563a53a805226e1f9da09c28f6aa8d55ccfaedb57960
