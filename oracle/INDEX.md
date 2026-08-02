# `doc`

## Summary
- cmoc の正本仕様ドキュメントをまとめるディレクトリ。アプリケーション共通仕様、branch・commit・worktree モデル、不採用案の検討記録、Python 開発規則を扱い、各仕様領域の入口となる。

## Read this when
- cmoc のアプリケーション挙動、branch・worktree lifecycle、開発規則、テストや環境構築の正本仕様を探すとき
- 特定の仕様領域に対応する文書やサブディレクトリを選ぶとき
- 採用しなかった設計案の背景や判断理由を確認するとき

## Do not read this when
- 確認対象の仕様文書やサブディレクトリがすでに特定されているとき
- 実装構造、具体的なテスト実行、一般的な開発作業だけを調査するとき

## hash
- f32417f2e650bee68a57635aa90f903273dc9c0856cfd21ed011134f1fafef04

# `src`

## Summary
- 参照可能な正本ソース本文の有無を確認するための入口。
- リポジトリ設定、パスモデル、規範モデル、構造化文書レンダラーを担う Python ソース群。
- oracle・realization、適合性レビュー、ファイルアクセス、INDEX.md ルーティングなどの規範を prompt builder 用の構造化文書へ変換する実装群。

## Read this when
- oracle/src 配下の正本ソースの有無や構成を確認するとき。
- 設定、パス解決、規範モデル、構造化文書の変換・Markdown レンダリングを調査・変更するとき。
- oracle・realization の規範、適合性レビュー、ファイルアクセス規則、INDEX.md ルーティング規則、prompt builder 用文書生成を調査・変更するとき。

## Do not read this when
- 実装仕様や処理内容を確認したいときは、oracle/src 配下の具体的な実装を直接読む。
- CLI の実行フロー、設定ファイルの生成・同期、agent call prompt 生成などの利用側処理だけを調査するとき。
- 特定の oracle 文書や realization 実装そのものの仕様・挙動だけを調査するとき。
- Codex CLI の実行権限や sandbox 設定そのものを確認するとき。

## hash
- 7a59440d630d046b7448c3e583446ba8782ba36bde058772de6e0371bf455e21
