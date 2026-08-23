# `conflict_resolution.py`

## Summary
- `cmoc session join` における merge conflict marker 解消用の AI エージェント呼び出しパラメータを構築する定義。
- conflicted_paths を実パスへ解決し、対象ファイル一覧、conflict 解消専用 policy、REPO_WRITE 権限、最高品質のモデル・推論設定を含む prompt と AgentCallParameter を生成する。

## Read this when
- `cmoc session join` の conflict 解消で、prompt の目的・完了条件・対象ファイルの渡し方を確認するとき
- conflict 解消用 agent call の path context、file access mode、policy 選択、model class、reasoning effort、preflight 設定を変更するとき

## Do not read this when
- merge conflict marker を実際に解消する対象ファイルの内容を確認・編集するとき
- 通常の prompt 生成処理や session join の別処理を調べるときは、まずこの conflict 解消専用パラメータ定義ではなく、該当する prompt builder または session join 実装を直接読む

## hash
- 41842a068165e831138023fabd2315dc4fdb6028496c53b0e43fbc815ca7fb26
