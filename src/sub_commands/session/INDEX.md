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
- session branch を session home branch へ merge し、事前条件確認、conflict 解消依頼、merge 完了、状態更新、local branch 削除と結果表示までを実行する CLI 実装。
- merge conflict 時は対象 path を安全に列挙し、Codex に conflict marker 解消を依頼したうえで、対象外変更・marker 残存・unmerged path を検査してから commit する。

## Read this when
- `cmoc session join` の実行フロー、事前条件、状態遷移、merge 後の branch 削除条件を確認するとき。
- session join の merge conflict 解消、Codex 呼び出し、対象外差分の検査、conflict marker 判定を変更または調査するとき。

## Do not read this when
- session 作成や session 状態管理全般を調査するだけで、join サブコマンドの挙動を扱わないとき。
- conflict resolution parameter の仕様や Codex 実行規則そのものを確認する場合は、対応する設定・仕様ファイルを直接読むとき。

## hash
- 4db399ac22ea9860918c2283317bd42e702d73015c22a544dabf6504031743e9
