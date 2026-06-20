# `index_entry.json`

## Summary

- `INDEX.md` 用の目次情報を表す Structured Output schema である。
- 必要な項目は `summary`、`read_this_when`、`do_not_read_this_when` の 3 つである。
- 機械的な識別情報は含めず、ルーティング説明の自然言語だけを受け付ける。

## Read this when

- `INDEX.md` 用の目次情報を JSON でどう返すか確認したいとき。
- 対象を紹介する要約、読むべき条件、読まなくてよい条件の 3 分類を揃えたいとき。
- `cmoc indexing` の出力 schema を把握して、生成結果を検証したいとき。

## Do not read this when

- INDEX.md への反映手順や markdown レンダリング方法だけを確認したいとき。
- インデクシング以外の Structured Output schema や別の agent call parameter を探しているとき。
- 出力項目はすでに分かっていて、JSON の形だけを再確認したいとき。

## hash

- ae0ec45ebc0afcd5c1e83a5a01655b75075b0d0da3ce141b4e0913339ba56494

# `index_entry.py`

## Summary

- `cmoc indexing` の目次情報生成呼び出しの入口である。
- 対象パスを正規化し、対象内容と同階層の情報を含む complete prompt を組み立てる。
- 読み取り専用前提で、効率重視モデルと中程度の推論強度を使う構成になっている。

## Read this when

- ルーティング文書の目次情報を生成する流れを確認したいとき。
- 対象内容と同階層の情報が prompt にどう入るかを把握したいとき。
- 読み取り専用前提で、効率重視モデルと中程度の推論強度を使う呼び出し仕様を確認したいとき。
- Structured Output を使う `INDEX.md` 目次生成の入口を整理したいとき。

## Do not read this when

- `cmoc indexing` 以外のサブコマンドの呼び出し仕様を探しているとき。
- 対象パスの正規化や complete prompt の組み立てを追う必要がなく、出力形式だけを確認したいとき。
- 読み取り専用前提や Structured Output を使う流れではなく、別の実行経路を確認したいとき。

## hash

- 044a8a70d99e02aa13d215f4a03e99301cfcd1d46a59e94ded65cac119a77798
