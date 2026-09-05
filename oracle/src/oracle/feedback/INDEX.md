# `reporter_input.json`

## Summary
- cmoc feedback reporter が受け取る問題報告入力の正本スキーマ。分類、重要度、影響、workload 内で解消できない制約、原因、再確認用根拠、作業継続状態を定義する。

## Read this when
- cmoc_feedback.submit_observation に渡す報告入力の必須項目、許容値、文字数制約、根拠の記述条件を確認するとき。
- 問題報告の JSON 形式や、根拠の種類に応じた path 必須条件を確認するとき。

## Do not read this when
- 実際の問題報告を送信する手順や collector の処理を確認したいとき。
- reporter input のスキーマではなく、フィードバックの収集結果や重複判定の実装を確認したいとき。

## hash
- 7b17a9d08b99bd759f347a6a613599ee6229b46e7765e2012afbfbc208f72dfe
