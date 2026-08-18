# `fork`

## Summary
- `cmoc realization apply fork` における差分追従 Agent Call の起動パラメータを構築する実装群への入口。追従対象の commit 範囲や oracle file の raw git diff を prompt に埋め込む処理、モデル・推論・ファイルアクセス設定、完了条件と参照方針を確認・変更するときに読む。

## Read this when
- `cmoc realization apply fork` が生成する prompt の文面や、追従対象変更の渡し方を確認・変更するとき。
- Agent Call の起動時設定、差分追従処理の完了条件、oracle/realization の参照方針、リポジトリ全体を対象とする routing 設定を確認するとき。

## Do not read this when
- realization の具体的な実装・テスト・補助ファイルを確認または変更するときは、対象ファイルを直接読む。
- 一般的な prompt 構築、共通の AgentCall 型・パス型、構造化文書の仕様を確認するときは、各共通モジュールを直接読む。

## hash
- d34550787a8d0e8e0f69dcb04b27f6fb337235baa8f8e3de2f5f93170ecbde9f
