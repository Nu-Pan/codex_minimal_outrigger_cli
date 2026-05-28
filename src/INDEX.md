# `commons`

## Summary

- `cmoc` 全体で使う共通ユーティリティをまとめたパッケージです。
- Codex CLI 実行、コマンド共通制御、エラー整形、git / session state 操作、サブコマンドログ、タイマー、タイムスタンプ、`INDEX.md` メンテナンスを含みます。
- 個別サブコマンドではなく、横断処理の土台を探す入口です。

## Read this when

- cmoc 全体で共有する共通基盤の実装や修正をしたいときに読むべきです。
- Codex CLI の実行ラッパー、Structured Output、リトライや quota 待ちの流れを確認したいときに読むべきです。
- repo root 探索、session / apply state、branch 判定、サブコマンドログ、経過時間、タイムスタンプ、`INDEX.md` 更新を追いたいときに読むべきです。
- サブコマンドの共通実行制御やエラー表示を実装・レビューしたいときに読むべきです。

## Do not read this when

- 個別サブコマンドの引数や業務ロジックを確認したいときは、この配下ではなく `src/sub_commands` を読むべきです。
- cmoc の使い方や運用フロー全体を知りたいだけなら、この配下ではなく上位の正本仕様を読むべきです。
- 1 つの機能だけを深掘りしたいときは、このディレクトリ全体ではなく該当モジュールだけを読むべきです。
- テストコードや別パッケージの実装を探しているときは、この配下ではありません。

## hash

- 4685f1abb42cd0edd196b0a8eca7f3d6a5d26174b7d42771c2cc34845f58e1c1

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

- `src/sub_commands` は cmoc のサブコマンド実装群の入口で、`__init__.py`、`init.py`、`eval_oracles.py`、`apply/`、`session/` をまとめるディレクトリです。
- `apply/` と `session/` はそれぞれ独自の `INDEX.md` を持つ配下ディレクトリで、個別コマンドの実装詳細はそこへルーティングします。
- この目次は、サブコマンド実装の全体構造を把握し、目的のモジュールや下位 INDEX へ最短でたどるための案内です。

## Read this when

- `src/sub_commands` 配下のサブコマンド実装の全体像と、どのファイルに何があるかを把握したいとき。
- `cmoc init`、`cmoc review oracles`、`cmoc apply`、`cmoc session` の入口ファイルを素早く見分けたいとき。
- 個別モジュールを読む前に、`sub_commands` ディレクトリの役割分担を整理したいとき。

## Do not read this when

- `src/sub_commands` 配下の特定ファイル 1 つだけの詳細仕様や処理順を確認したいとき。
- `cmoc apply` や `cmoc session` の状態遷移、引数、終了条件などを個別に追いたいとき。
- `cmoc review oracles` の評価ロジックや `init` の初期化手順だけを確認したいとき。

## hash

- e415ab19148746cd93d133c6d3f444cfe78c30339a25c777b11c44af119b243a
