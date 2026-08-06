# `__init__.py`

## Summary
- feedback normalization 用の builder adapter パッケージ入口。feedback の正規化処理を builder 層から扱う必要があるときの起点となる。

## Read this when
- feedback normalization に対応する builder adapter の入口や責務を確認するとき。

## Do not read this when
- feedback の具体的な正規化ロジックや他の builder 実装を直接確認したいとき。

## hash
- 15f4c28e13a780cd6cf9d07ab5dbab29668875a19050011905cde72428413b05

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
