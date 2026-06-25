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
- isolated apply worktree 上で apply fork の実行全体を制御する realization implementation。session branch と state の事前条件確認、apply branch/worktree 作成、対象ファイル列挙、finding 列挙と適用、変更 commit、report 出力、apply state と process id の更新・後始末を扱う。
- apply fork 中に編集禁止対象へ差分が出た場合の検出・ロールバック・再実行制御、Codex CLI による commit subject 生成、apply scope に応じた調査対象の正規化と重複排除もこの対象にまとまっている。

## Read this when
- apply fork サブコマンドの実行フロー、終了コード、出力内容、state 遷移、process id のライフサイクルを確認・変更したいとき。
- apply scope が full・session・rolling の各場合に、どのファイルを finding 列挙対象にするかを確認・変更したいとき。
- apply fork の finding 列挙、finding 適用、適用後 commit、report 作成までの制御順序や Codex CLI 呼び出し条件を追いたいとき。
- apply fork 中に oracle・エージェント設定・memo などの編集禁止対象へ発生した差分をどう扱うか、ロールバックとエラー化の挙動を確認・変更したいとき。
- apply fork が変更対象から binary、git ignored、INDEX、特定ディレクトリ配下を除外する条件を確認・変更したいとき。

## Do not read this when
- apply fork の report 本文の構成や保存内容だけを確認・変更したい場合は、report 生成を担う対象を読む。
- finding 列挙用または finding 適用用の AgentCallParameter の prompt 構築だけを確認・変更したい場合は、builder 側の対象を読む。
- 通常の apply 実行時 process id の低レベルな保存・削除処理だけを確認したい場合は、apply runtime 側の対象を読む。
- repo root、worktree 作成、git 実行、state 読み書きなど共通 runtime helper の実装だけを確認したい場合は、runtime 側の対象を読む。
- apply fork 以外の subcommand の CLI 定義や Typer command 登録を確認したい場合は、その command 定義を担う対象を読む。

## hash
- 897d7fe865dd1e448402e3d4468a6c9859466d24f87eff8a1637f58f28471cbd

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
- apply run が completed または error になった後、apply branch を session branch へ join する処理を扱う。session/apply branch 上での実行位置判定、clean worktree 確認、想定外差分の検出と force resolve、merge、INDEX.md だけの conflict 自動解決、state 更新、apply worktree/branch cleanup、join report 出力までを担う。
- join report の生成と、apply/session branch の差分が許可範囲内かを判定する補助処理も含む。apply 側では INDEX.md と gitignore 対象外の通常ファイルを許可し、oracle・memo・.agents・.git などを想定外として扱う一方、session 側では INDEX.md・oracle・memo の差分を許可する。

## Read this when
- apply join の実行条件、対象 branch の決定、session state の更新、apply branch の merge と後片付けの流れを確認したいとき。
- apply join 時の想定外差分判定、--force-resolve による revert/commit、または apply/session branch ごとの許可差分ルールを調べたいとき。
- apply branch merge conflict の扱い、INDEX.md だけの conflict 自動解決、未解決 conflict 時の report 生成とエラー内容を確認したいとき。
- apply join report の front matter、Result、Unexpected Changes、Merge Conflicts に出る内容を変更・検証したいとき。

## Do not read this when
- apply run の開始、実行、完了状態への遷移そのものを調べたいだけのとき。
- session branch や apply branch の worktree を探す共通ロジックだけを確認したいとき。
- git 実行、state の読み書き、branch 削除、worktree 削除、report directory、timestamp などの runtime 共通 API の実装を調べたいとき。
- INDEX.md エントリー生成一般の仕様や、oracle/realization の基本概念を確認したいだけのとき。

## hash
- a46597caba8c76a624e78bd71a978eafb8f0f96fc9c12877b16c8d320534558e
