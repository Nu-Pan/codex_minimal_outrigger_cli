# `doc`

## Summary
- `oracle/doc` 配下の個別仕様断片を束ねる入口。CLI の起動経路、補完、ログ、事前検証、エラー処理、外部 provider との境界、状態や実行分離など、利用者に見える機能仕様の断片を探すときにここから進む。

## Read this when
- アプリ全体の仕様断片を、どの文書へ進んで読むべきか判断したいとき。
- CLI の起動前処理、補完、ログ、エラー、状態、実行分離、外部 provider 境界のうち、個別の振る舞いを実装・修正・検証したいとき。

## Do not read this when
- oracle file と realization file の一般的な役割分担や編集規則だけを確認したいとき。
- 個別のサブコマンド仕様やデータ構造の細部だけを直接見たいときは、該当する下位文書へ進むほうが適切なとき。

## hash
- df61f8338e0c2d3a0cdb38bcd2ad71af2fd748daacbd48f0b2a06ed6423384f2

# `src`

## Summary
- `oracle/src` 配下の正本仕様断片を用途別に辿るための入口。`acp_builder`、`other`、`prompt_builder` などの下位領域へ進む前に、どの責務を読むべきかを絞り込む。

## Read this when
- `oracle/src` 配下のどの領域を読むべきか、まず入口を絞りたい。
- builder 間で共有する概念、型、出力契約、各サブコマンドの prompt や実行条件のどれを確認すべきか整理したい。
- agent call 用プロンプトの構成要素や、共通規範の注入位置を確認したい。
- 設定、パス表現、文書モデル、Markdown レンダリング補助の基礎を確認したい。

## Do not read this when
- 個別の実装詳細やテストの中身だけを確認したい。
- `oracle/src` 以外の仕様を探している。
- 既に読む対象の下位領域が特定できていて、この入口で再度絞り込みたくない。

## hash
- d5ad6722b357196bc8982fd41dc955016ded1cd1924d3d9e52e73222438ea9fc
