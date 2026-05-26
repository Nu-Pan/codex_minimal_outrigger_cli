# `commons`

## Summary

- `src/commons` にある cmoc 共通基盤モジュール群の入口です。CLI 実行制御、git リポジトリ操作、共通エラー整形、ログ、タイムスタンプ、経過時間計測、`INDEX.md` 生成・維持をまとめています。
- `command_runner.py` と `errors.py` はサブコマンド全体の実行制御と利用者向けエラーレポートを担います。
- `repo.py` は repo root 探索、ブランチ判定、session state、差分確認、`.cmoc` の無視保証、pathspec 単位の commit を扱います。
- `codex.py`、`indexing.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` は Codex 呼び出し、INDEX 生成、tee ログ、時刻文字列、ステップ計測をそれぞれ担当します。

## Read this when

- `src/main.py` やサブコマンドから呼ぶ共通処理の置き場所と責務を確認したいとき。
- `codex exec` の共通ラッパー、Structured Output 検証、quota 待機、再試行の流れを追いたいとき。
- git リポジトリのルート探索、session / apply ブランチ判定、`.cmoc` の無視保証、未コミット差分や commit の扱いを確認したいとき。
- エラーレポート、ログ保存、タイムスタンプ、経過時間表示、`INDEX.md` の生成・維持ルールを実装・修正したいとき。

## Do not read this when

- 個別サブコマンドの引数解析や業務ロジックだけを確認したいときは、`src/sub_commands` 側を直接読むべきです。
- `cmoc` の利用手順やユーザー向けコマンド説明だけが目的なら、この共有モジュール群は優先して読む必要はありません。
- `oracles` 配下の正本仕様そのものを確認したいときは、この実装ディレクトリではなく該当する仕様文書を読むべきです。
- テストコードだけで足りる、または `src/commons/__init__.py` のパッケージ宣言だけを確認したいときは、この目次は不要です。

## hash

- 9d86b490f4830b214240c020d024532b0d5408d8a1bb52e09f0d16acdf5529dc

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

- `cmoc` の個別サブコマンド実装をまとめたディレクトリの入口です。
- `apply.py`、`apply_abandon.py`、`apply_join.py`、`session_fork.py`、`session_join.py`、`session_abandon.py`、`init.py`、`eval-oracles.py` の各実装へ案内します。
- `__init__.py` は `src.sub_commands` パッケージを宣言する最小モジュールです。
- このディレクトリを起点に、各サブコマンドの本体処理、前提条件、状態遷移、後始末を素早くたどれるようにします。

## Read this when

- `cmoc` の個別サブコマンド実装の入口をまとめて確認したいとき。
- `apply`、`session`、`eval-oracles`、`init` のどの実装ファイルへ進むべきか整理したいとき。
- サブコマンドごとの実装本体、状態遷移、前提条件、終了処理の対応関係を俯瞰したいとき。
- `src/sub_commands` 配下のモジュール構成や、`main.py` から参照される実装の所在を把握したいとき。

## Do not read this when

- 個別サブコマンドの実装だけを確認したいときは、この目次ではなく該当する `apply.py`、`apply_abandon.py`、`apply_join.py`、`session_fork.py`、`session_join.py`、`session_abandon.py`、`init.py`、`eval-oracles.py` を直接読むべきです。
- `cmoc` の共通仕様や `oracles` 全体のルーティングだけを確認したいときは、このディレクトリではなく上位の `INDEX.md` や関連仕様を読むべきです。
- 実装コードやテストコードだけで足りる作業では、このディレクトリの案内を読む必要はありません。
- `__init__.py` のようなパッケージ宣言そのものだけを確認したいときは、他のサブコマンド実装を読む必要はありません。

## hash

- 10880ca8852f86330f8c78be6c7e3a62c1dc3f294a79d86cfc17bffb38436919
