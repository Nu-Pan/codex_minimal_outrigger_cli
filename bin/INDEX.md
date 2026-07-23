# `cmoc`

## Summary
- cmoc の実行ラッパー。仮想環境の Python を検証し、通常実行では `src/main.py` に引数を渡す。仮想環境が利用できない場合はセットアップ案内と呼び出し位置を含むエラーを表示し、補完プローブ時は実行可能性だけを確認する。

## Read this when
- cmoc コマンドの起動経路、仮想環境 Python の検証、起動失敗時のエラー表示、シェル補完プローブ時の挙動を確認するとき。

## Do not read this when
- cmoc のサブコマンドや CLI 本体の処理内容を確認するときは、`src/main.py` などの実装を直接読む。
- Python の仮想環境作成・依存関係・開発環境の正本仕様を確認するときは、参照先の oracle ドキュメントを読む。

## hash
- acf83c979d3b1776874ea0c582bc094f6efba437c625e0f84cc687ce0a415c6a
