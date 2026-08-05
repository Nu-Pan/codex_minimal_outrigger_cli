# `edit`

## Summary
- 現時点で本文ファイルを含まない空のディレクトリです。

## Read this when
- このディレクトリにファイルが追加され、その内容や用途を確認する必要があるとき。

## Do not read this when
- このディレクトリ配下の具体的なファイルを直接確認できる場合。

## hash
- 5a0738490b6b32407892ee1cfe8c82273cebcea45d9451bbc9c34cc67ec0c2fe

# `investigation`

## Summary
- `cmoc oracle investigation` の TUI 起動パラメータを構築する実装。リポジトリルートを作業ディレクトリとして確定し、ユーザー指示を含む完全プロンプトの生成・保存、固定されたモデル・推論強度・ファイルアクセス権・起動設定の返却を担う。

## Read this when
- `cmoc oracle investigation` の TUI 起動パラメータ、完全プロンプト生成、作業パス確定、起動ログ保存の挙動を変更・調査するとき。

## Do not read this when
- oracle investigation の調査プロンプト本文や一般的なプロンプト組み立て規則だけを確認したいとき。完全プロンプト生成実装や関連する prompt builder を直接読む。
- TUI 起動以外の agent call パラメータ構築を変更するとき。

## hash
- 4b8e91f02a0cbc1814d86e74fce265c56c2c18045f8a0e539d69e095191183c8

# `review`

## Summary
- `cmoc oracle review` の各段階で使う、所見列挙・判定・擁護・反証・統合に関する Structured Output schema と agent call パラメータ構築実装をまとめた領域。レビュー処理の個別段階を調査する入口となる。

## Read this when
- `cmoc oracle review` の所見生成、妥当性判定、擁護・反証理由の列挙、所見統合を変更または調査するとき。
- 各処理の prompt、oracle-only アクセス、モデル設定、作業ディレクトリ、Structured Output schema の接続を確認するとき。

## Do not read this when
- レビュー基準や個別所見の内容を確認するときは、対応する oracle review 仕様やレビュー対象を直接読む。
- 共通の agent call パラメータ、prompt 構築、パス解決の仕様だけを確認するときは、参照先の共通モジュールを直接読む。
- 所見統合結果の適用処理など、agent call パラメータ構築以外の実装を調査するときは、該当する実行・編集側の実装を直接読む。

## hash
- b905b66d3e6f9d152ffc02296b9fef4fe75b8bdf0ed2d91af1efb37a647dfb93
