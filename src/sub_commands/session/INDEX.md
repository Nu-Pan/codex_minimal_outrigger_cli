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
- session join サブコマンドの実行本体を扱う。active session branch を session home branch へ merge し、state 更新、session branch 削除判定、利用者向け結果出力までを担当する。
- merge conflict 発生時に Codex CLI へ conflict 解消を依頼し、conflict 対象外の差分混入、未解消 marker、unmerged path を検出して merge commit まで進める制御を含む。
- session join の事前条件確認、clean worktree 確認、cmoc ignore 確認、post-precondition failure の stderr 報告指定など、CLI runtime と git 操作をつなぐ入口として読む。

## Read this when
- session join の実行条件、状態遷移、merge 先、session branch 削除可否、結果出力を確認または変更したいとき。
- session join 中の merge conflict 解消フロー、Codex CLI に渡す conflict 対象、oracle conflict 書き込み例外、対象外差分の拒否を確認または変更したいとき。
- conflict marker 検出、unmerged path 検出、merge commit 実行、git status snapshot や path fingerprint による差分監視の挙動を確認したいとき。
- session join の失敗時に CmocError がどの文脈情報や stderr 報告指定を持つか調べたいとき。

## Do not read this when
- session join conflict 解消用に Codex CLI へ渡す prompt や実行 parameter の内容だけを確認したい場合は、builder 側の conflict resolution 定義を読む。
- session state や apply state のデータ構造、永続化形式、branch と state file の対応を確認したいだけの場合は、runtime や state model の定義を読む。
- 他の session サブコマンドの CLI 仕様や処理を調べたい場合は、それぞれのサブコマンド実装へ進む。
- INDEX.md エントリー生成や indexing preflight 自体の仕様を調べたい場合は、indexing 側の実装を読む。

## hash
- 2bab0b8755c1f1ea15a06cb24170cd761e236bc680131d28c9f38200241e073d
