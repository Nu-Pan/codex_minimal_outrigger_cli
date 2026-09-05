# `oracle`

## Summary
- Codex CLI を用いる cmoc の正本実装領域で、agent call 構築、prompt 生成、パス解決、構造化文書処理、設定管理を扱う。
- quota probe、indexing、feedback、oracle、realization、session、TUI など、用途別の agent call builder への入口を提供する。
- agent call の共通パラメータ、ファイルアクセスモード、Structured Output schema、cwd、editor input handoff、indexing preflight の組み合わせを確認できる。

## Read this when
- cmoc の agent call 構築全体の責務分担や、共通パラメータから用途別 builder へ進む入口を確認するとき。
- prompt の組み立て、policy の集約、oracle・realization の扱い、INDEX.md routing の構成を調べるとき。
- agent call の作業ルート、placeholder、Git worktree の解決、または構造化文書の Markdown 化を確認するとき。
- quota probe、indexing、feedback、oracle、realization、session、TUI のいずれかの agent call builder を探すとき。

## Do not read this when
- 特定用途の prompt、出力契約、または起動パラメータの詳細だけを確認したいときは、該当する用途別 builder と schema を直接読む。
- editor input handoff や feedback reporter の入力契約だけを確認したいときは、それぞれの入力 schema を直接読む。
- agent call の実行処理や Codex CLI の実際の挙動、oracle・realization の意味仕様、feedback の保存・受付処理だけを調べるとき。

## hash
- d78a71d8b55497723663c7b32a82f28148ad9096f4a26646504d6c1e8602e131
