# `commons`

## Summary

- `src/commons` は、cmoc 全体で共有する基盤処理をまとめたディレクトリです。
- `codex exec` の呼び出しラッパー、共通エラー整形、サブコマンド実行制御、時間計測、タイムスタンプ生成、標準入出力ログ、`<repo-root>` 探索や変更収集、`INDEX.md` 自動生成を扱います。
- CLI の各サブコマンド本体から直接使われる共通ユーティリティと、リポジトリ状態に依存する補助処理を集約しています。
- このディレクトリは、個別サブコマンドの業務ロジックではなく、複数機能で再利用される共通層の入口として読むのが適切です。

## Read this when

- `cmoc` の共通基盤として、どのモジュールが何を担うか確認したいとき。
- `codex exec` の呼び出し、Structured Output、リトライ、quota 回復待ちの扱いを確認したいとき。
- 共通エラー表示、終了コード、`typer.Exit` への変換、サブコマンド全体の実行制御を確認したいとき。
- `<repo-root>` の探索、`.cmoc` の追跡外保証、変更差分の収集、`INDEX.md` の生成・更新ルールを確認したいとき。
- 標準出力・標準エラー出力のログ保存、経過時間表示、タイムスタンプ生成の共通仕様を確認したいとき。

## Do not read this when

- 個別サブコマンドの入出力仕様や業務ロジックだけを知りたいとき。
- `oracles` 配下の正本仕様断片や、ユーザー向け実行時仕様だけを追いたいとき。
- `src/commons` 以外の実装ファイルやテストファイルの構成を確認したいとき。
- `README.md`、`AGENTS.md`、`memo` などの運用ルールだけを確認したいとき。
- このディレクトリの共通処理ではなく、特定のサブコマンド専用の仕様を直接読みたいとき。

## hash

- 6700090e8b8d8722768bbb846fd316a8a1b7ba2e6b741c5d65da3e8139aac71a

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

- `src/sub_commands` 配下の cmoc サブコマンド実装へのルーティング用目次です。
- `__init__.py` と `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の各実装ファイルへの入口をまとめます。
- 各サブコマンドの処理順、前提条件、入出力、共通制御の詳細を探すときの最初の案内役になります。

## Read this when

- `src/sub_commands` 配下のどの実装ファイルを読むべきか判断したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の本体実装の場所を知りたいとき。
- サブコマンド実装パッケージの境界や、各モジュールの役割をざっと確認したいとき。
- サブコマンド横断の実装フローや、個別処理のつながりを追いたいとき。

## Do not read this when

- `oracles` 側の正本仕様だけを調べたいとき。
- 開発者向けのコーディング規約、設計規約、テスト規約、開発環境だけを確認したいとき。
- CLI の実行時仕様ではなく、ルーティングや文書構成の変更可否だけを確認したいとき。
- サブコマンドの個別挙動が既に分かっていて、このディレクトリ全体の案内が不要なとき。

## hash

- 435bb2b8ce6c73bdd728ba592c7b8c93ca3df7bb5828f2f17a8542e2f485117a
