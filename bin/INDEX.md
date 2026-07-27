# `cmoc`

## Summary
- cmoc の実行ラッパー。仮想環境内の Python 実行ファイルを検査し、利用可能な場合に CLI 本体へ引数を渡して起動する。通常実行時の環境エラー報告と、補完プローブ時の起動経路も扱う。

## Read this when
- cmoc の起動処理、仮想環境 Python の検査、起動失敗時のエラー表示、シェルラッパーから CLI 本体への委譲を変更・調査するとき。

## Do not read this when
- CLI の実際のコマンド処理や引数解析を変更・調査するときは、Python の CLI 本体を直接読む。仮想環境の作成・依存関係・開発手順を確認するときは、指定された開発環境の oracle 文書を読む。

## hash
- 3b059d3a3e174efefb9f01ebdc81ca0fb7b5cd6b77d2d743794355295279048c
