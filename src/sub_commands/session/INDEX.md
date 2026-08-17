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
- active な session を home branch へ merge せず破棄する CLI サブコマンドの実装。session branch 上での事前条件確認、clean worktree と home branch の検証、home branch への切替、session state の abandoned 化、session branch の削除、terminal result の確定を担う。cleanup 中に失敗した場合は state と branch を復元し、再実行可能性と rollback 結果をエラーとして報告する。session abandon の実行経路や cleanup・rollback 挙動を調べる際の入口。

## Read this when
- session abandon サブコマンドの実装を変更・レビューするとき
- active session の破棄、home branch への切替、session branch の削除の挙動を確認するとき
- cleanup failure 時の session state と branch rollback を調査するとき

## Do not read this when
- session の作成・再開・完了など、abandon 以外のサブコマンドの実装を調べるとき
- session の一般的な状態定義や branch model の正本仕様だけを確認したいとき
- CLI 共通実行基盤や primary report 更新の共通実装を直接確認したいとき

## hash
- b3cdcb0356f351024191dba2d8fd41285dc05d6f9eb5256c95940d3d1fcac70f

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
