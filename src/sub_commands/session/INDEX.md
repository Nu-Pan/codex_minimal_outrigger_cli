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
- `cmoc session abandon` の CLI 実装。active session を検証し、home branch へ切り替えた後に session state を abandoned として保存し、session branch を削除する。
- cleanup 中に失敗・中断した場合は state と session branch を復元し、再実行可能な状態に戻せたかを含むエラー情報を返す。

## Read this when
- session abandon の事前条件、home branch への切替、session branch 削除、cleanup 失敗時の rollback 挙動を確認・変更するとき
- session abandon の terminal result や primary report の更新内容を確認するとき

## Do not read this when
- session の作成・実行・完了など、abandon 以外のライフサイクル処理を確認するとき
- branch モデルや state ファイル形式そのものの正本仕様を確認するときは、対応する oracle 文書を直接読む

## hash
- 4ae2c8a1df21e91e62492ee37e9cebced2e19e6a0cbf6f26ad8f2ea3b82f4b2d

# `fork.py`

## Summary
- 通常の local branch から cmoc の session branch を作成し、session state を保存する CLI 実装。既存の active session や dirty worktree、managed branch を拒否し、session-id と branch の衝突を避けながら fork 処理を進める。
- branch 作成または state 保存に失敗した場合は、作成済み branch と state file を可能な範囲で rollback し、失敗状況を CmocError として報告する。session fork の実行手順、排他制御、primary report 更新、terminal result 確定までを一つの実行入口で扱う。

## Read this when
- `cmoc session fork` の実行フロー、事前条件、session branch 作成、session state 保存の挙動を確認するとき
- session-id の衝突回避や、fork 失敗時の rollback・エラー報告を変更または調査するとき
- session fork と active session の競合防止、branch/state の整合性を確認するとき

## Do not read this when
- session state の項目や永続化形式そのものを確認したい場合は、session state の仕様・実装を直接読むとき
- session join や abandon など、fork 後の session 操作だけを調査するとき
- 一般的な Git branch 操作や CLI 共通実行基盤の仕様だけを確認するとき

## hash
- ea1db2907745121b66ea0bf80bc5e44e088acd60f87974654dba75f007ef2b7d

# `join.py`

## Summary
- `session join` サブコマンドの実行制御を担う実装です。active な session branch の事前条件を確認し、session home branch へ `--no-ff` merge した後、状態を `joined` に更新します。merge target HEAD から到達可能な場合だけ local session branch を削除し、削除できない場合は警告を返します。
- merge conflict 発生時は Codex に解消を依頼し、conflict marker、unmerged path、conflict 対象外の変更、marker 外の内容変更を検査してから merge を完了します。session join の branch 操作、状態更新、conflict 解消の安全性、terminal result を確認・変更するときの入口です。

## Read this when
- session join の事前条件、session home branch への merge、session state の更新、local session branch の削除を確認・変更するとき
- session join の merge conflict 解消、conflict marker 検査、Codex 呼び出し後の差分制限を確認・変更するとき
- session join の terminal result、警告、primary report 更新を確認するとき

## Do not read this when
- session の状態モデルや状態値の正本仕様だけを確認するとき
- Codex 実行や prompt 生成の共通規則だけを確認するとき
- session join 以外のサブコマンド固有の挙動を確認・変更するとき

## hash
- 3c8e08d2248d8498b4486e71e86153d3aa236b05d3a01045af0e0631ec05eb6f
