# `edit`

## Summary
- `cmoc oracle edit` の TUI 起動用パラメータを構築する oracle src と、現時点で空のサブディレクトリを含む、oracle 編集向け起動処理の入口です。

## Read this when
- `cmoc oracle edit` の TUI 起動条件、完全 prompt の生成・保存、固定モデル設定、または Codex CLI 起動パラメータを確認・変更するとき。
- oracle file 編集用 agent call の role、summary、goal、アクセスモード、モデル、推論設定を確認するとき。
- このディレクトリにファイルが追加され、その内容や用途を確認する必要があるとき。

## Do not read this when
- oracle file 編集そのものの仕様や編集処理を確認したいとき。生成された完全 prompt や対象の oracle file を直接確認する。
- 一般的な prompt 構築、構造化文書のレンダリング、パス解決の実装を確認したいとき。各担当モジュールを直接確認する。
- このディレクトリ配下の具体的なファイルを直接確認できるとき。

## hash
- c78cd45b3c46bbc2310a9c45ff87af9f48c6cb6ae37379d872e41e23c3cee295

# `investigation`

## Summary
- `cmoc oracle investigation` の TUI 起動パラメータと完全プロンプトを構築する oracle src。固定のモデル・権限・作業ディレクトリ・インデックス事前処理を指定した `AgentCallParameter` を生成し、ユーザー指示を埋め込んだプロンプトをログ保存する実装入口。

## Read this when
- `cmoc oracle investigation` の TUI 起動動作、起動パラメータ、完全プロンプトの構築・保存方法を調査または変更するとき
- 起動時のモデル、推論強度、ファイルアクセスモード、cwd、構造化出力設定、インデックス事前処理を確認するとき
- ユーザー指示のプロンプトへの埋め込みや cmoc 管理ログへの保存処理を変更するとき

## Do not read this when
- oracle investigation の調査内容や oracle file の正本仕様を確認するときは、`oracle` 配下の調査対象文書を直接読む
- TUI 起動以外の agent call パラメータ生成や共通プロンプト構築の仕様を確認するときは、それぞれの担当モジュールを直接読む

## hash
- a5b0e8d85893dcba128fa9aeef4b1f85ea098766417c8ad5896be8190b1942b4

# `review`

## Summary
- `cmoc oracle review` 用の agent call prompt builder と Structured Output schema をまとめたディレクトリです。新規所見の列挙、所見の擁護・反証、採否判定、重複整理に関する入出力契約と呼び出し条件を確認する入口になります。

## Read this when
- `cmoc oracle review` の所見列挙・検証・判定・マージ処理の prompt や agent call 設定を変更・調査するとき。
- レビュー所見に関する Structured Output schema の形式や、所見・理由・根拠 oracle file の受け渡しを確認するとき。

## Do not read this when
- oracle review の標準的な判定基準そのものを確認するとき。
- 一般的な agent call の共通型・prompt 生成・実行設定を確認するとき。
- レビュー所見を扱わない ACP builder 実装を調査するとき。

## hash
- 286e3cbbe5568cd82d37ff3d1c8bdaf560e9d5ae7e69e20de3253aba2b5db836
