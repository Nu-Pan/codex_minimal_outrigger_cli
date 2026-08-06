# `reporter_input.json`

## Summary
- agent が検出した問題を人間向けの feedback reporter input として表現する JSON Schema。問題分類・重要度・影響・人間対応の理由・原因の確信度・再確認可能な根拠・作業継続状態を検証し、feedback collector へ渡す入力形式の入口となる。

## Read this when
- feedback reporter の入力項目、許容値、必須項目、文字数制限、原因や証拠の構造を確認するとき。
- agent が検出した問題を collector が受け取れる形式へ整形する処理を実装・検証するとき。

## Do not read this when
- collector 側の保存・集約・重複判定の仕様を確認したいとき。
- feedback の検出方法や agent の作業継続判断そのものを確認したいとき。

## hash
- c3c07e9f43494e5bcda5f9fefd3c65f6d89617409082a24f6a67656143b38f97
