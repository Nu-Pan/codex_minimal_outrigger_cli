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
- `cmoc apply fork` は、隔離された作業用ブランチ上で Codex CLI のファイル単位レビュー・修正・検証ループを実行し、実装と oracle の一致を目指すサブコマンド。スコープ選択、事前条件、状態遷移、割り込み、差分コミット、作業レポート、終了コードを定義する。apply の実行制御や結果報告の仕様を確認する入口であり、run 隔離や agent call の詳細仕様そのものではない。

## Read this when
- `cmoc apply fork` の引数、事前条件、apply ループ、スコープ、状態遷移、割り込み動作を実装・レビューするとき
- apply 実行時のブランチ差分、agent call の再投入条件、自動コミット、収束・未収束・エラー判定を確認するとき
- apply fork の作業レポート形式や終了コードを変更・検証するとき

## Do not read this when
- run の隔離実行の詳細だけを確認したいときは、指定された run isolation の正本を直接読む
- ファイル単位レビュー agent call のパラメータ詳細だけを確認したいときは、対応する parameter 仕様を直接読む
- apply fork 以外のサブコマンドの仕様や、個別の realization file の実装詳細を調査するとき

## hash
- fccbe3f974ac0a672cded52b2a56f4f5acb4382c99771769eb1e8c9fd3f53887

# `apply_join.md`

## Summary
- `cmoc apply fork` の成果物をセッション本流へマージするサブコマンドの仕様。事前条件、通常・強制モードの差分処理、状態更新、マージコンフリクト、使用済みブランチ削除までを定義する。

## Read this when
- `cmoc apply join` の挙動、実行条件、差分処理、マージ結果、ブランチ削除条件を実装・検証するとき。
- apply セッション状態や apply ブランチからセッション本流へのマージ処理を確認するとき。

## Do not read this when
- `cmoc apply fork` 自体の処理や、fork 側で積み上げる対象の詳細だけを確認したいとき。
- apply サブコマンド以外の CLI 仕様を調べるとき。

## hash
- 08610c8a3d7335b41a61385e3e26888bef9d618126e18fb072024f79b6f7d936

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

# `edit_oracle.md`

## Summary
- `cmoc oracle edit` サブコマンドの仕様を定義する。エディタから oracle file の最終状態に関する指示を受け取り、構築済みパラメータで Codex CLI の TUI を起動する処理、入力規則、起動条件、変更の扱いを扱う。

## Read this when
- `cmoc oracle edit` の実装・テスト・動作確認を行うとき
- oracle file の編集指示をエディタ入力から TUI 起動へ渡す流れを確認するとき
- Codex CLI 起動時の環境変数、preflight validation、設定上書きの扱いを確認するとき

## Do not read this when
- `cmoc tui` の一般的なオリジナルプロンプト入力仕様だけを確認したいときは、そちらの仕様を直接読む
- TUI 起動パラメータの prompt や agent call parameter の正本を確認したいときは、指定された `build_edit_oracle_launch_tui_parameter` の定義を直接読む
- oracle file の変更を自動 commit する処理を確認したいとき

## hash
- 0b4732a15b2cb3fe1d1dd348ef5e212788d22a0c6ae8c79f00e0d9fc6687c49a

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
- oracle ファイルの致命的問題をレビューし、所見を反復的に列挙・統合・検証・判定して Markdown レポートとして保存する `cmoc oracle review` の仕様を定義する。セッション／フルスコープ、隔離実行、中断処理、レポート形式と責務境界を扱う。

## Read this when
- oracle のレビュー機能、レビュー対象スコープ、所見の列挙・統合・検証・採否判定を変更または確認するとき
- レビューの中断時挙動、隔離実行、レポートの frontmatter や本文構成を確認するとき

## Do not read this when
- oracle 全般の開発環境・設計・テスト規則を確認したいとき
- 実装ファイルの詳細や自動生成 INDEX.md のレビュー仕様だけを確認したいとき

## hash
- 59cc50e955c6263a8d1bc382e2615a98bc61c2e6ee63950bfd33f4873e47784e

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
- `cmoc tui` サブコマンドの起動フロー、ユーザー入力プロンプトの編集先と初期テンプレート、agent call で決める起動パラメータ、Codex CLI 起動時に持ち込む固有要件を確認したいときに読む。
- この文書は、TUI 起動時の人間入力と自動決定の境界、エディタ選択順、入力読み出しの扱い、バックエンド共通の起動条件を決める役割を持つ。

## Read this when
- `cmoc tui` の起動手順、入力テンプレート、または起動パラメータの正本を確認したいとき。
- AI Agent CLI/TUI の起動条件や、Codex CLI を使う場合に追加で引き継ぐ要素を確認したいとき。
- ユーザーが入力するオリジナルプロンプトの編集場所、初期文面、読み出し時の整形規則を変更したいとき。

## Do not read this when
- TUI 以外のサブコマンドの仕様を知りたいときは、より直接の対象を読む。
- agent call の個別の解決仕様だけを知りたいときは、`build_tui_resolve_parameter_parameter` の正本を読む。
- 全バックエンド共通の launch パラメータだけを知りたいときは、`build_tui_launch_tui_parameter` の正本を読む。
- Codex CLI 固有の preflight validation や環境変数の正本だけを知りたいときは、`codex_exec_rule.md` を読む。

## hash
- b28837a3690a3d1a2fceae1388d903d29067e4a4990400dbf0a66ae1da2fa57b
