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
- ACP builder の realization パッケージ。oracle 側の canonical builder への互換入口を提供し、prompt section の Markdown fence 補正、index・oracle・realization・session・TUI 関連の AgentCallParameter 生成や builder adapter を扱う。下位項目から処理領域別の互換経路・adapter 実装へ進むための起点。

## Read this when
- ACP builder の realization package 全体の責務、互換 import 経路、canonical 実装への接続を確認するとき
- prompt 生成における動的 section の code fence 保護や、各 builder adapter の配置領域を選ぶとき
- oracle、realization、indexing、session、TUI など特定領域の builder 実装へ進む入口を判断するとき

## Do not read this when
- canonical な oracle builder の仕様・実装そのものを確認または変更するときは、oracle 側の対応対象を直接読む
- 特定コマンドや処理の詳細実装を調査するときは、この階層ではなく対応する下位項目を直接読む
- ACP builder の利用箇所や利用者向け公開面を調査するときは、各参照元を直接読む

## hash
- 4a0a1c833dff4a201e4186b36631cdc9ae15a85cfbc0e99b05ff311a487bfae0
