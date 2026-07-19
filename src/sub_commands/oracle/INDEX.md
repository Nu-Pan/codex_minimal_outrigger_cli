# `__init__.py`

## Summary
- oracle 系サブコマンドをまとめる package の境界を示す。oracle サブコマンド群への入口として扱う。

## Read this when
- oracle 系サブコマンドの package 構成や入口を確認するとき。

## Do not read this when
- 個別の oracle サブコマンド実装の詳細を確認するとき。

## hash
- 2c8110c7811042f7162e1264e7027bb2d801f4687eb66f48f1668402c8eeb0df

# `edit`

## Summary
- oracle edit サブコマンドの workload を扱うパッケージ。
- fork.py は `cmoc oracle edit fork` の編集指示収集から isolated editing run、Codex agent 実行、oracle 差分検証・commit、run 状態更新、fork report 保存までの実行フローを担う。

## Read this when
- oracle edit サブコマンドの workload や実行責務を確認するとき。
- `cmoc oracle edit fork` の実行フロー、事前条件、差分検証、commit、状態更新、fork report の挙動を変更・調査するとき。

## Do not read this when
- oracle 編集 agent の prompt 生成仕様だけを確認したいとき。
- run 共通ライフサイクルの詳細だけを確認したいとき。
- fork report の出力形式だけを確認したいとき。
- oracle edit 以外のサブコマンドを扱うとき。

## hash
- 7123f8105b871765fac0aab68915be583d8021aa42b9adc2c0e8ea2c76f9be01

# `investigation.py`

## Summary
- `cmoc oracle investigation` サブコマンドの read-only TUI workload を実装するエントリポイント。インデックス事前処理、調査指示の入力、Codex TUI 起動パラメータの構築、設定済みランタイムでの TUI 起動を担当する。

## Read this when
- `cmoc oracle investigation` の CLI 実行フロー、調査指示入力、Codex TUI 起動処理を変更・調査するとき。
- oracle investigation サブコマンドのステップ構成や実行時コンテキストを確認するとき。

## Do not read this when
- Oracle investigation の調査指示テンプレートや正本仕様を確認したいときは、対応する oracle doc を直接読む。
- TUI 起動パラメータの詳細実装を確認したいときは、`acp.builder.oracle.investigation.launch_tui` を直接読む。
- 共通 CLI ランタイム、プロンプトエディタ入力、インデックス事前処理の仕様だけを確認したいときは、各共通モジュールを直接読む。

## hash
- 7ea8e16b7d631e28f1e208d4683ec600dd20c333046f5eae32e94aca5e25d58b

# `review.py`

## Summary
- oracle review サブコマンドの実行入口と orchestration を担う実装。active session branch の検証、隔離 review worktree の作成・レビュー実行・結果マージ・後始末・レポート出力をまとめ、関連する review helper の公開入口も提供する。

## Read this when
- oracle review の CLI 実行フロー、session branch の前提条件、隔離 worktree のライフサイクル、レビュー中断・失敗時のレポート処理を確認または変更するとき。
- oracle review 関連の review index、review loop、review report、review target 機能への実行入口を確認するとき。

## Do not read this when
- レビュー対象の列挙、所見ループ、INDEX 変更のコミット・マージ、レポートの描画や保存の詳細だけを調べるときは、対応する review helper モジュールを直接読む。
- oracle review 以外の CLI サブコマンドや一般的な runtime/git helper の実装を調べるとき。

## hash
- 4529cf1ace449dfe0cd653408c2bd4131964112acfc4a3786fc320cecc5cf2e1

# `review_index.py`

## Summary
- oracle review 用 worktree の差分を検査し、INDEX.md だけを commit・merge する処理を担う。変更対象の制限、review branch の差分確認、INDEX.md の merge conflict 解決が主な入口。

## Read this when
- oracle review による INDEX.md 変更の commit 条件を確認するとき
- review branch の merge や INDEX.md 限定の conflict 解決を変更・調査するとき

## Do not read this when
- 通常の INDEX.md 生成内容やルーティング方針を確認したいとき
- oracle review 自体の仕様を確認したいときは、対応する oracle 文書を先に読む

## hash
- 9586f7d7c1998e7bfed6efad77b4a94b9e1a634df874e307e6f8c4737b0ed5c9

# `review_loop.py`

## Summary
- oracle review の finding 列挙・マージ・妥当性検証・採否判定ループを実装する中核モジュール。中断時の確定済み進捗保持、対象 oracle file の関連付け、Structured Output のマージ操作検証と再試行も扱う。

## Read this when
- oracle review の処理フロー、finding の列挙・統合・検証・判定を変更または調査するとき
- KeyboardInterrupt 発生時の部分結果の扱いを確認するとき
- merge operation の target_ids、kind、finding の妥当性検証や semantic retry を確認するとき

## Do not read this when
- oracle review の各 agent call 用パラメータ生成文面だけを変更または調査するときは、対応する builder モジュールを直接読む
- oracle review の path 解決規則だけを確認するときは、review_paths モジュールを直接読む
- ステップ通知の表示やサブコマンド全体の割り込み制御だけを確認するときは、呼び出し元や割り込み仕様を直接読む

## hash
- 9f698fcd963ee8773aae1a36385c4f0b0f19d111af1c92f6144341d26b9d480d

# `review_paths.py`

## Summary
- Oracle の検出結果に含まれるパスを、シンボリックリンクを追跡せず絶対パスへ解決する処理と、Oracle ファイルをリポジトリ相対キーへ変換する処理を提供する。メイン worktree と cmoc 管理下の isolated worktree の境界を検証し、対象外のパスは無視する。

## Read this when
- Oracle review の finding から oracle_path を解決・正規化するとき
- worktree 間で Oracle ファイルの相対キーを生成するとき
- パスの所属範囲やシンボリックリンク非追跡の挙動を変更・確認するとき

## Do not read this when
- Oracle review のレポート生成や finding の内容自体を変更する作業
- 一般的なパス操作や runtime path の仕様を確認する作業

## hash
- eddbb1a5f24d266c525ab726d9961e9b5cc95ae97c62f3b4e1ce076712725fb7

# `review_report.py`

## Summary
- oracle review の結果を Markdown レポートとして保存・描画する実装。レポートの保存先、YAML frontmatter、Verdict、対象 oracle 一覧、severity/verdict 別の所見表示を扱う。レビュー結果の判定、所見抽出・整形、repository-relative path 表示の補助関数も含む。

## Read this when
- oracle review レポートの保存形式、本文構成、Verdict 判定、所見の分類・表示順を変更または確認するとき
- レビュー実行状態、対象 oracle 数、branch/commit 情報などのレポート metadata の扱いを確認するとき

## Do not read this when
- oracle review の対象探索や path 解決だけを変更するときは、review_paths の実装を直接読む
- レビュー処理そのものや session 状態管理を変更するときは、このレポート描画モジュールではなく該当する実装を直接読む

## hash
- fec2c9e349afb412bb9901bdef02636cf8f6c91fe81b250bff887dba37db22df

# `review_targets.py`

## Summary
- oracle review の scope に応じてレビュー対象となる oracle file を列挙する実装。全件列挙と、セッション開始時点からの変更分に限定する列挙を扱う。

## Read this when
- oracle review の対象範囲、scope 判定、oracle file の列挙条件、セッションスコープの変更差分を確認・変更するとき。

## Do not read this when
- 個別の oracle file の内容やレビュー処理そのものを確認したいとき。対象ファイルの列挙後に実行されるレビュー処理の実装を直接読むべき場合。

## hash
- 34257a1d97f8acf23267a1c66587837067e891aa3e3e8d30045979517fe357bd
