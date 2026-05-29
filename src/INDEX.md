# `commons`

## Summary

- cmoc 全体で共有する実行基盤をまとめたディレクトリです。
- Codex CLI 呼び出し、共通エラー整形、repo root / branch / session state 操作、サブコマンドログ、経過時間計測、タイムスタンプ生成、INDEX.md メンテナンスを扱います。
- 個別サブコマンドではなく、複数機能から再利用される共通部品の入口です。

## Read this when

- Codex CLI 呼び出し、Structured Output 検証、quota 待機や再試行の共通処理を確認したいとき。
- repo root 探索、branch 判定、session/apply state、git 操作補助を確認したいとき。
- 共通エラー表示、サブコマンドログ、経過時間計測、タイムスタンプ、INDEX.md 自動生成の仕組みを追いたいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数だけを確認したいとき。
- `src/commons` の特定モジュールだけを直接見たいときは、この目次ではなく該当ファイルを読むべきです。
- `src` 配下の別機能や `tests` の実装だけを追いたいとき。

## hash

- e3dc47e0b9023b8290ec846676040ffde9c76196984d9bfc9120e260536bc102

# `main.py`

## Summary

- `cmoc` CLI のエントリーポイントで、Typer アプリ本体と `session` / `apply` / `review` のサブアプリを組み立てています。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の各コマンドを定義し、実処理は `src/sub_commands/` 側へ委譲しています。
- Typer / Click の例外を共通エラーレポートへ変換し、`NoArgsIsHelpError` を含む起動時エラーを終了コード付きで処理します。

## Read this when

- `cmoc` のエントリーポイント、Typer アプリの構成、サブコマンド登録を修正・レビューしたいとき
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` とその引数定義を確認したいとき
- サブコマンドなし起動時の `NoArgsIsHelpError` の扱い、`--help` 相当の挙動、終了コードの伝播を確認したいとき
- Typer / Click の例外を `CmocError` と共通エラーレポートへ変換する起動経路を確認したいとき
- `python src/main.py` で直接起動する経路の振る舞いを確認したいとき

## Do not read this when

- 各サブコマンド本体の処理内容だけを確認したいとき
- 共通エラー型やエラーレポートの整形だけを確認したいとき
- CLI の設計ルールや配置方針だけを確認したいとき
- サブコマンドごとの仕様断片だけを確認したいとき

## hash

- 0c76935e2e4d5e562d321e1b65e17c49e36e89415a7d311c6f037b13785a396f

# `sub_commands`

## Summary

- cmoc のサブコマンド実装をまとめた入口ディレクトリです。
- `init.py` と `eval_oracles.py` に加え、`apply` と `session` の各サブパッケージをまとめて管理しています。
- 個別コマンドの実装位置を素早く辿るためのルーティング目次です。

## Read this when

- cmoc の各サブコマンド実装がどのファイル・サブパッケージにあるか確認したいとき。
- 新しいサブコマンドや内部モジュールを追加・整理するとき。
- `apply` / `session` / `init` / `review oracles` の実装入口を俯瞰したいとき。

## Do not read this when

- 個別サブコマンドの引数、状態遷移、終了条件などの詳細仕様だけを確認したいときは、該当モジュールや正本仕様を直接読むべきです。
- `src.sub_commands` のパッケージ宣言だけを確認したいときは `__init__.py` で足ります。
- CLI の使い方や `oracles` の評価仕様だけを確認したいときは、このディレクトリではなく対応する仕様文書を読むべきです。

## hash

- 87c9ebc733503366dce29c5b771e9a59fc2e091098d92dc4ed934062d5ac4b0b
