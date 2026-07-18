# `cmoc_config.py`

## Summary
- cmoc のリポジトリ固有設定を集約する dataclass 群。並列実行数、Codex CLI のモデル・推論強度・復旧試行回数、oracle review の各ループ上限を定義し、JSON 永続化される設定構造の入口となる。

## Read this when
- cmoc の設定項目、既定値、Codex CLI 向けモデル対応、oracle review のループ回数を変更または確認するとき。
- CmocConfig の JSON 化対象や設定 dataclass の構造を調べるとき。

## Do not read this when
- 実際の設定ファイル生成・同期や人間による設定調整の手順を確認したいときは、指定された JSON 設定ファイルと doctor 関連実装を直接読む。
- ModelClass や ReasoningEffort 自体の定義・意味を確認したいときは、それらを定義するモジュールを直接読む。
- Codex CLI の呼び出し処理や oracle review の実行ロジックを調べるときは、各処理の実装モジュールを直接読む。

## hash
- 122c507614e38cc44ad2d5866223d25b53966296f1adc3cb96aec754d9cee519

# `path_model.py`

## Summary
- パス表記のルールと、`{{cmoc-root}}`・`{{repo-root}}`・`{{run-root}}`・`{{work-root}}` の各プレースホルダを実パスへ解決する機能を定義する。プレースホルダ表記への逆変換、git とディレクトリ探索による各ルートの特定も扱う。

## Read this when
- パスのプレースホルダ表記、実パス解決、worktree やリポジトリルートの特定処理を変更・調査するとき。
- `resolve_real_path`、各 `resolve_*_root` 関数、または実パスとプレースホルダの相互変換の挙動を確認するとき。

## Do not read this when
- 特定の CLI 機能やパス操作の実装を調査しており、プレースホルダ解決やルート探索の挙動に関係しないとき。
- 対象機能の責務が別の oracle src または oracle doc に直接定義されているとき。

## hash
- 2b5999ec6bd2c7cae52565994d96eb2348be7e3f788632a76944d8e883838f88

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
