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
- `cmoc apply abandon` CLI の実装。active な apply run を検証し、実行中プロセスの停止、apply worktree と branch の削除、session state の apply 状態を ready に戻す処理を担う。cleanup 中の警告を収集して結果を表示し、補助関数で対象 run の整合性を検証する。

## Read this when
- `cmoc apply abandon` の挙動、エラー条件、cleanup 手順、apply state の reset を変更または調査するとき。
- apply branch・worktree・process tracking・session state の連携を確認するとき。

## Do not read this when
- `apply abandon` 以外の apply サブコマンドの処理だけを調査するとき。
- 共通の apply lock や process 操作の実装詳細を確認したい場合は、先に対応する共通 runtime モジュールを読むとき。

## hash
- 5ce86dd86376452efa2c294276d63a713f6e08bd4efce666a0c7c21fef80b6c2

# `fork.py`

## Summary
- apply fork の一連の実行制御を担う実装。session branch の事前確認から、隔離 worktree・apply state・プロセス追跡の準備、対象ファイルの列挙、Codex によるレビュー・修正ループ、commit、report 出力、完了・中断・失敗時の復旧までを扱う。apply fork の orchestration、状態遷移、worktree cleanup、再調査対象、commit subject の挙動を確認する入口。

## Read this when
- apply fork の実行フロー、対象 scope の決定、apply state の lifecycle、隔離 branch/worktree の作成・cleanup を変更または調査するとき
- Codex review/fix loop、finding に基づく再キュー、commit、収束・未収束・中断・エラー時の挙動を確認するとき
- apply fork の report、PID tracking、abandon と競合する復旧処理を調査するとき

## Do not read this when
- レビュー・修正処理そのものの Codex 呼び出しパラメータを調べる場合は、file review/fix builder の実装を直接読む
- apply fork の report 内容や出力生成だけを調べる場合は、fork report 実装を直接読む
- apply fork 以外の session 操作、join、abandon の主処理を調べる場合は、それぞれのサブコマンド実装を直接読む

## hash
- 81ca549e885026df7c18e6b3dee86e59fce89be0a16f984a7bbe8b605d0aeae0

# `fork_report.py`

## Summary
- cmoc apply fork の実行結果レポートを生成・描画する実装。fork 時点以降の tracked、staged、untracked 差分を収集し、Codex 要約または機械的 fallback で変更内容をまとめる。
- 収束・未収束・エラー・中断時の結果、所見数の推移、ブランチや commit などの frontmatter を Markdown レポートとして保存する。

## Read this when
- apply fork の成功・失敗・中断時レポートの生成や表示を変更するとき
- fork 後の Git 差分・未追跡ファイルの収集、変更要約 fallback の挙動を確認するとき
- apply fork レポートの frontmatter、結果文、所見数、変更内容の形式を確認するとき

## Do not read this when
- apply fork のループ制御、所見列挙、worktree 作成そのものを変更・調査するとき
- レポート以外のサブコマンド出力や一般的な Git 操作を確認するときは、該当する実装・仕様へ直接進む

## hash
- 498293e7a077f29e62bef385a6718d860a5b8e5f0418608335bec2ed2936a05d

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
