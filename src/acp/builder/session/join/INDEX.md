# `conflict_resolution.py`

## Summary
- `cmoc session join` で検出された merge conflict marker を解消するための AI エージェント呼び出しパラメータを構築する実装。
- 解消対象パスを実パスへ解決し、conflict 対象ファイル一覧、作業範囲、編集禁止事項、oracle file に conflict marker がある場合の限定的な編集許可を含む complete prompt を組み立てる。
- 返すパラメータでは mainstream model、medium reasoning、realization write のファイルアクセス方針、生成済み markdown prompt を指定する。

## Read this when
- `cmoc session join` の merge conflict marker 解消エージェントに渡す prompt や呼び出し条件を確認・変更したいとき。
- conflict 解消時に許可する編集範囲、git add/commit 禁止、conflict marker 残存禁止などの制約をどこでプロンプト化しているか確認したいとき。
- conflict 対象ファイルのパス一覧をどのように解決し、エージェント向け補助文書へ埋め込んでいるか確認したいとき。

## Do not read this when
- `cmoc session join` 全体の制御フロー、conflict marker の検出処理、merge 実行処理を確認したいだけのとき。
- complete prompt の共通構造、markdown レンダリング、StructDoc/StructCodeBlock の汎用仕様を確認したいとき。
- path model の `<work-root>` 解決や実パス解決そのものの仕様・実装を確認したいとき。

## hash
- caceb7b108026650c89706b5a14843849da1f7f4c861170455ee863feab7f786
