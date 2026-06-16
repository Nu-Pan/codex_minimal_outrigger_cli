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

- この `src` ディレクトリのルーティング文書で、`agent_call_parameter/` と `utils/` への入口です。
- `agent_call_parameter/` は `base.py`、`prompt_builder/`、`apply/`、`review/` をまとめる主要パッケージです。
- `utils/` は `path_model.py`、`standard.py`、`struct_doc.py` の共通基盤をまとめます。

## Read this when

- `<cmoc-root>/oracle/src` 配下のどのパッケージから読むべきか迷ったとき。
- `agent_call_parameter/` と `utils/` の役割差を整理したいとき。
- `AgentCallParameters`、`ModelClass`、`ReasoningEffort`、prompt builder、`apply` / `review` の入口をまとめて把握したいとき。
- `<cmoc-root>` / `<repo-root>` / `<run-root>` / `<work-root>` の解決規則や、`StructDoc` と標準定義の共通基盤を確認したいとき。

## Do not read this when

- 読みたい対象のファイルやサブディレクトリがすでに分かっていて、`base.py`、`path_model.py`、`standard.py`、`struct_doc.py`、各 `INDEX.md` を直接開くとき。
- `<work-root>/oracle/src` 全体ではなく、`agent_call_parameter/` や `utils/` の個別実装だけを確認したいとき。
- すでに `agent_call_parameter/` か `utils/` のどちらへ進むか決まっていて、この階層の入口を経由する必要がないとき。

## hash

- 03fe23c1264a0d88113c1f16773e4547a635f5c101c212edb7f321c8e9fb0caf
