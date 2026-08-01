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
- `cmoc oracle edit` サブコマンドの正本仕様。oracle file の編集指示を受け取り、事前検査後に main worktree 上の Codex CLI TUI を起動し、oracle file の未コミット変更を人間の確認対象として残す。
- 引数、エディタ入力、TUI 起動パラメータ、実行順序、編集禁止範囲、終了時の差分維持、中断・排他制御、ログ方針を定義する。oracle edit の実装・テストや関連する app specification を確認する入口。

## Read this when
- `cmoc oracle edit` の挙動、起動前提条件、TUI パラメータ、編集境界を変更・調査するとき
- oracle file の編集指示入力、事前検査、終了後の差分・indexing の扱いを確認するとき
- oracle edit サブコマンドのテストや関連 builder・prompt editor input の仕様を確認するとき

## Do not read this when
- realization file の具体的な実装配置や Python 実行環境だけを確認したいときは、対応する realization code または開発環境の oracle file を直接読む
- `cmoc oracle investigation` の権限やライフサイクルを確認したいときは、この oracle edit 仕様ではなく investigation の仕様を読む
- INDEX.md の生成・更新方法そのものを確認したいときは、indexing 関連の正本仕様を直接読む

## hash
- d6ab16734df840a9438e85810a2503cbf531d6e34ed7870616e5dc422c39ef41

# `oracle_investigation.md`

## Summary
- oracle file に関するユーザーの調査指示を受け取り、doctor preprocess 後に Codex CLI の TUI を起動するサブコマンドの仕様を定義する。入力編集、TUI 起動パラメータ、Codex CLI 起動条件、調査結果の扱いと変更禁止事項を扱う。関連する oracle investigation の実装・起動条件を確認する入口となる。

## Read this when
- oracle file の調査用サブコマンドの挙動を確認・変更するとき
- エディタ入力から Codex CLI TUI 起動までの処理を追うとき
- oracle file を読み取り専用、realization file を読み書き禁止として扱う調査フローを確認するとき

## Do not read this when
- Codex CLI TUI の一般的な起動パラメータの正本を確認したいときは、指定された launch_tui の oracle src を直接読む
- エディタ入力仕様だけを確認したいときは、prompt_editor_input の oracle doc を直接読む
- Codex CLI の環境変数・preflight validation・引数上書き規則だけを確認したいときは、codex_exec_rule の oracle doc を直接読む

## hash
- e40e4e04abc6a8d526f4e566449aaa858bd29ffd1f40ffc74d8eae79f34101da

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
- `cmoc realization apply fork` の目的、追従対象となる oracle 差分、agent call の実行制約、実行手順、エラー処理、report、join 後 hook を定義する正本仕様。realization apply の fork 処理や編集 run の lifecycle、差分適用と結果報告の実装入口となる。

## Read this when
- realization apply fork の差分始点・終点、oracle file の rename を含む追従範囲を確認するとき
- 本命 agent call の実行回数、cwd、file access mode、変更対象を確認するとき
- fork の実行手順、エラー時の state、report 内容・保存先、join 後 hook を実装または検証するとき

## Do not read this when
- fork・join・abandon に共通する lifecycle だけを確認したいときは、指定された共通 lifecycle の正本を直接読む
- realization file の具体的な実装やテストの詳細を調べるとき
- ファイル単位の網羅的な realization 追従や refactor の仕様を調べるとき

## hash
- a98e7be894f3092fa4bc7493d0d87c9f5db19691675509f7283ed3912e48c1b0

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
- cmoc tui サブコマンドの正本仕様。ユーザー入力と自動生成プロンプトを組み合わせ、パラメータ解決後に AI Agent CLI/TUI を起動する実行手順、プロンプト編集、TUI 起動、および Codex CLI 固有の設定引き継ぎを扱う。

## Read this when
- cmoc tui の実行手順、引数・事前条件、プロンプト編集入力の仕様を確認するとき
- agent call による起動パラメータ決定や、AI Agent CLI/TUI の起動条件を変更・検証するとき
- Codex CLI 起動時の CODEX_HOME、preflight validation、CLI 引数による設定上書きを確認するとき

## Do not read this when
- doctor preprocess 単体の仕様を確認するときは、doctor 関連の正本仕様を直接読む
- エディタ入力の詳細仕様だけを確認するときは、prompt_editor_input.md を直接読む
- Codex exec の共通仕様だけを確認するときは、codex_exec_rule.md を直接読む

## hash
- df5b0d7b743e52f741c020b0532fcb5eff5bb9e1f1e49e6db5a3f9bcd397d2f3
