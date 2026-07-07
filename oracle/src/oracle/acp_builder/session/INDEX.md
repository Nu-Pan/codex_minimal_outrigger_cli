# `join`

## Summary
- `cmoc session join` の merge conflict marker 解消専用の agent call parameter を組み立てる正本実装を含む領域。conflict 対象パス一覧、追加の oracle file 編集許可、prompt、モデル・推論強度・書き込み権限・preflight 抑制の設定へ進む入口。

## Read this when
- session join の conflict marker 解消用 agent 呼び出しで使う prompt、権限、モデル設定を確認したいとき。
- conflict 対象ファイル一覧を prompt に渡す方法を確認したいとき。
- conflict marker 解消時だけ oracle file 編集を許可する境界を確認したいとき。
- merge conflict marker 解消時に indexing preflight を実行しない理由や設定を確認したいとき。

## Do not read this when
- session join 全体の通常処理、merge 実行、run 管理、または conflict 検出の実装を探しているとき。
- prompt builder や agent call parameter 型そのものの一般仕様を確認したいとき。
- conflict marker 解消以外のサブコマンド用 prompt や agent 呼び出し設定を調べたいとき。

## hash
- a0246bdae18cfbf8f1044ad88301e003c6292d9c0c5005b6118086f0411d2816
