# `join`

## Summary
- `cmoc session join` のうち、merge conflict marker 解消を AI エージェントへ委任するための呼び出し条件とプロンプト構築を扱う領域。
- 解消対象パスの実パス化、対象一覧の提示、oracle file に marker がある場合の限定的な編集許可、実行モデル・reasoning・file access mode の指定を確認する入口となる。

## Read this when
- session join で検出された merge conflict marker の解消依頼を、どの role・goal・完了条件・禁止事項で AI に渡すか確認または変更したいとき。
- conflict 対象ファイル一覧や追加アクセス規則が、エージェント向けプロンプトへどう反映されるかを確認したいとき。
- oracle file に conflict marker が含まれる場合に、通常の編集禁止規則へどのような最小例外を与えるかを確認したいとき。
- merge conflict 解消専用のエージェント呼び出しで、利用する model、reasoning effort、実現ファイル編集権限の指定を調整したいとき。

## Do not read this when
- merge conflict marker を実際に解析・削除する編集アルゴリズムや解消結果の内容判断を探しているとき。
- session join 全体の制御フロー、conflict 対象の検出、git 操作、join 成功後の後処理を確認したいとき。
- 汎用的な markdown プロンプト部品、構造化ドキュメント描画、path model の実パス解決そのものを調べたいとき。
- merge conflict 以外の session join エージェント呼び出しや、通常の oracle/realization 更新方針を確認したいとき。

## hash
- f3ebc8b4e31d2f112ede8674c70afa589034013385cad2d636477271686f8c18
