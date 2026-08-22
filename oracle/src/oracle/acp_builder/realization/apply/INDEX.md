# `fork`

## Summary
- `cmoc realization apply fork` における差分追従 agent call の起動パラメータを構築する関数を収録する。commit 範囲と oracle file の raw git diff を動的 prompt に組み込み、リポジトリ全体の realization file への反映と整合性・実装・テスト・補助成果物の確認を委譲する。
- 差分追従用の prompt、ファイルアクセスモード、作業ディレクトリ、モデル・推論設定、indexing preflight などの起動条件を確認・変更する際の入口である。

## Read this when
- `cmoc realization apply fork` の差分追従 agent call に渡す commit 範囲、oracle file の raw diff、作業ディレクトリ、アクセスモード、品質設定を確認するとき
- oracle file の変更を realization file 全体へ反映する agent call の prompt と完了条件を確認・変更するとき

## Do not read this when
- 差分追従 agent call の具体的な realization 実装、テスト、補助成果物の内容を調査するとき
- `cmoc realization apply fork` 以外の agent call 構築や、通常の realization 実装そのものを確認するとき

## hash
- f036f9ef4b7df97aec26a7a89b2196e74ee84d878480e596dea58d4a3dbdb1f8
