# `join`

## Summary
- `cmoc session join` の merge conflict 解消用に、AI 呼び出しへ渡すパラメータを組み立てる入口。競合ファイルの実パスを正規化し、conflict 解消に必要な範囲だけを扱う prompt と実行設定を返す。

## Read this when
- `cmoc session join` で merge conflict marker を解消する呼び出し条件や、AI に渡す指示内容・実行設定を確認したいとき。
- 競合ファイルの扱いを変えたいとき、または conflict 解消時に許される編集範囲や品質設定の根拠を確認したいとき。

## Do not read this when
- session join の通常の接続や同期処理を探しているときは、join 本体の実装や周辺の session モジュールを先に読む。
- merge conflict 解消の実行結果そのものや後段の適用処理を知りたいときは、このパラメータ生成ではなく、呼び出し先の実行経路を読む。

## hash
- 6a35517220794414368499c04b978d9e1d772bbd2ab1be4e16c2ae72da14a4c9
