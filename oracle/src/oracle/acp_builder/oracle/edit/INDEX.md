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
- `cmoc oracle edit` における本命・仕様削減の 2 回の `codex exec` 起動パラメータを構築する。
- ユーザー指示を共通の参照情報として完全 prompt に組み込み、oracle file 専用の編集境界、モデル、推論強度、作業ディレクトリ、indexing preflight を固定する。
- 本命用は初回 indexing preflight を実行し、仕様削減用は現在の oracle file と Git 未コミット差分だけを根拠にして preflight を再実行しない。

## Read this when
- `cmoc oracle edit` の agent call 起動パラメータを変更または確認するとき。
- 本命 agent call と、その成功後に行う仕様削減 agent call の prompt 構築・編集境界・実行条件を確認するとき。
- oracle file の編集専用パラメータ、リポジトリルートの確定、または indexing preflight の設定を確認するとき。

## Do not read this when
- 一般的な ACP のパラメータ型や列挙値だけを確認するときは、`oracle.acp_builder.basic` を直接読む。
- prompt の共通構築規則だけを確認するときは、`oracle.prompt_builder.complete_prompt` を直接読む。
- oracle file の編集内容や仕様そのものを確認するときは、この起動パラメータ定義ではなく対象の oracle file を直接読む。

## hash
- f12a30d1652e661701f213bacddf4795df591aa840030f708df4dbcb09748c22
