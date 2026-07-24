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
- ACP builder の互換入口と realization adapter 群をまとめるディレクトリ。canonical な oracle 実装への委譲、prompt の code fence 補正、index・session・TUI・quota probe・realization・review 向け builder 接続を扱う下位要素への入口。

## Read this when
- acp.builder 配下の互換 import 経路や builder adapter の構成を確認するとき
- 各サブコマンドの builder 接続、AgentCallParameter 生成、prompt 加工、canonical 実装への委譲経路を調査するとき
- このディレクトリ直下の builder 共通処理または下位 adapter の責務を切り分けるとき

## Do not read this when
- canonical な oracle builder の正本仕様・実装や prompt 内容を確認するときは oracle 側の対象を直接読む
- 具体的な adapter の実装詳細を確認するときは該当する下位パッケージやモジュールを直接読む
- builder 以外の TUI 本体、CLI 処理、利用側の参照を調査するとき

## hash
- 358d520c88bf7df2dc4a96cf01c83198730822212a39b757d790576b4986b867
