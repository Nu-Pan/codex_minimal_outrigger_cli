# `join`

## Summary
- `cmoc session join` の merge conflict marker 解消に向けた AI エージェント呼び出しパラメータを構築する実装への入口。対象パスの解決、競合解消用 prompt、最高品質設定を扱う。

## Read this when
- `cmoc session join` の merge conflict 解消フローを変更・調査するとき
- 競合対象ファイルのパス解決、prompt 内容、エージェント呼び出し設定を変更するとき

## Do not read this when
- `session join` 以外のサブコマンドの prompt 構築を変更するとき
- merge conflict 解消処理そのものや共通 prompt 構築処理を直接変更するとき

## hash
- b9e16aae5abced3607ff61610005c3d9e04d48157e9ed4176ee53f506c091178
