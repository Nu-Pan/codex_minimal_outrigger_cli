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
- `cmoc session join` の実行処理と merge conflict 解消を担う実装。session branch の事前条件確認、home branch への merge、マージ後の状態保存と branch 削除、警告表示までを扱う。
- conflict 発生時は対象 path を NUL 区切りで取得し、Codex に解消を依頼した後、許可外の変更・marker 外の変更・未解決 marker・unmerged path を検査して merge commit を完了する。

## Read this when
- `cmoc session join` の CLI 挙動、実行前提、branch merge、session state 更新、branch 削除条件を確認するとき
- session join の merge conflict 処理、conflict marker 検査、Codex 呼び出し後の変更範囲検証を調査・変更するとき
- session join のエラー出力先、進捗 step、警告表示を確認するとき

## Do not read this when
- session の作成・実行・離脱など、session join 以外のサブコマンドの挙動だけを確認するとき
- conflict 解消用 prompt の内容や Codex 実行共通規則を直接確認したいときは、それぞれの prompt 定義・実行規則を読む
- Git 状態取得の共通処理だけを確認したいときは、共通の runtime Git 実装を直接読む

## hash
- b8e19759006c930fb59075adae4e8ff8bc78a3d8de25a6ca14f7d2e3459fc69e
