# `cmoc_config.py`

## Summary
- cmoc のリポジトリ固有設定を集約するデータクラス群を定義する oracle src。JSON/TOML 共通値、Codex CLI の provider・モデル・推論 effort、oracle review のループ上限を扱う設定構造の入口。

## Read this when
- cmoc の設定項目や既定値を変更・参照するとき。
- Codex CLI のモデル provider、モデル指定、推論 effort、ファイルアクセス規則違反時のリカバリ回数を確認するとき。
- `cmoc oracle review` の所見列挙・マージ・検証ループの設定を確認するとき。

## Do not read this when
- 永続化された設定 JSON の生成・同期・人手調整の実態だけを確認するときは、指定された設定ファイルや doctor の実装を直接読む。
- `ModelClass` や `ReasoningEffort` の列挙値の定義を確認するときは、参照元の型定義を直接読む。

## hash
- e90bca5f30bc59a885acd876512c52f6c26d38d3ebd0d5c68a92862d5300ca5d

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
- 階層構造を持つ文書モデルを Markdown にレンダリングするヘルパーを提供する。文書・ブロック・コードブロックの構造化、cmoc_block 参照の検証、見出し深度の自動計算、空行と三重引用文字列の正規化を扱う。

## Read this when
- 構造化文書のデータモデル、Markdown レンダリング、cmoc_block 参照検証、見出し深度計算、または関連する文字列正規化の挙動を確認・変更するとき。

## Do not read this when
- 一般的な Markdown 生成や、構造化文書以外の CLI・プロンプト処理を確認するとき。cmoc_block の正本仕様を確認する場合は、先に仕様文書を読む。

## hash
- 3486a19956bf59e4ea551c4cdbb81105a9de2e6d5337fb2c0239eb85a0e1eb7a
