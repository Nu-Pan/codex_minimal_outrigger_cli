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
- review oracle サブコマンドの実行入口と全体制御を担う。active session branch と clean worktree を前提条件として検証し、isolated review worktree の作成、oracle 対象列挙、review loop 実行、INDEX 変更の commit/merge、作業用 worktree/branch の後始末、review report 出力までを接続する。
- review 対象列挙、review loop、report 描画、INDEX 競合解決などの個別処理は下位 module に委譲し、この対象はそれらを CLI runtime 上の一連の workflow として組み立てる位置づけである。

## Read this when
- review oracle サブコマンドの実行順序、前提条件、作業用 branch/worktree のライフサイクル、失敗時 report 出力を確認したいとき。
- oracle review workflow がどの下位 module を呼び出し、INDEX 変更の commit/merge と report 作成をどのタイミングで行うかを追いたいとき。
- 未コミット差分がある場合や active session branch 以外での実行を拒否する制御を確認したいとき。

## Do not read this when
- oracle file の列挙条件や scope ごとの対象選択だけを確認したいときは、review target 列挙を担う module を読む。
- review loop 内で Codex に渡す指示、finding の解釈、merge operation の適用だけを確認したいときは、review loop を担う module を読む。
- review report の文面、section 表現、report file の書き込み形式だけを確認したいときは、review report を担う module を読む。
- INDEX 変更の検出、commit、merge、競合解決の詳細だけを確認したいときは、review index 操作を担う module を読む。

## hash
- 6ec5af26c01ade97f16328fa10bdb21f6480824d061dc5c8776718ead3214b78
