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
- `cmoc oracle edit` における本命編集 agent call と、編集後の仕様削減 agent call の起動パラメータを構築する。
- oracle file 編集向けの共通制約、ユーザー指示、ファイルアクセス権限、作業ディレクトリ、indexing 実行条件を各 call の prompt と parameter に反映する。

## Read this when
- `cmoc oracle edit` の agent call 起動条件、2 段階の prompt 構成、または起動パラメータを変更・調査するとき。
- 本命の oracle 編集 call と、成功後に行う仕様削減 call の責務分担や共通編集制約を確認するとき。

## Do not read this when
- oracle file の編集処理そのものや、仕様削減の判断基準を変更する場合。対象の agent call が利用する prompt builder や oracle policy の定義を直接確認するとき。
- session の join・競合解決や、`cmoc oracle edit` 以外の agent call の起動処理を調べるとき。

## hash
- 19c637c880f6b5cf0b45147a1fbec63b7849264fc7e5edea4c2d4fc0d4f5104e
