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
- 対象ディレクトリには、ACP builder の互換入口、共通プロンプト整形、各 workload 別 adapter、canonical 実装への橋渡しを担う要素が配置されている。個別の責務や実装詳細を調査する際は、該当する下位要素へ進むためのルートである。

## Read this when
- ACP builder realization の全体構成や、互換入口・共通処理・workload 別 adapter の配置を確認するとき
- 対象ディレクトリ直下で、調査対象となる builder の種類や下位パッケージへの入口を判断するとき

## Do not read this when
- 特定の builder の具体的な入出力、CLI 挙動、canonical 実装、または利用側の参照を調査するときは、該当する下位対象や参照元を直接読む
- ACP builder と無関係な処理や、個別 adapter 内部の実装詳細だけを確認するとき

## hash
- 309313ae611238abfe470f492de7d2c0abed71d23cfc0b384e7a9a388d2a00ef
