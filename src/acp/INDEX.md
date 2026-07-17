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
- `acp.builder` 配下の互換 builder package と、各 builder の canonical 実装への委譲入口を扱うディレクトリ。apply、indexing、review、session、TUI、quota probe などの既存 import 経路を維持し、必要に応じて各下位要素から個別の委譲経路や fallback を確認する。

## Read this when
- 既存の `acp.builder.*` import 互換性、canonical builder への委譲、builder parameter の公開経路を調査・変更するとき。
- apply、review、session、TUI、indexing、quota probe など特定 builder の互換入口や fallback の位置を確認するとき。

## Do not read this when
- canonical な builder の仕様・prompt・処理本体を確認したいときは、対応する `oracle.acp_builder` 側の実装を直接読む。
- TUI の画面挙動、apply fork のループ制御、session の具体的な状態遷移など、builder 入口以外の処理を調査するとき。
- 既存の互換 import 経路と無関係な新規公開 API や設計を検討するとき。

## hash
- 6dca84f0cced70681653adf3eca49a8b8f2812abc52fa7d05d1729a66d82d9f4
