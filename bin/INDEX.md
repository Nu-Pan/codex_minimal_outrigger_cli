# `cmoc`

## Summary

- `bin/cmoc` は cmoc コマンドのシェル製エントリーポイントです。
- スクリプト自身の場所から `<cmoc-root>` を解決し、`<cmoc-root>/.venv/bin/python` を実行 Python として使用します。
- 仮想環境 Python が存在し実行可能な場合は、`<cmoc-root>/src/main.py` に全引数を渡して `exec` します。
- 仮想環境 Python が見つからない、または実行不可の場合は、日本語の構造化エラーを標準出力へ表示し、セットアップ手順、必要な実行ファイル、簡易 Call stack を示して終了ステータス 1 で終了します。
- `line_number_of` はエラー表示内の Call stack 用に、このスクリプト内で指定パターンに一致する最初の行番号を求める補助関数です。

## Read this when

- cmoc コマンド起動時に、どの Python とどの Python ファイルが実行されるか確認したいとき。
- .venv/bin/python が無い場合や実行権限が無い場合のエラー文面、終了ステータス、復旧手順を確認したいとき。
- 配布用または開発用の CLI ラッパーとして `bin/cmoc` の挙動を確認したいとき。
- `bin/cmoc` から `<cmoc-root>/src/main.py` への引数受け渡し方法を確認したいとき。
- 仮想環境未セットアップ時のユーザー向け案内や Call stack 表示の実装を変更・検証したいとき。

## Do not read this when

- cmoc のサブコマンド本体や引数処理を追いたいとき。
- `<cmoc-root>/src/main.py` 以降の Python 実装や共通処理を確認したいとき。
- pytest などのテスト実装やテストケースの観点を確認したいとき。
- `oracles` 側の仕様断片や `INDEX.md` の生成ルールだけを確認したいとき。
- 仮想環境の作成手順そのものではなく、Python パッケージ構成や依存関係定義を確認したいとき。

## hash

- ad61286380c31b08548fc54089fc4097d1fb116a324e6fc55e7ff94da53e530a
<!-- cmoc-index-kind: file -->
