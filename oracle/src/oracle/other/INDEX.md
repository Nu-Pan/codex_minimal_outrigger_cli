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
- 構造化された自然言語文章を、見出し階層・コードブロック・cmoc_block参照を含むMarkdownへ変換するヘルパー実装。構造文書、ブロック、コードブロックのモデルと、参照検証・空行整理・インデント正規化を扱う。

## Read this when
- 構造化文章のデータモデルやMarkdownレンダリング挙動を確認するとき
- cmoc_blockの定義・参照検証、見出し深度、コードブロック出力を調査するとき
- Markdown生成前の入力検証やテキスト正規化の仕様を確認するとき

## Do not read this when
- 通常のプロンプト構成やINDEX.mdのルーティング規則だけを確認したいとき
- 対象の具体的なCLI機能やエージェント実装の責務を調査するとき
- 既存のテストケースや開発環境の実行手順を確認したいとき

## hash
- 7378c55498f0d1c78e3428694ffa9c0cecce12013c3a2d1e632a07f2522cbf05
