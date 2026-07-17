# `__init__.py`

## Summary
- `acp.builder.apply` 系の既存 import を保つための互換パッケージ。実処理は正本側の apply 実装へ進める入口として扱う。

## Read this when
- `acp.builder.apply` 配下の実装を探していて、既存の import 経路を壊さずに正本側の実装へ進みたいとき。

## Do not read this when
- 新しい apply 実装の正本を探したいときは、互換層ではなく `oracle/src/oracle/acp_builder/apply` 側を見る。
- この互換層の内部に実処理や仕様本体がある前提で読むべきではない。

## hash
- 484f419d6ff82058c68a8e19540e3837fc6e40e96b976026d61532af98ae9bfb

# `fork`

## Summary
- 対象ディレクトリは、apply fork 用の realization 側 ACP builder 入口と、その共通委譲処理・変更要約・ファイルレビュー／修正用 builder をまとめる。各ファイルは正本側 builder を呼び出し、realization 側で利用する parameter を公開する薄い境界層である。

## Read this when
- apply fork の builder package の責務や、realization 側から正本 builder へ委譲する入口を確認・変更するとき。
- repo root 解決、oracle builder の import、ACP parameter の受け渡しを確認するときは共通処理を読む。
- 変更要約の agent call parameter を確認するときは変更要約 builder を読む。
- ファイル単位のレビュー・修正・検証用 parameter の委譲経路を確認するときは file review and fix builder を読む。

## Do not read this when
- apply fork のループ制御や state 遷移を調べる場合は、対応するサブコマンド実装を直接読む。
- prompt、schema、変更要約、レビュー・修正の正本仕様を確認する場合は、対応する oracle 側の実装を直接読む。
- apply fork 以外の ACP builder の具体的な処理を確認する場合は、対象の builder package を直接読む。

## hash
- cc011deeb76dfdb4bf74083832c3c3ae0533bc3dd45d5aaab951d185b67bfedb
