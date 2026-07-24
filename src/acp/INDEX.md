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
- ACP builder realization の互換 adapter 群をまとめるディレクトリ。oracle 実装への互換入口、prompt の code fence 補正、oracle command・realization・session・TUI 向け builder adapter、quota probe fallback を扱う。各機能の詳細は対応する下位ディレクトリまたはモジュールへの入口となる。

## Read this when
- 既存の acp.builder.* import 経路、互換 adapter、canonical oracle builder への委譲を調査・変更するとき
- ACP builder の prompt 境界補正、oracle command builder、realization builder、session、TUI、quota probe の構成を確認するとき

## Do not read this when
- canonical な oracle builder の仕様や具体的な実装を確認するときは oracle 側の対象を直接読む
- 個別 builder の実装詳細を確認するときは対応する下位ディレクトリまたはモジュールを直接読む
- builder と無関係な TUI 本体、fork 処理、利用側の公開面を調査するとき

## hash
- f740e7285e7ba8338662bc641e9fcb1592761b551d0d52d011d35a5221ae7afa
