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

- `cmoc apply fork` の作業レポート用変更要約生成 prompt 正本への入口です。
- `change_summary.json` は、変更を意味論カテゴリごとにまとめる Structured Output schema です。
- `<cmoc-apply-branch>` 上の差分情報を、人間向けレポート用の要約へ変換する Codex CLI 呼び出しを案内します。

## Read this when

- `cmoc apply fork` の作業レポート用変更要約生成 prompt を確認したいとき。
- 変更カテゴリ、要約文、主要変更ファイルを含む Structured Output schema を確認したいとき。
- `build_apply_fork_change_summary_parameter()` が差分要約からどの呼び出しパラメータを作るかたどりたいとき。

## Do not read this when

- `cmoc apply fork` の要修正点検出、要修正点リスト改善、要修正点 1 件の実装修正を探しているとき。
- 変更要約ではなく、`change_summary.py` の Markdown 描画処理だけを確認したいとき。
- `cmoc review oracle` や `cmoc indexing` など、別系統の agent call parameter を探しているとき。

## hash

- f150b3084ea69bc2e0c129c43e03ba5cc3c0cc47266c7b6433f264b2532b95ac

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

- この `<cmoc-root>/oracle/src/agent_call_parameter/builder/apply/fork/file_audit_finding.py` のルーティング文書で、`cmoc apply fork` のファイル単位監査用 agent call parameter への入口です。
- `build_apply_fork_file_audit_parameter()` は `target_path` を起点に prompt と `AgentCallParameters` を組み立て、`file_audit_finding.json` で使う Structured Output schema を指します。
- 監査対象ファイルを起点に、oracle file と realization file の不整合や、実装上の致命的問題を洗い出す流れを案内します。

## Read this when

- `build_apply_fork_file_audit_parameter()` がどう prompt と `AgentCallParameters` を構築するか確認したいとき。
- `cmoc apply fork` のファイル単位監査の入口をまとめて把握したいとき。
- 監査対象ファイルを起点に、oracle file と realization file の不整合や実装上の致命的問題を確認したいとき。

## Do not read this when

- すでに目的のファイルが分かっていて、`file_audit_finding.py` や `file_audit_finding.json` を直接開くとき。
- `cmoc apply fork` の要修正点リスト改善、要修正点 1 件の実装修正、変更要約生成を探しているとき。
- `cmoc review oracle`、`cmoc indexing`、`cmoc session join` など、別系統の agent call parameter を探しているとき。

## hash

- 99e74b2a01831aa639c431c7cc8d451c9d54a6120e89be983cf953b482195602

# `fixing_point_application.py`

## Summary

- `cmoc apply fork` の要修正点 1 件に対する実装修正作業 prompt の入口です。
- realization file の修正を前提とし、Structured Output は要求しません。
- 要修正点情報は作業ヒントとして扱い、`git add` と `git commit` は実行しない方針を案内します。

## Read this when

- `cmoc apply fork` で検出済みの要修正点 1 件を、実際に修正するための prompt 正本を確認したいとき。
- realization file を編集する write-enabled な呼び出しで、どのようなファイルアクセス規則が前提になるか知りたいとき。
- 要修正点を絶対指示ではなく作業ヒントとして扱う、という実行方針を確認したいとき。

## Do not read this when

- `cmoc apply fork` のファイル単位監査や要修正点リスト改善など、読み取り専用の処理を探しているとき。
- 要修正点の抽出結果や Structured Output schema だけを確認したいとき。
- Codex CLI 実行後の `git add` や `git commit` の扱いだけを確認したいとき。

## hash

- 3511f9957d03d0e45a39e50875c7e7baa8d66f42b3021512e92bf921511643d4

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

- `<cmoc-root>/oracle/src/agent_call_parameter/builder/apply/fork/fixing_point_refinement.py` は、`cmoc apply fork` の連結済み要修正点リスト改善用 agent call parameter の入口です。
- `fixing_point_refinement.json` は、改善後の要修正点リストを表す Structured Output schema です。
- 重複、相互矛盾、False Positive を整理し、必要な見落としを補完する Codex CLI 呼び出しをたどるための目次です。

## Read this when

- 連結済み要修正点リストの改善 prompt や schema を確認したいとき。
- 要修正点の重複整理、矛盾解消、False Positive の扱いを確認したいとき。
- このファイルの `INDEX.md` を作成・修正する前に、どの資料へ分岐するか整理したいとき。

## Do not read this when

- ファイル単位監査を行う `file_audit_finding.py` / `file_audit_finding.json` を確認したいとき。
- 要修正点 1 件の実装修正を行う `fixing_point_application.py` を探しているとき。
- `cmoc review oracle` や別サブコマンドの agent call parameter を探しているとき。

## hash

- 6c6273ad3136363747cfcb6e404f026253deac4f0b4799dc824845ae85c5e8ce
