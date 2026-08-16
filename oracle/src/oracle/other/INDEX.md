# `cmoc_config.py`

## Summary
- cmoc のリポジトリ固有設定を表すデータモデル。Codex CLI のモデル・推論設定、AI 呼び出しの並列数、ファイルアクセス違反時のリカバリ回数、oracle review の各ループ上限を定義する。設定の JSON/TOML 表現や既定値の構成を確認する入口でもある。

## Read this when
- cmoc の設定項目を追加・変更するとき
- Codex CLI のモデル、provider-local 設定、推論 effort、リカバリ試行回数の扱いを確認するとき
- `cmoc oracle review` の所見列挙・マージ・検証ループの設定を確認するとき
- 設定のシリアライズ規則や既定の設定構造を確認するとき

## Do not read this when
- Codex CLI の呼び出し処理そのものや CLI 実装の責務を確認したいとき
- `cmoc oracle review` のレビュー処理の実装や所見生成ロジックを確認したいとき
- 設定ファイルの実際の保存内容や人間による調整結果だけを確認したいとき

## hash
- 8b7d86400aa658565b80abc2ecd33aa4f7b0af8d9a43f907cd939972cc422efd

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

# `policy.py`

## Summary
- agent 向け instruction の規定を表す immutable な Policy、適用範囲ごとにまとめる PolicyGroup、合成単位の PolicyCollection を定義する。Policy の入力検証と immutable 化、ID 衝突・定義競合を検査した決定的な collection 合成、および合成済み規定を StructDoc の agent 向け文面へ変換する処理の入口となる。

## Read this when
- agent 向け instruction の規定値や規定グループのデータモデルを変更・利用するとき
- 複数の policy collection を競合検査付きで合成する処理を確認するとき
- policy を StructDoc の見出し・要求文へレンダリングする処理を確認するとき

## Do not read this when
- agent 向け instruction の規定モデルや合成・レンダリングに関係しない StructDoc の一般的な利用だけを確認するとき
- 具体的な instruction の宣言内容や prompt 全体の組み立てを確認する場合（この対象ではなく、規定を定義・利用する上位の対象を読む）

## hash
- 354778fdd844f394f06749ab576373fb6ea2368b8b8a8d9d5cb85abfcb4fad71

# `struct_doc.py`

## Summary
- 階層化された自然言語文書を Markdown にレンダリングするためのデータクラスと補助関数を定義する。`StructDoc`、`StructBlock`、`StructCodeBlock` の構造表現、見出し深度・コードフェンス・空行の整形、`cmoc_ref` の検証、三重引用文字列のインデント正規化を扱う。Markdown の構造化文書生成、cmoc ブロック参照の検証、またはこれらのレンダリング規則を変更・確認するときの実装入口である。

## Read this when
- 構造化された文書や cmoc ブロックを Markdown に変換する処理を変更・調査するとき
- 見出し深度、コードフェンス、空行、`cmoc_ref` の妥当性検査、三重引用文字列の正規化の挙動を確認するとき

## Do not read this when
- Markdown 以外の文書生成処理を調べるとき
- cmoc のプロンプト構成やブロック参照ポリシーそのものを確認する場合で、レンダリング実装を確認する必要がないとき

## hash
- 398e1c8d1d609ff8ff2fd92a8addb6a064372bf66e00c8f79125a6640e5dad06
