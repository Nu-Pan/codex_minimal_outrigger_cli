# `__init__.py`

## Summary
- session サブコマンド実装を収める Python package の入口であることだけを示す package 初期化ファイル。本文は package の役割を示す docstring のみで、具体的な処理や公開 API は持たない。

## Read this when
- session サブコマンド実装群の package 境界や、package 自体に初期化処理があるかを確認したいとき。
- session サブコマンド関連の import 経路を調べる前に、package 直下で定義されている内容の有無を確認したいとき。

## Do not read this when
- 個別の session サブコマンドの挙動、引数、入出力、制御ロジックを調べたいとき。
- session サブコマンド以外の CLI 実装を調べたいとき。

## hash
- a2616b13a1c260f66ad6dfda2f7821fc573b581179e92bbad014a023d5958042

# `abandon.py`

## Summary
- active な session branch 上で `session abandon` を実行し、home branch へ切り替えたうえで session state を `abandoned` に更新し、session branch だけを削除する CLI サブコマンド実装。
- 実行時ラッパー、事前条件検証、git ignore/index 状態の準備、cleanup 失敗時の state・branch rollback、成功時の利用者向け出力を扱う。

## Read this when
- `cmoc session abandon` の実行条件、状態遷移、branch 切り替え、session branch 削除、失敗時 rollback を確認・変更したいとき。
- session abandon がどの runtime helper を使い、どの順序で worktree clean 確認、home branch 存在確認、state 書き込み、branch 削除を行うか調べたいとき。
- session abandon のエラーメッセージ、cleanup 失敗時の詳細情報、成功時の CLI 出力を確認・変更したいとき。

## Do not read this when
- session abandon の正本仕様を確認したいだけなら、対応する oracle doc を読む。
- session abandon 以外の session サブコマンドや共通 runtime helper の仕様・実装を調べたい場合は、それぞれの対象へ直接進む。
- 生成済み build 配下ではなく編集対象の実装を変更したい場合は、対応する source 配下の実装を読む。

## hash
- e8792415573dda32702ca7f56c0363674bee0c83d42c9b2c7eddc11b8bb8e39d

# `fork.py`

## Summary
- `cmoc session fork` の実行処理を担う実装ファイル。CLI runtime 経由で fork 本体を呼び出し、通常の local branch から管理対象 session branch を作成し、session state を保存して結果を表示する。
- 現在 branch の検証、clean worktree 要求、既存 active session の検出、一意な session-id 生成、session branch 作成、session state 初期化までの一連の制御を扱う。

## Read this when
- `cmoc session fork` の挙動、失敗条件、出力内容、または session branch 作成処理を確認・変更したいとき。
- session-id の生成衝突、既存 active session、managed branch 上での禁止、clean worktree 要求など、fork 開始前の検証ロジックを調べたいとき。
- session fork が作成する state file の初期値や、home branch/start commit の記録処理を確認したいとき。

## Do not read this when
- session fork 以外の session 操作を調べたいとき。join、abandon など該当する別の subcommand 実装へ進む方がよい。
- session state のデータ構造そのものや state file path の規則を調べたいとき。このファイルはそれらを利用する側であり、定義元を読む方が直接的。
- CLI runtime、git command wrapper、branch 判定、worktree 検証などの共通 helper の詳細を調べたいとき。このファイルは呼び出し側に留まる。

## hash
- 5e18dd55b0b201249fadfa3b37594b06e52030b37c4d27622f18755fac7b2096

# `join.py`

## Summary
- `session join` サブコマンドの実行本体を担い、active session branch を session home branch へ merge し、状態更新、session branch 削除判定、ユーザー向け結果出力までを扱う。
- merge conflict 発生時には Codex CLI へ解消を依頼し、conflict marker 残存確認、unmerged path 確認、merge commit 作成までを制御する。

## Read this when
- `cmoc session join` の事前条件、merge 手順、状態遷移、出力内容を確認または変更したいとき。
- session join 中の merge conflict 解消フロー、Codex CLI 呼び出し、conflict 対象ファイルの扱いを確認または変更したいとき。
- session branch の削除可否判定、削除失敗時 warning、post-precondition failure の stderr 報告を確認したいとき。
- conflict marker 検出ロジック、特に Git の conflict-marker-size を考慮した判定を確認または変更したいとき。

## Do not read this when
- session join 以外の session サブコマンドを調べたいとき。
- CLI runtime 共通処理、git 実行 wrapper、state 読み書き、worktree clean 判定そのものを調べたいとき。
- Codex CLI に渡す conflict 解消プロンプトや parameter の組み立て内容だけを調べたいとき。
- INDEX 生成や indexing preflight の仕組みそのものを調べたいとき。

## hash
- 3954acd06c08ebdafcb234136542fc75d68aadfe0f783b4ea157641247a6016c
