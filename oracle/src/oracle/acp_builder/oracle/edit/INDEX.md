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
- `cmoc oracle edit` が起動する本命編集 agent call と、成功後の仕様削減 agent call の `codex exec` 固定パラメータを構築する入口。
- 各起動で、完全 prompt、oracle 専用のファイルアクセスモード、作業ディレクトリ、indexing preflight の実行有無を定義する。

## Read this when
- `cmoc oracle edit` の agent call 起動条件、prompt 構成、oracle 編集権限、または本命後の仕様削減処理を確認・変更するとき。
- 本命起動と仕様削減起動で異なる preflight 設定や参照情報の渡し方を調べるとき。

## Do not read this when
- oracle file の具体的な編集内容や仕様削減の判断基準を確認したい場合は、実際に編集対象となる oracle file を直接読む。
- 一般的な agent call パラメータや共通 prompt 構築の仕様を確認したい場合は、対応する共通 builder や型定義を直接読む。

## hash
- e473d7bb0df4c1b7a0fae1dfb97f78be78fe482247134bf26195dee63ca0b4e5
