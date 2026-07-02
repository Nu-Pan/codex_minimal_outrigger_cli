# `file_access_rule_vaolation_recovery.py`

## Summary
- ファイルアクセス規則違反が発生した agent call をリカバリーするための AI エージェント呼び出しパラメータを構築する oracle src。違反時の規則本文、違反ファイル一覧、対象ログの時刻情報をプロンプトへ埋め込み、修復担当 agent に渡す入力を定義している。

## Read this when
- ファイルアクセス規則違反のリカバリー用 agent call parameter の内容、モデル種別、推論強度、アクセスモードを確認・変更したいとき。
- 違反ファイル一覧や違反したファイルアクセス規則を、リカバリー担当 agent のプロンプトへどう渡すか確認したいとき。
- `build_file_access_rule`、`build_complete_prompt`、`AgentCallParameter` を組み合わせた違反復旧用プロンプト生成の正本仕様断片を確認したいとき。

## Do not read this when
- 通常の agent call parameter 全般、モデル種別、推論強度、ファイルアクセスモードの型定義を確認したいだけのとき。
- ファイルアクセス規則そのものの本文生成や、各アクセスモードの規則内容を確認したいとき。
- 完成プロンプトの汎用的な組み立て規則や placeholder 展開の全体仕様を確認したいとき。

## hash
- 4dce6d56f411c97e097aa661604e08a4d60d36403cbad7d436262aafbf1e4506
