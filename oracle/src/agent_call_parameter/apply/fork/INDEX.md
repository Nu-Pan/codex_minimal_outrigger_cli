# `file_audit_finding.json`

## Summary

- `cmoc apply fork` のファイル単位監査 prompt 本体と Structured Output schema への入口です。
- `file_audit_finding.py` は監査用の AI 呼び出しパラメータを構築し、`file_audit_finding.json` は返却 JSON の形を定義します。
- 監査対象ファイルを起点に、`oracle file` と `realization file` の要修正点を調べる流れを案内します。

## Read this when

- `cmoc apply fork` のファイル単位監査 prompt と、その返却 JSON schema の入口をまとめて把握したいとき。
- `file_audit_finding.py` と `file_audit_finding.json` のどちらを読むべきか迷ったとき。
- 監査対象ファイルを起点に `oracle file` / `realization file` の要修正点を調べる呼び出しパラメータ生成や、Structured Output 形式を確認したいとき。
- `apply/fork/` 配下のルーティング文書を更新・点検したいとき。

## Do not read this when

- `cmoc apply fork` のファイル単位監査 prompt 本体や Structured Output schema の場所がすでに分かっていて、`file_audit_finding.py` または `file_audit_finding.json` を直接読むとき。
- この階層ではなく、`apply/fork/` 配下の他の実装・仕様ファイルだけを個別に確認したいとき。
- `INDEX.md` の生成ルールや `oracle` 全体のルーティング方針だけを確認したいとき。

## hash

- 2e202d6b5652992666de1f176eb80ed21e5304ecc0349da3b46ee9dfd48cf4dc

# `file_audit_finding.py`

## Summary

- この `<work-root>/oracle/src/agent_call_parameter/apply/fork` ディレクトリは、`cmoc apply fork` のファイル単位監査用 agent call parameter をまとめる入口です。
- `file_audit_finding.py` では監査プロンプトと呼び出しパラメータ生成を定義し、`file_audit_finding.json` では要修正点一覧の Structured Output schema を定義します。
- ここは、調査対象ファイルを起点に oracle file と realization file の不整合や致命的問題を洗い出すための目次です。

## Read this when

- `cmoc apply fork` のファイル単位監査プロンプトや Structured Output schema を確認・修正したいとき。
- 要修正点の検出条件、`fixing_points` の構造、証拠の持ち方を確認したいとき。
- `file_audit_finding.py` と `file_audit_finding.json` のどちらを読むべきか迷ったとき。

## Do not read this when

- `cmoc apply join` や `cmoc apply abandon` など、`apply fork` 以外のフローを確認したいとき。
- 他の agent call parameter や review 用 schema を探していて、このディレクトリの内容は不要なとき。
- 監査対象の oracle file / realization file 本体や、上位の共通仕様・開発規約だけを確認したいとき。

## hash

- 1b00beaa92742d52500415397aef847a4cf54fcb8a867c1040634abb4c89bc9c
