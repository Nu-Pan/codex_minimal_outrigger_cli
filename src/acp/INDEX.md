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
- acp.builder 配下の builder adapter と共通処理をまとめるパッケージ。oracle 実装への互換入口、realization・feedback・session・TUI などの処理別 adapter、共有プロンプト整形、indexing を下位要素へ振り分ける上位入口。

## Read this when
- acp.builder の全体構成や、処理種別ごとの builder adapter の入口を確認するとき
- 既存の互換 import 経路から oracle 実装・realization・feedback・session・TUI 関連の下位要素へ進む先を判断するとき
- builder 間で共有されるプロンプト整形や index-entry 生成の配置を確認するとき

## Do not read this when
- 特定の builder の実装仕様・入力制約・生成結果を確認したいときは、対応する下位要素または oracle の正本実装を直接読む
- acp.builder の利用箇所や利用者向け公開面を調査するときは、各参照元を直接読む
- builder と無関係な CLI 処理や、正本仕様・実装そのものを確認するとき

## hash
- 7fa14aaee877bcde1d604c21b7b424c3eb90557e1d0e102affbbcd1101386be1
