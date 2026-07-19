# `launch_exec.py`

## Summary
- Oracle 側で定義された差分追従用 `codex exec` の AgentCallParameter 構築処理。oracle file の raw git diff と commit 範囲を prompt に埋め込み、realization file 全体への反映を委譲するための prompt・実行設定・linked worktree を組み立てる。

## Read this when
- `cmoc realization apply fork` の実行 prompt、realization 追従処理、または oracle 差分を realization file へ反映する AgentCallParameter の動作を変更・調査するとき。
- 対象 agent call のモデル、推論強度、ファイルアクセスモード、作業ディレクトリ、indexing preflight の設定を確認するとき。

## Do not read this when
- 通常の realization 実装やテストの内容を変更・調査するとき。
- prompt の一般的な組み立て規則だけを確認したいときは、prompt builder の実装を直接読む。

## hash
- 2f62a61956371b2154da3ededf6103c79ec999bfcabdae2983231f9f9364b97b
