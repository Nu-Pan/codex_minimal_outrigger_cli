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
- `oracle/src/oracle/acp_builder/review/oracle` にあるレビュー用 oracle 実装群の入口で、各モジュールの互換 import、正本 builder への委譲、静的 typo の最小補正を確認するための案内を置く。

## Read this when
- 旧 import 経路の互換維持や削除条件を確認したいとき。
- review oracle の finding 生成・判定・検証の入口や、symlink 由来の path 表記補正の有無を確認したいとき。
- 正本 builder からの委譲範囲と、realization 側で残す最小限の補正だけを確認したいとき。

## Do not read this when
- canonical な正本実装そのものを追いたいときは、対応する oracle src の実装を直接読む。
- この層ではなく、レビュー以外の builder や一般的な oracle file 定義を調べたいとき。
- 新規 caller の実装方針を決めたいだけで、旧 import 互換の有無が関係しないとき。

## hash
- 789aa9e6cb33ba04afa5eca48e511144cbf1a015362c90c8036fe9da7dd3ffc6
