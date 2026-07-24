# `prompt_fence.py`

## Summary
- ACP builder で共有する Markdown code fence 補正を提供するモジュール。動的本文に含まれるバッククォート列を調べ、外側の code fence を必要に応じて長くして、Markdown の誤った閉鎖を防ぐ。

## Read this when
- ACP builder の prompt 生成で、動的な code block 内容により Markdown code fence が壊れる問題を扱うとき。
- section heading、終了マーカー、info string を指定して既存 prompt の該当セクションを補正する処理を確認するとき。

## Do not read this when
- prompt の正本仕様や固定長 fence の定義を確認したいときは、参照される oracle 文書を直接読む。
- ACP builder 共通処理以外の prompt 生成や Markdown 解析を変更するとき。

## hash
- a9d03b29e9fc28dc05ed5edf4c252db081428c472a71ef2f2f79d0f0f01adb79
