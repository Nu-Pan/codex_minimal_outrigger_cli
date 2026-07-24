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
- ACP builder の互換入口をまとめるパッケージ。oracle 側の canonical builder を既存の `acp.builder.*` import 経路へ接続し、共通の prompt 境界補正、indexing、oracle・realization・session・TUI 向け adapter、quota probe の fallback を提供する。各下位要素の責務を確認するための入口。

## Read this when
- ACP builder realization の全体構成や、既存 `acp.builder.*` import 経路を調査するとき。
- canonical builder への委譲、互換 adapter、prompt の code fence 補正、oracle・realization・session・TUI builder の配置を確認するとき。
- quota probe を含む builder parameter 生成の互換経路を横断的に確認するとき。

## Do not read this when
- canonical な正本実装や prompt 仕様そのものを変更・調査するときは、対応する oracle 側の対象を直接読む。
- 特定の builder adapter、共通補正、利用箇所の詳細を確認するときは、対応する下位要素または参照元を直接読む。
- ACP builder と無関係な TUI、session、realization workload、一般的な ACP parameter 処理を調査するとき。

## hash
- 37e11a4974f7df63d93efca5455742329ee0ae8060b6cbbfd3b85bfda80e607f
