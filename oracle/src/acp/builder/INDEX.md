# `apply`

## Summary

- この `fork` ディレクトリのルーティング文書で、`change_summary.*`、`file_audit_finding.*`、`fixing_point_refinement.*`、`fixing_point_application.py` への入口です。
- `change_summary.*` は変更要約、`file_audit_finding.*` はファイル単位監査、`fixing_point_refinement.*` は要修正点リスト改善、`fixing_point_application.py` は要修正点 1 件の実装修正を案内します。
- `fixing_point_application.py` は Structured Output を使わない write-enabled な入口で、他の 3 系統は Structured Output schema を伴う read-only な入口です。

## Read this when

- `cmoc apply fork` 配下で、変更要約・ファイル単位監査・要修正点リスト改善・要修正点 1 件の実装修正のどれへ進むべきか整理したいとき。
- `change_summary.*`、`file_audit_finding.*`、`fixing_point_refinement.*`、`fixing_point_application.py` の役割分担をまとめて把握したいとき。
- このディレクトリの `INDEX.md` を作成・修正する前に、下位ファイルの入口構成を確認したいとき。
- read-only の呼び出しと write-enabled の呼び出しの違いを、この階層で整理したいとき。

## Do not read this when

- すでに読む対象が `fork/INDEX.md`、`change_summary.py`、`change_summary.json`、`file_audit_finding.py`、`file_audit_finding.json`、`fixing_point_refinement.py`、`fixing_point_refinement.json`、`fixing_point_application.py` のいずれかに決まっていて、この目次を経由する必要がないとき。
- `cmoc apply fork` のうち、変更要約、ファイル単位監査、要修正点リスト改善、要修正点 1 件の実装修正のどれか一つだけを直接確認したいとき。
- Structured Output schema そのものではなく、個別の prompt 実装や JSON schema を直接読みたいとき。
- `cmoc review oracle`、`cmoc indexing`、`cmoc session join` など、別系統の agent call parameter を探しているとき。

## hash

- 641b4c737bdaac01d74c452293a892e28d3546b1f7cf1e1a035dc631c33328ed

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

- 79403c3adc61b12fd6f788ac96b00815a4d01c3011860c9a36e8cc3470531b08

# `review`

## Summary

- この `oracles` ディレクトリのルーティング文書で、`enumerate_finding.py/json`、`merge_finding.py/json`、`validate_finding_advocate.py/json`、`validate_finding_challenger.py/json`、`judge_finding.py/json` への入口です。
- 新規所見の列挙、所見リストの整理、妥当理由の列挙、否定理由の列挙、採否判定の 5 系統を案内します。
- いずれも `cmoc review oracle` の所見処理に使う、読み取り中心の prompt と Structured Output schema の対応をまとめます。

## Read this when

- `cmoc review oracle` の所見処理フロー全体をまとめて把握したいとき。
- 新規所見列挙、所見マージ、擁護理由列挙、否定理由列挙、採否判定のどれを使うべきか迷ったとき。
- `oracles/` 配下の Python 実装と JSON schema の対応関係を確認したいとき。
- 各所見処理が返す JSON 形式や入力前提を確認したいとき。

## Do not read this when

- すでに目的のファイル名が分かっていて、`enumerate_finding.py`、`enumerate_finding.json`、`merge_finding.py`、`merge_finding.json`、`validate_finding_advocate.py`、`validate_finding_advocate.json`、`validate_finding_challenger.py`、`validate_finding_challenger.json`、`judge_finding.py`、`judge_finding.json` を直接開くとき。
- `cmoc review oracle` 以外のサブコマンドの agent call parameter を探しているとき。
- 所見の列挙、統合、擁護理由列挙、否定理由列挙、採否判定のどれか 1 つだけを個別に確認したいとき。
- Structured Output schema ではなく、このディレクトリ配下の実装コードだけを確認したいとき。

## hash

- f38e2ff8c61fb36b1a79991ee3a18e980b53ed66bae7af3b76bfe8d3c791a051

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

- f60f4c305fc4af498505c7ff8c8abdca7c19e7e05fe2ef99adb8521abebbde6b
