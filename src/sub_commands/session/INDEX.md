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
- `cmoc session fork` の実行本体を持つ。現在の local branch から session branch と session state を新規作成し、競合時は既存 session の存在確認、worktree の clean 確認、失敗時の rollback までまとめて扱う。
- `_new_session_id` は session branch と session state の両方に対する一意性を担保する生成ロジックで、fork 作成時の衝突回避条件を読むときに見る。

## Read this when
- `cmoc session fork` の作成手順、事前条件、失敗時の rollback、表示する結果を確認したいとき。
- session の開始時に、home branch と session branch/state の競合をどう避けるかを確認したいとき。
- session-id の一意性判定に branch と state file の両方が関わる理由を確認したいとき。

## Do not read this when
- `cmoc session fork` の CLI runtime 起動や subcommand 共通の前処理だけを見たいときは、より上位の共通実行層を読む。
- session の join や abandon の振る舞いを知りたいときは、このファイルではなく各サブコマンドの実装を読む。
- session state の保存形式そのものを詳細に知りたいときは、state 定義側を読む。

## hash
- 46bf49b6e4df0d246eaa8480e88b1ddeedb35592c907d27615484f058cc816c0

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
