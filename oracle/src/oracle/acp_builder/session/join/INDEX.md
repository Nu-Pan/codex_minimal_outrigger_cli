# `conflict_resolution.py`

## Summary
- `cmoc session join` が検出した merge conflict marker を解消するための AI エージェント呼び出しパラメータを構築する正本仕様断片。対象パスを作業ルート基準の実パスへ解決し、conflict 解消に限定した role・summary・goal・追加ファイルアクセス規則を含む complete prompt を組み立て、MAINSTREAM / MEDIUM / REALIZATION_WRITE の呼び出し設定として返す責務を持つ。

## Read this when
- `cmoc session join` の実行中に merge conflict marker 解消用エージェントを呼び出す条件、prompt 内容、許可される編集範囲を確認したいとき。
- conflict 対象ファイル一覧を prompt にどう渡すか、作業ルートや実パス解決をどこで行うかを確認したいとき。
- oracle file に conflict marker がある場合に限った最小編集許可や、git add / git commit を禁止する join 時の conflict 解消方針を確認したいとき。

## Do not read this when
- 通常の `cmoc session join` 全体の制御フロー、merge 実行、conflict 検出、join 後処理を確認したいだけのとき。
- merge conflict marker の具体的な解消アルゴリズムや、対象ファイル本文のマージ判断基準を探しているとき。
- `cmoc session join` 以外のサブコマンド用 agent prompt や、一般的な complete prompt 構築部品の仕様を確認したいとき。

## hash
- 178b29ee724b5e7ba01760409af66a822e2463ff42db68de5125061b5a4138ab
