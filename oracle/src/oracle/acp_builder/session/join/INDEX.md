# `conflict_resolution.py`

## Summary
- `cmoc session join` の merge conflict 解消に使う AI 呼び出しパラメータを組み立てる入口。競合ファイルの実パスを正規化し、修正対象の範囲を conflict 解消に限定した prompt と実行設定を返す。

## Read this when
- `cmoc session join` で merge conflict marker を解消する呼び出し条件や、AI に渡す指示内容・実行設定を確認したいとき。
- 競合ファイルの扱いを変えたい、または conflict 解消時に許される編集範囲や品質設定の根拠を確認したいとき。

## Do not read this when
- session join の通常の接続や同期処理を探しているときは、join 本体の実装や周辺の session モジュールを先に読む。
- merge conflict 解消の実行結果そのものや後段の適用処理を知りたいときは、このパラメータ生成ではなく、呼び出し先の実行経路を読む。

## hash
- 5f646aac557f2c4083580311cb0aef8d2b055d400fbea13bee43603b97e52910
