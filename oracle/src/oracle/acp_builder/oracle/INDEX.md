# `edit`

## Summary
- `cmoc oracle edit` の TUI 起動に必要なパラメータを構築する oracle src を含むディレクトリ。ユーザー指示を埋め込んだ完全プロンプトの生成・ログ保存と、固定設定で Codex CLI を起動するための入力生成が主な責務。

## Read this when
- `cmoc oracle edit` の TUI 起動処理、完全プロンプトの構成、モデル・推論強度・ファイルアクセス設定を確認または変更するとき。
- ユーザー指示を含む editor_input ログの保存方法や、TUI 起動用 AgentCallParameter の生成を確認するとき。

## Do not read this when
- oracle file の編集内容や編集担当 agent のプロンプト仕様を変更するとき。関連する prompt builder または oracle 編集処理を直接読む。
- 一般的な ACP パラメータ定義やパス解決の仕様だけを確認するとき。各共有モジュールを直接読む。

## hash
- 595423ea0a51245864528aca035f041aebed65b16237cf81e6d7e1027565db07

# `investigation`

## Summary
- `cmoc oracle investigation` の TUI 起動用パラメータを構築する実装。ユーザー調査指示を含む完全プロンプトを生成・保存し、モデルやアクセス権限などの固定起動設定とともに返す。

## Read this when
- `cmoc oracle investigation` の TUI 起動処理を変更・調査するとき
- 完全プロンプトの構築・保存処理を変更・調査するとき
- モデルやアクセス権限などの起動時固定値を確認するとき

## Do not read this when
- 調査用プロンプトの本文構成や共通プロンプト生成規則だけを確認したいとき
- oracle investigation 以外の agent call パラメータや TUI 起動処理を調査するとき

## hash
- c5f3cd682c896b600f5ce3188f406ef7f52e4cb1dceeda6062955ba7b19c0076

# `review`

## Summary
- `cmoc oracle review` の所見レビュー用エージェント呼び出し定義と Structured Output スキーマをまとめたディレクトリです。新規所見の列挙、所見の採否判定、賛否理由の検証、所見リストの重複・矛盾整理を扱い、それぞれの処理実装と入出力契約の入口になります。

## Read this when
- `cmoc oracle review` の所見列挙・判定・擁護理由・反証理由・マージ処理を変更または追跡するとき。
- レビュー用 agent call の prompt、読み取り権限、モデル設定、Structured Output schema の対応関係を確認するとき。
- レビュー所見の入力・出力形式、重複排除や既知理由の除外条件を確認するとき。

## Do not read this when
- 通常の ACP builder 実装や、oracle review 以外の prompt 構築を調べるとき。
- レビュー結果の schema または実装を個別に確認でき、ディレクトリ全体の構成を知る必要がないとき。
- 実際の oracle file のレビュー基準そのものを確認するとき。

## hash
- 2c05a5aaf7bf06cba4d019c69706e8ba87dd9d3dbbb630ff813dd5afcdc2bd57
