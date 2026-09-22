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
- realization workload サブコマンド群の入口。apply と refactor の fork 処理を、それぞれ差分追従と realization ファイルの調査・修正として実行し、run lifecycle・Codex 呼び出し・差分管理・report 保存までを統括する。
- apply は配下の fork 実装へ進み、oracle 差分を基準に realization 側を追従させる処理を確認するときの入口。
- refactor は配下の fork 実装へ進み、realization file の選択、調査・修正、未解決 finding の管理、完了判定を確認するときの入口。

## Read this when
- realization サブコマンド全体の責務や apply/refactor のどちらへ進むべきか判断したいとき。
- run の作成、Codex agent 実行、差分の検査・commit、joinable 公開、report 保存が realization workload でどう束ねられているか確認したいとき。

## Do not read this when
- apply の差分追従処理の具体的な lifecycle を確認したい場合は apply/fork.py を直接読んでください。
- refactor の target 選択、file review、finding 解決、完了判定の詳細を確認したい場合は refactor/fork.py を直接読んでください。
- realization 以外のサブコマンドや共通 runtime の仕様を確認したい場合は、それぞれの対象ディレクトリ・共通モジュールへ直接進んでください。

## hash
- 8ed8cb54c41a7f86e43d6ac96becc69e63b1136b99f0fd9304c4bff206f5b3ea

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
- `cmoc run` の共通 lifecycle サブコマンド入口。active editing run の join と abandon を扱い、差分検査、merge、状態同期、report 保存、process/worktree/branch の cleanup までを実行する。
- `join.py` は active run の差分を検証して merge・post-join 処理・cleanup・失敗時の復旧状態を一続きで管理する。
- `abandon.py` は running・joinable・error の run を停止し、残存 process、worktree、branch、state を破棄する。
- `lifecycle.py` と `report.py` は旧 import path を維持する互換 shim で、共通実装を `commons` 側へ委譲する。

## Read this when
- `cmoc run join` または `cmoc run abandon` の lifecycle、run 資源の cleanup、状態遷移、report 生成の入口を確認するとき。
- run サブコマンド配下の join/abandon 実装と、旧 import path から共通 helper/report writer へ委譲する構成を把握するとき。

## Do not read this when
- run の共通 lifecycle ではなく、個別 workload の実行処理や別サブコマンドの仕様を確認するとき。
- 共通 helper の具体的な差分検査・状態管理・report 生成ロジック自体を確認したい場合は、`commons` 配下の実装を直接読むとき。

## hash
- 5dbf72af186979cb7f3a15000c0370971cd5ca84a83a441de5ff9d67db47f064

# `session`

## Summary
- セッションのライフサイクルを扱うサブコマンド群で、現在のローカルブランチからの session fork、session branch の home branch への join、active session の abandon と、join 時の conflict 解消・後始末を実装する。

## Read this when
- session の作成・統合・破棄の挙動を確認または変更するとき。
- session branch、session state、home branch の連携や、session join の merge conflict 解消処理を調べるとき。

## Do not read this when
- session サブコマンドの個別処理を直接確認すべき場合。
- session 以外のサブコマンドや、共通 runtime・state 定義そのものを調べる場合。

## hash
- ce4bd4c74792e950f549ab9cc3b3bd97f15021d6bb850edc1cdf56b567e9cfd3

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
