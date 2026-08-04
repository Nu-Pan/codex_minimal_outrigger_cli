# `acp_builder`

## Summary
- AIエージェント呼び出しに関する正本ソースの配置領域。共通パラメータモデル、INDEX生成、oracle・realization・session・tui 各機能の起動パラメータ構築を扱う下位ファイルへの入口であり、`apply` は参照可能な正本ソースの有無を確認するための空の追加予定領域。

## Read this when
- AIエージェント呼び出し設定や各サブコマンドの起動パラメータ構築について、該当する下位実装の入口を選ぶとき。
- この領域に新しい正本ソースが追加されているか確認するとき。

## Do not read this when
- 個別機能の具体的な処理内容や実装詳細を確認したい場合は、該当する下位ファイルを直接読むとき。
- 共通仕様、prompt 構築規則、パス解決、agent call パラメータ型の定義だけを確認したいとき。
- 実際の INDEX.md ルーティング内容を判断したいとき。

## hash
- 9d95d3b381413af8377bb2e1f8602dfbf3883b336b20ef33aff55919e0c17e3f

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
