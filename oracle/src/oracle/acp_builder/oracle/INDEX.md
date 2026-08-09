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
- oracle review の各 agent call 用スキーマと prompt builder をまとめた領域。所見の列挙、判定、統合、妥当性の擁護・反証に関する出力契約と呼び出し条件を確認する入口。

## Read this when
- oracle review の所見列挙出力形式や新規所見列挙フローを扱うとき。
- レビュー所見の採否判定形式や判定用 agent call を扱うとき。
- レビュー所見の重複・矛盾の統合処理を扱うとき。
- 所見の妥当性を支持・反証する理由の出力形式や prompt builder を扱うとき。

## Do not read this when
- 個々のレビュー所見の内容や、その根拠となる oracle 仕様を確認するとき。
- oracle review の判定基準そのものや共通の agent call 基盤を調査するとき。
- 所見列挙・判定・統合・妥当性検証以外の oracle review サブコマンドを調査するとき。

## hash
- 6523641af3d13ce33fbb31edc74b8691945fb982cf3af8628347f026e7c8ccce
