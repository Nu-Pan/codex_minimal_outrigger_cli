# `conflict_resolution.py`

## Summary
- `cmoc session join` で発生した merge conflict marker を解消するための AI エージェント呼び出しパラメータを構築する。対象パスを解決し、競合解消用 prompt と最高品質設定を含む実行パラメータを返す。

## Read this when
- `cmoc session join` の merge conflict 解消フローを変更・調査するとき
- 競合対象ファイルのパス解決、prompt 内容、エージェント呼び出し設定を変更するとき

## Do not read this when
- `session join` 以外のサブコマンドの prompt 構築を変更するとき
- merge conflict 解消処理そのものや、共通 prompt 構築処理を直接変更するときは、それぞれの実装ファイルを先に読む

## hash
- e2a1871c13a73eb27762822ef9c5cda48ca7662a504295ce182ad70c88a62ad4
