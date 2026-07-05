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
- apply abandon サブコマンドの実行本体を定義する実装。session branch または apply branch 上で、未 join の active apply run を破棄し、apply worktree・apply branch・process id を掃除して apply state を ready に戻す。
- apply run の状態検証、実行中 process の停止、session worktree への退避、削除後の orphan 確認、利用者向け結果出力を一連の制御として扱う。

## Read this when
- apply abandon の外部挙動、失敗条件、出力内容を確認または変更したいとき。
- apply run の破棄時に、apply branch、apply worktree、apply process id、session state がどう扱われるかを調べたいとき。
- session branch と apply branch のどちらから実行できるか、また current branch と state 上の apply branch の整合性を確認したいとき。

## Do not read this when
- apply start、apply join など abandon 以外の apply サブコマンドの制御を調べたいとき。
- branch・worktree・state file・process id を操作する低レベル helper の実装詳細だけを確認したいとき。
- CLI runtime の共通ラップ処理や run_cli_subcommand 自体の挙動を調べたいとき。

## hash
- bcdcc131818c1e23500761134a43a75f1277f85f8fc017f5fd2040a8a12a3b7f

# `fork.py`

## Summary
- apply fork の実行開始から isolated worktree 上での finding 列挙、Codex による適用、commit、apply state 更新、report 出力までを一つの apply run として制御する。
- apply scope から列挙対象ファイルを決め、変更後の再キュー、対象重複排除、commit subject 生成、直近 apply join commit の解決も扱う。

## Read this when
- apply fork サブコマンドの事前条件、branch/worktree 作成、apply state 遷移、process tracking、report 出力の流れを確認・変更したいとき。
- apply scope ごとの finding 列挙対象、oracle や ignored file の除外、変更ファイルの再キュー条件を確認・変更したいとき。
- Codex に渡す finding 列挙・finding 適用処理、apply fork 中の commit 作成、unconverged/converged/error の扱いを追いたいとき。
- session 内で前回 join 済みの apply merge commit を起点に差分対象を決める処理を確認したいとき。

## Do not read this when
- apply fork の report 本文生成だけを変更したいときは、report 生成を担う別対象を読む。
- Codex prompt や Structured Output parameter の内容だけを変更したいときは、apply fork 用 builder 側を読む。
- apply fork 以外の apply join や session 管理の CLI 挙動を調べたいだけのときは、それぞれのサブコマンド実装を読む。
- INDEX.md の生成規則や一般的な indexing preflight の実装だけを確認したいときは、indexing 側の対象を読む。

## hash
- eb4270e179eddb7a5759b7c1bbff9ebddb61c2bb089600831a5edf81ea714755

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を Markdown report として保存し、frontmatter、作業結果、所見数推移、変更内容要約を組み立てる実装。
- apply worktree の fork 以降の管理対象差分、未 staged 差分、staged 差分、untracked file 差分を収集し、Codex による構造化要約または path のみの fallback 要約へ変換する。
- apply fork report の出力内容、未収束時警告、変更なし・要約失敗時の表示、削除済み path を除外した差分扱いに関する処理の入口となる。

## Read this when
- apply fork の作業レポート生成、失敗時レポート生成、保存先、Markdown 構成、YAML frontmatter の内容を確認または変更したいとき。
- apply fork で発生した変更差分の集め方、untracked file の扱い、rename や deleted path の扱い、変更 path の重複排除を確認または変更したいとき。
- Codex による apply fork 変更要約の入力、出力が空の場合の扱い、例外時の fallback 要約を確認または変更したいとき。
- 未収束時に所見数推移へ残す注意文や、converged・unconverged・error の report 表示文を確認または変更したいとき。

## Do not read this when
- apply fork のループ制御、branch 作成、worktree 作成、session state 更新そのものを確認したいだけのとき。
- 変更要約を依頼する Codex parameter の prompt や Structured Output schema を確認したいとき。
- report 保存ディレクトリや timestamp の共通仕様、git 実行 wrapper、session state 型の定義を確認したいとき。
- apply fork 以外の sub command の report 生成や差分収集を確認したいとき。

## hash
- a8d4396799cbe46740ee05059b78a5f5dbb4ed8b96b8c2bcb4da78df99122cb3

# `join.py`

## Summary
- apply join サブコマンドの実行本体を担い、apply branch を session branch へマージして apply state を初期状態へ戻す。
- join 前のブランチ種別、session/apply state、作業ツリーの clean 状態、想定外差分、merge conflict を検査し、必要に応じて report 作成・エラー終了・force-resolve による復元を行う。
- apply/session branch 上の許可差分判定、想定外差分の分類、INDEX.md conflict の機械解決、apply worktree と apply branch の cleanup も扱う。

## Read this when
- apply join の実行条件、成功時の状態更新、apply branch/worktree の削除条件を確認したいとき。
- apply join が検出する想定外差分の分類基準、force-resolve 時の復元・commit 挙動、report 内容を変更したいとき。
- apply branch の merge conflict 処理、特に INDEX.md だけの conflict を自動解決する挙動を確認したいとき。
- apply branch 上と session branch 上で許可される変更範囲の判定を調べたいとき。

## Do not read this when
- apply join 以外の apply サブコマンドの作成・実行・状態遷移を調べたいとき。
- CLI 共通のエラー表示、git 実行、state 読み書き、worktree 探索などの基盤処理だけを調べたいとき。
- oracle file や realization file の一般的な定義・ルールを確認したいとき。
- INDEX.md のルーティング文書生成ルールそのものを確認したいとき。

## hash
- 0af4c5756155990fb87e3bd82613cdeeb0953bc7b2f3dd54be6877238e9ac34f
