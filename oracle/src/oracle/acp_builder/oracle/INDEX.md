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
- `cmoc oracle review` の所見生成・検証・判定・統合に用いる agent call パラメータ構築実装と、各処理の Structured Output schema をまとめた領域。oracle review の各段階へ進むための入口となる。

## Read this when
- `cmoc oracle review` の所見列挙、妥当性検証、採否判定、重複・矛盾の統合処理を変更・調査するとき。
- レビュー用 prompt、oracle-only の実行条件、モデル設定、Structured Output schema の接続を確認するとき。

## Do not read this when
- レビュー所見そのものや oracle file のレビュー基準を確認するとき。
- oracle review 全体の制御フローや共通の agent call・prompt 構築仕様だけを確認するとき。
- 特定の判定結果・擁護理由・反証理由の出力形式だけを確認するときは、対応する JSON schema を直接読む。

## hash
- aa5a80c4e150edd79472a494ab3f2e7844dac648ca9f7b235aad75d187414bfc
