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
- `apply abandon` サブコマンドの実行本体を提供する。session branch または apply branch 上で、未 join の active apply run を破棄し、apply process の停止、apply worktree と apply branch の削除、process id の削除、session state の ready 復帰、結果表示までを扱う。

## Read this when
- `cmoc apply abandon` の実行条件、失敗条件、状態遷移、削除対象、出力内容を確認したいとき。
- running 状態の apply run を abandon する際の process id 読み取り、停止処理、警告の扱いを確認したいとき。
- apply branch 上と session branch 上のどちらから実行した場合に、どの worktree・branch・state file を対象にするかを調べたいとき。

## Do not read this when
- apply run の開始、join、状態生成など abandon 以外の apply 操作を調べたいとき。
- worktree 削除、branch 削除、process 停止、state 読み書きの低レベル実装そのものを確認したいとき。
- CLI subcommand 共通の実行ラッパーやエラー表示の仕組みを調べたいとき。

## hash
- ef1be500d0c01731d346c9b7fd3cce45a56737e2215aa3760b4307ca13925785

# `fork.py`

## Summary
- apply fork の 1 回の実行を開始し、isolated worktree 上で対象ファイル列挙、Codex による finding 列挙と適用、変更 commit、apply state 更新、report 生成までを制御する。
- scope、session state、前回 join 履歴、変更差分から apply finding の調査対象を決め、oracle file・realization file・除外対象の境界に従って対象を正規化する。
- apply fork の orchestration 全体を一つの loop として扱い、apply state、worktree、再キュー、commit subject、失敗時 report の復旧条件を同じ文脈で管理する。

## Read this when
- apply fork サブコマンドの事前条件、branch/worktree 作成、apply state の running/completed/error 遷移、process id 管理を確認または変更したいとき。
- apply fork がどのファイルを finding 列挙対象にするか、scope ごとの差分基準、oracle file や git ignored file の除外条件を確認または変更したいとき。
- Codex による finding 列挙・finding 適用の呼び出し、適用後の再キュー、commit message 生成、converged/unconverged/error report の扱いを確認または変更したいとき。
- apply fork の失敗時に state や report path がどう更新されるか、stdout や returncode がどう決まるかを追うとき。

## Do not read this when
- apply fork の report 本文の書式や出力内容だけを変更したいときは、report 生成側を直接読む。
- Codex に渡す finding 列挙・finding 適用プロンプトや parameter の詳細だけを変更したいときは、builder 側を直接読む。
- apply 以外のサブコマンド、join 処理、session 作成処理、共通 CLI runtime の一般仕様を調べたいだけのときは、それぞれの担当箇所を読む。
- oracle file や realization file の定義そのもの、INDEX.md 生成規則、path model の正本仕様を確認したいだけのときは、oracle 側の該当文書を読む。

## hash
- b248a93c6cd1cce17d3f14a48961350a5cf2b13ef24acef803841c1ba626a0c1

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を Markdown レポートとして保存する処理を担う。
- apply worktree 上の fork 起点以降の管理対象差分と未追跡ファイル差分を集め、Codex による変更要約または機械的な fallback 要約をレポートへ含める。
- 収束状態、所見数推移、apply branch や fork commit などの作業文脈を YAML frontmatter と本文に描画する。

## Read this when
- apply fork の作業レポート生成、失敗時レポート生成、保存先、frontmatter、本文構成を確認または変更したいとき。
- apply fork の変更内容要約がどの git diff 範囲、未追跡ファイル、fallback 条件から作られるかを確認したいとき。
- 未収束時の警告文、所見数推移、変更なし表示など、apply fork レポート上の利用者向け文言を扱うとき。

## Do not read this when
- apply fork のループ制御、所見列挙、作業ブランチ作成や worktree 管理そのものを確認したいだけのとき。
- Codex に渡す変更要約用パラメータの schema や prompt の詳細を確認したいとき。
- apply fork 以外のサブコマンドのレポート生成や git 差分取得を扱うとき。

## hash
- 690ca1ebff01a6a1ac9195d36ffc86e75bd1813b5048748f25df508d82db8524

# `join.py`

## Summary
- apply run の完了またはエラー状態を session branch へ join する CLI 処理を扱う。apply branch/session branch の検証、想定外差分の検出と force-resolve、merge、state 更新、report 出力、apply worktree/branch の後片付けまでを担う。
- apply join 時に許可される差分範囲、INDEX.md conflict の機械解決、root memo や oracle file の扱いなど、join 固有の branch 差分分類ロジックへの入口になる。

## Read this when
- apply join の実行条件、失敗条件、force-resolve の挙動、merge conflict 処理、join 後の state 更新や cleanup を確認・変更したいとき。
- apply branch と session branch のどの変更を想定内または想定外として扱うかを確認・変更したいとき。
- apply join の結果レポート内容、保存先、CLI 表示内容を確認・変更したいとき。
- INDEX.md の merge conflict を自動解決する条件や、apply worktree/branch を削除せず残す条件を確認したいとき。

## Do not read this when
- apply run の開始、apply branch の作成、agent 実行そのものを扱う場合は、apply join ではなく apply 開始側の処理を読む。
- session state のデータ構造、git wrapper、worktree 探索、report directory の共通実装だけを確認したい場合は、runtime や共通 helper を直接読む。
- oracle file や realization file の一般定義、ファイルアクセス規則そのものを確認したい場合は、仕様文書を読む。

## hash
- 53094712717080e09e22d5e504c61f7e7180669a215ad4abb5ef24366a828982
