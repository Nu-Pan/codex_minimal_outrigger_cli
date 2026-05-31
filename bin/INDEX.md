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
- 仮想環境 Python が無い、または実行できない場合のエラー文面、終了ステータス 1、復旧手順を確認したいとき。
- `src/main.py` へ引数をそのまま渡す流れを確認したいとき。
- エラー表示に出る簡易 Call stack の行番号の取り方を追いたいとき。

## Do not read this when

- `src/main.py` 以降の CLI 登録やサブコマンド実装だけを確認したいとき。
- `commons` の共通処理や Python 実装の詳細だけを追いたいとき。
- テストコードや `INDEX.md` の生成仕様だけを確認したいとき。
- 仮想環境の作成手順そのものではなく、依存関係やパッケージ構成を確認したいとき。

## hash

- 7776f1a8bd801b136138460cbf22be2952aa2a01188c8c59b411a5cfc2b6aff6
