# `commons`

## Summary

- cmoc 全体で共有する基盤モジュール群をまとめたディレクトリです。
- Codex CLI 呼び出し、サブコマンド実行制御、git リポジトリ/作業ツリー操作、共通例外処理、`INDEX.md` メンテナンス、ログ出力、経過時間計測、タイムスタンプ生成などを扱います。

## Read this when

- cmoc 全体で共通に使う処理の所在を確認したいとき。
- Codex CLI の起動、Structured Output の検証、再試行、quota 待機の流れを追いたいとき。
- git リポジトリ探索、session/apply ブランチ、worktree、`.cmoc` 配下の状態管理を確認したいとき。
- 共通エラー整形、サブコマンドログ、経過時間計測、レポートファイル保存、`INDEX.md` 自動メンテナンスを確認したいとき。

## Do not read this when

- 個別サブコマンドの引数解釈や業務ロジックだけを追いたいとき。
- tests や CLI エントリーポイントだけを確認したいとき。
- このディレクトリの共通基盤ではなく、特定コマンド側の実装や仕様だけを確認したいとき。
- README や上位の仕様文書だけを確認したいとき。

## hash

- 375792a8fb6750151276fff85d16fab382e43656931a2ee9e364db7754b11972

# `main.py`

## Summary

- cmoc CLI のエントリーポイントで、Typer のルート `app` と `session` / `apply` / `review` の各サブアプリを組み立てるファイルです。
- `init`、`session`、`apply`、`review` の各コマンド登録に加えて、`eval-oracle` / `eval-oracles` の隠し別名や各コマンドの既定オプションをまとめています。
- サブコマンド未指定時の `CmocError` 生成、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc CLI の起点と、`session` / `apply` / `review` のサブアプリ構成を確認したいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録名や隠し別名を確認したいとき。
- `apply fork` の繰り返し回数や `scope`、`apply join` の `--force-resolve` など既定オプションを確認したいとき。
- サブコマンド未指定時の利用者向けエラー、補完プローブ時の分岐、Click/Typer 例外の共通整形を追いたいとき。
- `python src/main.py` で直接起動する経路と、そのときの例外処理を確認したいとき。

## Do not read this when

- `src/sub_commands/` 配下の個別サブコマンド本体だけを確認したいとき。
- `commons.errors` の例外型や `format_error_report()` の整形ロジックだけを確認したいとき。
- CLI 登録や補完、例外変換ではなく、各機能の業務ロジックそのものを追いたいとき。
- `INDEX.md` の生成ルールや `oracles` 側の正本仕様だけを確認したいとき。

## hash

- 1a1bb5753238e77dc6df1252d876b3fc6c7cc1706bd8b8499554963755c0a4d7

# `sub_commands`

## Summary

- `src/sub_commands` は `cmoc` のサブコマンド実装をまとめる入口ディレクトリです。
- `__init__.py` はパッケージ宣言だけを担う最小モジュールです。
- `init.py` は `cmoc init` の本体処理です。
- `apply/` は `cmoc apply` 系、`review/` は `cmoc review oracles`、`session/` は `cmoc session` 系の実装入口です。

## Read this when

- `src/sub_commands` 配下の入口ファイルと、どの実装へ進むべきかを整理したいとき。
- `cmoc init`、`cmoc apply`、`cmoc review oracles`、`cmoc session` のどの実装ファイルを開くべきかを素早く判断したいとき。
- `src/sub_commands` の配下にある `apply/`、`review/`、`session/`、`init.py`、`__init__.py` の役割分担を俯瞰したいとき。
- 実装・修正・レビュー・テストを始める前に、このディレクトリのルーティングだけ把握したいとき。

## Do not read this when

- `src/sub_commands` 全体の入口構造ではなく、`cmoc` の個別サブコマンド 1 本だけを追いたいときは、この目次ではなく対応する実装モジュールを直接読むべきです。
- `cmoc apply`、`cmoc review oracles`、`cmoc session` のいずれかの詳細実装を確認したいだけのときは、この目次ではなく各サブディレクトリの `INDEX.md` を読むべきです。
- `src/sub_commands` のパッケージ宣言だけを確認したいときは、この目次ではなく `__init__.py` を直接読むべきです。
- 利用手順や仕様断片だけを確認したいときは、この目次ではなく `oracles` 側の正本仕様を読むべきです。

## hash

- 3bf38f19dbc44cd0302c29d14881f6ffcd33d4785c3927029991846f27ba146b
