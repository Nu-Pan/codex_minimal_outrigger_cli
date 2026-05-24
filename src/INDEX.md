# `commons`

## Summary

- `src/commons` は、cmoc 全体で共有する基盤処理の目次です。Codex CLI 呼び出し、共通エラー処理、repo / git 操作、`INDEX.md` 自動生成、サブコマンドログ、タイムスタンプ、経過時間計測への入口をまとめます。
- このディレクトリは `__init__.py`、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` に分かれています。
- `codex.py` は `codex exec` の共通ラッパー、`command_runner.py` は CLI サブコマンドの共通実行制御、`errors.py` は共通例外とエラーレポート整形を扱います。
- `indexing.py` は `<repo-root>` 配下の `INDEX.md` を列挙・生成・更新し、`repo.py` は repo root 探索や git 操作、`subcommand_log.py` は tee ログ、`timestamps.py` は `<time-stamp>`、`timing.py` はステップ別経過時間を担当します。

## Read this when

- 共通処理のうち、どのモジュールを読むべきか迷ったとき。
- `codex exec` の引数、Structured Output、リトライ、JSON 検証、ログ保存の共通仕様を確認したいとき。
- 共通エラーハンドリング、`<repo-root>` 探索、git 操作、`INDEX.md` メンテナンス、サブコマンドログ、タイムスタンプ、経過時間表示を確認したいとき。
- CLI サブコマンドの共通実行制御や、`typer.Exit` を含む終了コードの扱いを確認したいとき。
- `src/commons` 全体の役割を、パッケージ境界として把握したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを調べたいとき。
- `src` 全体や `tests` 全体の設計方針、コーディング規約、開発環境ルールだけを調べたいとき。
- `README.md`、`AGENTS.md`、`oracles`、`memo` などのリポジトリ運用ルールだけを確認したいとき。
- 特定の共通モジュールの実装詳細だけを追いたいときで、このディレクトリ全体の案内が不要なとき。
- サブコマンドごとの正本仕様やユーザー向け実行時仕様だけを確認したいとき。

## hash

- bb3896a736ba2f0fbda175bcc5e29e43c4bc179b665713758d81dedd74a1e863

# `main.py`

## Summary

- `cmoc` CLI の Typer エントリーポイントとサブコマンド登録をまとめる目次です。
- `init`、`branch`、`eval-oracles`、`apply`、`merge` の各コマンド定義と、対応する `src/sub_commands` 実装への委譲関係を案内します。
- Typer / Click の parse error、`NoArgsIsHelpError`、想定外例外を共通エラーレポートへ変換して終了コードを決める処理への入口です。
- `python src/main.py` で直接起動される経路も含めて、CLI 起動全体の入口を整理します。

## Read this when

- `cmoc` のトップレベルコマンド一覧や、各サブコマンドの登録箇所を確認したいとき。
- 各コマンドがどの `src/sub_commands` の実装関数へ渡されるかを調べたいとき。
- `apply` の `--repeat`、`--repeat-inveatigate-and-fix`、`--full` などの引数定義や既定値を確認したいとき。
- `eval-oracles` の `--full` や `eval-oracle` の互換 alias を含む CLI 挙動を確認したいとき。
- Typer / Click の parse error や想定外例外が、どのようにエラーレポートと終了コードへ変換されるか確認したいとき。
- `app` オブジェクトや `main()` の起動条件、`python src/main.py` での直接実行時挙動を調べたいとき。

## Do not read this when

- 各サブコマンドの業務ロジックや `src/sub_commands` 配下の本体実装を追いたいとき。
- 共通エラーレポートの本文生成や `commons.errors` の内部を詳しく確認したいとき。
- `src/commons` の共通基盤仕様や `INDEX.md` 自動生成など、CLI 入口以外の横断仕様を調べたいとき。
- `cmoc` の利用手順全体や、`oracles` 側の正本仕様そのものを知りたいとき。

## hash

- cb380259debbaae71cb88e4b9959201e67bf14dedef7073dec0c842bc4ad9a8b

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc のサブコマンド実装をまとめるパッケージの目次です。
- `__init__.py` はパッケージの入口、`apply.py` は `cmoc apply`、`branch.py` は `cmoc branch`、`eval_oracles.py` は `cmoc eval-oracles`、`init.py` は `cmoc init`、`merge.py` は `cmoc merge` を担当します。
- `apply.py` は oracle と実装の差分検出から修正適用、レポート保存までを扱い、`eval_oracles.py` は oracle 断片の評価と Markdown レポート生成を扱います。
- `branch.py` は作業ブランチ作成と base commit 記録を扱い、`init.py` は `.cmoc` の ignore 保証と初期化変更の commit を扱います。
- `merge.py` は cmoc ブランチの merge、conflict 解消依頼、必要時のブランチ削除を扱います。

## Read this when

- `src/sub_commands` 配下のどのファイルがどのサブコマンドに対応するかを確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の個別実装の入口を探したいとき。
- 新しいサブコマンド実装をこのパッケージに追加するとき。
- 各サブコマンドの責務分担をざっと把握して、読むべき実装ファイルを切り分けたいとき。

## Do not read this when

- CLI 引数の定義やエントリーポイントの登録方法だけを知りたいとき。
- `commons` の共通処理や `oracles` の正本仕様そのものを調べたいとき。
- 開発規約、テスト規約、環境規約だけを確認したいとき。
- 対象サブコマンドの個別ファイルがすでに決まっていて、この目次だけでは判断が不要なとき。

## hash

- 16f3dc24027bbeb888b7cb1a00ee2a93824e6a70b0449c371eef613fe549254b
