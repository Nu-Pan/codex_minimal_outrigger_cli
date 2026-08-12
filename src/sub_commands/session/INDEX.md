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
- `cmoc session join` の実行処理を担い、active な session branch を session home branch に安全に merge して後始末する実装。事前条件の検証、競合解消の委譲、変更範囲・conflict marker・unmerged path の検査、merge 後の session branch 削除と結果表示までを扱う。session join の実行フローや競合解消の制約を確認・変更するときの入口であり、session 状態の一般定義や他サブコマンドの処理を調べる場合は直接それぞれの仕様・実装へ進む。

## Read this when
- `cmoc session join` の事前条件、merge 対象、session branch の削除条件を確認するとき。
- merge conflict の自動解消、Codex 呼び出し後に許可外変更を拒否する検査、conflict marker と unmerged path の扱いを確認・変更するとき。
- session join の CLI 出力、失敗時の stderr 処理、Git path の安全な取得方法を確認するとき。

## Do not read this when
- session join 以外のサブコマンドの実行フローを確認するとき。
- session state や Codex 実行規則の一般定義だけを確認する場合は、それぞれの正本仕様を直接読む。

## hash
- 4d9415b661b1f766f7affd1e1cb477872bd1fa1bbd00d06274d5e906b256bcf7
