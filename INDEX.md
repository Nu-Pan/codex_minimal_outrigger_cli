# `AGENTS.md`

## Summary

- この `AGENTS.md` のルーティング文書で、リポジトリ全体の作業ルールと参照先の入口を案内する。
- 閲覧・編集の制約、`oracle` 配下の読み方、`src` と `test` の配置前提を整理するための目次である。
- 作業開始前に、どの規約や仕様断片を読むべきかを切り分けるための入口である。

## Read this when

- このリポジトリで作業を始める前に、基本ルールと役割分担を確認したいとき。
- `memo`、`README.md`、`AGENTS.md`、`oracle` の閲覧・編集制約を確認したいとき。
- `oracle` の正本仕様を読む前に、どの `INDEX.md` を起点にたどるか知りたいとき。

## Do not read this when

- このリポジトリ全体の作業ルールや参照先の入口を確認する必要がないとき。
- 個別サブコマンドの引数や終了条件だけを直接確認したいとき。
- 実装コードやテストコードの内容だけを見たいとき。

## hash

- 3a1ea63ae7c7c50f65474c7a2c0f0e6884ad15e82af35e63fbd80fbee958f7d3

# `LICENSE`

## Summary

- このリポジトリのライセンス本文です。
- 利用、改変、配布の許可条件と、保証および責任の免責を定めています。
- 法的条件の確認が必要なときに参照する入口です。

## Read this when

- このリポジトリに適用されるライセンス条件を確認したいとき。
- 再配布、改変、サブライセンス、免責の扱いを確認したいとき。
- ソフトウェアをコピー・利用・配布する前に、権利と制約を把握したいとき。

## Do not read this when

- このリポジトリの実装方針、CLI 仕様、テスト方針を確認したいとき。
- `cmoc` の使い方や `oracle` のルーティングを調べたいとき。
- ライセンス条文そのものではなく、ファイル構成や開発手順を確認したいとき。

## hash

- a894f2547af0349f234986eb4661f0146f37b7d82f8b22a27a674d5c1236f08f

# `README.md`

## Summary

- このリポジトリの概要、初期セットアップ、基本ワークフロー、作業時の補足事項をまとめた入口です。
- `cmoc` を使い始める前に、何を最初に行うかと、次にどこを読むかを確認するための案内です。

## Read this when

- このリポジトリ全体の概要を短く把握したいとき。
- 初期セットアップとして clone、仮想環境作成、`cmoc` への PATH 設定を確認したいとき。
- 基本ワークフローの入口として `oracle` 配下の利用手順へ進みたいとき。
- Ctrl+S によるターミナルロックなど、作業時の補足情報を確認したいとき。

## Do not read this when

- cmoc の個別サブコマンドの引数や状態遷移を確認したいとき。
- `oracle` 配下の正本仕様を直接たどって、実装やテストの詳細を確認したいとき。
- 実装ルールやテスト規約だけを確認したいとき。

## hash

- e7f8b64d5a986f5bb2a696a71e2d6327bdc6d2cc72c909d0b6e2832c5c7df09a

# `bin`

## Summary

- この `bin` ディレクトリのルーティング文書で、`cmoc` コマンドの入口です。
- `<work-root>/bin/cmoc` の役割、Python 実行ファイルの選択、補完プローブ時の分岐、エラー時の案内へ進むための目次です。

## Read this when

- `<work-root>/bin` 配下の入口文書として、どのファイルへ進むべきか確認したいとき。
- `cmoc` のシェル製エントリーポイントの役割や、起動時の分岐を把握したいとき。
- 仮想環境 Python の有無によって `cmoc` がどう振る舞うかを知りたいとき。

## Do not read this when

- `<work-root>/bin/cmoc` の実装内容を直接確認したいとき。
- `bin/` 配下ではなく、`src/` や `oracle/` の別ディレクトリの文書を探しているとき。
- `cmoc` コマンドの利用手順全体ではなく、個別の実行ファイルだけを追いたいとき。

## hash

- 06c5f5f4145b6aa6d3f881761b05f09b4fdf00336454e1336db384b724d37e98

# `codex_minimal_outrigger_cli.code-workspace`

## Summary

- `codex_minimal_outrigger_cli.code-workspace` は、このリポジトリ全体を 1 つの VS Code ワークスペースとして開くための設定ファイルです。
- `folders` でルート `.` を開き、`files.exclude` で `**/__pycache__`、`**/*.egg-info`、`**/INDEX.md` を非表示にします。
- `python.analysis.extraPaths` と Markdown 設定を含み、Python 編集・補完・整形の前提をまとめます。

## Read this when

- このリポジトリを VS Code などで単一ワークスペースとして開く設定を確認したいとき。
- ワークスペースのルート、表示除外、Python 補完パス、Markdown 編集設定を把握したいとき。
- エディタ起点で `<cmoc-root>` を開く前提を素早く確認したいとき。

## Do not read this when

- cmoc の実装コードやサブコマンド仕様そのものを確認したいとき。
- このワークスペース設定ではなく、`src`、`test`、`oracle` の個別ファイルを直接追いたいとき。
- リポジトリ運用ルールや仕様断片だけを確認したいとき。

## hash

- a486d130bc988b4be2adee6368d38bc0e0e7ac3825cc1fb472075109c8b5805a

# `oracle`

## Summary

- `oracle` 配下のルーティング文書で、`doc/` と `src/` への入口を案内します。
- `doc/` は利用手順・共通仕様・非採用案・開発規約・branch モデルの入口です。
- `src/` は `acp/`、`basic/`、`config/` に分かれる共通基盤と設定の入口です。

## Read this when

- `oracle` 配下のどこから読むべきかを整理したいとき。
- `doc/` と `src/` の役割分担を先に把握してから、関連する正本仕様へ進みたいとき。
- 利用手順、共通仕様、非採用案、開発規約、branch モデルの入口をまとめて確認したいとき。

## Do not read this when

- `oracle` 配下全体の入口説明ではなく、`doc/` や `src/` の個別仕様をすでに読む先が決まっているとき。
- この階層の案内ではなく、`branch_model.md` や下位の `INDEX.md` の詳細だけを直接確認したいとき。
- cmoc の実装やテストの作業を進めていて、この階層のルーティング情報が不要なとき。

## hash

- bec8b73cf6b6e9b8cfa6857a10debc1c893a94796b55a0340750348b2fa5c99f

# `pyproject.toml`

## Summary

- この `pyproject.toml` のルーティング文書で、Python パッケージ定義とビルド設定の入口です。
- プロジェクト情報、依存関係、CLI エントリポイント `cmoc`、`setuptools` のパッケージ探索設定、pytest 設定を案内します。
- `src` と `<work-root>/oracle/src` を含むパッケージ配置前提を確認したいときの起点です。

## Read this when

- プロジェクト名、バージョン、説明、対応 Python 版を確認したいとき。
- 依存パッケージや `cmoc` のコンソールスクリプト定義を確認したいとき。
- `setuptools` の `src` レイアウト設定や pytest の基本設定を把握したいとき。

## Do not read this when

- このリポジトリ全体の作業ルールや `oracle` 配下のルーティングを確認したいとき。
- CLI の個別サブコマンド実装やテストコードの内容だけを追いたいとき。
- `src` や `<work-root>/oracle/src` の内部モジュールの詳細だけを直接確認したいとき。

## hash

- 4243188ef61246c642868f481696df0e74dd4f8e86c7495b6dece745ea8ae350

# `src`

## Summary

- この `src` ディレクトリのルーティング文書で、cmoc の実装側ソースへの入口です。
- 実装本体はこの配下に置き、共通基盤、サブコマンド別処理、補助ユーティリティへ分岐します。
- どのモジュールから読むべきか迷ったときの起点になります。

## Read this when

- `src` 配下で読むべき実装ファイルやサブディレクトリの入口を整理したいとき。
- 共通型、prompt 組み立て、引数生成、ユーティリティのどこから入るか迷ったとき。
- 実装やテストの前に、この階層の役割分担を確認したいとき。
- 新しいソースモジュールや下位 `INDEX.md` を追加・修正する前に、全体の導線を把握したいとき。

## Do not read this when

- すでに目的のファイル名やサブディレクトリが分かっていて、`src` を経由せず直接そちらへ進むとき。
- この階層の導線ではなく、個別モジュールの実装詳細だけを確認したいとき。
- `test` や `oracle` 側の文書だけを読みたいとき。
- この階層に新しい入口を追加する予定がなく、既存ファイルをそのまま開けば足りるとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `test`

## Summary

- この `test` ディレクトリのルーティング文書で、`test_prompt_parts.py` への入口を案内します。
- `test_prompt_parts.py` は prompt 部品の StructDoc 生成と Markdown 表現、ならびに `complete_prompt` への条件付き含有や既定の省略を検証するテスト群です。

## Read this when

- `test` 配下で、まずどのテストファイルを読むべきか整理したいとき。
- prompt 部品の StructDoc 生成、Markdown レンダリング、`complete_prompt` への含有条件を確認したいとき。
- `index_entry_standard`、`apply_review_standard`、`review_oracle_standard` の回帰テスト観点を把握したいとき。

## Do not read this when

- すでに `test_prompt_parts.py` を直接開く対象が決まっていて、この階層の案内を経由する必要がないとき。
- prompt 部品の実装本体や `src/` 側の仕様を確認したいだけで、テスト観点の整理が不要なとき。
- この階層ではなく、別のテスト群や別ディレクトリの目次を探しているとき。

## hash

- eb475920a6f1be4bc3a617984f8ca2e2611b4ea6a6cb58d5b6f8488fea219d7a
