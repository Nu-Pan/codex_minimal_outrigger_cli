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
- `cmoc oracle edit` の CLI 実行フローを担当する main-worktree 側の実装。入力された oracle 編集指示をもとに、本命の oracle 編集 agent call と、正常終了後の仕様削減 agent call を順に起動する。
- prompt editor の入力予約・編集・抽出・確定、indexing preflight、起動前提検証、実行状態の primary report 更新、CLI の進捗管理をまとめて扱う。oracle 編集サブコマンドの実行入口として、起動パラメータ構築や session 要件の検証へ進む際に読む対象。

## Read this when
- `cmoc oracle edit` の CLI 実行順序、入力プロンプトの編集処理、agent call の起動条件や成功・失敗状態の更新を確認するとき。
- oracle 編集を main worktree 上の active な `cmoc/session/` branch に限定する検証を変更・調査するとき。
- 本命 oracle 編集 call と、正常終了後に実行する reduction call の連携を確認するとき。

## Do not read this when
- oracle 編集用の agent prompt の契約や起動パラメータの詳細を確認する場合は、直接 `launch_exec` 実装または oracle 編集仕様を読むとき。
- prompt editor の入力予約・抽出・確定処理そのものを調査する場合は、`commons.prompt_editor_input` を直接読むとき。
- session 状態、branch 判定、CLI 共通実行、report 更新など単一の共通機能だけを調査する場合は、それぞれの共通モジュールを直接読むとき。

## hash
- 880200249722b8c67b6a2453358834912f8b4b4e786dce6d7fe1ffce0ed1b0f0

# `investigation.py`

## Summary
- `cmoc oracle investigation` サブコマンドの read-only TUI 実行入口。oracle 調査指示の入力受付、完全な調査プロンプトの構築、設定済みの Codex TUI 起動までを CLI runtime 経由で調整する。oracle investigation の CLI フローやプロンプト編集・TUI 起動処理を確認するときの入口。

## Read this when
- `cmoc oracle investigation` の CLI 実行フローを変更・調査するとき
- oracle 調査指示の編集、プロンプト skeleton の生成、Codex TUI 起動の連携を確認するとき
- このサブコマンドの preflight、進捗段階、実行時設定の扱いを確認するとき

## Do not read this when
- oracle investigation の調査契約や prompt 内容そのものを確認したいとき
- TUI 起動パラメータの詳細実装を確認したいとき
- 共通の prompt editor 入出力処理だけを確認したいとき

## hash
- b3511825621dd0ec025ea9cd1f9a1cffc0cf67f11581636bb480c9d62cb3501a

# `review.py`

## Summary
- oracle review の CLI 実行と isolated run lifecycle を統括する実装。active session の検証、clean worktree 確認、review target の隔離 worktree・branch 作成、review loop 呼び出し、INDEX 差分の commit・merge、review report の保存を一連の処理として扱う。
- 割り込み、部分作成、例外、cleanup failure を含む終了経路と resource ownership を管理する。oracle review の実行経路全体、隔離 run の作成・merge・cleanup、または失敗時の report と terminal result を調査・変更するときの入口であり、個別の target 列挙・review loop・report 表示の詳細だけを扱う場合はそれぞれの専用実装を直接読む。

## Read this when
- oracle review CLI の起動条件、session branch・worktree の検証、review run の隔離 target 作成を確認するとき
- review loop の呼び出しから INDEX 差分の commit・merge、run resource の cleanup までの lifecycle を追うとき
- KeyboardInterrupt、部分作成、例外、cleanup failure、interrupted report の挙動を調査または変更するとき

## Do not read this when
- レビュー対象ファイルの列挙条件だけを調べるとき
- oracle review loop の所見生成や個別 oracle の評価処理だけを調べるとき
- review report の描画・保存形式だけを調べるとき
- INDEX 差分の merge 実装だけを直接調べるとき

## hash
- 183c901c1f37737fa771f2ca4f10abda96cae50a76a8155b76577c537c43f583

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
- 対象は oracle review の一連の状態を保持して実行する中核ループです。finding の列挙、同一対象の finding のマージ、反証・擁護による妥当性検証、採否判定、KeyboardInterrupt 時の確定済み部分結果の引き渡しをまとめて扱います。
- oracle review の進捗通知、評価済みファイルの追跡、finding の ID 付与・関連付け・正規化、merge operation の適用と入力 ID 検証まで含むため、review loop の挙動や中断時保存、finding 編集を確認・変更する際の入口になります。

## Read this when
- oracle review の finding 列挙、merge、validate、judge の反復処理を確認・変更するとき
- レビュー中断時に、どの finding や評価済みファイルが確定済み結果として残るかを確認するとき
- finding の対象 oracle path への関連付け、ID 採番、merge operation 適用、step callback 通知の挙動を確認するとき

## Do not read this when
- 個別の enumerate、validate challenger/advocate、judge、merge の prompt parameter 構築だけを確認したいときは、それぞれの builder を直接読む
- oracle review 全体の利用条件や外部向け仕様だけを確認したいときは、sub-command の正本仕様を直接読む
- review loop を呼び出す側の CLI 制御やログ保存だけを確認したいときは、その呼び出し元を直接読む

## hash
- f7957f7dba6ea569f664b54b59b3268cd35a342d7915305d27061c731ad7a534

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
- 日本語の技術文書として、対象モジュールの責務と、oracle review のレポート生成・描画処理へ進むべき入口を簡潔に示します。

## Read this when
- oracle review の実行結果を Markdown レポートとして保存・描画する処理を調べるとき
- レポートの verdict、frontmatter、finding 表示、対象 oracle path 表示の挙動を確認するとき

## Do not read this when
- oracle review の対象選定、finding の判定、または review 自体の実行制御を調べるとき
- レポート出力以外の sub-command の仕様や runtime path 処理を直接調べるとき

## hash
- 91278a4fd6e9eb55d21f879480b7ae0e2ac3a9edc34470443b5c1259fa4d1f30

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
