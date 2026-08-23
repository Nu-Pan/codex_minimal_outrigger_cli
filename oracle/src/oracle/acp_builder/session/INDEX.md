# `join`

## Summary
- 対象ディレクトリは、`cmoc session join` の merge conflict marker 解消専用 agent call を組み立てる定義への入口である。conflicted paths の実パス解決、対象ファイル一覧、conflict 解消専用 policy、REPO_WRITE 権限、最高品質の model・reasoning 設定、prompt と AgentCallParameter の生成を扱う。
- 実ファイルの conflict 解消や通常の prompt/session join 処理そのものではなく、conflict 解消 agent call のパラメータ境界を確認するために読む。

## Read this when
- `cmoc session join` で conflict marker を解消する agent call の prompt、完了条件、対象ファイルの渡し方を確認するとき
- conflict 解消 agent call の path context、file access mode、policy、model class、reasoning effort、preflight 設定を変更・調査するとき

## Do not read this when
- conflict marker を含む対象ファイルを直接確認・編集するとき
- 通常の prompt 生成処理や session join の別処理を調べるときは、該当する prompt builder または session join 実装を直接読む。

## hash
- 4dc26e6d1b1fbe7208e65bf19c5b9133161969aa651c7a578155da80c10528e6
