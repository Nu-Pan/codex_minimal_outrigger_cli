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
- `cmoc oracle edit` が起動する本命 agent と仕様削減 agent の `codex exec` パラメータを構築する。オリジナル指示を prompt に埋め込み、oracle file の編集権限、作業ルート、モデル、推論強度、初回 indexing 実行有無などを固定する。
- oracle 編集処理の起動条件・prompt 構成・agent call パラメータを確認または変更するときの入口であり、実際の prompt 生成規則は `build_complete_prompt`、パス解決は `AgentCallPathContext` と `resolve_repo_root` を確認する。

## Read this when
- `cmoc oracle edit` の本命または仕様削減 agent call の起動パラメータを調査・変更するとき
- oracle file 編集用 prompt に渡すユーザー指示、ファイルアクセスモード、作業ディレクトリ、実行前 indexing の設定を確認するとき

## Do not read this when
- oracle file 編集用 prompt の共通構造だけを確認したい場合は `complete_prompt` 側を直接読むとよい
- agent call の基本的な型や enum の定義を確認したい場合は `oracle.acp_builder.basic` を直接読むとよい
- oracle file の編集対象や仕様そのものを確認する場合は、この起動パラメータ定義ではなく対象の oracle file を読むべきである

## hash
- 5dc5d5a714987cd5b72f164731d77aaf54f9c6f660c7cab2f1223a575765adf5
