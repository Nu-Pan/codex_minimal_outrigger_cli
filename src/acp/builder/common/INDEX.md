# `prompt_fence.py`

## Summary
- ACP builder が共有して利用する Markdown code fence 補正処理を提供する。動的本文中のバッククォート列に応じて code block の外側 fence を調整し、prompt の構造化されたセクション境界を維持する。

## Read this when
- ACP builder の prompt 生成で、動的本文に code fence や長いバッククォート列が含まれる場合の補正処理を確認するとき。
- prompt 内の指定セクションを検出し、code block の fence 長を安全に置換する処理を変更するとき。

## Do not read this when
- ACP builder の正本となる prompt 仕様や固定長 fence の定義を確認したいときは、参照先の oracle 文書を直接読む。
- ACP builder の共有補正以外の prompt 生成処理や CLI 挙動を調査するとき。

## hash
- 847469d6bfedd14a4a31fb8ab7b50bb58bfde1be4595408f10622d127894af4c
