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
- active session を home branch へ merge せず破棄する CLI サブコマンド実装。session branch 上で事前条件と clean worktree を確認し、home branch へ切り替え、state を abandoned に更新して session branch だけを削除する。
- cleanup 失敗時は state を active に戻し、可能なら session branch へ戻って、手動復旧に必要な詳細を含む CmocError を出す。

## Read this when
- session abandon の実行条件、成功時の branch 切り替え、state 更新、session branch 削除の挙動を確認したいとき。
- session abandon の失敗時 rollback、cleanup error、手動復旧メッセージを変更または調査するとき。
- session branch と home branch の扱い、特に home branch を保持して session branch だけを削除する処理を確認したいとき。
- session abandon の CLI 出力内容や runtime 経由のサブコマンド実行方法を確認したいとき。

## Do not read this when
- session abandon の正本仕様そのものを確認したいだけなら、対応する oracle doc を読む。
- session abandon 以外の session 操作、merge を伴う完了処理、または session 作成処理を調べたいときは、それぞれのサブコマンド実装へ進む。
- git 操作、state 読み書き、worktree 検証の共通 helper の詳細を調べたいときは、runtime 側の実装を読む。

## hash
- abd53dc11ea61498a8c9269fe10304cf0e91d10b35042b89baa96b3c7f9753bb

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
- `session join` の実行本体を担い、active session branch を session home branch へ merge し、状態更新、session branch 削除判定、CLI 出力までを扱う。
- merge conflict 発生時は Codex CLI に解消を委譲し、conflict 対象外の差分混入、残存 conflict marker、unmerged path を検査して merge commit まで進める。
- session branch・apply 状態・clean worktree・cmoc ignore・home branch の事前条件と、post-precondition 失敗時の stderr 報告境界を実装する。

## Read this when
- `session join` の事前条件、merge 手順、状態遷移、出力内容、session branch 削除条件を確認または変更したいとき。
- `session join` の merge conflict 自動解消、Codex CLI へ渡す conflict 対象、oracle conflict 書き込み許可、対象外差分の拒否ロジックを確認したいとき。
- conflict marker 検出、unmerged path 検査、merge commit 実行、git status に基づく変更スナップショットの扱いを調べたいとき。
- `session join` 実行中の git 操作失敗をどの出力経路で報告するか、または手動解決が必要な失敗の扱いを確認したいとき。

## Do not read this when
- session join 以外の session サブコマンドの実装を調べたいとき。
- Codex CLI に渡す conflict 解消 prompt や parameter の組み立て自体を変更したいときは、その builder 側を読む。
- branch/state/path model の正本仕様や状態データ構造そのものを確認したいときは、対応する oracle または runtime 側を読む。
- INDEX.md 生成、ルーティング文書、preflight indexing の一般仕様だけを調べたいとき。

## hash
- 959ce69a327c7a5d0acfeee433ffbf92f16512b48b5eb03b065888e2e3a08f80
