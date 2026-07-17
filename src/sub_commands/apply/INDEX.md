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
- apply fork の一連の実行制御を担う実装。session branch の検証、隔離 worktree と apply state の初期化、対象ファイルの列挙、Codex によるレビュー・修正ループ、commit、完了・中断・エラー時の state／report／process tracking／resource cleanup を扱う。apply fork の orchestration と失敗時復旧の入口。

## Read this when
- apply fork サブコマンドの実行フロー、対象スコープ、apply loop、commit subject、完了・中断・エラー時の復旧を変更または調査するとき。
- apply branch、apply worktree、apply state、report、PID tracking のライフサイクルや相互作用を確認するとき。
- apply 対象ファイルの列挙・正規化や、Codex review-and-fix 呼び出しの起点を確認するとき。

## Do not read this when
- apply fork 内の Codex review-and-fix 用 prompt／parameter の詳細だけを確認したいときは、専用の builder 実装を直接読む。
- apply report の出力内容や生成処理だけを確認したいときは、fork report 実装を直接読む。
- apply abandon の cleanup 処理そのものだけを確認したいときは、abandon サブコマンドの実装と関連仕様を直接読む。

## hash
- 72421d07a8a30cc0d811a413c08f8e6caf2a55f041c78b082ae0fb786a7199da

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
