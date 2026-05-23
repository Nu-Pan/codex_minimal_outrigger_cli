# `commons`

## Summary

- `src/commons` は cmoc 全体で共有する基盤処理を集約するディレクトリです。
- `codex exec` 呼び出し、`INDEX.md` 自動生成、git リポジトリ操作、共通エラー処理、サブコマンド実行制御、ログ、タイムスタンプ、経過時間表示を担当します。
- CLI 本体や各サブコマンドから横断的に再利用される共通ユーティリティ群として位置づけられます。

## Read this when

- `codex exec` の共通ラッパー、Structured Output、再試行、quota 待機、出力検証の実装を確認したいとき。
- `<repo-root>` 探索、`.cmoc` の追跡外保証、未コミット差分の確認、部分評価・部分適用のための git 操作を確認したいとき。
- サブコマンド実行時の標準出力・標準エラーの tee、ログファイル保存、待機時間の累積を確認したいとき。
- サブコマンドの終了コード処理、例外の共通レポート、Typer との接続を確認したいとき。
- `<time-stamp>` の生成や経過時間表示など、横断的な時間系ユーティリティを確認したいとき。
- `INDEX.md` の自動生成、再利用、更新、ハッシュ管理の共通処理を確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数定義だけを確認したいとき。
- `oracles` の正本仕様や各サブコマンド仕様の本文を読みたいとき。
- `README.md`、`AGENTS.md`、`memo` などの運用ルールだけを確認したいとき。
- 具体的な実装ファイルの配置やテストコードの場所だけを探したいとき。
- 共通処理ではなく、`src` の別パッケージの仕様を確認したいとき。

## hash

- 65a81084ea8233f81827007259e848f68128f1e41ddc0438c893c036f21539b3

# `main.py`

## Summary

- `cmoc` CLI の Typer エントリーポイントを定義するファイルです。
- `init`、`branch`、`eval-oracles`、`apply`、`merge` を `app` に登録し、それぞれ対応する `src/sub_commands` 実装へ処理を委譲します。
- `main()` で Typer / Click の起動を包み、parse error や想定外例外を共通エラーレポート形式に整えて終了コードを決めます。
- `python src/main.py` で直接実行された場合の起動経路も、このファイルでまとめています。

## Read this when

- `cmoc` のトップレベルコマンド一覧と、各サブコマンドの登録箇所を確認したいとき。
- 各コマンドがどの `src/sub_commands` 実装関数へ渡されるかを調べたいとき。
- `apply` の `--repeat` や `--full`、`eval-oracles` の `--full` などの Typer 引数定義や既定値を確認したいとき。
- Typer / Click の parse error、`NoArgsIsHelpError`、想定外例外がどのように終了コード付きのエラーレポートへ変換されるか確認したいとき。
- `app` オブジェクトや `main()` の起動条件、`python src/main.py` での直接実行時挙動を調べたいとき。

## Do not read this when

- 各サブコマンドの業務ロジックや `src/sub_commands` 配下の本体実装を追いたいとき。
- 共通エラーレポートの本文生成や `commons.errors` の内部を詳しく確認したいとき。
- `INDEX.md` 自動生成、repo 探索、ログ保存などの共通基盤の仕様を調べたいとき。
- `cmoc` の利用手順全体や各サブコマンドの正本仕様を知りたいとき。

## hash

- d8532edf006b5e6a2d51210f24708a8edb537cc004a848ebe834777bdb456caa

# `sub_commands`

## Summary

- `src/sub_commands` は、cmoc の各サブコマンド本体実装を集めたルーティング用ディレクトリです。
- `__init__.py` はパッケージ境界を示す最小ファイルで、実行ロジックは持ちません。
- `init.py`、`branch.py`、`apply.py`、`eval_oracles.py`、`merge.py` に、それぞれ `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の本体実装があります。
- この目次は、個別サブコマンドの実装入口を素早く見つけるための案内です。

## Read this when

- 特定のサブコマンド実装が `src` のどのファイルにあるか確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の実装位置を一覧したいとき。
- サブコマンド実装パッケージの境界や、各モジュールの役割を把握したいとき。
- 実装コードを読む前に、どのファイルから追い始めるべきか判断したいとき。

## Do not read this when

- 個別サブコマンドの引数、詳細な実行手順、終了条件だけを知りたいときは、対応するモジュールを直接読むほうがよいとき。
- cmoc 全体の設計規約、テスト規約、開発環境ルールだけを調べたいとき。
- CLI の共通ルーティングや共通ヘルパーの仕様だけを確認したいとき。
- `README.md`、`AGENTS.md`、`oracles` の運用ルールだけを確認したいとき。

## hash

- 72cedd67d728075b0bdaf20765e58c0d354b15d0bbd4581a47e5105b14086676
