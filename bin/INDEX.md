# `cmoc`

## Summary

- `bin/cmoc` は cmoc コマンドのシェル製エントリーポイントです。
- スクリプト自身の場所から `<cmoc-root>` を解決し、`<cmoc-root>/.venv/bin/python` を実行 Python として使用します。
- 仮想環境 Python が存在し実行可能な場合は、`<cmoc-root>/src/main.py` に全引数を渡して `exec` します。
- 仮想環境 Python が見つからない、または実行不可の場合は、日本語の構造化エラーを標準出力へ表示し、セットアップ手順、必要な実行ファイル、簡易 Call stack を示して終了ステータス 1 で終了します。
- `line_number_of` はエラー表示内の Call stack 用に、このスクリプト内で指定パターンに一致する最初の行番号を求める補助関数です。

## Read this when

- cmoc コマンド起動時に、どの Python とどの Python ファイルが実行されるか確認したいとき。
- `.venv/bin/python` が無い場合や実行権限が無い場合のエラー文面、終了ステータス、復旧手順を確認したいとき。
- cmoc の配布用または開発用 CLI ラッパーの挙動を調べたいとき。
- `bin/cmoc` から `<cmoc-root>/src/main.py` への引数受け渡し方法を確認したいとき。
- 仮想環境未セットアップ時のユーザー向け案内や Call stack 表示の実装を変更・検証したいとき。

## Do not read this when

- cmoc の各サブコマンドの具体的な処理内容やアプリケーション仕様を調べたいとき。
- `src/main.py` 以降の Python 実装、コマンドディスパッチ、共通処理の詳細を調べたいとき。
- pytest や Fake Codex CLI など、テスト実装の規約やテストケース本体を調べたいとき。
- `<repo-root>` 側で cmoc が生成・管理するファイルや `INDEX.md` の仕様を調べたいとき。
- 仮想環境の作成手順ではなく、Python パッケージ構成や依存関係定義の詳細を確認したいとき。

## hash

- 2b0bcfff0746f06777bfe77462672a4ade59b2a3d578472141e120ad98c1c4d2
<!-- cmoc-index-kind: file -->
