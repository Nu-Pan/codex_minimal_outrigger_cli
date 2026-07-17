# `cmoc_config.py`

## Summary
- cmoc のリポジトリ固有設定を集約する dataclass 群を定義する oracle src。並列数、Codex CLI のモデル・推論設定と復旧回数、apply fork の処理上限、oracle review の各ループ上限を扱う。設定 JSON の永続化・同期仕様を確認する際の入口。

## Read this when
- CmocConfig や CodexModelSpec の設定項目・既定値・Enum の JSON 化規則を変更または確認するとき
- cmoc apply fork、cmoc oracle review、Codex CLI 呼び出しの設定上限を調査するとき

## Do not read this when
- 設定値の永続化処理や doctor による同期処理の実装を調べるとき
- モデル種別や推論 effort の Enum 定義そのものを調べるとき

## hash
- 22455da013612acebfd49d4042bcb2f927ccd04bc0ae8fbcfeb5bdbee60ffc67

# `path_model.py`

## Summary
- `oracle/src/oracle/other/path_model.py` の、`{{cmoc-root}}`・`{{repo-root}}`・`{{run-root}}`・`{{work-root}}` の解決規則と、実パスとプレースホルダ表記の相互変換を扱う入口。パス解決の境界条件や例外を確認したいときに読む。

## Read this when
- ルートパスプレースホルダの意味や解決方法を変えるとき
- 絶対パス・相対パス・プレースホルダ付きパスの受け入れ条件を確認したいとき
- `work-root` / `repo-root` / `run-root` / `cmoc-root` の見つけ方や失敗時挙動を調べたいとき
- 実パスをプレースホルダ表記へ戻す変換の仕様を確認したいとき

## Do not read this when
- CLI のサブコマンド全体や他の設定モデルを探したいとき
- 個別コマンドの入出力や業務ロジックを確認したいとき
- パス解決以外の共通ユーティリティや別の `oracle/other` ファイルを見たいとき

## hash
- a3d1106f01ca2a08139a30ecb7f60467f1f40b8071f1cf99cd77897d53dca932

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
