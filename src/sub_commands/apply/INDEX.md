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
- 未 join の apply run を破棄し、apply state を ready に戻す apply abandon の実処理を担う実装。
- session branch または apply branch 上で実行されていることを確認し、対象 apply branch と worktree、apply process id、session state を照合しながら破棄処理を行う。
- running 状態なら apply process の停止を試み、apply worktree の削除、apply branch の強制削除、process id file の削除、state.apply の初期化と結果表示までを扱う。

## Read this when
- apply abandon の実行条件、破棄対象の判定、active apply run がない場合のエラー条件を確認したいとき。
- apply branch 上または session branch 上から abandon した場合に、どの root、session branch、apply worktree を使うかを追いたいとき。
- running apply の停止、apply process id file の読み取り・削除、apply worktree と apply branch の削除順序や warning 出力を確認したいとき。
- apply state を ready に戻す処理や、ApplyPart の再初期化、write_state による session state 更新を変更・調査したいとき。

## Do not read this when
- apply run の生成、開始、join、通常完了の挙動を調べたいだけで、破棄処理の詳細が不要なとき。
- apply process id file や apply worktree path の低レベル helper 自体の仕様を調べたいときは、apply runtime helper 側を直接読む。
- branch 操作、worktree 削除、state 読み書き、clean worktree 判定の共通実装を調べたいときは、cmoc_runtime 側を直接読む。
- Typer のコマンド登録や CLI 全体のサブコマンド配線だけを確認したいとき。

## hash
- c244472d3c7aab7bfbdafb0b800c434a34ed297fbd8116a6861c168385636c51

# `fork.py`

## Summary
- isolated apply worktree 上で apply loop を実行し、scope に応じた調査対象の列挙、finding 列挙、finding 適用、変更コミット、レポート作成、session state 更新までを統括する実装。
- apply 実行中に編集禁止対象へ差分が出た場合の検出・ロールバック・再試行、apply 対象として扱える通常テキストファイルへの正規化、Codex CLI による commit subject 生成もここで扱う。

## Read this when
- apply fork サブコマンドの実行条件、session/apply state 遷移、apply branch/worktree 作成、process id 管理、成功・失敗時のレポート出力を確認または変更したいとき。
- apply scope ごとの finding 列挙対象、変更済み path の再投入、重複排除、oracle・memo・INDEX・binary・git ignored file の除外条件を確認したいとき。
- finding 適用時に編集禁止対象の差分を戻す制御、再試行後も差分が残る場合のエラー処理、適用後 commit message 生成と commit 作成の流れを確認したいとき。

## Do not read this when
- apply fork の Codex 呼び出し用 prompt や AgentCallParameter の詳細だけを確認したい場合は、その builder 側を読む。
- apply fork のレポート本文やエラーレポートの構成だけを確認したい場合は、レポート生成側を読む。
- apply process id の保存形式や共通 runtime helper の実装だけを確認したい場合は、apply runtime または cmoc runtime 側を読む。

## hash
- 571226ee0c7d1c40ee03cb77e7a3b672e1ff784d6ebd8ec67a09353207ea2b02

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
- apply run 完了後またはエラー後に、apply branch の成果を session branch へ merge して apply state を初期状態へ戻す処理を担う。
- session/apply branch の状態検証、想定外差分の検出と force-resolve 時の復元、merge conflict の扱い、join report 作成、apply worktree と branch の後片付けまでを扱う。
- apply join の CLI ラッパーと実処理、join report の描画、想定差分判定、復元、INDEX.md だけの conflict 自動解決 helper への入口になる。

## Read this when
- apply run の結果を session branch に取り込む join 処理の条件、状態遷移、副作用を確認したいとき。
- apply join がどの branch 上で実行可能か、clean worktree や apply state をどう検証するかを調べるとき。
- apply/session branch の想定外差分判定、--force-resolve による復元 commit、merge conflict 時の report 出力を変更したいとき。
- apply join 後に apply worktree を削除し apply branch を消す条件や、削除できない場合の warning 出力を確認したいとき。
- INDEX.md だけの merge conflict を機械的に解決する特例を確認したいとき。

## Do not read this when
- apply run の開始、apply branch の作成、または作業用 worktree の初期化だけを調べたいとき。
- session state のデータ構造そのもの、永続化形式、branch からの state 読み込み規則を確認したいだけのとき。
- git wrapper、worktree 探索、report 保存先、cmoc ignore 判定などの共通 runtime helper の詳細を調べたいとき。
- apply join 以外の subcommand の CLI 定義や dispatch だけを確認したいとき。
- oracle file や realization file の仕様上の扱い、INDEX.md 生成ルールそのものを確認したいとき。

## hash
- db531dc6c7d8aed77c5678dc687dbaa7f52d1681cacaf8da526854a53562291f
