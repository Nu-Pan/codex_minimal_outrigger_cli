# `prompt_fence.py`

## Summary
- ACP builder で共有する Markdown code fence の補正処理を提供する。動的本文を含む code block の外側 fence を本文中の backtick より長くし、canonical Markdown renderer による本文位置の特定、review prompt の複数 section 補正、描画後本文の正規化を扱う。

## Read this when
- 動的な prompt section や review section の Markdown code fence が本文中の code fence によって誤って閉じる問題を修正・検証するとき。
- ACP builder の prompt 生成で、section の実体位置や canonical Markdown rendering 後の本文を基準に補正する処理を確認するとき。

## Do not read this when
- ACP builder の固定 prompt 内容や review 判定ロジック自体を変更するとき。
- Markdown code fence や動的 prompt section を扱わない ACP builder の機能を調査するとき。

## hash
- 66fc738eb9344e5789ae9176fa6cf003b3e4525e6bd45ecf1c1d736fa6b8dd22
