# `join`

## Summary
- `cmoc session join` 中の merge conflict marker 解消エージェント呼び出し仕様へ進むための領域。conflict 対象パスの解決、解消専用 prompt、編集許可範囲、呼び出し設定を確認する入口になる。

## Read this when
- `cmoc session join` が merge conflict marker 解消用エージェントをどの条件・設定・prompt で呼び出すか確認したいとき。
- conflict 対象ファイル一覧を作業ルート基準の実パスとして扱う仕様や、解消作業に限定した role・summary・goal・ファイルアクセス規則を確認したいとき。
- join 時の conflict 解消で許される最小編集範囲、oracle file の conflict marker への扱い、git add / git commit 禁止方針を確認したいとき。

## Do not read this when
- `cmoc session join` 全体の制御フロー、merge 実行、conflict 検出、join 後処理を確認したいだけのとき。
- merge conflict marker の具体的な解消アルゴリズムや、対象ファイル本文をどう統合判断するかを探しているとき。
- `cmoc session join` 以外のサブコマンド用 agent prompt や、汎用的な complete prompt 構築部品の仕様を確認したいとき。

## hash
- 51eb14ded23a71985441098a20da86d73d213509c631b89034fc0b204e97ed98
