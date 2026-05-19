# `commons`

## Summary

- cmoc のサブコマンド実装から共有される横断的な Python 共通モジュール群です。
- Codex CLI 呼び出し、Structured Output 検証、`INDEX.md` 自動メンテナンス、git リポジトリ操作、`.cmoc` の追跡対象外保証、共通エラー整形、Typer サブコマンド実行ラッパー、タイムスタンプ生成、ステップ時間計測を扱います。
- 個別サブコマンドの業務ロジックではなく、`src/commands` などから再利用される基盤処理を集約しています。
- `__init__.py` はパッケージ宣言のみで、実処理は `codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`timestamps.py`、`timing.py` に分かれています。
- `__pycache__` は Python 実行時のキャッシュであり、設計や実装調査の対象ではありません。

## Read this when

- cmoc のサブコマンド間で共通利用される実行制御や補助処理の入口を探したいとき。
- `codex exec` の呼び出し方法、sandbox 指定、ログ保存、Structured Output schema、JSON parse・検証・リトライの実装を確認したいとき。
- `INDEX.md` の配置対象列挙、除外規則、内容ハッシュに基づく再利用、Codex CLI による目次生成、Markdown ブロック生成、自動コミットの流れを調べたいとき。
- `<repo-root>` 探索、cwd 移動、git ブランチ・HEAD 取得、未コミット差分検査、oracle ファイル列挙、`.cmoc` ignore 保証など、git リポジトリ周辺の共通処理を確認したいとき。
- cmoc 固有の `CmocError`、stdout 向けエラーレポート、終了コード変換、Typer サブコマンド本体の共通ラップ処理を調べたいとき。
- ログ名やブランチ名などで使う `<time-stamp>` 文字列の生成形式、またはサブコマンドのステップ別経過時間レポートを確認したいとき。
- 新しいサブコマンドを実装する際に、既存の共通ユーティリティへ委譲すべき処理がないか確認したいとき。

## Do not read this when

- 個別サブコマンドのユーザー向け仕様、引数、プロンプト、正常系ワークフローだけを調べたいとき。
- cmoc の正本仕様断片そのものを確認したいとき。仕様調査では `oracles` 配下の適切な `INDEX.md` から辿る必要があります。
- README、AGENTS、oracles、memo などの編集可否やリポジトリ運用ルールだけを確認したいとき。
- テストコードの具体的な fixture、Fake Codex CLI、期待値、pytest 構成だけを調べたいとき。
- Python パッケージであることだけを確認できれば十分で、共通処理の実装詳細が不要なとき。
- Codex CLI、git、Typer、JSON Schema、subprocess など外部技術の一般的な使い方だけを知りたいとき。
- `__pycache__` など生成物や実行時キャッシュの内容を調べようとしているとき。

## hash

- 92995819e6337a34c0615d3749c2e2ee250b7f4545d58c9152bd3fe6284aef90

# `main.py`

## Summary

- cmoc CLI の Typer エントリーポイントを定義するファイルです。
- `init`、`branch`、`eval-oracles`、`apply`、`merge` の各サブコマンドを Typer コマンドとして登録し、実処理を `sub_commands` 配下の実装関数へ委譲します。
- `main()` では `app(standalone_mode=False)` を起動し、Typer/Click の終了・パース例外および想定外例外を cmoc 共通のエラーレポート形式へ変換して終了コードを返します。
- スクリプトとして直接実行された場合は `src` ディレクトリを `sys.path` に追加してから `main()` を呼び出します。

## Read this when

- cmoc の CLI にどのサブコマンドが登録されているか確認したいとき。
- 新しいサブコマンドを追加し、Typer のコマンド関数から `sub_commands` 配下の実装へ接続したいとき。
- `eval-oracles --full` や `merge [cmoc_branch]` など、トップレベル CLI 引数・オプションの定義場所を探しているとき。
- Click/Typer のパースエラーや想定外例外が、共通エラーレポートと終了コードに変換される入口を確認したいとき。
- `bin/cmoc` や直接実行経路から cmoc アプリケーションが起動される流れを追いたいとき。

## Do not read this when

- 各サブコマンドの具体的な処理内容、git 操作、Codex CLI 呼び出し、ファイル生成内容を調べたいとき。
- 共通エラーレポートの文面や整形ロジックそのものを確認したいとき。
- cmoc の正本仕様断片やサブコマンド仕様を調べたいとき。
- テスト実装、Fake Codex CLI、pytest の規約やテストケースを探しているとき。
- 対象リポジトリ側の `INDEX.md` 生成ルールや oracle 評価の詳細仕様を確認したいとき。

## hash

- 23a4dadfbcac249e5ed15d7d1e5d3c34b6c84d908c9ce28c8e47b8ea196ccaf2

# `sub_commands`

## Summary

- cmoc の各サブコマンド本体実装を集約するディレクトリです。
- `init.py` は `cmoc init` の実装で、`.cmoc` を git 追跡対象外にする初期化、`.gitignore` と `.cmoc` の clean 判定、初期化変更のコミット、進捗表示と時間計測を扱います。
- `branch.py` は `cmoc branch` の実装で、`cmoc_<timestamp>` 形式の作業ブランチ作成、base commit の記録、`.cmoc` ignore 保証、ブランチ名衝突時のリトライを扱います。
- `apply.py` は `cmoc apply` の実装で、cmoc 作業ブランチ検証、oracle 以外の未コミット差分拒否、oracle 差分コミット、`INDEX.md` メンテナンス、Codex CLI による不整合調査と追従修正、禁止領域差分検査、レポート保存、終了コード判定を扱います。
- `eval-oracles.py` は `cmoc eval-oracles` の実装本体で、`.cmoc` ignore 保証、`INDEX.md` メンテナンス、部分評価と全体評価の切り替え、Codex CLI による oracle 評価、Markdown レポート保存を扱います。
- `eval_oracles.py` は `eval-oracles.py` を Python import 互換名から読み込む薄いラッパーで、テストなどからの monkeypatch を本体モジュールへ同期します。
- `merge.py` は `cmoc merge` の実装で、作業ツリー検証、マージ元 cmoc ブランチ解決、`git merge --no-ff`、conflict 発生時の Codex CLI 解消依頼、marker 検査、merge commit、作業ブランチ削除、例外時の手動解決案内を扱います。
- `__init__.py` は `sub_commands` を Python パッケージとして示すだけの初期化ファイルです。

## Read this when

- cmoc の個別サブコマンドの実装本体がどのファイルにあるか判断したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の処理順序、進捗表示、終了条件、共通 helper との接続箇所を調べたいとき。
- サブコマンドごとの `run_command` 呼び出し、`StepTimer` によるステップ計測、stdout 表示の実装箇所を確認したいとき。
- `.cmoc` の ignore 保証、base commit 記録、oracle 差分の扱い、`INDEX.md` メンテナンス、レポート保存が各サブコマンド内でいつ実行されるか確認したいとき。
- Codex CLI を呼び出すサブコマンドで、read-only と workspace-write の使い分け、Structured Output の schema、プロンプト内容、禁止領域の指定を確認したいとき。
- `eval-oracles.py` と `eval_oracles.py` の関係や、hyphen を含む実装ファイルを import 互換ラッパーから扱う仕組みを調べたいとき。
- merge conflict 解消時に cmoc がどこまで自動処理し、どこから手動解決案内に切り替えるか調べたいとき。

## Do not read this when

- CLI エントリーポイント、argparse のサブコマンド登録、トップレベルのコマンド分岐だけを調べたいとき。
- git コマンド実行、repo root 検出、`.cmoc` パス生成、oracle ファイル列挙、タイムスタンプ生成、時間計測、共通エラー処理などの helper 実装そのものを詳しく調べたいとき。
- `INDEX.md` 自動メンテナンスの対象ファイル、除外規則、Structured Output による目次生成ロジックだけを確認したいとき。
- cmoc の正本仕様断片やユーザー向け仕様を確認したいだけで、Python 実装の制御フローが不要なとき。
- テストコード、Fake Codex CLI、pytest 規約など、自動テスト側の構成だけを調べたいとき。
- README、AGENTS、oracles、memo の編集可否やリポジトリ運用ルールだけを確認したいとき。
- `__pycache__` 配下の生成済み bytecode を調べたいとき。

## hash

- 49a61b048ad635c3cfe17bf7972fb23eed989b3c0f255f140ac3bb172c5753b2
