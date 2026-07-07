# `conflict_resolution.py`

## Summary
- `cmoc session join` で merge conflict marker を解消するための agent call parameter を組み立てる正本実装。対象パス一覧、追加の oracle file 編集許可、完全 prompt、モデル・推論強度・書き込み権限・preflight 抑制を定義する。

## Read this when
- session join の conflict marker 解消用 agent 呼び出しで、どの prompt・権限・モデル設定を使うべきか確認する必要があるとき。
- conflict 対象ファイル一覧を prompt に渡す方法や、conflict 解消時だけ oracle file 編集を許可する境界を確認するとき。
- merge conflict marker 解消時に indexing preflight を実行しない理由や、その設定値を確認するとき。

## Do not read this when
- session join 全体の通常処理、merge 実行、run 管理、または conflict 検出の実装を探しているとき。
- prompt builder や agent call parameter 型そのものの一般仕様を確認したいとき。
- conflict marker 解消以外のサブコマンド用 prompt や agent 呼び出し設定を調べたいとき。

## hash
- b14b023338d816126d7e6536dbc1b37b6b43e72a11fcbdeccc3b150d3dacd234
