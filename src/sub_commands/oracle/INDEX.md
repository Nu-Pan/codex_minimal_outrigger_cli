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
- oracle review の CLI 実行と isolated run のライフサイクルを統括する。active session branch の検証、レビュー対象の列挙と review loop の実行、INDEX 差分の commit・merge、割り込みや失敗時の report と作成済み resource の cleanup を扱う。oracle review の実行経路、隔離 worktree・branch の所有権、cleanup または中断時の挙動を確認する際の入口となる。

## Read this when
- oracle review サブコマンドの実行開始から report 出力までの制御フローを変更・調査するとき
- review run の worktree・branch 作成、merge、cleanup、lifecycle lock の扱いを確認するとき
- KeyboardInterrupt、部分作成、失敗、cleanup failure 時の report と状態遷移を確認するとき

## Do not read this when
- レビュー対象の列挙規則だけを確認したい場合は、対象列挙を担う下位実装を直接読む
- review loop 内の所見生成・評価処理だけを確認したい場合は、review loop の実装を直接読む
- report の表示形式や INDEX merge の詳細だけを確認したい場合は、それぞれの専用実装を直接読む

## hash
- 54c6c1a0de7e75cdee1703f509fd1f01203c0c9ddc305ed59e7a06c98ed1e8a4

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
- oracle review の finding を対象に、列挙、同一対象に関する既存 finding の提示、merge operation の反復適用、challenger と advocate による妥当性検証、judge による採否判定を一つの review loop として実行する。
- review の進捗として評価済みファイルと確定済み finding を保持し、KeyboardInterrupt 時には未完了 agent call の結果を捨てて、確定済み部分結果を OracleReviewInterrupted で呼び出し元へ渡す。
- finding の対象 oracle path を review worktree と main repository の双方から正規化し、merge の Structured Output が既存 finding_id だけを参照することを検証してから編集操作を適用する。

## Read this when
- oracle review の finding 列挙から merge、妥当性検証、採否判定までの制御フローを確認または変更するとき
- review の反復回数、dirty file・dirty finding の進捗管理、同一 oracle path に関連する finding の選別を調べるとき
- merge operation の適用規則や Structured Output の参照先検証を確認するとき
- KeyboardInterrupt 時の部分結果保存と評価済みファイルの扱いを確認するとき

## Do not read this when
- finding の列挙、challenger、advocate、judge、または merge agent の prompt parameter だけを確認するときは、それぞれの専用実装へ直接進む
- oracle review loop を呼び出す上位サブコマンドの進行表示や全体 orchestration だけを調べるとき
- oracle review と無関係なサブコマンドや、単純な finding データ構造の定義だけを確認するときは、該当する直接の対象へ進む

## hash
- 07707374a530fca2677035eb9e121c375e18d7ce041cfcd53347c9f72575d63d

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
