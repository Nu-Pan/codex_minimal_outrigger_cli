# `commons`

## Summary

- `src/commons` は、cmoc のサブコマンド実装から共有される横断ユーティリティをまとめる Python パッケージです。
- Codex CLI 呼び出し、Structured Output 検証、ログ保存、INDEX.md 自動メンテナンス、共通エラー整形、Typer 実行ラッパー、git リポジトリ操作、タイムスタンプ生成、ステップ時間計測を扱います。
- `codex.py` は `codex exec` 実行、サンドボックス指定、schema ファイル保存、最大 3 回の JSON 検証リトライ、ログ出力、JSON object パースを提供します。
- `indexing.py` は INDEX 配置対象の列挙、除外規則、内容ハッシュ比較、既存目次再利用、Structured Output による目次生成、INDEX 更新差分の自動コミットを実装します。
- `repo.py` は `<repo-root>` 探索、カレントディレクトリ移動、git 状態確認、`.cmoc` 追跡対象外保証、oracle ファイル列挙、cmoc ブランチ情報、共通 git 実行を提供します。
- `errors.py`、`command_runner.py`、`timestamps.py`、`timing.py` は、それぞれ共通エラー型とレポート、CLI 実行制御、仕様タイムスタンプ、サブコマンドの経過時間表示を担当します。

## Read this when

- cmoc の複数サブコマンドで共有する処理がどのモジュールにあるか判断したいとき。
- サブコマンドの Typer 関数から本体処理を呼び出す共通ラッパー、`<repo-root>` 解決、例外から終了コードへの変換を確認したいとき。
- Codex CLI 呼び出し、read-only / workspace-write サンドボックス指定、Structured Output schema、JSON 検証リトライ、`.cmoc/logs/codex_exec` のログ保存を調べたいとき。
- INDEX.md の自動生成・更新、対象ディレクトリや除外対象、既存目次の再利用、Codex への目次生成依頼、自動コミット処理を確認したいとき。
- git リポジトリルート探索、現在ブランチや HEAD commit の取得、未コミット差分検査、`.cmoc` の gitignore 保証、oracle ファイル列挙を利用または修正したいとき。
- cmoc 共通の `CmocError`、利用者向けエラーレポート、復旧アクション、詳細情報、コールスタック表示の形式を確認したいとき。
- ログ名・ブランチ名・ファイル名などに使う `<time-stamp>` 形式や、サブコマンドのステップ別タイミング表示を実装・検証したいとき。

## Do not read this when

- 個別サブコマンドのユーザー向け仕様、CLI オプション、具体的な業務フローだけを調べたいとき。
- cmoc の正本仕様断片を読むべき場面で、`oracles` 配下の仕様ルーティングや個別仕様ファイルを探しているとき。
- Python コーディング規約、テスト規約、開発環境ルールなど、実装者向けルールだけを確認したいとき。
- README、AGENTS、oracles、memo などの編集可否やリポジトリ運用ルールだけを確認したいとき。
- cmoc を用いて別リポジトリを開発する際の `<repo-root>` 側アプリケーションコードや、そのリポジトリ固有の設計を調べたいとき。
- テストコード、Fake Codex CLI、pytest fixture、期待出力など、自動テストの具体的な実装だけを探しているとき。

## hash

- 995b21f5b7250c7c39ee82b27c88fd58569f55b9a6aba3578203ef0cb3a957f7

# `main.py`

## Summary

- cmoc の Typer ベース CLI エントリーポイントを定義するファイル。
- `cmoc` アプリケーション本体 `app` を生成し、`init`、`branch`、`eval-oracles`、`apply`、`merge` の各サブコマンドを登録している。
- 各 CLI callback は引数やオプションを受け取り、実処理を `sub_commands` 配下の `cmoc_*_impl` 関数へ委譲する薄い層になっている。
- `eval-oracles` は `--full` / `-f`、`apply` は `--repeat` / `-r`、`merge` は任意の `cmoc_branch` 引数を受け取る。
- `main()` は Typer/Click の parse error や想定外例外を `commons.errors.format_error_report` に通し、共通エラーレポート形式で表示して終了コードへ変換する。
- `python src/main.py` で直接実行された場合も `main()` を呼び出して CLI を起動する。

## Read this when

- cmoc の CLI エントリーポイント、Typer アプリ定義、サブコマンド登録の入口を確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` がどの実装関数へ委譲されるか調べたいとき。
- 各サブコマンドの CLI 引数やオプションの受け取り部分だけを確認したいとき。
- Typer/Click の例外、parse error、想定外例外が cmoc の共通エラーレポートへ変換される起動時処理を調べたいとき。
- `python src/main.py` による直接起動経路や `main()` の役割を確認したいとき。

## Do not read this when

- 各サブコマンドの本体処理、git 操作、Codex CLI 呼び出し、ファイル生成などの詳細実装を調べたいとき。
- `init`、`branch`、`eval-oracles`、`apply`、`merge` の個別仕様や業務ロジックを確認したいとき。
- 共通エラーレポートのフォーマット実装そのものを調べたいとき。
- oracle 仕様、開発ルール、テスト規約など、実装コード以外の正本仕様を調べたいとき。
- cmoc を用いて開発する `<repo-root>` 側の `INDEX.md` や oracle ファイルの内容を調べたいとき。

## hash

- fc72184fc2aef64cc56fcf0c5246e84532705ced92ba255d0e90e39f6630e15e

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc の各サブコマンド本体実装を置くパッケージです。
- `__init__.py` はサブコマンド実装パッケージであることを示すだけの初期化ファイルです。
- `init.py` は `cmoc init` の実装で、`.cmoc` を git 追跡対象外にする保証、初期化差分のコミット、2段階の進捗表示と時間レポートを扱います。
- `branch.py` は `cmoc branch` の実装で、`cmoc_<timestamp>` 形式の作業ブランチ作成、衝突時リトライ、`.cmoc` ignore 保証、作成元 commit の `.cmoc/branch` 記録を扱います。
- `eval-oracles.py` は `cmoc eval-oracles` の実装で、`.cmoc` ignore 保証、`INDEX.md` メンテナンス、部分評価または全体評価の対象 oracle 選択、Codex CLI による oracle 評価、Markdown レポート保存を扱います。
- `apply.py` は `cmoc apply` の実装で、cmoc ブランチ制約、oracle 外差分の拒否、`INDEX.md` メンテナンス、oracle と実装の不整合調査、Codex CLI による実装修正、禁止パス検査、コミット、apply レポート生成を扱います。
- `merge.py` は `cmoc merge` の実装で、未コミット差分確認、merge 元 cmoc ブランチ解決、`git merge --no-ff`、conflict 時の Codex CLI 解消依頼、marker 残存検査、merge commit、source branch の安全な削除を扱います。
- 各サブコマンドは主に `commons.command_runner`、`commons.repo`、`commons.codex`、`commons.indexing`、`commons.timing`、`commons.timestamps` などの共通処理を組み合わせ、ユーザー向け進捗表示と実行フローを制御します。

## Read this when

- cmoc の個別サブコマンド本体がどのファイルに実装されているか判断したいとき。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` の実行フローや責務を確認したいとき。
- サブコマンドごとの stdout 進捗表示、StepTimer による時間計測、レポート生成、コミット処理の呼び出し箇所を追いたいとき。
- サブコマンドが共通ユーティリティとどう接続しているか、特に repo root 解決、git 操作、`.cmoc` ignore 保証、Codex CLI 呼び出し、`INDEX.md` メンテナンスとの連携点を調べたいとき。
- oracle 評価、oracle と実装の不整合追従、merge conflict 解消など、Codex CLI をサブコマンドから呼び出す具体的なプロンプトや実行条件を確認したいとき。
- サブコマンド実装に対するテストを書くために、直接呼び出し可能な `cmoc_*_impl` 関数や補助関数の責務を把握したいとき。

## Do not read this when

- CLI エントリーポイントや argparse へのサブコマンド登録方法だけを調べたいとき。
- repo root 探索、git コマンドラッパー、Codex CLI 共通実行、Structured Output パース、`INDEX.md` 自動生成、タイマー、タイムスタンプなど、共通処理の内部実装だけを調べたいとき。
- cmoc の正本仕様断片やユーザー向け仕様だけを確認したいとき。
- cmoc 自体の開発規約、テスト規約、環境構築、README、AGENTS の編集可否など、リポジトリ運用ルールだけを確認したいとき。
- `tests` 配下の pytest 実装や Fake Codex CLI の詳細を調べたいとき。
- `__pycache__` 配下の Python バイトコードや生成物を調べようとしているとき。

## hash

- 692d5340418aefa4fec7b535cd3caac986a1ad47771e66c0365654280790dccb
