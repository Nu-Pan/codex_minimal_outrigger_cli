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
- cmoc 内で扱うルートパス表記と実パス解決のモデルを定義する。プレースホルダの種類、agent call 単位のパスコンテキスト、各ルートの導出・変換関数を提供し、prompt builder などが一貫したパス解決を行うための入口となる。

## Read this when
- cmoc のファイルパスをプレースホルダ表記と実際の絶対パスの間で変換・解決するとき
- agent call の cwd から work root や repository root を導出する処理を確認するとき
- ルートプレースホルダの定義、Git worktree の探索、パス表記変換の責務を確認するとき

## Do not read this when
- 特定の CLI 機能や prompt の内容だけを確認し、パスの解決・表記変換に関係しないとき
- Git worktree の一般的な操作や repository 固有の開発規則を確認するときは、対応する開発規則・実装対象を直接読む

## hash
- 4af5fea100ef4985e4eca9c556c53b91187a151fc0919b394e12f5d7585faf33

# `struct_doc.py`

## Summary
- 構造化された文章ノードを Markdown にレンダリングするヘルパークラスと関数を提供する。見出し、参照可能な cmoc ブロック、コードブロック、構造化ポリシー、文字列を扱い、見出し深度やコードフェンスを自動調整する。
- SDTagBlock は cmoc_block の生成と参照タグの提供を担い、SDPolicy は必須・禁止・許容・補足情報の規定を表現する。cmoc_block／cmoc_ref、SDPolicy、GFM rendering の実装責務を持つが、参照検査、ポリシー統合、prompt part 選択は担当しない。
- Markdown 出力の整形では、三重引用文字列のインデント除去、連続空行の圧縮、本文中のバッククォートに応じたコードフェンス長の調整を行う。

## Read this when
- 構造化された文章や規定を Markdown にレンダリングする処理を変更・調査するとき
- SDHeader、SDTagBlock、SDCodeBlock、SDPolicy、または ntqs の挙動を確認するとき
- cmoc_block／cmoc_ref の出力形式やコードブロックのフェンス生成を確認するとき

## Do not read this when
- 参照タグの対応関係の検査、ポリシーの意味的統合、prompt part の選択を調査・変更するとき
- Markdown 以外のレンダリング機能を直接扱うとき
- このモジュールが提供するノードやレンダリング結果を利用するだけで、実装詳細を確認する必要がないとき

## hash
- 43ad89185abadeec6997caaec0cef99916ac9f0adce5ada31b2b1ef15cee18f7
