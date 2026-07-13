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
- `cmoc session abandon` の実行本体です。session branch 上で、active な session を home branch へ戻してから破棄し、state を abandoned に更新して結果を表示します。
- 事前条件確認、cleanup、失敗時の rollback と再実行可能状態への復帰までを含むので、session 終了時のブランチ・state の扱いを確認したいときに読む対象です。

## Read this when
- `session abandon` の実行条件、branch 遷移、state 更新、cleanup 失敗時の rollback 方針を確認したいとき。
- session branch を home branch へ戻さずに破棄する流れや、ユーザー中断時の再実行可能性を確認したいとき。

## Do not read this when
- `session abandon` の CLI 入口だけ知りたいときは、より上位のコマンド定義側を読むべきです。
- session ではなく join や apply など別の session 操作を追いたいとき。

## hash
- 616a326f6aea60b890393cdc6e50834f90bf02f71bb6712fa91e53557d3886ac

# `fork.py`

## Summary
- `cmoc session fork` の CLI 実行本体を扱う。現行 branch の検査、managed branch の拒否、作業ツリーの clean 判定、active session の重複防止、session branch 作成、session state 保存、完了表示までをまとめて読む入口。
- `_new_session_id` は session branch と state file の衝突回避に関わる。session-id の一意性や衝突時の失敗条件を確認したいときに読む。

## Read this when
- `cmoc session fork` の開始条件、失敗条件、表示内容、保存される session state を確認したいとき。
- session branch 名や state file 名の生成規則、または session-id 衝突の扱いを確認したいとき。

## Do not read this when
- `cmoc session join` や `abandon` の挙動を知りたいときは、各コマンドの実装へ進む。
- branch 判定や state 保存の共通部品だけを探しているときは、まず `cmoc_runtime` 側を読む。
- session 機能全体の仕様一覧を知りたいだけなら、このファイルではなく上位の app spec を読む。

## hash
- 40837dff685456659e4d693ec0e88ca8203497f4ec94cfd379f7d96bc34ba143

# `join.py`

## Summary
- `cmoc session join` の実行本体です。session branch 上で事前条件を確認し、home branch へ merge して、必要なら conflict 解消を Codex CLI に依頼し、state 更新・branch 削除・結果表示までをまとめて扱います。
- このファイルは `session join` 固有の制御ロジックを読む入口です。merge conflict の対象列挙、conflict marker の残存確認、stage、commit まで含めて確認したいときに進みます。

## Read this when
- `cmoc session join` の実行条件、失敗条件、出力内容、状態遷移を確認したいとき。
- merge 失敗時にどのファイルを conflict 対象にし、どの時点で手動介入を要求するかを確認したいとき。
- session branch の削除可否や、state 更新と git 操作の順序が重要なとき。

## Do not read this when
- `session join` の CLI 入口だけを知りたいときは、上位のコマンド登録側を読むべきです。
- session 機能全体の一覧や、`fork` / `abandon` など別サブコマンドを追いたいとき。
- 一般的な git 操作や Codex 実行規約だけを知りたいときは、このファイルではなく共通実装側を読むべきです。

## hash
- 47d8cabd5fdd2641858ffb632add670674f7d18bcb2450c1c1026c40cd7a8189
