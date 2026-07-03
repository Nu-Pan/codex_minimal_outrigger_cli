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
- review oracle finding 周辺の agent call parameter builder と、旧 import 経路を維持する互換層を扱う realization 側の領域。
- 正本側 builder の結果を最小補正して使う実装と、既存 caller の移行完了まで canonical 実装を再公開する shim が混在する。
- 実処理本体や正本仕様ではなく、realization 側で必要な一時補正・互換 import・削除条件を確認する入口になる。

## Read this when
- review oracle finding の merge や validation advocate の agent call parameter 生成を確認・変更したい。
- 正本側 builder 出力を realization 側でどう補正しているか、また補正を削除できる条件を確認したい。
- review finding enumeration、judgment、challenger validation について、旧 import 経路から canonical 実装へ委譲する互換層を調べたい。
- 既存 caller の移行状況に応じて、互換 module を削除できるか判断したい。

## Do not read this when
- review oracle の正本仕様、prompt の本来の文面、判定仕様、検証ロジックそのものを確認したい場合は、対応する oracle file または canonical 実装を読む。
- AgentCallParameter の基礎構造、model、reasoning effort、file access mode などの共通定義を確認したい場合は、基礎定義側を読む。
- review oracle finding 以外の builder や review 処理を調べたい場合は、それぞれの対象へ進む。
- 互換 import 経路や一時的な prompt 補正に関係しない、新しい公開 API や新規実装責務を探している場合。

## hash
- 68b7ecc937832c441d760ea14b0822e9de37756fa25c4bc2442b875578749f30
