# `join`

## Summary
- `cmoc session join` における merge conflict marker 解消用 AI エージェント呼び出しの構築を扱う領域。
- conflict 対象パスの実パス解決、対象ファイル一覧や作業範囲の提示、編集禁止事項、oracle file に conflict marker がある場合の限定的な編集許可を含む complete prompt の組み立てを確認する入口。
- エージェント実行パラメータとして、利用モデル、reasoning 設定、ファイルアクセス方針、生成済み markdown prompt をどう指定するかを扱う。

## Read this when
- `cmoc session join` の merge conflict marker 解消を AI エージェントへ委譲する条件や prompt 内容を確認・変更したいとき。
- conflict 解消時の編集可能範囲、git add/commit 禁止、conflict marker 残存禁止などの制約がどのようにエージェントへ渡されるかを確認したいとき。
- conflict 対象ファイルのパス一覧を解決し、エージェント向け補助文書へ埋め込む処理を確認したいとき。
- oracle file に conflict marker が含まれる場合だけ許す限定的な編集方針を確認したいとき。

## Do not read this when
- `cmoc session join` 全体の制御フロー、merge 実行、conflict marker 検出処理を確認したいだけのとき。
- complete prompt の共通構造、markdown レンダリング、構造化ドキュメント部品の汎用仕様を確認したいとき。
- path model の語彙定義、作業ルート解決、実パス解決そのものの仕様や共通実装を確認したいとき。
- merge conflict 解消後の検証、保存、コミット、ブランチ操作など、エージェント呼び出しパラメータ構築の外側にある処理を調べたいとき。

## hash
- f3ebc8b4e31d2f112ede8674c70afa589034013385cad2d636477271686f8c18
