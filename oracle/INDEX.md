# `doc`

## Summary

- この `doc` ディレクトリのルーティング文書で、`app_spec/`、`considered_alternative/`、`dev_rule/`、`branch_model.md` への入口です。
- `app_spec/` では利用手順と共通仕様を、`considered_alternative/` では採用しなかった設計判断を、`dev_rule/` では開発規約を案内します。
- `branch_model.md` では cmoc の branch と worktree の関係をまとめ、各下位文書へ分岐するための起点になります。

## Read this when

- cmoc の利用方法、共通仕様、branch モデルの入口をまとめて把握したいとき。
- 採用しなかった設計案とその理由を確認したいとき。
- 実装やテストの前に、開発規約・設計方針・開発環境・テスト規約を整理したいとき。
- どの下位ディレクトリの文書や個別仕様を読むべきか迷ったとき。

## Do not read this when

- 目的の文書がすでに分かっていて、`app_spec/`、`considered_alternative/`、`dev_rule/`、`branch_model.md` の該当文書へ直接進めるとき。
- この階層ではなく、各下位ディレクトリの `INDEX.md` や個別仕様ファイルだけを確認したいとき。
- `README.md` や `AGENTS.md` など、`doc` 以外のリポジトリ運用ルールだけを確認したいとき。

## hash

- 4fedb8a4189eb2704b75fa3953023cb687403c48c8993377555f1dd08e3fc510

# `src`

## Summary

- この `src` ディレクトリのルーティング文書で、`acp/`、`basic/`、`config/` への入口です。
- `acp/` は AI コーディングエージェント呼び出しに関する仕様と prompt 構成を案内し、`basic/` は共通基盤、`config/` は cmoc 全体設定の入口を案内します。
- この階層は、cmoc の共通仕様・設定・パス解決・文書レンダリングの入口を切り分ける起点です。

## Read this when

- `<cmoc-root>/oracle/src` 配下で、まず `acp/`、`basic/`、`config/` のどれから読むべきか整理したいとき。
- `AgentCallParameters`、`ModelClass`、`ReasoningEffort`、`FileAccessMode`、`RootToken`、`Standard`、`StructDoc` など、この階層の共通基盤をまとめて把握したいとき。
- `<cmoc-root>` / `<repo-root>` / `<run-root>` / `<work-root>` の解決規則や、設定・prompt 組み立て・標準文書・markdown レンダリングの入口を確認したいとき。
- この階層の下位 `INDEX.md` や個別仕様へ進む前に、役割分担を先に整理したいとき。

## Do not read this when

- すでに `acp/`、`basic/`、`config/` のどれかに進む対象が決まっていて、この階層の入口を経由する必要がないとき。
- `acp.py`、`path_model.py`、`standard.py`、`struct_doc.py`、`cmoc_config.py` など個別ファイルを直接開いて内容を確認したいとき。
- `<cmoc-root>/oracle` 全体の別ルートや、開発規約だけを確認したいとき。

## hash

- aacb195dba29c3bc3df326d7389a35f52ae31a11feb460c01e0b90ebd8921d03
