# `apply`

## Summary
- この場所には現在サブコマンドの実装ソースがなく、現行の realization apply fork 処理は realization 系統にあります。

## Read this when
- apply の実装を探していて、現行の realization apply fork 処理の所在を確認したいとき。

## Do not read this when
- realization apply fork の処理を調べたり変更したりするときは、その実装を直接確認してください。
- run の join や abandon の処理を調べるときは、run 系統の実装を確認してください。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `doctor.py`

## Summary
- `cmoc doctor` の CLI 固有の入口です。共通の CLI 実行管理に接続し、doctor 前処理を明示的な単一ステップとして実行して、そのコマンド固有の結果を組み立てます。

## Read this when
- `cmoc doctor` の呼び出し単位の挙動や、前処理の明示実行・コマンド固有の結果を変更または確認するとき。

## Do not read this when
- doctor 前処理の修復内容や Git・index の扱いを調べるときは、共通前処理の実装を直接確認してください。
- 全サブコマンドに共通する実行ライフサイクルを調べるときは、共通 CLI 実行管理を確認してください。
- コマンドの登録や CLI 全体の構成を調べるときは、CLI のコマンド定義を確認してください。

## hash
- 1eb417245f2ab7964031bcace08e76c91beda19e6b7c26b38e163f2ec9977c3b

# `feedback`

## Summary
- `cmoc feedback report` が observation を report cut に固定し、issue の集約・判定・修復から通常または未完了レポートの公開まで進める実装群への入口です。
- feedback 専用 run の自動 join、判定根拠の再確認、publication 後の回復と cleanup も扱います。

## Read this when
- feedback report の入力固定、候補集約、修復の反復、収束・中断時の処理、レポート公開の挙動を変更・調査するとき。
- feedback 専用 run の join や publication 後の回復、および修復結果の判定根拠を確認するとき。

## Do not read this when
- 共通 feedback artifact の保存形式や共有検証だけが主題なら、共通 runtime 側から確認するとき。
- CLI のコマンド登録だけが主題なら CLI 入口を、issue 用 agent の prompt や出力 schema だけが主題なら builder 側を確認するとき。

## hash
- c859de4db18a02664dc23f2d49a76187f99576ca08d03c0c40b2eb7aff981b64

# `indexing.py`

## Summary
- `indexing` CLI サブコマンドの入口として、Codex 実行前のインデックス更新を登録し、明示実行時は work root の前提条件を検査して更新処理を呼び出す。
- 更新状況を primary report に記録し、更新された INDEX の commit までを CLI runtime につなぐため、コマンド固有の実行経路を調べる入口となる。

## Read this when
- 明示実行する indexing コマンドの起動条件、実行順、work root の扱いを確認・変更するとき。
- 更新の開始・完了・失敗・中断と commit 結果が primary report にどう反映されるか、また CLI から更新処理がどう呼び出されるかを追うとき。

## Do not read this when
- INDEX 対象の列挙、entry の再利用・hash・生成、書き戻し・復元、排他制御や Git commit の内部手順を調べるときは、共通 indexing lifecycle の実装から確認する。
- CLI runner や worktree 前提チェックなど、共通 runtime の動作を調べるときは、該当する共通 runtime 実装を直接読む。

## hash
- 273cd0aecd7905c02ed812dd0c3aba37321fc748312192759e24f211db0c7dc3

# `oracle`

## Summary
- oracle 固有の `edit` と `investigation` サブコマンドの実行フローを組み立てる入口。編集では indexing preflight 後に Codex exec を2回実行し、調査では Codex TUI を起動する。

## Read this when
- `cmoc oracle edit` の編集指示の受け取り、起動前提、または Codex exec 呼び出しの流れを追う・変更する場合。
- `cmoc oracle investigation` の調査指示の受け取りや、read-only TUI 起動の流れを追う・変更する場合。

## Do not read this when
- 変更対象が複数コマンドで共有される prompt 入力、indexing preflight、起動パラメータ構築、または Codex 実行処理そのものである場合は、その共通処理の実装から確認する。
- oracle コマンド以外のサブコマンドの処理を追う場合は、そのコマンドの実装から確認する。

## hash
- 1a9e0c51494360d2a9d1b70d5b85eced5b137036aaec5e8584803914f1c38434

# `realization`

## Summary
- realization workload の実行処理を担い、oracle 差分を realization に追従させる処理と、realization file を巡回して調査・修正する処理の入口となる。
- 差分追従では run の差分検査と公開を扱い、巡回調査では対象ごとの進捗や未解決所見、完了判定を扱う。

## Read this when
- `realization apply fork` の差分追従や run 公開の挙動を調査・変更するとき。
- `realization refactor fork` の対象巡回、file 単位の修正、所見や完了判定の挙動を調査・変更するとき。

## Do not read this when
- 差分追従の処理だけが対象なら、その処理の下位項目から読み始める。
- file 単位の refactor cycle だけが対象なら、対応する下位項目から読み始める。
- CLI の引数解析・コマンド登録だけ、または共有 editing-run lifecycle が対象なら、その責務を担う実装を直接読む。

## hash
- 8ed8cb54c41a7f86e43d6ac96becc69e63b1136b99f0fd9304c4bff206f5b3ea

# `review`

## Summary
- 現状、レビュー関連の実装ソースはなく、無視対象のコンパイル済みキャッシュだけが残っています。現行 CLI のレビュー機能の実装入口としては扱えません。

## Read this when
- このディレクトリにレビュー実装が存在するか、残存キャッシュの状態を確認するとき。

## Do not read this when
- 現行 CLI のコマンド構成や oracle edit・investigation の挙動を調べるときは、CLI 定義とそれらの実装を直接確認してください。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `run`

## Summary
- editing run を完了する `cmoc run join` の差分検査、merge、post-join 同期、結果記録、run 資源の cleanup を扱います。run 単位の統合手順を追う入口であり、session 全体の lifecycle や workload ごとの fork 処理とは責務が異なります。
- `cmoc run abandon` の process 停止、worktree・branch・state の cleanup と結果記録を扱います。
- 共有 lifecycle・report 処理への旧 import path を保つ互換層も含みます。

## Read this when
- `cmoc run join` の差分検査、merge、post-join 処理、失敗時の rollback、report、cleanup の流れを変更するとき。
- `cmoc run abandon` の process 停止、state 更新、worktree・branch の cleanup を変更するとき。
- 共有 lifecycle・report 処理への旧 import path の互換性を保守するとき。

## Do not read this when
- run の共有 lifecycle、report、join helper 自体を変更するときは、その共有 runtime の実装を直接参照してください。
- session 全体の fork・join・abandon を変更するときは、session lifecycle の実装を参照してください。
- workload 固有の fork や実行処理を変更するときは、該当 workload の実装を参照してください。

## hash
- 88a67686777c235c098c1a860ee9dbc17ebc7dfef9ce5614dcfb638e6b48fb01

# `session`

## Summary
- `session fork` による session 作成と `session join`・`session abandon` による取り込み・破棄を実行する CLI 処理の実装群です。
- branch 切替や session state 更新を担い、fork と abandon の失敗時復旧も扱うため、session の lifecycle 動作を調べる入口になります。

## Read this when
- `cmoc session fork` の作成条件、session branch と state の作成、または失敗時の rollback を確認・変更するとき。
- `cmoc session join` の home branch への merge、conflict 解消、state 更新や session branch の後始末を扱うとき。
- `cmoc session abandon` で session を取り込まず破棄する処理や、失敗時の復旧を扱うとき。

## Do not read this when
- CLI のコマンド登録や名前を確認する場合は `src/main.py` を読むとき。
- session state のデータ形式、検証、永続化自体を調べる場合は `src/commons/runtime_state.py` を読むとき。

## hash
- 664c168771428e71725c317487f8328ea05c9f72db44a66b39d5aa95f450f263

# `tui.py`

## Summary
- `cmoc tui` の実行を CLI runtime に接続し、インデックス事前処理と prompt editor 保存先の ignore 確認を登録する入口。
- 依頼文の skeleton を用意し、エディタ入力の予約・編集・確定を経て起動パラメータを作り、Codex TUI へ渡す流れを統括する。

## Read this when
- `cmoc tui` の起動経路、事前処理、設定の読み込み、またはコマンド実行枠への接続を追う・変更するとき。
- 利用者の依頼文がエディタ入力から起動パラメータになり、TUI に渡る順序を追う・変更するとき。

## Do not read this when
- 完全 prompt の文面や TUI 起動パラメータの定義を変更するときは、その構築定義を読む。
- エディタの選択、入力ファイルの保存・検証、handoff の仕組みを変更するときは、共通の prompt editor 入力処理を読む。
- 共通 CLI runtime のログ、ステップ管理、実行時エラーの扱いを変更するときは、その runtime の実装を読む。

## hash
- 52be00ca2b1f26a3ffa44743eeed684258aed27c06159476b93bf37d9cc4e2d2
