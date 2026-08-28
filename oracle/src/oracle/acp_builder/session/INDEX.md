# `join`

## Summary
- `cmoc session join` の git merge conflict marker 解消用エージェント呼び出しパラメータを構築する。
- conflict 対象ファイルのパス、専用の conflict 解消ポリシー、リポジトリ書き込み権限、起動時 prompt を設定する。

## Read this when
- `session join` の conflict 解消で、エージェントの prompt や起動パラメータを確認・変更するとき。
- conflict 対象ファイルの渡し方、oracle file の編集範囲、専用 policy、preflight を行わない起動設定を確認するとき。

## Do not read this when
- merge conflict marker の検出や解消処理そのものの実装を確認したいとき。
- 一般的な prompt 構築、パス解決、または `session join` の他の処理を直接確認するとき。

## hash
- ed5066dffdad8bf41dd14283cb3f55909165ea1b5e6b2d8e28d84269254cc962
