# `oracle`

## Summary
- oracle/src/oracle 配下の正本ソース群へのルーティング入口。空の acp_builder、設定・パス・構造化文書を扱う other、エージェントプロンプト構成を扱う prompt_builder に分かれる。

## Read this when
- oracle の正本ソースから、設定・パス解決・構造化文書や Markdown レンダリングの実装を確認するとき。
- エージェントプロンプトの構成、プレースホルダ、oracle・realization 規則、ファイルアクセスやルーティング規則を確認するとき。
- 正本ソースが存在するディレクトリと、存在しないディレクトリを見分ける必要があるとき。

## Do not read this when
- CLI の実行フローや設定ファイルの生成・同期処理だけを調べるとき。
- 個別のプロンプト部品、ModelClass、ReasoningEffort、StructDoc の定義元を直接確認したいとき。
- 個別の規範本文や、Markdown レンダリングを経由しない機能の仕様を確認するとき。

## hash
- c9734bfddaabfa37a5f10cf1aad83bf50edf01205ff3e411efd6ae39435f36e2
