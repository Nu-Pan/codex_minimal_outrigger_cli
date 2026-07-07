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
- session join サブコマンドの実行本体を担う。active session branch を session home branch に切り替えて merge し、成功時に session 状態を joined へ更新し、到達可能な local session branch だけを削除し、結果サマリを出力する。
- merge conflict 発生時は Codex CLI に conflict 解消を依頼し、対象外差分・残存 conflict marker・未解消 unmerged path を検査してから merge commit を完了する。

## Read this when
- session join の事前条件、branch 切り替え、merge、状態更新、session branch 削除、成功時出力を確認または変更したいとき。
- session join の merge conflict 自動解消、Codex CLI へ渡す conflict 対象、oracle conflict 書き込み許可、対象外差分の拒否、merge commit 完了処理を調べるとき。
- Git の unmerged path 検出、作業ツリー差分 snapshot、symlink を含む path fingerprint、conflict marker 残存判定の実装を確認したいとき。

## Do not read this when
- session join 用の Codex prompt や実行パラメータの内容だけを確認したいときは、conflict resolution parameter を組み立てる側を読む。
- session 状態モデル、状態ファイルの schema、branch からの state 読み込みそのものを調べたいときは、runtime や state 定義側を読む。
- session join の正本仕様断片を確認したいときは、対応する oracle doc を読む。

## hash
- 5a9899b688fcb2fafd51d98f9fcc17605740d898a02d33d254b6f774d01ccea8
