# `doc`

## Summary

- この `doc` ディレクトリのルーティング文書で、`app_spec/`、`considered_alternative/`、`dev_rule/`、`branch_model.md` への入口です。
- `app_spec/` では利用手順と共通仕様を、`considered_alternative/` では採用しなかった設計判断を、`dev_rule/` では開発規約を案内します。
- `branch_model.md` では cmoc の branch と worktree の関係をまとめ、各下位文書へ分岐するための起点になります。

## Read this when

- cmoc の利用方法、共通仕様、パス表記、branch モデルの入口をまとめて把握したいとき。
- 採用しなかった設計案とその理由を確認したいとき。
- 実装やテストの前に、コーディング規約・設計方針・開発環境・テスト規約を整理したいとき。
- どの下位ディレクトリの文書や個別仕様を読むべきか迷ったとき。

## Do not read this when

- 目的の文書がすでに分かっていて、`app_spec/`、`considered_alternative/`、`dev_rule/`、`branch_model.md` の該当ファイルへ直接進めるとき。
- この階層ではなく、各下位ディレクトリの `INDEX.md` や個別仕様ファイルだけを確認したいとき。
- `README.md` や `AGENTS.md` など、`doc` 以外のリポジトリ運用ルールだけを確認したいとき。

## hash

- 45ecdb3afe2ae6383f469c0471265a71948b301b322e4b8ac75e03e414822207

# `src`

## Summary

- この `src` ディレクトリのルーティング文書で、`agent_call_parameter/`、`agent_call_parameters/`、`utils/` への入口です。
- `agent_call_parameter/` は `base.py`、`prompt_builder/`、`apply/`、`review/` をまとめる主要パッケージです。
- `agent_call_parameters/` は `prompt_builder/` 配下の `oracles_standards.py` を案内し、`utils/` は `path_model.py`、`standard.py`、`struct_doc.py` の共通基盤をまとめます。

## Read this when

- `<work-root>/oracle/src` 配下のどのパッケージから読むべきか迷ったとき。
- `agent_call_parameter/` と `agent_call_parameters/` の役割差を整理したいとき。
- パス解決、標準定義、`StructDoc` 変換の共通基盤を探したいとき。
- `apply` / `review` / `prompt_builder` の入口をまとめて把握したいとき。

## Do not read this when

- 読みたい対象のファイルやサブディレクトリがすでに分かっていて、直接 `base.py`、`path_model.py`、`standard.py`、`struct_doc.py`、各 `INDEX.md` に進むとき。
- `<work-root>/oracle/src` 全体ではなく、個別の実装やテストだけを確認したいとき。
- すでに `agent_call_parameter/`、`agent_call_parameters/`、`utils/` のいずれかの目次に入ることが決まっているとき。

## hash

- 498ed00632205a5ed90fefdbd3706181a99c2d76ca21f9d18c508577f0bc214b
