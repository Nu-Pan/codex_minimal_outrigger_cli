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
- active session を home branch へ merge せず破棄する `session abandon` サブコマンド実装。実行時コンテキスト取得、session branch と state の事前条件確認、clean worktree 要求、home branch への switch、state の `abandoned` 更新、session branch 削除、結果表示を担う。
- cleanup 失敗時は state を `active` に戻し、可能なら session branch へ戻して、再実行可能性を保つための詳細付き `CmocError` を返す。

## Read this when
- `cmoc session abandon` の外部挙動、事前条件、成功時出力、失敗時エラーを確認または変更する。
- session branch を merge せず破棄し、home branch は残しつつ session branch だけを削除する処理を確認する。
- cleanup 中の例外、ユーザー中断、state rollback、branch rollback、再実行可能状態への復旧方針を確認する。
- session state の `active` から `abandoned` への更新、`joined_at` の扱い、state file 書き込みタイミングを確認する。

## Do not read this when
- session 作成、join、通常の merge 完了など、abandon 以外の session lifecycle を確認したい。
- git 操作、state 読み書き、worktree 検査、CLI runtime 実行ラッパーの共通実装自体を確認したい。
- oracle 上の `session abandon` 正本仕様を確認したい。

## hash
- f32f7a66d991cb31193050f5a2c915d260df0590ce18f0ba9e498c64d725d9bd

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
- `cmoc session join` の実行本体を持つ実装。`session join` の起動、事前条件確認、`git switch` / `git merge`、conflict 解消の再実行、`session.state` の更新、join 後の branch 削除可否判定までをここで読む。
- 同じ責務の別ファイルを探す前に読む入口であり、`session_join.md` に書かれた外部仕様を実装へ落とす箇所として扱う。

## Read this when
- `cmoc session join` の CLI 実行フロー、事前条件、merge 後の後始末を実装・修正・テストしたいとき。
- conflict 発生時の unmerged path 列挙、Codex CLI への解消依頼、conflict marker 確認、`git add`、merge commit 生成の流れを確認したいとき。
- session branch を安全に削除できる条件や、削除失敗時の warning 扱いを確認したいとき。

## Do not read this when
- session の作成や破棄を扱うときは、fork や abandon の実装へ進む。
- conflict 解消用 agent call の引数構築そのものを確認したいときは、対応する builder 定義を直接読む。
- `cmoc session join` の外部仕様だけを確認したいときは、実装ではなく `oracle/doc/app_spec/sub_command/session_join.md` を読む。

## hash
- f933a93c79ed5d5c1a5c363ce25d0191eefe36774b6368b771a489e92845e778
