# `file_access_rule_vaolation_recovery.py`

## Summary
- ファイルアクセス規則違反が発生した agent call をリカバリーするための AI エージェント呼び出しパラメータを構築する oracle src。違反時のアクセス規則、違反ファイル一覧、発生ログを動的プロンプトへ埋め込み、リカバリー担当 agent に渡す完全プロンプトと実行条件を定義する。

## Read this when
- ファイルアクセス規則違反のリカバリー用 agent call がどの role・summary・goal・補助プロンプトで起動されるかを確認したいとき。
- 違反したファイル一覧、違反時のファイルアクセスモード、発生ログのタイムスタンプがプロンプトへどう渡されるかを確認したいとき。
- ファイルアクセス規則違反リカバリーの AgentCallParameter、モデル種別、reasoning effort、file access mode の正本仕様断片を確認したいとき。

## Do not read this when
- 通常の agent call パラメータ全般、モデル種別、reasoning effort、file access mode の型定義を確認したいだけのとき。
- ファイルアクセス規則そのものの文章生成や各アクセスモードの具体的な規則を確認したいとき。
- 完全プロンプトの共通組み立て処理や markdown rendering の仕様を確認したいとき。

## hash
- 77808a6704659eb65d9f68bbeb85494648b62786f3a8e77eef1568a254b6edc7
