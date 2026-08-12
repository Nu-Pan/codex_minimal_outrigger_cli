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
- ACP builder の realization adapter と互換 import 入口を収めるディレクトリ。canonical な oracle builder への委譲、動的 prompt の code fence 保護、既存 import 経路の維持を担う。
- 下位には、共通 prompt 処理、feedback・indexing・session・TUI の互換入口、oracle command builder、realization apply/refactor adapter がある。個別 builder の実装責務へ進むための起点となる。

## Read this when
- ACP builder の adapter 構成、canonical oracle builder との接続、または既存 import 経路を調査・変更するとき。
- 動的 prompt の code fence 保護を含む builder 呼び出しの実装箇所を探すとき。
- oracle edit・investigation・review、realization apply・refactor など処理別の builder adapter へ進むとき。

## Do not read this when
- canonical な oracle builder の仕様や本体ロジックを確認・変更するときは、oracle 側の対象を直接読む。
- 個別 builder の具体的な prompt 内容や処理詳細を調査するときは、対応する下位ファイルを直接読む。
- builder の利用箇所や利用者向け公開面を調査するときは、各参照元を直接読む。

## hash
- 52487f2eb8feb63395bbe29d5e1dfd63ed4b1407f59f970e88ca2fdb9d5d5bc7
