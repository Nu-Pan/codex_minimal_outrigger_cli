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
- ACP builder の realization adapter と互換入口をまとめるパッケージ。oracle 実装への接続、各 workload・command 向けの parameter/prompt builder、旧来の `acp.builder.*` import 経路を扱う下位要素への入口を提供する。

## Read this when
- ACP builder の全体構成や、各 command・workload・TUI・session 向け adapter の入口を確認するとき。
- `acp.builder.*` の互換 import、canonical な oracle builder への接続、builder 共通の prompt/fence 処理を調査するとき。
- quota probe や review builder に関する realization 側の入口・実行時補助を確認するとき。

## Do not read this when
- canonical な builder の正本仕様や実装そのものを確認・変更するときは、対応する oracle 側の対象を直接読む。
- CLI・TUI・session などの利用側の挙動や公開面を調査するときは、各利用元を直接読む。
- builder と無関係な prompt 処理、パス解決、コマンド本体の実装を調査するとき。

## hash
- 512abfa278a6763d6aea7d39cc348830f50b8874e0ecec7fe480e6aaac5f1517
