# `fork`

## Summary
- 対象ディレクトリは、`cmoc realization apply fork` における realization 追従処理の起動パラメータ構築を担う実装入口です。oracle file の差分や対象コミット範囲、linked worktree の情報を codex exec 用の完全なプロンプトと AgentCallParameter に組み立てます。
- 配下の実装を確認すると、fork 起動時の prompt 生成・実行設定・関連する補助ロジックを把握するための入口として機能します。

## Read this when
- `cmoc realization apply fork` が realization 追従用 AgentCallParameter や codex exec prompt をどのように構築するか確認したいとき。
- oracle file の変更差分、対象コミット範囲、linked worktree 情報が完全な追従プロンプトへ組み込まれる流れを調べたいとき。
- fork 起動時に指定される実行モデル、推論設定、ファイルアクセス権限などの対応関係を確認したいとき。

## Do not read this when
- `cmoc realization apply fork` 以外の用途における prompt 構築を調べるときは、各用途に対応する prompt builder を直接確認してください。
- realization file の具体的な変更処理や、その処理を検証するテスト内容を確認したいときは、対応する realization implementation または realization test を直接確認してください。

## hash
- 18abf661a7dd926af2851f35ea535356b19c169fb7269b375ea3c1d44e3f3b0c
