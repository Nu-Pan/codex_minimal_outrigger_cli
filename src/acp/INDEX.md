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
- ACP builder の realization adapter と互換入口をまとめるディレクトリ。oracle、realization、session、indexing、tui などの command/package 別 builder adapter と、Markdown code fence 保護の共通処理を下位要素へ案内する。
- canonical な oracle 実装への委譲や既存 import 経路の互換維持を確認するための入口であり、各処理の具体的な実装は対応する下位 package・モジュールから調査する。

## Read this when
- ACP builder 全体の構成、command 別 adapter の配置、互換入口から正本実装への接続を切り分けるとき。
- apply・refactor・oracle・session・indexing・tui builder のいずれかを調査・変更する前に、進むべき下位要素を判断するとき。
- 動的 Markdown section の code fence 保護など、builder 共通処理の所在を確認するとき。

## Do not read this when
- canonical な oracle builder の仕様や実装そのものを確認するときは、oracle 側の対象を直接読む。
- 特定 builder の具体的な生成ロジックや処理本体を調査するときは、このディレクトリ入口ではなく該当する下位 package・モジュールを直接読む。
- ACP builder と無関係な CLI 実装、利用箇所、利用者向け公開面だけを調査するとき。

## hash
- c78c8a84393293da2770c4f551781dffcaeda386ffeb701b0956b3cce70b0f45
