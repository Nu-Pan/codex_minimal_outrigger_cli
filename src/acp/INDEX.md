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
- acp.builder の互換 builder adapter 群を収めるパッケージ。oracle.acp_builder の canonical builder を既存の acp.builder.* import 経路から利用できるよう再公開し、oracle・realization・feedback・indexing・session・TUI・quota probe の各領域へ進む入口を提供する。
- oracle edit／investigation では prompt 保存先の準備を行う realization adapter があり、その他の多くの builder は canonical 実装の関数を互換 import として再公開する。

## Read this when
- 既存の acp.builder.* import 経路を維持・移行・削除する条件を調査するとき
- oracle、realization、feedback、indexing、session、TUI、quota probe の builder adapter の構成と下位要素への入口を確認するとき
- canonical 実装への委譲関係や、oracle edit／investigation adapter が実行前に行う prompt 保存先準備を確認するとき

## Do not read this when
- oracle.acp_builder の canonical 実装そのものの仕様や詳細を調査・変更するときは、oracle 側の対象を直接読む
- builder の利用箇所や利用者向け公開面を調査するときは、各参照元を直接読む
- builder 共通の prompt 整形など、このディレクトリに含まれない共通処理を調査するときは、その実装対象を直接読む

## hash
- 11896ceb6b8393a3f3591e6887a401486516ff1176e6d6f9569da9e456cee8c3
