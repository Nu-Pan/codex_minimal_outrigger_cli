# `join`

## Summary
- 対象ディレクトリ内の conflict_resolution.py は、session join のマージ競合マーカー解消を担当するエージェント呼び出し定義である。競合対象ファイルの実パスを prompt に渡し、リポジトリ編集を許可しつつ、oracle・realization・conflict resolution・routing の各ポリシーと indexing preflight を適用しない実行条件をまとめている。

## Read this when
- session join の conflict 解消で、競合対象ファイルの prompt への指定方法や、その解消エージェントに渡す実行条件を確認するとき。
- conflict 解消 prompt にどのポリシーを適用し、どの preflight を省略するかを確認するとき。

## Do not read this when
- 通常の merge 処理や session join 以外のサブコマンドにおけるエージェント呼び出し条件を確認するとき。
- prompt の共通構築規則や共通パラメータの定義を確認するときは、共通の prompt 構築定義を直接読むべきである。

## hash
- 9a895c2c67fed3d039706710c7e4a84cf716a5308c1cdc9e41dd1ff9c46e9ee3
