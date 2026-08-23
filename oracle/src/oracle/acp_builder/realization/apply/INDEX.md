# `fork`

## Summary
- `launch_exec.py` は、`cmoc realization apply fork` の一回の Agent call に必要な prompt と `AgentCallParameter` を構築する起動定義である。commit 範囲、oracle file の raw git diff、linked worktree を構造化して prompt に渡し、リポジトリ全体の realization file を oracle file の変更へ追従させる実行方針と完了条件を固定する。

## Read this when
- `realization apply fork` の Agent call に渡す commit 範囲、oracle diff、linked worktree の組み立て方を確認・変更するとき。
- prompt に埋め込む realization 追従方針、oracle/realization/routing policy、realization write 権限を確認するとき。
- 起動時のモデル品質、推論強度、作業ディレクトリ、indexing preflight などの `AgentCallParameter` 設定を確認するとき。

## Do not read this when
- prompt 生成の共通部品や構造化ドキュメントの仕様だけを調べるときは、`build_complete_prompt` や `struct_doc` の定義を直接読む。
- `realization apply fork` 以外の apply 経路、個別の realization implementation・test・ancillary の挙動を調べるときは、各対象を直接読む。
- oracle file の変更内容や repository 共通の開発ルールだけを確認するときは、該当する oracle file・開発規約を直接読む。

## hash
- fc6256c425f86b933f6c0fbca0913ec876cf2c6a5580493a5d7d347304131265
