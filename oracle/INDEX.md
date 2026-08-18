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
- cmoc の agent call 用パラメータと prompt を構築する実装群です。設定・パス解決・構造化文書レンダリングなどの共通基盤に加え、TUI、session join、oracle review、indexing、feedback、realization 操作など用途別の起動定義と Structured Output schema を扱います。
- `oracle/other` が設定・パスモデル・構造化文書処理、`oracle/prompt_builder` が共通 prompt と policy 部品、`oracle/acp_builder` が用途別 agent call と schema、`oracle/feedback` が feedback 入力契約の入口です。

## Read this when
- agent call の起動パラメータ、モデル・推論設定、cwd、ファイルアクセス権、Structured Output schema の対応を確認するとき
- prompt の共通構成、oracle/realization や routing などの policy 統合、editor input の生成を調査・変更するとき
- cmoc の設定値・placeholder 付きパス解決・構造化文書のレンダリング処理を確認するとき
- indexing による INDEX.md エントリー生成、oracle review の所見処理、feedback の入力契約を確認するとき

## Do not read this when
- CLI サブコマンドの解析や実行制御そのものだけを確認したいとき
- 実際の agent backend・モデル名の解決や外部プロセス実行だけを確認したいとき
- oracle または realization の正本仕様、具体的な realization 実装・テストを確認したいとき
- TUI の画面表示・操作ロジック、または collector による feedback の保存・集約だけを確認したいとき

## hash
- 147db26ce3ac4bd915a20d102c67d821fc0b52dcce284e81d079552506e1dc29
