# `edit`

## Summary
- このディレクトリは、oracle 編集向けの起動関連実装を配置する領域です。現時点では空のサブディレクトリと、`cmoc oracle edit` の TUI 起動パラメータを構築する実装を含みます。

## Read this when
- `cmoc oracle edit` の TUI 起動設定、agent call パラメータ、完全 prompt の保存や動的構成を確認・変更するとき。
- このディレクトリに追加されたファイルの内容や用途を確認するとき。

## Do not read this when
- oracle file の編集内容や realization 側の実装だけを確認する場合。
- prompt の共通構築ロジックを確認する場合は、共通 prompt builder の対象を直接読む場合。
- 空のサブディレクトリ配下を確認する必要がなく、具体的なファイルを直接確認できる場合。

## hash
- 014f1bb2b9e944bb525857130e0c65a9705a18df0639e5f79c6a243dc902317c

# `investigation`

## Summary
- `cmoc oracle investigation` の TUI 起動設定を構築する実装。oracle file 調査用プロンプトを生成・保存し、モデル、アクセスモード、作業ディレクトリ、インデックス事前処理を含む起動パラメータを提供する。

## Read this when
- `cmoc oracle investigation` の TUI 起動条件、調査プロンプト、使用モデル、ファイルアクセスモード、起動ログ保存の変更や確認を行うとき。

## Do not read this when
- 他の cmoc コマンドの起動パラメータを扱うとき。
- 汎用的なプロンプト生成処理を扱うとき。

## hash
- c80256b46fbf3a6ec4f065d31ee05e741f68cd13446ab6b0d47be66509b58657

# `review`

## Summary
- oracle review の所見列挙・判定・マージ・擁護・反証に関する Structured Output スキーマと agent call パラメータ実装を扱う領域です。各ファイルは、所見の生成、妥当性判定、重複整理、賛成理由・反証理由の列挙という個別フローへの入口を提供します。

## Read this when
- `cmoc oracle review` の所見生成、妥当性判定、所見リスト整理、擁護理由または反証理由の列挙処理を変更・調査するとき。
- レビュー用 agent call のプロンプト、oracle 読み取り範囲、モデル設定、Structured Output との対応を確認するとき。
- 所見関連の Structured Output の入力・出力契約を確認するとき。

## Do not read this when
- レビュー所見の内容や妥当性基準そのものを確認する場合は、対応するレビュー標準または対象 oracle file を直接読む。
- Structured Output の共通生成処理や一般的な agent call 基盤だけを確認する場合は、共通実装を直接読む。
- 所見列挙・判定・マージ・擁護・反証以外の `cmoc oracle review` サブコマンドを調査する場合。

## hash
- 348c466b7b71e9efe8ce66188142a1cca30f4397c9735e2d43e175b8a3be9f6b
