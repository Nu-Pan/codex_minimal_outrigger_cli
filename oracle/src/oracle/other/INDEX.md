# `cmoc_config.py`

## Summary
- cmoc のリポジトリ固有設定を表す frozen dataclass 群を定義する oracle source。並列数、Codex CLI のモデル・推論設定、managed Ollama 起動方針、oracle review のループ上限を扱い、設定の既定値と JSON 永続化に関する設計意図を確認する入口となる。

## Read this when
- cmoc の設定項目、既定値、Codex CLI 用モデル指定、推論 effort、managed Ollama 起動方針を変更・調査するとき。
- cmoc oracle review の列挙・マージ・検証ループ上限を変更・調査するとき。
- CmocConfig とそのネストした設定 dataclass の構造や Enum の設定値変換を確認するとき。

## Do not read this when
- CLI コマンドの具体的な実装や入出力処理だけを調査するとき。
- Codex CLI や Ollama 自体の一般的な利用方法を調査するとき。
- oracle review の所見生成・統合・検証ロジックそのものを調査するときは、該当する実装・仕様を直接読む。

## hash
- 106156981624f685daad073178e44421fee18594b8cb9d417ea3112f4308d895

# `path_model.py`

## Summary
- cmoc のルートパスプレースホルダを実パスへ解決・逆変換するモデルと補助関数を定義する。`{{cmoc-root}}`、`{{repo-root}}`、`{{run-root}}`、`{{work-root}}` の探索規則や、プレースホルダ付きパスの検証を扱うパス処理の入口。

## Read this when
- ルートパスプレースホルダの追加・変更や、プレースホルダと実パスの変換仕様を確認するとき
- cmoc・repo・run・work の各ルート探索、git 状態に基づくルート解決を調査するとき
- パス表記の検証や、相対パスにプレースホルダを要求する挙動を変更・確認するとき

## Do not read this when
- 特定の CLI 機能の処理だけを調査し、ルートパス解決やプレースホルダ変換に関係しないとき
- 既存のプレースホルダ定義を利用するだけで、探索規則やパスモデル自体を変更しないとき

## hash
- 7e21eb8ee080188e53233c61ea05477d2fffc3c76d2b63195d87537d72aaea42

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
