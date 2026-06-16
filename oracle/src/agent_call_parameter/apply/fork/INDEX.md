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

- `cmoc apply fork` のファイル単位監査用 agent call parameter を構築する入口です。
- `build_apply_fork_file_audit_parameter()` が監査対象パスから prompt と `AgentCallParameters` を生成し、返却先の Structured Output schema は隣接する `file_audit_finding.json` です。
- 監査対象ファイルを起点に、oracle file と realization file の不整合や致命的問題を洗い出すための正本です。

## Read this when

- `cmoc apply fork` のファイル単位監査 prompt や呼び出しパラメータの組み立てを確認・修正したいとき。
- `target_path` を起点にどのモデル・推論強度・Structured Output schema が使われるか追いたいとき。
- `file_audit_finding.py` と `file_audit_finding.json` のどちらを開くべきか迷ったとき。

## Do not read this when

- `cmoc apply join` や `cmoc apply abandon` など、`apply fork` 以外のフローを確認したいとき。
- すでに目的の関数や schema 名が分かっていて、直接 `file_audit_finding.py` または `file_audit_finding.json` を確認するとき。
- oracle 全体の共通規約や `INDEX.md` 生成ルールだけを確認したいとき。

## hash

- 414fa61b13f8e62dc6b73dfd2a1ac452adf936bf97a9aa18d0a000a31439511c
