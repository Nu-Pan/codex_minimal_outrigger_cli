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
- `cmoc oracle edit` が起動する本命 agent call と、成功後の仕様削減 agent call の `codex exec` パラメータ構築を担う。ユーザー指示を完全 prompt に組み込み、oracle-only の書き込み範囲、モデル・推論設定、作業ディレクトリ、Structured Output 設定、索引付け前処理の有無を定義する。oracle 編集起動条件や、仕様変更後の削減・整合性調整の起動条件を確認する際の入口となる。

## Read this when
- `cmoc oracle edit` の本命または仕様削減 agent call の起動パラメータを変更・確認するとき
- oracle 編集用 prompt の構成、ユーザー指示の埋め込み、ファイルアクセスモード、起動前索引付け設定を確認するとき
- 本命成功後の仕様削減 call に渡す参照境界や、既存未コミット差分の扱いを確認するとき

## Do not read this when
- oracle file の編集ルールや仕様削減そのものの正本規範を確認する場合は、関連する oracle の規範文書を直接読む
- 一般的な agent call パラメータや共通 prompt 構築の挙動だけを確認する場合は、対応する共通 builder を直接読む
- `cmoc oracle edit` 以外のコマンドの起動パラメータを確認する場合

## hash
- 24b45a5f20509912affc623b82127fcd96be5aa14aa03b618f05005829a2bca5
