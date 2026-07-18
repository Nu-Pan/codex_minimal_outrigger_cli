# realization run 共通仕様

## 対象

- realization run は、oracle file に realization file を追従させる隔離作業である。
- 以下の 2 種類を扱う。
    - apply run: `cmoc realization apply fork|join|abandon`
    - refactor run: `cmoc realization refactor fork|join|abandon`
- `cmoc apply fork|join|abandon` は廃止する。後方互換性を維持してはいけない。
- apply run と refactor run の具体的な作業内容は、それぞれ `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_apply.md` と `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` を正本とする。

## 同時実行の境界

- 1 つの session が保持できる未 join の realization run は高々 1 つとする。
- `{{cmoc-session-state-file}}` の `realization_run` セクションで、run の種類と状態を共有管理する。
- apply run と refactor run を同時に active にしてはいけない。

## fork の共通事前条件

以下の場合はエラー終了する。

- 現在の branch が `{{cmoc-session-branch}}` ではない。
- 対応する `{{cmoc-session-state-file}}` が存在しない。
- `session.state` が `active` ではない。
- `realization_run.state` が `ready` ではない。
    - `cmoc realization refactor fork` による `paused` run の再開だけは例外とする。
- `{{cmoc-session-branch}}` 側の worktree に git 未コミット差分が存在する。

## fork の共通開始処理

1. doctor preprocess を呼び出す。
2. run 開始時点の `{{cmoc-session-branch}}` HEAD を `{{realization-oracle-snapshot-commit}}` とする。
3. run の種類に対応する `{{cmoc-realization-run-branch}}` と `{{cmoc-realization-run-worktree}}` を作成する。
4. `realization_run.state` を `running` にし、run の種類、branch、`{{realization-oracle-snapshot-commit}}` を保存する。
5. 以後の realization 作業を `{{cmoc-realization-run-worktree}}` 上で行う。

`paused` な refactor run の再開では新しい snapshot, branch, worktree を作らず、保存済みの `{{realization-oracle-snapshot-commit}}`, branch, worktree を使う。`realization_run.state` だけを `running` に戻す。

## run branch の想定内差分

- apply run が積み上げてよい差分は以下とする。
    - realization file
    - cmoc が自動生成する任意階層の `INDEX.md`
- refactor run が積み上げてよい差分は以下とする。
    - realization file
    - `{{work-root}}/.cmoc/gt/ar/realization/refactor/state.json`
    - cmoc が自動生成する任意階層の `INDEX.md`
- agent は realization file だけを変更する。
- refactor state の更新と `INDEX.md` の生成は cmoc が担う。

## join

### 対象コマンド

- `cmoc realization apply join` は apply run だけを join する。
- `cmoc realization refactor join` は refactor run だけを join する。
- run の種類と異なる join コマンドを呼び出した場合はエラー終了する。

### 引数

- 位置引数なし。
- オプション引数 `--force-resolve` を受け取る。

### 事前条件

以下の場合はエラー終了する。

- 現在の branch が `{{cmoc-session-branch}}`, `{{cmoc-realization-run-branch}}` のいずれでもない。
- `session.state` が `active` ではない。
- `realization_run.state` が `completed`, `paused`, `error` のいずれでもない。
    - `paused` は refactor run に限る。
- git 未コミット差分が存在する。

### 想定外の差分

- `{{cmoc-session-branch}}` では、run 開始後も oracle file, `memo`, `INDEX.md` を変更してよい。
- `{{cmoc-realization-run-branch}}` では、「run branch の想定内差分」に含まれるものだけを変更してよい。
- 通常モードでは、想定外の差分をレポートして join を中止する。
- `--force-resolve` を指定した場合は、想定外の差分を revert し、その事実をレポートして続行する。

### 実行手順

1. doctor preprocess を呼び出す。
2. 事前条件と想定外の差分を検査する。
3. `{{cmoc-session-branch}}` 上で `git merge --no-ff {{cmoc-realization-run-branch}}` を実行する。
4. merge が完了した場合、`realization_run.state` を `ready` にして run 情報を初期化する。
5. apply run の場合だけ、`session.last_joined_realization_apply_oracle_snapshot_commit` を、その run の `{{realization-oracle-snapshot-commit}}` で更新する。
6. 結果をレポートする。

### merge conflict

- `INDEX.md` はコンフリクト自動解決対象とし、衝突したファイルを削除して解決してよい。
- `INDEX.md` 以外のコンフリクトを cmoc が解決してはいけない。対象をユーザーへ報告する。

### 使用済み branch の削除

以下を全て確認できた場合だけ、`{{cmoc-realization-run-branch}}` と `{{cmoc-realization-run-worktree}}` を削除してよい。

- `realization_run.state` が `ready` である。
- run branch の HEAD が `{{cmoc-session-branch}}` から到達可能である。
- run の結果が保存済みである。

確認に失敗した場合は削除せず、warning として報告する。

## abandon

### 対象コマンド

- `cmoc realization apply abandon` は apply run だけを破棄する。
- `cmoc realization refactor abandon` は refactor run だけを破棄する。
- run の種類と異なる abandon コマンドを呼び出した場合はエラー終了する。

### 引数

- 引数なし。

### 事前条件

以下の場合はエラー終了する。

- 現在の branch が `{{cmoc-session-branch}}`, `{{cmoc-realization-run-branch}}` のいずれでもない。
- `session.state` が `active` ではない。
- `realization_run.state` が `ready` である。
- run branch または worktree を状態から特定できない。
- `{{cmoc-session-branch}}` 側の worktree に git 未コミット差分が存在する。

### 破棄対象と手順

- run worktree、その未コミット差分、run branch、および session state 上の active run 情報を破棄してよい。
- session branch、その commit、session home branch、保存済み report、session state file 自体を破棄してはいけない。
- `realization_run.state` が `running` の場合は、対応する process を停止し、停止を確認してから cleanup する。
- 現在の worktree が削除対象である場合は、削除対象の外から cleanup できる状態へ移動する。
- run worktree と run branch は、未 merge でも強制削除してよい。
- cleanup 後に `realization_run.state` を `ready` にし、run 情報を初期化する。
- refactor run branch 上だけにある refactor state の更新は、run branch とともに破棄される。
- abandon は Codex CLI を呼び出さない機械的な cleanup とする。
- 対象が既に存在しない場合は warning として続行してよいが、session state を `ready` に戻せない場合はエラー終了する。

## report

- fork, join, abandon は、run の種類、branch、worktree、実行前後の状態、warning を stdout から判別可能にする。
- fork は、run で変更した path と完了理由も判別可能にする。
- apply fork は、AI による意味的な変更要約を作るためだけの追加 agent call を行わない。
- fork の report file と終了コードは workload の個別仕様を正本とする。
