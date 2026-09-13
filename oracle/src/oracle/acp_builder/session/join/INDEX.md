# `conflict_resolution.py`

## Summary
- `cmoc session join` が対象ファイルの merge conflict marker を解消するために呼び出す AI エージェントの prompt と起動パラメータを構築する。

## Read this when
- `cmoc session join` の conflict 解消処理で、対象ファイルの指定方法、編集モード、専用 conflict 解消 policy、または indexing preflight の無効化を確認したいとき。
- merge conflict marker 解消用のエージェント呼び出し設定の入口を探しているとき。

## Do not read this when
- session join の通常のマージ処理や conflict 解消以外の prompt 構築を確認したいとき。
- 構築済み prompt の共通仕様そのものを確認したいときは、prompt builder や各 policy の定義を直接読むべき。

## hash
- 8db7571866a2ab3f937b2387df7e9281fd2899960167ec5b9204205ed87bbd59
