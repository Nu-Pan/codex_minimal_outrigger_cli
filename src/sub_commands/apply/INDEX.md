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
- isolated apply worktree 上で Codex CLI による apply loop を実行し、scope に応じた対象列挙、finding 列挙、finding 適用、変更コミット、レポート作成、session state 更新までを統括する実装を扱う。
- apply 中に編集禁止対象へ差分が出た場合の検出、未コミット差分の rollback、再実行、最終エラー化の制御もここにまとまっている。
- apply 対象として扱う通常テキスト file の正規化、重複排除、worktree 変更 path の収集、Codex 出力から commit subject を作る補助処理への入口でもある。

## Read this when
- apply fork の実行条件、session branch・clean worktree・apply state などの事前条件、apply 用 worktree と branch の作成、apply 実行中から完了・エラーへの state 遷移を確認または変更したいとき。
- rolling・session・full の scope ごとに、どの変更 file または全体 file を finding 列挙対象へ回すかを確認または変更したいとき。
- Codex による finding 列挙、finding 適用、適用後変更の commit、commit subject 生成、apply fork report 作成までの apply loop 全体の制御を追いたいとき。
- oracle、.agents、memo など apply 中の編集禁止対象に対する差分検出・rollback・再試行・エラー処理を確認または変更したいとき。
- apply finding 列挙対象から git 管理外、binary、INDEX.md、ignore 対象、必要に応じた oracle 配下を除外する正規化条件を確認または変更したいとき。

## Do not read this when
- apply fork の利用者向けレポート本文やエラーレポートの markdown 構成だけを確認したい場合は、レポート生成を担当する対象へ進む。
- Codex に渡す finding 列挙用または finding 適用用の prompt・AgentCallParameter の詳細だけを確認したい場合は、それぞれの builder を担当する対象へ進む。
- apply process id の保存・削除という runtime marker の低レベルな入出力だけを確認したい場合は、apply runtime 補助処理を担当する対象へ進む。
- git コマンド実行、worktree 作成、state 読み書き、config 読み込み、path model など共通 runtime API の実装だけを確認したい場合は、共通 runtime 側へ進む。

## hash
- d6a3b2ec16181aa4a42bbc016e18d4525b3335ceee8f270e66aa655ee8250de9

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を Markdown report として保存する処理を担う。git diff から変更要約を生成し、生成失敗時は変更 path の機械的な要約へフォールバックし、結果・所見数・変更要約を frontmatter 付き report 本文へ描画する。

## Read this when
- apply fork 後に作られる report の保存先、ファイル生成タイミング、本文構成を確認したいとき。
- apply fork の変更要約が Codex 実行結果、空 diff、例外、空の構造化結果でどう扱われるかを確認したいとき。
- apply fork の report に含まれる result 表示、finding count、変更 path 収集の挙動を変更したいとき。

## Do not read this when
- apply fork のループ制御、worktree 作成、branch 操作そのものを調べたいとき。
- 変更要約を生成するために Codex へ渡す prompt や parameter の中身を調べたいとき。
- apply 以外のサブコマンドの report 生成や、report 保存先 helper の共通仕様を調べたいとき。

## hash
- f113ecf9145fa7473d50065a224ebdae4655f0bc1d06993d77053ebf115c9ecc

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
