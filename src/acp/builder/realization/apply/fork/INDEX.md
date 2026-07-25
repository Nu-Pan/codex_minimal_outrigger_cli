# `__init__.py`

## Summary
- `cmoc realization apply fork` 用の builder adapter を示す初期化モジュール。fork 適用処理の builder 接続点を確認する際の入口となる。

## Read this when
- `cmoc realization apply fork` の builder adapter の責務や配置を確認するとき。

## Do not read this when
- fork 適用処理そのものの実装詳細を調査するとき。
- `cmoc realization apply fork` 以外の builder adapter を調査するとき。

## hash
- 8ac1b4ff7590d29ce880b9d540f7fcace726de341416b79123260b174c415a65

# `launch_exec.py`

## Summary
- realization apply fork 用の launch_exec builder を再公開する adapter。正本 builder で生成した AgentCallParameter の prompt に対し、raw oracle git diff のコードフェンスを保護する。

## Read this when
- realization apply fork の launch_exec builder の挙動、prompt 生成、または raw oracle git diff の埋め込みを変更・調査するとき。

## Do not read this when
- apply fork 以外の builder を扱うとき。正本 builder 自体の仕様や実装を確認する場合は、対応する oracle file を直接読む。

## hash
- edf6e79c8004629ae426c74f51846e1c3291f4285ddcc771db1c6d9ce4a79a3d
