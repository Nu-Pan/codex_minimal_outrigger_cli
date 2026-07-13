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
- `cmoc apply abandon` の実行本体。active な apply run を破棄し、apply state を ready に戻すまでの制御、状態検証、作業ツリーと branch の後始末、追跡中 process の停止をまとめて扱う。

## Read this when
- `apply abandon` の CLI 挙動、破棄可能条件、状態遷移、後始末の責務を確認したいとき。
- apply branch か session branch から実行する処理、session state と apply state の整合確認、worktree と branch の削除順を追いたいとき。
- 破棄処理で process 追跡情報をどう初期化するか、警告をどの条件で出すかを確認したいとき。

## Do not read this when
- `apply abandon` ではなく apply の開始、join、通常の更新フローを見たいとき。
- branch や worktree の基本操作だけを見たいときは、`cmoc_runtime` や `commons.runtime_apply` 側を先に読むべきで、このファイルは不要。
- CLI の共通実行ラッパーや step 表示の実装だけを確認したいときは、`run_cli_subcommand` や `start_subcommand_step` の定義を直接読むべき。

## hash
- ed9998e8cdd362ccaaf1998a48a7139baa51ad042320d94691a76ae104ab1a5e

# `fork.py`

## Summary
- session branch 上の apply fork 実行をまとめる orchestration 入口。run worktree の作成、所見列挙、Codex による適用、commit、state/report 更新までの一連の loop を扱う。
- 対象ファイルの列挙条件や正規化、重複排除、直前の apply merge commit の解決など、適用対象の決定ロジックを読むときにここから入る。
- apply loop の失敗時復旧、process tracking、エラー報告、commit subject 生成、個別 finding 適用の実行経路を追うときに読む。

## Read this when
- apply fork の全体フローを変更したいとき
- 対象ファイルの選び方、正規化、重複排除、再キュー条件を確認したいとき
- Codex 実行後の finding 適用、commit 生成、state/report 更新、異常終了時の処理を追いたいとき

## Do not read this when
- file ごとの finding 列挙ルールだけを見たいなら、対応する列挙用 helper を直接読む
- finding の内容生成や適用パラメータの詳細だけを見たいなら、対応する parameter 生成側を直接読む
- apply 報告書の書式だけを確認したいなら、report 出力側を直接読む

## hash
- ac742f18b1eef2246bca569580737e6ccb09e7c4aada1f11acb69096e36c2e70

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
