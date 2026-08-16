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
- `cmoc oracle edit` における本命および仕様削減の2回の `codex exec` 起動パラメータを構築する定義。完全 prompt、ファイルアクセス範囲、モデル・推論設定、作業ディレクトリ、索引事前処理の有無をそれぞれ固定する。oracle edit の起動条件や prompt 構成、oracle file の編集権限・実行方針を確認する際の入口となる。

## Read this when
- `cmoc oracle edit` の本命 agent call または本命成功後の仕様削減 agent call の起動パラメータを変更・レビューするとき
- oracle file 編集用 prompt に、ユーザー指示・作業範囲・仕様削減時の参照境界を組み込む方法を確認するとき
- 2回の agent call で異なる索引事前処理や仕様削減方針が必要な理由を確認するとき

## Do not read this when
- realization 実装そのものの責務や配置を確認する場合は、realization 側の実装・設計資料を直接読むとき
- oracle file の内容や仕様自体を変更・確認する場合は、対象となる oracle file と関連仕様を直接読むとき
- 通常の agent call 起動処理や `codex exec` 共通設定だけを確認する場合は、共通の起動パラメータ定義を読むとき

## hash
- 5e66923f8843e68d58698bd746bc9d7a785644deb137c82df25faf4a6a9372c5
