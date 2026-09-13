# `conflict_resolution.py`

## Summary
- `cmoc session join` で発生した merge conflict marker を解消するエージェント呼び出しパラメータと prompt を構築する定義。
- conflict 対象ファイルの実パスを prompt に埋め込み、リポジトリ書き込み権限、各種ポリシー、indexing preflight を行わない実行条件を設定する。

## Read this when
- `cmoc session join` の conflict 解消処理で、対象ファイルの指定方法やエージェント呼び出し条件を確認したいとき。
- conflict 解消用 prompt に適用する oracle・realization・conflict resolution・routing の各ポリシーを確認したいとき。

## Do not read this when
- session join の conflict 解消ではなく、通常の merge 処理や別サブコマンドのエージェント呼び出し条件を確認したいとき。
- prompt の共通構築規則そのものを確認したいときは、共通 prompt 構築定義を直接読むべきである。

## hash
- d3d540546185bbb5c3d563cebd8a74820bdeac0f4e6bd05fb823865c3d21966d
