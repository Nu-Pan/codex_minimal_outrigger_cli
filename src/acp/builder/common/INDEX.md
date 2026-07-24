# `prompt_fence.py`

## Summary
- ACP builder 間で共有する Markdown code fence 補正処理を提供する。動的本文中のバッククォート列に応じて外側 fence を調整し、prompt 内の対象セクションを安全に囲むための共通実装。

## Read this when
- ACP builder の prompt 生成で、動的本文に code fence やセクション終了マーカーが含まれる場合の補正処理を変更・調査するとき。
- prompt の code block 境界検出、終了マーカーの選択、fence 長の決定ロジックを確認するとき。

## Do not read this when
- ACP builder の個別 prompt 構成や正本の prompt 仕様を確認したいだけの場合。
- code fence 補正を直接利用しない他領域の ACP 実装を変更するとき。

## hash
- 33f0c0d417163cde880933bb3d45067f64f278156a5533e0cb36c7e6b192c685
