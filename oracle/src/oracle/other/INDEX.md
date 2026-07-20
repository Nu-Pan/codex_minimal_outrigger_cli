# `cmoc_config.py`

## Summary
- cmoc のリポジトリ固有設定を表す dataclass 群を定義する oracle src。並列数、Codex CLI のモデル・provider・推論設定、oracle review のループ上限、および JSON/TOML 共通値の型を扱う。

## Read this when
- cmoc の設定項目、既定値、Codex CLI 向けモデル設定、provider-local 設定、oracle review のループ回数を変更・確認するとき
- 設定のシリアライズ対象となる型や Enum の扱いを確認するとき

## Do not read this when
- CLI の設定読み書き処理や doctor による生成・同期動作を確認したいとき
- モデル分類や推論 effort の Enum 定義そのものを確認したいとき

## hash
- 82b2b2d6a4f0ec05c05422a969c4d2e961f13844569bbb3fdbe811208fedcf88

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
- `Standard` と `Requirement` の定義、および `standard_to_struct_doc` を扱う。規範文書の見出し・背景・要求・判断例をどの形で保持し、`StructDoc` に落とすかを読む入口にする。

## Read this when
- 規範を表すデータ構造の必須項目や検証条件を確認したいとき。
- `Requirement` のラベル制約や、`examples` に何を書いてよいかの境界を確認したいとき。
- `Standard` を `StructDoc` に変換する際の章立てや、どのフィールドが出力に使われるかを確認したいとき。

## Do not read this when
- `oracle file` 全体の命名規則や配置方針を知りたいだけのときは、より上位の oracle 標準文書を読む。
- `StructDoc` 自体の仕様や実装詳細を知りたいだけのときは、このファイルではなく `StructDoc` の定義元を読む。
- この定義を使う個別の標準文書の内容を確認したいときは、各標準文書を直接読む。

## hash
- d19edf009065fcbd4a29ea2693bccd0f09a9860ab31fba30d25aaaa1f0108eaf

# `struct_doc.py`

## Summary
- 構造化された文書ツリーを Markdown に変換するヘルパー実装。見出し深度、入れ子文書、ブロック、コードブロック、文字列本文を扱い、cmoc_block 参照の検証や空行・インデントの正規化も提供する。

## Read this when
- 構造化文書の Markdown レンダリング処理を変更・調査するとき
- StructDoc、StructBlock、StructCodeBlock の構造や cmoc_ref 検証を確認するとき
- Markdown 出力の見出し深度、空行、コードブロック、インデント正規化を確認するとき

## Do not read this when
- CLI の実行経路やプロンプト生成全体を調査するとき
- このモジュールを利用する呼び出し側の仕様だけを確認するとき
- Markdown 以外の文書形式のレンダリングを調査するとき

## hash
- 672fa1d47b8aff4554c00a24c3cb667b8eaf9fa8f8d50253e0778486b84a822e
