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
- `cmoc oracle edit` の main worktree 向け TUI workload を実装する。oracle 編集指示の収集、TUI 起動パラメータの構築、indexing preflight、起動前検証、Codex TUI 起動を担当する。
- active な `cmoc/session/` branch、main worktree、clean worktree を要求し、条件不成立時は `CmocError` で再実行案内を返す。

## Read this when
- `cmoc oracle edit` の CLI 動作、TUI 起動処理、oracle 編集指示の受け渡しを変更または調査するとき。
- main worktree・session branch・active session・clean worktree の起動前提を確認するとき。
- oracle edit の step 管理、indexing preflight、設定読み込み、runtime state 参照の連携を確認するとき。

## Do not read this when
- oracle 編集指示の入力収集そのものを変更する場合は、prompt editor input の実装を直接読む。
- TUI 起動パラメータの内容や構築規則を変更する場合は、oracle edit launch builder を直接読む。
- 一般的な CLI runtime や session state の共通仕様を調査する場合は、それぞれの共通 runtime 実装・oracle 文書を直接読む。

## hash
- f94e9d22580ddbdea7684c75c960f3190f4f71d2d6430773e1868710e61b0324

# `investigation.py`

## Summary
- `cmoc oracle investigation` サブコマンドの read-only TUI 実行入口。oracle 調査指示を入力として受け取り、TUI 起動パラメータを構築し、設定を読み込んで Codex TUI を起動する。

## Read this when
- `cmoc oracle investigation` の CLI 実行フロー、入力収集、TUI 起動処理を確認するとき。
- oracle 調査時の read-only 制約や自動注入指示の適用箇所を確認するとき。

## Do not read this when
- TUI 起動パラメータの詳細仕様を確認したいときは、パラメータ構築側を直接読む。
- 共通の CLI 実行基盤、設定読み込み、プロンプト入力処理の仕様を確認したいときは、それぞれの共通モジュールを直接読む。

## hash
- 5b60675fc30fb84c69ec1e5117ec5bb99c04b3bfb6a50e8d105910c0d07e54da

# `review.py`

## Summary
- oracle review の CLI 実行と isolated run のライフサイクルを統括する実装。review target の作成、レビュー loop、INDEX 差分の merge、割り込み・失敗時の report と resource cleanup を扱う。

## Read this when
- oracle review の CLI 実行経路や active session branch の検証を変更するとき
- review worktree・run branch の作成、merge、割り込み、cleanup、失敗 report の挙動を調査または変更するとき
- oracle review の全体 lifecycle と review loop・report・index 操作の接続点を確認するとき

## Do not read this when
- review 対象ファイルの列挙規則だけを変更する場合は review target の実装を直接読む
- 所見の評価 loop 内部だけを変更する場合は review loop の実装を直接読む
- レポートの表示・書式だけを変更する場合は review report の実装を直接読む
- INDEX 差分の commit・merge・conflict 解決だけを変更する場合は review index の実装を直接読む

## hash
- c5d96614701b0728ada22d2b8e4b76946315c6e2f6d07a80ee5ef1e0290ae609

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
- oracle review の finding 列挙、同一対象 finding の関連付け、merge operation 適用、妥当性検証、採否判定を一つの review loop として実行する実装。
- レビュー進捗を保持し、KeyboardInterrupt 時には完了済みの finding と評価済みファイルだけを部分結果として返す。semantic な merge operation 検証失敗には再試行上限を設け、契約違反時はレビューを失敗させる。

## Read this when
- oracle review の列挙・merge・validate・judge のループ挙動を変更または調査するとき
- レビュー中断時の部分保存や evaluated_files、確定済み finding の扱いを確認するとき
- merge operation の target_ids、delete・replace・merge の検証規則や semantic retry を変更するとき

## Do not read this when
- oracle review の prompt parameter 構築だけを変更するときは、各 review parameter builder を直接読む
- oracle review のパス解決規則だけを変更するときは、review_paths の実装を直接読む
- oracle review の CLI 起動や上位コマンドの進捗表示だけを変更するときは、呼び出し元の sub-command 実装を直接読む

## hash
- 57969895f69fcb91848255f0a096f58c74c5cb57d154673d889445b8fbc37503

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
