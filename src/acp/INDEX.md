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
- ACP builder の prompt・parameter 構築を担うパッケージ。oracle、realization、session、TUI、indexing の各 builder adapter と、共通の prompt fence 補正・quota probe を下位要素として案内する。

## Read this when
- ACP builder の公開 import 経路、各 workload 用 builder adapter、prompt 生成、session join、TUI 起動、index entry 生成を調査・変更するとき。
- oracle または realization の edit・investigation・review・apply・refactor builder の呼び出し経路を確認するとき。

## Do not read this when
- canonical な正本仕様や具体的な builder 実装内容を確認したいとき。
- TUI 本体、fork 適用処理、一般的な Markdown 解析など、builder adapter の責務外を調査するとき。

## hash
- 7d62a474801724ccc519c2f4d96ebd2f94ad8e2b69407b0483ff612cf896ff85
