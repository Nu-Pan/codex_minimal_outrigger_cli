# `__init__.py`

## Summary
- review 系サブコマンド群の package 境界を示す最小の package 初期化モジュール。
- 具体的な処理や公開 API は持たず、この階層が review 系サブコマンドのまとまりであることだけを表す。

## Read this when
- review 系サブコマンド群の package 境界そのものを確認したいとき。
- この階層が review 系サブコマンド用の Python package として扱われる根拠を確認したいとき。

## Do not read this when
- review 系サブコマンドの具体的な CLI 挙動、引数、出力、制御フローを調べたいとき。
- review 系サブコマンド内の個別機能や実装詳細を調べたいとき。
- package 初期化時の import、副作用、公開シンボルを調べたいとき。ただし現在内容からはそのような責務は読み取れない。

## hash
- 6eae64139b4951465b5b7ea5834aa77b1eeeaf892115aeaac7cbf14deb7ea1e2

# `oracle.py`

## Summary
- review oracle コマンドの実行入口と全体制御を担う。active session branch の検証、oracle file 以外の未コミット差分の拒否、isolated review worktree の作成、対象 oracle file の列挙、review loop 実行、INDEX 変更の commit/merge、report 出力、worktree と branch の後始末をまとめる。
- review oracle に必要な下位処理を他モジュールから集約して公開し、実際の差分検出・対象列挙・review loop・report 描画などの詳細実装へ進む入口になる。

## Read this when
- review oracle コマンドの開始条件、実行順序、失敗時の report 出力、cleanup の責務を確認したいとき。
- active session branch 上でのみ動く制約や、oracle file 以外の未コミット差分を拒否する挙動を調べるとき。
- 未コミットの oracle 変更を review worktree に snapshot commit してから review する流れを変更または検証するとき。
- review 結果による INDEX 変更を review branch に commit し、必要に応じて session branch へ merge する制御を追うとき。
- review oracle 関連の対象列挙、review loop、report、INDEX merge 処理のどの下位モジュールを読むべきか判断したいとき。

## Do not read this when
- oracle file の列挙条件や scope ごとの対象選択だけを確認したい場合は、対象列挙の実装へ直接進む。
- review loop 内で Codex に渡す内容、finding の解釈、修正適用の詳細を確認したい場合は、review loop の実装へ直接進む。
- review report の表示文面、section 描画、report file の書き込み形式だけを確認したい場合は、report 生成の実装へ直接進む。
- INDEX 変更の conflict 解決、review branch の merge、worktree status path の詳細だけを確認したい場合は、INDEX review 操作の実装へ直接進む。
- 汎用の git 実行、worktree 作成削除、状態読み込み、config 読み込みの挙動だけを確認したい場合は、runtime 側の実装へ直接進む。

## hash
- 7d7dd0de0368a9e287777a209f912cffd9942ac7ac01f1e2cee442a68619f2f4
