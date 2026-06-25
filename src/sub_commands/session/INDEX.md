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
- active な session branch を home branch に merge せず破棄する `cmoc session abandon` の実装。現在 branch と session state を検証し、clean worktree と cmoc ignore 状態を確認したうえで home branch へ切り替え、session state を `abandoned` に更新し、元の session branch を削除する。
- cleanup 失敗時は state を `active` に戻し、可能なら session branch へ戻す rollback を試み、失敗内容・rollback 結果・関連 branch/state 情報を含む `CmocError` にまとめる。

## Read this when
- `cmoc session abandon` の事前条件、成功時の branch 切り替え、session state 更新、session branch 削除の流れを確認したいとき。
- session abandon の失敗時に、state rollback や branch rollback がどのように試みられ、どの情報がエラー詳細に含まれるかを確認したいとき。
- active session を破棄した後の利用者向け出力項目を確認したいとき。

## Do not read this when
- session を home branch へ取り込む処理や、merge/join 系の完了処理を確認したいとき。
- session 作成、session state file の schema、branch 名の生成規則、path keyword の定義そのものを確認したいとき。
- git helper、worktree 検証、state 読み書きなどの共通 runtime 関数の実装詳細を確認したいとき。

## hash
- 886fed5bb8d716cfa16663f237154a5e45501d336f0d1d954c78a9141cd85831

# `fork.py`

## Summary
- 現在の通常 local branch から cmoc managed session branch を新規作成し、その session state を初期化する session fork 処理を定義する実装。
- 作業ツリーの清潔性、cmoc 管理 branch 上でないこと、同じ home branch に active session がないことを確認してから、Git branch 作成、session metadata 保存、利用者向け結果表示を行う。

## Read this when
- session fork の実行条件、拒否条件、作成される session branch 名や session state の初期値を確認したいとき。
- active session の重複検出、managed branch からの fork 禁止、clean worktree 要求、cmoc ignore 確保が session fork でどう組み合わされているかを調べるとき。
- session fork 成功時に利用者へ表示される情報、または session state file に保存される home branch と開始 commit の由来を確認したいとき。

## Do not read this when
- session fork 以外の session 操作、たとえば既存 session への参加、放棄、統合などの具体挙動を調べたいとき。
- Git コマンド実行、branch 判定、worktree 検査、state file の読み書き形式そのものの共通実装を調べたいとき。
- Typer のサブコマンド登録や CLI ルーティング全体を確認したいだけのとき。

## hash
- 20a60dc2af872ac95e7885c085938ee36695778f1001625fd002721d34b16217

# `join.py`

## Summary
- active session branch を session home branch へ join する実装を扱う。事前条件の検証、home branch への切り替え、merge、状態更新、session branch 削除、結果表示までの一連の制御を担う。
- merge conflict が発生した場合に Codex CLI へ解消を依頼し、conflict marker と unmerged path の残存確認、stage、merge commit 完了までを扱う。

## Read this when
- session join の実行条件、失敗条件、状態遷移、Git 操作順、CLI 表示内容を確認・変更したいとき。
- active session branch を home branch へ merge する処理、join 後の state 更新、joined_at 記録、session branch 削除の扱いを追いたいとき。
- session join 中の merge conflict 解消フロー、Codex CLI へ渡す conflict 解決依頼、解消後の marker 検査や commit 完了条件を確認したいとき。

## Do not read this when
- session join 以外の session サブコマンドの挙動を確認したいとき。
- session state の永続化形式、branch と state file の対応、repo root や clean worktree 判定など共通 runtime helper 自体を調べたいとき。
- Codex CLI に渡す conflict 解決依頼パラメータの具体的な組み立て内容を調べたいとき。

## hash
- 096eb0fa9d7704bb973c4fb8585d421711e59a411656a3088a8bffcd5c450337
