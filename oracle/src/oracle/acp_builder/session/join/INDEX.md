# `conflict_resolution.py`

## Summary
- `session join` の conflict marker 解消を依頼する agent call の prompt と起動パラメータを組み立てる oracle 実装です。
- conflict 対象のパスや書き込み範囲、適用する policy、indexing preflight の有無など、call 固有の設定を確認する入口です。

## Read this when
- `session join` の conflict 解消用 agent call の指示構成や起動設定を調べる、または変更するとき。
- conflict 対象の渡し方、適用 policy、ファイルアクセス範囲、preflight の扱いを確認するとき。

## Do not read this when
- conflict 解消の意味上の優先順位や解消結果の条件を確認するときは、session join の正本仕様を参照してください。
- agent に渡す conflict 解消 policy の文面を確認するときは、その policy を構築する専用の実装を参照してください。

## hash
- d3d540546185bbb5c3d563cebd8a74820bdeac0f4e6bd05fb823865c3d21966d
