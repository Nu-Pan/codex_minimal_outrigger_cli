# `change_summary.json`

## Summary

- `cmoc apply fork` の作業レポート用変更要約生成結果を表す Structured Output schema です。
- 変更内容を意味論カテゴリごとにまとめ、各カテゴリの要約と主要変更ファイルの一覧を含みます。
- `<cmoc-apply-branch>` 上の差分を、人間向けレポートへ変換する出力形式です。

## Read this when

- `cmoc apply fork` の変更要約生成で、出力 JSON の形式を確認したいとき。
- 変更カテゴリ、カテゴリ要約、主要変更ファイルの構造を把握したいとき。
- `build_apply_fork_change_summary_parameter()` が参照する schema の中身を確認したいとき。

## Do not read this when

- ファイル単位監査や要修正点改善など、変更要約以外の `cmoc apply fork` の prompt を探しているとき。
- markdown へのレンダリング方法や git 運用だけを確認したいとき。
- `cmoc review oracle` や `cmoc indexing` など、別系統の agent call parameter を探しているとき。

## hash

- bd5d65618cd5fc33d6a1fa0c2a63d0ec909c69990c2cc066b57f003a0c0b11d6

# `change_summary.py`

## Summary

- `<cmoc-root>/oracle/src/acp/builder/apply/fork/change_summary.py` のルーティング文書で、`change_summary.json` への入口です。
- `build_apply_fork_change_summary_parameter()` は `<cmoc-apply-branch>` 上の差分情報を受け取り、作業レポート向けの変更要約 prompt と Structured Output schema を結びつけます。
- 変更内容を意味論カテゴリごとに整理し、各カテゴリの要約と主要変更ファイルを返す流れを案内します。

## Read this when

- `cmoc apply fork` の変更要約生成で、prompt と出力 JSON の関係を確認したいとき。
- `change_summary.json` が定義する変更カテゴリ、カテゴリ要約、主要変更ファイルの対応を把握したいとき。
- `build_apply_fork_change_summary_parameter()` がどの `AgentCallParameter` を組み立てるかたどりたいとき。

## Do not read this when

- すでに `build_apply_fork_change_summary_parameter()` の用途が分かっていて、このファイルの実装を直接確認するとき。
- `cmoc apply fork` のファイル単位監査、要修正点リスト改善、要修正点 1 件の実装修正を探しているとき。
- 変更要約ではなく、`change_summary.json` の Structured Output schema だけを確認したいとき。

## hash

- cfc74bfed881f5e7cad97427b143dbc5110cc38b99a5a8c4852ac9ebd7b43353

# `file_audit_finding.json`

## Summary

- `cmoc apply fork` のファイル単位監査で使う Structured Output schema です。
- ファイル起点で見つけた要修正点を `fixing_points` として返す JSON 形式を定義します。
- `target_path` を起点に、oracle file と realization file の不整合や致命的な実装問題をまとめる出力の受け皿です。

## Read this when

- `file_audit_finding.json` が返す JSON の項目構造や必須フィールドを確認したいとき。
- ファイル起点の監査結果として、要修正点リストをどの形式で出力すべきか把握したいとき。
- `build_apply_fork_file_audit_parameter()` が参照する schema の内容を確認したいとき。

## Do not read this when

- `cmoc apply fork` のファイル単位監査ロジックそのものや、prompt 正本の実装を確認したいとき。
- 要修正点の修正作業や要修正点リストの改善仕様を探しているとき。
- `cmoc review oracle` や `cmoc indexing` など、別系統の Structured Output schema を確認したいとき。

## hash

- 6a83530f560f906540f4ab6d567b848a2f864dfb1d02e5cfd6aa08826c37752a

# `file_audit_finding.py`

## Summary

- この `<cmoc-root>/oracle/src/acp/builder/apply/fork/file_audit_finding.py` のルーティング文書で、`cmoc apply fork` のファイル単位監査用 agent call parameter への入口です。
- `build_apply_fork_file_audit_parameter()` は `target_path` を起点に prompt と `AgentCallParameters` を組み立て、`file_audit_finding.json` で使う Structured Output schema を指します。
- 監査対象ファイルを起点に、oracle file と realization file の不整合や、実装上の致命的問題を洗い出す流れを案内します。

## Read this when

- `build_apply_fork_file_audit_parameter()` がどう prompt と `AgentCallParameters` を構築するか確認したいとき。
- `cmoc apply fork` のファイル単位監査の入口をまとめて把握したいとき。
- 監査対象ファイルを起点に、oracle file と realization file の不整合や実装上の致命的問題を確認したいとき。

## Do not read this when

- すでに目的のファイルが分かっていて、`file_audit_finding.py` や `file_audit_finding.json` を直接開くとき。
- `cmoc apply fork` の変更要約、要修正点リスト改善、要修正点 1 件の実装修正を探しているとき。
- Structured Output schema だけを確認したいとき。

## hash

- bfc327295a549245fc8ad9e55c9fff3433d17abcea7fa600b4c15f5a8051ab8c

# `fixing_point_application.py`

## Summary

- この `<cmoc-root>/oracle/src/acp/builder/apply/fork/fixing_point_application.py` のルーティング文書で、`cmoc apply fork` の要修正点 1 件に対する実装修正作業用の入口です。
- この入口は realization file の修正を前提とする write-enabled な呼び出しで、Structured Output は要求しません。
- 要修正点は作業ヒントとして扱い、`git add` と `git commit` を行わない前提を案内します。

## Read this when

- 検出済みの要修正点 1 件を実際に修正する入口を確認したいとき。
- realization file を書き換える write-enabled な呼び出しで、前提となるファイルアクセス規則と実行方針を知りたいとき。
- 要修正点情報を絶対指示ではなく作業ヒントとして扱い、`git add` と `git commit` を行わない方針を確認したいとき。
- このファイルの `INDEX.md` を作成・修正する前に、どの資料へ分岐するか整理したいとき。

## Do not read this when

- すでに `build_apply_fork_fixing_point_application_parameter()` の用途が分かっていて、実装コードを直接確認したいとき。
- `cmoc apply fork` の変更要約、ファイル単位監査、要修正点リスト改善など、別段階の入口を探しているとき。
- Structured Output schema だけを確認したいとき。
- この入口ではなく、他の `cmoc review oracle`、`cmoc indexing`、`cmoc session join` 系の仕様を探しているとき。

## hash

- 44ad3e52c2528a022bac07ffbf4438dab09c99f9cbe9dc0f418f5b1815df65eb

# `fixing_point_refinement.json`

## Summary

- `cmoc apply fork` で改善後の要修正点リストを返すための Structured Output schema を定義している。
- 先頭に実行時点の git HEAD を入れる欄と、要修正点配列を返す構成になっている。
- 各要修正点は、見出し、根拠、要求仕様、実装観測、理由、修正方針を持つ。

## Read this when

- 改善後の要修正点リストの出力 JSON 形状を確認したいとき。
- 構造化出力の必須項目や入れ子構造を実装・検証したいとき。
- 生成結果を機械処理するためのパーサやバリデータを合わせ込みたいとき。

## Do not read this when

- 要修正点の検出ロジックやプロンプト本文だけを確認したいとき。
- 変更要約や要修正点 1 件の修正作業など、別段階の定義を探しているとき。
- ルーティング文書そのものではなく、実装コードの処理だけを追いたいとき。

## hash

- dc20fba5cd71e2bb6cbcf4208f1fbaa07347777182838e3e50b9a159bc04ccfb

# `fixing_point_refinement.py`

## Summary

- `<cmoc-root>/oracle/src/acp/builder/apply/fork/fixing_point_refinement.py` のルーティング文書で、`fixing_point_refinement.json` への入口です。
- `build_apply_fork_fixing_point_refinement_parameter()` は、連結済み要修正点リストを改善するための prompt と `AgentCallParameter` を組み立てます。
- 改善後の要修正点リストを、Structured Output schema に一致する JSON だけで返す前提を案内します。

## Read this when

- 連結済みの要修正点リストを改善する prompt と出力 schema の入口を確認したいとき。
- 要修正点の重複、相互矛盾、明らかな False Positive の整理方針を把握したいとき。
- このファイルの `INDEX.md` を作成・修正する前に、どの資料へ分岐するか整理したいとき。

## Do not read this when

- すでに `fixing_point_refinement.json` や `fixing_point_application.py` を直接確認する対象が決まっていて、この目次を経由する必要がないとき。
- `cmoc apply fork` の変更要約やファイル単位監査など、別段階の入口を探しているとき。
- このファイルの実装ではなく、Structured Output schema だけを直接読みたいとき。

## hash

- 16912e7bc5b98bc6abcbcbb4b39823f883f303c865784ff3d9d3c7b1d20a94d6
