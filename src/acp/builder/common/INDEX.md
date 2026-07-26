# `prompt_fence.py`

## Summary
- ACP builder で共有する Markdown code fence 補正処理を提供する。動的本文を含むコードブロックの外側 fence が本文中のバッククォート列と衝突しないよう、正規化済み本文を解析して必要な長さへ調整する。

## Read this when
- ACP builder のプロンプト生成で、動的な Markdown code block の fence 補正や関連する本文レンダリングを変更・調査するとき。

## Do not read this when
- ACP builder の共有処理ではなく、プロンプト全体の構成や他の Markdown レンダリング仕様だけを確認するとき。

## hash
- 319a21d63913d35b7417428b382754827cb6c535887cd6299fbee6197b3cabf5
