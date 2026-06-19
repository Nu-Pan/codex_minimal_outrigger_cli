# `index_entry.json`

## Summary

- `INDEX.md` 用の目次情報を表す Structured Output schema である。
- 必要な項目は `summary`、`read_this_when`、`do_not_read_this_when` の 3 つである。
- 機械的な識別情報は含めず、ルーティング説明の自然言語だけを受け付ける。

## Read this when

- `INDEX.md` 用の目次情報を JSON でどう返すか確認したいとき。
- 対象を紹介する要約、読むべき条件、読まなくてよい条件の 3 分類を揃えたいとき。
- `cmoc indexing` の出力 schema を把握して、生成結果の検証をしたいとき。

## Do not read this when

- 目次情報の markdown レンダリング方法や、`INDEX.md` への書き込み手順だけを確認したいとき。
- インデクシング以外の Structured Output schema や別の agent call parameter を探しているとき。
- 出力に含めるべき項目がすでに分かっていて、JSON の形だけを再確認したいとき。

## hash

- 39fab97858c4e81c5ec3ebe8a1c0d3cfcc3d798ffbe3631ddcf5ba639eac9916

# `index_entry.py`

## Summary

- ルーティング文書の目次情報を生成する呼び出しの入口である。
- 対象パスを正規化し、対象内容と同階層の情報を含む完全な prompt を組み立てる。
- 読み取り専用前提で、効率重視モデルと中程度の推論強度を使う構成になっている。

## Read this when

- ルーティング文書の目次情報を生成する流れを確認したいとき。
- 対象内容と同階層の情報がどのように prompt に入るかを把握したいとき。
- 効率重視モデルと中程度の推論強度を使う読み取り専用の呼び出し仕様を確認したいとき。
- Structured Output を使う目次生成の入口を整理したいとき。

## Do not read this when

- 目次情報の生成処理そのものではなく、別の呼び出し仕様や別サブコマンドの入口を確認したいとき。
- 対象パスの正規化や完全な prompt の組み立てを追う必要がなく、出力形式だけを確認したいとき。
- 読み取り専用前提や Structured Output 付き呼び出しの流れを確認する目的ではないとき。

## hash

- b048a1cdfb6fcb60c747f6e26fa24744488d65db2f5a81d3e5eb004bf49b8fe6
