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
- cmoc におけるパス表記と、agent call の作業ルート・リポジトリルートを扱う正本モデル。root placeholder の定義、placeholder と実パスの相互変換、Git worktree からの各ルート解決を提供する。パスの解決規則や agent call のパスコンテキストを確認・変更する作業では、この対象を入口にする。

## Read this when
- root placeholder の意味や `{{repo-root}}`・`{{work-root}}`・`{{run-root}}` の解決規則を確認するとき
- agent call の cwd から worktree root や repository root を導出する処理を変更するとき
- placeholder 表記と実際の絶対パスの変換処理を確認・変更するとき

## Do not read this when
- 特定の CLI 機能や realization の責務配置だけを確認する場合
- パスモデルを利用する個別機能の挙動を確認する場合は、その機能の実装や仕様を直接読むべきとき

## hash
- 8fc522d7e3ef8f4b608c64102a5f4a6d7eb7cf64422cd3c3f7b239dab4255418

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
