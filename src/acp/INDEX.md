# `__init__.py`

## Summary
- `acp` 互換の公開入口を扱う。`acp.*` を利用している既存参照を、`oracle.*` または実体モジュールへ移す必要があるときに読む。

## Read this when
- `acp` という公開名を残すべきか、削除できるかを判断したいとき。
- 既存の利用者向け参照を壊さずに、`oracle` 側の実体へ切り替える導線を確認したいとき。

## Do not read this when
- `acp` 配下の具体的な実装内容や移行先の詳細を知りたいだけなら、直接その実体モジュールを読む。
- 互換入口の存廃ではなく、`acp.*` の内部挙動そのものを変えたいだけならここではない。

## hash
- fe0939ab61e919bfb5ae35264e02859ee36efb102a15498d95fcbd45f9670e76

# `builder`

## Summary
- ACP builder の互換入口と realization adapter をまとめるディレクトリ。canonical な oracle 実装への接続、Markdown code fence 保護、index・oracle・realization・TUI・session などの builder 経路を下位要素として提供する。

## Read this when
- acp.builder 配下の互換 import 経路や canonical oracle 実装への接続を調査するとき
- ACP builder の prompt 生成、index entry、oracle・realization workload、TUI・session・quota probe の adapter を変更・確認するとき
- 下位の builder package や共通 code fence 補正処理へ調査を進めるとき

## Do not read this when
- canonical な builder の正本仕様・実装そのものを確認するときは oracle 側の対象を直接読む
- TUI の画面実装、CLI 本体、利用側の参照元を調査するときは、それぞれの対象を直接読む
- ACP builder と無関係な Markdown 処理や一般的な agent call parameter の仕様を調査するとき

## hash
- 37b45a410a3a1d56a4e5b9f87d0b3af73b528e59bc5bea081cb2f48daaeee03a
