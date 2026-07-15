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
- `cmoc apply abandon` の実行本体を扱う。apply run を破棄して apply state を ready に戻す流れと、その途中で必要になる branch/worktree/process cleanup の入口になる。
- この対象は、apply run の破棄条件の判定、cleanup 対象の特定、実行中 process の停止、apply branch と worktree の削除、状態更新、結果表示をまとめて扱う。

## Read this when
- `cmoc apply abandon` のルーティング先を決めたいとき。
- apply run を破棄する条件、どの branch から実行できるか、どの状態を ready に戻すかを確認したいとき。
- apply branch / worktree / process の cleanup 手順の入口を探しているとき。

## Do not read this when
- session state の作成や更新の定義だけを確認したいときは、apply abandon ではなく session state 側の対象を読む。
- branch や worktree の一般的な操作仕様だけを見たいときは、より基礎の runtime や branch/worktree 操作側を読む。
- CLI 全体のサブコマンド一覧や共通実行基盤だけを見たいときは、この対象ではなく上位の CLI ルーティングや共通実行基盤を読む。

## hash
- 723d1243b709cbcaa1f10f9dd9aa8ba241e6e0e279a10a629fb90689617f7523

# `fork.py`

## Summary
- apply fork の実行開始から、対象ファイルの列挙、Codex による所見適用、commit、state/report の確定、異常終了時の巻き戻しまでをまとめる入口。apply run のライフサイクル全体や中断・復旧条件を追うときに読む。

## Read this when
- apply fork の実行フロー、対象選定、findings の適用、commit 生成、完了報告の流れを確認したい。
- 中断時の部分結果確定、child process 停止、未確定差分破棄、初期化失敗時の rollback など、apply run の失敗時挙動を確認したい。
- apply ループでどの file を再調査対象に戻すか、また commit subject をどう決めるかを確認したい。

## Do not read this when
- apply fork ではなく、別 subcommand の CLI 入口や別の orchestration を追いたい。
- apply 内で使う個別の parameter 生成や report 生成の詳細だけを見たい場合は、対応する下位モジュールを直接読む。
- oracle file や INDEX.md の書き方そのものを確認したい場合は、このファイルではなく該当する仕様文書を読む。

## hash
- fec4b9113a8a152e65be5b864536a3a044132984da015a14d02f59f5c134abf0

# `fork_report.py`

## Summary
- `cmoc apply fork` の実行結果レポートを組み立てる対象。成功・未収束・エラーの本文、所見数の推移、変更内容要約、YAML frontmatter 付き Markdown 出力を確認したいときの入口。
- fork 実行の本体ではなく、変更差分の収集結果をどの文面で保存するかを扱う。変更要約のフォールバック、未追跡ファイルの差分扱い、中断時の注記を確認したいときに読む。

## Read this when
- `apply fork` の保存レポートの見た目や文言を変えたいとき。
- 所見数の履歴や中断メモをレポートにどう残すかを確認したいとき。
- fork 以後の変更差分をレポートへどう反映するか、要約生成失敗時に何を出すかを確認したいとき。

## Do not read this when
- `apply fork` の実行フロー、branch/worktree 作成、state 更新、commit などの制御を追いたいときは本体側を読む。
- 差分収集に使う git 操作の共通部だけを確認したいときは、`run_git` や関連ユーティリティ側を読む。
- `apply join` や `apply abandon` のレポートではなく、fork 専用の出力だけを見たいときはこの対象に限る。

## hash
- 832f69581c8b3e36aba2a138b729c17b20c85c3fe638ba8e5e9fb6641b0d363c

# `join.py`

## Summary
- `apply join` の実行本体を読む入口。差分検査、merge、report 保存、force-resolve、後始末までをまとめて確認したいときに進む。
- この対象を読むのは、apply/session state と worktree・branch の整合性、想定外差分の扱い、cleanup の条件を追いたい場合。

## Read this when
- apply join の正常終了条件や失敗条件を確認したい。
- force-resolve 時に何を revert し、何を残すかを確認したい。
- merge conflict や report 生成、apply worktree と branch の削除条件を追いたい。

## Do not read this when
- apply join 以外の apply サブコマンドを追いたい。
- managed branch 一般の差分列挙や rename 扱いだけを確認したい場合は、対応する共通処理を先に読む。
- report だけ、あるいは conflict 解消だけを確認したい場合は、この対象より該当する個別処理を直接読む。

## hash
- de1aa378a9a1f623bbfe00473a289e710e8799fed4b4ed0c12a09fdc521242f1
