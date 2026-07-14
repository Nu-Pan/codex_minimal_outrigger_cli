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
- `acp.builder.review.oracle` の互換層と正本 oracle への橋渡しをまとめた領域。旧 import 経路を維持する薄い shim と、review finding の生成・判定・擁護・反証に関する入口を分けて読む。

## Read this when
- 旧い import 経路の互換維持条件や削除可否を確認したいとき。
- review oracle の所見生成、判定、擁護、反証のどの入口に進むべきかを切り分けたいとき。
- symlink 経由の path 表示や、既知の互換修正がどこで入るかを確認したいとき。

## Do not read this when
- 新しい review 機能全体の設計や、oracle 以外の builder 群を探したいとき。
- 互換 shim ではなく、正本の review oracle 本体だけを直接追いたいとき。
- この配下のどの薄い入口でもなく、実装本体の詳細ロジックを確認したいとき。

## hash
- 4bbc0b556f3dca37ae6d63ef5e75a17e9a6a5990ab2e8c941306b9ac27ce3917
