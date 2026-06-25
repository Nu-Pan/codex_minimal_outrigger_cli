# `conflict_resolution.py`

## Summary
- `cmoc session join` で検出済みの merge conflict marker を解消するための AI 呼び出しパラメータを組み立てる実装。対象パスを実パスへ解決し、conflict 解消に作業範囲を限定する prompt と、realization 書き込み権限・標準的な oracle/realization 指示を含む `AgentCallParameter` を生成する。

## Read this when
- `cmoc session join` の conflict marker 解消フェーズで、AI に渡す role・summary・goal・補助プロンプト・ファイルアクセス権限を確認または変更したいとき。
- conflict 対象ファイル一覧が prompt 内でどのように提示されるか、また対象パスがどの時点で実パスへ解決されるかを確認したいとき。
- merge conflict 解消作業に限って oracle file の最小編集を許可する例外条件や、git add/git commit を禁止する join 用 prompt の境界を確認したいとき。

## Do not read this when
- 通常の `cmoc session join` の全体制御、conflict marker の検出、merge 実行、または join 後の状態更新を調べたいとき。
- AI 呼び出しパラメータの共通データ構造、モデル種別、推論努力、ファイルアクセスモード自体の定義を調べたいとき。
- prompt 部品の markdown レンダリングや共通 prompt 構築ロジックそのものを変更したいとき。

## hash
- caceb7b108026650c89706b5a14843849da1f7f4c861170455ee863feab7f786
