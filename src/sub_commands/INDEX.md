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
- `cmoc feedback report` の観測集約、issue の検証、レポート公開と未完了時の診断を扱う。
- 修復 run の進行・join と再開後の後処理をまとめ、判定入力の再確認履歴も管理する。

## Read this when
- feedback report の固定入力、候補集約・正規化・検証、表示内容や公開結果を変更・調査するとき。
- feedback report 固有の逐次修復、自動 join、中断後の再開、finalization を追うとき。
- 修正や証拠の変化が過去の判定に与える影響、再確認や循環診断を調べるとき。

## Do not read this when
- `submit_observation` の受付、reporter/collector の通信、raw observation の保存だけを変更するときは、受付・保存を担う共通処理から確認する。
- feedback report 固有ではない共通の状態保存や run/session lifecycle の挙動を変更するときは、それぞれの共通実装から確認する。

## hash
- f2d2912851836f069573712d51956412bf0e83533f2fb1c453ba49d9b7657a20

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
- editing run の join と abandon の lifecycle を担います。join の検査・merge 呼び出し、state と report の更新、失敗時の復旧、資源 cleanup を追う入口です。
- abandon 時の process 停止、run worktree と branch の削除、state と report の更新を扱います。
- 旧 import path を保つ互換 shim も含みます。共通 helper と report writer の正規実装は commons にあります。

## Read this when
- active editing run の join について、merge 前の検査から post-join 処理、state・report 更新、失敗時の復旧や cleanup まで調べるとき。
- active editing run の abandon に伴う process 停止、worktree・branch 削除、state 更新を調べるとき。
- 旧 import path の互換性や、ここから公開される共通 helper の利用を調べるとき。

## Do not read this when
- session 全体の fork・join・abandon の処理を調べるときは、session の lifecycle 処理を参照してください。
- workload ごとの editing run の fork や実行処理を調べるときは、該当する workload の fork 処理を参照してください。
- 共通の run lifecycle helper、join 共通処理、report writer の実装を変更するときは、commons にある正規実装を直接参照してください。

## hash
- 5614640a93310490b428e0ffe253e8270725fe73428f80f614384dae636d314b

# `session`

## Summary
- session branch を作成し、home branch へ統合するか、統合せず破棄する CLI 処理の実装入口です。
- 各操作の state 遷移、branch の後始末、失敗時の復旧処理を横断して確認できます。

## Read this when
- session の fork・join・abandon の事前条件や処理、state 遷移、失敗時の復旧を調べる・変更する場合。
- 複数の session 操作にまたがる branch と state の整合を確認する場合。

## Do not read this when
- 単一の session 操作だけを調べる場合は、その操作の実装へ直接進んでください。
- 共通の state 形式や Git・session runtime の処理自体を調べる・変更する場合は、それらの定義へ直接進んでください。

## hash
- 300aee23aa170007f8f71e9386a3ee9d7f75553c7d4dea7d5d8eebebb446f3ea

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
