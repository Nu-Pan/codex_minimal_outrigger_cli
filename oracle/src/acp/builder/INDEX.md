# `apply`

## Summary

- この `fork` ディレクトリのルーティング文書で、`change_summary.py`、`file_audit_finding.py`、`refine_fixing_point.py`、`consume_fixing_point.py` への入口です。
- `change_summary.py` は `change_summary.json` を使う変更要約、`file_audit_finding.py` は `finding_list.json` を使うファイル監査、`refine_fixing_point.py` は同じく `finding_list.json` を使う要修正点リスト改善を案内します。
- `consume_fixing_point.py` は要修正点 1 件を受け取って realization file を修正する write-enabled な入口です。

## Read this when

- `cmoc apply fork` 配下で、変更要約・ファイル単位監査・要修正点リスト改善・要修正点 1 件の実装修正のどれへ進むか整理したいとき。
- `change_summary.py`、`file_audit_finding.py`、`refine_fixing_point.py`、`consume_fixing_point.py` の役割分担を把握したいとき。
- read-only の Structured Output 系と write-enabled な実装修正系の違いを、この階層で確認したいとき。
- `file_audit_finding.py` と `refine_fixing_point.py` が共通参照する `finding_list.json` を含め、出力先 schema の対応を押さえたいとき。

## Do not read this when

- すでに対象が `change_summary.py`、`change_summary.json`、`file_audit_finding.py`、`finding_list.json`、`refine_fixing_point.py`、`consume_fixing_point.py` のいずれかに決まっていて、この目次を経由する必要がないとき。
- `cmoc apply fork` のうち、変更要約、ファイル単位監査、要修正点リスト改善、要修正点 1 件の実装修正のいずれかを単独で確認したいとき。
- Structured Output schema そのものではなく、個別の prompt 実装や JSON schema を直接読みたいとき。

## hash

- 320daa3f9d85d9c18f3bac1a04b446de54c07bd17f4812d0e3b5cd0ba14d88dd

# `indexing`

## Summary

- この `indexing` ディレクトリのルーティング文書で、`index_entry.py` と `index_entry.json` への入口です。
- `index_entry.py` は `cmoc indexing` の目次情報生成呼び出しの入口で、対象パスを正規化して complete prompt を組み立てます。
- `index_entry.json` は `INDEX.md` 用の目次情報を表す Structured Output schema です。

## Read this when

- ルーティング文書の目次情報を JSON でどう返すか確認したいとき。
- 対象内容と同階層の情報をどう組み合わせて案内するか把握したいとき。
- `cmoc indexing` の出力 schema と、その生成呼び出しの入口を整理したいとき。

## Do not read this when

- すでに対象が `index_entry.py` か `index_entry.json` に決まっていて、この目次を経由せず直接確認したいとき。
- `INDEX.md` への反映手順や markdown レンダリング方法だけを確認したいとき。
- `cmoc indexing` 以外のサブコマンドや、別の Structured Output schema を探しているとき。

## hash

- 960ee4d6fc9f1af66a665095088a13880ae61d9178aef7ab2ce9de164c4d564e

# `review`

## Summary

- この `review` ディレクトリのルーティング文書で、`oracle/` への入口です。
- `oracle/` には `enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py` と各対応 `*.json` があり、`cmoc review oracle` の 5 系統を案内します。
- 各 `*.py` は prompt 正本、各 `*.json` は対応する Structured Output schema を表します。

## Read this when

- `cmoc review oracle` の 5 系統の入口をひとまとめに把握したいとき。
- `enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py` のどれが何を担当するか整理したいとき。
- 各 `*.py` が prompt 正本で、各 `*.json` が対応する Structured Output schema である対応関係を確認したいとき。
- 新規所見列挙、所見整理、妥当理由列挙、否定理由列挙、採否判定のどこから読むべきか迷ったとき。

## Do not read this when

- すでに `enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py`、または対応する `*.json` を直接確認する目的が決まっていて、この目次を経由する必要がないとき。
- 5 系統のうち 1 つだけを直接確認したいとき。
- `cmoc review oracle` 以外のサブコマンドや、レビュー用 Structured Output schema 以外の仕様を探しているとき。
- 所見の列挙、整理、擁護理由列挙、否定理由列挙、採否判定のいずれにも当てはまらない文書を探しているとき。

## hash

- b386670446a404ac9292008c76c7c3e0187041be21ae1331b4f4a2c2da4e11cc

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

- 123ff5f31327b641c8bc893dbb702eb5bcc841dd99b6781b6d07c6f7f59932d1
