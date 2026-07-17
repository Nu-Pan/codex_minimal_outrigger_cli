# `__init__.py`

## Summary
- `oracle.acp_builder.apply.fork` の正本 builder を realization 側から呼び出す package。ファイル単位レビュー・修正と変更要約の公開入口をまとめる。

## Read this when
- apply fork の realization 側 builder package の役割を確認するとき。
- 正本 builder への委譲入口を追加・削除するとき。

## Do not read this when
- apply fork のループ制御や state 遷移を調べたいとき。
- prompt や schema の正本仕様そのものを確認したいとき。

## hash
- 41c42a6aa5bded6005a7579fe2cd55249da6f57871e7ac83b67f41c8c65e24cc

# `_common.py`

## Summary
- apply fork ACP builder が共通利用する補助関数を提供する。repo root の解決、oracle 側ソースの import 可否確認と開発・パッケージ layout 対応、oracle が返す ACP parameter の realization 公開型としての受け渡しを扱う。

## Read this when
- apply fork の ACP builder を実装・修正するとき
- oracle builder の import 経路や repo root 解決を確認するとき
- oracle 側の ACP parameter を realization 側へ渡す処理を確認するとき

## Do not read this when
- apply fork 以外の ACP builder の具体的な処理を確認するとき
- ACP parameter や oracle builder の実装本体を直接確認したいとき

## hash
- 29e5f7a547c83fd6e23281a62a320c81a33bca76b7921ba6d9638a45821bf195

# `change_summary.py`

## Summary
- `cmoc apply fork` の変更要約用 agent call parameter を組み立てる入口。作業レポート向けの変更要約を作るときに読む。正本側の `oracle.acp_builder.apply.fork.change_summary` を参照して実体を委譲するため、ここでは委譲の流れだけを確認すればよい。

## Read this when
- `cmoc apply fork` の変更要約を作る処理の入出力や、どの正本実装に渡しているかを確認したいとき。

## Do not read this when
- `cmoc apply fork` の変更要約の正本仕様そのものを確認したいときは、対応する oracle 側を見る。変更要約以外の fork 系変換や共通処理を追いたいときも、まずはそれぞれの直接の入口を読む。

## hash
- 83474b219a58ee86b8aa07876c6e7e7ca83df70e821edef6a6e35e15cc907aa9

# `file_review_and_fix.py`

## Summary
- `cmoc apply fork` のファイル単位レビュー・修正用 parameter を正本 builder へ委譲する realization 入口。所見調査、修正、検証を一つの agent call で行う parameter を返す。

## Read this when
- ファイル単位レビュー・修正用 parameter の realization import 経路を確認するとき。
- packaged layout と開発 tree の双方から正本 builder を呼び出す委譲を変更するとき。

## Do not read this when
- レビュー・修正 prompt や schema の内容を確認したいときは、対応する oracle src を読む。
- apply ループの再投入・commit 制御を調べたいときは、サブコマンド実装を読む。

## hash
- 47d7279d95aafad8f2be16f343f89b5436eed9348b5d961719a0b79c1a0e264f
