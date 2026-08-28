# `conflict_resolution.py`

## Summary
- `cmoc session join` における git merge conflict marker 解消用のエージェント呼び出しパラメータを構築する。対象ファイルのパス、専用の conflict 解消ポリシー、リポジトリ書き込み権限、起動時の prompt を定義する。

## Read this when
- `session join` の conflict 解消処理で、エージェント呼び出しの prompt や起動パラメータを確認・変更するとき。
- conflict 対象ファイルの渡し方、専用 policy の選択、preflight を行わない起動設定を確認するとき。

## Do not read this when
- merge conflict 解消そのものの実装や marker 検出の挙動を確認したいとき。
- 一般的な prompt 構築、パス解決、または他の session join 処理を直接確認する場合。

## hash
- 3f84977ff8ed2dbb6a3b6f3ad879a8ff87250576db2059d36087cfdd78ba3ee0
