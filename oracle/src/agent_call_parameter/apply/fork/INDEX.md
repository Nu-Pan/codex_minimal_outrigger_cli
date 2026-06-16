# `change_summary.py`

## Summary

- `cmoc apply fork` の作業レポート用変更要約生成 prompt 正本です。
- `change_summary.json` は、変更内容を意味論カテゴリごとにまとめる Structured Output schema です。
- `<cmoc-apply-branch>` 上の差分情報を人間向けレポート用の要約へ変換する Codex CLI 呼び出しを案内します。

## Read this when

- `cmoc apply fork` の作業レポートに載せる変更要約生成の prompt を確認したいとき。
- 変更カテゴリ、要約文、主要変更ファイルの Structured Output schema を確認したいとき。

## Do not read this when

- 要修正点の検出、改善、修正作業そのものの prompt を探しているとき。
- レポート markdown のレンダリング処理だけを確認したいとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `file_audit_finding.py`

## Summary

- `cmoc apply fork` のファイル単位監査用 agent call parameter を構築する prompt 正本です。
- `file_audit_finding.json` は、ファイル起点で見つけた要修正点リストの Structured Output schema です。
- `target_path` を起点に、oracle file と realization file の不整合や実装上の致命的問題を洗い出す流れを案内します。

## Read this when

- `build_apply_fork_file_audit_parameter()` がどのように prompt と `AgentCallParameters` を組み立てるか確認したいとき。
- `cmoc apply fork` のファイル起点要修正点リストアップ呼び出しを確認したいとき。

## Do not read this when

- 要修正点リスト全体の改善、要修正点対応作業、作業レポート要約を探しているとき。
- `cmoc review oracle` や `cmoc indexing` の agent call parameter を探しているとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `fixing_point_application.py`

## Summary

- `cmoc apply fork` の要修正点 1 件に対する実装修正作業 prompt 正本です。
- この呼び出しは realization file の編集を伴い、Structured Output は要求しません。
- 要修正点情報を絶対指示ではなく作業ヒントとして扱うこと、git add と git commit を禁止することを定義します。

## Read this when

- `cmoc apply fork` が検出済み要修正点を Codex CLI に修正させる prompt を確認したいとき。
- 書き込み可能な Codex CLI 呼び出しのファイルアクセス規則を確認したいとき。

## Do not read this when

- 要修正点の検出やリスト改善など、読み取り専用の監査系呼び出しを探しているとき。
- Codex CLI 実行後の git commit 処理だけを確認したいとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `fixing_point_refinement.py`

## Summary

- `cmoc apply fork` の連結済み要修正点リスト改善 prompt 正本です。
- `fixing_point_refinement.json` は、改善後の要修正点リストの Structured Output schema です。
- 重複、相互矛盾、False-Positive を整理し、必要なら漏れを追加する Codex CLI 呼び出しを案内します。

## Read this when

- `cmoc apply fork` の要修正点リスト改善 prompt を確認したいとき。
- 改善後の要修正点リストの schema を確認したいとき。

## Do not read this when

- ファイル単位監査や要修正点 1 件の修正作業を探しているとき。
- review oracle の所見整理を探しているとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
