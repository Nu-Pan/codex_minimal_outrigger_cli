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

# `consume_fixing_point.py`

## Summary

- この `<cmoc-root>/oracle/src/acp/builder/apply/fork/consume_fixing_point.py` のルーティング文書で、要修正点 1 件を消化して realization file を修正する入口です。
- `build_apply_fork_consume_fixing_point_parameter()` が、`fixing_point` を受け取り、`build_complete_prompt()` と `AgentCallParameter` を組み立てます。
- この入口は write-enabled で、Structured Output は要求しません。

## Read this when

- 検出済みの要修正点 1 件を、実際の修正作業に渡したいとき。
- write-enabled な実装修正フローの前提として、ファイルアクセス規則や実行方針を確認したいとき。
- `fixing_point` が作業ヒントとして扱われ、`git add` と `git commit` を行わない方針を確認したいとき。

## Do not read this when

- すでに `build_apply_fork_consume_fixing_point_parameter()` の用途が分かっていて、実装コードを直接確認したいとき。
- `change_summary.*`、`file_audit_finding.*`、`refine_fixing_point.*` など、別段階の `cmoc apply fork` 入力を探しているとき。
- Structured Output schema だけを確認したいとき。

## hash

- 40de8039f83a34e71a15efb0ee4c21e496c5c58def5feae30f7970cb4e23d1e2

# `file_audit_finding.py`

## Summary

- この `<cmoc-root>/oracle/src/acp/builder/apply/fork/file_audit_finding.py` のルーティング文書で、`cmoc apply fork` のファイル単位監査用 agent call parameter への入口です。
- `build_apply_fork_file_audit_parameter()` は `target_path` を起点に prompt と `AgentCallParameters` を組み立て、`finding_list.json` で使う Structured Output schema を指します。
- 監査対象ファイルを起点に、oracle file と realization file の不整合や、実装上の致命的問題を洗い出す流れを案内します。

## Read this when

- `build_apply_fork_file_audit_parameter()` が prompt と `AgentCallParameter` をどう組み立てるか確認したいとき。
- `cmoc apply fork` のファイル単位監査の入口を整理したいとき。
- `target_path` を起点に oracle file と realization file の不整合や致命的問題を洗い出したいとき。

## Do not read this when

- すでに `file_audit_finding.json` や `build_apply_fork_file_audit_parameter()` の実装を直接確認する対象が決まっていて、この目次を経由する必要がないとき。
- `cmoc apply fork` の変更要約、要修正点リスト改善、要修正点 1 件の実装修正を探しているとき。
- Structured Output schema だけを確認したいとき。

## hash

- 86fb2d7c3fb908514e632f95c9c0d63518cde12a104304786adbb4c7868f1657

# `finding_list.json`

## Summary

- `cmoc apply fork` で共通利用する要修正点リストの Structured Output schema です。
- `fixing_points` 配列の各要素に、見出し、根拠、要求仕様、実装観測、理由、修正方針をまとめます。
- `file_audit_finding.py` と `refine_fixing_point.py` が参照する出力先で、監査結果の集約と改善の両方に使います。

## Read this when

- `file_audit_finding.py` や `refine_fixing_point.py` が参照する JSON 形状を確認したいとき。
- 要修正点リストの項目構造、必須フィールド、証拠の持ち方を把握したいとき。
- 監査結果の連結や改善後の出力を機械処理するために schema を合わせ込みたいとき。

## Do not read this when

- 変更要約や要修正点 1 件の実装修正など、別系統の `cmoc apply fork` 仕様を探しているとき。
- `file_audit_finding.py` や `refine_fixing_point.py` の実装ではなく、出力先の Structured Output schema だけを確認したいとき。
- `cmoc review oracle` や `cmoc indexing` など、`apply fork` 以外の Structured Output schema を確認したいとき。

## hash

- 8bb1874451e6e8276f5d68a687f1ae0a76f95697aec84c806c10a78a7af19b64

# `refine_fixing_point.py`

## Summary

- `<cmoc-root>/oracle/src/acp/builder/apply/fork/refine_fixing_point.py` のルーティング文書で、`finding_list.json` への入口です。
- `build_apply_fork_refine_fixing_point_parameter()` は、連結済み要修正点リストを改善するための prompt と `AgentCallParameter` を組み立てます。
- 改善後の要修正点リストを、Structured Output schema に一致する JSON だけで返す前提を案内します。

## Read this when

- `cmoc apply fork` の要修正点リスト改善の prompt と出力 schema の入口を確認したいとき。
- 要修正点の重複、相互矛盾、明らかな False Positive の整理方針を把握したいとき。
- このファイルの `INDEX.md` を作成・修正する前に、どの資料へ分岐するか整理したいとき。

## Do not read this when

- すでに `build_apply_fork_refine_fixing_point_parameter()` の用途が分かっていて、このファイルの実装を直接確認したいとき。
- `cmoc apply fork` の変更要約やファイル単位監査など、別段階の入口を探しているとき。
- `finding_list.json` などの Structured Output schema だけを直接確認したいとき。

## hash

- c93700d0d8ea4b50f322349a9ab01e340efa378dac38ebcc365a530ed7eaf4d9
