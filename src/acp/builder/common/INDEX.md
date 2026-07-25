# `prompt_fence.py`

## Summary
- `src/acp/builder/common/prompt_fence.py` は、ACP builder 間で共有する Markdown code fence 補正処理を提供する。動的本文に含まれるバッククォート列を調べ、外側の fence が本文中の fence より長くなるよう prompt の該当 section を置換する。対象 section の厳密な一致を確認できない場合は prompt を変更せず返す。

## Read this when
- ACP builder で、動的本文を含む Markdown code block の fence が正しく閉じない問題を調査・修正するとき。
- 共有される prompt section の検出条件、fence 長の決定、変更しない場合の挙動を確認するとき。

## Do not read this when
- ACP builder の prompt 固定文面や正本仕様を確認したいときは、対応する oracle 文書を直接読む。
- Markdown code fence 補正を使わない ACP builder の機能を調査するとき。

## hash
- ddf2098c98436ee26f3d2583832c6f85a970809635fd18aeda3c85d437bf16c8
