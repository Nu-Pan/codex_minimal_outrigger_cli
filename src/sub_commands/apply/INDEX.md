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
- 未 join の apply run を破棄し、apply state を ready に戻す処理を担う。
- session branch または apply branch 上で実行され、対象 apply branch・worktree・process id を掃除し、状態ファイルの apply 部分を初期化して結果と警告を CLI 出力する。

## Read this when
- active な apply run を中断・破棄して ready 状態へ戻す挙動を確認または変更したいとき。
- apply branch、apply worktree、apply process id の削除条件や、削除失敗・既欠損時の warning 出力を確認したいとき。
- session branch と apply branch のどちらから abandon を実行できるか、また実行時に clean worktree を要求する条件を確認したいとき。

## Do not read this when
- apply run の開始、join、通常完了など、破棄以外の apply lifecycle を調べたいとき。
- apply 用 worktree パス、process id ファイル、プロセス停止などの低レベル helper 自体の実装を確認したいとき。
- session state のデータ構造、branch 操作、worktree 操作、clean worktree 判定の共通実装を調べたいとき。

## hash
- b0fc2f6cfbc108dcd378b2ab65b0af8e3ab12b88db8e00fe35862a109e31e67c

# `fork.py`

## Summary
- session branch 上で apply fork を開始し、isolated apply worktree を作成して Codex CLI による finding 列挙・適用・commit・report 生成までの apply loop を制御するサブコマンド実装。
- scope に応じた apply 対象 file の列挙、編集禁止対象差分の検出と rollback、finding 適用後の変更 path 再投入、Codex 生成 commit subject の整形を扱う。

## Read this when
- apply fork の実行条件、状態遷移、apply branch/worktree 作成、process id 管理、正常終了・エラー時 report 生成の流れを確認したいとき。
- rolling、session、full の scope ごとに、どの file を finding 列挙対象にするかを確認または変更したいとき。
- apply fork 中に oracle、.agents、memo など編集禁止対象へ差分が出た場合の rollback と再実行、最終エラー化の挙動を調べたいとき。
- Codex CLI に渡す finding 列挙・finding 適用・commit message 生成の呼び出し条件や、commit message の sanitization を変更したいとき。
- apply loop の収束判定、未収束時の終了コード、変更 commit 作成、dirty target の重複排除や再列挙の制御を追いたいとき。

## Do not read this when
- apply fork の report 本文の構成や出力 markdown の詳細だけを変更したい場合は、report 生成側を読む。
- finding 列挙や finding 適用の AgentCallParameter 構築プロンプトそのものを変更したい場合は、builder 側を読む。
- apply process id の保存形式や削除処理の低レベル実装だけを確認したい場合は、apply runtime 側を読む。
- repo root、worktree 作成、git 実行、state 読み書きなど共通 runtime primitive の実装を調べたい場合は、cmoc runtime 側を読む。

## hash
- f26fdcfc1e13c081731bf08cbf000da34fde33946fe592f7aca081f6a4f68685

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を Markdown report として保存する処理を扱う。report 保存先の作成、timestamp 名の report file 生成、git diff からの変更要約作成、YAML frontmatter と本文の描画をまとめて担う。
- apply fork の report に含める session branch、fork commit、apply branch、apply worktree、result、finding count、change summary の組み立てを確認する入口になる。

## Read this when
- apply fork 実行後または失敗時に生成される report の内容、保存場所、frontmatter、本文構成を確認・変更したいとき。
- apply fork の変更差分をどの git diff 範囲から取得し、Codex に構造化要約させ、空差分や空要約をどう report に出すかを確認したいとき。
- finding count の loop 表示、result label から表示文への変換、change summary の行形式など、apply fork report の Markdown 描画を調整したいとき。

## Do not read this when
- apply fork の実行ループ本体、branch 作成、worktree 操作、state 更新の制御を調べたいだけのとき。
- 変更要約を Codex に依頼する prompt や parameter の詳細を調べたいときは、変更要約 parameter を組み立てる対象を直接読む。
- reports directory や timestamp の共通仕様、git command 実行 wrapper、SessionState や CmocConfig の定義だけを調べたいときは、それぞれの共通 runtime・config 定義を直接読む。

## hash
- 5225eb807c0686a87cc08ac42902b8db251f456d1618867e2a847d2cba9bf17a

# `join.py`

## Summary
- apply run の成果を session 側へ join する処理を担う。session/apply branch の判定、作業ツリー清潔性確認、想定外差分の検出と必要時の復元、apply branch の merge、INDEX.md だけの conflict 自動解決、state 更新、report 生成、apply worktree と branch の後始末までを扱う。
- join 結果の利用者向け出力と保存 report の本文もここで組み立てるため、apply join の成功・失敗時にどの情報が残るかを確認する入口になる。

## Read this when
- apply run 完了後または error 後に session branch へ取り込む制御を変更したいとき。
- apply join が許可される branch/state 条件、clean worktree 要件、apply branch 特定失敗時の扱いを確認したいとき。
- apply/session branch 上の想定外差分の分類、--force-resolve 時の復元・commit、許可される差分の境界を調べたいとき。
- apply branch merge の失敗処理、INDEX.md conflict の機械解決、未解決 conflict report の生成を変更したいとき。
- join 後に session state を ready 相当に戻す処理、last joined oracle snapshot の記録、apply worktree 削除や apply branch 削除の cleanup 挙動を確認したいとき。
- apply join の標準出力や保存 report に含める項目・文言・warning を変更したいとき。

## Do not read this when
- apply run の開始、apply branch/worktree の作成、apply state を completed/error にする処理を探しているとき。
- session の作成・開始・終了、または session state 全体の schema 定義だけを確認したいとき。
- git 実行、branch 削除、worktree 削除、report 保存先、cmoc ignore 判定などの共通 runtime helper の実装自体を調べたいとき。
- INDEX.md エントリー生成や oracle 文書のルーティング仕様そのものを確認したいとき。
- apply join のテスト観点や期待外部挙動だけを見たいときは、対応する realization test を先に読む。

## hash
- f8726217151f3d623d5b78aa87408012ba5cc861e0d26d7bf3a4703eecde6209
