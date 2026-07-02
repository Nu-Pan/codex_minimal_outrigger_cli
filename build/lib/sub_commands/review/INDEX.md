# `__init__.py`

## Summary
- review 系サブコマンド群をまとめる Python package の境界を示す初期化ファイル。本文は package の所属領域だけを示し、具体的な command 挙動や実装責務は下位 module 側に委ねる。

## Read this when
- review 系サブコマンドがどの package に属するかを確認したいとき。
- review 系サブコマンド領域の package 境界だけを確認し、具体的な処理内容までは不要なとき。

## Do not read this when
- review 系サブコマンドの具体的な CLI 挙動、入出力、制御処理を調べたいとき。その場合は実処理を持つ下位 module を読む。
- review 以外のサブコマンド領域を調べたいとき。

## hash
- 6eae64139b4951465b5b7ea5834aa77b1eeeaf892115aeaac7cbf14deb7ea1e2

# `oracle.py`

## Summary
- review oracle サブコマンドの公開実行関数と実体処理をまとめる。CLI 共通実行ラッパーを通じて scope を検証し、active session branch・clean worktree などの前提を確認したうえで、隔離された review worktree を作成して oracle 対象列挙、レビュー実行、INDEX 変更コミット、必要時のマージ、レポート出力、後始末を統括する。
- レビュー対象列挙、レビュー loop、レポート描画・保存、review branch の merge/conflict 補助などは下位モジュールから再公開され、この場所は review oracle ワークフロー全体の入口として位置づけられる。

## Read this when
- review oracle コマンドの実行順序、事前条件、scope の扱い、review worktree・review branch の作成と削除、レポート出力のタイミングを確認したいとき。
- review oracle の失敗時にもレポートを出してから例外を再送出する制御や、INDEX 変更がある場合だけ review branch を merge する制御を変更・確認したいとき。
- review oracle 関連の helper がどのモジュールから集約・再公開され、コマンド本体からどの順で呼ばれるかを追いたいとき。

## Do not read this when
- 個別の oracle file 列挙条件や scope ごとの対象選定ロジックだけを確認したい場合は、対象列挙を担う下位モジュールを直接読む。
- レビュー loop 内で Codex 実行結果をどう扱うか、finding をどう merge 操作へ変換するかだけを確認したい場合は、loop 処理を担う下位モジュールを読む。
- レポート本文の表示形式、finding section の描画、出力先パスの組み立てだけを確認したい場合は、レポート処理を担う下位モジュールを読む。

## hash
- 6668c5f93f455067d5d657c4a170265efd714d6b3cbe19c1dd55a34bcc49a9d1
