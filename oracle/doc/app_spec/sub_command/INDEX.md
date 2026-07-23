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

# `editing_run.md`

## Summary
- 編集 run を開始する workload 固有 fork と、`cmoc run join` / `cmoc run abandon` による終了 lifecycle の共通仕様を定義する正本文書。
- session 単位の同時実行制約、fork・join・abandon の事前条件、state 管理、差分検査、merge、cleanup、report 要件を扱う。
- 編集 run lifecycle の実装・レビューでは本書を入口として参照し、workload 固有仕様や session lifecycle の確認はそれぞれの正本文書へ進む。

## Read this when
- realization apply/refactor の fork、run join、run abandon の挙動を実装・変更・レビューするとき
- 編集 run の state、branch/worktree、想定内差分、merge conflict、cleanup、report 形式を確認するとき
- 複数の編集 run の同時実行境界や fork 共通処理を確認するとき

## Do not read this when
- `cmoc session join` や `cmoc session abandon` など外側の session lifecycle だけを扱うとき
- `cmoc oracle edit`、read-only investigation/review、cmoc の機械的更新だけを扱うとき
- workload 固有の編集内容や join 後 hook の詳細だけを確認するときは、対応する workload 固有仕様を直接読む

## hash
- 76969e326f23fb26b657950058ecd8d28206799f0c14986258f9627523c9a85e

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
- oracle file をユーザー指示に基づき Codex CLI TUI で直接編集する `cmoc oracle edit` サブコマンドの正本仕様。引数、入力注入、起動前提条件・パラメータ、実行順序、編集境界、終了後の差分維持、中断・排他制御、ログ方針を扱う。oracle edit の挙動や起動条件、oracle file 編集権限を確認する際の入口。

## Read this when
- `cmoc oracle edit` の実行フローや引数仕様を確認するとき
- oracle file 編集用 TUI の起動条件、builder パラメータ、file access mode を確認するとき
- TUI agent の編集対象・禁止操作、終了後の差分や indexing の扱いを確認するとき
- 中断、排他制御、並行編集、ログの仕様を確認するとき

## Do not read this when
- realization file の実装配置や CLI 責務境界を確認したいとき
- oracle file の調査専用サブコマンドの仕様を確認したいとき
- Codex CLI の一般的な起動規則だけを確認したいときは、参照されている共通規則を直接読む

## hash
- 13bdca10481604c07cf3bba64b6cb48c1533173e70d6841a7bf1a5b7207f967f

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
- `cmoc oracle review` サブコマンドの正本仕様。oracle ファイルのレビュー範囲、所見の列挙・統合・検証・判定、ユーザー中断時の扱い、Markdown レポート形式と保存先を定義する。oracle レビュー機能の実装や関連パラメータ仕様へ進むための入口。

## Read this when
- `cmoc oracle review` の引数、事前条件、実行手順、所見管理、ループ上限、中断処理を変更・確認するとき
- oracle レビュー結果の YAML frontmatter、本文セクション、所見分類、保存先を変更・確認するとき
- oracle review の実装で参照される agent call パラメータ仕様や run isolation の仕様を調査するとき

## Do not read this when
- INDEX.md など自動生成ファイル自体のレビュー対象や生成方法だけを確認するとき
- oracle review と無関係なサブコマンドの引数・実行手順・レポート形式を確認するとき
- 個別 agent call の詳細仕様だけを確認する場合は、本文中で参照される対応する parameter 定義を直接読むとき

## hash
- 586aa78654ae95846265f5e5d09bbceda171d80724f5ebcde510fd0d6fd05d8f

# `realization_apply.md`

## Summary
- realization apply fork の目的、追従対象となる oracle 差分、agent call の実行制約、実行手順、エラー処理、report と終了コード、join 後 hook を定義する仕様文書。realization apply の fork 処理を実装・検証・運用する際の入口となる。

## Read this when
- realization apply fork の挙動や lifecycle を変更・検証するとき
- oracle 差分の始点・終点、rename の扱い、agent call の制約を確認するとき
- fork report、終了状態、join 後の session 更新を扱うとき

## Do not read this when
- realization apply fork 以外の sub-command の仕様を確認するとき
- 共通する fork・join・abandon lifecycle の詳細だけを確認したいときは、指定された editing_run.md を直接読む
- ファイル単位の realization 追従や refactor の仕様を確認するとき

## hash
- c38be9c0824711d2152006094ff8f7291415ce015e3349c076ebb4442dabb90c

# `realization_refactor.md`

## Summary
- realization refactor fork の目的、refactor state の JSON schema と同期規則、current fork の unresolved target 管理、調査ループ、完了・中断・エラー時の lifecycle、report と終了 log の要件を定める oracle doc。realization refactor fork の実装や仕様確認における正本として、関連する下位実装・テストへの入口となる。

## Read this when
- realization refactor fork の挙動、state 管理、調査対象選択、unresolved target、完了条件を確認するとき
- fork の中断・エラー処理、report、終了コード、join 後の動作を変更または検証するとき

## Do not read this when
- realization refactor fork 以外の workload や共通 lifecycle の詳細だけを確認するときは、各 workload または共通 lifecycle の正本文書を直接読む
- 実装・テストの具体的な配置や開発環境の規則だけを確認するときは、対応する realization file や開発規則を直接読む

## hash
- 49ed124e4e4d48ea9baee1d3014cf98ad0b8240d7a3720d9b9a1474ed26853a8

# `session_abandon.md`

## Summary
- `cmoc session abandon` の仕様を定義する文書。session branch を home branch に統合せず破棄する際の引数、事前条件、破棄対象、実行手順、状態遷移、失敗時の扱いを扱う。session abandon の実装・テストや、session の破棄条件と状態管理を確認する入口となる。

## Read this when
- `cmoc session abandon` の挙動を実装・修正・レビューするとき
- session branch、session state、run state の事前検証やクリーンアップ処理を確認するとき
- session の abandon 後の状態遷移や失敗時ロールバックを確認するとき

## Do not read this when
- session の成果物を home branch に取り込む `cmoc session join` の仕様だけを確認するとき
- 未 join の編集 run を破棄する `cmoc run abandon` の詳細だけを確認するとき
- join 済み session の rollback や、session fork の詳細だけを確認するとき

## hash
- 2a06a246197e7eae75c325ccf2b7c6c10a5641b249900af9c7b143c770ea9e0d

# `session_fork.md`

## Summary
- `cmoc session fork` の正本仕様。現在のローカルブランチを分岐元兼マージ先として、セッション用ブランチを作成・checkoutし、session情報を保存してブランチ名を表示する。引数、事前条件、実行手順、ブランチ命名規則、start point制約、sessionの原則を扱う。

## Read this when
- `cmoc session fork` の挙動、引数、実行前エラー条件を確認するとき
- session branch の作成・命名・初期状態保存の実装やテストを変更するとき
- ローカルブランチ、managed branch、active session の扱いを確認するとき

## Do not read this when
- session fork 以外のサブコマンドの仕様だけを確認するとき
- 共通の doctor preprocess や session 状態形式の詳細を確認したいときは、それぞれの共通仕様・実装を直接読むとき

## hash
- e914f7872441d53ee60a6b5dd13d02a515e9a1159130098b798a0160a2f46a69

# `session_join.md`

## Summary
- `cmoc session join` の正本仕様。セッション用ブランチをホームブランチへマージしてセッションを完了するコマンドの、引数・事前条件・マージ手順・conflict 解消・状態更新・ブランチ削除条件を定める。

## Read this when
- `cmoc session join` の実装、テスト、エラー条件、ブランチマージ、セッション状態更新を変更または確認するとき。
- `git merge` の conflict 発生時に行う agent call や後始末の仕様を確認するとき。

## Do not read this when
- 通常の git branch 間 merge wrapper や、`cmoc session join` 以外の session サブコマンドを扱うとき。
- conflict 解消用 agent call の詳細仕様だけを確認する場合は、`build_session_join_conflict_resolution_parameter` の正本を直接読む。

## hash
- 6b979c851055d04a45abb56293b24dd00cc7b2fd997b8bcf7d0bd3fa6cc3871b

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの正本仕様。プロンプト入力、agent call による起動パラメータ決定、AI Agent CLI/TUI 起動までの手順と、Codex CLI 固有の起動条件を扱う。

## Read this when
- `cmoc tui` の実行手順、プロンプト入力、agent call のパラメータ決定、または AI Agent CLI/TUI の起動仕様を確認するとき。
- Codex CLI 起動時の `$CODEX_HOME`、preflight validation、CLI 引数による設定上書きの扱いを確認するとき。

## Do not read this when
- エディタ入力の詳細仕様だけを確認したい場合は、`prompt_editor_input.md` を直接読む。
- agent call で決定するパラメータの詳細だけを確認したい場合は、`build_tui_resolve_parameter_parameter` の正本を直接読む。
- TUI 起動パラメータの詳細だけを確認したい場合は、`build_tui_launch_tui_parameter` の正本を直接読む。

## hash
- be9faf25edcb1c5a094206c1ad538e66195cd6dcaef06552ae63ef8375d6229d
