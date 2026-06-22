
# `file_finding_enumeration.py`

## Summary

- この `file_finding_enumeration.py` のルーティング文書で、`cmoc apply fork` のファイル単位所見リストアップ用 prompt 正本への入口です。
- `target_path` を起点に、必要なら関連する oracle file や realization file も読みながら所見を調査し、`finding_list.json` 形式の出力を返します。
- `cmoc apply fork` の調査対象ファイルごとの列挙処理を案内する、所見リスト生成の起点です。

## Read this when

- `cmoc apply fork` のファイル単位所見リストアップの入口を確認したいとき。
- `target_path` を起点に、対象ファイルごとの所見を個別に列挙する仕様を把握したいとき。
- `build_apply_fork_file_finding_enumeration_parameter()` がどの prompt と出力先 schema を結びつけるか確認したいとき。

## Do not read this when

- すでに `build_apply_fork_file_finding_enumeration_parameter()` の用途が分かっていて、このファイルの実装を直接確認したいとき。
- `cmoc apply fork` の変更要約、所見リスト改善、所見 1 件の実装修正など、別段階の入口を探しているとき。
- `finding_list.json` などの Structured Output schema だけを確認したいとき。

## hash

- 0afe13d940c449eb500b7516868d85ccaac1ffe20a43e645c1558ae157322dda
