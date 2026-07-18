# `oracle`

## Summary
- cmoc のサブコマンド別 ACP エージェント呼び出しパラメータを構築する oracle src の領域。apply fork、oracle、session、TUI、indexing などの prompt、Structured Output schema、モデル・推論・アクセス設定を扱う下位領域への入口。
- cmoc の設定モデル、パス解決、規範文書モデル、構造化文書の Markdown 変換を担う oracle src の領域。設定・パス・標準文書・Markdown レンダリングを確認する入口。
- プレースホルダ展開用の型、完全なプロンプトの組み立て、oracle・realization・INDEX.md・ファイルアクセス規則・レビュー基準などの標準ルール部品を扱う oracle src の領域。プロンプト生成に注入する共通要素を確認・変更する入口。

## Read this when
- サブコマンドがエージェントへ渡す AgentCallParameter、prompt、Structured Output schema、モデル・推論強度、ファイルアクセス設定を調査・変更するとき。
- cmoc 固有設定、Codex CLI の実行上限、ルートパスのプレースホルダ解決、規範文書のデータ構造、構造化文書の Markdown 出力を確認するとき。
- プレースホルダ展開、完全なプロンプトの構造、動的プロンプト、標準ルールの依存関係や注入内容を調査・変更するとき。

## Do not read this when
- ACP パラメータの共通型や既定値だけを確認するときは、共通定義を直接読む。
- agent call の実行本体、TUI 画面処理、差分適用、conflict 解消、設定 JSON の永続化や doctor 同期だけを調べるとき。
- 特定サブコマンドの実装・schema、個別標準文書、個別注入パーツ、プロンプト置換ロジックやファイル探索処理だけを確認するとき。

## hash
- 2f8eceb3cffcd7843012e61019d2fdfe16a351531cdd598adaa744052d4c5acd
