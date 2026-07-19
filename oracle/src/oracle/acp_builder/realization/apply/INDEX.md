# `fork`

## Summary
- Oracle 側の差分を realization file 全体へ反映する `codex exec` 用 AgentCallParameter の構築処理を扱う。raw git diff と commit 範囲を prompt に埋め込み、実行設定と linked worktree を組み立てる。

## Read this when
- `cmoc realization apply fork` の実行 prompt や realization 追従処理を変更・調査するとき。
- 対象 agent call のモデル、推論強度、ファイルアクセス、作業ディレクトリ、indexing preflight を確認するとき。

## Do not read this when
- 通常の realization 実装・テストを変更または調査するとき。
- prompt の一般的な組み立て規則だけを確認したいとき。

## hash
- 7c89cc510f69445bc05e90b52eaa820466a335c6d0b593b049f4b1f85564c9c9
