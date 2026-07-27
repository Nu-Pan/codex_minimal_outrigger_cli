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
- ACP builder の realization package。oracle、realization、互換入口、共通処理、indexing、session、TUI などの builder 関連実装へ進むための入口を提供する。
- 配下には、ACP builder の初期化・互換公開、Markdown code fence 補正、index entry builder、quota probe、oracle/realization 向け adapter、session・TUI 向け builder、および review builder の実行時キャッシュが含まれる。

## Read this when
- ACP builder 関連の realization 実装の責務や配下モジュールの入口を確認するとき。
- builder adapter、互換 import 経路、prompt の code fence 保護、session・TUI・indexing 向け builder を調査・変更するとき。
- 目的の処理が配下の oracle、realization、indexing、session、tui などのどの領域に属するかを判断するとき。

## Do not read this when
- ACP builder の canonical な正本仕様・実装そのものを調査するときは、対応する oracle 側の対象を直接読む。
- TUI、CLI、apply、refactor など builder 以外の処理本体を調査するときは、それぞれの実装入口を直接読む。
- review builder の具体的な finding 処理や実装を変更するときは、生成キャッシュではなく対応する実装・テストを直接読む。

## hash
- 903f318d7cf1338b3fc282aa99f871603ab699d461e32e87d1a54ecd5631ccf3
