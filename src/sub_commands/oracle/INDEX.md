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
- `cmoc oracle edit` の実行入口。入力された oracle 編集指示を準備し、編集前の indexing と起動前提の確認を行ったうえで、同一設定を共有する 2 回の Codex exec を main worktree から実行する。

## Read this when
- `cmoc oracle edit` の CLI 実行手順、2 回の編集 agent call、編集前 indexing、または main worktree・active session branch の起動条件を確認したいとき。

## Do not read this when
- oracle 編集 prompt の内容や生成規約そのものを確認したいときは、編集 prompt の定義を直接読む。
- prompt editor の入力保存・抽出・後処理だけを確認したいときは、共用 prompt editor 部品を直接読む。
- oracle edit の agent 起動パラメータ生成だけを確認したいときは、対応する launch parameter builder を直接読む。

## hash
- febd747e83ac4ac59bf08cc98699077cf8683955a708d5ed50a0d0bd84d1d229

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
