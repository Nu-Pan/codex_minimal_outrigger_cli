# `apply`

## Summary

- この `apply` ディレクトリのルーティング文書で、`fork/` への入口です。
- `fork/` では `cmoc apply fork` の変更要約、ファイル単位監査、要修正点リスト改善、要修正点 1 件の実装修正を案内します。
- `change_summary.json` と `change_summary.py` は変更要約、`file_audit_finding.json` と `file_audit_finding.py` はファイル単位監査、`fixing_point_refinement.json` と `fixing_point_refinement.py` は要修正点リスト改善、`fixing_point_application.py` は書き込み中心の実装修正の入口です。

## Read this when

- `cmoc apply fork` 配下で、変更要約・ファイル単位監査・要修正点リスト改善・要修正点 1 件の実装修正のどれへ進むべきか整理したいとき。
- `fork/` にある `change_summary.*`、`file_audit_finding.*`、`fixing_point_refinement.*`、`fixing_point_application.py` の役割分担をまとめて把握したいとき。
- この階層の `INDEX.md` を作成・修正する前に、`apply` 配下の入口構成を確認したいとき。

## Do not read this when

- すでに `cmoc apply fork` の読む対象が決まっていて、`fork/INDEX.md` や個別の `*.py` / `*.json` を直接開くとき。
- `cmoc review oracle`、`cmoc indexing`、`cmoc session join` など、`apply` 以外の agent call parameter を探しているとき。

## hash

- b9a95385118a95dede94bf29ba8db9f1862d924d95014c8bcbd396a009de27eb

# `indexing`

## Summary

- 目次情報を生成するための呼び出し仕様と Structured Output schema をまとめた入口です。
- 対象の内容と同階層の情報を受け取り、要約・読む条件・読まない条件を返す構成です。
- ルーティング文書の作成時に使う入力の組み立て方と出力の形を定義しています。

## Read this when

- 目次情報を生成するための入力と出力の形を確認したいとき。
- 対象の内容と同階層の情報をどう渡すか把握したいとき。
- 目次生成の呼び出し仕様と Structured Output schema の対応を確認したいとき。

## Do not read this when

- すでに目次情報の入力仕様と出力形式が分かっていて、細部を確認する必要がないとき。
- 別の呼び出し仕様や別のサブコマンド向けの案内を探しているとき。
- 対象の列挙やコミット処理だけを確認したいとき。

## hash

- 1f43bd1f156abe946f06fcec326d0c7dbdd65ac4f51b58981b7d5bd1b2996f3a

# `review`

## Summary

- この `review` ディレクトリのルーティング文書で、`oracles/` への入口です。
- `oracles/` には、`enumerate_finding.py/json`、`merge_finding.py/json`、`validate_finding_advocate.py/json`、`validate_finding_challenger.py/json`、`judge_finding.py/json` がまとまっています。
- `cmoc review oracle` の所見処理に使う prompt と Structured Output schema を、読み取り中心の入口として案内します。

## Read this when

- `<cmoc-root>/oracle/src/agent_call_parameter/builder/review` 配下で、どの review oracle から読むべきか迷ったとき。
- `cmoc review oracle` の所見処理フロー全体を把握し、`oracles/` 配下の入口をまとめて確認したいとき。
- 新規所見列挙、所見マージ、妥当理由列挙、否定理由列挙、採否判定のどれを使うべきか切り分けたいとき。

## Do not read this when

- すでに目的のファイル名が分かっていて、`oracles/INDEX.md` や `enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py` を直接開くとき。
- `cmoc review oracle` 以外のサブコマンドの agent call parameter を探しているとき。
- この階層ではなく、`oracles/` 配下の個別 schema や実装だけを確認したいとき。

## hash

- 17a848cba59ee909d5d3cc69687b02b57b98724563be9fb6d75c35211e00c74f

# `session`

## Summary

- この `session` ディレクトリのルーティング文書で、`join/` への入口です。
- `join/` は `cmoc session join` の merge conflict marker 解消用 agent call parameter を案内し、`conflict_resolution.py` を正本として扱います。
- Structured Output を要求しない、ファイル編集を伴う `session join` の呼び出し仕様をまとめます。

## Read this when

- `cmoc session join` で conflict 発生時に Codex CLI へ何を依頼するか確認したいとき。
- `build_session_join_conflict_resolution_parameter()` が組み立てる prompt と `AgentCallParameters` の所在を確認したいとき。
- conflict 解消時の禁止事項、特に `git add` と `git commit` の禁止を確認したいとき。
- この階層から `conflict_resolution.py` へ進むべきか迷ったとき。

## Do not read this when

- `cmoc session join` 以外の session 状態管理や git 操作だけを確認したいとき。
- すでに目的のファイルが `conflict_resolution.py` だと分かっていて、この目次を経由せず直接開くとき。
- `apply`、`review`、`indexing` など別サブコマンドの agent call parameter を探しているとき。

## hash

- 0402fb794bbf484eb267a84bf91d3c8c73ea94d4a62b121b6369c6d9eb8a1a0e
