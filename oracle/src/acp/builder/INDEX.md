# `apply`

## Summary

- この `apply` ディレクトリのルーティング文書で、`fork/` への入口です。
- `fork/` では変更要約、ファイル単位監査、要修正点リスト改善、要修正点 1 件の実装修正を案内します。
- `fork/` 配下には read-only の Structured Output 系と、write-enabled な実装修正系の入口があります。

## Read this when

- `cmoc apply fork` 配下で、変更要約・ファイル単位監査・要修正点リスト改善・要修正点 1 件の実装修正のどれへ進むべきか整理したいとき。
- `fork/` 配下の各入口の役割分担をまとめて把握したいとき。
- このディレクトリの `INDEX.md` を作成・修正する前に、下位ファイルの入口構成を確認したいとき。
- read-only の呼び出しと write-enabled の呼び出しの違いを、この階層で整理したいとき。

## Do not read this when

- すでに読む対象が `fork/INDEX.md`、`change_summary.py`、`change_summary.json`、`file_audit_finding.py`、`file_audit_finding.json`、`fixing_point_refinement.py`、`fixing_point_refinement.json`、`fixing_point_application.py` のいずれかに決まっていて、この目次を経由する必要がないとき。
- `cmoc apply fork` のうち、変更要約、ファイル単位監査、要修正点リスト改善、要修正点 1 件の実装修正のどれか一つだけを直接確認したいとき。
- Structured Output schema そのものではなく、個別の prompt 実装や JSON schema を直接読みたいとき。
- `cmoc review oracle`、`cmoc indexing`、`cmoc session join` など、別系統の agent call parameter を探しているとき。

## hash

- c75d1ba9b5afb7d4f7ed3c0d5fa99ff5df5a568947ff535f59815f54a7c1964b

# `indexing`

## Summary

- このディレクトリの目次情報生成用の入口で、`index_entry.py` と `index_entry.json` を案内する。
- 対象パスの内容と同階層の情報を受け取り、`summary`、`read_this_when`、`do_not_read_this_when` を返す構成である。
- ルーティング文書を作るための入力の組み立て方と Structured Output schema をまとめている。

## Read this when

- 目次情報を生成するための入力と出力の形を確認したいとき。
- 対象の内容と同階層の情報をどう渡すか把握したいとき。
- `index_entry.py` と `index_entry.json` の対応関係を確認したいとき。
- ルーティング文書の作成時に使う要約・読む条件・読まない条件の構成を整理したいとき。

## Do not read this when

- `cmoc indexing` の目次情報生成仕様ではなく、別のサブコマンドや別の呼び出し仕様を探しているとき。
- すでに `index_entry.py` と `index_entry.json` を直接確認する目的が決まっているとき。
- Structured Output の出力形式ではなく、この階層の実装コードだけを確認したいとき。
- 対象の列挙やコミット処理だけを確認したいとき。

## hash

- c304ded8dfdd84fcd44a1fc9b64bb89625d1873eb4c3b61d7b00f3639eedc2f7

# `review`

## Summary

- この `review` ディレクトリのルーティング文書で、`oracles/` への入口です。
- `oracles/` には `enumerate_finding`、`merge_finding`、`validate_finding_advocate`、`validate_finding_challenger`、`judge_finding` の 5 系統があり、それぞれの prompt と対応 schema を案内します。
- 各 `.py` は prompt 正本、各 `.json` は対応する Structured Output schema を表す、読み取り中心の入口です。

## Read this when

- `cmoc review oracle` のレビュー用 oracle 群で、どの prompt 本体や schema に進むべきかを整理したいとき。
- 新規所見列挙、所見マージ、所見が妥当である理由の列挙、所見が妥当ではない理由の列挙、採否判定のどれを使うかを切り分けたいとき。
- 各 `.py` が参照する対応 `.json` の Structured Output schema を確認したいとき。

## Do not read this when

- すでに読む対象の `enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py`、または各 `.json` が決まっていて、この目次を経由せず直接開くとき。
- 新規所見列挙・所見マージ・妥当理由列挙・否定理由列挙・採否判定のうち、特定の 1 本だけを個別に確認したいとき。
- `cmoc review oracle` 以外のサブコマンドや、レビュー用 Structured Output schema 以外の仕様を探しているとき。

## hash

- 95d950c66b5d74a8e19984d134d24b81a2dfaf50cb7ec21ae148285cad35f09d

# `session`

## Summary

- この `session` ディレクトリのルーティング文書で、`join/` への入口です。
- `join/` は `cmoc session join` の merge conflict marker 解消用 agent call parameter を案内し、`conflict_resolution.py` を正本として扱います。
- Structured Output を要求しない、ファイル編集を伴う `session join` の呼び出し仕様をまとめます。

## Read this when

- `cmoc session join` で conflict が発生したときに、Codex CLI へ何を依頼する仕様かを把握したいとき。
- `build_session_join_conflict_resolution_parameter()` が組み立てる prompt と `AgentCallParameters` の所在を確認したいとき。
- conflict 解消時の禁止事項、特に `git add` と `git commit` の禁止を確認したいとき。
- この階層から `join/` へ進むべきか迷ったとき。

## Do not read this when

- すでに `cmoc session join` の conflict 解消用 prompt 仕様が分かっていて、`join/INDEX.md` や `conflict_resolution.py` を直接確認するとき。
- `cmoc session join` 以外の session 状態管理や git 操作だけを確認したいとき。
- `apply`、`review`、`indexing` など別サブコマンドの agent call parameter を探しているとき。

## hash

- 7679e03d4cfc90e841f483079836f59f23bb5a0ae49195a4cc72f11962960fa8
