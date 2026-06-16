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

- この `src` ディレクトリのルーティング文書で、`agent_call_parameter/`、`prompt_parts/`、`utils/` への入口です。
- `agent_call_parameter/` は `base.py` と各サブコマンド別の呼び出し仕様をまとめ、`prompt_parts/` は prompt 断片と組み立て処理をまとめます。
- `utils/` は `path_model.py`、`standard.py`、`struct_doc.py` の共通基盤をまとめます。

## Read this when

- `<cmoc-root>/oracle/src` 配下で、どのパッケージから読むべきか迷ったとき。
- `agent_call_parameter/`、`prompt_parts/`、`utils/` の役割差を整理してから、下位の `INDEX.md` や個別ファイルに進みたいとき。
- `AgentCallParameters`、`complete_prompt.py`、`StructDoc`、`RootToken` など、この階層の共通基盤や主要入口をまとめて把握したいとき。
- `<cmoc-root>` / `.<repo-root>` / `<run-root>` / `<work-root>` の解決規則、prompt 組み立て、Structured Output schema、共通ユーティリティの入口を確認したいとき。

## Do not read this when

- 読みたい対象がすでに `agent_call_parameter/`、`prompt_parts/`、`utils/` のいずれかに決まっていて、この階層の入口を経由する必要がないとき。
- `agent_call_parameter/INDEX.md`、`prompt_parts/INDEX.md`、`utils/INDEX.md` など、下位ディレクトリの目次を直接開くとき。
- `base.py`、`complete_prompt.py`、`path_model.py` など、個別ファイルをそのまま確認したいとき。
- `<work-root>/oracle/src` ではなく、`<work-root>/oracle/doc` や他のリポジトリ運用ルールだけを確認したいとき。

## hash

- ec33fa0bdaedb3f2023456bb52b25ff682e6c036c7119c15885e342942f1cb0a
