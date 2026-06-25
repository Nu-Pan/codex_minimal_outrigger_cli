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
- 未 join の active apply run を破棄し、apply state を ready に戻すサブコマンド実装。session branch または対象 apply branch 上で実行されることを確認し、状態ファイル・apply worktree・apply branch・apply process id を整理して結果と警告を CLI に出力する。

## Read this when
- apply abandon の実行条件、失敗条件、状態遷移、削除対象を確認したいとき。
- active apply run を中断・破棄する処理で、apply process の停止、apply worktree の削除、apply branch の強制削除、apply state の初期化に関わる挙動を調べるとき。
- apply branch 上から実行された場合と session branch 上から実行された場合の root 解決や branch 照合を確認したいとき。
- apply abandon の CLI 出力に含まれる before/after、apply branch、apply worktree、warnings の内容を確認したいとき。

## Do not read this when
- apply run の開始、join、通常の完了処理など、破棄以外の apply サブコマンド挙動を調べたいとき。
- apply state や process id の低レベルな読み書き helper、worktree path の算出、process 停止 helper 自体の詳細を変更したいとき。
- 一般的な git branch/worktree 操作 helper、state schema、clean worktree 判定の共通実装を調べたいとき。

## hash
- 62bb749659c923570b2d7a686dc18b15a65e83f74ff24eae52a55edaaecf31fe

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
- apply run の完了またはエラー状態を session branch へ取り込む join 処理を実装する。実行位置が apply branch の場合は対応する session worktree へ移動し、状態ファイルを確認して join 可能性を検証する。
- join 前に session/apply 双方の想定外差分を検出し、通常時は report を保存して中止し、force resolve 時は oracle snapshot 等の基準 commit へ戻してから merge する。
- merge 後は apply state を初期化し、join 済み oracle snapshot commit を session state に記録し、report 出力、apply worktree 削除、apply branch 削除を試みる。
- join report の生成、想定外差分の分類、許可差分の判定、force resolve による復元、INDEX.md だけの merge conflict の機械解決を同じ文脈で扱う。

## Read this when
- apply run を session branch に取り込む `apply join` の制御フロー、前提条件、状態更新、cleanup の挙動を確認したいとき。
- join 前に検出される想定外差分の分類条件や、force resolve が session/apply 側の差分をどの基準へ戻すかを確認したいとき。
- join report の内容、保存タイミング、merge conflict や想定外差分がある場合のエラー報告を調べたいとき。
- apply branch と session branch の merge 処理、apply worktree の扱い、apply branch 削除失敗時の warning を調べたいとき。
- INDEX.md だけが conflict した場合に自動で削除 commit して解決する特例を確認したいとき。

## Do not read this when
- apply run の作成、実行、状態を completed/error にする処理を調べたいだけのとき。
- session state や apply state のデータ構造定義、永続化形式、共通 runtime helper の詳細を調べたいとき。
- 通常の git worktree 検出、branch 削除、clean worktree 検証、report directory 計算などの共通処理そのものを変更したいとき。
- apply join の利用者向け仕様ではなく、他の apply サブコマンドの CLI 定義や command 登録だけを確認したいとき。
- INDEX.md の一般的な生成規則やルーティング文書の仕様を調べたいとき。

## hash
- b1aee735dd8c291dd4c8326519dfcb0528563109ac523d403bcc4b646bf9fd8f
