# `edit`

## Summary
- `cmoc oracle edit` の TUI 起動関連を扱うディレクトリです。現時点では空の `fork` と、TUI 起動パラメータを構築する `launch_tui.py` を含みます。

## Read this when
- `cmoc oracle edit` の TUI 起動方法、編集 prompt、モデル・権限・作業ディレクトリなどの起動設定を確認または変更するとき。
- このディレクトリに追加されたファイルの内容や用途を確認するとき。

## Do not read this when
- oracle file の編集処理そのものを確認または変更するとき。
- prompt 共通生成規則、パス解決、構造化文書のレンダリングを確認または変更するとき。
- `launch_tui.py` など対象ファイルを直接確認できるとき。

## hash
- c2d7be308c0da03ba02dc172c32c84646643a7b7356b27d85318fccd6beb2462

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
