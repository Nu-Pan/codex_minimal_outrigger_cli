# `doc`

## Summary

- この `doc` ディレクトリのルーティング文書で、`app_spec/`、`considered_alternative/`、`dev_rule/`、`branch_model.md` への入口をまとめます。
- `app_spec/` は利用手順と共通仕様、`considered_alternative/` は採用しなかった設計判断、`dev_rule/` は開発規約への入口です。
- `branch_model.md` は cmoc の branch と worktree の関係を整理した、branch モデルの起点です。

## Read this when

- cmoc の利用手順、非採用案、開発規約、branch モデルをこの階層からまとめて把握したいとき。
- `app_spec/`、`considered_alternative/`、`dev_rule/`、`branch_model.md` のどこから読むべきか迷っているとき。
- 実装やテストの前に、関連する正本仕様や設計方針の入口を整理したいとき。

## Do not read this when

- `app_spec/`、`considered_alternative/`、`dev_rule/`、`branch_model.md` の個別文書へ進む先がすでに決まっていて、この階層の案内が不要なとき。
- `app_spec/` 内の利用手順や共通仕様だけ、`considered_alternative/` 内の非採用案だけ、`dev_rule/` 内の開発規約だけを確認したいとき。
- この階層全体ではなく、`oracle` の別階層や上位のルーティング文書を探しているとき。

## hash

- 6419f9517ec4dcd514f3522917ce4b064c3cb785f544cffdc87cdece0ba8c17a

# `src`

## Summary

- この `src` ディレクトリのルーティング文書で、`acp/`、`basic/`、`config/` への入口をまとめます。
- `acp/` は AI コーディングエージェント呼び出しに関する仕様と prompt 断片群、`basic/` は共通基盤、`config/` は cmoc 全体設定の入口です。
- この階層は、cmoc の共通仕様・設定・パス解決・文書レンダリングの入口を切り分ける起点です。

## Read this when

- `<cmoc-root>/oracle/src` 配下で、まず `acp/`、`basic/`、`config/` のどこから読むべきか整理したいとき。
- `ModelClass`、`ReasoningEffort`、`FileAccessMode`、`AgentCallParameter`、`RootToken`、`Standard`、`StructDoc` など、この階層の共通基盤をまとめて把握したいとき。
- `<cmoc-root>` / `<repo-root>` / `<run-root>` / `<work-root>` の解決規則や、設定・prompt 組み立て・標準文書・Markdown レンダリングの入口を確認したいとき。
- 下位の `INDEX.md` や個別仕様へ進む前に、この階層の役割分担を先に整理したいとき。

## Do not read this when

- `acp/`、`basic/`、`config/` のうち、読む先がすでに決まっていて、この階層の入口説明が不要なとき。
- `acp.py`、`path_model.py`、`standard.py`、`struct_doc.py`、`cmoc_config.py` など、個別ファイルを直接確認したいとき。
- `<cmoc-root>/oracle/src` ではなく、`oracle` 全体の別ルートや別階層の仕様だけを探しているとき。

## hash

- 053965b0bd9a2d1e78047db8cf1779516aaeb8ca26ed7d52366e1597c8fa1aa6
