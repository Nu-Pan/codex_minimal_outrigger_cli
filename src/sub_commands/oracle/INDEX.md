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
- `cmoc oracle edit` サブコマンドの実行入口と TUI 起動処理を担う。oracle 編集指示の収集、起動パラメータ構築、main worktree・session branch・clean worktree の事前条件検証を経て Codex TUI を起動する。

## Read this when
- `cmoc oracle edit` の起動フロー、入力収集、TUI 起動前検証、または main-worktree 制約を変更・調査するとき。

## Do not read this when
- oracle 編集プロンプトの具体的な生成内容を確認したいときは、参照される oracle edit 起動ビルダーや oracle 仕様を直接読む。
- 共通の CLI 実行基盤、git 状態確認、session 状態管理の実装だけを調査するときは、それぞれの共通モジュールを直接読む。

## hash
- 965daee686edf600e90e21ba52cb1563358abc875f915dcb62bb3820f3af926b

# `investigation.py`

## Summary
- `cmoc oracle investigation` サブコマンドの実装。oracle 調査指示を入力として TUI 起動パラメータを構築し、CLI runtime 経由で Codex TUI を read-only workload として起動する。インデックス作成の事前処理、入力ルートの ignore 設定、oracle/realization の読み書き制約も調査セッションへ適用する。

## Read this when
- `cmoc oracle investigation` の実行フロー、入力編集、TUI 起動、または oracle 調査時の自動注入指示を変更・確認するとき。

## Do not read this when
- oracle 調査の具体的な TUI 起動パラメータ生成ロジックを確認したい場合は、直接 `launch_tui` の実装を読む。
- CLI runtime の共通処理や prompt editor 入力の詳細を確認したい場合は、各共通モジュールを直接読む。

## hash
- bfecfa3273928372af6209d2aa865f59ccece71dd051d3a01edbecb0f6ea3743

# `review.py`

## Summary
- oracle review の CLI 実行と isolated run lifecycle を統括する実装。review 対象の選定・実行、所見と INDEX 差分の処理、review branch の merge、割り込み・失敗時の report、worktree と branch の cleanup を一貫した resource ownership と lifecycle lock のもとで管理する。oracle review の実行経路や中断・失敗時の状態遷移、cleanup 挙動を確認する際の入口。

## Read this when
- oracle review サブコマンドの実行フローや active session branch の前提を調べるとき
- review run の worktree・branch 作成、merge、cleanup、lifecycle lock の扱いを変更または確認するとき
- oracle review の割り込み、部分作成、cleanup failure、report 生成時の挙動を調べるとき
- review loop、対象列挙、INDEX 差分処理、report 処理を統合した CLI runtime の責務を確認するとき

## Do not read this when
- review 判定ロジックそのものだけを変更・確認する場合は review_loop.py を直接読む
- review 対象ファイルの列挙条件だけを調べる場合は review_targets.py を直接読む
- INDEX 差分の commit・merge・conflict 解決だけを調べる場合は review_index.py を直接読む
- review report の表示内容や出力だけを調べる場合は review_report.py を直接読む
- oracle review 以外のサブコマンドの run lifecycle を調べる場合は、対象サブコマンドの実装または共通 runtime を直接読む

## hash
- 37757f94b4c746550c998be8efa3ff1c28b483f5cd1f793407b95e3c32e17850

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
- oracle review の finding 列挙・マージ・妥当性検証・採否判定を行う review loop の実装。
- レビュー進捗、同一 round の finding、semantic retry、割り込み時の部分結果保存を一体として管理し、各段階の agent call と結果反映を制御する。
- merge operation の検証・適用、oracle path に基づく finding 関連付け、検証理由の反復収集、judge 結果の付与を担う。

## Read this when
- oracle review の実行フロー、finding の列挙・マージ・検証・判定を変更または調査するとき
- レビュー処理の KeyboardInterrupt 時の部分結果保持や evaluated files の更新を確認するとき
- merge finding operation の契約検証、semantic retry、finding ID の採番・削除・置換・統合を確認するとき

## Do not read this when
- oracle review の各 agent call に渡す個別パラメータ生成だけを調査するときは、review 配下の対応する parameter builder を直接読む
- oracle review のファイルパス解決だけを調査するときは review_paths の実装を直接読む
- レビュー以外のサブコマンドや一般的な Codex 実行規則を調査するとき

## hash
- 0152c77343761b7b4bae2620d96df9f85bc6386ea64f025883bf6369726cc40f

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
- oracle review の scope に応じてレビュー対象の oracle file を列挙する処理。full scope では全件、session scope ではセッション開始時点から review fork までに変更された oracle 配下のファイルだけを対象にする。対象判定には repository path 上の oracle file 判定を用い、symlink も扱う。

## Read this when
- oracle review の対象ファイル列挙、scope 別の対象範囲、session fork 間の差分判定を変更・確認するとき。

## Do not read this when
- oracle review の実行処理や、oracle file の内容そのものを確認したいとき。対象列挙後の処理や各 oracle file を直接読む方が適切。

## hash
- 95936d0c2a0e48b4b1d262160a9446dea0d9cb6d80f6fa8fe673a825e6e5ade3
