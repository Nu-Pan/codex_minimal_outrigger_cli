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
- `cmoc session abandon` の実処理をまとめる。active な session を破棄し、home branch へ戻して session branch だけを削除する。失敗時は state と branch を元に戻して再実行可能な状態に復帰する責務を持つ。

## Read this when
- session の破棄フローを変更したいとき。
- cleanup 中の rollback や中断時の再実行可能性を変えたいとき。
- session branch の削除条件、home branch への切り替え順、session state の `abandoned` 化を確認したいとき。
- このサブコマンドの利用者向け出力を変えたいとき。

## Do not read this when
- session の作成・参加・継続の処理を見たいときは、これではなく該当サブコマンド側を読む。
- branch/state の低レベル操作だけを確認したいときは、まず共通の runtime や git/state 操作側を読む。
- CLI 起動や step 管理の共通仕組みだけを見たいときは、個別サブコマンドではなく共通層を読む。

## hash
- d71932d5c122862305302cef12235d93296e3bf83a130082246045290c65d9cc

# `fork.py`

## Summary
- `cmoc session fork` の実体実装。現在の local branch を session の home branch として扱い、session branch 作成、session state 保存、失敗時の巻き戻しまで確認したいときに読む。
- CLI 入口ではなく、branch 条件・active session の再確認・session-id 生成・rollback の制御を変更するときに読む。

## Read this when
- `cmoc session fork` の挙動を修正したい。
- 現在の branch から session branch を作る条件、既存 active session の拒否、state file 生成、失敗時の cleanup を確認したい。
- 一意な session-id の生成条件や、session branch と state file の衝突回避を見たい。

## Do not read this when
- CLI の引数定義やサブコマンド配線だけを確認したい場合は、main 側の entry を読む。
- session 作成後の join / abandon / apply / review の仕様を知りたい場合は、それぞれの対象を読む。
- branch model 全体の整理だけが目的なら、より上位の branch / session の仕様を読む。

## hash
- 2d3bca97287f3069ae1782ae1c9e08996401287f8245e506f54c9cfbda8f132b

# `join.py`

## Summary
- session branch を対応する session home branch に merge し、事前条件確認、conflict 解消依頼、merge 完了確認、状態更新、session branch 削除と結果表示までを実行する CLI runtime。
- session join の Git 操作、conflict 対象の NUL 区切り列挙、Codex CLI による conflict marker 解消、残存 marker・unmerged path の検査を担う。

## Read this when
- `cmoc session join` の実行条件、merge 先、branch 削除条件、状態遷移、結果表示を変更・調査するとき。
- session join における merge conflict の検出、Codex CLI への解消依頼、conflict marker 検査、stage・commit 処理を変更・調査するとき。
- session join の失敗時における stderr 出力や、Git path の newline を含む conflict 対応を確認するとき。

## Do not read this when
- session join の conflict 解消パラメータ生成そのものを変更・調査するときは、専用の conflict resolution builder を直接読む。
- session の状態モデル、state ファイルの形式、共通 CLI 実行制御を変更・調査するときは、それぞれの定義元を直接読む。
- session join 以外の session サブコマンドの挙動だけを変更・調査するとき。

## hash
- 99407dc7366639cf1f44ff87052ff42019d7f7277a1f968b48b1e2d168564ed4
