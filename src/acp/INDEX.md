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
- ACP builder の互換アダプター群を収めるパッケージ。既存の acp.builder.* import 経路を維持しつつ、oracle 側の canonical builder、共通処理、feedback・indexing・oracle・realization・session・TUI 関連の下位実装へ進む入口を提供する。

## Read this when
- acp.builder 配下の互換 import 経路、builder adapter の構成、canonical 実装への委譲先を確認するとき
- ACP builder の共通処理、feedback・indexing・oracle・realization・session・TUI 関連の adapter を調査・変更するとき
- quota probe など、パッケージ直下にある個別 builder の呼び出しパラメータ生成や fallback を確認するとき

## Do not read this when
- canonical な oracle builder の仕様や本体ロジックを確認するときは、oracle 側の対象を直接読む
- 特定の下位 adapter の詳細実装を調査するときは、対応する下位パッケージまたはモジュールを直接読む
- acp.builder の利用箇所や利用者向け公開面を確認するときは、各参照元を直接読む

## hash
- 85f1ce5a05b815c10d79797e0be8827377c6bf6bd996b90f8e71cdeccc12d8cf
