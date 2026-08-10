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
- `cmoc oracle edit` サブコマンドから、oracle 編集指示を入力する Codex TUI を起動する実装。
- main worktree、active な `cmoc/session/` ブランチ、clean worktree などの起動前提を検証し、プロンプト入力の確定と indexing preflight を経て TUI を開始する。
- oracle edit の CLI 起動経路と実行前提を確認する際の入口であり、個別のプロンプト編集処理や TUI パラメータ構築の詳細は import 先へ委ねる。

## Read this when
- `cmoc oracle edit` の CLI runtime、TUI 起動フロー、または main worktree・session branch・clean worktree の実行前提を確認するとき。
- oracle 編集指示の受付から Codex TUI 起動までの処理順序を確認するとき。

## Do not read this when
- oracle edit の正本仕様や編集契約を確認するときは、oracle 編集の仕様文書を直接読む。
- プロンプト入力の予約・収集・確定処理を確認するときは、プロンプト編集入力の実装を直接読む。
- TUI 起動パラメータの内容や session 状態のロード処理を確認するときは、それぞれの import 先を直接読む。

## hash
- 4bcb74fa76fe2be27b2af6e014479981d256266e41b45106ed294f882230866a

# `investigation.py`

## Summary
- `cmoc oracle investigation` サブコマンドの read-only TUI workload を実行する CLI ランタイム実装です。
- 入力された oracle 調査指示を完全なプロンプトへ組み立て、設定を読み込んで Codex TUI を起動します。

## Read this when
- `cmoc oracle investigation` サブコマンドの起動処理、oracle 調査指示の入力、プロンプト確定、Codex TUI 起動の流れを確認するとき。
- インデックス作成の preflight、プロンプト編集入力の予約・確定、サブコマンドの進捗表示や通知設定を調べるとき。

## Do not read this when
- oracle investigation の調査契約やプロンプト内容そのものを確認する場合は、対応する oracle 仕様を直接読む。
- TUI 起動パラメータの構築方法だけを確認する場合は、`build_oracle_investigation_launch_tui_parameter` の実装を直接読む。
- 共通のプロンプト編集入力処理やリポジトリ設定の詳細だけを確認する場合は、対応する共通モジュールを直接読む。

## hash
- d0a41777b0c16eed6008bafb57a56bff6a1694711b6b0ac0fad0d90eef3a122c

# `review.py`

## Summary
- oracle review の CLI 実行と isolated run lifecycle を統括するエントリー。review 対象の収集、review loop の実行、所見と INDEX 差分の処理、レポート生成までを扱う。
- run 用 worktree・branch の作成から merge、割り込み・失敗時の cleanup とエラー報告まで、共有される resource ownership と例外処理を一体で管理する。
- review の個別処理や対象列挙、INDEX merge、レポート形式の詳細を確認する場合は、本文から参照される下位モジュールが直接の入口になる。

## Read this when
- oracle review サブコマンドの CLI 実行フローを確認するとき
- review run の worktree・branch 隔離、lifecycle lock、merge、cleanup の挙動を確認するとき
- oracle review の中断、部分作成、cleanup failure、レポート生成の処理を変更または調査するとき

## Do not read this when
- review loop の所見判定や個別の merge 操作だけを確認するとき
- review 対象の列挙規則だけを確認するとき
- review レポートの表示内容や出力形式だけを確認するとき

## hash
- 4e9455fb5a9b4e7c5b09a861f650096881d04730b297bd37446d193f9cee16aa

# `review_index.py`

## Summary
- oracle review 用 worktree の INDEX.md 差分を検査・commitし、review branch を session branch へ安全に merge する処理を扱う。
- INDEX.md 以外の変更検出、merge conflict の解決、失敗時の worktree 復旧、Git path の安全な列挙を下位実装への入口として提供する。

## Read this when
- oracle review の INDEX.md commit、review branch の merge、INDEX.md 限定 conflict 解決、merge 失敗時の復旧挙動を変更・調査するとき。
- review worktree の変更 path 判定や Git の rename・quote 済み path の扱いを確認するとき。

## Do not read this when
- 通常の oracle review 機能や INDEX.md 生成処理の仕様を確認したいだけで、review branch の Git 操作実装を変更・調査しないとき。
- 一般的な Git 実行ヘルパーの仕様や他サブコマンドの中断処理を直接確認する場合。

## hash
- 9d8452af51dc2c2076407b1ddb8daa9152eb8e7e3b6170c7a014dff1e06382a7

# `review_loop.py`

## Summary
- oracle review の所見列挙・マージ・妥当性検証・採否判定を一連のループとして実行する実装。中断時には確定済みの所見と評価済みファイルを部分結果として保持し、再開可能な進捗管理を担う。
- 所見の対象パス正規化、merge 操作の Structured Output 検証、所見リストへの追加・削除・置換適用も扱う。oracle review の状態共有とループ制御を確認するための入口であり、個別 agent prompt の内容を調べる場合は各 review builder へ進む。

## Read this when
- oracle review の列挙、マージ、反証・擁護、採否判定の実行順序やループ回数を変更・確認するとき
- KeyboardInterrupt 発生時の部分保存、評価済みファイル、確定済み所見の扱いを調べるとき
- finding の対象 oracle path の関連付けや merge operation の適用・入力 ID 検証を調べるとき

## Do not read this when
- 個別の enumerate、validate、judge、merge agent prompt のパラメータ仕様だけを確認したいときは、対応する review builder を直接読む
- oracle review の CLI 起動条件や利用者向けコマンド仕様だけを確認したいときは、review loop の呼び出し元または oracle review の仕様文書を読む
- 一般的な finding データ構造やパス操作の定義だけを確認したいときは、対応する review path・finding utility を直接読む

## hash
- 3bd2bac468cf8543617a42ba0c84d70aaad30d530ae5b088d21e999ce434178f

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
- oracle review の実行結果を Markdown レポートとして生成・保存する実装。frontmatter、レビュー verdict、評価対象 oracle file、finding の分類・表示、YAML 値と Markdown パスの安全な描画を扱う。

## Read this when
- oracle review レポートの保存先、frontmatter、verdict 判定、finding の表示順や分類を変更するとき
- レビュー結果の Markdown/YAML 出力形式やパス・文字列のエスケープ処理を確認するとき

## Do not read this when
- oracle review の対象 oracle file の選定やレビュー実行制御を変更するとき
- レビュー結果以外のレポート形式、CLI 引数、git ブランチ操作を調べるとき

## hash
- 32d7ee8529ceffacf71e9f434037b3f0122da45b27006de2292036c47036f791

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
