# `__init__.py`

## Summary
- feedback normalization 用の builder adapter を扱う。対応する oracle 実装を参照する際の入口となる。

## Read this when
- feedback の normalization 用 builder adapter の責務や対応する oracle file を確認するとき。

## Do not read this when
- feedback normalization 以外の builder 実装を調べるとき。具体的な normalization 処理の実装を確認する場合は、対応する oracle file を直接読む。

## hash
- 146a63c76ef83bf2091b863cb528329ee2171de4c27917d4367e8076d999d8c5

# `normalize_issue.py`

## Summary
- feedback issue の正規化パラメータを構築する正本 builder を再公開する adapter。feedback builder の公開入口として、正規化処理を利用する際に参照する。

## Read this when
- feedback issue の正規化パラメータ builder の公開入口を確認したいとき。
- feedback builder 経由で正規化処理を利用する箇所を調査するとき。

## Do not read this when
- 正規化 builder の実装や仕様そのものを確認したいときは、対応する oracle file を直接読む。
- feedback issue 以外の builder や正規化処理を調査するとき。

## hash
- e2c6155ff2f901eb4f7ffaa2e6a756a17bdf85e4d61d8bec81ae369673d228a3
