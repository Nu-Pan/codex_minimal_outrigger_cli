# `cmoc`

## Summary

- `bin/cmoc` は cmoc コマンドのシェル製エントリーポイントです。
- スクリプト自身の位置から `<cmoc-root>` を解決し、`<cmoc-root>/.venv/bin/python` を実行 Python として使います。
- 仮想環境 Python が使えるときは、全引数を `<cmoc-root>/src/main.py` にそのまま渡して `exec` します。
- 自動補完プローブでも、Python が使える場合は同じく `src/main.py` を起動し、使えない場合は終了ステータス 1 で終わります。
- 仮想環境 Python が見つからない、または実行できないときは、日本語の構造化エラー、セットアップ手順、必要な実行ファイル、簡易 Call stack を標準エラーに出します。
- `line_number_of` は、エラー表示用の Call stack に必要な行番号を求める補助関数です。

## Read this when

- `cmoc` がどの Python で `src/main.py` を起動するか確認したいとき。
- `_CMOC_COMPLETE` が設定された自動補完プローブ時の分岐を確認したいとき。
- 仮想環境 Python が見つからない、または実行できない場合のエラー文面、終了ステータス 1、復旧手順を確認したいとき。
- `src/main.py` へ引数をそのまま渡す流れを確認したいとき。
- エラー表示に出る簡易 Call stack の行番号の取り方を追いたいとき。

## Do not read this when

- `src/main.py` 以降の CLI 登録やサブコマンド実装だけを確認したいとき。
- Python 側の共通エラー整形や各種ユーティリティだけを追いたいとき。
- 仮想環境の作成手順や導入手順だけを確認したいとき。

## hash

- 6ec823a6700c58a9d3d5fe70bdbdbe61aebc15b6c81e0985b09d9c9a3d5bb386
