# `__init__.py`

## Summary
- 既存の review builder 系 import 互換性を保つためだけに残された package 初期化部分。現行実装や公開面から互換 import が消えた時点で削除候補になる境界を示す。

## Read this when
- review builder 周辺の import 互換性を確認する。
- 古い acp.builder.review 系参照を削除できるか判断する。
- 互換 package の残存理由や削除条件を確認する。

## Do not read this when
- review builder の実処理や変換ロジックを調べたい。
- 新しい公開 API や利用者向け機能の仕様を確認したい。
- 互換 import と無関係な builder 実装を変更する。

## hash
- 20e0879d03952a8b860e9d09a0f9c7e08c05699e96390ec504f3e0481a897ebb

# `oracle`

## Summary
- レビュー用 oracle builder の互換 import 経路を集約するディレクトリ。finding の列挙・判定・マージ・擁護・反証用パラメータ生成を扱い、canonical な oracle 実装への橋渡しや、必要な最小補正を担う。各ファイルの互換性維持・移行・削除可否を確認する入口。

## Read this when
- レビュー finding の互換 import 経路、canonical 実装への委譲、呼び出し元の移行状況を調査するとき。
- review oracle の prompt やパラメータ生成で、互換層が加える補正とその削除条件を確認するとき。
- 旧来の import 経路を維持する必要性や、互換 package・shim を削除できるか判断するとき。

## Do not read this when
- canonical なレビュー finding 列挙・判定・検証処理の仕様や実装詳細だけを確認したいとき。
- 互換経路と無関係な builder、oracle path 処理、または別サブコマンドのパラメータ生成を調べるとき。
- 新しいレビュー機能の仕様を確認したいとき。

## hash
- a73562e940351b2377912d69014bd9d9c305f33eacaf5c5ec4f0ea0eaa5c4f0f
