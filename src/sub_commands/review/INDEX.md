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
- review oracle サブコマンドの実行入口と制御フローを担う実装。active session branch 上で scope を検証し、isolated review worktree を作成して oracle 対象の列挙、review loop、INDEX 変更の commit と merge、worktree と branch の後始末、成功・失敗時の report 出力までを統括する。
- review oracle に関係する対象列挙、review loop、INDEX 反映、report rendering などの実処理は別モジュールへ委譲し、この対象はそれらを CLI runtime 上で順序付けて実行するオーケストレーション層として読む。

## Read this when
- review oracle サブコマンドがどの前提条件で実行可能か、scope validation、active session branch 判定、clean worktree 要求、cmoc ignore 確保の流れを確認したいとき。
- review 用 worktree と一時 branch の作成、review loop の実行、INDEX 変更の commit と session branch への merge、後始末の順序や失敗時 report 生成を確認したいとき。
- review oracle 実行時にどの下位モジュールが呼ばれるか、対象列挙・findings 生成・report 書き出し・merge conflict 関連処理への入口をたどりたいとき。
- CLI から review oracle を実行する際の command name、command argv、Codex exec callback の受け渡し、preflight 実行位置を確認したいとき。

## Do not read this when
- oracle file の列挙条件や scope ごとの対象選択ロジック自体を確認したいだけなら、review target 列挙を担う対象を直接読む。
- Codex による review loop の prompt、finding の生成・統合・merge operation 適用の詳細を確認したいだけなら、review loop を担う対象を直接読む。
- report の本文構成、finding section の描画、report ファイルへの書き出し形式を確認したいだけなら、review report を担う対象を直接読む。
- review 用 INDEX 変更の status 判定、commit、merge、conflict 解決の詳細を確認したいだけなら、review index 反映を担う対象を直接読む。

## hash
- 6668c5f93f455067d5d657c4a170265efd714d6b3cbe19c1dd55a34bcc49a9d1
