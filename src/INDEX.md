# `commons`

## Summary

- `src/commons` は、cmoc 自体の CLI 実行を支える共通ユーティリティ群のルーティング用ディレクトリです。
- `codex.py` は `codex exec` の呼び出し、Structured Output、JSON 検証、リトライ、quota 待機と resume の共通処理をまとめます。
- `repo.py` は `<repo-root>` の探索、git 状態確認、`.cmoc` の追跡外保証、初期化やブランチ関連の共通検査を扱います。
- `errors.py`、`subcommand_log.py`、`timing.py`、`timestamps.py`、`command_runner.py` は、共通エラー表示、ログ保存、経過時間計測、時刻文字列生成、サブコマンド実行制御を分担します。
- `indexing.py` は各ディレクトリの `INDEX.md` を自動生成・更新するための入口です。

## Read this when

- cmoc の共通処理を実装・修正していて、責務ごとの入口を素早く見つけたいとき。
- Codex CLI の呼び出し方、JSON 応答の扱い、再試行や quota 待機の流れを確認したいとき。
- `<repo-root>` の探索、git 状態確認、`.cmoc` の ignore 保証、初期化時の検査を追いたいとき。
- 共通のエラーレポート、サブコマンドログ、タイミング表示、タイムスタンプ、`INDEX.md` 自動保守の仕様を確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数仕様だけを調べたいとき。
- `oracles` の正本仕様や、ユーザー向け実行時仕様の全体ルーティングだけを見たいとき。
- `src/commons` 以外の実装コードやテストコードの場所を探しているとき。
- README、AGENTS、memo の運用ルールや編集可否だけを確認したいとき。

## hash

- 0cc076fe4f9470e84c0fde81c044c01c6c7b900e53c84e7bb93d0debc4a2d699

# `main.py`

## Summary

- `cmoc` CLI の Typer エントリーポイントを定義するファイルです。
- `init`、`branch`、`eval-oracles`、`apply`、`merge` を `app` に登録し、それぞれ対応する `sub_commands` 実装へ処理を委譲します。
- `main()` で Typer / Click の起動を包み、parse error や想定外例外を共通エラーレポート形式に整えて終了コードを決めます。
- `python src/main.py` で直接実行された場合の起動経路も、このファイルでまとめています。

## Read this when

- `cmoc` のトップレベルコマンド一覧と、各サブコマンドの登録箇所を確認したいとき。
- 各コマンドがどの `sub_commands` 実装関数へ渡されるかを調べたいとき。
- `apply` の `--repeat` や `--full`、`eval-oracles` の `--full` などの Typer 引数定義や既定値を確認したいとき。
- Typer / Click の parse error、`NoArgsIsHelpError`、想定外例外がどのように終了コード付きのエラーレポートへ変換されるか確認したいとき。
- `app` オブジェクトや `main()` の起動条件、`python src/main.py` での直接実行時挙動を調べたいとき。

## Do not read this when

- 各サブコマンドの業務ロジックや `src/sub_commands` 配下の本体実装を追いたいとき。
- 共通エラーレポートの本文生成や `commons.errors` の内部を詳しく確認したいとき。
- `INDEX.md` 自動生成、repo 探索、ログ保存などの共通基盤の仕様を調べたいとき。
- `cmoc` の利用手順全体や各サブコマンドの正本仕様を知りたいとき。

## hash

- 0332175dfe26d12c8c9399d5f7bf9d97c1aaf35044ca0eb67fbe696644a3d041

# `sub_commands`

## Summary

- `src/sub_commands` は、cmoc のサブコマンド実装をまとめるパッケージです。
- `init`、`branch`、`apply`、`eval_oracles`、`merge` の各サブコマンド本体を個別モジュールとして配置しています。
- `__init__.py` はパッケージ境界を示す最小ファイルで、実行ロジックは持ちません。
- このディレクトリは、各サブコマンドの実装入口を追うための目次として使います。

## Read this when

- 特定のサブコマンド実装が `src` のどのファイルにあるか確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の実装位置を一覧したいとき。
- サブコマンド実装パッケージの境界や、各モジュールの役割を把握したいとき。
- 実装コードを読む前に、どのファイルから追い始めるべきか判断したいとき。

## Do not read this when

- 個別サブコマンドの引数、詳細な実行手順、終了条件だけを知りたいときは、対応するモジュールを直接読むほうがよいです。
- cmoc 全体の設計規約、テスト規約、開発環境ルールだけを調べたいとき。
- CLI の共通ルーティングや共通ヘルパーの仕様だけを確認したいとき。
- `README.md`、`AGENTS.md`、`oracles` の運用ルールだけを確認したいとき。

## hash

- 7a31b1b1517ddad594c0ac81782392141b5c12cd278192b5acf7a27b12075a23
