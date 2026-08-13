# `launch_tui.py`

## Summary
- 対象は `cmoc oracle investigation` の調査用 TUI 起動パラメータを構築する実装です。ユーザー指示を組み込んだ完全プロンプトを生成・ログ保存し、oracle 限定の読み取り調査を行うためのモデル、推論強度、作業ディレクトリ、構造化出力設定、インデックス事前処理などの固定起動条件を返します。調査プロンプト生成、調査ログ保存、またはこの TUI 起動設定の変更を扱う際の入口です。

## Read this when
- `cmoc oracle investigation` の TUI 起動パラメータや、その完全プロンプトの構築・保存処理を変更または確認するとき。
- oracle file 調査用 agent call のモデル設定、ファイルアクセス範囲、作業ディレクトリ、構造化出力設定、起動前インデックス処理を確認するとき。

## Do not read this when
- 通常の oracle 調査内容や正本仕様を確認するだけで、TUI 起動設定や完全プロンプトの構築を扱わないとき。
- 他の agent call 種別の起動パラメータを確認するときは、その起動処理を直接参照する。

## hash
- 83d0e02aa99d55e57cbad5d6287927b44a150244e891f2d4aa47a9c3db1dfb54
