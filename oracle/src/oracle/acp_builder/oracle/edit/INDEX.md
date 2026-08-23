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
- `cmoc oracle edit` における本命および仕様削減用の `codex exec` 起動パラメータを構築する定義。prompt、対象ファイルアクセスモード、モデル・推論設定、作業ディレクトリ、indexing 実行有無を定める。

## Read this when
- `cmoc oracle edit` の本命 agent call または本命成功後の仕様削減 agent call の起動条件・パラメータを確認または変更するとき。
- oracle file の編集用 prompt 構築や、仕様削減時の参照境界を確認するとき。

## Do not read this when
- oracle file の編集内容や仕様そのものを確認したいとき。
- agent call の一般的なパラメータ定義だけを確認したいときは、より直接的な共通定義を読む。

## hash
- 83d515c323b4868a58fbc846936d6db9e61736ac982dcefc8e823a2988d89e9f
