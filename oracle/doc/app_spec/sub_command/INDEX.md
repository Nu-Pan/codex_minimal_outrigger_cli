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
- 編集 run の共通 lifecycle 仕様を定義する正本。realization apply/refactor fork から run join/abandon までの対象範囲、同時実行境界、fork・join・abandon の事前条件と状態遷移、差分検査、merge、cleanup、report および terminal result の共通要件を扱う。workload 固有の編集 run lifecycle や関連する実装・仕様の整合性を確認するときの入口となる。

## Read this when
- realization apply または realization refactor の編集 run を fork、join、abandon する挙動を定義・実装・レビューするとき
- 編集 run の状態管理、想定内差分、merge conflict、cleanup、report、terminal result の共通規則を確認するとき
- workload 固有仕様に共通する run lifecycle の境界や、session lifecycle との違いを確認するとき

## Do not read this when
- cmoc session join/abandon だけの lifecycle を扱うとき
- cmoc oracle edit、read-only investigation/review、cmoc 自身による機械的更新、session join の conflict 解消だけを扱うとき
- 共通 lifecycle ではなく、realization apply/refactor 固有の編集責務や join 後処理だけを確認するとき

## hash
- 9362e08fbecfa6e1a5804deb043e14cc86c04d9849a2e8c7f77207b44075b568

# `feedback_report.md`

## Summary
- `cmoc feedback report` の仕様書。pending observation と直前の active state を report cut に固定し、candidate の検証結果に応じて正常な active generation・Markdown report、または `incomplete` 診断 report を publication する責務を定義する。
- CLI の引数・副作用、事前条件、report cut、validation・deduplication・集約・候補形成、normalization と verification agent の境界、output 受理条件、正常 publication、`incomplete`、中断・再開、cleanup、保存形式、終了コードを扱う。feedback report サブコマンドの実装・テスト・仕様適合性を確認する際の入口であり、raw observation や state の詳細は参照先の正本仕様へ案内する。

## Read this when
- `cmoc feedback report` の CLI 契約、publication 条件、候補検証、agent 呼び出し境界を実装または変更するとき。
- feedback report の正常結果、`incomplete` 診断、active state、report cut、再開・中断、cleanup、終了コードの挙動を確認するとき。
- feedback report に関するテスト要件や仕様適合性を調査するとき。

## Do not read this when
- raw observation の schema や記録方法だけを確認する場合は、feedback observation の正本仕様を直接読む。
- state、checkpoint、publication、cleanup の永続化規則だけを確認する場合は、feedback state の正本仕様を直接読む。
- normalization または verification agent の正確な prompt、起動パラメータ、Structured Output schema を確認する場合は、対応する oracle の実装・schema を直接読む。
- サブコマンド共通の中断動作だけを確認する場合は、subcommand interruption の正本仕様を直接読む。

## hash
- 7485894160bf4111749af728074e0e5cc71f5fc573ce481d9eba3efc8c4d1ef7

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
- oracle file を編集する `cmoc oracle edit` サブコマンドの正本仕様。目的、ユーザー指示の入力経路、起動前条件、TUI 起動パラメータ、実行順序、編集境界、終了時の差分保持、中断・排他制御、ログ方針を定める。サブコマンドの実装や関連するプロンプト生成・doctor・indexing・Codex CLI 連携の入口となる。

## Read this when
- `cmoc oracle edit` の挙動、引数、実行順序、終了条件を確認するとき
- oracle file を編集する TUI の起動条件、起動パラメータ、編集権限を実装・変更するとき
- TUI 終了後の未コミット差分、indexing、branch・worktree・session state の扱いを確認するとき
- oracle edit 固有の中断、排他制御、ログ、feedback の責務を確認するとき

## Do not read this when
- realization file の通常編集や `cmoc oracle investigation` の権限を確認するとき
- プロンプト入力形式そのものの詳細を確認するときは、指定された prompt editor input の正本を直接読む
- doctor preprocess、indexing、Windows toast、Codex CLI 実行規則など個別機能の詳細仕様を確認するときは、各機能の正本を直接読む

## hash
- 64ed9944a0db51b73cf6716d01dd3e193b2c90164720a96215c4c019855e98e2

# `oracle_investigation.md`

## Summary
- エディタから受け取った oracle file 調査指示を完全プロンプトへ組み込み、Codex CLI の TUI を起動するサブコマンドの仕様を扱う。oracle file の調査フロー、入力編集、起動パラメータ、調査結果と変更の扱いを確認するための入口である。

## Read this when
- oracle file を根拠に調査するサブコマンドの挙動や実行手順を確認するとき
- エディタ入力から調査用 TUI 起動までのプロンプト構築契約を確認するとき
- oracle file と realization file の読み書き制約、調査結果の扱いを確認するとき

## Do not read this when
- oracle file の内容そのものを調査するとき
- プロンプト編集機構や起動パラメータの実装詳細を直接確認するとき
- oracle file の調査を伴わない別のサブコマンドの仕様を確認するとき

## hash
- f4c19cf7e8fd5019ff0f12a59f12ad199d8a530c21c62b66bc7b933c17c7b257

# `oracle_review.md`

## Summary
- `cmoc oracle review` サブコマンドの正本仕様。oracle のレビュー範囲、前提条件、隔離実行、所見の列挙・統合・検証・採否判定、レポート生成、責務境界を定義する。
- oracle review の実装や挙動仕様、レビュー所見の成立条件、スコープ・中断・レポート形式を確認する際の入口となる。

## Read this when
- `cmoc oracle review` の引数、事前条件、実行手順、agent call の責務を変更または確認するとき
- oracle review の finding 判定基準、ループ上限、所見 ID 管理、ユーザー中断時の扱いを確認するとき
- oracle review レポートの保存先、frontmatter、本文セクション、verdict の意味を確認するとき
- oracle review の責務境界や、oracle file・実装・自動生成ファイルの扱いを確認するとき

## Do not read this when
- oracle 全般の判断基準だけを確認したい場合は、misc_spec.md の該当節を直接読むとよい
- run の隔離実行の詳細だけを確認したい場合は、run_isolation.md を直接読むとよい
- サブコマンド中断の共通動作だけを確認したい場合は、subcommand_interruption.md を直接読むとよい
- oracle review 以外のサブコマンドの仕様や、実装コードそのものを確認する場合

## hash
- eeb34c78afab9a7043f5241a10552fdb3d9631c7534a4481dd2812db3b124034

# `realization_apply.md`

## Summary
- realization apply fork の目的、追従対象となる oracle 差分、agent call と realization file の変更範囲、fork の実行手順、エラー処理、report、join 後 hook を定める正本仕様。apply fork の実装や lifecycle、差分追従、終了状態、reporting の挙動を確認する際の入口となる。

## Read this when
- realization apply fork の引数・差分範囲・agent call 制約を確認するとき
- fork の実行手順、変更可能なファイル、commit と run state の扱いを確認するとき
- fork report の必須項目や join 後の session 更新を確認するとき

## Do not read this when
- fork・join・abandon に共通する lifecycle の詳細だけを確認したいときは editing run の正本を読む
- oracle file に対する realization file の適合性基準だけを確認したいときは misc spec の該当節を読む
- feedback の共通収集規則だけを確認したいときは feedback spec を読む

## hash
- b3adf5b647db7850c4e49ce5213fce18646d66ea6e57ce4bce3cf9aa2424fabf

# `realization_refactor.md`

## Summary
- oracle file と realization file を起点に、realization の適合性をファイル単位で調査・修正し、調査要求がなくなるまで反復する realization refactor fork workload の仕様を定義する。
- refactor state の schema と entry 同期、current fork の unresolved target、調査対象の選択順、agent call 後の changed_paths 検証、state 更新、commit、完了判定を扱う。
- fork の中断・エラー時の整合性、run state、report、終了コード、および join 後の共通 lifecycle との境界を確認する際の入口である。

## Read this when
- realization refactor fork の処理順、調査対象選択、処理単位、所見の正規化、変更 path 検証を確認するとき
- refactor state の保存形式、同期条件、investigation_required や last_investigation_result の更新規則を確認するとき
- unresolved target を含む fork の完了条件、user interruption、その他のエラー、fork report の内容を確認するとき

## Do not read this when
- 短い変更ループを担う realization apply の仕様だけを確認するとき
- fork・join・abandon の共通 lifecycle を確認するときは editing_run.md を直接読む
- oracle file と realization file の適合性判定基準を確認するときは misc_spec.md を直接読む
- 中断処理の共通動作だけを確認するときは subcommand_interruption.md を直接読む

## hash
- 03695d65a161518eee09425cc6f8d44c02626589a19a08e50f1d93d2dde42346

# `session_abandon.md`

## Summary
- 現在の session branch を home branch に merge せず破棄する、cmoc 管理下の session 終了コマンド。session join や join 済み結果の rollback とは異なり、session branch 上の commit・oracle 改訂・実装修正を破棄する。

## Read this when
- session を merge せず終了し、session branch とその固有成果物を破棄する処理を実装・レビューするとき
- abandon の実行条件、doctor preprocess から cleanup・状態更新・branch 削除までの手順、正常終了後の session.state を確認するとき
- cleanup 失敗時のロールバックと再実行要求、session join および cmoc run abandon との責務境界を確認するとき

## Do not read this when
- session の成果物を home branch に取り込む処理を確認するとき
- 未 join の編集 run の破棄処理だけを確認するとき
- join 済み session の結果を取り消す rollback 処理を確認するとき

## hash
- cf6cd74694fa8d83f5a5b8df964228e01ea3dc801b7bcf919757ce8f7875f9a3

# `session_fork.md`

## Summary
- 対象は、現在のローカルブランチを分岐元として cmoc 管理下の session ブランチを作成し、session 情報を初期状態付きで保存する `cmoc session fork` の挙動仕様である。session fork の引数・実行前提・ブランチ命名、実行手順、任意の start point を許さない規則、session の一意性を確認・変更するときの入口になる。

## Read this when
- `cmoc session fork` の CLI 挙動、引数、事前条件、エラー条件、ブランチ作成または session 状態保存の仕様を確認するとき
- session の分岐元・merge 先や active session branch の一意性を扱う実装・テスト・仕様を確認するとき

## Do not read this when
- session fork 以外の session サブコマンドの挙動だけを確認するとき
- session fork の詳細仕様ではなく、一般的な git branch 操作や repository default branch の仕様を確認するとき

## hash
- 7c72e3ad559542deb8a2397250d46b1b21d8bb6f4d15154ea543225bec16b085

# `session_join.md`

## Summary
- `cmoc session join` の正本仕様。セッション作業ブランチをホームブランチへマージし、状態更新と安全な後始末を行うコマンドの責務・引数・事前条件・実行手順を定義する。通常の汎用 git merge や repository-local feedback state の統合仕様ではない。
- マージ競合時の conflict marker 解消手順、oracle file の扱い、両ブランチの意図を保持する優先順位、想定外エラー時の停止条件とブランチ削除条件を確認するための入口。

## Read this when
- `cmoc session join` の実装、テスト、CLI 挙動、事前検証、セッション状態遷移を変更または確認するとき。
- session join における merge conflict 解消、oracle file の編集範囲、feedback state との境界、セッションブランチ削除の安全条件を判断するとき。

## Do not read this when
- 通常の git branch 間 merge wrapper の仕様を確認したいとき。
- session の作成・実行・離脱など、join 固有のマージ処理や状態更新を扱わない別サブコマンドの仕様を確認するとき。
- repository-local feedback state の生成・集約・レポート自体を確認するとき。

## hash
- ea5ba2b9a3e98d25a0f3b21c2ebd8ed345627f6a535bf2c2003bdc7c14920147

# `tui.md`

## Summary
- `cmoc tui` サブコマンドの正本仕様。ユーザープロンプトへの固定規範・契約の注入、エディタによる完全プロンプト確定、固定パラメータでの AI Agent CLI/TUI 起動手順を定義する。共通バックエンド規則と Codex CLI 固有の起動条件の入口となる。

## Read this when
- `cmoc tui` の引数、事前条件、実行手順、プロンプト編集フローを確認するとき
- AI Agent CLI/TUI に注入される cmoc 固有規範、モデル設定、ファイルアクセス、Structured Output、indexing・feedback・通知の起動条件を確認するとき
- Codex CLI バックエンドの起動コマンド、環境変数、preflight、引数による設定上書きを確認するとき

## Do not read this when
- プロンプト編集の詳細仕様だけを確認したい場合は、本文から参照される prompt editor input の正本を直接読むとき
- oracle file と realization file の一般的な責務や oracle review の成立条件だけを確認したい場合は、本文から参照される各正本仕様を直接読むとき
- `cmoc tui` 以外のサブコマンドや、builder 内部の実装詳細だけを調べるとき

## hash
- 7b3ddf391d97c35b5ed27eccedce59e66d13e19dc5255a905172ae2bb898c6b3
