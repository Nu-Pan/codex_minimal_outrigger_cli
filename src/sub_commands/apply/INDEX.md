# `__init__.py`

## Summary
- サブコマンド実装パッケージの入口として、パッケージの役割を短い docstring で示すだけの対象。
- 具体的な処理、公開 API、import 副作用、設定値は持たないため、実装詳細への入口ではなく、パッケージ単位の責務確認に限って使う。

## Read this when
- サブコマンド実装パッケージそのものに、パッケージ説明や初期化時の処理があるかを確認したいとき。
- パッケージ import 時に実行される処理や再 export が存在しないことを本文で確認したいとき。

## Do not read this when
- 具体的なサブコマンドの引数定義、実行処理、入出力、エラー処理を調べたいとき。
- 実装変更やテスト追加のために、実際の制御ロジックを読む必要があるとき。
- パッケージ説明の文言確認以外が目的で、同階層または下位の具体的な実装対象へ直接進めるとき。

## hash
- e5354bb58c94a87f51093db4681c6f341202c07abf4b77772fb37b788f40b7b1

# `abandon.py`

## Summary
- `cmoc apply abandon` の実行本体を扱う。active な apply run を破棄し、apply worktree と apply branch を削除して、apply state と process 追跡情報を ready に戻す。
- 実行位置による分岐、session/apply state の整合性確認、cleanup 対象の検証、削除後の警告表示までをまとめて読む入口。

## Read this when
- `cmoc apply abandon` の挙動や失敗条件を確認したいとき。
- active な apply run を終了させるときに、どの状態確認と cleanup が行われるかを追いたいとき。
- apply branch と session branch のどちらから実行した場合でも同じ破棄処理になる理由を確認したいとき。

## Do not read this when
- session の生成・join・report の処理を知りたいときは、各コマンド実装を読むべきで、この file だけでは足りない。
- apply branch の作成や fork の開始条件を知りたいときは、破棄ではなく開始側の実装を読むべき。
- 共通の state 読み書きや worktree 操作の詳細だけを知りたいときは、対応する runtime helper の実装を直接読むべき。

## hash
- d4c9396e4155bd0f939f69a7754182c3d6fd5425831a6c9238c1592471e82ba6

# `fork.py`

## Summary
- `apply fork` の実行制御をまとめる入口で、session branch 上の前提確認から isolated apply worktree 作成、対象ファイル列挙、Codex による所見適用、commit、state 更新、成功・失敗レポート出力までを追うときに読む。
- 対象ファイルの選び方、重複排除、oracle file と追跡対象の扱い分け、既存 join 由来の差分再開条件を確認したいときに読む。
- commit subject の生成規則や、apply loop の途中で発生した失敗時に PID と report をどう扱うかを確認したいときに読む。

## Read this when
- `cmoc apply fork` の全体フローを変更したいとき。
- apply 対象の列挙条件、重複排除、oracle file を含めるかどうかの境界を変えたいとき。
- apply 成功時・失敗時の state 更新、worktree、report、commit message の振る舞いを確認したいとき。

## Do not read this when
- 単一の finding 列挙ロジックだけを見たいなら、対象の build parameter 側を先に読む。
- finding の実適用手順だけを見たいなら、このファイルではなく finding application 側を読む。
- report の書式だけを見たいなら、このファイルではなく apply fork report 側を読む。

## hash
- 519b9ef548abc6e726f6455c402f56046734b4d43962655e2694d0b549229b1b

# `fork_report.py`

## Summary
- apply fork の実行結果または失敗結果を Markdown レポートとして保存する処理を担う。
- apply worktree 上の fork 起点以降の管理対象差分と未追跡ファイル差分を集め、Codex による変更要約または機械的な fallback 要約をレポートへ含める。
- 収束状態、所見数推移、apply branch や fork commit などの作業文脈を YAML frontmatter と本文に描画する。

## Read this when
- apply fork の作業レポート生成、失敗時レポート生成、保存先、frontmatter、本文構成を確認または変更したいとき。
- apply fork の変更内容要約がどの git diff 範囲、未追跡ファイル、fallback 条件から作られるかを確認したいとき。
- 未収束時の警告文、所見数推移、変更なし表示など、apply fork レポート上の利用者向け文言を扱うとき。

## Do not read this when
- apply fork のループ制御、所見列挙、作業ブランチ作成や worktree 管理そのものを確認したいだけのとき。
- Codex に渡す変更要約用パラメータの schema や prompt の詳細を確認したいとき。
- apply fork 以外のサブコマンドのレポート生成や git 差分取得を扱うとき。

## hash
- 690ca1ebff01a6a1ac9195d36ffc86e75bd1813b5048748f25df508d82db8524

# `join.py`

## Summary
- apply join の実行本体を扱う。session branch / apply branch の整合確認、想定外差分の判定、`--force-resolve` 時の復旧、`git merge`、状態更新、後始末までを一連の流れとしてまとめている。
- apply join の結果レポート生成と、想定外差分の分類・復元・rename 元追跡・INDEX.md だけの conflict 解消もここに含まれる。
- branch や worktree の一般的な runtime 操作は別モジュールに寄せ、このファイルは join 固有の制御と判定に読む。

## Read this when
- apply join の CLI 挙動、成功時の cleanup、失敗時メッセージや report 出力を変えたいとき。
- session branch と apply branch のどちらを対象にするか、どの差分を許可・禁止するか、`--force-resolve` で何を戻すかを確認したいとき。
- merge conflict の扱い、rename を含む想定外差分の分類、結果レポートの内容を追いたいとき。

## Do not read this when
- apply branch を作る・開始する・終了するなど join 以外の apply フローを追いたいときは、より直接の subcommand 実装を読む。
- branch/worktree の基礎操作だけを確認したいときは、このファイルより `cmoc_runtime` や `commons.runtime_apply` を先に読む。
- 単に `INDEX.md` や oracle 側の正本仕様を探しているだけなら、この実装ではなく oracle 文書を読む。

## hash
- f041901b929c362452351cfc4db5c1a6e3a959ad6026c20ca7bd42d70cea0519
