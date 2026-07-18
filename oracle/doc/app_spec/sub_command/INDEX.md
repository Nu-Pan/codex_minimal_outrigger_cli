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

# `oracle_edit.md`

## Summary
- `cmoc oracle edit` の仕様を定義するサブコマンド文書。エディタで oracle file への指示を受け取り、指定のパラメータで Codex CLI の TUI を起動する流れ、入力コメント、起動条件、変更の扱いを確認する入口。

## Read this when
- `cmoc oracle edit` の実行手順や引数・事前条件を確認するとき
- oracle file 編集指示の入力方法や自動注入コメントを確認するとき
- Codex CLI TUI の起動方法、起動パラメータの扱い、変更の自動 commit 方針を確認するとき

## Do not read this when
- エディタ入力仕様の詳細だけを確認したいときは、指定された prompt editor input の正本を直接読む
- TUI 起動パラメータの詳細だけを確認したいときは、指定された launch_tui 実装を直接読む
- Codex CLI 共通の起動規則だけを確認したいときは、指定された codex exec rule を直接読む

## hash
- ebe20b04c9e643c0cb230260488286864dbcddbbbb96d7b220a42d11af72bd1c

# `oracle_investigation.md`

## Summary
- `cmoc oracle investigation` のサブコマンド仕様。エディタから oracle file に関する調査指示を受け取り、doctor preprocess と専用の起動パラメータ構築を経て Codex CLI の TUI で調査結果を回答する。入力コメント、TUI 起動、Codex CLI 設定、調査結果や変更禁止の扱いを定める。

## Read this when
- oracle file を根拠に調査する `cmoc oracle investigation` の動作、入力方法、Codex CLI TUI の起動条件を確認するとき。
- oracle investigation の起動パラメータ、Codex CLI の環境変数・preflight validation・設定上書き、または読み書き制約を変更・検証するとき。

## Do not read this when
- oracle file の具体的な仕様や規約そのものを調査する場合は、このサブコマンド仕様ではなく対象の oracle file を直接読む。
- エディタ入力の共通仕様を確認する場合は、指定された prompt editor input の正本を読む。
- TUI 起動パラメータの実装詳細を確認する場合は、専用 builder の正本実装を直接読む。

## hash
- f9ad127a8fbfb4aeef8eaed77a0ca6f796b897127149f964bccce3df7a2a292a

# `oracle_review.md`

## Summary
- `cmoc oracle review` の責務・引数・事前条件・実行手順を定義する正本仕様。oracle file のレビュー、所見の列挙・マージ・検証・判定、中断処理、Markdown レポート生成と保存条件を扱う。

## Read this when
- oracle review サブコマンドの挙動、スコープ、レビュー対象、所見ライフサイクルを確認するとき
- oracle file のレビュー処理や agent call の役割分担を変更・検証するとき
- レビュー結果の frontmatter、本文構成、判定値、保存先を確認するとき
- ユーザー中断時の部分結果の扱いを確認するとき

## Do not read this when
- oracle file 自体の内容をレビューするだけで、oracle review サブコマンドの仕様やレポート形式を確認する必要がないとき
- 実装ファイルを交えたレビューや Codex CLI の出力品質を検証するとき
- INDEX.md など cmoc が自動生成するファイルのレビュー方法を確認するとき
- レビュー結果を受けて次に何をするべきか判断するとき

## hash
- d495188324876e0e14dc178db85e923e257ebdf21571b61489cc0c609dd61d34

# `realization_apply.md`

## Summary
- `cmoc realization apply fork|join|abandon` の仕様を定義する oracle doc。oracle file の変更を realization file へ追従させる fork の差分範囲・実行手順・Codex CLI 呼び出し・エラー処理・report と、join/abandon の正本参照先を扱う。realization apply の各サブコマンド仕様を確認する入口。

## Read this when
- `cmoc realization apply fork` の差分追従、TUI 起動、作業範囲、終了処理、report または終了コードを変更・確認するとき。
- `cmoc realization apply join` または `abandon` の引数・事前条件・merge・状態更新・cleanup の正本参照先を確認するとき。

## Do not read this when
- ファイル単位の網羅的な realization 追従やリファクタリング方針を確認したいときは、`cmoc realization refactor` の仕様を直接読む。
- join または abandon の詳細手順を確認したいときは、共通仕様を定義する `oracle/doc/app_spec/sub_command/realization_run.md` を直接読む。

## hash
- a7c05415f89c6debdc0a5a62e490247414ac497e298fa1fcbe744dac70c1771f

# `realization_refactor.md`

## Summary
- realization file の oracle 追従調査を、未調査ファイルがなくなるまで反復する refactor workload の仕様を定める。fork の状態管理・調査ループ・中断・エラー・report と、join／abandon の責務および共通仕様への委譲を扱う。

## Read this when
- realization refactor の fork、join、abandon の挙動を実装・変更・検証するとき
- refactor state、run branch、worktree、agent call、commit、report のライフサイクルを確認するとき
- 中断・再開・エラー時の状態遷移や終了コードを確認するとき

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを扱うとき
- realization run 共通の fork／join／abandon 手順だけを確認する場合は、参照先の realization_run.md を直接読むとき
- 中断処理の共通仕様だけを確認する場合は、subcommand_interruption.md を直接読むとき

## hash
- b25af504cfca983d94759344080a6e77de03846daa8ba95a9f43413ee94c154d

# `realization_run.md`

## Summary
- realization run の共通仕様を定義する正本文書。apply/refactor run の fork・join・abandon における同時実行制約、事前条件、branch/worktree 管理、想定内外差分、merge conflict、cleanup、report の共通ルールを扱う。各 run の具体的な作業内容は個別仕様へ委ねる。

## Read this when
- realization apply または realization refactor の fork・join・abandon の共通挙動を実装・変更・レビューするとき
- run の状態管理、snapshot、branch、worktree、未コミット差分、join/abandon の cleanup 条件を確認するとき
- run の report、想定外差分、merge conflict、使用済み branch の削除ルールを確認するとき

## Do not read this when
- apply run 固有の作業内容や report file・終了コードを確認するときは realization_apply.md を読む
- refactor run 固有の作業内容を確認するときは realization_refactor.md を読む
- 共通仕様と無関係な realization 機能や通常の CLI サブコマンドを扱うとき

## hash
- db16530a6d3bff5509d5880aab7912afe8f8b7511144841588908be32868daaa

# `session_abandon.md`

## Summary
- `cmoc session abandon` の仕様を定義する文書。session branch を home branch に取り込まず破棄するための引数、事前条件、破棄対象、実行手順、状態遷移、失敗時の扱いを扱う。session の破棄処理や関連する realization abandon との責務境界を確認する入口。

## Read this when
- `cmoc session abandon` の実装・テスト・仕様確認を行うとき
- session の事前検証、branch・state file の更新と削除、cleanup 失敗時のロールバックを確認するとき
- `cmoc session fork` や `cmoc session join` との状態遷移上の関係を確認するとき

## Do not read this when
- session を本流へ取り込む `cmoc session join` の仕様だけを確認するとき
- 未 join の realization run を破棄する処理だけを確認するときは、対応する realization abandon の仕様を直接読む
- session の共通状態形式や doctor preprocess の一般仕様だけを確認するときは、対応する共通仕様を直接読む

## hash
- 41be2a31e1651afc34e1f03919c12bfb6aaab6790452ae4bbddfe3f68364d1e2

# `session_fork.md`

## Summary
- `cmoc session fork` の正本仕様。現在のローカルブランチを分岐元・merge 先として session 用ブランチを作成し、session 情報を保存して checkout する。引数、事前条件、実行手順、命名規則、旧仕様の非互換方針を扱う。

## Read this when
- `cmoc session fork` の実装、テスト、エラー条件、ブランチ命名、session 状態保存を変更または確認するとき。
- `cmoc session fork` とレガシーな `cmoc branch` や `cmoc_{{time-stamp}}` 形式との関係を確認するとき。

## Do not read this when
- session fork 以外のサブコマンドの仕様だけを調べるとき。
- 一般的な session 管理やブランチ操作を確認したいが、`cmoc session fork` の挙動を変更・検証しないとき。

## hash
- 284e843d98e0d94bd9ba52e82b57a3a629c76fff3fc03f5412bbb27dc2851551

# `session_join.md`

## Summary
- `cmoc session join` の正本仕様。セッションブランチの事前条件、ホームブランチへの merge、conflict 解消、状態更新、ブランチ削除、安全な失敗処理を定義する。session join の CLI 実装・テスト・エラー処理を確認する入口。

## Read this when
- `cmoc session join` の実装、引数、事前検証、merge 手順、conflict 解消、セッション状態更新を変更またはレビューするとき。
- `cmoc merge` の廃止や後方互換性方針を確認するとき。

## Do not read this when
- 通常の git merge wrapper や、session join 以外のサブコマンドを扱うとき。
- conflict 解消 agent call の詳細仕様だけを確認する場合は、`build_session_join_conflict_resolution_parameter` の正本を直接読む。

## hash
- 65937a8759844560b7335de8a09063f95a562c306eb0fff62388c9488b1cfd6e

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの正本仕様。ユーザー入力と自動生成プロンプトを組み合わせ、agent call で決定したパラメータに基づいて AI Agent CLI/TUI を起動する実行手順と、Codex CLI 固有の起動条件を扱う。

## Read this when
- `cmoc tui` の実行手順、引数・事前条件、プロンプト入力、agent call によるパラメータ決定を確認するとき
- AI Agent CLI/TUI の起動パラメータや、Codex CLI 起動時の環境変数・preflight validation・引数上書きを確認するとき

## Do not read this when
- プロンプトエディタ入力の詳細仕様だけを確認したいときは、指定された prompt editor input の正本を直接読む
- agent call によるパラメータ決定の詳細だけを確認したいときは、build_tui_resolve_parameter_parameter を直接読む
- 共通の TUI 起動パラメータだけを確認したいときは、build_tui_launch_tui_parameter を直接読む

## hash
- c0710e4864ebf312dd63aeef74d3d58b555e606cded00770dfa4125ec568ffed
