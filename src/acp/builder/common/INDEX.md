# `prompt_fence.py`

## Summary
- ACP builder で共有する Markdown code fence 補正処理を提供する。動的な section 本文に含まれるバッククォート列に応じて外側の fence を延長し、正規化済み本文と section 境界を維持する。

## Read this when
- ACP builder の prompt 生成で、動的本文を含む Markdown code block の fence 補正や、その canonical rendering との整合性を確認するとき。

## Do not read this when
- ACP builder 共通処理ではない prompt 生成仕様や、Markdown code block 補正を必要としない処理を調べるとき。

## hash
- 0341e548daca01c7a0f6096e14da47039764c752289325e6db30eba1317186e7
