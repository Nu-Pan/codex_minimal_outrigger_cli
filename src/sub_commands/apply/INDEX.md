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

# `_runtime.py`

## Summary
- apply 実行時に使う worktree 特定、apply 用 branch 名から期待される worktree path の導出、apply process の pid 状態ファイル操作、実行中 apply process の停止確認を扱う補助実装。
- git worktree list の porcelain 出力を読んで branch が checkout されている linked worktree を探し、見つからない場合や apply branch 形式が不正な場合は CmocError で利用者向けの確認手順を返す。
- apply process の pid は session_id ごとに状態ディレクトリへ保存・読取・削除され、abandon 系処理では自己 process を停止対象から除外したうえで TERM、待機、KILL、待機の順に終了を確認する。

## Read this when
- apply が対象にする session branch または apply branch の worktree をどのように特定するか確認・変更したいとき。
- apply 用 branch 名から worktree 配置を導く規則や、不正な branch 名に対するエラーを確認・変更したいとき。
- apply process の pid 状態ファイルの保存場所、書き込み、読み取り、削除の挙動を確認・変更したいとき。
- cmoc apply abandon などで実行中 apply process を停止する手順、自己 process 停止の禁止、TERM/KILL 待機、process 存在判定を確認・変更したいとき。

## Do not read this when
- apply サブコマンドの CLI 引数、利用者向けコマンド分岐、全体の実行フローを確認したいだけのときは、呼び出し元の command 実装を読む。
- session state の schema、apply.apply_branch の意味、session_id の生成・管理を確認したいときは、状態モデルや session 管理側を読む。
- git 操作の共通 wrapper、worktrees root の定義、CmocError の表示形式を確認したいときは、共通 runtime 側を読む。
- apply 結果の差分反映、ファイル変更、コミット操作、またはテスト観点を確認したいときは、それぞれの処理本体または対応するテストを読む。

## hash
- 9d43928760557507a0e04d8c88e82d54d6d3eaed0d02298e8b76fe2a0f5eee0b

# `abandon.py`

## Summary
- 未 join の active apply run を破棄し、apply state を ready に戻す処理を実装する。session branch または対象 apply branch 上で実行され、作業ツリーの clean 確認、必要に応じた実行中 apply process の停止、apply worktree と apply branch の削除、process id の削除、state の初期化、結果出力を扱う。

## Read this when
- active な apply run を破棄して session を再び apply 可能な ready 状態へ戻す挙動を確認・変更したいとき。
- apply run の破棄時に、現在 branch、session state、apply branch、apply worktree、process id がどの順序で検証・削除されるかを追いたいとき。
- apply state が running の場合に process id を読み、apply process 停止を試みる制御を確認したいとき。
- apply worktree や apply branch が既に存在しない場合の warning 出力、または破棄後に orphan が残った場合の warning 出力を確認したいとき。

## Do not read this when
- apply run を作成・開始・join する通常フローを調べたいだけのとき。
- apply 専用 worktree の期待パス計算、process id ファイルの読み書き、process 停止処理そのものの詳細を調べたいとき。
- session state のデータ構造、branch 操作、worktree 操作、clean worktree 判定などの共通 runtime 実装を調べたいとき。
- active apply run が存在しない状態での利用者向けコマンド一覧や CLI 登録だけを確認したいとき。

## hash
- a71f5892659911c33b485305dbb89dfa9b6a8a407374ddedf2b8eed865935e11

# `fork.py`

## Summary
- isolated apply worktree 上で Codex CLI による apply loop を実行する処理を担う。session branch と apply 状態の事前条件確認、apply 用 branch/worktree 作成、対象ファイル列挙、finding 列挙、finding 適用、差分 commit、report 出力、状態更新までの制御フローをまとめて扱う。
- apply 中に編集禁止対象へ差分が出た場合の検出・ロールバック・再実行制御、commit subject 生成、対象候補の重複排除・変更 path 抽出・finding 列挙対象への正規化もこの実装に含まれる。

## Read this when
- apply fork サブコマンドの実行条件、状態遷移、apply branch/worktree の作成、process id の記録・削除、成功・失敗時の report 出力を確認または変更したいとき。
- apply scope ごとの調査対象ファイル選定、oracle や編集禁止領域を含めるかどうか、binary・git ignored・INDEX.md を除外する条件を確認または変更したいとき。
- Codex による finding 列挙、finding 適用、適用後差分の commit 化、commit message 生成 prompt、unconverged 時の終了コードに関わる挙動を確認または変更したいとき。
- apply fork 中に編集禁止対象へ生じた差分を検出して戻す処理、再実行後も差分が残る場合のエラー化を確認または変更したいとき。

## Do not read this when
- apply fork の report 本文の構成や書き込み形式だけを確認したい場合は、report 生成側を直接読む。
- Codex 呼び出し用 parameter の具体的な prompt/schema 構築だけを確認したい場合は、apply fork 用 builder 側を直接読む。
- apply process id の低レベルな保存・削除実装だけを確認したい場合は、apply runtime 側を直接読む。
- 汎用的な git 実行、worktree 作成、状態ファイル読み書き、config 読み込みの基盤挙動だけを確認したい場合は、runtime 側を直接読む。

## hash
- 8fb74920b4bdbc01a721a1c83c0e04ee178e3bd9bdeed5ce4d06a6d8f70e92b8

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗時の report を生成する実装。git diff から変更要約を作り、要約生成に失敗した場合は変更 path の記録へフォールバックし、結果・所見数・変更要約を Markdown report として書き出す。

## Read this when
- apply fork の report 出力内容、frontmatter、結果ラベル、所見数、変更要約の描画を確認・変更したいとき。
- apply fork の差分要約生成、差分なし時の扱い、要約生成失敗時のフォールバック、変更 path 収集の挙動を確認・変更したいとき。
- apply fork 実行後またはエラー時に reports 配下へ保存される report の生成タイミングや保存内容を追いたいとき。

## Do not read this when
- apply fork のループ制御、所見検出、作業ツリー作成、branch 操作そのものを確認したいだけのとき。
- Codex に渡す変更要約生成プロンプトや structured output の詳細を確認したいとき。
- report 保存先の基礎ルール、timestamp 生成、git コマンド実行 wrapper の共通挙動を確認したいとき。

## hash
- 970d90ece648fc4a499da74ba1ccb67fa6a3b78d33d87cfd2639a698bb71a42d

# `join.py`

## Summary
- apply run 完了後に apply branch を session branch へ取り込み、apply state を初期状態へ戻す処理を実装している。
- session branch または apply branch 上での実行判定、状態検証、作業ツリーの clean 確認、想定外差分の検出と force-resolve、merge conflict 処理、report 作成、apply worktree と branch の後始末を扱う。
- 想定外差分の分類、許可される apply/session 差分の判定、指定 commit への path 復元、INDEX.md だけの conflict 自動解決など、join 専用の補助処理も同じ責務内にまとまっている。

## Read this when
- apply run を session branch へ join する挙動、実行可能条件、状態遷移、merge、cleanup、CLI 出力を確認または変更したいとき。
- apply join 時の想定外差分検出、--force-resolve による revert、apply/session それぞれで許可される差分の境界を確認または変更したいとき。
- apply join report の保存場所、front matter、結果文、unexpected changes、merge conflicts の記録内容を確認または変更したいとき。
- apply branch の merge conflict 処理、特に INDEX.md だけの conflict を自動的に削除 commit で解決する挙動を確認または変更したいとき。
- join 成功後に apply worktree を削除し apply branch を削除する条件、削除できなかった場合の warning を確認または変更したいとき。

## Do not read this when
- apply run の開始、実行、完了状態への更新そのものを調べたいだけのとき。
- session state の型定義、永続化形式、branch や worktree 操作の共通 helper 実装を調べたいとき。
- apply join 以外の subcommand の CLI 定義、引数登録、dispatch を調べたいとき。
- oracle file の正本仕様や INDEX.md 生成規則を確認したいとき。
- 単に report directory、timestamp、git command wrapper、ignore 判定などの共通 runtime 処理を調べたいとき。

## hash
- 2a1da1b962174c71616a4b03cb8ccb7ce5fef62d5005be60a6f8382527cdd066
