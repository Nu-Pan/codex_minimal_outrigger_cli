# `__init__.py`

## Summary
- apply サブコマンドの実装パッケージ。apply サブコマンドの処理内容を確認・変更するときの入口。

## Read this when
- apply サブコマンドの実装を確認または変更するとき。

## Do not read this when
- apply 以外のサブコマンドを扱うとき。

## hash
- 0153b6c682ac5e698798223fa6bd60c41cc130afc2127bcf09139fd4d30136e3

# `abandon.py`

## Summary
- 未 join の apply run を破棄し、関連する apply process・worktree・branch・process tracking を整理して apply state を ready に戻す CLI 実装。
- session branch または対象 apply branch 上での実行を検証し、session state と apply branch の対応を確認したうえで cleanup と結果表示を行う。
- apply サブコマンドの abandon 動作や、apply run の cleanup 対象検証を変更・確認するときの入口。

## Read this when
- `cmoc apply abandon` の実装やエラー条件を変更するとき。
- apply run の停止、worktree・branch 削除、state 初期化、process tracking 消去の流れを確認するとき。
- 現在の branch と保存済み session state から cleanup 対象を検証する処理を確認するとき。

## Do not read this when
- apply の開始・実行・join・fork など、abandon 以外のサブコマンドだけを変更・確認するとき。
- apply process の共通 lock や process ID 操作そのものを変更するときは、まず共通 runtime 実装を読む。

## hash
- e6861669b16654fe11d2f69151115e40083c14f489e4dacba8df601f136d7fd1

# `fork.py`

## Summary
- apply fork の実行オーケストレーションを担う。session branch 上で隔離 worktree と apply branch を作成し、対象ファイルの列挙、Codex によるレビュー・修正、差分 commit、finding の再キュー、収束判定、report 出力、apply state・process tracking の更新までを一つの apply run として制御する。中断・初期化失敗・cleanup 失敗時の復旧も扱う。

## Read this when
- apply fork の開始条件、worktree／branch lifecycle、apply loop、対象ファイル列挙、commit subject、state 更新、完了・中断・失敗時の復旧を変更または調査するとき。
- apply run の finding 再キュー、差分の realization／oracle file 判定、前回 join commit からの対象決定を確認するとき。

## Do not read this when
- apply fork 内のファイル単位レビュー・修正プロンプトの生成や実行仕様だけを確認したいときは、レビュー・修正用モジュールを直接読む。
- apply fork の report 内容だけを確認したいときは、fork report の実装を直接読む。
- apply state、共通 git 操作、worktree 操作、Codex 実行基盤そのものだけを確認したいときは、各共通 runtime 実装を直接読む。

## hash
- 4efd0ae892570526be92bd87ebde40e8f2aca0bafeb06768603ab6cb49717d96

# `fork_report.py`

## Summary
- apply fork の実行結果レポートを生成・描画する実装。Git の fork 時点以降の変更差分や未追跡ファイルを収集し、Codex 要約または機械的 fallback で変更内容をまとめる。
- 収束・未収束・中断・エラーの結果、所見数の推移、ブランチや worktree 情報を Markdown + YAML frontmatter のレポートとして保存する。

## Read this when
- apply fork の成功・未収束・中断・エラー時レポートの形式や生成処理を変更するとき
- fork 時点からの tracked、staged、untracked 差分や変更 path の収集挙動を調査するとき
- Codex 要約失敗時や中断時の fallback 変更要約を変更・検証するとき

## Do not read this when
- apply fork のループ制御や所見列挙そのものを変更するとき
- 他のサブコマンドのレポート形式だけを調査するとき
- Git 差分収集やレポート描画に関係しない設定・CLI 入出力を変更するとき

## hash
- 3140342de603dcbbe390791f47ae2033cf82c87d5429d71f98ee012633515914

# `join.py`

## Summary
- apply join の実行単位を担い、apply branch と session branch の差分確認、想定外変更の force-resolve、merge、state 更新、report 保存、process 停止、worktree・branch 後始末を一体で処理する。apply join の CLI 実装と、差分分類・rename 復元・INDEX.md conflict の機械解決などの内部処理への入口である。

## Read this when
- `cmoc apply join` の挙動、事前条件、merge conflict、想定外差分、`--force-resolve`、apply state 更新、report、process 停止、worktree または branch cleanup を変更・調査するとき。
- apply/session branch の managed diff 判定、rename path の復元、INDEX.md conflict の自動解決を確認するとき。

## Do not read this when
- apply join 以外のサブコマンドの実装や、一般的な CLI 実行基盤だけを調査するとき。
- apply join の仕様・出力・状態遷移を確認することが目的で、実装詳細を読む必要がないときは、対応する oracle 文書を先に読む。

## hash
- a83d8a4687f82871d60589fe8627e94d22e23f574dc34aaab2106a524671e06e
