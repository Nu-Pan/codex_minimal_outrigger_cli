# `edit`

## Summary
- `cmoc oracle edit` 向けの TUI 起動パラメータと、完全 prompt を管理ログへ保存する oracle src を含むディレクトリ。パス、アクセスモード、モデル・推論設定、構造化出力、インデックス前処理などの agent call 条件を確認する入口。

## Read this when
- `cmoc oracle edit` の TUI 起動動作や agent call パラメータを変更・調査するとき
- oracle file 編集用 prompt の構築、ユーザー指示の埋め込み、ファイルアクセス制約を確認するとき

## Do not read this when
- oracle file の編集処理そのものを調査するとき
- 一般的な prompt 構築の詳細だけを調査するとき
- TUI を起動しない agent call や `cmoc oracle edit` 以外のサブコマンドを調査するとき

## hash
- 2d2f53cb81d73889706ce5ad0305038c3b5f1934b9c5eb5dce9dbf21c95ec205

# `investigation`

## Summary
- `cmoc oracle investigation` の TUI 起動処理を担当し、固定プロンプト、エージェント呼び出しパラメータ、ログ保存、TUI 起動設定を構築する。

## Read this when
- `cmoc oracle investigation` の TUI 起動処理を変更・調査するとき
- 完全プロンプト、エージェント呼び出しパラメータ、editor input ログ保存の挙動を変更・調査するとき

## Do not read this when
- oracle file の調査内容そのものを変更・調査するとき
- 完全プロンプトの共通構築ロジックを変更・調査するときは、対応する調査処理または prompt builder を直接読む

## hash
- a9577f323e7d83ff7ce7f194dee04eec9a701b0f325f260633c236cf28f27e0f

# `review`

## Summary
- `cmoc oracle review` の所見列挙・判定・統合・妥当性検証に関する Structured Output schema と agent call パラメータ構築用 oracle source をまとめた領域。各ファイルは、レビュー所見の構造化出力契約または対応する prompt・アクセス権限・実行設定を定義する。

## Read this when
- `cmoc oracle review` の所見列挙、採否判定、重複・矛盾整理、妥当性の支持・反証に関する prompt 構築や agent call パラメータを変更・調査するとき。
- これらの処理で利用する Structured Output schema の入力・出力契約を確認するとき。

## Do not read this when
- レビュー所見の内容や oracle 仕様そのものの妥当性を確認するとき。
- 所見レビュー全体の実行制御や共通 prompt 生成だけを確認するとき。
- `cmoc oracle review` と無関係な agent call や Structured Output を扱うとき。

## hash
- c84e53dc0546b88f41fdcceed717a6500ea8847f5b8aa1b704c1fd587fae65eb
