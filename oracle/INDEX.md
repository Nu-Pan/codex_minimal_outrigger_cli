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

- 目的の文書がすでに分かっていて、`app_spec/`、`considered_alternative/`、`dev_rule/`、`branch_model.md` の該当ファイルへ直接進めるとき。
- この階層ではなく、各下位ディレクトリの `INDEX.md` や個別仕様ファイルだけを確認したいとき。
- `README.md` や `AGENTS.md` など、`doc` 以外のリポジトリ運用ルールだけを確認したいとき。

## hash

- bd7daaf6406236cd73c5a2d5fd867c66796e747ad3487bcc0072a58ac3742910

# `src`

## Summary

- この `src` ディレクトリのルーティング文書で、`agent_call_parameter/` と `utils/` への入口です。
- `agent_call_parameter/` は共通型、サブコマンド別の呼び出し仕様、prompt 断片と完全 prompt の組み立てを案内します。
- `utils/` はパス解決、標準表現、構造化文章レンダリングの共通基盤を案内します。

## Read this when

- `<cmoc-root>/oracle/src` 配下で、まず `agent_call_parameter/` と `utils/` のどちらから読むべきか整理したいとき。
- `AgentCallParameters`、`ModelClass`、`ReasoningEffort`、`FileAccessMode`、`RootToken`、`Standard`、`StructDoc` など、この階層の共通基盤をまとめて把握したいとき。
- `<cmoc-root>` / `<repo-root>` / `<run-root>` / `<work-root>` の解決規則や、prompt 組み立て・標準文書・markdown レンダリングの入口を確認したいとき。
- この階層の下位 `INDEX.md` や個別仕様へ進む前に、役割分担を先に整理したいとき。

## Do not read this when

- 読む対象がすでに `agent_call_parameter/` または `utils/` に決まっていて、この階層の入口を経由せず直接進めるとき。
- `base.py`、`builder/INDEX.md`、`prompt_parts/INDEX.md`、`path_model.py`、`standard.py`、`struct_doc.py` など、個別ファイルをそのまま確認したいとき。
- この階層の案内ではなく、`oracle` 全体の別ルートや運用規約だけを確認したいとき。

## hash

- e3011bd9b70e06113a64c3f1e9d135bd0fb75b233c00b0b01796b5a2b428a68a
