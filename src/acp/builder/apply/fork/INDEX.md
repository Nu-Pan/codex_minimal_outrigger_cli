# `change_summary.json`

## Summary

- `cmoc apply fork` の変更要約を返す Structured Output schema です。
- 差分を意味論ベースでカテゴリ分けし、各カテゴリの要約と主要な変更パスを `changes` 配列で表します。
- 対応する prompt 正本は `change_summary.py` です。

## Read this when

- `cmoc apply fork` の変更要約の JSON 出力仕様を確認したいとき。
- `changes` 配列の `category`、`summary`、`changed_paths` の構造を把握したいとき。
- `change_summary.py` と `change_summary.json` の対応関係を確認したいとき。

## Do not read this when

- すでに `change_summary.py` か `change_summary.json` を直接開いて内容を確認するとき。
- 所見列挙、所見 1 件の実装修正、所見リスト改善など、別の `cmoc apply fork` ファイルを探しているとき。
- `cmoc apply fork` 以外のサブコマンドや、別の Structured Output schema を確認したいとき。

## hash

- 51ffe6e61588c7c347494a36267c02b8d48f69f6e264fcaf396096938cdd672d

# `change_summary.py`

## Summary

- この `change_summary.py` のルーティング文書で、`cmoc apply fork` の変更要約生成への入口を案内します。
- `raw_git_diff` を受け取り、変更内容を意味論に基づいて要約し、`change_summary.json` の Structured Output schema に従って返します。
- `cmoc apply fork` の read-only 系処理の中で、変更要約を担当する起点です。

## Read this when

- `cmoc apply fork` の変更要約生成の入口がどのファイルか確認したいとき。
- `raw_git_diff` を入力にして、差分を人間向けの作業レポートとして要約する仕様を把握したいとき。
- 読み取り専用で `change_summary.json` 形式の出力を返す、`change_summary.py` の役割を整理したいとき。

## Do not read this when

- すでに `<cmoc-root>/oracle/src/acp/builder/apply/fork/change_summary.py` を直接開いて、変更要約生成の実装や prompt 構成を確認したいとき。
- `cmoc apply fork` のうち、変更要約ではなく `file_finding_enumeration.py`、`finding_application.py`、`refine_finding.py` のどれかを確認したいとき。
- `change_summary.json` の Structured Output schema だけを確認したいとき。

## hash

- e958bca0852f6b124010f16314781a5093835941077ed2faef44217ce9587626

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

# `finding_application.py`

## Summary

- この `<cmoc-root>/oracle/src/acp/builder/apply/fork/finding_application.py` のルーティング文書で、`cmoc apply fork` の所見 1 件を実装修正する prompt 正本への入口をまとめます。
- このファイルは realization file を書き換える write-enabled 系で、所見本文を作業の手掛かりとして使いながら、修正後の実装が realization standard に従うことを目指します。
- `git add` と `git commit` は実行禁止で、Structured Output schema を返すための入口ではありません。

## Read this when

- `<cmoc-root>/oracle/src/acp/builder/apply/fork/finding_application.py` が `cmoc apply fork` のどの役割を担うか整理したいとき。
- 1 件の所見を手掛かりに realization file を修正する write-enabled な prompt 正本を確認したいとき。
- `oracle_and_realization_basic` と `realization_standard` を前提に、所見本文をヒントとして扱う実装修正フローを把握したいとき。
- `git add` と `git commit` の禁止を含む、所見対応作業の注意点を確認したいとき。

## Do not read this when

- すでに `cmoc apply fork` の変更要約、ファイル単位の所見列挙、所見リスト改善へ進む対象が決まっていて、このファイルの入口説明が不要なとき。
- 所見を読むだけで、実装修正を伴わない read-only 系の prompt や Structured Output schema を確認したいとき。
- `finding_application.py` の実装本体ではなく、`finding_list.json` や別の出力 schema を直接確認したいとき。

## hash

- 5ccbcdfb0b6df05c24d272cc714f85e83eda521118be32160ce9294c947e0064

# `finding_list.json`

## Summary

- この `finding_list.json` のルーティング文書で、`cmoc apply fork` のファイル単位所見列挙結果を表す Structured Output schema への入口をまとめます。
- `findings` 配列の各要素は `title`、`evidences`、`oracle_requirement`、`observed_implementation`、`reason`、`suggested_fix` を持つ所見オブジェクトです。
- 各 `evidences` は絶対パス・行番号・要約を含み、根拠箇所を機械可読に示すための定義です。

## Read this when

- `cmoc apply fork` でファイル単位の所見一覧を JSON で返す形式を確認したいとき。
- `file_finding_enumeration.py` が出力先として参照する `finding_list.json` の項目構成を把握したいとき。
- `evidences` に入れる絶対パスや、所見 1 件に必要な必須フィールドを確認したいとき。

## Do not read this when

- `file_finding_enumeration.py` の prompt 本文や調査手順を直接確認したいとき。
- `change_summary.json` や別の `review oracle` 系 schema など、別用途の Structured Output 形式を探しているとき。
- `cmoc apply fork` の結果ではなく、別サブコマンドの仕様や個別実装を確認したいとき。

## hash

- 0bed168a2a89c47730cdc914c08c08f2a3ad4022595c4b910c5d8ff9ca335524

# `refine_finding.py`

## Summary

- この `refine_finding.py` のルーティング文書は、`cmoc apply fork` の所見リスト改善への入口をまとめる。
- 所見リストを入力に受け取り、重複・矛盾・明らかな False-Positive を整理し、新規所見を必要に応じて追加したうえで、`finding_list.json` に一致する JSON を返す流れを案内する。
- この階層では、所見列挙や所見 1 件の修正ではなく、既存の所見群を作業可能な順序に整える役割を持つ。

## Read this when

- `cmoc apply fork` 配下で、所見リスト改善用の入口を確認したいとき。
- 複数ファイルから集めた所見リストを、重複や矛盾を整理したうえで再構成する仕様を把握したいとき。
- `build_apply_fork_refine_finding_parameter()` がどの prompt と出力先 schema を結びつけるか確認したいとき。

## Do not read this when

- すでに `refine_finding.py` の実装本体を直接確認する目的が決まっていて、この目次を経由する必要がないとき。
- `cmoc apply fork` の所見リスト改善ではなく、変更要約・ファイル単位の所見列挙・所見 1 件の実装修正を確認したいとき。
- `finding_list.json` の Structured Output schema だけを直接確認したいとき。

## hash

- dbcd18cc3d27d4bf74eb05d955961889209e4d95d238beac43350f7867314d6a
