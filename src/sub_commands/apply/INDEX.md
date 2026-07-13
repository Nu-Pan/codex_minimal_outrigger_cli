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
- `apply fork` の 1 回分の実行制御をまとめる入口。session branch 上での前提確認、isolated worktree 作成、調査対象の列挙、Codex による所見適用、commit、state 更新、report 出力、異常時の復旧までを扱う。
- この層を読むべきなのは、`apply fork` 全体の流れ、失敗時の状態遷移、worktree / process 管理、結果レポートの責務境界を確認したいとき。
- 個別の対象列挙や finding 適用の詳細だけが知りたいなら、ここではなく同階層の専用実装に進む方がよい。

## Read this when
- `apply fork` の実行フロー全体を追いたいとき
- session branch の前提確認、apply state の更新、worktree 作成、commit / report / cleanup の関係を確認したいとき
- 異常終了時に何を残し、何を回収するかを見たいとき

## Do not read this when
- 調査対象の抽出ルールだけを知りたいときは、対象列挙の実装を読む
- finding の生成条件や Codex への渡し方だけを知りたいときは、finding 適用の実装を読む
- apply fork 以外の subcommand の仕様だけを確認したいときは、その subcommand の本文へ進む

## hash
- f612c9a2257c5967b05b136259bec9dfd7fb30e945b5ba32d4eb63737b5061d4

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
