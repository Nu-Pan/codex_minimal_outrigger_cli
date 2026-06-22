# `change_summary.json`

## Summary

- `cmoc apply fork` の作業レポート用変更要約を返す Structured Output schema です。
- 変更内容を意味論カテゴリごとにまとめ、各カテゴリの要約と主要変更ファイルの一覧を含みます。
- `<cmoc-apply-branch>` 上の差分を、人間向けレポートへ変換する出力形式です。

## Read this when

- `cmoc apply fork` の変更要約生成で、出力 JSON の形式を確認したいとき。
- 変更カテゴリ、カテゴリ要約、主要変更ファイルの構造を把握したいとき。
- `build_apply_fork_change_summary_parameter()` が参照する schema の中身を確認したいとき。

## Do not read this when

- ファイル単位監査、要修正点リスト改善、要修正点 1 件の実装修正など、変更要約以外の `cmoc apply fork` の入口を探しているとき。
- markdown へのレンダリング方法や git 運用だけを確認したいとき。
- `cmoc review oracle` や `cmoc indexing` など、別系統の agent call parameter や Structured Output schema を探しているとき。

## hash

- 51ffe6e61588c7c347494a36267c02b8d48f69f6e264fcaf396096938cdd672d

# `change_summary.py`

## Summary

- `<cmoc-root>/oracle/src/acp/builder/apply/fork/change_summary.py` のルーティング文書で、`change_summary.json` への入口です。
- `build_apply_fork_change_summary_parameter()` は `<cmoc-apply-branch>` 上の差分情報を受け取り、変更要約 prompt と Structured Output schema を結びつけます。
- 変更内容を意味論カテゴリごとに整理し、各カテゴリの要約と主要変更ファイルを返す流れを案内します。

## Read this when

- `cmoc apply fork` の変更要約生成で、prompt と出力 JSON の対応を確認したいとき。
- `change_summary.json` が定義する変更カテゴリ、カテゴリ要約、主要変更ファイルの構造を把握したいとき。
- `build_apply_fork_change_summary_parameter()` がどの `AgentCallParameter` を組み立てるかたどりたいとき。

## Do not read this when

- すでに `build_apply_fork_change_summary_parameter()` の用途が分かっていて、実装コードを直接確認するとき。
- `cmoc apply fork` のファイル単位監査、要修正点リスト改善、要修正点 1 件の実装修正を探しているとき。
- 変更要約ではなく、`change_summary.json` の Structured Output schema だけを確認したいとき。

## hash

- e958bca0852f6b124010f16314781a5093835941077ed2faef44217ce9587626

# `file_audit_finding.py`

## Summary

- この `file_audit_finding.py` のルーティング文書は、`cmoc apply fork` のファイル単位監査用 agent call parameter への入口です。
- `build_apply_fork_file_audit_parameter()` は `target_path` を起点に prompt と `AgentCallParameters` を組み立て、`finding_list.json` で使う Structured Output schema を参照します。
- 監査対象ファイルを起点に、oracle file と realization file の不整合や、実装上の致命的問題を洗い出す流れを案内します。

## Read this when

- `<cmoc-root>/oracle/src/acp/builder/apply/fork/file_audit_finding.py` がどこへつながるか整理したいとき。
- `build_apply_fork_file_audit_parameter()` が `target_path` を起点に prompt と `AgentCallParameters` をどう組み立てるか確認したいとき。
- `cmoc apply fork` のファイル単位監査の入口を把握し、oracle file と realization file の不整合や致命的問題の洗い出し方針を確認したいとき。

## Do not read this when

- すでに `build_apply_fork_file_audit_parameter()` の用途が分かっていて、実装コードや prompt 本体を直接確認したいとき。
- `cmoc apply fork` の変更要約、要修正点リスト改善、要修正点 1 件の実装修正を探しているとき。
- `finding_list.json` そのものの Structured Output schema だけを確認したいとき。

## hash

- 0afe13d940c449eb500b7516868d85ccaac1ffe20a43e645c1558ae157322dda

# `finding_application.py`

## Summary

- この `<cmoc-root>/oracle/src/acp/builder/apply/fork/finding_application.py` のルーティング文書で、`cmoc apply fork` の所見対応作業への入口です。
- `build_apply_fork_finding_application_parameter()` は `finding` を受け取り、`build_complete_prompt()` と `AgentCallParameter` を組み立てます。
- この入口は write-enabled で、Structured Output は要求しません。

## Read this when

- `cmoc apply fork` で検出済みの所見 1 件を、実際の realization file 修正へ渡したいとき。
- `finding` が作業ヒントとして扱われ、write-enabled で修正を進める前提を確認したいとき。
- `build_apply_fork_finding_application_parameter()` がどの `AgentCallParameter` を組み立てるか確認したいとき。

## Do not read this when

- すでに `build_apply_fork_finding_application_parameter()` の用途が分かっていて、このファイルの実装を直接確認したいとき。
- `cmoc apply fork` の変更要約、ファイル単位監査、要修正点リスト改善など、別段階の入口を探しているとき。
- `finding_list.json` の Structured Output schema だけを確認したいとき。

## hash

- 5ccbcdfb0b6df05c24d272cc714f85e83eda521118be32160ce9294c947e0064

# `finding_list.json`

## Summary

- `cmoc apply fork` で共通利用する要修正点リストの Structured Output schema です。
- `fixing_points` 配列の各要素に、見出し、根拠、要求仕様、実装観測、理由、修正方針をまとめます。
- `file_audit_finding.py` と `refine_finding.py` が参照する出力先で、監査結果の集約と改善の両方に使います。

## Read this when

- `file_audit_finding.py` や `refine_finding.py` が参照する `finding_list.json` の JSON 形状を確認したいとき。
- 要修正点リストの項目構造、必須フィールド、証拠の持ち方を把握したいとき。
- 監査結果の連結や改善後の出力を機械処理するために schema を合わせ込みたいとき。

## Do not read this when

- `cmoc apply fork` の変更要約や `finding` 1 件の実装修正など、別段階の入口を探しているとき。
- `file_audit_finding.py` や `refine_finding.py` の実装を直接確認したいとき。
- `cmoc review oracle` や `cmoc indexing` など、`apply fork` 以外の Structured Output schema を確認したいとき。

## hash

- 0bed168a2a89c47730cdc914c08c08f2a3ad4022595c4b910c5d8ff9ca335524

# `refine_finding.py`

## Summary

- この `<cmoc-root>/oracle/src/acp/builder/apply/fork/refine_finding.py` のルーティング文書で、`finding_list.json` への入口です。
- `build_apply_fork_refine_finding_parameter()` は、連結済みの所見リストを改善する prompt と `AgentCallParameter` を組み立てます。
- 改善後の所見リストを、`finding_list.json` に一致する JSON だけで返す前提を案内します。

## Read this when

- `cmoc apply fork` の所見リスト改善の prompt と出力 schema の入口を確認したいとき。
- 所見の重複、相互矛盾、明らかな False Positive の整理方針を把握したいとき。
- このファイルの `INDEX.md` を作成・修正する前に、どの資料へ分岐するか整理したいとき。

## Do not read this when

- すでに `build_apply_fork_refine_finding_parameter()` の用途が分かっていて、このファイルの実装を直接確認したいとき。
- `cmoc apply fork` の変更要約やファイル単位監査など、別段階の入口を探しているとき。
- `finding_list.json` などの Structured Output schema だけを直接確認したいとき。

## hash

- dbcd18cc3d27d4bf74eb05d955961889209e4d95d238beac43350f7867314d6a
