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

- ルーティング文書の目次情報をどう生成するか確認したいとき。
- 対象パス、対象内容、同階層の情報がどのように prompt に入るか知りたいとき。
- 生成呼び出しのモデル種別、推論強度、読み取り専用前提を確認したいとき。
- Structured Output 付きの呼び出しの流れを整理したいとき。

## Do not read this when

- 入力の組み立て方と出力形式がすでに分かっていて、実装を直接追いたいとき。
- 目次生成ではなく、別の呼び出し仕様を探しているとき。
- パス解決や prompt 部品の個別仕様だけを確認したいとき。

## hash

- 17067b80fa795c4985bd797561fd92f86c849461634a31d4c0d9287cb588b26d
