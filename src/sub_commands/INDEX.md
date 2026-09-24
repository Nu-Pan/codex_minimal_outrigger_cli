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
- `cmoc indexing` CLI の実行入口と本体を提供し、対象 work root の INDEX.md を更新して必要な差分を commit する。実行前に cmoc の ignore 設定と clean worktree を検査し、ロック、進捗・結果報告、割り込みや失敗状態の記録まで統括する。

## Read this when
- INDEX.md の自動更新・commit を行う indexing サブコマンドの実行条件、処理順序、失敗時状態、結果報告を確認したいとき
- `cmoc indexing` の CLI 入口や、インデックス更新処理をどの runtime API 経由で呼び出すかを変更・調査するとき

## Do not read this when
- INDEX.md の個別内容の生成規則やファイル探索・更新アルゴリズムそのものを確認したいときは、`commons.indexing` の実装を直接読むべき場合
- clean worktree 検査や cmoc ignore 判定の共通仕様だけを確認したいときは、runtime 側の precondition 実装を直接読むべき場合
- indexing 以外の CLI サブコマンドの挙動を調べるとき

## hash
- 273cd0aecd7905c02ed812dd0c3aba37321fc748312192759e24f211db0c7dc3

# `oracle`

## Summary
- oracle 系サブコマンドの実装入口をまとめるパッケージ。
- `oracle edit` は main worktree の active な cmoc session branch で、編集指示に基づく Codex exec を 2 回実行する。
- `oracle investigation` は入力された調査指示から Codex TUI を起動する read-only ワークロード。

## Read this when
- `cmoc oracle edit` の入力処理、事前条件、indexing、2 回の agent call、実行状態更新を確認するとき
- `cmoc oracle investigation` の入力処理、prompt 構築、TUI 起動経路を確認するとき
- oracle 系サブコマンドの CLI 実装入口を特定するとき

## Do not read this when
- oracle 編集・調査用 prompt の正本契約を確認したい場合は `oracle/doc` 配下の対象を直接読む
- Codex 起動パラメータの生成ロジックを確認したい場合は `acp/builder/oracle` 配下の対応する builder を直接読む
- 共通の入力編集、runtime、indexing 処理だけを確認したい場合は、それぞれの `commons` または `cmoc_runtime` の実装へ直接進む

## hash
- 1a9e0c51494360d2a9d1b70d5b85eced5b137036aaec5e8584803914f1c38434

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
- `cmoc run` 配下の実装入口で、active editing run の join と abandon の lifecycle を扱う。
- `join.py` は差分検査、merge、post-join 状態同期、report 保存、cleanup と失敗時の復旧状態を一連で処理する。
- `abandon.py` は実行中 run の停止、worktree・branch・state の cleanup、report 保存を処理する。
- `lifecycle.py` と `report.py` は旧 import path を維持する互換 shim で、共通実装を `commons` へ委譲する。

## Read this when
- `cmoc run join` または `cmoc run abandon` の処理フロー、状態遷移、merge・cleanup・report の挙動を確認・変更するとき。
- run サブコマンド固有の lifecycle 実装や、旧 import path の互換 shim を調べるとき。

## Do not read this when
- run 以外のサブコマンドの処理を確認するとき。
- 共通 lifecycle・report 処理の本体や正本仕様を確認する場合は、`commons` 配下または `oracle` 配下の対応対象を直接読むとき。

## hash
- 88a67686777c235c098c1a860ee9dbc17ebc7dfef9ce5614dcfb638e6b48fb01

# `session`

## Summary
- session サブコマンドの実装パッケージ。現在の local branch から session branch を作成する fork、session branch を home branch に取り込む join、取り込まず破棄する abandon の処理をまとめている。
- 各サブコマンドは CLI runtime、session state、Git branch 操作、事前条件検証、失敗時の rollback または conflict 解消を担当する。

## Read this when
- session fork・join・abandon のCLI挙動や相互関係を調べるとき
- session branch、home branch、session state の生成・取り込み・破棄処理の実装入口を探すとき
- session 操作の失敗時処理、cleanup、rollback、merge conflict 解消の流れを確認するとき

## Do not read this when
- session 操作以外のサブコマンドを調べるとき
- fork、join、abandon のいずれか特定の処理の詳細だけを確認する場合で、該当する個別ファイルを直接読めるとき
- session state の共通データ形式や CLI 全体の dispatch 機構だけを調べるとき

## hash
- 664c168771428e71725c317487f8328ea05c9f72db44a66b39d5aa95f450f263

# `tui.py`

## Summary
- `cmoc tui` サブコマンドの実行入口と本体処理を提供し、indexing preflight・入力エディタ・TUI 起動処理を所定の順序で連携する。
- 現在の repository と設定を取得し、完全な prompt skeleton を用意して利用者の依頼文を編集・収集した後、TUI 起動パラメータを構築して Codex TUI を起動する。

## Read this when
- `cmoc tui` の CLI 実行入口、処理順序、prompt 編集入力から Codex TUI 起動までの連携を確認・変更するとき。
- TUI サブコマンドが indexing preflight、ログ付き共通 CLI runner、TUI 固有の通知・起動設定をどのように接続するかを確認するとき。

## Do not read this when
- TUI 起動時に注入する prompt の内容や固定起動パラメータ自体を確認・変更するときは、TUI parameter builder の実装を直接読む。
- prompt の予約・編集・収集や共通 Codex TUI runtime の挙動だけを確認するときは、それぞれの専用モジュールを直接読む。

## hash
- 52be00ca2b1f26a3ffa44743eeed684258aed27c06159476b93bf37d9cc4e2d2
