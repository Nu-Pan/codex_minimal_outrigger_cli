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
- ACP builder の realization package 群をまとめるディレクトリ。旧 acp.builder 系の互換入口、oracle builder への委譲、indexing・oracle・realization・session・TUI 関連の builder adapter を下位要素への入口として扱う。

## Read this when
- acp.builder 配下の互換 import 経路、builder adapter、正本 builder への委譲先を確認・変更するとき
- oracle・realization・session・TUI・indexing の builder 関連実装の配置を判断するとき

## Do not read this when
- builder の canonical な正本実装や CLI 本体の挙動を直接確認したいとき
- builder と無関係な ACP 処理や、個別機能の詳細実装を調査するとき

## hash
- ba4cd7c106d8cc3e084ee85ced6ae6837cb95edbfaa1c0ef3510c52a743bef57
