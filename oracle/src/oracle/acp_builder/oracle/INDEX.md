# `edit`

## Summary
- oracle 編集フローの TUI 起動処理を扱うディレクトリで、agent call の起動パラメータと完全 prompt の生成・管理ログ保存を確認する入口です。現時点では本文ファイルを含まない空のディレクトリです。
- 配下の具体的なファイルを確認できる場合は、そのファイルを直接読み、共通 prompt 構築規則や agent call パラメータ型は担当モジュールを参照してください。

## Read this when
- `cmoc oracle edit` の TUI 起動処理、agent call パラメータ、完全 prompt の生成、または関連する作業環境・権限・ログ保存の挙動を確認するとき。
- このディレクトリにファイルが追加され、その内容や用途を確認する必要があるとき。

## Do not read this when
- oracle file の具体的な編集内容や仕様を確認するとき。
- prompt の共通構築規則や agent call パラメータの型定義を確認するとき。
- このディレクトリ配下の具体的なファイルを直接確認できるとき。

## hash
- 52be3bfbd9a1fc56345bb483733f54d2e6757e54707cd2f5966b076a4bde6169

# `investigation`

## Summary
- `cmoc oracle investigation` 向けに、調査用プロンプトと Codex CLI TUI の起動情報を構築する実装の入口。固定の役割・制約・作業範囲、ログ保存先、実行設定を扱う。

## Read this when
- `cmoc oracle investigation` の TUI 起動条件、プロンプト構築、調査用ファイルアクセスモード、モデル・推論設定を確認または変更するとき。

## Do not read this when
- oracle investigation の調査内容や oracle file の仕様を確認するときは、調査対象の oracle file やプロンプト構築処理を直接読む。
- 通常の Codex CLI 起動処理や、他の cmoc コマンドの起動パラメータだけを確認するとき。

## hash
- 38e50e5b8701ac3ea37f69f8e6b656928c722718536d2eeb50a7d43cbc2d36c3

# `review`

## Summary
- oracle review の所見列挙・採否判定・検証理由生成・統合に関するスキーマと、各処理のエージェント呼び出しパラメータ構築実装をまとめた領域。oracle review の処理経路や入出力契約を調べる際の入口となる。

## Read this when
- oracle review で所見を列挙、判定、擁護・反証、統合する処理を確認するとき。
- 各レビュー処理の Structured Output schema、プロンプト、モデル設定、アクセス範囲、起動条件を確認・変更するとき。

## Do not read this when
- oracle review 以外の agent call parameter 構築を調べるとき。
- レビュー所見の内容や根拠仕様そのものを調査するとき。
- 個別の出力形式だけを確認する場合は、該当する JSON Schema を直接読む。

## hash
- f260447b6475c8470ac7f1305b41a6297fef12da5609cd42855c9ca197c43707
