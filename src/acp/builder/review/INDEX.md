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
- review/oracle builder の互換 import 経路と、canonical builder への委譲・限定的な prompt typo 補正を扱うディレクトリ。review finding の enumeration、judgment、merge、advocate、challenger validation に関する各入口を確認するためのルーティング先。

## Read this when
- review/oracle builder の旧 import 経路、canonical 実装への移行、削除条件を確認するとき
- review finding の AgentCallParameter 生成や、oracle root placeholder の既知 typo 補正を調査・変更するとき
- 絶対 symlink の oracle path、dynamic input の保持、prompt の限定的な補正挙動を確認するとき

## Do not read this when
- canonical oracle builder の本体仕様や prompt 本文だけを確認したいとき
- review routing、finding 検証ロジック、その他の新しい実装責務を調査するとき
- 旧 import 経路や prompt 補正と無関係な一般的な AgentCallParameter 処理を扱うとき

## hash
- 6d40679bba0a21f795e69479ffbfcbef367fc6e23eaf9f9902335c614aede8b4
