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

- `cmoc` CLI の Typer エントリーポイントで、`init`、`session`、`apply`、`eval-oracles` のトップレベルルーティングを定義します。
- `session fork/join/abandon` と `apply fork/join/abandon` の CLI 入口を登録し、各サブコマンド実装への委譲をまとめています。
- `eval-oracles` は `src/sub_commands/eval-oracles.py` を動的読み込みし、互換の `eval-oracle` hidden alias も含めています。
- `main()` は Typer / Click の例外を `cmoc` 形式のエラーレポートへ変換し、`python src/main.py` の直接起動経路も担います。

## Read this when

- `cmoc` のトップレベルコマンド登録と、`init`、`session`、`apply`、`eval-oracles` のルーティング構成を確認したいとき。
- `session fork/join/abandon` や `apply fork/join/abandon` の CLI 入口がどこで登録されているかを確認したいとき。
- `eval-oracles` の動的読み込みや、互換用の hidden alias `eval-oracle` の扱いを確認したいとき。
- `NoArgsIsHelpError` を含む Typer / Click の例外を、`cmoc` 形式のエラーレポートへ変換する流れや、`python src/main.py` での直接起動経路を確認したいとき。

## Do not read this when

- 各サブコマンド本体の業務ロジックや状態遷移だけを確認したいときは、`src/sub_commands` 配下の該当モジュールを読むべきです。
- 共通エラー整形の内部実装や、`commons.errors` の詳細だけを追いたいときは、このファイルではなく共通モジュールを読むべきです。
- `cmoc` の利用手順や `oracles` 側の正本仕様だけを確認したいときは、この CLI  प्रवेश点ではなく該当文書を読むべきです。
- `apply` や `session` の個別処理そのものを見たいだけで、トップレベルのルーティングや起動処理が不要なときは読む必要がありません。

## hash

- 1d39a93edfb5c7866f8de10ccc4cb645f39cf6684d9ede63ee90507bed1e7431

# `sub_commands`

## Summary

- `src/sub_commands` ディレクトリの入口です。cmoc の各サブコマンド実装をまとめ、`apply`、`session`、`eval-oracles`、`init` の本体モジュールとパッケージ定義への案内を行います。
- このディレクトリでは `apply.py`、`apply_join.py`、`apply_abandon.py`、`session_fork.py`、`session_join.py`、`session_abandon.py`、`init.py`、`eval-oracles.py`、`__init__.py` が対象です。
- 各モジュールは対応するコマンドの実行本体と状態検証、cleanup、merge、report 出力などを担当します。

## Read this when

- cmoc のサブコマンド実装全体の配置や役割分担を確認したいとき。
- `apply`、`session`、`init`、`eval-oracles` のどの実装モジュールを読むべきか判断したいとき。
- パッケージ境界や `src/sub_commands` 全体のルーティングを整えたいとき。
- サブコマンド共通の入口を把握してから個別実装へ進みたいとき。

## Do not read this when

- 個別サブコマンドの詳細仕様だけを確認したいときは、このディレクトリ全体ではなく対応する `*.py` を直接読むべきです。
- `src/sub_commands` ではなく、`commons` など別ディレクトリの共通機能を調べたいときはこの目次は適していません。
- コマンドの利用方法や正本仕様だけを確認したいときは、`oracles/app_specs/sub_commands/INDEX.md` 側を参照すべきです。
- `__init__.py` のような最小モジュール単体の役割だけを確認したいときは、対象ファイルを直接読むべきです。

## hash

- caef25ce36a8d0894178865f7c06a5d19d91b7ab7573cfa1b4ce0b96f42c6525
