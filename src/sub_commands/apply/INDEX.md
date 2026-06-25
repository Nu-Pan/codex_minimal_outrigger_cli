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
- isolated apply worktree 上で apply loop を実行するサブコマンド実装。session branch の状態検証、apply branch/worktree 作成、対象ファイル列挙、finding 列挙、finding 適用、変更 commit、report 作成、状態更新までの制御フローを担う。
- apply 中に編集禁止対象へ差分が出た場合の検出、ロールバック、再実行、最終エラー化の制御を含む。
- apply 対象の scope 解釈、対象 path の正規化・除外条件、変更済み path の取得、commit subject 生成とサニタイズを扱う補助関数群も含む。

## Read this when
- apply fork の実行条件、終了コード、状態遷移、apply branch/worktree/report の生成タイミングを確認または変更したいとき。
- apply scope が rolling、session、full の各場合にどのファイルを finding 列挙対象にするかを確認または変更したいとき。
- apply fork 中に oracle、.agents、memo など編集禁止対象へ差分が出た場合のロールバック挙動やエラー処理を確認または変更したいとき。
- finding 列挙、finding 適用、適用後の git commit、commit subject 生成、未収束時の扱いに関する apply loop の制御を追いたいとき。
- apply fork が Codex CLI 呼び出しへ渡す parameter、cwd、purpose、logger などの接続点を確認したいとき。

## Do not read this when
- apply fork の report 本文や error report の具体的な出力内容だけを確認したいときは、report 生成側を直接読む。
- apply fork 用の Codex prompt/parameter の本文や structured output の詳細だけを確認したいときは、builder 側を直接読む。
- apply process id の保存・削除形式だけを確認したいときは、apply runtime 側を直接読む。
- git wrapper、worktree 作成、設定読み込み、session state の永続化など共通 runtime の低レベル実装だけを確認したいときは、runtime 側を読む。
- apply fork ではない apply サブコマンドの CLI 定義や他サブコマンドの挙動を確認したいときは、それぞれの実装を読む。

## hash
- 6c79d6153f330178786f35d2c2f7ed387250de60958d9f25530f35b54358fd97

# `fork_report.py`

## Summary
- apply fork の実行結果を Markdown report として保存する処理を扱う。通常終了・エラー終了の report 生成、apply fork 差分の要約生成、YAML frontmatter と本文を含む report 描画の入口になる。
- apply fork report は、session/apply branch、fork commit、worktree、結果ラベル、所見数推移、変更要約をまとめ、差分がない場合や構造化要約が空の場合の fallback 表示もここで決める。

## Read this when
- apply fork の実行結果 report の保存場所、ファイル生成、frontmatter、本文構成を確認・変更したいとき。
- apply fork の成功・未収束・エラー結果が report 上でどう表現されるかを確認・変更したいとき。
- apply fork worktree の git diff を Codex に渡して変更要約を作る流れ、または差分なし・要約空の場合の fallback を確認・変更したいとき。
- finding count の loop ごとの表示や、変更カテゴリ・要約・変更 path の report 表示を扱うとき。

## Do not read this when
- apply fork のループ制御、所見検出、収束判定そのものを調べたいだけのとき。
- apply fork の変更要約プロンプトや Structured Output schema の詳細を変更したいとき。
- reports directory や timestamp の共通仕様、git 実行 helper、session state 定義を調べたいとき。
- 通常の apply 以外の subcommand report や、apply fork 以外の report 出力を調べたいとき。

## hash
- f8f18a2c7cef586ecd5d69086bce8628dcddbfa215ecd236f482ba1abf8f8cc4

# `join.py`

## Summary
- apply run の成果 branch を session branch へ join する処理を扱う実装。session/apply branch 上での実行判定、state 検証、想定外差分の検出と force-resolve 時の復元、merge conflict 処理、join report 生成、apply worktree と branch の後片付け、利用者向け結果出力をまとめて担う。
- INDEX.md conflict だけを機械解決する補助処理や、apply/session branch それぞれで許可される差分の判定も含むため、apply join の制御フローと安全性境界を確認する入口になる。

## Read this when
- apply join の実行条件、状態遷移、merge、report 出力、apply branch/worktree の cleanup を変更または調査するとき。
- apply join で想定外差分がどのように分類され、--force-resolve でどの commit 基準へ戻されるかを確認するとき。
- apply join の merge conflict 時の挙動、特に INDEX.md conflict の自動解決可否や未解決 conflict report を確認するとき。
- apply 実行中に session branch または apply branch で許可される変更範囲を調整するとき。

## Do not read this when
- apply run の開始、実行、完了状態への更新など、join 前の apply lifecycle を調べたいだけのとき。
- worktree_for_branch など apply worktree 探索 helper の実装詳細だけを確認したいとき。
- git command 実行、state の読み書き、branch 削除、report directory 解決など runtime 共通処理の詳細を調べたいとき。
- INDEX.md エントリーの生成方針や oracle/realization の一般規約だけを確認したいとき。

## hash
- 37fd5df8bdae3c62a5b59b0dd1d99cb58c68b967a220bdea8cdb74dab428989c
