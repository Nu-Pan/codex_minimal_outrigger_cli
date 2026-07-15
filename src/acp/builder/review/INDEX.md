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
- `acp.builder.review.oracle` の互換 import 群をまとめる入口。旧 import 経路を維持するだけの包みか、正本 oracle 実装へ進むべきかを見分けるときに使う。

## Read this when
- 旧来の `acp.builder.review.oracle.*` import をまだ使っている呼び出し元の整理や削除可否を確認したいとき。
- 互換層を残す理由や、どの条件で削除できるかを確認したいとき。
- 正本 oracle 実装へ進む前に、この package で維持している互換の範囲だけを確認したいとき。

## Do not read this when
- 新しい review oracle の実装仕様や生成ロジックを確認したいときは、対応する `oracle/src` 側を読む。
- 互換 import 経路ではなく、review oracle 本体の挙動や入力仕様を追いたいとき。

## hash
- a73562e940351b2377912d69014bd9d9c305f33eacaf5c5ec4f0ea0eaa5c4f0f
