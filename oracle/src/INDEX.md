# `oracle`

## Summary
- 参照可能な正本ソース本文の有無を確認するための入口。配下の具体的な実装内容を扱わない。
- リポジトリ設定、パスモデル、規範モデル、構造化文書レンダラーを担う Python ソース群。設定、永続化構造、root 解決、規範構造化、Markdown 出力の調査・変更時の入口。
- oracle・realization、適合性レビュー、ファイルアクセス、INDEX.md ルーティングなどの規範を prompt builder 用の構造化文書へ変換する実装群。レビュー規範、アクセス制約、仕様分類、ルーティング規則の生成処理を扱う。

## Read this when
- このディレクトリの内容や、参照可能な正本ソースの有無を確認するとき。
- 設定、パス解決、規範モデル、構造化文書の変換・Markdown レンダリングを調査・変更するとき。
- oracle・realization の規範、適合性レビュー、ファイルアクセス規則、INDEX.md ルーティング規則、prompt builder 用文書生成を調査・変更するとき。

## Do not read this when
- 実装仕様や処理内容を確認したいときは、配下の具体的な実装を直接読む。
- CLI の実行フロー、設定ファイルの生成・同期、agent call prompt 生成などの利用側処理だけを調査するとき。
- 特定の oracle 文書や realization 実装そのものの仕様・挙動だけを調査するとき。
- Codex CLI の実行権限や sandbox 設定そのものを確認するとき。

## hash
- fcee0b428f4bd724e7fe24c67ac3817b73a5379cbb4a7c83c0e4218ae7cc1ffc
