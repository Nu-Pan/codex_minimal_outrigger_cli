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
- `cmoc oracle edit` サブコマンドの実行フローを担う実装。入力された oracle 編集指示を編集・抽出し、本命の oracle 編集 agent call と、成功後に続く仕様削減 agent call を順序どおり実行する。main worktree、active な cmoc session branch など本命起動前提の検証もここで行う。

## Read this when
- `cmoc oracle edit` の CLI 実行フロー、prompt 編集入力の収集、oracle 編集 agent call の起動条件や実行順序を確認するとき。
- 本命 agent call と仕様削減 agent call の状態報告、失敗時の扱い、subcommand step の進行を変更・調査するとき。
- oracle 編集処理が main worktree または active な cmoc session branch を要求する理由と検証箇所を確認するとき。

## Do not read this when
- oracle 編集 prompt の具体的な契約や最終状態の仕様を確認したいだけの場合は、参照コメントで示される oracle 編集仕様を直接読む。
- prompt 編集入力の予約・編集・抽出・確定処理の詳細だけを確認したい場合は、`commons.prompt_editor_input` の実装を直接読む。
- agent 起動パラメータの構築規則だけを確認したい場合は、`acp.builder.oracle.edit.launch_exec` の実装を直接読む。
- CLI 共通の実行制御、設定読込、セッション状態管理、報告更新の詳細だけを確認したい場合は、それぞれの `cmoc_runtime` または `commons` の実装を直接読む。

## hash
- 3fea2c4033a83d2e9495d8289341e4208205a0549b40ec929d9f7814d63989fe

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
- oracle review CLI の実行入口と、active session branch 上での isolated review run のライフサイクルを統括する実装。
- review 対象の列挙、review loop、INDEX 差分の commit・merge、interruption/error report、worktree・run branch の cleanup までを一貫して扱う。
- oracle review の実行フロー、隔離 run の resource ownership、中断時の状態遷移、cleanup failure の処理を確認するための主要な入口。

## Read this when
- oracle review サブコマンドの CLI 実装や実行順序を調べるとき
- review run の worktree・branch 作成、session branch への INDEX 差分 merge、cleanup を変更または確認するとき
- KeyboardInterrupt、部分作成、例外、cleanup failure 時の report と terminal result の挙動を調べるとき

## Do not read this when
- review 対象の列挙規則だけを確認したい場合は review_targets の実装を読むとき
- 所見の評価ループだけを確認したい場合は review_loop の実装を読むとき
- INDEX 差分の commit・merge・conflict 解決だけを確認したい場合は review_index の実装を読むとき
- review report の形式や所見表示だけを確認したい場合は review_report の実装を読むとき

## hash
- 4f3dc7c7ca19cc85da415b15a18011601fb88001c09be08daa928299879019d1

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
- oracle review の finding 列挙から merge、擁護・反証による妥当性検証、採否判定までのループを実装する。中断時には完了済みの finding と評価済みファイルを部分結果として保持し、同一 review 状態を再開可能にする。

## Read this when
- oracle review の finding 列挙、merge 操作、妥当性検証、judge 判定、または中断時の部分保存の挙動を変更・調査するとき
- review loop の進捗通知、対象 oracle path の関連 finding 判定、merge operation の適用規則を確認するとき

## Do not read this when
- 個別 agent call の Structured Output パラメータ生成だけを変更・調査するときは、対応する review builder を直接読む
- oracle review の CLI 入出力やパス解決だけを確認するときは、対応する sub-command または review_paths の実装を直接読む

## hash
- 30978e168999dcc5c19decf8d25b9851aaaa4fedc5c1a9c35186c208a4761cc5

# `review_paths.py`

## Summary
- oracle_path を finding の値から絶対パスへ解決し、oracle root 略記や既知の root placeholder を扱うレビュー用パス変換の入口。
- oracle_path_key は oracle 配下または cmoc 管理下の isolated worktree にある oracle file だけを repository-relative key へ変換し、対象外のパスを除外する。symlink を追跡しない正規化処理もこのファイルが担う。

## Read this when
- finding の oracle_path 解決、oracle root alias・root placeholder の扱い、またはレビュー対象パスの相対キー化を変更・確認するとき。
- main worktree と cmoc 管理下 isolated worktree の所属境界、symlink 非追跡の絶対パス変換を調査するとき。

## Do not read this when
- oracle file と realization file の責務やレビュー仕様そのものを確認したいときは、参照されている oracle 文書を直接読む。
- レビュー用パス変換を利用する各サブコマンドの振る舞いだけを確認する場合は、その利用側実装を直接読む。

## hash
- 8bf8d3fe5cce6fd0daee1afeb00d3343ac64674617714ab2c5a5f92071832178

# `review_report.py`

## Summary
- oracle review のレポートを保存・描画する実装。レビュー結果の判定、YAML frontmatter、評価対象 oracle 一覧、所見の分類・表示、対象パスの Markdown 表示をまとめて担う。oracle review レポート形式や表示内容を変更するときの実装入口。

## Read this when
- oracle review レポートの保存、Markdown/YAML frontmatter の生成、verdict の決定を変更・調査するとき
- fatal/minor および accepted/rejected の所見表示順や内容を変更するとき
- 評価対象 oracle ファイルの相対パス表示や Markdown table のエスケープ処理を確認するとき

## Do not read this when
- oracle review の対象 oracle 探索、パス解決、レビュー実行そのものを変更・調査するとき
- レポート形式の正本仕様だけを確認する場合
- 他のサブコマンドのレポート生成を扱う場合

## hash
- b890e1c243a32d38ee834b75180b9d1e13f921a11cd908d14ed616e91416d917

# `review_targets.py`

## Summary
- oracle review の scope に応じて、レビュー対象となる oracle file のパスを列挙する関数を定義する。full scope では全候補を返し、session scope ではセッション開始時点から review fork commit までの oracle 差分に限定する。
- 全候補の分類には oracle と realization の列挙処理を使用し、session scope の差分判定では Git の NUL 区切り出力でパスを扱う。

## Read this when
- oracle review の対象ファイル範囲、full scope と session scope の切り替え、または review fork commit を基準とする差分抽出を確認するとき。
- oracle review 対象候補の列挙元と、セッション状態の session_fork_commit が対象選択にどう使われるかを確認するとき。

## Do not read this when
- oracle review の実際のレビュー内容や oracle file の仕様本文を確認したいとき。
- レビュー対象ではなく、oracle と realization の全ファイル分類規則を直接確認したいとき。

## hash
- d45e4990e19cc96e4178f7104dbc58130d3261a93f4a683e988c35785fe232dc
