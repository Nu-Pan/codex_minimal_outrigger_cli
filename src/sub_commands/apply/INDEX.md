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
- `cmoc apply abandon` の実行本体を扱う。session branch または apply branch 上で、未 join の active apply run を検証し、実行中 process の停止、apply worktree と apply branch の削除、apply state の ready への復帰、追跡情報の消去までをまとめて確認したいときに読む。

## Read this when
- apply run を中断して cleanup したいとき
- active apply run の有無・所属 session・cleanup 対象 worktree/branch の整合性確認を追いたいとき
- abandon 時の process 停止順序や cleanup 後の state 復帰を確認したいとき

## Do not read this when
- apply run の開始や Codex による適用 loop を追いたいときは `fork.py` を読む
- apply run の join / merge / report / cleanup を追いたいときは `join.py` を読む
- apply fork の report 生成や変更要約の組み立てだけを確認したいときは `fork_report.py` を読む

## hash
- ed4541038815a7b31a15ede89718b5265b90bafa582eafd08a0fbd8f01153294

# `fork.py`

## Summary
- `apply fork` の起点から完了までの制御を読むための入口。branch/worktree の作成、対象ファイルの列挙、Codex による所見適用、commit、state 更新、異常時の復旧までを一つの実行単位として扱う。
- 中断時の部分完了や error 退避、process tracking、cleanup 条件を確認したいときにここを読む。所見の生成方法や適用方法の詳細は、参照先の専用ファイルを読む。

## Read this when
- `apply fork` の実行フロー全体を追いたいとき。
- 新しい apply run の開始条件、既存 branch/worktree の衝突、失敗時の rollback ルールを確認したいとき。
- 中断・エラー時に何を残し、何を破棄するかを確認したいとき。

## Do not read this when
- 所見の列挙ロジックだけを知りたいときは、対象列挙や finding 生成の専用ファイルを先に読む。
- レポートの出力形式だけを知りたいときは、report 生成の専用ファイルを読む。
- `apply fork` 以外の subcommand 全体像を見たいだけなら、このファイルではなく上位のルーティング文書を読む。

## hash
- ed8e733e8a08085ee6ae2b5fdbef106e8dc00cffb5204b181028af4b6e3b1c86

# `fork_report.py`

## Summary
- `apply/fork` の実行結果レポート生成に関わる入口。成功・失敗・中断のレポート本文、所見数の推移、変更要約、未追跡ファイルの差分扱いを確認したいときに読む。
- `git diff` と未追跡ファイルから変更要約を作る部分を扱う。差分の対象範囲、変更なし判定、要約生成失敗時の代替表現を調整したいときに読む。
- YAML frontmatter を含む Markdown レポートの組み立てを扱う。出力文面、結果ラベルの文言、所見数メモ、変更一覧の表現を確認したいときに読む。

## Read this when
- apply fork の完了報告や失敗報告の出力形式を変えたい。
- 所見数の履歴や中断時メモをレポートにどう出すかを確認したい。
- fork 以後の変更差分に未追跡ファイルを含めるか、変更要約のフォールバックをどうするかを確認したい。

## Do not read this when
- 実際の apply fork 実行フローや session 状態の更新を追いたい場合は、より上位の apply fork 実行処理を読む。
- 差分収集の個別コマンドや git 操作の共通部を追いたい場合は、`run_git` を使う共通ユーティリティ側を読む。
- レポート保存先のディレクトリ規則だけを知りたい場合は、このファイルではなく `reports_dir` 側を読む。

## hash
- 6f9fb260196190ef01b337f148c812744075453fb920d0b1654b6c97b947c133

# `join.py`

## Summary
- apply session の join 実行を扱う。差分検査、merge、report 保存、apply worktree と branch の後始末までを一連で見る必要があるときに読む。

## Read this when
- `apply join` の CLI 実行フロー、事前条件、merge conflict や想定外差分の扱いを確認したいとき。
- apply state の更新、report の生成、worktree / branch の cleanup 条件を確認したいとき。
- `--force-resolve` の有無で join の挙動がどう分かれるかを追いたいとき。

## Do not read this when
- `apply fork` や `apply abandon` の処理を見たいときは、それぞれのサブコマンド実装を読む。
- report の文面だけを見たいときは、report 専用の実装を読む。
- apply/session の共通 state 操作や worktree 操作だけを追いたいときは、個別の runtime helper を先に読む。

## hash
- 7b6a7efccd106ed55d49f845886882c2821395da91bb7d8ed79daf0a3988f542
