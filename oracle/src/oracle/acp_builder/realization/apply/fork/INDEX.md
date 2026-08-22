# `launch_exec.py`

## Summary
- `cmoc realization apply fork` の差分追従処理を起動する AgentCallParameter の構築定義。commit 範囲と oracle file の raw diff を prompt に組み込み、リポジトリ全体の realization file への反映、整合性確認、実装・テスト・補助成果物の検証を委譲する。realization の起動 prompt や実行パラメータを確認・変更するときの入口であり、同処理の具体的な実装やテストを直接確認する対象ではない。

## Read this when
- `cmoc realization apply fork` の差分追従 agent call がどのような prompt と起動設定で構築されるか確認するとき
- oracle file の変更を realization file 全体へ反映する追従フローの委譲範囲、作業ディレクトリ、アクセスモード、品質設定を確認するとき

## Do not read this when
- 差分追従 agent call の具体的な実装、テスト、補助成果物を調査するとき
- `cmoc realization apply fork` 以外の agent call 構築や、通常の realization 実装そのものを確認するとき

## hash
- baba1f74162e053746b72a01eea6bff32bb2ced618a98342e5a69ede86a5a866
