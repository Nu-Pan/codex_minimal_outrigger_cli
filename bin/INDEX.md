# `cmoc`

## Summary

- `bin/cmoc` は cmoc コマンドのシェル製エントリーポイントです。
- スクリプト自身の位置から `<cmoc-root>` を解決し、`<cmoc-root>/.venv/bin/python` を実行 Python として使います。
- 仮想環境 Python が利用可能なときは、全引数を `<cmoc-root>/src/main.py` にそのまま渡して `exec` します。
- 仮想環境 Python が見つからない、または実行不可のときは、日本語の構造化エラーを標準出力へ表示し、セットアップ手順・必要な実行ファイル・簡易 Call stack を示して終了ステータス 1 で終了します。
- `line_number_of` は、エラー表示内の Call stack 用に、このスクリプト内で指定パターンに一致する最初の行番号を求める補助関数です。

## Read this when

- `bin/cmoc` がどの Python で `src/main.py` を起動するか確認したいとき。
- `.venv/bin/python` が無い、または実行できない場合のエラー文面・終了ステータス・復旧手順を確認したいとき。
- シェル製 CLI エントリーポイントとしての挙動を把握したいとき。
- `bin/cmoc` から `src/main.py` へ引数をそのまま渡す流れを確認したいとき。
- エラー表示内の Call stack を組み立てる `line_number_of` の役割を確認したいとき。

## Do not read this when

- `src/main.py` 以降の Python 実装や共通処理の仕様だけを確認したいとき。
- `cmoc` の各サブコマンド本体や引数解析の仕様だけを確認したいとき。
- pytest などのテスト観点やテストケースの整理だけを確認したいとき。
- `oracles` 側の仕様断片や `INDEX.md` の生成ルールだけを確認したいとき。
- 仮想環境の作成手順そのものではなく、依存関係や Python パッケージ構成を確認したいとき。

## hash

- a4cf3ae40b19f485ed0761798c1e489b1cb4f77cee7440077d07f09d55ae5ed4
<!-- cmoc-index-kind: file -->
