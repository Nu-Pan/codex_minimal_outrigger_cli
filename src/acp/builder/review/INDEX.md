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
- review/oracle builder の互換 import 経路と、canonical builder に委譲する realization 実装をまとめたディレクトリ。review finding の enumerate・judge・merge・advocate・challenger 向け parameter 生成、および既知の prompt placeholder typo 補正を扱う。各モジュールは旧 caller の移行入口または限定的な prompt 補正の確認先であり、canonical な仕様・実装は委譲先を直接読む。

## Read this when
- review/oracle builder の旧 import 経路、canonical 実装への移行状況、互換 package の削除可否を確認するとき
- review finding の parameter 生成や、既知の oracle-root placeholder typo 補正の挙動を確認・変更するとき
- prompt への入力保持や、canonical builder への委譲関係をレビューするとき

## Do not read this when
- canonical builder の prompt 仕様・本体実装・検証ロジックを確認したいとき
- review routing、一般的な AgentCallParameter 処理、またはこのディレクトリの対象外の review 処理を調査するとき
- 旧 import 経路や限定的な prompt 補正に関係しない新しい実装責務・公開 API を確認するとき

## hash
- 613ebe11f0eaefeabd8468d3077a9433529c66dd1ff56df0e586ddeeacfe9cd6
