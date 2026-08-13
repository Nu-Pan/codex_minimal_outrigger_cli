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
- cmoc のパス表記に用いる root placeholder と、agent call 単位の work root・repository root を表現するモデルを定義する。
- placeholder を含むパスの実体解決と、Git worktree・repository root の探索および実パスから placeholder 表記への変換を担う。

## Read this when
- cmoc のパス placeholder、agent call の作業コンテキスト、worktree や repository root の解決規則を確認・変更するとき。
- placeholder 付きパスと実パスの相互変換、または root 探索の挙動を調査するとき。

## Do not read this when
- パスモデルを利用する個別機能の処理だけを確認するとき。
- cmoc の一般的な CLI 挙動や、パス解決とは無関係な oracle・realization の仕様を読むとき。

## hash
- 83cea74218b4c0877790ce4230ac7e1e8d0485e3c6d81fb290596f5d6709c70e

# `standard.py`

## Summary
- 標準（Standard）・標準グループ・標準コレクションの immutable な値オブジェクトと、標準コレクションの衝突検査付き合成および agent 向け StructDoc への変換を定義する。標準の検証規則、決定的なグループ／標準順序、instruction 文面の構築を確認するための入口。

## Read this when
- agent 向け instruction の標準定義、適用範囲、必須・禁止・推奨・許容事項を追加・変更するとき
- 複数の標準コレクションを合成する際の ID 衝突検査や決定的な出力順を確認するとき
- 合成済み標準を StructDoc の instruction 文面へ変換する処理を確認・変更するとき

## Do not read this when
- INDEX.md のルーティングだけを確認するとき
- 標準値の具体的な利用箇所や個別の instruction 内容だけを確認したいときは、直接その利用元または標準定義へ進む

## hash
- 90d295e650bfb26425810fe363c87be76fa078cf104b11fc22f0b23f4744272b

# `struct_doc.py`

## Summary
- 構造化された文書要素を見出し階層付き Markdown へ変換するヘルパーを提供する。StructDoc、StructBlock、StructCodeBlock で文書構造・参照可能なブロック・コードブロックを表現し、レンダリング時に参照先の欠落やブロック ID の重複を検証する。

## Read this when
- Markdown 文書をプログラムで組み立てる処理を変更または調査するとき。
- StructDoc の階層見出し、cmoc_block、cmoc_ref、コードフェンスのレンダリング挙動を確認するとき。
- 構造化文書内の参照検証やトリプルクォート文字列のインデント正規化を扱うとき。

## Do not read this when
- 通常の Markdown の記述方法や、構造化文書を利用しない別の文書生成処理を確認するとき。
- cmoc プロンプト全体の仕様や参照ルーティングを確認することが目的で、レンダリング実装の挙動を調べる必要がないとき。

## hash
- d9c978e1dfb51d768350c6e4baf3159c9db4f8a400a3ca8a29b97e7e764833e9
