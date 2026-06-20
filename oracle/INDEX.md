# `doc`

## Summary

- この `doc` ディレクトリのルーティング文書で、`app_spec/`、`considered_alternative/`、`dev_rule/`、`branch_model.md` への入口をまとめます。
- `app_spec/` は利用手順と共通仕様、`considered_alternative/` は採用しなかった設計判断、`dev_rule/` は開発規約への入口です。
- `branch_model.md` は cmoc の branch と worktree の関係を整理した、branch モデルの起点です。

## Read this when

- cmoc の利用手順・共通仕様・非採用案・開発規約・branch モデルを、この階層からまとめて把握したいとき。
- `app_spec/`、`considered_alternative/`、`dev_rule/`、`branch_model.md` のどこから読むべきか迷っているとき。
- 実装やテストの前に、関連する正本仕様や設計方針の入口を整理したいとき。

## Do not read this when

- `app_spec/`、`considered_alternative/`、`dev_rule/` の個別文書や `branch_model.md` の内容がすでに分かっていて、該当先へ直接進むとき。
- この階層全体ではなく、`app_spec/` 内の利用手順・共通仕様だけ、あるいは `dev_rule/` 内の開発規約だけを確認したいとき。
- `INDEX.md` の生成ルールそのものではなく、リポジトリ運用ルールや別階層の文書を探しているとき。

## hash

- 1ceddbcd647a2976f9ba92598d30f3a2de3705c0516e72f6ebc2e4a4c1102c78

# `src`

## Summary

- この `src` ディレクトリのルーティング文書で、`acp/`、`basic/`、`config/` への入口です。
- `acp/` は AI コーディングエージェント呼び出しに関する仕様と prompt 構成を案内し、`basic/` は共通基盤、`config/` は cmoc 全体設定の入口を案内します。
- この階層は、cmoc の共通仕様・設定・パス解決・文書レンダリングの入口を切り分ける起点です。

## Read this when

- `<cmoc-root>/oracle/src` 配下で、まず `acp/`、`basic/`、`config/` のどこから読むべきか整理したいとき。
- `AgentCallParameter`、`ModelClass`、`ReasoningEffort`、`FileAccessMode`、`RootToken`、`Standard`、`StructDoc` など、この階層の共通基盤をまとめて把握したいとき。
- `<cmoc-root>` / `<repo-root>` / `<run-root>` / `<work-root>` の解決規則や、設定・prompt 組み立て・標準文書・markdown レンダリングの入口を確認したいとき。
- この階層の下位 `INDEX.md` や個別仕様へ進む前に、役割分担を先に整理したいとき。

## Do not read this when

- すでに `acp/`、`basic/`、`config/` のどれに進むか決まっていて、この階層の入口を経由する必要がないとき。
- `acp.py`、`path_model.py`、`standard.py`、`struct_doc.py`、`cmoc_config.py` などの個別ファイルを直接確認したいとき。
- `<cmoc-root>/oracle/src` ではなく、`<cmoc-root>/oracle` 全体の別ルートや開発規約だけを確認したいとき。

## hash

- 76efd6981d32138811e4e7e5768b9fd88d778404adf7005ce32afa3a652a47c2
