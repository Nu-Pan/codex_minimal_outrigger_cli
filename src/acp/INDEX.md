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
- ACP builder の realization package。canonical な oracle builder を互換入口や command 別 adapter として公開し、既存の `acp.builder.*` 参照を維持する。
- 動的 prompt section の Markdown code fence 補正、対象本文・差分・review finding の埋め込み、TUI 起動や quota probe の parameter 生成を扱う。
- 下位要素は、共通 fence 処理、indexing・feedback・session・TUI・quota probe、oracle command、realization apply/refactor の builder adapter に分かれる。

## Read this when
- ACP builder の realization 側における canonical builder への委譲、互換 import 経路、公開入口を調査・変更するとき。
- 動的な対象本文・差分・review finding を prompt に埋め込む際の code fence 保護を調査・変更するとき。
- oracle edit・investigation・review、realization apply・refactor、indexing・feedback、session join、TUI 起動、quota availability probe の builder adapter の入口を選ぶとき。

## Do not read this when
- canonical な oracle builder の仕様や prompt 本文を調査・変更するときは、対応する oracle 側の対象を直接読む。
- ACP builder の利用箇所や利用者向け公開面を調査するときは、各参照元を直接読む。
- 通常の CLI 処理、ACP 実行処理、または個別 adapter の詳細実装だけを調べるときは、該当する下位要素へ直接進む。

## hash
- a0f56b33ae8080c94d114d00f17692ff5919622d92c1a328634e69e606cab109
