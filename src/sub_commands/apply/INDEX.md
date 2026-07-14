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
- `apply` 用の fork 実行をまとめる制御層で、session branch 上の事前条件確認から isolated apply worktree の作成、対象列挙、Codex による所見適用、commit、state/report 更新、異常時の rollback までを扱う。
- この領域は一つの apply run のライフサイクルを通して読むべきで、`file_finding_enumeration` と `finding_application` はそれぞれ対象列挙と所見適用の詳細を分担する下位入力として参照される。
- worktree・branch・process tracking・report の失敗復旧条件を共有しているため、fork orchestration を読むときの入口として使う。

## Read this when
- `apply fork` の実行フロー、state 遷移、report 出力、異常時 cleanup の仕様を確認したいとき。
- 対象ファイルの選定基準や、変更されたファイルを再度 apply 対象へ戻す条件を追いたいとき。
- commit subject の生成や、Codex 実行に渡す apply parameter の組み立て方を確認したいとき。

## Do not read this when
- 対象列挙の生成ロジックだけを知りたいなら `file_finding_enumeration` 側を先に読む。
- 所見をどう適用するかの詳細だけを知りたいなら `finding_application` 側を読む。
- `apply` 以外の subcommand の入出力や state 管理を確認したいだけなら、この orchestration 層ではなく該当 subcommand の実装を読む。

## hash
- 2894d6d1df64b7725b6e86d2266d27e1cde822a2a75c06108d3ec81720f08f21

# `fork_report.py`

## Summary
- apply fork の実行レポート生成と、そのための差分要約・未追跡ファイル反映・失敗時フォールバックをまとめて扱う入口。
- 所見数の推移と変更内容要約を Markdown + frontmatter 形式で出力する責務が中心で、個別の差分収集や要約生成の詳細は下位の helper に委ねる。

## Read this when
- apply fork の実行結果レポートの出力形式や、収束・未収束・エラー時の文言を確認したいとき。
- fork 以後の変更をどの範囲までレポートに含めるか、未追跡ファイルや差分要約の扱いを確認したいとき。
- 所見数の推移と変更 path の記録が、どの条件で機械的フォールバックに切り替わるかを確認したいとき。

## Do not read this when
- apply fork 自体の実行制御、所見列挙ループ、または状態遷移の本体を追いたいときは、より上位の apply fork 実行側を読むべきである。
- 差分要約の生成ロジックだけを見たいときは、change summary 生成側の helper を直接読むべきである。
- 一般的な report 保存先や timestamp 生成の共通処理だけを確認したいときは、このファイルではなく共通 runtime 側を読むべきである。

## hash
- cd0deb8268393baf1aa15c853982d874772bc1583c0cdc943016503324a5c836

# `join.py`

## Summary
- apply join の実行本体を扱う。事前条件確認、想定外差分の判定、force-resolve 時の巻き戻し、merge、state 更新、report 保存、worktree/branch 後始末までを一連の責務としてまとめている。
- apply join に関する結果レポートの生成や、想定外差分の分類・復元・merge conflict の機械解決もここにある。
- apply join の判定基準や許可差分の境界、関連する branch/state/worktree 操作を追いたいときに読む。

## Read this when
- apply join の実行フロー全体を変更したいとき。
- 想定外差分の検出・force-resolve・復元・報告のどこかを変えるとき。
- join 後の apply state 更新や worktree/branch 後始末の条件を確認したいとき。
- apply join で許可される差分の判定根拠を追いたいとき。

## Do not read this when
- apply join 以外の subcommand の入出力や CLI 定義だけを見たいとき。
- 共通の Git runtime や session/state の基盤動作だけを確認したいとき。
- INDEX.md の対象選定だけが目的で、join の処理内容までは不要なとき。

## hash
- 0b125a9eb20693e071104bd7e0dc836889e5b0aba338f57e6d068b248bd3bf91
