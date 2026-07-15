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
- `cmoc session join` の実行経路をまとめた入口。現在の session branch を session home branch へ merge し、状態更新・ブランチ削除・結果表示までの一連の流れを追うときに読む。
- merge conflict を Codex CLI に解消させる分岐、残存 conflict marker の検査、unmerged path の確認を含むため、join 時の失敗時挙動や手動介入の境界を確認したいときにも読む。
- ここは join のオーケストレーションに集中しているので、conflict 解消用の引数構築や下位の session 状態定義だけを知りたい場合は、より直接の定義側を読む。

## Read this when
- session join サブコマンドの実行順序、事前条件、成功時の状態更新と出力を確認したい。
- merge conflict 発生時に Codex CLI へ何を渡し、どの条件で再試行や手動解決に切り替わるかを確認したい。
- session branch の削除条件や、merge 済み判定の取り方を確認したい。

## Do not read this when
- session の状態スキーマや永続状態の定義そのものを知りたいだけなら、状態定義側を読む。
- conflict resolution 用のパラメータ生成だけを知りたいなら、この実行オーケストレーションではなく引数構築側を読む。
- 他の session 系サブコマンドの routing を知りたいだけなら、join 実装ではなく該当サブコマンドの入口を読む。

## hash
- baf48c0407f1dbe353ef0915cfe2d1c6630d41873d95cde6b512cc05b8891e47
