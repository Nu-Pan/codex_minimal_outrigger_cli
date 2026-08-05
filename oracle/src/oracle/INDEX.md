# `acp_builder`

## Summary
- oracle の agent call パラメータ構築に関する正本実装を用途別にまとめたディレクトリです。共通の呼び出しパラメータ型、INDEX.md 生成、oracle 関連、realization 関連、session join、TUI 起動の各実装への入口を提供します。

## Read this when
- AgentCallParameter の型やモデル・推論強度・アクセスモードを確認するとき。
- INDEX.md エントリー生成のスキーマや構築処理を調査するとき。
- oracle、realization、session join、TUI など特定用途の agent call パラメータ構築を変更・調査するとき。

## Do not read this when
- 実際の処理本体、差分適用、競合解消、git 操作を調査するとき。
- 共通 prompt 構築やパスコンテキストなど、各用途の下位実装より共通領域を直接確認すべきとき。
- 個別の構造化出力フィールド定義だけを確認するとき。

## hash
- 2a571ac6da46c0f867122d11910d7f72f3de07fb3e0e1f7ea3e97ffe585a2479

# `other`

## Summary
- リポジトリ設定、パスモデル、規範モデル、構造化文書レンダラーを担う Python ソース群。設定値や永続化構造、root 解決、規範の構造化、Markdown 出力を調査・変更する際の入口となる。

## Read this when
- CmocConfig や Codex 設定、oracle review の上限、JSON/TOML シリアライズを確認するとき
- agent call の cwd・work/repository/run root、root placeholder、パス変換や検証を確認するとき
- Standard・Requirement の構造や StructDoc への変換を確認するとき
- StructDoc の階層、Markdown レンダリング、cmoc_ref 検証、コードブロックや空行処理を確認するとき

## Do not read this when
- CLI の実行フロー、設定ファイルの生成・同期、agent call prompt 生成などの利用側処理だけを調査するとき
- ModelClass、ReasoningEffort、StructDoc 自体など、別ファイルに定義された概念の詳細だけを確認するとき
- 個別の規範本文や、Markdown レンダリングを通らない他の oracle 文書の仕様だけを確認するとき

## hash
- 01ecbe8fd695e08e7b934d3c8c596ce87ab0fd7d09615d8dc1fb9728229c4da7

# `prompt_builder`

## Summary
- oracle と realization、適合性レビュー、ファイルアクセス、INDEX.md ルーティングなどの規範を、prompt builder 用の構造化文書へ変換する実装群を収録するディレクトリ。特定のレビュー規範やアクセス制約、仕様分類、ルーティング規則の生成処理への入口となる。

## Read this when
- oracle file と realization file の適合性、レビュー所見、conflict 解消規範を調査・変更するとき。
- AI エージェント向けのファイルアクセス規則や oracle・realization の定義を変更するとき。
- INDEX.md のエントリー規範やルーティング規則の生成処理を調査・変更するとき。
- prompt builder に注入する標準文書の構造、Requirement・Standard の扱い、oracle 参照ルールを確認するとき。

## Do not read this when
- 特定の oracle 文書や realization 実装そのものの仕様・挙動を調査するとき。
- Codex CLI の実行権限や sandbox 設定そのものを確認するとき。
- prompt builder 以外のサブコマンド処理や、一般的なコード品質・ベストプラクティスだけをレビューするとき。

## hash
- dcb504c92f81d240b75e76c3ff2b11d6e83ee502510f7e4236ae8a6b09d48879
