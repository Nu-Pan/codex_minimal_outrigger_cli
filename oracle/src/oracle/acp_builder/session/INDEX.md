# `join`

## Summary
- 対象ディレクトリは、session join における通常のマージ処理と分離して、merge conflict marker を解消するためのエージェント呼び出し設定を構築する層への入口です。
- conflict 対象ファイルの指定、編集モード、専用の conflict 解消 policy、indexing preflight の扱いを確認・変更するときに読む対象です。

## Read this when
- session join の conflict 解消処理で、どのファイルを対象にどの編集条件でエージェントへ渡すかを確認したいとき。
- merge conflict marker 解消用の prompt と起動パラメータを構築する実装の入口を探しているとき。

## Do not read this when
- session join の通常のマージ処理や、conflict 解消以外の prompt 構築を確認したいとき。
- 構築済み prompt の共通仕様や個別 policy の定義そのものを確認したいときは、それぞれの prompt builder または policy 定義を直接読むべきです。

## hash
- ef52fb55bb2d74983186220c1a9c8ada7dbb290151f495891721e30577fa3f67
