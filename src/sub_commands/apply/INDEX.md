# `__init__.py`

## Summary
- サブコマンド実装パッケージの入口として、パッケージの役割を短い docstring で示すだけの対象。
- 具体的な処理、公開 API、import 副作用、設定値は持たないため、実装詳細への入口ではなく、パッケージ単位の責務確認に限って使う。

## Read this when
- サブコマンド実装パッケージそのものに、パッケージ説明や初期化時の処理があるかを確認したいとき。
- パッケージ import 時に実行される処理や再 export が存在しないことを本文で確認したいとき。

## Do not read this when
- 具体的なサブコマンドの引数定義、実行処理、入出力、エラー処理を調べたいとき。
- 実装変更やテスト追加のために、実際の制御ロジックを読む必要があるとき。
- パッケージ説明の文言確認以外が目的で、同階層または下位の具体的な実装対象へ直接進めるとき。

## hash
- e5354bb58c94a87f51093db4681c6f341202c07abf4b77772fb37b788f40b7b1

# `abandon.py`

## Summary
- `cmoc apply abandon` の CLI 実装。active な apply run を検証し、実行中プロセス・apply worktree・apply branch・process 追跡情報を整理して、session state の apply 状態を `ready` に戻す。

## Read this when
- `cmoc apply abandon` の挙動、cleanup 対象の検証、apply process の停止、worktree・branch 削除、state 更新を変更または調査するとき。
- apply branch と session branch の実行位置による分岐、lock 中の再検証、cleanup 警告や CLI 出力を確認するとき。

## Do not read this when
- apply の開始・実行・完了・join など、abandon 以外のサブコマンドの挙動だけを扱うとき。
- 共通の process lock、worktree 解決、process ID 操作の詳細を確認することが目的で、このファイルの abandon フローを読む必要がないとき。

## hash
- 723d1243b709cbcaa1f10f9dd9aa8ba241e6e0e279a10a629fb90689617f7523

# `fork.py`

## Summary
- apply fork の単一実行を制御するオーケストレーション実装。session branch の検証、隔離 worktree と apply state の準備、対象ファイルの列挙、Codex によるレビュー・修正、差分 commit、収束判定、レポート生成、完了・中断・失敗時の復旧までを扱う。apply fork の実行ライフサイクルや再実行・中断・cleanup 条件を確認する入口。

## Read this when
- `cmoc apply fork` の実行開始条件、対象 scope、apply loop、commit、収束判定を変更・調査するとき
- apply state、apply branch/worktree、プロセス追跡、完了レポートの更新や失敗時 rollback を変更・調査するとき
- apply 対象の正規化・重複排除・列挙、Codex による対象レビューと修正の呼び出しを確認するとき

## Do not read this when
- apply 対象ファイル単位の Codex review/fix パラメータ生成や finding schema の詳細だけを確認したいときは、`file_review_and_fix` の実装を直接読む
- apply 完了後の report 内容や abandon 専用の cleanup 挙動だけを確認したいときは、対応する report または abandon 実装を直接読む
- apply fork 以外の subcommand の実行制御や共通 runtime の一般仕様だけを調査するとき

## hash
- 0575102b1ad2e157603fc18a065c5edc702078440a953bce72d0c823b9fe6a8d

# `fork_report.py`

## Summary
- apply fork の実行結果・失敗結果を Markdown レポートとして生成するモジュール。変更差分の取得、未追跡ファイルの収集、Codex による変更要約と機械的フォールバック、所見数・収束状態・中断警告を含むレポート描画を扱う。apply fork のレポート生成や変更内容要約の挙動を確認する際の実装入口。

## Read this when
- apply fork 完了・中断・エラー時のレポート内容を変更または検証するとき
- fork 時点からの変更差分、未追跡ファイル、変更 path の収集方法を確認するとき
- Codex 要約失敗時やユーザー中断時のフォールバック挙動を確認するとき

## Do not read this when
- apply fork のループ制御や所見列挙そのものを変更するとき
- レポート以外の apply サブコマンドの入出力仕様を確認するとき
- 一般的なレポート保存先やセッション状態の定義を確認するときは、対応する仕様・状態管理のファイルを直接読む

## hash
- cc104036f5111d5a4bdd661d8223b242284d9ef583475e70887bcd195a41898c

# `join.py`

## Summary
- `cmoc apply join` の一連の実行単位を担う実装。apply/session branch の事前条件と差分を確認し、必要に応じて想定外変更を force-resolve し、apply branch を session branch に merge する。
- merge 結果に応じて apply state の更新、Markdown report の保存、apply process・worktree・branch の後始末、CLI 結果と警告の出力までを扱う。merge conflict、rename、tracked/ignored path、INDEX.md・oracle・memo の許可差分判定もこのファイルから追える。

## Read this when
- `cmoc apply join` の挙動、失敗条件、`--force-resolve`、merge conflict、report、state 更新、process 停止、worktree/branch cleanup を変更・調査するとき
- apply/session branch の想定外差分分類、rename 復元、INDEX.md conflict の自動解決を確認するとき

## Do not read this when
- apply join 以外のサブコマンドの処理を調査するとき
- 共通の CLI runtime、session state、Git 操作、apply process lock の一般実装を確認するときは、それぞれの共通モジュールを直接読む

## hash
- de1aa378a9a1f623bbfe00473a289e710e8799fed4b4ed0c12a09fdc521242f1
