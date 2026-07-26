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
- ACP builder の realization adapter と互換入口をまとめるディレクトリ。`acp.builder` の公開初期化、Markdown code fence 補正、indexing・oracle・realization・session・TUI 向け builder 接続、quota probe の互換 fallback を下位要素への入口として提供する。

## Read this when
- ACP builder の互換 import 経路、builder adapter の構成、または各 workload・TUI・session・quota probe への導線を調査するとき。
- prompt 内の Markdown code fence 保護や、canonical oracle builder と realization 側の接続箇所を特定するとき。

## Do not read this when
- canonical な oracle builder の仕様や実装そのものを確認・変更するときは、対応する oracle 側の対象を直接読む。
- TUI・CLI・apply・refactor などの処理本体や、builder の利用箇所を調査するときは、それぞれの実装・参照元を直接読む。
- レビュー実行時のキャッシュや、builder と無関係な一般的な Markdown 処理だけを調査するとき。

## hash
- aeec7fa0d0940604d242e577c8a19ec5ffeec63f6f56ac258c76878e371f5cb5
