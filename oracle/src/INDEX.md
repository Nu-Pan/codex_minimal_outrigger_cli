# `oracle`

## Summary
- `oracle/src/oracle` 配下の正本仕様断片を束ねる入口。ACP builder の共通部品、cmoc の共通基盤、prompt 組み立て部品のどれを読むべきかを、扱いたい概念から切り分けるために使う。

## Read this when
- oracle src 全体の中で、まずどの共通基盤を読むべきかを絞り込みたいとき。
- ACP builder の共有状態・共通ルール・結果表現、cmoc の設定やパス解決や構造化文書、prompt 組み立てのどれかにまたがる仕様を確認したいとき。
- 個別の機能ファイルに入る前に、共有概念の責務境界を確認したいとき。

## Do not read this when
- 特定機能の個別仕様だけを確認したいときは、対応する下位エントリーを直接読む。
- realization code の実装詳細やテスト構成を確認したいときは、この配下ではなく実装側を読む。
- oracle src の共通基盤ではなく、別系統の正本仕様断片を探しているとき。

## hash
- fa8bbed139c27bfe019d5d374bced727f3234b3f984221ab7a646f46374f7f08
