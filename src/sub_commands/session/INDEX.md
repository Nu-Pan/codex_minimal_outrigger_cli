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
- `session join` サブコマンドの実行処理を担う。active な session branch の事前条件・clean worktree・session state を検証し、session home branch へ merge した後、状態更新と session branch 削除、警告結果の表示までを行う。
- merge conflict 発生時は、conflict 対象の列挙、Codex による解消依頼、対象外変更や marker 外変更の検査、stage、merge commit までを制御する。Git path の NUL framing、conflict marker、ファイル内容 fingerprint など安全性検査の実装も含む。
- session join の CLI runtime 入口と、merge/conflict 解消を支える内部関数群を確認するための入口である。

## Read this when
- `cmoc session join` の実行条件、branch merge、session state 更新、branch 削除の挙動を変更・調査するとき。
- session join の merge conflict 解消フロー、Codex 呼び出し、変更範囲の検証、conflict marker 検査を確認するとき。
- session join のエラー出力先、警告表示、Git path の安全な取り扱いを調査するとき。

## Do not read this when
- session の作成・開始・終了など、join 処理以外の session lifecycle を扱うとき。
- 一般的な conflict resolution prompt の仕様や Codex 実行規則そのものを確認したいときは、それぞれの正本仕様を直接読む。
- Git 状態取得や共通 runtime、session join の conflict parameter 生成だけを調査する場合は、該当する共通実装を直接読む。

## hash
- c62cec28c8bf686a8b1ef803f64fc98886aef4939e1ddff2e7fbe17a90fd23b9
