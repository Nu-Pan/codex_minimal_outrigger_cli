# `edit`

## Summary
- oracle 編集用 TUI の起動パラメータを構築する実装を含む領域です。リポジトリルート、oracle 編集専用のアクセス制御、固定プロンプト、モデル設定、構造化出力、管理ログ保存を確認する入口になります。現時点では、確認対象となる本文ファイルを含まない空の領域もあります。

## Read this when
- `cmoc oracle edit` の TUI 起動条件やパラメータを確認・変更するとき。
- oracle 編集時に使われるプロンプト、パスコンテキスト、アクセスモード、モデル設定、ログ保存の挙動を調べるとき。

## Do not read this when
- oracle file の編集内容や編集エージェントの一般的な役割を確認するとき。
- 共通のプロンプト構築処理や realization 側の CLI・TUI 動作を確認するとき。
- この領域に具体的な本文ファイルがなく、配下のファイルを直接確認できる場合。

## hash
- 906c47065e8fde322cc925923c398f022ea6230fc1b3fcece490d0d0d70e280b

# `investigation`

## Summary
- `cmoc oracle investigation` の TUI 起動パラメータを構築する正本実装。oracle file 調査用プロンプトの生成・ログ保存と、モデル、権限、作業ディレクトリなどを固定した `AgentCallParameter` の返却を担う。

## Read this when
- `cmoc oracle investigation` の TUI 起動条件、調査用プロンプト、起動パラメータ構成を変更・確認するとき。
- ユーザー指示を含む完全プロンプトの生成から起動前ログ保存までの流れを確認するとき。

## Do not read this when
- oracle file 調査の仕様や完全プロンプト共通構造を確認するとき。
- `AgentCallParameter` の型定義やファイルアクセスモードの一般的な意味だけを確認するとき。

## hash
- 7c5fc3c611d4d9eba23dff64427007dff368c17235754cdd9d84ce1f8a9897ea

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
