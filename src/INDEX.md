# `commons`

## Summary

- cmoc のサブコマンドで共通利用するユーティリティ群をまとめたディレクトリです。
- Codex CLI 呼び出し、サブコマンド実行ラッパー、共通エラー、git リポジトリ操作、INDEX.md 生成、ログ、タイムスタンプ、経過時間計測の実装が入っています。
- 各サブモジュールは個別機能ごとに分かれており、`__init__.py` はパッケージ宣言のみを担当します。

## Read this when

- 複数のサブコマンドから使う共通処理を追加・修正したいとき。
- Codex CLI の呼び出し方、Structured Output、INDEX.md 生成、ログ保存、タイミング表示、git リポジトリ操作の仕様を確認したいとき。
- エラー整形や共通例外の扱いを確認したいとき。
- 共有処理をどのモジュールへ置くべきか判断したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを確認したいとき。
- `src/sub_commands` の実装や `src/main.py` の引数解釈だけを追いたいとき。
- 特定の共通処理 1 つだけを詳しく知りたいときは、このディレクトリ全体ではなく該当モジュールを直接読むべきです。
- `README.md`、`AGENTS.md`、`oracles`、`memo` の運用だけを確認したいとき。

## hash

- 0c67c0b50ddd4bd9b5e315f94472a56a5e818be2763e4965ad3c7d874825016a

# `main.py`

## Summary

- `src/main.py` は `cmoc` CLI の Typer エントリーポイントで、`init`、`session`、`apply`、`eval-oracles` のルーティングをまとめる。
- `eval-oracles` は `src/sub_commands/eval-oracles.py` を動的に読み込み、互換の hidden alias `eval-oracle` も登録する。
- `session fork / join / abandon` と `apply fork / join / abandon` の CLI 入口を定義し、前者は実装へ委譲、後者の `join` / `abandon` は未実装エラーを返す。
- `main()` は Typer / Click の例外を共通エラーレポートへ変換し、`python src/main.py` の直接起動経路も担う。

## Read this when

- `cmoc` のトップレベルコマンド登録と各サブコマンドへの委譲関係を確認したいとき。
- `eval-oracles` の動的読み込みや `eval-oracle` 互換 alias の扱いを確認したいとき。
- `NoArgsIsHelpError` を含む Typer / Click の parse error や、共通エラーレポートへの変換処理を追いたいとき。
- `python src/main.py` で直接実行した場合の起動経路を確認したいとき。

## Do not read this when

- `src/sub_commands` 配下の各サブコマンド本体の業務ロジックだけを確認したいとき。
- `commons.errors` の内部実装やエラーレポートの詳細だけを確認したいとき。
- `cmoc` の利用手順や `oracles` 側の正本仕様だけを確認したいとき。
- `apply` や `session` の個別処理の詳細を知りたいだけで、CLI 入口のルーティングは不要なとき。

## hash

- 85f01fb2466c77f6becadfc3100f40c8b58330c5a552a8a603165bcd42859c8e

# `sub_commands`

## Summary

- cmoc のサブコマンド実装をまとめたパッケージです。
- apply.py は oracle と実装の不整合調査・修正・レポート作成の実行本体です。
- eval-oracles.py は oracles の評価と結果レポート生成の実行本体です。
- init.py はリポジトリ初期化処理を担当し、session_fork.py / session_join.py / session_abandon.py は session の開始・完了・破棄を担当します。
- __init__.py はパッケージ初期化用の最小ファイルです。

## Read this when

- 各サブコマンドの実装フロー、分岐条件、補助関数の役割を確認したいとき。
- apply、eval-oracles、init、session 系のコマンド実装を修正・レビュー・テストしたいとき。
- branch、worktree、state ファイル、レポート生成などの処理をソースコード側から追いたいとき。

## Do not read this when

- 正本仕様だけを確認したいときは、`oracles/app_specs/sub_commands/INDEX.md` から該当文書へ進むべきです。
- 利用手順や概念整理だけが目的なら、`oracles/app_specs/usage.md` や `oracles/app_specs/INDEX.md` を読むべきです。
- 共通規約だけを見たいときは、`oracles/app_specs/branch_model.md`、`oracles/app_specs/codex_call.md`、`oracles/app_specs/indexing.md` などの別文書を読むべきです。

## hash

- 6b8fc27547e5581290af8e2338a3aeff11b635104438ea60d961f3249383ecb4
