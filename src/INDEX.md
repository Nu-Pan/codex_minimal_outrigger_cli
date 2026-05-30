# `commons`

## Summary

- `cmoc` の CLI 全体で共有する基盤処理をまとめるディレクトリの入口です。
- Codex 呼び出し、リポジトリ判定、エラー整形、サブコマンドログ、時間計測、タイムスタンプ、レポート保存を扱います。
- 個別サブコマンドではなく、横断的な共通処理を追うときの起点になります。

## Read this when

- `src/commons` 配下のどのモジュールに共通処理があるかを素早く把握したいとき。
- CLI 実行基盤、リポジトリ判定、エラー整形、ログ、計測、レポート、INDEX 生成の責務分担を確認したいとき。
- 新しい共通ユーティリティを追加する前に、既存の共通処理の参照先を探したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数定義だけを確認したいとき。
- `oracles` の本文や `README.md` のような仕様書そのものを読みたいとき。
- 共通処理ではなく、画面表示や外部連携の個別実装だけを追いたいとき。

## hash

- f61df7bbf4764f775e21d4801a49381c989afd011386f5cd429993880c12086c

# `main.py`

## Summary

- cmoc CLI のエントリーポイントで、Typer のルート app と `session` / `apply` / `review` のサブアプリを組み立てます。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録と、それぞれのオプション既定値やエイリアスをまとめます。
- サブコマンド未指定時の利用者向けエラー、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc の起動点やサブコマンド登録を修正・レビューしたいとき。
- `init` / `session` / `apply` / `review` のコマンド名、エイリアス、オプション既定値を確認したいとき。
- サブコマンドなし起動時の利用者向けエラー、終了コード、`--help` への誘導を確認したいとき。
- `python src/main.py` で直接起動する経路と、その例外ハンドリングを確認したいとき。

## Do not read this when

- 各サブコマンドの本体ロジックや `src/sub_commands/` 配下の処理だけを確認したいとき。
- 共通エラー型や `format_error_report` の整形仕様だけを確認したいとき。
- `INDEX.md` の生成ルールや共通ユーティリティの設計だけを追いたいとき。

## hash

- 725244cd04649c14efdc472340862818b2eabfb76416af919258408edf3121cc

# `sub_commands`

## Summary

- `src/sub_commands` は `cmoc` のサブコマンド実装群をまとめるパッケージで、`__init__.py`、`init.py`、`eval_oracles.py`、`apply/`、`session/` に役割が分かれています。
- `__init__.py` はパッケージ宣言だけを担い、`init.py` は `cmoc init`、`eval_oracles.py` は `cmoc review oracles`、`apply/` と `session/` は各系サブコマンドの入口です。
- ここは実装入口の全体地図であり、個別コマンドの詳細は各モジュールや下位 `INDEX.md` に分かれています。

## Read this when

- `src/sub_commands` 配下で、どのモジュールがどのサブコマンドを担当しているかを把握したいとき。
- `cmoc init`、`cmoc review oracles`、`cmoc apply`、`cmoc session` の実装入口を素早く見分けたいとき。
- このパッケージ配下の実装・修正・レビュー・テストを始める前に、関連ファイルの役割を整理したいとき。
- `src/sub_commands` が Python パッケージとして宣言されていることと、下位パッケージが分割されていることを確認したいとき。

## Do not read this when

- 個別の `cmoc init`、`cmoc review oracles`、`cmoc apply`、`cmoc session` の詳細仕様や状態遷移を確認したいときは、該当モジュールや下位の `INDEX.md` を読むべきです。
- `src/sub_commands` のパッケージ宣言だけを確認したいときは `__init__.py` を直接見れば足ります。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを確認したいときは、このディレクトリではなく `oracles/app_specs/indexing.md` を読むべきです。

## hash

- 4048a31b0e9db72945cd9b537cdf349ddef4970de669b51168fa18f673394e0c
