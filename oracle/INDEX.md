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
- oracle の実装定義を構成する領域。AI エージェント呼び出しの共通パラメータと用途別起動定義、設定・パス・構造化文書モデル、完全 prompt と各種 policy の構築処理を扱う。用途別の agent call は `acp_builder`、共通モデルや設定・レンダリングは `other`、prompt と policy の組み立ては `prompt_builder` へ進む。

## Read this when
- AI コーディングエージェント呼び出しのパラメータや、`cmoc` の用途別起動処理を確認するとき
- cmoc の設定モデル、root path 解決、構造化文書の Markdown レンダリングを確認するとき
- 完全 prompt の生成、placeholder の統合、oracle・realization・feedback・routing などの agent 向け policy を確認するとき

## Do not read this when
- 実際の CLI サブコマンド解析、TUI 実行、Codex CLI 呼び出しなど、oracle の定義を利用する側だけを確認したいとき
- oracle や realization の正本仕様、または個別機能の保存・適用処理だけを確認したいとき
- 共通の実装定義ではなく、下位領域の特定機能の具体的な挙動を直接確認できるとき

## hash
- d1db54ec1c00479286986364824e21ca2e297ed931e6f141b460f46d53462a36
