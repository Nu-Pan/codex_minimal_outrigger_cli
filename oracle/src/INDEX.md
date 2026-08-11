# `oracle`

## Summary
- AI コーディングエージェント呼び出しに関する正本ソースの入口。共通モデル、用途別の agent call 定義、feedback 入力契約、prompt 構築、oracle の共通基盤を扱う下位領域へ進むための起点。

## Read this when
- agent call の共通パラメータ、モデル、推論強度、ファイルアクセス設定を確認するとき。
- indexing、feedback、oracle、realization、session、tui など用途別の agent call 定義を調査・変更するとき。
- feedback reporter の入力契約や、問題の分類・重要度・根拠・継続状態の表現を確認するとき。
- prompt の placeholder 解決、統合順序、標準規則、Structured Output 契約の入口を確認するとき。
- oracle の設定、パスモデル、agent instruction、構造化文書モデル、Markdown レンダリングを確認するとき。

## Do not read this when
- 通常のコマンド処理や agent call の生成処理そのものを確認するとき。
- collector 側の feedback 保存・集約・重複判定だけを確認したいとき。
- 個別の oracle 文書、realization 実装、realization test、既存 INDEX.md の内容を確認するとき。
- agent call と無関係な実装仕様や処理内容だけを調査するとき。

## hash
- a1beb47ea6b0f6593537431098cf6e5fe3784878032686f8bd812d145eba7d85
