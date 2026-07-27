# `prompt_fence.py`

## Summary
- ACP builder で、動的な Markdown code block 本文に含まれる backtick によって外側の fence が誤って閉じないよう補正する共通処理を提供する。単一 section と review prompt 内の連続 section を対象に、canonical renderer で正規化した本文を特定して fence 長を調整する。

## Read this when
- ACP builder の prompt 生成で、動的 section の code fence 保護や section 実体位置の特定を変更・調査するとき。

## Do not read this when
- 固定的な prompt 定義や builder 固有の section 内容だけを変更するとき。Markdown code fence の補正処理を直接扱わない場合は、まず各 caller の実装を確認する。

## hash
- 53bf45c68f2496bd7c4ea1cbc7c3033d6fb47970634dba3ead9e5c4226418224
