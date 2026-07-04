# `oracle`

## Summary
- AI エージェント呼び出しパラメータ、プロンプト構築、設定・パス・文書モデルなど、oracle src 内の基礎的な正本仕様断片をまとめる領域。
- agent call の入力契約・出力契約と共通規範プロンプト、cmoc の横断的な設定・パス・構造化文書 helper への入口になる。

## Read this when
- cmoc が AI agent call をどの prompt、Structured Output schema、モデル設定、ファイルアクセス権限、preflight 設定で組み立てるか確認したいとき。
- agent call 用の完全プロンプトが、役割・概要・ゴール・標準文書・読み書き規則・プレースホルダ定義などからどう構築されるか確認したいとき。
- oracle standard、realization standard、review standard、apply review standard、index entry standard など、AI に注入する共通規範プロンプトの生成元を探すとき。
- cmoc のリポジトリ別設定、モデル指定、実行予算、設定 JSON 保存方針、管理対象 Ollama に関する正本仕様断片を探すとき。
- パスプレースホルダ、ルート探索、実パス変換、構造化 Markdown レンダリング helper など、複数領域から参照される基礎概念を確認したいとき。

## Do not read this when
- CLI サブコマンド固有の利用者向け入出力、実行フロー、状態ファイル仕様、branch 操作、diff 取得、merge 実行などを調べたいとき。
- バックエンド API へ送る実リクエスト形式、具体的なモデル名解決、agent CLI 実行処理など realization src 側の実装詳細を調べたいとき。
- 個別の規範本文や生成済み Markdown 文書の意味だけを読みたいとき。
- oracle file、realization file、INDEX.md などの管理方針そのものだけを確認したいとき。
- 実装ファイルやテストファイルの現在構造を把握して直接修正したいだけで、agent call parameter、prompt 生成、設定・パス・文書モデルに関係しないとき。

## hash
- 443beddd7fe32ab31686b14e45d26f238265bb70770bf7dc3defd3f078dae18d
