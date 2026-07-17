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
- ACP builder の互換入口と各種 builder 実装をまとめるディレクトリ。`acp.builder` 名前空間を維持しつつ、apply、review、session、TUI、indexing、quota probe などの下位 builder へ進むための入口を提供する。

## Read this when
- ACP builder の互換 import 経路、下位 builder package の構成、または builder 関連機能の入口を確認・変更するとき。
- apply、review、session、TUI、indexing、quota probe のいずれかを対象とする作業で、適切な下位要素への入口を判断するとき。

## Do not read this when
- 特定の builder の canonical な仕様や具体的な処理を確認したいときは、対応する oracle 側実装または下位の対象を直接読む。
- apply のループ制御、session の状態遷移、TUI の画面構成など、builder 以外の処理本体だけを調べるとき。

## hash
- 4355f2e0bdbc811fa3499b63272f199c8feaac3e436a55ce04277b29d101c7b0
