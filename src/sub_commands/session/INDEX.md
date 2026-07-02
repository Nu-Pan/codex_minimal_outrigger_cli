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
- active な session branch で、home branch へ merge せずに session を破棄する CLI 実装を扱う。
- 実行ラッパーから本体処理を呼び、session branch・状態・clean worktree・home branch 存在の事前条件を検証したうえで、home branch への切り替え、状態の abandoned 化、session branch の強制削除、結果表示を行う。
- cleanup 失敗時は state を active に戻し、可能なら session branch へ戻して、rollback 結果を含むエラーを返す。

## Read this when
- session abandon の実行条件、状態遷移、git branch 操作、成功時出力を確認・変更したいとき。
- active session を merge せず破棄する処理で、home branch の保持、session branch の削除、state file 更新の順序や失敗時挙動を調べるとき。
- session abandon が満たすべき oracle 根拠コメント、cleanup 失敗時の rollback とエラー詳細を確認したいとき。

## Do not read this when
- session 作成、apply、merge など、破棄以外の session サブコマンドの処理を調べたいとき。
- session state のデータ構造、永続化形式、branch 操作 helper、worktree clean 判定そのものの実装を調べたいとき。
- CLI 全体のコマンド登録や Typer アプリ構成だけを確認したいとき。

## hash
- e8792415573dda32702ca7f56c0363674bee0c83d42c9b2c7eddc11b8bb8e39d

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
- session join サブコマンドの実行本体。active session branch を session home branch へ merge し、状態更新、session branch 削除、結果表示までを扱う。
- merge conflict 発生時は Codex CLI に conflict 対象の解消を依頼し、対象外差分、残存 conflict marker、unmerged path を検査して merge commit を完了する。

## Read this when
- session join の事前条件、成功時の状態遷移、session home branch への merge、session branch 削除条件、出力内容を確認または変更したいとき。
- session join 中の merge conflict 解消フロー、Codex CLI へ渡す conflict 対象、oracle conflict 書き込み例外、対象外差分の拒否、conflict marker 検出を確認または変更したいとき。
- session join 失敗時のエラー出力先、手動解決を要する merge 状態、git status や merge-base に基づく判定を調査するとき。

## Do not read this when
- session join 以外の session サブコマンドの挙動を調べたいとき。
- Codex CLI に渡す conflict 解消 prompt の内容やパラメータ構築そのものを変更したいときは、conflict resolution parameter builder を直接読む。
- branch 状態ファイルの schema、repo/work root 解決、git 実行 wrapper、CLI 実行 wrapper の汎用挙動を調べたいだけのときは、runtime 側を直接読む。

## hash
- 0cb7e79dd80f8783c5b3b6c434e595030162b2f19376e3d11c5d0ba4a6278031
