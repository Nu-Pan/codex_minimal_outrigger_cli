# `launch_exec.py`

## Summary
- `cmoc realization apply fork` 実行時に、差分追従用 AgentCallParameter と完全 prompt を構築する定義。commit 範囲と oracle file の raw git diff を追従対象として組み込み、run worktree を作業ディレクトリに設定する。
- realization file への変更、oracle file 非変更、関連する実装・テスト・補助ファイルの整合性確認を完了条件とする agent call のモデル、推論強度、アクセスモード、インデックス事前処理などの起動設定も定める。

## Read this when
- `cmoc realization apply fork` の launch exec パラメータや prompt 構築を変更・確認するとき。
- oracle の変更を realization 全体へ追従させる agent call の作業範囲、完了条件、起動設定を確認するとき。

## Do not read this when
- `cmoc realization apply fork` 以外のコマンドの prompt 構築を確認するとき。
- 実際の realization 追従処理、個別の oracle・realization ファイル、または一般的な AgentCallParameter の仕様を直接確認するとき。

## hash
- ddc01c61d3643203ef6d40b83aba454a29a73df145fee5d4b849b065b3ea0790
