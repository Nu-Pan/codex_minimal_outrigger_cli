# `__init__.py`

## Summary
- oracle 系サブコマンドをまとめる package の境界を示す。oracle サブコマンド群への入口として扱う。

## Read this when
- oracle 系サブコマンドの package 構成や入口を確認するとき。

## Do not read this when
- 個別の oracle サブコマンド実装の詳細を確認するとき。

## hash
- 2c8110c7811042f7162e1264e7027bb2d801f4687eb66f48f1668402c8eeb0df

# `edit`

## Summary
- 編集関連の実装ファイルを含まない空のディレクトリです。現時点で下位要素へのルーティング先はありません。

## Read this when
- このディレクトリに編集関連ファイルが追加されたか確認するとき。

## Do not read this when
- Oracle サブコマンドの実装を調査するとき。親ディレクトリの実装ファイルを直接確認してください。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `edit.py`

## Summary
- `cmoc oracle edit` の実行入口として、入力した oracle 編集指示から本命 agent call と、正常終了後に行う仕様削減 agent call までの処理を扱う。
- 本命起動前の indexing と起動前提の検証を行い、各 agent call の開始・成功・失敗状態を primary report に反映する。

## Read this when
- `cmoc oracle edit` の入力から本命編集、後続の仕様削減までの実行順序を確認したいとき。
- 本命 agent call の起動条件や agent call 状態の記録処理を確認したいとき。

## Do not read this when
- oracle 編集 prompt や起動パラメータの内容を確認したいとき。
- 入力エディタ、session 状態、Git branch、runtime report の個別仕様を確認したいとき。

## hash
- f0d8bf212602a8c1e6bb8c66481ecf2f3eb7c3243eefce1f43269e8522705b66

# `investigation.py`

## Summary
- `cmoc oracle investigation` サブコマンドの実行入口。入力した oracle 調査指示を編集・収集し、調査契約付きの起動パラメータで read-only Codex TUI を開始する。

## Read this when
- oracle investigation サブコマンドの実行手順や、調査指示の入力から Codex TUI 起動までの処理を確認・変更するとき。
- oracle 調査用プロンプトの編集、設定読込、実行前処理、進捗ステップの連携を確認するとき。

## Do not read this when
- oracle 調査用 TUI の起動パラメータそのものを変更するときは、起動パラメータ構築側の対象を直接読む。
- 共通のプロンプト編集処理や CLI ランタイムの実装を確認するときは、それぞれの共通モジュールを直接読む。

## hash
- 65a583fe03422d9cb705c5055952e67db1df02b2631bd482e1c9918295fa6b9f
