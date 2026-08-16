# `conflict_resolution.py`

## Summary
- `cmoc session join` における git merge conflict 解消用エージェント呼び出しパラメータを構築する定義。競合対象パスを実体パスへ解決し、conflict marker のみを解消するための prompt、アクセス方針、最高品質のモデル・推論設定、実行コンテキストをまとめる。

## Read this when
- `cmoc session join` の merge conflict 解消処理に使う agent call の prompt や起動パラメータを変更・確認するとき。
- conflicted paths の解決、conflict 対象ファイルの prompt への埋め込み、または conflict 解消時のモデル・実行設定を調査するとき。

## Do not read this when
- session join の通常の結合処理や conflict 解消以外の prompt 構築を調べるとき。
- 競合解消対象のファイル内容や git 操作の実装を直接確認したいときは、まずそれぞれの対象実装を読む。

## hash
- 64fe8f0375b797b1b01e47c3e5eec62f8fa4ea8c2388d4b694c08b0190993915
