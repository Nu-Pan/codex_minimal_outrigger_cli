# `apply_abandon.md`

## Summary
- `cmoc apply abandon` の正本仕様断片。未 join の apply run を破棄し、`{{cmoc-apply-branch}}` と `{{cmoc-apply-worktree}}` の cleanup、`{{cmoc-session-state-file}}` の `apply.state` を `ready` へ戻す処理を扱う。
- `cmoc apply fork` で作られた apply 成果物を取り消したいとき、または session を破棄する前に active / completed / error の apply run を先に片付けたいときに読む。
- `cmoc apply join` のような merge ではなく破棄を行う場面、`cmoc session abandon` の前提となる apply 側 cleanup を実装・確認したい場面で読む。

## Read this when
- 現在の session に紐づく未 join の apply run を破棄する挙動を実装・確認するとき。
- `{{cmoc-apply-branch}}` や `{{cmoc-apply-worktree}}` を削除する正規手順と、その前提条件・警告・終了コードを確認したいとき。
- `cmoc apply fork` の結果を取り消したいが、`cmoc apply join` は行わず、session 本体は維持したいとき。
- `cmoc session abandon` 実行前に、残っている apply run を先に片付ける必要があるかを確認したいとき。

## Do not read this when
- apply 成果物を `{{cmoc-session-branch}}` に取り込む処理を知りたいときは、`cmoc apply join` を読む。
- session 自体を破棄したいときは、`cmoc session abandon` を読む。
- apply の実行や探索、差分反映のループを知りたいときは、`cmoc apply fork` を読む。
- report 保存や merge 後のブランチ削除など、join 側の後処理を知りたいときは、この対象ではなく `cmoc apply join` を読む。

## hash
- 5b0680f4bce466a631f035f15800d028b8a60a4a1da5f0aa3f16bc9bbd349289

# `apply_fork.md`

## Summary
- `cmoc apply fork` の実行条件、状態遷移、調査待ちファイルの初期化、所見調査と修正依頼のループ、レポート生成までを扱う入口。apply ループ全体の責務と、`run` 隔離実行や各 agent call 正本へのつなぎ先を確認したいときに読む。

## Read this when
- `cmoc apply fork` の引数、事前条件、終了コード、作業レポート形式を確認したいとき。
- apply ループの流れ、`apply.state` の更新条件、ユーザー中断時の扱いを確認したいとき。
- 調査待ちファイルリストの初期化基準や、所見調査・修正反映の起点となる正本を確認したいとき。

## Do not read this when
- `run` の隔離実行そのものの詳細だけを知りたいときは、`app_specs/run_isolation.md` を直接読む。
- `build_apply_fork_file_finding_enumeration_parameter` や `build_apply_fork_finding_application_parameter` の個別仕様だけを知りたいときは、それぞれの正本を直接読む。
- `cmoc apply fork` 以外のサブコマンドの責務やレポート仕様を探しているとき。

## hash
- 4fb82f5d1608b87bb80d4e9c2f02a6fd80e58cedb24805da8d8fe4fc40117f54

# `apply_join.md`

## Summary
- `cmoc apply join` の実行条件と分岐を確認したいときに読む。apply の成果物を session 本流へマージする責務があり、通常モードと強制モード、`apply.state = error`、ユーザー中断済み apply、merge conflict、使用済み branch/worktree の削除条件を扱うため、実行時の制御と失敗時挙動を実装・修正するときの入口になる。

## Read this when
- `cmoc apply join` の引数、事前条件、モード分岐、マージ時の conflict 扱い、state 更新、branch/worktree 削除条件を確認したいとき。
- apply 実行後に session 側へ結果を取り込む処理や、想定外の差分を通常モードで止めるか強制モードで revert するかを判断したいとき。

## Do not read this when
- apply の実行本体や fork 側の処理を調べたいときは、そちらの対象を読む。
- session/state file の保存形式そのものだけを確認したいときは、より直接その state 定義を扱う対象を読む。

## hash
- 2257bce933ed9cf50c749288ed9bf496ef760adf394c22ae37af3690928cf675

# `doctor.md`

## Summary
- `cmoc doctor` の役割は、リポジトリが `cmoc` を正常実行できる状態かを検証し、必要なら修復を試みることにある。中身は doctor preprocess を明示的に呼ぶための入口なので、このコマンドの振る舞いを実装・変更するときに読む。

## Read this when
- `cmoc doctor` の実行開始条件や、doctor preprocess への委譲方法を確認したいとき。
- `cmoc` の環境診断と修復の入口として、このコマンドが何を保証すべきかを把握したいとき。

## Do not read this when
- doctor preprocess の内部処理だけを変えたいときは、まずその処理側の定義を読む。
- 引数設計や追加オプションの検討ではなく、単に `cmoc doctor` の入力なし実行を前提にしたいだけのとき。

## hash
- 8354ebcd7f732dcf70eb06ee6ed33abe6093b06e6effe5dcf1084dc3dce1f39c

# `indexing.md`

## Summary
- `cmoc indexing` のサブコマンド入口として、作業ツリー全体に対するインデクシングの実行条件と、その結果を自動コミットする責務を持つ。
- この文書は、引数なしで実行されること、実行前に未コミット差分がある場合は失敗すること、そして `doctor preprocess` の後にインデクシングと git commit を行う必要があることを確認したいときに読む。
- インデクシングの意味そのものは別の正本仕様に委ねられているため、この文書はサブコマンドの手順と事前条件の確認に絞る。

## Read this when
- `cmoc indexing` の実行可否や前提条件を確認したいとき。
- このサブコマンドが何を順に呼び出し、どこで差分が確定してコミットされるかを確認したいとき。
- インデクシングの定義そのものではなく、サブコマンドとしての入出力や実行フローだけを知りたいとき。

## Do not read this when
- インデクシング処理の詳細仕様そのものを知りたいときは、参照先の正本仕様を読む。
- 引数設計や他サブコマンドとの比較を知りたいだけなら、ここではなくより上位のルーティング文書を読む。
- git commit の一般的な運用や doctor preprocess の内部動作を知りたいときは、この文書ではなく各処理の本体を読む。

## hash
- 00122849aac5fb7274dffd1fdeadb48c89c3dc735f7dfc6668c3a2fa8fe02b15

# `review_oracle.md`

## Summary
- `cmoc review oracle` は、`oracle` ツリー内の正本仕様を対象に、致命的または重要な所見を収集して人間へレポートするためのレビュー用サブコマンドです。
- この項目は、レビューの実行条件、隔離実行、所見リストの列挙・統合・検証・判定、そして Markdown レポート生成までを扱うときに読むべき入口です。
- 一方で、`cmoc` 自身の実装詳細や、レビュー対象ではない自動生成ファイル、別サブコマンドの仕様はここからは追いません。

## Read this when
- `oracle` 配下の仕様をレビューするサブコマンドの入出力、実行順序、停止条件を確認したいとき。
- レビュー対象の選定、所見の生成・統合・検証・採否判定、レポート保存の流れを把握したいとき。
- 中断時にどこまでを確定結果として扱うか、また最終レポートに何を含めるかを確認したいとき。

## Do not read this when
- `cmoc` の一般的な実行基盤や隔離実行の共通仕様だけを確認したいときは、`run isolation` や共通のサブコマンド中断仕様を先に読むべきです。
- `oracle` 以外の対象をレビューする場合は、この項目ではなく、その対象のサブコマンド仕様を読むべきです。
- `INDEX.md` の自動生成や他のルーティング情報だけを更新したい場合は、本文仕様ではなく該当階層の案内を直接扱うべきです。

## hash
- 759423a1c9aad0df869d39332f750e7eaed47b5e61ce02a0b94cc5944b041d66

# `session_abandon.md`

## Summary
- `cmoc session abandon` の実行条件、破棄してよい対象、失敗時の扱いを読むための入口。`session join` との差分や、`session` と `apply` の状態制約を確認したいときに読む。

## Read this when
- `cmoc session abandon` の引数、事前条件、終了時の状態遷移を確認したいとき。
- session を破棄する正規手段と、手作業でのブランチ削除や rollback との違いを確認したいとき。
- `session.state` と `apply.state` の整合条件、またはクリーンアップ中の失敗時に何をロールバックするかを確認したいとき。

## Do not read this when
- session を本流へ取り込む処理を知りたいときは、`cmoc session join` を読む。
- すでに `session join` 済みの結果を取り消す処理を探しているときは、この文書ではなく rollback 系の定義を探す。
- `apply run` の破棄だけを扱いたいときは、`cmoc apply abandon` を読む。

## hash
- 5baf43474a1dee9a372d6b19827f6b24f83b16d07d95d664fdd6812779d45bfe

# `session_fork.md`

## Summary
- `cmoc session fork` の実行条件、分岐元の決め方、session ブランチ命名、保存情報、legacy `cmoc branch`/`cmoc_...` を切り捨てる方針を確認したいときに読む。
- 現在 checkout 中の local branch を session の home branch として扱う点、未コミット差分や既存 active session がある場合のエラー、任意 start point を受け取らない点がこの対象の主眼。

## Read this when
- `cmoc session fork` の新規実装や挙動変更を確認したい。
- session fork がどの状態で実行可能か、どの branch 名を作るか、どこに session 情報を保存するかを知りたい。
- legacy の `cmoc branch` や `cmoc_{{time-stamp}}` 仕様を残す必要があるか判断したい。

## Do not read this when
- session 作成後の別サブコマンドの動作を知りたい場合は、そちらの仕様を読む。
- branch 管理の一般論だけを確認したい場合は、この対象ではなくより基礎的な branch/session 系の仕様を読む。
- すでに session が作成された後の apply/review/join の詳細を調べたい場合は、この対象は直接は不要。

## hash
- 40a2393b3f6ec060887750acb08460c93dd460ef65b087713059dcd1d2785dfd

# `session_join.md`

## Summary
- `cmoc session join` の実行条件と終了までの流れを知りたいときに読む。セッション完了時の merge 先、事前条件、コンフリクト時の扱い、完了後の後始末がこの文書の責務である。

## Read this when
- `cmoc session join` の入力なしコマンドとしての仕様、実行前の検証条件、merge 手順、コンフリクト解消の流れ、セッション終了時の状態更新やブランチ削除条件を確認したいとき。
- `cmoc session join` と旧名の `cmoc merge` の関係、あるいは `home branch` が session 作成後に進んでいた場合の扱いを確認したいとき。

## Do not read this when
- session 開始や状態取得など、`cmoc session join` 以外の session コマンドの仕様を知りたいとき。
- 一般的な git merge の使い方や汎用 merge wrapper の設計を知りたいとき。
- conflict marker 解消用 agent call の詳細そのものを知りたいときは、そちらの正本仕様断片を直接読むべきである。

## hash
- a6250333e1b9d484a7a7dd1a4da58cd32fd47c1462b561544fb274afb7277742

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの入口。ユーザー入力のオリジナルプロンプトをエディタで受け取り、必要な実行パラメータを agent call で決めて、AI Agent CLI/TUI を起動する処理を扱う。
- ここでは、プロンプト編集フロー、パラメータ決定、起動時の共通制約と Codex CLI 固有の持ち込み要件を確認する。

## Read this when
- `cmoc tui` の起動手順、エディタ入力、パラメータ決定、または起動コマンドの仕様を確認したいとき。
- Codex CLI をこのサブコマンド経由で起動するときの前提条件や、持ち込むべき実行制約を確認したいとき。
- オリジナルプロンプトの初期内容、保存先、読み出し時の整形ルールを確認したいとき。

## Do not read this when
- `cmoc tui` 以外のサブコマンドのルーティングだけを知りたいとき。
- `build_tui_resolve_parameter_parameter` や `build_tui_launch_tui_parameter` の個別仕様そのものを確認したいときは、そちらの正本を直接読むべきであり、この入口だけでは足りない。
- `skill_authoring_write` の具体的な書き込み仕様を知りたいときは、`tui` ではなく Skill 作成・保守側の文書を読むべきである。

## hash
- a5f93a2959ca250c7500f610a55c96fed5b6a1bbb7a61d650479bfbef96e8a7a
