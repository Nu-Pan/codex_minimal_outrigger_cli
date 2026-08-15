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
- `session join` サブコマンドの実行処理と、session branch の merge conflict 解消を担う。active な session branch の事前条件を検証し、session home branch へ安全に merge した後、状態を joined に更新し、merge 済みの場合だけ session branch を削除する。
- merge conflict 発生時は conflict 対象の列挙、Codex による marker 解消、許可外の変更や marker 外の変更の検査、stage、merge commit 完了確認までを行う。Git path の NUL framing、file 種別・mode・内容の fingerprint、conflict marker 検査など、競合解消の安全性を担保する補助処理も含む。
- session join の実装や挙動、merge・conflict 解消・branch 削除の安全性、またはこれらの内部検査を変更・調査するときの入口となる。通常の session 作成・状態管理や conflict 解消プロンプト自体を確認する場合は、それぞれの専用対象へ進む。

## Read this when
- `cmoc session join` の事前条件、merge 対象、session state 更新、merge 後の branch 削除動作を確認するとき
- session join 中の merge conflict 解消、Codex 呼び出し、許可外変更の拒否、conflict marker 検査を調査・変更するとき
- session join の primary report 更新や terminal result、Git path の安全な取り扱いを確認するとき

## Do not read this when
- session の状態や session_home_branch の正本仕様を確認することが目的で、サブコマンド実装の挙動を調べる必要がないとき
- conflict 解消時に Codex へ渡すプロンプト仕様そのものを確認するとき
- session join 以外の session サブコマンドの実装を直接調査するとき

## hash
- c96a47dc6a8c381176cb56d82ef7f0e8dae578fce8a7c0b565287f473abdd958
