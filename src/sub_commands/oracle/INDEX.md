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
- oracle review サブコマンドの CLI 実行入口とライフサイクルを担当する。active session branch の検証、隔離 worktree・run branch の作成と cleanup、oracle file の列挙・レビュー実行、INDEX 更新の merge、レポート生成、中断・例外処理をまとめて扱う。詳細なレビュー処理やレポート整形は下位モジュールへの入口から確認する。

## Read this when
- oracle review サブコマンドの実行条件、隔離 run の作成・統合・cleanup、中断時や例外時の挙動を変更・調査するとき
- oracle file のレビュー対象選択からレビュー結果レポート出力までの全体フローを確認するとき

## Do not read this when
- レビュー対象の列挙ロジックだけを変更・調査するときは review_targets の実装へ進む
- レビュー loop の所見生成や中断状態だけを変更・調査するときは review_loop の実装へ進む
- レポートの表示・書き込みだけを変更・調査するときは review_report の実装へ進む
- INDEX 更新の commit・merge・conflict 解決だけを変更・調査するときは review_index の実装へ進む

## hash
- cbb742f56682a3ef131e18c4dd0b38441b8e5617b038e8ccadfb4f12bf25e9ee

# `review_index.py`

## Summary
- oracle review 用 worktree の差分を検査し、INDEX.md 以外の変更を拒否したうえで INDEX.md 変更だけを commit する処理を提供する。review branch の INDEX.md 差分確認、merge、INDEX.md 限定の conflict 解決、Git の変更パス取得を扱う。

## Read this when
- oracle review の INDEX.md commit、review branch の差分検証・merge、INDEX.md 限定の conflict 解決、Git パス取得処理を変更または調査するとき。

## Do not read this when
- INDEX.md の内容や一般的な indexing 仕様だけを確認したいとき。oracle review の処理以外のサブコマンド実装を変更するとき。

## hash
- 157de481d039aa6c6907735bc8f294f1af4dce9846a26d07a27a90c4c0172996

# `review_loop.py`

## Summary
- oracle review の所見列挙・マージ・妥当性検証・採否判定を一連のループとして実行する実装。レビュー進捗、finding の関連付け、semantic retry、KeyboardInterrupt 時の部分結果保存、merge operation の契約検証を扱う。

## Read this when
- oracle review の enumerate／merge／validate／judge のループ動作を変更・調査するとき
- レビュー中断時の確定済み所見や評価済みファイルの扱いを確認するとき
- finding の merge operation、ID、重複、対象妥当性、semantic retry の挙動を確認するとき

## Do not read this when
- oracle review の prompt parameter 構築だけを変更・調査するときは、各 review parameter builder を直接読む
- oracle review のファイルパス解決だけを変更・調査するときは、review_paths の実装を直接読む
- oracle review 以外のサブコマンドのループや所見処理を扱うとき

## hash
- fb099dd2b6671a992b5f01c1942f062d345e5b1c6972408f4408da05df098ab1

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
- oracle review の結果を Markdown レポートとして保存・描画する実装。YAML frontmatter、判定結果、評価対象 oracle file、finding の分類・順序・安全な Markdown 表示を扱う。

## Read this when
- oracle review レポートの保存先、frontmatter、verdict 判定、finding 表示、対象 path 表示の挙動を変更・確認するとき。
- oracle review の出力形式や、エラー・中断・対象なし・fatal・minor・ok の結果処理を調査するとき。

## Do not read this when
- oracle review の対象 oracle file の収集・評価ロジック自体を変更・確認するとき。
- 他のサブコマンドのレポート形式や、共通の timestamp path 予約処理だけを調査するとき。

## hash
- 975b64084bf01f45bfc91495bde6359f29dca3875d6df4cf23cf9ecb478b2eca

# `review_targets.py`

## Summary
- oracle review の scope に応じてレビュー対象の oracle file を列挙する処理。full scope では全件、session scope ではセッション開始時点から review fork までに変更された oracle 配下のファイルだけを対象にする。対象判定には repository path 上の oracle file 判定を用い、symlink も扱う。

## Read this when
- oracle review の対象ファイル列挙、scope 別の対象範囲、session fork 間の差分判定を変更・確認するとき。

## Do not read this when
- oracle review の実行処理や、oracle file の内容そのものを確認したいとき。対象列挙後の処理や各 oracle file を直接読む方が適切。

## hash
- 95936d0c2a0e48b4b1d262160a9446dea0d9cb6d80f6fa8fe673a825e6e5ade3
