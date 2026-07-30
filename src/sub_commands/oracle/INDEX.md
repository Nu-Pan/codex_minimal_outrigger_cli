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
- oracle review サブコマンドの CLI 実装。active session branch 上での実行条件を確認し、隔離 worktree・run branch の作成、oracle 対象列挙、レビュー loop、結果の index merge、レポート出力までを統括する。
- 中断・例外・cleanup 失敗を含む review run のライフサイクルと、未コミット差分の拒否を扱う。詳細な対象列挙、レビュー処理、レポート生成、index 操作の実装へ進む入口でもある。

## Read this when
- oracle review サブコマンドの実行フロー、隔離 run の作成・統合・削除、割り込みや失敗時の処理を変更または調査するとき
- oracle review の CLI 前提条件、clean worktree 検査、レポート出力の呼び出し関係を確認するとき

## Do not read this when
- oracle review の対象ファイル列挙・レビュー判定・所見処理だけを変更するときは、対応する review_targets または review_loop の実装を直接読む
- レビュー所見の表示形式やレポート本文だけを変更するときは、review_report の実装を直接読む
- review branch の index 差分処理だけを変更するときは、review_index の実装を直接読む

## hash
- 0f9e9430a82211077c5f889e3861d5098bb6790403f59c654faa36499c2e666e

# `review_index.py`

## Summary
- oracle review 用の review worktree・review branch を扱う Git 処理をまとめた実装。INDEX.md だけの変更を検証して commit し、review branch の merge、INDEX.md 限定の競合解決、失敗時の復旧を担う。

## Read this when
- oracle review の review worktree で変更を commit する処理を調べるとき
- review branch の merge、INDEX.md 限定の競合解決、merge 失敗時の worktree 復旧を変更または確認するとき
- Git の status、name-only path、ours stage の扱いを確認するとき

## Do not read this when
- INDEX.md の内容生成や一般的なインデックスルーティングを変更するとき
- oracle review の仕様や merge 方針そのものを確認するときは、先に対応する oracle 文書を読むべき場合
- review worktree や review branch を使わない Git 操作を調べるとき

## hash
- ba2545c74a613ca45442845862f7684acae6ea9b01bf5138ab1d4b4660439633

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
