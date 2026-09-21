# `apply`

## Summary
- 現在、apply サブコマンドの実装ファイルはありません。

## Read this when
- apply サブコマンドの実装が追加された後、その内容を確認するとき。

## Do not read this when
- apply 以外のサブコマンドを扱うとき。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `doctor.py`

## Summary
- `cmoc doctor` の CLI 入口を提供する。
- CLI runtime 経由で doctor preprocess を明示的に 1 ステップ実行する。
- 実行結果に現在の repo root を固有情報として返す。

## Read this when
- `cmoc doctor` のサブコマンド入口や、doctor preprocess の明示実行経路を確認するとき。
- doctor 実行時のステップ定義や terminal result に含まれる repo root 情報を確認するとき。

## Do not read this when
- doctor preprocess の具体的な処理内容や成果物を確認したいとき。
- CLI サブコマンド共通 runtime の実装や一般的な実行制御を確認したいとき。

## hash
- 1eb417245f2ab7964031bcace08e76c91beda19e6b7c26b38e163f2ec9977c3b

# `feedback`

## Summary
- feedback サブコマンドの実装群への入口。観測から候補生成・判定・修復・publication、run の recovery まで、feedback 処理全体の責務を確認・変更するための対象。

## Read this when
- feedback サブコマンドの処理全体や、report・decision・remediation・recovery 間の連携を確認するとき。
- feedback observation の report 化、判定根拠の固定、issue 修復、publication 後の cleanup・状態遷移を調べるとき。
- feedback run の checkpoint、auto join、再開、失敗・割り込み時の recovery を確認するとき。

## Do not read this when
- feedback 以外のサブコマンドを扱うとき。
- feedback の共通 run lifecycle、MCP 受付、永続 artifact の共通形式だけを確認したいときは、それぞれの共通実装を直接読む。
- feedback の個別判定・report・remediation・recovery の詳細だけを確認したいときは、対応する実装対象を直接読む。

## hash
- c859de4db18a02664dc23f2d49a76187f99576ca08d03c0c40b2eb7aff981b64

# `indexing.py`

## Summary
- work root の INDEX.md を更新する indexing CLI の実行入口を提供する。
- 実行前に cmoc 管理対象と clean worktree を確認し、排他ロック下で INDEX.md を更新・差分 commit し、結果を primary report に反映する。

## Read this when
- `cmoc indexing` の CLI 入口、実行前提条件、または indexing 処理全体の実行フローを確認するとき
- INDEX.md の更新、更新差分の commit、または indexing 実行結果の報告処理の呼び出し元を確認するとき

## Do not read this when
- INDEX.md の具体的な更新規則や探索・生成ロジックを確認したいときは、indexing 共通処理の対象を直接読む
- CLI 共通の実行制御や step 管理の仕様だけを確認したいときは、CLI runtime 共通処理の対象を直接読む
- worktree の clean 判定や cmoc 管理対象の検査実装だけを確認したいときは、対応する runtime 検査処理を直接読む

## hash
- 1b5fb1518b06f7acdfb54acdb2e8ab410c4772fa381bae42ed1af943e6209ce0

# `oracle`

## Summary
- oracle 系サブコマンドの実行境界を提供し、調査系と編集系の CLI ワークフローを分担する。
- oracle investigation は入力された調査指示をもとに prompt を組み立て、indexing 前処理後に read-only の Codex TUI を起動する。
- oracle edit は oracle 編集指示を受け取り、main worktree 上の active session branch などの前提を検証したうえで、共通設定による編集 agent call を 2 回実行し、各結果を primary report に反映する。

## Read this when
- oracle investigation または oracle edit の CLI 実行フロー、prompt 入力、agent 起動、実行前後の状態更新を確認・変更するとき。
- oracle edit の main worktree・session branch 前提や、2 回の編集 agent call の制御を調べるとき。
- oracle 系サブコマンドの処理へ入る入口や、調査系と編集系の責務分担を判断するとき。

## Do not read this when
- Codex 起動パラメータの詳細な構築規則だけを確認したいときは、対応する builder 実装を直接読むべきである。
- prompt 編集用の共通入出力や indexing、session 状態管理の詳細だけを確認したいときは、それぞれの共通 runtime 実装を直接読むべきである。
- oracle の正本仕様や編集対象そのものを確認したいときは、この実行ラッパーではなく oracle 側の仕様・対象ファイルへ進むべきである。

## hash
- 48440dc909a9ff3dc83a8f6cf0a475468df0f0b49112edd3bb0086e9c61d0191

# `realization`

## Summary
- `realization` サブコマンド配下の workload 実装をまとめるディレクトリ入口。apply と refactor の各処理へ進むための上位ルーティング対象。

## Read this when
- realization サブコマンドの workload 構成や、apply／refactor の処理入口を確認するとき。
- realization 配下で apply または refactor の workload 実装を調査・変更するとき。

## Do not read this when
- realization サブコマンド以外の処理を扱うとき。
- apply または refactor の具体的な lifecycle・実装詳細だけを確認したい場合は、対応する下位対象を直接読む。

## hash
- 485bfb2542457396c18017597ca6537502902f62230f1c638da651edbaddf10d

# `review`

## Summary
- review サブコマンドの realization 実装を配置するディレクトリ。現在は実装本文がなく、レビュー処理の具体的な入口として参照できる下位要素はない。

## Read this when
- review サブコマンドの実装ファイルを追加・変更する場所を確認するとき。

## Do not read this when
- oracle review の処理内容や仕様を調べるときは、対応する oracle 実装・仕様文書を直接読む。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `run`

## Summary
- 日本語の技術文書として、対象ディレクトリにある editing run のライフサイクル関連実装への入口。abandon・join の停止／統合／cleanup と、旧 import path の互換 shim を含む配下を、run lifecycle の共通処理やサブコマンド固有処理の調査時に振り分ける。

## Read this when
- editing run の停止・統合・cleanup・report・状態遷移など、複数の run lifecycle 実装を横断して確認するとき。
- `cmoc run abandon` または `cmoc run join` の処理入口を探すとき。
- 旧 import path の lifecycle／report 互換性を確認するとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。
- 共通 lifecycle の canonical 実装や workload 固有の merge・差分処理など、配下の特定実装を直接確認すべきとき。
- run 作成・通常編集・差分生成など、abandon／join のライフサイクル範囲に直接関係しない処理だけを調べるとき。

## hash
- b692c0592ebbf0f3b0b5fd155b8143d42f7edb6c6653a1301d983d594801c52c

# `session`

## Summary
- session サブコマンドのライフサイクル操作を実装するパッケージ。session の fork・join・abandon に関する処理を確認する際の入口となる。

## Read this when
- session サブコマンドの作成、home branch への統合、破棄、branch や state の更新・cleanup を確認または変更するとき。
- session lifecycle 操作間の競合制御や、失敗時の rollback・完了報告を追跡するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- SessionState のデータ形式や共通 CLI 実行基盤など、session lifecycle の個別操作より下位・共通の実装を直接確認したいとき。

## hash
- 17d723012891b050c8bc34a1457a07c14395b92a377ae134af87d7abb9b06331

# `tui.py`

## Summary
- `cmoc tui` サブコマンドの実行入口と本体処理を担い、インデックス前処理・入力編集・TUI 起動までの手順を統括する。
- 現在のリポジトリと作業ルートから設定を読み込み、入力された依頼文を TUI 起動用パラメータへ変換して Codex TUI を起動する処理への入口。

## Read this when
- `cmoc tui` の CLI 実行フロー、プロンプト編集、TUI 起動パラメータ構築、または Codex TUI 起動処理の連携を調べるとき。
- サブコマンド共通ランタイムへの接続や、現在の repository・work root・設定の受け渡しを確認するとき。

## Do not read this when
- TUI 起動パラメータの詳細な構築規則だけを確認したいときは、`acp.builder.tui.launch_tui` の実装を直接読む。
- プロンプト編集ファイルの予約・収集・確定処理だけを確認したいときは、`commons.prompt_editor_input` を直接読む。
- Codex TUI の実際の起動処理や実行結果の扱いだけを確認したいときは、`cmoc_runtime` の `run_codex_tui` 実装を直接読む。

## hash
- 70f2b0260c5debb76680c0f1935b776b0313bdf02fbb06eb7466d9d159212a8d
