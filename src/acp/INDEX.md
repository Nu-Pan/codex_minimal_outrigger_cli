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
- `acp.builder` の互換公開パッケージ。旧 `acp.builder.*` import 経路を維持しつつ、oracle 側の canonical builder 実装へ委譲する各 builder adapter・互換入口をまとめる。下位の `oracle`、`realization`、`tui`、`session`、`indexing` などから、対象の builder 群や公開経路へ進むための入口となる。

## Read this when
- `acp.builder` 配下の互換 import 経路、公開入口、canonical 実装への委譲関係を確認・変更するとき
- oracle・realization・TUI・session・indexing など、builder 関連の下位パッケージの責務や入口を選ぶとき

## Do not read this when
- 個別 builder の canonical 実装や正本仕様を確認したいときは、対応する下位実装または `oracle` 側を直接読む
- TUI 画面本体、CLI 全体の動作、builder と無関係な処理を調査するとき

## hash
- e9e65853cae1861f85dffa50c39f34a57747d59358d8347ef179a6e025751158
