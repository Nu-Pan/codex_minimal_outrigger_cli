# `conflict_resolution.py`

## Summary
- 対象は `cmoc session join` 実行中に競合したファイルを解消するためのエージェント呼び出しパラメータを構築する。
- 競合対象ファイルのパスを解決してプロンプトへ渡し、conflict marker の除去と共通の oracle・realization・競合解消・ルーティング規定を有効にした実行条件を定義する。

## Read this when
- `cmoc session join` の merge conflict marker 解消処理の起動条件、対象ファイルの受け渡し、または解消後のエージェント呼び出し設定を確認するとき。
- session join の競合解消で、通常の indexing preflight を行わない呼び出しパラメータの構築箇所を特定するとき。

## Do not read this when
- session join の競合検出や merge 自体の進行、競合ファイルの内容に対する具体的な解消判断を確認したいとき。
- 一般的な prompt 生成や共通のエージェント呼び出し規定を確認したいときは、それぞれの共通実装・規定を直接読む。

## hash
- d3d540546185bbb5c3d563cebd8a74820bdeac0f4e6bd05fb823865c3d21966d
