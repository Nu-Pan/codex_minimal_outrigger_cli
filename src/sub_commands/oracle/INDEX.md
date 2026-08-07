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
- `cmoc oracle edit` サブコマンドの実行フローを担う実装。入力された oracle 編集指示を受け取り、起動パラメータを構築し、main worktree・active session branch・clean worktree などの前提を検証したうえで Codex TUI を起動する。oracle 編集 CLI の起動条件や実行手順を確認する際の入口。

## Read this when
- `cmoc oracle edit` の CLI 実行フロー、TUI 起動、入力受付、起動前提の検証を調べるとき。

## Do not read this when
- oracle 編集そのものの正本仕様や編集プロンプトの内容を確認するとき。
- TUI 起動パラメータの詳細実装、入力エディタ、git 状態確認、session 状態管理の詳細を直接調べるとき。

## hash
- cd8a3c105c06d089fc166338f1847122c3d38e1b7d52dc09925adaf8fed768f9

# `investigation.py`

## Summary
- `cmoc oracle investigation` サブコマンドの read-only TUI ワークロードを実装する。調査指示の入力、TUI 起動パラメータの構築、Codex TUI の起動、および oracle 調査向けの自動注入指示を扱う。

## Read this when
- `cmoc oracle investigation` の CLI 実行フロー、調査指示入力、または Codex TUI 起動処理を変更・調査するとき。
- oracle file の読み取り専用制約や realization file の読み書き禁止を、調査ワークロードへどう適用するか確認するとき。

## Do not read this when
- oracle investigation の具体的な TUI 起動パラメータ生成規則だけを確認する場合は、起動パラメータ構築モジュールを直接読む。
- プロンプトエディタ入力の収集や ignore 設定だけを変更・調査する場合は、対応する共通モジュールを直接読む。

## hash
- 2d11eb1f2e99c0309e06cfb882c224853d406790678269499d01886114ce1821

# `review.py`

## Summary
- oracle review の CLI 実行と isolated run lifecycle を統括する実装。review 対象の列挙・review loop 呼び出し・INDEX 差分の commit/merge・中断や失敗時の report・worktree/branch cleanup を、共有する resource ownership と例外処理の境界内で管理する。oracle review のサブコマンド実装と、その run lifecycle の入口として読む。

## Read this when
- oracle review サブコマンドの起動条件、active session branch の検証、review run の隔離 target 作成、review loop から merge/report までの制御フローを確認するとき
- 中断、部分的な resource 作成、cleanup failure、review worktree と run branch の所有権処理を調査または変更するとき
- oracle review における INDEX 差分の commit/merge や失敗時・中断時の report 生成を確認するとき

## Do not read this when
- review 対象ファイルの列挙規則だけを確認する場合は review targets の実装を直接読む
- review loop 内の所見評価や merge operation の詳細だけを確認する場合は review loop の実装を直接読む
- review report の表示形式や出力内容だけを確認する場合は review report の実装を直接読む
- run lifecycle の一般仕様や branch/worktree の正本仕様を確認する場合は、参照されている oracle 文書を直接読む

## hash
- 6ac4648b5fc5439d0aed1aa23065323215e7e29d410b528919846f6a094a120d

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
- oracle review の scope に応じてレビュー対象の oracle file を列挙する処理。full scope では全件、session scope ではセッション開始時点から review fork までに変更された oracle 配下のファイルだけを対象にする。対象判定には repository path 上の oracle file 判定を用い、symlink も扱う。

## Read this when
- oracle review の対象ファイル列挙、scope 別の対象範囲、session fork 間の差分判定を変更・確認するとき。

## Do not read this when
- oracle review の実行処理や、oracle file の内容そのものを確認したいとき。対象列挙後の処理や各 oracle file を直接読む方が適切。

## hash
- 95936d0c2a0e48b4b1d262160a9446dea0d9cb6d80f6fa8fe673a825e6e5ade3
