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
- `cmoc oracle edit` サブコマンドの実装。oracle 編集指示を収集し、TUI 起動パラメータを構築したうえで、main worktree 上の active session branch から Codex TUI を起動する。indexing、入力ルートの ignore 確認、worktree・branch・session・clean 状態の事前検証も担う。

## Read this when
- `cmoc oracle edit` の CLI 動作、oracle 編集指示の入力処理、Codex TUI 起動条件を変更または調査するとき。
- oracle edit の indexing preflight、prompt editor 入力、session branch と clean worktree の検証経路を確認するとき。

## Do not read this when
- oracle 編集指示の入力部品そのものを変更する場合は、prompt editor 入力の共通実装を直接読む。
- TUI 起動パラメータの構築仕様を確認する場合は、oracle edit launch TUI builder を直接読む。
- 他のサブコマンドの CLI runtime や session 状態処理だけを調査する場合は、このファイルを起点にしない。

## hash
- 337fbe660a404600575a320131d1cf1d36b710d08a30c6cb33a2bb332da9809f

# `investigation.py`

## Summary
- `cmoc oracle investigation` サブコマンドの read-only TUI workload を実装する。入力された oracle 調査指示を編集・収集し、TUI 起動パラメータを構築して Codex TUI を起動する。

## Read this when
- `cmoc oracle investigation` の CLI 実行フロー、入力テンプレート、TUI 起動処理を確認・変更するとき。
- oracle 調査指示の入力前処理や indexing preflight、実行ステップの構成を確認するとき。

## Do not read this when
- 他の oracle サブコマンドや、TUI 起動パラメータの具体的な構築ロジックだけを確認したいときは、それぞれの実装先を直接読む。
- Codex TUI 自体の実装や共通 CLI runtime の詳細だけを調べるとき。

## hash
- 82d05024db9f62a0c049f64b3f6163d532cdfe1b8d691142961abcf9e49b3c10

# `review.py`

## Summary
- oracle review サブコマンドの CLI 実行入口と隔離 run のライフサイクルを担う。active session branch の検証、clean worktree の要求、review 用 worktree・branch の作成と cleanup、oracle review loop の実行、INDEX 変更の merge、所見レポート生成、中断・例外時の結果記録を扱う。review 対象列挙、review loop、レポート描画、INDEX 変更処理の詳細へ進むための上位入口。

## Read this when
- oracle review サブコマンドの実行条件、隔離 worktree/branch の作成・cleanup、review loop の呼び出し順を確認するとき
- oracle review の中断・例外処理、cleanup 失敗時の報告動作を確認するとき
- oracle review に関係する対象列挙、所見処理、レポート、INDEX merge の連携箇所を特定するとき

## Do not read this when
- oracle review の対象ファイル列挙規則だけを確認したいときは review_targets の実装を読む
- 所見の反復評価や中断時の部分結果処理だけを確認したいときは review_loop の実装を読む
- レポートの表示形式や出力内容だけを確認したいときは review_report の実装を読む
- review branch の commit、merge、conflict 解決だけを確認したいときは review_index の実装を読む

## hash
- 9c3e5aa9187b5d7b2e5a6646d4d38a7caab0cf00043cf621473eecaabccd0eb2

# `review_index.py`

## Summary
- oracle review 用 worktree・branch の INDEX.md 差分だけを検査し、必要に応じて commit・merge・conflict 解決を行う Git 操作を扱う実装。レビュー隔離終了時の INDEX.md 変更反映処理を確認する入口。

## Read this when
- oracle review による INDEX.md 変更の commit 条件や差分検査を変更・確認するとき
- review branch の merge、INDEX.md 限定の conflict 解決、Git path 復元処理を調査するとき

## Do not read this when
- 通常の INDEX.md 生成・ルーティング内容を確認するとき
- oracle review の仕様やレビュー全体の実行フローを確認するときは、対応する oracle 文書を先に読む場合
- Git 実行共通処理そのものを変更・調査するとき

## hash
- 0e19aa384667a4d42a288ccd740473f11fae20edad33138bb4604132c2357550

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
