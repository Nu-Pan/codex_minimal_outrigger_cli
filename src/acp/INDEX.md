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
- ACP builder の互換入口と realization adapter 群をまとめるパッケージ。canonical な oracle 実装への委譲、prompt の code fence 保護、indexing・session・TUI・quota probe・realization・command builder 向けの下位入口を扱う。各機能の詳細調査は対応する下位ディレクトリへ進む。

## Read this when
- acp.builder の互換 import 経路や公開入口を調査するとき
- ACP builder の prompt 補正、quota probe、session、TUI、indexing、realization adapter の構成を確認するとき
- oracle command builder の realization adapter 群への入口や下位パッケージの責務を把握するとき

## Do not read this when
- canonical な oracle builder の仕様・実装や prompt 内容を確認するときは oracle 側の対象を直接読む
- 具体的な adapter の実装詳細を確認するときは該当する下位ディレクトリのファイルを直接読む
- TUI 本体、fork 適用処理、builder 以外の CLI 処理を調査するとき

## hash
- a7d6580d49decf1962f4690ff055bf3312dd0070334eec45080cce8f7e0917a2
