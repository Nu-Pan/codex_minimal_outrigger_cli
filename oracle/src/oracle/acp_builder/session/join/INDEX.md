# `conflict_resolution.py`

## Summary
- session join の merge conflict marker 解消を行うエージェント呼び出しパラメータを構築する。対象パスの解決、専用ポリシーを含む prompt、書き込み権限、完了条件、起動設定をまとめる。

## Read this when
- `cmoc session join` で指定されたファイルの merge conflict marker を解消するための prompt 文面やエージェント起動パラメータを確認・変更するとき。
- conflict 解消対象パスの prompt への埋め込み方、conflict 解消専用の policy、preflight を行わない起動設定を確認するとき。

## Do not read this when
- merge conflict marker の具体的な解消ロジックや対象ファイルの内容を確認したいときは、実際の conflict 対象ファイルを直接読む。
- 通常の session join 動作、一般的な prompt 構築、または広い edit・refactor policy の定義だけを確認するとき。

## hash
- e34c50e655efc2b31b504a888b3a1bb5da5dd02de5bbeffc8ba9c27f82d87264
