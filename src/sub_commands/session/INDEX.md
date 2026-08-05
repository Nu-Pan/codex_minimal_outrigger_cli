# `__init__.py`

## Summary
- session サブコマンドの実装パッケージ。session サブコマンドに関する実装を確認する際の入口となる。

## Read this when
- session サブコマンドの実装や構成を確認・変更するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。

## hash
- bfd8539ef9776e0e27e2e2e0d6365626dc832eb3abf90403affec4b29f1f8364

# `abandon.py`

## Summary
- `cmoc session abandon` サブコマンドの実装。active session を検証し、home branch へ切り替えた後に session branch と state を abandoned としてクリーンアップする。失敗時は state・branch を可能な限りロールバックし、結果または cleanup error を表示する。

## Read this when
- `cmoc session abandon` の事前条件、branch 切り替え・削除、state 更新、cleanup 失敗時の復旧処理を変更・調査するとき。

## Do not read this when
- session の開始・継続・完了など、abandon 処理以外の session サブコマンドを変更・調査するときは、各サブコマンドの実装を直接読む。

## hash
- 4409f62cddd5b057e30bd1769b75c2bbddcfdcb40636b89b68e7075effa1c815

# `fork.py`

## Summary
- 現在の local branch から cmoc 管理対象の session branch と state file を作成する CLI 実装。active session の重複確認、clean worktree 検証、session-id 衝突回避、branch/state 作成、結果表示を担う。作成途中の失敗時には branch と state file をロールバックし、復旧情報を含むエラーを報告する。

## Read this when
- `cmoc session fork` の branch 作成、session state 保存、session-id 生成、競合制御、失敗時ロールバックの挙動を変更・調査するとき。

## Do not read this when
- session の join・abandon など、fork 実行以外のライフサイクル処理を確認するとき。
- session state のデータ構造や共通 runtime 関数の仕様を直接確認する必要があるとき。

## hash
- 9f402913f831a35fc4e90001691620f8eed657cda8878eeb7ae91320860736e7

# `join.py`

## Summary
- `cmoc session join` の CLI 実装。active な session branch の事前条件を検証し、session home branch へ merge した後、到達可能な場合のみ元 branch を削除して結果を表示する。
- merge conflict 発生時は未解決 path を安全に列挙し、Codex に conflict marker の解消を依頼する。conflict 対象外の変更や marker 外の内容変更を検査し、解決後に stage・commit まで行う。
- session join の実行本体と、conflict 解決、差分監視、path fingerprint、marker 検出などの内部補助処理を含む。

## Read this when
- session join CLI の実行条件、merge・branch 削除・結果表示の挙動を確認または変更するとき
- session join における merge conflict の Codex 委譲、安全な差分制限、marker 検証を確認または変更するとき
- session branch の join 後 cleanup や failure 時の stderr 出力を調査するとき

## Do not read this when
- session の作成・開始・終了など join 以外の subcommand の挙動を確認するとき
- conflict resolution 用 prompt の正本仕様や builder 実装そのものを確認するときは、対応する oracle または builder の対象を直接読む
- 共通 CLI runtime、state 永続化、Git status 取得の一般仕様だけを確認するときは、それぞれの共通実装・仕様を直接読む

## hash
- b8e19759006c930fb59075adae4e8ff8bc78a3d8de25a6ca14f7d2e3459fc69e
