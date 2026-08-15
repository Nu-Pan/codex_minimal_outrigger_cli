# `fork`

## Summary
- 現時点で本文ファイルを含まない空のディレクトリです。

## Read this when
- このディレクトリにファイルが追加され、その内容や用途を確認する必要があるとき。

## Do not read this when
- このディレクトリ配下の具体的なファイルを直接確認できる場合。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `launch_exec.py`

## Summary
- 対象は `cmoc oracle edit` 用に起動する2回の `codex exec` の固定パラメータを構築する実装です。初回の本命編集呼び出しでは、ユーザー指示を埋め込んだ完全 prompt を生成してログへ保存し、oracle 専用書き込み・最大推論・インデックス事前処理などの起動条件を設定します。成功後の仕様削減呼び出しでは、現在の oracle と未コミット差分を根拠に仕様削減を依頼する prompt と同じ oracle 専用の起動条件を構築します。oracle 編集起動の設定や、2段階の編集・削減フローのパラメータを変更・確認するときの入口です。

## Read this when
- `cmoc oracle edit` の本命 agent call または成功後の仕様削減 agent call の起動パラメータを変更・確認するとき。
- ユーザー指示、oracle 専用ファイルアクセス、完全 prompt の保存、推論設定、インデックス事前処理の組み合わせを確認するとき。
- oracle 編集処理の2段階フローにおける起動定義の責務を調査するとき。

## Do not read this when
- oracle file の具体的な編集規則や正本仕様そのものを確認したいときは、関連する oracle file を直接読む。
- `codex exec` の一般的な実行機構や共通データ型を確認したいときは、この対象ではなく `AgentCallParameter`、prompt builder、または関連する共通実装を直接読む。
- INDEX.md の生成・更新方法だけを確認したいとき。

## hash
- a7a2f94a39c0d9bd8f4bcba298cdf21cf410bd275a658aa157a4902d3e145ce5
