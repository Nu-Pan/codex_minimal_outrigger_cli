# `oracle`

## Summary
- cmoc の正本ソースを集約する領域です。エージェント呼び出しのパラメータ・用途別プロンプト・Structured Output 契約、feedback 入力契約、パス・設定・規範・構造化 Markdown のモデルを扱います。各機能領域の実装やスキーマを確認する際の入口です。

## Read this when
- エージェント呼び出しの共通設定、用途別の prompt 構築、Structured Output の契約を調査・変更するとき。
- feedback reporter の入力形式や問題正規化の契約を確認するとき。
- パス解決、設定、規範モデル、構造化文書のレンダリングを確認するとき。
- oracle と realization の扱い、レビュー、ルーティングに関する正本プロンプトを確認するとき。

## Do not read this when
- 実際の CLI・TUI 実行フローや上位の agent call 制御を調査するとき。
- oracle/doc の自然言語仕様そのもの、通常の realization 実装・テスト、feedback の保存・集約処理だけを確認したいとき。
- 特定の下位領域の詳細が明らかな場合は、この領域全体を読まず、該当する下位要素へ直接進むとき。

## hash
- 8052eee95fafecc138dcaf9289c3d61c74ac59e8c131ca0e4404aaf7a7093624
