# `apply`

## Summary

- この `apply` ディレクトリのルーティング文書で、`fork/` への入口をまとめます。
- `fork/` は `cmoc apply fork` の変更要約、ファイル単位所見列挙、所見 1 件の実装修正、所見リスト改善を案内します。
- この階層は、`cmoc apply fork` の入口を整理する起点です。

## Read this when

- `<cmoc-root>/oracle/src/acp/builder/apply` 配下で、まず `fork/` のどこから読むべきか整理したいとき。
- `cmoc apply fork` の変更要約、ファイル単位所見列挙、所見 1 件の実装修正、所見リスト改善という役割分担をまとめて把握したいとき。
- この階層の入口を確認してから、下位の `INDEX.md` や個別仕様へ進みたいとき。

## Do not read this when

- すでに `fork/` に進むことが決まっていて、この階層の案内を経由する必要がないとき。
- `change_summary.py`、`file_finding_enumeration.py`、`finding_application.py`、`refine_finding.py` など、`cmoc apply fork` の個別ファイルを直接確認したいとき。
- `INDEX.md` の目次情報ではなく、個別の prompt 実装や Structured Output schema そのものを探しているとき。

## hash

- cb6702b62db86b3347fca734b6e17b4452c485dfea50869db207aa66fe40a7fd

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

- この `review` ディレクトリのルーティング文書で、`oracle/` への入口をまとめます。
- `oracle/` は `cmoc review oracle` の 5 系統を案内し、新規所見列挙、所見整理、妥当理由列挙、否定理由列挙、採否判定を切り分けます。
- 各 `*.py` は prompt 正本、各 `*.json` は対応する Structured Output schema です。

## Read this when

- `<cmoc-root>/oracle/src/acp/builder/review` 配下で、まず `oracle/` のどこから読むべきか整理したいとき。
- `enumerate_finding.py`、`merge_finding.py`、`validate_finding_advocate.py`、`validate_finding_challenger.py`、`judge_finding.py` の役割分担をひとまとめに把握したいとき。
- 各 `*.py` が prompt 正本で、各 `*.json` が対応する Structured Output schema である対応関係を確認したいとき。

## Do not read this when

- すでに `oracle/` の 5 系統のいずれか、または対応する `*.py` / `*.json` を直接確認する対象が決まっていて、この目次を経由する必要がないとき。
- `cmoc review oracle` のうち 1 つの処理だけを直接見たいとき。
- レビュー用 Structured Output schema ではなく、`cmoc review` の個別実装や別サブコマンドの仕様を探しているとき。

## hash

- 1f44605bcec2f53a34070ccade660845bb6f959934cce5af5adcfb8ed0fd8fae

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
