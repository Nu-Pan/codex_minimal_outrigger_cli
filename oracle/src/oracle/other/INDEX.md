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
- ルートパスプレースホルダと、agent call の cwd から repo/work/run root を導出するパスモデルを定義する。実パスとの相互変換、root 探索、call-scoped context の構築を扱う。パス解決や root placeholder、worktree 境界の実装・変更を確認するときの入口。

## Read this when
- root placeholder の追加・変更や、placeholder を含むパスの実体解決を調査するとき
- agent call の cwd、work root、repository root、run root の導出規則を確認するとき
- 実パスと placeholder 表記の変換、worktree 探索、パス入力の検証を変更・テストするとき

## Do not read this when
- CLI の具体的なサブコマンドや agent call prompt の生成処理だけを調査するとき
- パスモデルを利用する個別機能の挙動だけを確認し、root 解決や placeholder 変換自体を扱わないとき

## hash
- 8660330a40e76a5e7acf35ec03434282d0e05c4569a0319712e061d391fc848b

# `standard.py`

## Summary
- 規範（Standard）の定義モデルと、規範を構造化文書（StructDoc）へ変換する処理を提供する。Standard は題名、背景、要求、任意の判断例を保持し、Requirement は要求のラベルと本文を表す。

## Read this when
- Standard や Requirement のデータ構造・入力検証を確認するとき
- 規範定義を StructDoc 形式へ変換する処理を確認するとき
- INDEX.md エントリーなど、規範の適用形式を調査するとき

## Do not read this when
- 個別の規範本文や適用対象の要件を確認したいとき
- StructDoc 自体の仕様や実装を確認したいときは、まず StructDoc の定義を直接読む場合
- 規範を利用する呼び出し側の処理だけを調査するとき

## hash
- dc88f4650fb393d33b5b609ee0a739f9960737fd8fc42fd7cda51f037e1dab00

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
