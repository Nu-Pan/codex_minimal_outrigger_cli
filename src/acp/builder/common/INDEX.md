# `prompt_fence.py`

## Summary
- ACP builder で共有する Markdown code fence 補正処理を提供する。動的なセクション本文に含まれるバッククォート列より外側 fence を長くし、code block が途中で閉じないようにする。補正対象の特定には canonical Markdown renderer を用いる。
- 外部からは code fence 補正関数と、canonical rendering 後の code block 本文を取得する補助関数が入口となる。

## Read this when
- ACP builder の prompt 生成で、動的本文を含む Markdown code block の fence が正しく維持される仕組みを変更・調査するとき
- section heading、終了 marker、info string、section body を用いた fence 補正の探索条件や置換処理を確認するとき
- Markdown rendering normalization または struct_doc との連携を確認するとき

## Do not read this when
- ACP builder の個別 prompt 内容や正本の prompt 仕様自体を確認したいときは、prompt の生成元または指定された oracle file を直接読む
- Markdown code fence 補正と無関係な ACP builder の機能、CLI 挙動、または一般的な Markdown 処理を調査するとき

## hash
- 1fec148c42e2f78ecc72949b6abc72ddd6bd5dae869844eed6d5c43d490100e0
