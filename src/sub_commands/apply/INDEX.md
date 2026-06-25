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
- isolated apply worktree 上で apply loop を実行し、対象ファイルごとの finding 列挙、適用、禁止領域差分の巻き戻し、変更コミット、レポート生成、apply 状態更新までを統括するサブコマンド実装。
- scope に応じた apply 対象ファイルの列挙・正規化、重複排除、変更ファイル再投入、Codex CLI 呼び出し用パラメータ生成、commit subject 生成結果の整形もこの中で扱う。

## Read this when
- apply fork の実行条件、状態遷移、worktree/branch 作成、process id 管理、成功・失敗時のレポート出力を確認または変更したいとき。
- apply scope ごとの対象ファイル選択、oracle・memo・.agents・INDEX.md・binary・git ignored file を対象外にする判定を確認または変更したいとき。
- apply finding の列挙、finding 適用後の禁止対象差分検出と rollback、再実行、エラー化の制御を追いたいとき。
- apply fork が生成するコミットの作成タイミング、commit subject を Codex CLI で生成する prompt、出力整形 fallback を変更したいとき。

## Do not read this when
- apply fork の最終レポート本文やエラーレポート本文の構造だけを変更したいときは、レポート生成側を直接読む。
- Codex CLI に渡す finding 列挙用または finding 適用用の AgentCallParameter の詳細だけを変更したいときは、各 builder 側を直接読む。
- apply process id の保存形式や削除処理そのものだけを確認したいときは、apply runtime 側を直接読む。
- apply ではない session、join、review など他サブコマンドの CLI 挙動を調べたいときは、それぞれのサブコマンド実装を読む。

## hash
- 82df1a33aa57124772125e76713decba970ff0208550575a8b1ef196f18b12e1

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
- apply run の完了またはエラー状態を session branch へ join する処理を担う実装。session/apply branch の判定、clean worktree 確認、想定外差分の分類と force-resolve、apply branch の merge、INDEX.md のみの conflict 自動解決、report 出力、apply worktree と branch の cleanup、state 更新までを扱う。
- join 結果 report の生成内容、想定外差分として扱う apply/session 側の変更範囲、force-resolve 時の復元 commit と commit 作成、merge conflict が残った場合のエラー導線を確認する入口になる。

## Read this when
- apply run を session branch に取り込む join 処理の挙動を変更・調査するとき。
- join 可能条件、対象 branch の決定、apply branch/worktree の cleanup、state の ready 相当へのリセットを確認したいとき。
- apply join で許容される差分と想定外差分の分類、または --force-resolve による revert 動作を確認したいとき。
- apply branch の merge 失敗時、特に INDEX.md だけの conflict を機械解決する挙動や、未解決 conflict report の内容を調べるとき。
- apply join の標準出力、保存 report、警告行、last_joined_apply_join_commit の更新を検証するテストを書くとき。

## Do not read this when
- apply run の開始、分岐作成、Codex 実行、または apply state を completed/error にする処理を調べたいだけのとき。
- session の作成・終了・状態ファイル schema 全体・path model など、join の制御フローから独立した基盤仕様を調べたいとき。
- apply join 以外のサブコマンドの CLI 定義や Typer option 配線だけを確認したいとき。
- git worktree 探索、state 読み書き、report directory 計算、git wrapper など共有 runtime helper 自体の実装を変更したいとき。

## hash
- 738a7b537ea39a752ccb00c3e1081226d89630ca5ab473246b67df6df85b82b7
