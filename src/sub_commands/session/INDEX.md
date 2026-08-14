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
- `cmoc session join` の実行本体と merge conflict 解消処理を担う。session branch の事前条件、clean worktree、home branch への `--no-ff` merge、到達可能性を確認した local branch 削除、状態更新、結果表示を扱う。
- merge conflict 発生時は対象 path を NUL 区切りで取得し、Codex に解消を依頼する。conflict 対象外の変更、file type・mode の変更、marker 外の内容変更、未解決 marker、unmerged path を検査して拒否し、解決後に対象を stage して merge commit を作成する。
- session join の CLI 実装や、conflict 解消の安全性・差分制限・branch cleanup の挙動を確認する際の入口となる。

## Read this when
- `cmoc session join` の実行フロー、事前条件、merge 後の state 更新または branch 削除を調査・変更するとき。
- session join の merge conflict 解消で、Codex 呼び出し後に許可される変更範囲、conflict marker 検査、stage、merge commit の挙動を確認するとき。
- session join の Git path 取扱い、到達可能性確認、エラー出力先、完了結果の表示を調査するとき。

## Do not read this when
- session state のデータ構造や session lifecycle の正本仕様だけを確認する場合。
- conflict resolution parameter のプロンプト内容だけを確認する場合。
- session join とは無関係な CLI subcommand、一般的な Git 実行、または共通 runtime の実装を直接調査する場合。

## hash
- ef11fba3d00358a86ef405a3a8b3f494d47f74048c356a844cad9c4fec3a7dbf
