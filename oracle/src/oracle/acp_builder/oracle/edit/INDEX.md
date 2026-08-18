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
- `cmoc oracle edit` で使用する本命 agent call と仕様削減 agent call の起動パラメータ構築を定義する。ユーザー指示を完全 prompt に埋め込み、oracle-only のファイルアクセス、モデル・推論設定、作業ディレクトリ、indexing preflight などを固定する。
- 本命 call はユーザー指示に基づく oracle file 編集用、仕様削減 call は現在の oracle file と未コミット差分に基づく過剰仕様の整理用であり、各 call の prompt 構成と `AgentCallParameter` 生成が責務である。

## Read this when
- `cmoc oracle edit` の codex exec 起動パラメータや prompt 構成を変更・確認するとき
- oracle 編集の本命 call と、その後の仕様削減 call の責務・アクセス制約・起動設定を確認するとき

## Do not read this when
- oracle file 自体の仕様内容や編集方針を確認する場合
- 一般的な agent call の基底型、パス解決、prompt builder、構造化文書レンダリングの実装を確認する場合は、それぞれの定義元を直接読むとき
- realization 側の CLI 動作やテストの実装を確認する場合

## hash
- 567402b380a887291f2879c3f6e9e4f19f4b586fb6d94c71158f3f8703384c98
