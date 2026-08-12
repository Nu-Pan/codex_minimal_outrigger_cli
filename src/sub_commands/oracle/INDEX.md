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
- `cmoc oracle edit` サブコマンドの実行入口と、oracle 編集指示から Codex TUI を起動する処理を担う。入力予約・収集・完全プロンプト確定、indexing 前処理、main worktree 上の active な session branch の検証を経て TUI を起動する。

## Read this when
- `cmoc oracle edit` の CLI 実行フロー、TUI 起動条件、oracle 編集プロンプトの入力処理を確認または変更するとき。

## Do not read this when
- oracle 編集プロンプトの内容や契約そのものを確認したいときは、参照コメントで示される oracle 仕様を直接読む。
- 他のサブコマンドの実行フローや、共通のプロンプト入力・runtime state 実装だけを調べるとき。

## hash
- 0b47a7f3dccecd7d83a526a3a7203e743a2912e63d47d3267d10cd68de6dbe67

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
- oracle review の CLI 実行と isolated run lifecycle を統括する実装。active session branch の検証、review worktree と run branch の作成、review loop の実行、INDEX 差分の commit・merge、完了時の report 出力を扱う。中断・例外・部分作成にも対応し、作成した resource の cleanup と cleanup failure の report まで一貫して管理する。

## Read this when
- oracle review の CLI runtime、isolated review run の resource ownership、lifecycle lock、worktree・branch の作成と削除を確認または変更するとき
- oracle review の中断、失敗、部分作成、cleanup failure における状態遷移と report 処理を追跡するとき
- review run の結果を session branch へ merge する呼び出し経路を確認するとき

## Do not read this when
- review 対象ファイルの列挙条件だけを確認したいときは review target の実装へ直接進む
- review loop の所見生成・評価済みファイル管理だけを確認したいときは review loop の実装へ直接進む
- INDEX 差分の commit・conflict resolution・merge の詳細だけを確認したいときは review index の実装へ直接進む
- report の表示形式や出力内容だけを確認したいときは review report の実装へ直接進む

## hash
- 5b3efa63d2fb04804ac5cfb0da202990775cad00c5c0322f840438a1f7430d17

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
- oracle review の finding 列挙から merge、反証・擁護による検証、採否判定までの反復処理を一元管理する実装。review worktree への実行コンテキスト束縛、進捗保持、中断時の部分結果引き継ぎ、finding の path 正規化と merge 操作適用も扱う。oracle review loop の全体挙動や中断・再開、finding の統合・検証・判定を追跡する際の入口となる。

## Read this when
- oracle review の finding 列挙、merge、検証、judge の処理順序や反復終了条件を確認するとき
- review worktree 用に agent call parameter の prompt と実行コンテキストを束縛する挙動を調べるとき
- KeyboardInterrupt 発生時に確定済み finding と評価済みファイルをどう保持するか確認するとき
- finding の対象 oracle path の対応付けや merge operation の適用規則を確認するとき

## Do not read this when
- finding の列挙・検証・判定用 agent prompt の内容や Structured Output 定義だけを確認したいときは、各 review builder の対象へ直接進む
- oracle review のパス計算だけを確認したいときは、review path を扱う対象へ直接進む
- review loop を呼び出す上位コマンドの CLI 引数や外部実行フローだけを確認したいときは、呼び出し元の対象へ進む

## hash
- 809a65591544df21ce62e85cce214680fbc9dbeca79c6d6e6aedef1116f300de

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
