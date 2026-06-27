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
- active な session branch を home branch へ merge せず破棄するサブコマンド実装。CLI runtime 経由で処理本体を実行し、事前条件検証、worktree clean 確認、home branch への切り替え、session state の abandoned 更新、session branch の強制削除、失敗時の state と branch の rollback を扱う。

## Read this when
- session abandon の実行条件、成功時の branch 遷移、state 更新、session branch 削除の挙動を確認したいとき。
- session branch 上でない場合、session/apply state が事前条件を満たさない場合、home branch が無い場合や存在しない場合のエラー処理を確認したいとき。
- abandon 処理中の cleanup 失敗時に、state を active に戻し session branch へ戻る rollback と診断情報の組み立てを確認したいとき。
- session abandon 成功時に利用者へ表示する出力内容を確認したいとき。

## Do not read this when
- session abandon 以外の session サブコマンドの挙動を確認したいとき。
- git 操作、branch 存在確認、state file の読み書き、clean worktree 確認などの共通 runtime helper 自体の実装を調べたいとき。
- session state schema や apply state schema の定義そのものを確認したいとき。
- home branch へ merge する apply 系の処理や、session 作成・開始・一覧表示の処理を調べたいとき。

## hash
- 23d6f74860f9fcc56fc69ec0652b7b89128ecc7a0825164bc853dca21e8c220f

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
- active な session branch を session home branch へ join する CLI 実行本体を扱う実装。事前条件確認、home branch への切替、merge、状態更新、session branch 削除、結果出力までの制御を担う。
- merge conflict 発生時に Codex CLI へ解消を依頼し、conflict marker や unmerged path の残存確認、add、merge commit までを行う conflict resolution 経路を含む。

## Read this when
- session join の実行条件、状態遷移、git 操作順序、出力内容、失敗時の扱いを確認・変更したいとき。
- session join 中の merge conflict を Codex CLI に解消させる処理、conflict marker 検出、unmerged path 検査、merge commit 作成の挙動を確認・変更したいとき。
- session branch から home branch へ合流した後の状態保存や session branch 削除失敗時 warning の扱いを調べたいとき。

## Do not read this when
- session join 以外の session サブコマンドの通常処理を調べたいとき。
- Codex CLI に渡す conflict resolution parameter の具体的な組み立てを調べたいとき。
- state schema、branch 名の管理、repo/work root 解決、git 実行 wrapper など、共通 runtime の詳細を調べたいとき。
- INDEX.md 生成や indexing preflight の共通仕様・実装を調べたいとき。

## hash
- c265941188148d6e1c5f9b536ccc09d3f3872b1706107b5666ba668c41374a35
