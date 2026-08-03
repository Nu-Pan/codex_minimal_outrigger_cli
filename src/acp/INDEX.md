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
- ACP builder の realization パッケージ群をまとめる入口。oracle 実装への互換 adapter、prompt の共通処理、oracle・realization・session・TUI・indexing などの command-specific builder 接続を扱い、各下位要素へ進むための起点となる。

## Read this when
- acp.builder 配下の builder adapter 構成や、既存 import 経路から canonical 実装へ接続する仕組みを調査するとき
- oracle・realization・session・TUI・indexing の builder 接続先を特定するとき
- 動的 Markdown section の code fence 補正など、builder 共通処理の入口を確認するとき

## Do not read this when
- canonical な oracle 実装や正本仕様そのものを確認・変更するときは、oracle 側の対応対象を直接読む
- 個別 builder の具体的な生成ロジックや利用箇所を調査するときは、該当する下位パッケージまたは参照元を直接読む
- ACP builder と無関係な CLI、TUI、共通パス処理の実装を調査するとき

## hash
- ff4635a2e1ed805ca131816afcb1db8daa68cdc491fcb20d9b240d7eb0652780
