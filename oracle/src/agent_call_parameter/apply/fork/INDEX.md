# `file_audit_finding.json`

## Summary

- `cmoc apply fork` のファイル単位監査 prompt 本体と Structured Output schema への入口です。
- `file_audit_finding.py` は監査用の AI 呼び出しパラメータを構築し、`file_audit_finding.json` は返却 JSON の形を定義します。
- 監査対象ファイルを起点に、`oracle file` と `realization file` の要修正点を調べる流れを案内します。

## Read this when

- `cmoc apply fork` のファイル単位監査で返却 JSON schema の入口をまとめて把握したいとき。
- `file_audit_finding.py` と `file_audit_finding.json` のどちらを読むべきか迷ったとき。
- 監査対象ファイルを起点に `oracle file` / `realization file` の要修正点を調べる入出力形式を確認したいとき。
- `apply/fork/` 配下のルーティング文書を追加・修正する前に、schema の役割分担を整理したいとき。

## Do not read this when

- `cmoc apply fork` のファイル単位監査 prompt 本体や返却 JSON schema の場所がすでに分かっていて、`file_audit_finding.py` または `file_audit_finding.json` を直接読むとき。
- この階層ではなく、`apply/fork/` 配下の他の実装・仕様ファイルだけを個別に確認したいとき。
- `INDEX.md` の生成ルールや `oracle` 全体のルーティング方針だけを確認したいとき。

## hash

- 6a83530f560f906540f4ab6d567b848a2f864dfb1d02e5cfd6aa08826c37752a

# `file_audit_finding.py`

## Summary

- `cmoc apply fork` のファイル単位監査用 agent call parameter を構築する `file_audit_finding.py` への入口です。
- 隣接する `file_audit_finding.json` は、返却 JSON の形を定義する Structured Output schema です。
- `target_path` を起点に、`oracle file` と `realization file` の不整合や致命的問題を洗い出す流れを案内します。

## Read this when

- `build_apply_fork_file_audit_parameter()` がどのように prompt と `AgentCallParameters` を組み立てるか確認したいとき。
- `target_path` を起点に、どのモデル・推論強度・Structured Output schema が使われるか追いたいとき。
- `file_audit_finding.py` と隣接する `file_audit_finding.json` のどちらを先に読むべきか迷ったとき。

## Do not read this when

- `cmoc apply fork` の実行手順や、`apply` の他サブコマンドの仕様だけを確認したいとき。
- すでに目的の関数や schema 名が分かっていて、`file_audit_finding.py` または `file_audit_finding.json` を直接確認するとき。
- `oracle` 全体の共通ルールや、`INDEX.md` の生成方針だけを確認したいとき。

## hash

- fea481114415f91469ac6eeddab6763a8fd1e9c8cbd300d5edec35009de5f77a
