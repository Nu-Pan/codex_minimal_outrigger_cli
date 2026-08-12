# `conflict_resolution.py`

## Summary
- `cmoc session join` における merge conflict marker 解消用の AI エージェント呼び出しパラメータを構築する。conflict 対象ファイルの実パス、専用 prompt、モデル・推論設定、リポジトリ書き込み権限、作業ディレクトリ、事前 indexing の無効化を定義する。

## Read this when
- `cmoc session join` の conflict marker 解消処理に使う prompt の内容や、呼び出し時のモデル・権限・パス・実行設定を確認または変更するとき。

## Do not read this when
- 通常の session join 処理、一般的な prompt 構築、または conflict 解消以外の agent call parameter を確認するとき。

## hash
- dd808899820f2a13faf7e0abf63d22642b31b4c51e09da5cb30b9bea34eaa2c2
