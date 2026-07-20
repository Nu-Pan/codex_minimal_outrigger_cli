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
- `acp.builder` として公開される互換ビルダーパッケージ。`oracle.acp_builder` への委譲や、既存の `acp.builder.*` import 経路を維持する入口を提供する。
- TUI、session、indexing、realization、oracle などのビルダー関連サブパッケージと、quota probe の互換入口を含む。

## Read this when
- `acp.builder` のパッケージ入口や、既存 `acp.builder.*` 参照との互換性を確認・変更するとき
- TUI、session、indexing、realization、oracle、quota probe のビルダー公開経路を辿るとき
- 各サブパッケージの責務や、canonical 実装への委譲先を確認するとき

## Do not read this when
- canonical な正本仕様や具体的なビルダー実装そのものを確認・変更したいとき
- TUI 本体、session 本体、apply・refactor など、ビルダー入口以外の処理を調査するとき
- `acp.builder.*` 互換参照の削除可否だけを判断するとき

## hash
- 97204a6923fe3dd3db3c3319195ea37c30c92eabdcc9ea9db609588c54e86a73
