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
- 編集関連の実装ファイルを含まない空のディレクトリです。現時点で下位要素へのルーティング先はありません。

## Read this when
- このディレクトリに編集関連ファイルが追加されたか確認するとき。

## Do not read this when
- Oracle サブコマンドの実装を調査するとき。親ディレクトリの実装ファイルを直接確認してください。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `edit.py`

## Summary
- `cmoc oracle edit` サブコマンドの main-worktree 実行フローを担う実装。入力された oracle 編集指示を受け取り、本命の oracle edit agent call と、正常終了後に行う仕様削減 agent call を順序どおりに起動する。
- oracle edit の起動前提、session branch と active session の検証、indexing preflight、prompt 編集入力の確定処理を確認したい場合の入口となる。詳細な prompt 編集処理や agent 起動パラメータの構築は、呼び出し先の専用モジュールを読む。

## Read this when
- `cmoc oracle edit` の CLI 実行順序、agent call の条件、または main worktree・session branch の前提を変更するとき
- oracle edit の本命処理と仕様削減処理の責務分担や、正常終了後だけ後続処理を行う制御を確認するとき
- oracle 編集指示の受付から indexing、起動前検証、agent call までの統合フローを調査するとき

## Do not read this when
- prompt 編集入力の予約・収集・確定処理そのものを調べるときは、prompt editor 用モジュールを直接読む
- oracle edit agent call の launch parameter の内容や構築規則を調べるときは、oracle edit 用 launch builder を直接読む
- 他の oracle サブコマンドの実行フローだけを調べるとき

## hash
- 8eeadcfd957ed5009efd94818f4f452d400c63efb81cade1903c6a377392e0a3

# `investigation.py`

## Summary
- `cmoc oracle investigation` の read-only TUI workload を実行する CLI エントリー。oracle 調査指示の入力を受け、完全プロンプトを確定して Codex TUI を起動するまでのオーケストレーションを担う。
- インデックス前処理、プロンプト編集用入力の予約・収集・確定、TUI 起動パラメータ構築、設定読込、Codex TUI 起動をつなぐ入口であり、各処理の詳細は import 先の実装へ進む。

## Read this when
- `cmoc oracle investigation` サブコマンドの実行経路を確認・変更するとき。
- oracle 調査指示の入力から完全プロンプト確定、Codex TUI 起動までの責務分担を確認するとき。
- このサブコマンドの CLI 実行時に行われる index preflight、進捗管理、設定読込、TUI プロセス起動の連携を確認するとき。

## Do not read this when
- oracle investigation の調査契約や利用者向け仕様を確認する場合は、まず対応する oracle 仕様文書を読む。
- TUI 起動パラメータの内容や構築規則を確認する場合は、起動パラメータ構築モジュールを直接読む。
- プロンプト入力の予約、収集、ignore 設定、完全プロンプト確定の挙動を確認する場合は、プロンプト編集ヘルパーを直接読む。
- CLI 共通ランナー、設定、リポジトリルート、work root の実装詳細を確認する場合は、`cmoc_runtime` を直接読む。

## hash
- a100063cca0a6645889c85187bb70833f7c84baac45be4cf55ebb87d1df17ab0

# `review.py`

## Summary
- oracle review CLI の実行起点と isolated review run のライフサイクルを統括する実装。active session の検証、review target の列挙と review loop の実行、INDEX 差分の commit・session branch への merge、interruption・例外時の report 生成と worktree/branch cleanup を扱う。oracle review の実行経路、隔離 run の resource ownership、cleanup や中断時の挙動を確認・変更するときの入口。

## Read this when
- oracle review サブコマンドの実行フロー、隔離 worktree/branch の作成・merge・削除を調べるとき
- oracle review の中断、失敗、部分作成、cleanup failure、および report 生成の挙動を確認するとき
- review loop や review index の下位実装へ進む前に、CLI と lifecycle の統合責務を確認するとき

## Do not read this when
- review の個別 target 列挙、所見判定、INDEX merge の詳細だけを調べる場合は、それぞれの専用実装を直接読むとき
- oracle review 以外の CLI サブコマンドや一般的な run isolation の仕様だけを確認する場合

## hash
- 0743b4a0ef392b60e876c44a45569470e4a0a5cfd260c042c7b317b2a4528c9a

# `review_index.py`

## Summary
- oracle review 用 worktree の変更を検査し、INDEX.md だけを commit・merge する処理を担う。変更 path の収集、INDEX.md 以外の差分拒否、review branch の merge、INDEX.md 競合の自動解決、merge 失敗後の復旧を扱う。

## Read this when
- oracle review の隔離 worktree で、変更を INDEX.md のみに限定して commit する処理を確認・変更するとき
- review branch の merge、INDEX.md 競合の自動解決、merge 失敗後の worktree 復旧を確認するとき

## Do not read this when
- 通常の oracle 実装や review 以外の Git 操作を調べるとき
- INDEX.md の routing 生成規則や、別の sub_command の挙動だけを確認するとき

## hash
- 25c107dfb7502bb0b2f7548d2b556eb277d4f90054e95533b71e75c139ac077a

# `review_loop.py`

## Summary
- oracle review の finding 列挙・マージ・妥当性検証・採否判定を一連の状態で実行するループの実装。対象ファイルごとの列挙結果、merge operation の適用、challenger/advocate による反復検証、judge 結果の付与を扱う。
- レビュー処理の中断時には、完了済み agent call の結果と評価済みファイルを `OracleReviewInterrupted` として呼び出し元へ返し、部分的な進捗を保持する。finding の path 正規化や merge operation の target ID 検証もこの loop の補助責務に含まれる。
- oracle review の実行制御や中断・再開、finding の統合・検証・判定ロジックを変更または追跡するときの入口。個別 agent call の prompt/Structured Output 定義そのものを確認する場合は、インポート先の builder file を直接読む。

## Read this when
- oracle review の finding 列挙、重複・関連 finding の merge、反証・擁護・judge の反復処理を調査または変更するとき
- KeyboardInterrupt 発生時の部分結果保存、評価済みファイルの進捗、レビュー loop の再開挙動を確認するとき
- finding merge operation の適用規則、finding ID の事後検証、oracle path の正規化を確認するとき

## Do not read this when
- 個別の enumerate、validate、merge、judge agent の prompt や Structured Output schema だけを確認するときは、各 builder の実装を直接読む
- oracle review 全体の利用者向け仕様やステップ順だけを確認する場合は、対応する正本仕様を直接読む
- oracle review 以外のサブコマンドや、finding loop と無関係な共通 runtime 処理を調査するとき

## hash
- 8d7df5287d338d32bb4664836c1c41450eba54c14b96c8608fc9abfe10f3cb47

# `review_paths.py`

## Summary
- oracle_path の値を解決して絶対パスへ変換し、oracle file の repository-relative key を生成する補助処理。worktree 所属判定と symlink 非追跡のパス正規化を担当する。

## Read this when
- oracle_path の入力形式、{{oracle-root}} や root placeholder の解決、または oracle file の相対キー生成を変更・調査するとき。
- main worktree と cmoc 管理下の isolated worktree のパス境界や、symlink を追跡しない正規化処理を確認するとき。

## Do not read this when
- oracle review の全体仕様や finding の生成・評価ロジックを確認したいときは、まず対応する oracle review 文書や呼び出し元を読む。
- oracle_path の解決や oracle-relative key 生成に関係しないサブコマンド処理を調査するとき。

## hash
- 89eb16dfdab2aef4017794b8fb1e637fe91a6861d254dff3c5eb988a922b7b6c

# `review_report.py`

## Summary
- oracle review サブコマンドのレビュー結果レポートを生成・整形する実装。レポートの保存、判定結果、YAML frontmatter、評価対象一覧、所見グループ、パス表示を扱う。レビュー結果の出力形式や表示順、判定ロジックを確認・変更するときの入口となる。

## Read this when
- oracle review の Markdown レポート保存や描画形式を変更するとき
- レビュー結果の verdict（error、interrupted、no_targets、fatal、minor、ok）判定を確認するとき
- frontmatter、評価対象テーブル、finding の表示順やエスケープ処理を確認するとき

## Do not read this when
- oracle review の対象 oracle の選定・レビュー実行そのものを変更するとき
- レビュー仕様の正本を確認するときは、参照コメントに示された oracle_review 仕様を直接読む場合
- 一般的なレポート以外のサブコマンド出力や、所見データの生成処理を変更するとき

## hash
- f78dfc672cf520dde6f435fca6af84c71d2a1a0e3b025a03b5271a1fc282ab22

# `review_targets.py`

## Summary
- oracle review の scope に応じてレビュー対象となる oracle ファイルを列挙する補助モジュールです。full scope では全 oracle ファイルを返し、session scope ではセッション開始コミットから review fork commit までの oracle 配下の変更だけに絞ります。
- レビュー対象の全件列挙は oracle と realization の分類結果を共有し、差分パスは NUL 区切りで扱ってパス名の改行を保ちます。

## Read this when
- oracle review の対象範囲の決定方法、full/session scope の挙動、またはレビュー対象ファイル列挙の実装を確認・変更するとき。

## Do not read this when
- oracle review 以外のサブコマンドや、レビュー対象ファイルの内容そのものを確認したいとき。

## hash
- a7f12edcc489d57425843130c363e049cf06fcde33daceaa0f3030b242a24b25
