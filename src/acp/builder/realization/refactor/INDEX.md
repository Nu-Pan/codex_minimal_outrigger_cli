# `__init__.py`

## Summary
- realization refactor 用の builder adapter パッケージ。refactor 処理の builder 関連実装へ進む入口。

## Read this when
- realization refactor の builder adapter の責務や実装入口を確認するとき。

## Do not read this when
- builder adapter 以外の refactor 処理を確認するとき。

## hash
- 4c331bccb54a9842893b30e509c994292dd25afbf1159ad4b7929ebffb3a311d

# `fork`

## Summary
- cmoc realization refactor fork 用の builder adapter パッケージ。fork 関連の realization builder 接続処理への入口。
- realization refactor の change summary builder adapter。正本 builder の AgentCallParameter を再公開し、raw Git diff のコードフェンスを保護した prompt を生成する。
- realization refactor fork の file review and fix oracle builder を再公開する薄い adapter。詳細な parameter 定義は対応する oracle file に委譲する。

## Read this when
- cmoc realization refactor fork の builder adapter を変更・調査するとき。
- realization refactor fork の change summary 用 agent call parameter 生成経路や、raw Git diff の prompt 埋め込み処理を確認するとき。
- realization refactor fork の file review and fix parameter builder の参照先・公開 API・oracle builder との接続を確認するとき。

## Do not read this when
- fork 以外の builder 実装を調査するとき。
- 正本の builder 仕様、change summary JSON 定義、file review and fix の parameter 定義を確認・変更するとき。
- prompt fence 保護の共通実装自体を確認するとき。

## hash
- 684a048028b0f9ce11a6310d0c9f1813e085e3726980c2b5bceb6da83e4f331f
