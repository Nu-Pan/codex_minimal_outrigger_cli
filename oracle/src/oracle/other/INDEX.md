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
- パス表記とルートプレースホルダの解決モデルを定義するモジュール。`RootPathPlaceHolder`、agent call 単位の `AgentCallPathContext`、実パスとプレースホルダ表記の相互変換、Git worktree・repository・cmoc root の探索を扱う。パス解決や agent call の作業ルート境界を確認する際の入口となる。

## Read this when
- `{{repo-root}}`、`{{work-root}}`、`{{run-root}}`、`{{cmoc-root}}` の意味や解決方法を確認するとき
- agent call の cwd から work root と repository root を導出する不変コンテキストを調査するとき
- プレースホルダ付きパスと実際の絶対パスの変換、Git worktree の root 探索を変更・検証するとき

## Do not read this when
- 特定の CLI や prompt builder の責務だけを調べ、パスモデル自体を確認する必要がないとき
- 対象の下位実装や利用箇所を直接確認すれば、パス解決規則の理解を要しないとき

## hash
- 73e0f9e448de9b1cb5eb85d4e03e808c74dbe931b0b55fcdef0c172f02497f26

# `struct_doc.py`

## Summary
- `SDHeader`、`SDTagBlock`、`SDCodeBlock`、`SDPolicy` などの構造化文書ノードを保持し、Markdown としてレンダリングするヘルパーを定義する。
- 見出し深度の自動計算、cmoc_block／cmoc_ref タグ、コードフェンス、規定文書のカテゴリ別出力、空行・インデントの正規化を扱う。
- 構造化文書のモデルと GFM レンダリング処理の入口であり、参照検査やポリシー統合、プロンプト部品の選択を確認する場合は対象外の実装へ進む。

## Read this when
- 構造化文書ノードの型・保持方法・子要素検証を変更または確認するとき
- SDHeader の見出し深度、SDTagBlock の参照タグ、SDCodeBlock のフェンス、SDPolicy のカテゴリ出力を変更または確認するとき
- Markdown レンダリングや文字列の空行・インデント正規化の挙動を調査するとき

## Do not read this when
- 参照の対応検査、ポリシーの意味的統合、prompt part の選択を調査するとき
- このモジュール以外の CLI 責務や、構造化文書を利用する側の処理を直接確認するとき

## hash
- 14362b77a471f4edf930e8874b1bacea1e3db43e1407714aa8bdfe3aeaf7fa86
