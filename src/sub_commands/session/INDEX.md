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
- active session branch を session home branch に取り込む `session join` サブコマンドの実行本体を扱う。事前条件検証、worktree 清潔性確認、home branch への switch と merge、状態更新、session branch 削除、結果表示までの制御をまとめている。
- merge conflict が発生した場合に Codex CLI へ解消を依頼し、conflict marker や unmerged path の残存確認、add と commit まで行う補助処理も含む。

## Read this when
- `cmoc session join` の実行条件、merge 手順、状態遷移、成功時出力、session branch 削除失敗時 warning を確認または変更したいとき。
- session join 中の merge conflict 解消フロー、Codex CLI に渡す対象 path、解消後の conflict marker 検出、git add/commit の扱いを確認または変更したいとき。
- session join の失敗時に `CmocError` がどの条件で発生するか、post-precondition failure を stderr 扱いにする理由を追いたいとき。

## Do not read this when
- session join 以外の session サブコマンドの挙動を調べたいとき。
- merge conflict 解消依頼用の Codex CLI parameter の具体的な構築内容だけを調べたいとき。
- 状態ファイルの schema、branch からの state 読み込み、git wrapper、worktree root の定義など、runtime 共通処理そのものを調べたいとき。

## hash
- 865718edd0972f5bffaf1b915250d8d9130d92c49c2147cdb7f3352456d11a54
