# `oracle`

## Summary
- oracle/src/oracle は、cmoc の AI エージェント呼び出しを支えるモデル、設定、パス解決、構造化文書、プロンプト構築、および用途別の起動定義をまとめる実装領域です。
- AgentCallParameter などの共通呼び出し契約や quota probe は acp_builder、設定・パス・Markdown 構造化ヘルパーは other、完全 prompt と各種 policy は prompt_builder から確認できます。
- oracle、realization、feedback、indexing、session、TUI などの用途別処理を調査するときの上位入口であり、具体的な仕様・実装・テストは各下位ディレクトリへ進みます。

## Read this when
- AI エージェント呼び出し全体の構成、共通パラメータ、プロンプト、設定、パスコンテキストの関係を確認するとき
- acp_builder、other、prompt_builder、または用途別 agent call 定義の適切な参照先を判断するとき
- 複数の oracle 実装領域にまたがる呼び出し契約や prompt 構築経路を調査・変更するとき

## Do not read this when
- 特定の agent call の詳細な起動パラメータや用途別処理だけを確認したい場合は、対応する下位ディレクトリを直接読むとき
- Codex CLI のバックエンド固有のモデル解決や、oracle・realization の正本仕様・具体的な実装だけを確認したいとき
- 共通 prompt の個別 policy、設定・パス・構造化文書ヘルパーの詳細だけを調べるときは、それぞれの直接の実装ファイルへ進むとき

## hash
- 5047ab54030f1e203441e398ffeb1836a656e8782099d54e76fde887302ba1e2
