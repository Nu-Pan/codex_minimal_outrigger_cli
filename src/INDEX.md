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

- `src/sub_commands` 配下の cmoc サブコマンド本体実装へのルーティング用目次です。
- `apply.py`、`branch.py`、`eval_oracles.py`、`init.py`、`merge.py` に、それぞれ `cmoc apply` などの実処理が分かれています。
- `__init__.py` はサブコマンド実装パッケージであることを示す最小限の初期化ファイルです。

## Read this when

- 各サブコマンドの本体実装がどのファイルにあるか確認したいとき。
- `apply`、`branch`、`eval-oracles`、`init`、`merge` のどれを読むべきか切り分けたいとき。
- サブコマンド実装パッケージ全体の構成を把握したいとき。

## Do not read this when

- 共通ユーティリティや CLI エントリーポイントの実装だけを調べたいとき。
- `oracles` の正本仕様や `INDEX.md` 自動生成ルールだけを調べたいとき。
- `cmoc` 自体の開発規約、設計規約、テスト規約だけを確認したいとき。
- すでに個別サブコマンドの実装ファイルが分かっていて、所在確認が不要なとき。

## hash

- 6ff3c5218a6001243286eb527dd9f0a5ed981eff536ef9c08b3bf4b9ad78541f
