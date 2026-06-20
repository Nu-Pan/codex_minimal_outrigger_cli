# `apply`

## Summary

- この `apply` ディレクトリのルーティング文書で、`fork/` への入口です。
- `fork/` では変更要約、ファイル単位監査、要修正点リスト改善、要修正点 1 件の実装修正を案内します。
- `fork/` 配下には read-only の Structured Output 系と、write-enabled な実装修正系の入口があります。

## Read this when

- この配下で、変更要約・ファイル単位監査・要修正点リスト改善・要修正点 1 件の実装修正のどれへ進むべきか整理したいとき。
- `fork/` 配下の各入口の役割分担をまとめて把握したいとき。
- このディレクトリの `INDEX.md` を作成・修正する前に、下位ファイルの入口構成を確認したいとき。
- read-only の呼び出しと write-enabled の呼び出しの違いを、この階層で整理したいとき。

## Do not read this when

- すでに読む対象が `fork/INDEX.md`、`change_summary.py`、`change_summary.json`、`file_audit_finding.py`、`file_audit_finding.json`、`fixing_point_refinement.py`、`fixing_point_refinement.json`、`fixing_point_application.py` のいずれかに決まっていて、この目次を経由する必要がないとき。
- この配下の変更要約、ファイル単位監査、要修正点リスト改善、要修正点 1 件の実装修正のいずれかを単独で確認したいとき。
- Structured Output schema そのものではなく、個別の prompt 実装や JSON schema を直接読みたいとき。

## hash

- 8c4eb6235cddfb6b69693cae3effcc15f1d9e92692ac1aaf13f2ac72fdcac0f2

# `indexing`

## Summary

- ルーティング文書の目次情報を生成するための入口で、対象の内容と同階層の情報を組み合わせて案内します。
- 要約・読む条件・読まない条件の 3 項目だけを返す Structured Output を前提にしています。
- 読み取り専用で、目次文の生成と検証に向いた構成です。

## Read this when

- 目次情報を JSON でどう返すか確認したいとき。
- 対象の内容と同階層の情報をどう渡すか把握したいとき。
- ルーティング文書作成時の要約・読む条件・読まない条件の分担を整理したいとき。

## Do not read this when

- すでに目的の個別実装や対応 schema が分かっていて、ここを経由せず直接確認したいとき。
- 目次情報の markdown への反映手順だけを確認したいとき。
- ルーティング文書以外の呼び出し仕様を探しているとき。

## hash

- 3eac5e84efcf0c004b1489d9e6e06d5208a39e60a5f53697ead6ef212c5901c1

# `review`

## Summary

- この `review` ディレクトリのルーティング文書で、`oracle/` への入口です。
- `oracle/` には `enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py` と各対応 `*.json` があり、`cmoc review oracle` の 5 系統を案内します。
- 各 `*.py` は prompt 正本、各 `*.json` は対応する Structured Output schema を表します。

## Read this when

- どの review oracle 系統に進むべきか整理したいとき。
- `cmoc review oracle` の prompt 本体と Structured Output schema の対応を確認したいとき。
- 新規所見列挙、所見整理、妥当理由列挙、否定理由列挙、採否判定のどれを使うか切り分けたいとき。
- レビュー対象 oracle file と関連所見を入力に取る各フローの入口を把握したいとき。

## Do not read this when

- すでに開く対象が `enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py`、または対応する `*.json` に決まっているとき。
- 5 系統のうち 1 つだけを直接確認したいとき。
- `cmoc review oracle` 以外のサブコマンドや、レビュー用 Structured Output schema 以外の仕様を探しているとき。

## hash

- 56dddd8160803a9e42ffc8c3bd567dc1a2bfc1cc8de49598e3efe9c37cd654bc

# `session`

## Summary

- この `session` ディレクトリのルーティング文書で、`join/` への入口です。
- `join/` は `cmoc session join` の merge conflict marker 解消用 agent call parameter を案内し、`conflict_resolution.py` を正本として扱います。
- Structured Output を要求しない、ファイル編集を伴う `session join` の呼び出し仕様をまとめます。

## Read this when

- `cmoc session join` で conflict が発生したときに、Codex CLI へ何を依頼する仕様か確認したいとき。
- `build_session_join_conflict_resolution_parameter()` が組み立てる prompt と `AgentCallParameters` の所在を確認したいとき。
- conflict 解消時の禁止事項、特に `git add` と `git commit` の禁止を確認したいとき。
- この階層から `join/` へ進むべきか迷ったとき。

## Do not read this when

- `cmoc session join` 以外の session 状態管理や git 操作だけを確認したいとき。
- すでに目的のファイルが `conflict_resolution.py` だと分かっていて、この目次を経由せず直接開くとき。
- `apply`、`review`、`indexing` など別サブコマンドの agent call parameter を探しているとき。

## hash

- 5aa8592e57f9f272c613d0d9ee7c115afa795d191b6638d615c070824c3e210f
