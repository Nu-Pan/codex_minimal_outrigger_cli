# `__init__.py`

## Summary
- session 系サブコマンド実装を収めるパッケージであることを示す、最小限のパッケージ初期化モジュール。
- 具体的な処理や公開 API は定義せず、下位モジュールへ進むための入口として位置づく。

## Read this when
- session 系サブコマンド実装のパッケージ境界や、パッケージ自体に初期化処理があるかを確認したいとき。
- session 配下の実装を調べる前に、この階層がサブコマンド実装用のまとまりかだけを確認したいとき。

## Do not read this when
- 個別の session サブコマンドの処理、引数、入出力、状態操作を調べたいとき。その場合は具体的な実装モジュールを読む。
- 共通 CLI ルーティング、サブコマンド登録、または session 以外のサブコマンド実装を調べたいとき。

## hash
- a2616b13a1c260f66ad6dfda2f7821fc573b581179e92bbad014a023d5958042

# `abandon.py`

## Summary
- active な session branch 上で `cmoc session abandon` を実行し、home branch へ merge せず session を破棄する CLI サブコマンド実装。
- session state と apply state、clean worktree、home branch の存在を事前条件として確認し、home branch へ切り替えた後に state を abandoned に更新して session branch だけを強制削除する。
- cleanup 失敗時は state を active に戻し、可能なら session branch へ戻ったうえで、手動復旧と再実行に必要な情報を含む `CmocError` を返す。

## Read this when
- `cmoc session abandon` の実行条件、状態遷移、branch 切り替え、session branch 削除の挙動を確認したいとき。
- session abandon の失敗時 rollback、cleanup エラー、手動復旧メッセージを調べるとき。
- session abandon が home branch を保持し、session branch だけを削除する実装根拠を確認したいとき。

## Do not read this when
- session を home branch へ取り込む join/merge 系の挙動を調べたいとき。
- session 作成、状態ファイルの一般的な読み書き、git helper の詳細実装を調べたいとき。
- session abandon の正本仕様そのものを確認したいとき。

## hash
- 0754bb47dc52cd1096c081de7fc74b78890a7d701fb6192dbb5b534ba585e223

# `fork.py`

## Summary
- 現在の local branch から cmoc managed branch ではない新しい session branch を作成し、session home branch と開始 commit を記録した session state file を生成する `session fork` サブコマンド実装。
- CLI runtime 経由で実行し、`.cmoc` ignore 設定、clean worktree、既存 active session の不在、session-id と branch/state file の衝突回避を確認してから `git switch -c` と状態書き込みを行う。
- session-id 生成は timestamp を使い、既存 session branch または state file と衝突した場合に一定回数 retry し、失敗時は `CmocError` で利用者向け対処を返す。

## Read this when
- `cmoc session fork` の実行条件、失敗条件、作成される branch/state、または利用者向け出力を確認・変更したいとき。
- 通常の local branch から session branch を開始する処理、active session の重複検出、managed branch 上での禁止判定、clean worktree 要求を調べるとき。
- session-id の一意性判定、timestamp 衝突時の retry、既存 state file が残る joined/abandoned session との衝突扱いを確認したいとき。

## Do not read this when
- session fork 以外の session 操作、たとえば join、abandon、status などの挙動を調べたいとき。
- session state のデータ構造そのもの、state file の schema、または path model の定義を確認したいとき。
- git 実行 wrapper、CLI runtime、worktree clean 判定、branch 判定などの共通 helper の詳細実装を調べたいとき。

## hash
- 5e18dd55b0b201249fadfa3b37594b06e52030b37c4d27622f18755fac7b2096

# `join.py`

## Summary
- `session join` の実行本体を扱う CLI 実装。active session branch の事前条件確認、session home branch への merge、状態更新、session branch 削除判定、利用者向け結果出力を担う。
- merge conflict 発生時に Codex CLI へ conflict 解消を依頼し、conflict 対象外の差分拒否、conflict marker 残存検出、unmerged path 確認、merge commit 完了までの制御を担う。
- git の変更スナップショット、path fingerprint、可変長 conflict marker block 検出など、session join の安全境界を保つための補助処理を含む。

## Read this when
- `cmoc session join` の挙動、事前条件、出力、状態遷移、session branch 削除条件を確認または変更したいとき。
- session join 中の merge conflict 解消フロー、Codex CLI への依頼内容、oracle conflict 書き込み許可、conflict 対象外差分の拒否条件を確認または変更したいとき。
- session join 失敗時のエラー出力先、manual resolution を要求する条件、conflict marker 検出や unmerged path 検査の実装を調べるとき。

## Do not read this when
- session join 用 Codex prompt や conflict resolution parameter の組み立てだけを確認したい場合は、その builder 側を直接読む。
- git status の path status 解析や runtime git wrapper の一般挙動を確認したい場合は、共通 runtime または indexing 側を直接読む。
- session join 以外の session subcommand、apply workflow、または CLI 全体の dispatch を調べる場合は、それぞれの subcommand 実装や runtime 側を読む。

## hash
- 17b55332f672e0cd9519d19f2fcdfc2695585dc4de1c08681a9a3db569e174a9
