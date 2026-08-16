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
- `session abandon` の CLI 実行経路を定義し、active session の事前条件確認、home branch への切り替え、session state の abandoned 化、session branch の削除を扱う。cleanup 中に失敗した場合は state と branch を復元して再実行可能にするため、session abandon の実装挙動や失敗時 rollback を確認する際の入口となる。

## Read this when
- `cmoc session abandon` の実装や外部挙動を確認するとき
- session branch の破棄、home branch への切り替え、session state の更新を調査するとき
- cleanup 失敗時の state・branch rollback とエラー報告を確認するとき

## Do not read this when
- session の開始や再開など、abandon 以外のライフサイクル処理を確認するとき
- 一般的な Git branch 操作や、session に依存しない CLI 共通処理を確認するとき
- abandon の具体的な実装ではなく、session state のデータ構造や共通 runtime API の仕様を確認するとき

## hash
- cf1ab013e06c19645c074e980fc6fc318ff0dd6cf3c9ffa15fb50667ec104582

# `fork.py`

## Summary
- 通常の local branch から cmoc の session branch を作成し、session state を保存する CLI 実装。active session の重複防止、clean worktree 要件、session-id 衝突回避、branch・state 作成失敗時の rollback とエラー報告を扱う。session fork の実行経路を確認する際の入口となる。

## Read this when
- `cmoc session fork` の実行条件や、session branch・state の作成手順を確認するとき
- session fork 失敗時に branch と state file をどのように rollback し、残存状態を報告するか調べるとき
- active session の排他制御や session-id の衝突回避を確認するとき

## Do not read this when
- session の join・abandon の挙動を確認するとき
- session state の項目定義や永続化形式そのものを確認するとき
- CLI 共通のログ・step 実行機構だけを確認するとき

## hash
- 279de439ccb1104dac34d164c3eae7fb868689475fcb3d31d1af61bdef87ab59

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
