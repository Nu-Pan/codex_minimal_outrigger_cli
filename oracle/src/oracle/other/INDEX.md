# `cmoc_config.py`

## Summary
- cmoc のリポジトリ固有設定を集約するデータクラス群。並列数、Codex のモデル・provider・reasoning 設定、oracle review の各ループ上限を扱い、JSON/TOML 設定値や永続化対象の構造を定義する。

## Read this when
- CmocConfig の項目、デフォルト値、Codex CLI 向け設定、oracle review のループ回数を変更・参照するとき
- 設定の JSON シリアライズ対象や model provider 設定の型を確認するとき

## Do not read this when
- CLI コマンドの実行フローや設定ファイルの生成・同期処理を調べるとき
- ModelClass や ReasoningEffort 自体の定義・意味を調べるときは、直接その定義元を読む

## hash
- e7003c50485257f7fa16a0acaaf5ce70905c423e51d5a4c28ab9ab99113bc4eb

# `path_model.py`

## Summary
- ルートパスのプレースホルダ表記と実パスの相互変換、および cmoc・repo・run・work 各ルートの探索を定義するパスモデル。パス解決やルート判定に関する oracle 実装の入口。

## Read this when
- パスプレースホルダを実際の絶対パスへ解決する処理を確認・変更するとき
- cmoc、repo、run、work の各ルート探索条件や相互変換を確認するとき
- パス表記の検証規則や git worktree 構成への対応を調べるとき

## Do not read this when
- 特定の CLI 機能の実装や出力形式だけを確認したいとき
- INDEX.md のルーティング規則自体を確認したいとき
- パス解決を利用する側の個別機能だけを調べ、ルート探索の仕様に触れないとき

## hash
- a05616c36333cdccc95f284834f4260a7a3613dd30a7c4d886d81c54f3c4f3b3

# `standard.py`

## Summary
- 規範（Standard）とその要求（Requirement）のデータ構造、および Standard を StructDoc に変換する処理を定義する。oracle standard などの規範文書を構造化文書へ変換する実装の入口。

## Read this when
- Standard や Requirement のフィールド検証・公開プロパティを変更するとき
- 規範オブジェクトを StructDoc へ変換する処理を確認・変更するとき
- oracle standard の構造化表現に関わる実装を調査するとき

## Do not read this when
- 個別の規範本文や文書の内容を確認したいとき
- StructDoc 自体の仕様や実装だけを調査するとき
- oracle standard と無関係な CLI や realization 実装を変更するとき

## hash
- a030f66eb8db892df78b4e0246d71fcfb3a99d49a56a37ddd8ea96705340bf2f

# `struct_doc.py`

## Summary
- 階層構造を持つ文章を Markdown にレンダリングするクラスと補助関数を定義する。見出し深度、cmoc_block 参照の検証、コードブロック、空行、インデント正規化を扱う。

## Read this when
- 構造化文章の生成・編集・Markdown レンダリングを変更するとき
- StructDoc、StructBlock、StructCodeBlock のデータ構造や cmoc_ref 検証を確認するとき
- Markdown 出力の見出し深度、空行、コードブロック、インデント処理を確認するとき

## Do not read this when
- この構造化文章レンダラーの挙動やデータ構造に関係しない処理を変更・調査するとき
- 単に他の oracle 文書や実装の仕様を確認したいだけで、Markdown レンダリング処理を通らないとき

## hash
- a920e827d70debca2724d15ef4c6b998c684a458b2d73d79f8ec8cd9ebeb4b98
