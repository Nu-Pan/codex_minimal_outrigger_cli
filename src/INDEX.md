# `commons`

## Summary

- `src/commons` は、cmoc の複数サブコマンドから共通利用する基盤モジュール群をまとめたディレクトリです。
- `codex exec` 呼び出しの共通ラッパー、git リポジトリ操作、共通エラー整形、サブコマンドログ、経過時間計測、タイムスタンプ生成、`INDEX.md` 保守処理を収めています。
- `__init__.py` はパッケージ宣言のみで、実行ロジックや公開 API は持ちません。
- 個別サブコマンドの業務ロジックではなく、実装全体で再利用する横断的な処理の入口です。

## Read this when

- 複数のサブコマンドで共通に使う処理を探したいとき。
- `codex exec` の起動方法、Structured Output、リトライ、quota 待機、JSON 検証の実装を確認したいとき。
- `<repo-root>` の探索、git ブランチや `HEAD` 取得、`.cmoc` の追跡対象外保証、差分収集や commit 補助を調べたいとき。
- 共通エラーハンドリング、標準出力とファイルへのログ保存、ステップ単位の経過時間表示、タイムスタンプ形式を確認したいとき。
- `INDEX.md` の自動生成・更新に関わる共通処理を確認したいとき。

## Do not read this when

- 特定サブコマンドの入出力仕様や業務フローだけを知りたいとき。
- CLI のエントリーポイントや引数定義だけを調べたいとき。
- テスト実装や Fake Codex CLI の使い方だけを確認したいとき。
- `README.md`、`AGENTS.md`、`oracles` などの運用ルールだけを確認したいとき。

## hash

- 73a74cd42486d438c22fc5b94642204454e75f74dd1328941bacdf259f95f6c8

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

- `src/sub_commands` は cmoc のサブコマンド実装をまとめるルーティング用ディレクトリの目次です。
- 各サブコマンド本体の実装ファイルとして `apply.py`、`branch.py`、`init.py`、`eval_oracles.py`、`merge.py` を案内します。
- パッケージ境界を示す `__init__.py` も含め、サブコマンド実装群の入口を一箇所に集約します。
- このディレクトリはユーザー向け実行時仕様ではなく、実装ファイル同士の関連を把握するための案内です。
- 個別の処理順や入出力は各モジュールの `INDEX.md` または実装本体へ進みます。

## Read this when

- cmoc のサブコマンド実装がどのファイルに分かれているかを確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の本体実装へ進む入口が必要なとき。
- サブコマンド実装パッケージの境界や、どのモジュールがどの役割を持つかをざっと把握したいとき。
- 実装コードを読む前に、どのファイルを優先して読むべきか整理したいとき。

## Do not read this when

- cmoc 全体の開発ルール、コーディング規約、テスト規約だけを調べたいとき。
- 共通ユーティリティ、`commons` 配下、CLI エントリーポイントの仕様だけを知りたいとき。
- このディレクトリ全体ではなく、特定のサブコマンド 1 つの詳細仕様だけを確認したいとき。
- `README.md`、`AGENTS.md`、`oracles`、`memo` の運用ルールだけを確認したいとき。

## hash

- f482a345a236592985ceda9032bf35376becbbf13be37430f43f7c303b9d3735
