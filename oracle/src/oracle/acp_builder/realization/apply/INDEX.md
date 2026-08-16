# `fork`

## Summary
- realization apply fork の AgentCallParameter を構築する実装。oracle file の差分、commit 範囲、linked worktree を完全 prompt に組み込み、realization file への追従作業に必要なアクセスモード、モデル、推論強度、検証方針を固定する。差分追従の起動条件や prompt 構築を確認・変更する際の入口。

## Read this when
- realization apply fork の差分追従処理を起動する AgentCallParameter、prompt の構成、commit 範囲や raw oracle diff の渡し方を確認・変更するとき。
- realization file への追従作業における worktree、アクセスモード、モデル・推論設定、indexing preflight の起動条件を確認・変更するとき。

## Do not read this when
- realization file の具体的な実装・テスト・補助ファイルの内容だけを確認するとき。
- oracle file の仕様や、一般的な AgentCallParameter の定義を直接確認するとき。

## hash
- 82a89833ccfc29887a9de54723ebacc83358699131e138ab05a3cb583bce8b3b
