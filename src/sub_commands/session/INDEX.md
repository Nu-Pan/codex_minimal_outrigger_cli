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
- アクティブな session を home branch へ merge せず破棄する CLI サブコマンドの実装。session branch 上での事前条件確認、clean worktree の検証、home branch への切替、session state の abandoned 更新、session branch の削除と、失敗時の state・branch 復旧を扱う。session abandon の動作、cleanup、rollback、terminal result を確認・変更するときの入口となる。

## Read this when
- `cmoc session abandon` の実行条件、branch 切替、session state 更新、session branch 削除の挙動を調べるとき。
- cleanup 中のエラーや利用者中断時に、session を再実行可能な active state と元の branch に戻す処理を確認するとき。

## Do not read this when
- session の開始、継続、完了、再開など abandon 以外のライフサイクル処理を調べるとき。
- CLI 共通ランナーや git・state 操作の一般仕様を確認したい場合は、まずそれぞれの共通実装・仕様を直接読むとき。

## hash
- d36691fab8b6d83ed0172ad10897b0c62d3095bba5a98711497305f33f7f22e3

# `fork.py`

## Summary
- 現在の local branch から cmoc 管理対象外の session branch を作成し、fork 時点の HEAD と home branch を session state に保存する CLI 実装。session fork の開始条件、排他制御、branch/state の作成、失敗時の rollback、一意な session-id 生成を扱う。session fork の挙動や作成失敗時の復旧を確認・変更するときの入口。

## Read this when
- `cmoc session fork` の実装や、session branch・session state の作成手順を確認するとき
- active session の重複防止、session-id の衝突回避、branch/state 作成時の排他制御を調査するとき
- branch 作成または state 保存に失敗した場合の rollback とエラー情報を確認するとき

## Do not read this when
- session の join、abandon、state の一般的な形式だけを確認したいときは、それぞれの専用実装または session state の仕様を直接読む
- CLI 共通の実行制御や個別の git/state helper の仕様だけを確認したいときは、対応する共通実装・仕様を直接読む

## hash
- 2b4e7f6483300610ad42bfaf23f30394ee6dd9feefcba3ad2c386905d8a9f662

# `join.py`

## Summary
- `session join` サブコマンドの実行本体で、active な session branch を session home branch にマージし、状態を joined に更新して session branch の削除まで行う。事前条件検証、clean worktree 要求、Git merge、state 永続化、削除結果と警告の terminal result 化を担う。
- マージ競合時は Codex CLI に競合解消を依頼し、競合対象外の変更や conflict marker 外の変更を拒否したうえで、対象を stage して merge commit を完了する。Git path の安全な列挙、通常ファイルの fingerprint、競合文脈の保持検査もこの処理の補助責務である。
- session join の CLI 実装、session branch の join・競合解消・削除条件、または Codex に許可する競合解消範囲を確認・変更するときの入口。session の状態モデルや一般的な Codex 実行規則そのものを確認する場合は、それぞれの正本仕様へ直接進む。

## Read this when
- `cmoc session join` の動作、事前条件、merge target、state 更新、session branch 削除を調査・変更するとき
- session join 中の merge conflict 解消、Codex 呼び出し後の差分制限、conflict marker 検査を調査・変更するとき

## Do not read this when
- session の状態値やライフサイクルの定義だけを確認したいとき
- Codex exec の共通規則や conflict resolution prompt の仕様だけを確認したいとき
- session join 以外のサブコマンドの実装を調査するとき

## hash
- 2a668d45349607298708204de853611c64551a53cce9cb605ac705522ff40a8e
